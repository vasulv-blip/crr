"""Offline IQ analysis for the smart-jammer threat record.

This path is separate from the cognitive-radio channel recommender.
It estimates frequency, bandwidth, class, SNR, and noise from a short
complex baseband capture, then returns track / recommend / hold.
It does not command an exciter.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

FS_HZ = 200_000.0
CAPTURE_S = 0.04
WINDOW = 128
HOP = 64
MAX_HOP_SET = 1000
CLASSES = ("FIXED", "BURST", "HOPPER")


@dataclass
class EmissionTruth:
    kind: str
    frequencies_khz: list[float]
    bandwidth_hz: float
    modulation: str
    start_ms: float
    duration_ms: float
    snr_db: float


@dataclass
class Capture:
    iq: np.ndarray
    fs_hz: float
    truth: EmissionTruth


@dataclass
class ThreatEstimate:
    frequency_khz: float
    frequencies_khz: list[float]
    bandwidth_hz: float
    modulation: str
    kind_rule: str
    kind_ml: str
    ml_confidence: float
    snr_db: float
    noise_power: float
    start_ms: float
    duration_ms: float
    doa: str
    stable: bool
    decision: str
    decision_reason: str
    hop_rows: list[dict]
    burst_rows: list[dict]
    features: dict
    test_accuracy: float


def _noise(rng: np.random.Generator, n: int) -> np.ndarray:
    return (rng.normal(size=n) + 1j * rng.normal(size=n)) / np.sqrt(2.0)


def _tone(n: int, fs: float, freq_hz: float, amp: float, phase: float) -> np.ndarray:
    t = np.arange(n) / fs
    return amp * np.exp(1j * (2.0 * np.pi * freq_hz * t + phase))


def synthesize(kind: str, seed: int = 1, snr_db: float = 15.0, fs_hz: float = FS_HZ) -> Capture:
    """Build a known capture: fixed tone, 1 ms burst, or a short hopper."""
    rng = np.random.default_rng(seed)
    n = int(fs_hz * CAPTURE_S)
    iq = _noise(rng, n)
    amp = 10.0 ** (snr_db / 20.0)
    kind = kind.upper()

    if kind == "FIXED":
        freq = float(rng.uniform(8_000.0, 30_000.0))
        iq += _tone(n, fs_hz, freq, amp, float(rng.uniform(0, 2 * np.pi)))
        truth = EmissionTruth(
            kind="FIXED",
            frequencies_khz=[round(freq / 1000.0, 2)],
            bandwidth_hz=fs_hz / WINDOW,
            modulation="unmodulated tone",
            start_ms=0.0,
            duration_ms=CAPTURE_S * 1000.0,
            snr_db=snr_db,
        )
    elif kind == "BURST":
        freq = float(rng.uniform(8_000.0, 30_000.0))
        dur_s = 0.001
        start = int(0.015 * fs_hz)
        length = int(dur_s * fs_hz)
        iq[start : start + length] += _tone(length, fs_hz, freq, amp, float(rng.uniform(0, 2 * np.pi)))
        truth = EmissionTruth(
            kind="BURST",
            frequencies_khz=[round(freq / 1000.0, 2)],
            bandwidth_hz=fs_hz / WINDOW,
            modulation="unmodulated tone",
            start_ms=15.0,
            duration_ms=1.0,
            snr_db=snr_db,
        )
    elif kind == "HOPPER":
        plan = [6_000.0, 14_000.0, 22_000.0, 30_000.0]
        dwell = int(0.002 * fs_hz)
        phase = float(rng.uniform(0, 2 * np.pi))
        for i in range(0, n, dwell):
            freq = plan[(i // dwell) % len(plan)]
            m = min(dwell, n - i)
            iq[i : i + m] += _tone(m, fs_hz, freq, amp, phase)
        truth = EmissionTruth(
            kind="HOPPER",
            frequencies_khz=[round(f / 1000.0, 2) for f in plan],
            bandwidth_hz=fs_hz / WINDOW,
            modulation="unmodulated tone",
            start_ms=0.0,
            duration_ms=CAPTURE_S * 1000.0,
            snr_db=snr_db,
        )
    else:
        raise ValueError(f"Unknown kind {kind}")

    return Capture(iq=iq.astype(np.complex64), fs_hz=fs_hz, truth=truth)


def _window_peaks(iq: np.ndarray, fs_hz: float) -> list[dict]:
    rows: list[dict] = []
    if len(iq) < WINDOW:
        return rows
    window = np.hanning(WINDOW)
    for start in range(0, len(iq) - WINDOW + 1, HOP):
        spec = np.fft.fftshift(np.fft.fft(iq[start : start + WINDOW] * window))
        power = (np.abs(spec) ** 2) / WINDOW
        noise = float(np.median(power))
        peak_i = int(np.argmax(power))
        peak = float(power[peak_i])
        freqs = np.fft.fftshift(np.fft.fftfreq(WINDOW, d=1.0 / fs_hz))
        above = power >= max(peak * 0.25, noise * 4.0)
        bandwidth_hz = float(np.count_nonzero(above) * (fs_hz / WINDOW))
        rows.append(
            {
                "t_ms": 1000.0 * start / fs_hz,
                "freq_hz": float(freqs[peak_i]),
                "peak": peak,
                "noise": noise,
                "occupied": peak > noise * 12.0,
                "bandwidth_hz": bandwidth_hz,
            }
        )
    return rows


def _quantize_hz(freq_hz: float, fs_hz: float) -> float:
    bin_hz = fs_hz / WINDOW
    return round(freq_hz / bin_hz) * bin_hz


def measure(iq: np.ndarray, fs_hz: float) -> dict:
    """Rule baseline: energy, peak frequency, bandwidth, hop set, bursts."""
    rows = _window_peaks(iq, fs_hz)
    if not rows:
        return {
            "kind_rule": "NONE",
            "frequency_khz": 0.0,
            "frequencies_khz": [],
            "bandwidth_hz": 0.0,
            "modulation": "not resolved",
            "snr_db": 0.0,
            "noise_power": 0.0,
            "start_ms": 0.0,
            "duration_ms": 0.0,
            "hop_rows": [],
            "burst_rows": [],
            "features": {"duty": 0.0, "n_distinct": 0.0, "n_changes": 0.0, "longest_ms": 0.0, "bandwidth_hz": 0.0, "snr_db": 0.0},
        }

    occupied = [r for r in rows if r["occupied"]]
    noise_power = float(np.median([r["noise"] for r in rows]))
    duty = len(occupied) / len(rows)

    hop_counts: dict[float, dict] = {}
    changes = 0
    prev = None
    for r in occupied:
        q = _quantize_hz(r["freq_hz"], fs_hz)
        slot = hop_counts.setdefault(q, {"hits": 0, "last_ms": r["t_ms"], "dwell_ms": 0.0})
        slot["hits"] += 1
        slot["dwell_ms"] += 1000.0 * HOP / fs_hz
        slot["last_ms"] = r["t_ms"]
        if prev is not None and abs(q - prev) > (fs_hz / WINDOW) * 0.5:
            changes += 1
        prev = q

    hop_rows = [
        {
            "frequency_khz": round(freq / 1000.0, 2),
            "hits": slot["hits"],
            "dwell_ms": round(slot["dwell_ms"], 2),
            "last_ms": round(slot["last_ms"], 2),
        }
        for freq, slot in sorted(hop_counts.items(), key=lambda kv: -kv[1]["hits"])
    ][:MAX_HOP_SET]

    bursts: list[dict] = []
    run: list[dict] = []

    def _close_run() -> None:
        if not run:
            return
        bursts.append(
            {
                "start_ms": round(run[0]["t_ms"], 2),
                "duration_ms": round(1000.0 * HOP / fs_hz * len(run), 2),
                "frequency_khz": round(_quantize_hz(run[0]["freq_hz"], fs_hz) / 1000.0, 2),
                "bandwidth_hz": round(float(np.median([x["bandwidth_hz"] for x in run])), 1),
            }
        )

    for r in rows:
        if r["occupied"]:
            run.append(r)
        else:
            _close_run()
            run = []
    _close_run()

    if occupied:
        strongest = max(occupied, key=lambda r: r["peak"])
        freq_hz = _quantize_hz(strongest["freq_hz"], fs_hz)
        bandwidth_hz = float(np.median([r["bandwidth_hz"] for r in occupied]))
        start_ms = occupied[0]["t_ms"]
        duration_ms = occupied[-1]["t_ms"] + (1000.0 * HOP / fs_hz) - occupied[0]["t_ms"]
        noise_power = float(np.median([r["noise"] for r in rows]))
        sig_power = float(np.mean([r["peak"] for r in occupied]))
        spectral_db = 10.0 * np.log10(max(sig_power, 1e-12) / max(noise_power, 1e-12))
        # Remove FFT processing gain so the figure is near the time-domain SNR of the capture.
        snr_db = spectral_db - 10.0 * np.log10(WINDOW)
    else:
        snr_db = 0.0
        freq_hz = 0.0
        bandwidth_hz = 0.0
        start_ms = 0.0
        duration_ms = 0.0
        noise_power = float(np.median([r["noise"] for r in rows]))

    longest_ms = max((b["duration_ms"] for b in bursts), default=0.0)
    n_distinct = float(len(hop_counts))
    features = {
        "duty": float(duty),
        "n_distinct": n_distinct,
        "n_changes": float(changes),
        "longest_ms": float(longest_ms),
        "bandwidth_hz": float(bandwidth_hz),
        "snr_db": float(snr_db),
    }

    if duty < 0.25 and longest_ms <= 4.0 and longest_ms >= 0.4:
        kind_rule = "BURST"
    elif n_distinct >= 3 and changes >= 3 and duty > 0.4:
        kind_rule = "HOPPER"
    elif duty > 0.5 and n_distinct <= 2:
        kind_rule = "FIXED"
    elif n_distinct >= 3 and duty > 0.4:
        kind_rule = "HOPPER"
    elif duty < 0.35:
        kind_rule = "BURST"
    else:
        kind_rule = "FIXED"

    modulation = "unmodulated tone" if bandwidth_hz <= 2.5 * (fs_hz / WINDOW) else "not resolved"
    return {
        "kind_rule": kind_rule,
        "frequency_khz": round(freq_hz / 1000.0, 2),
        "frequencies_khz": [row["frequency_khz"] for row in hop_rows],
        "bandwidth_hz": round(bandwidth_hz, 1),
        "modulation": modulation,
        "snr_db": round(float(snr_db), 1),
        "noise_power": float(noise_power),
        "start_ms": round(float(start_ms), 2),
        "duration_ms": round(float(duration_ms), 2),
        "hop_rows": hop_rows,
        "burst_rows": bursts,
        "features": features,
    }


def _feature_vector(features: dict) -> np.ndarray:
    return np.array(
        [
            features["duty"],
            features["n_distinct"],
            features["n_changes"],
            features["longest_ms"],
            features["bandwidth_hz"],
            features["snr_db"],
        ],
        dtype=float,
    )


@dataclass
class EmissionClassifier:
    model: MLPClassifier
    scaler: StandardScaler
    test_accuracy: float
    n_train: int
    n_test: int

    def predict(self, features: dict) -> tuple[str, float]:
        x = self.scaler.transform(_feature_vector(features).reshape(1, -1))
        label = str(self.model.predict(x)[0])
        proba = self.model.predict_proba(x)[0]
        return label, float(np.max(proba))


def train_emission_classifier(n_per_class: int = 40, seed: int = 7) -> EmissionClassifier:
    """Train a small net on synthetic captures. Score is held-out test accuracy."""
    rng = np.random.default_rng(seed)
    xs: list[np.ndarray] = []
    ys: list[str] = []
    for kind in CLASSES:
        for i in range(n_per_class):
            cap = synthesize(kind, seed=int(rng.integers(0, 1_000_000)), snr_db=float(rng.uniform(10.0, 20.0)))
            measured = measure(cap.iq, cap.fs_hz)
            xs.append(_feature_vector(measured["features"]))
            ys.append(kind)
    x = np.vstack(xs)
    y = np.array(ys)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=seed, stratify=y
    )
    scaler = StandardScaler()
    x_train_s = scaler.fit_transform(x_train)
    x_test_s = scaler.transform(x_test)
    model = MLPClassifier(hidden_layer_sizes=(32, 16), activation="relu", solver="adam", max_iter=400, random_state=seed)
    model.fit(x_train_s, y_train)
    accuracy = float(model.score(x_test_s, y_test))
    return EmissionClassifier(
        model=model,
        scaler=scaler,
        test_accuracy=round(accuracy, 3),
        n_train=int(len(y_train)),
        n_test=int(len(y_test)),
    )


def picture(iq: np.ndarray, fs_hz: float) -> dict:
    """Spectrum and time-frequency image for the IQ screen. Frequencies in kHz."""
    window = np.hanning(WINDOW)
    frames: list[np.ndarray] = []
    times: list[float] = []
    for start in range(0, len(iq) - WINDOW + 1, HOP):
        spec = np.fft.fftshift(np.fft.fft(iq[start : start + WINDOW] * window))
        frames.append(np.abs(spec) ** 2)
        times.append(1000.0 * (start + WINDOW / 2.0) / fs_hz)
    power = np.vstack(frames)
    freqs_khz = np.fft.fftshift(np.fft.fftfreq(WINDOW, d=1.0 / fs_hz)) / 1000.0
    keep = (freqs_khz >= -45.0) & (freqs_khz <= 45.0)
    freqs_khz = freqs_khz[keep]
    power = power[:, keep]
    floor = float(np.median(power))
    spectrum_db = 10.0 * np.log10(np.maximum(power.mean(axis=0), 1e-12) / max(floor, 1e-12))
    image_db = np.clip(10.0 * np.log10(np.maximum(power, 1e-12) / max(floor, 1e-12)), 0.0, 30.0)
    return {
        "freq_khz": freqs_khz.astype(float),
        "spectrum_db": spectrum_db.astype(float),
        "time_ms": np.asarray(times, dtype=float),
        "image_db": image_db.astype(float),
    }


def gate(
    kind_rule: str,
    kind_ml: str,
    confidence: float,
    frequency_khz: float,
    protected_khz: list[float],
    confidence_threshold: float,
) -> tuple[str, str, bool]:
    """Track, recommend, or hold. Recommendation is a record, not an emission."""
    stable = kind_rule == kind_ml and kind_rule in CLASSES
    for protected in protected_khz:
        if abs(frequency_khz - float(protected)) <= 2.0:
            return "HOLD", "Frequency is on the protected list.", False
    if kind_rule == "NONE":
        return "TRACK", "No emission crossed the energy threshold.", False
    if not stable:
        return "HOLD", "Rule baseline and the IQ classifier disagree, so the class is not stable.", False
    if confidence < confidence_threshold:
        return "HOLD", "Confidence is below the threshold.", stable
    return (
        "RECOMMEND",
        "Class is stable and confidence is high enough to record a recommendation. No exciter is armed.",
        True,
    )


def analyse_capture(
    capture: Capture,
    classifier: EmissionClassifier,
    protected_khz: list[float] | None = None,
    confidence_threshold: float = 0.6,
) -> ThreatEstimate:
    measured = measure(capture.iq, capture.fs_hz)
    kind_ml, confidence = classifier.predict(measured["features"])
    decision, reason, stable = gate(
        measured["kind_rule"],
        kind_ml,
        confidence,
        measured["frequency_khz"],
        protected_khz or [],
        confidence_threshold,
    )
    return ThreatEstimate(
        frequency_khz=measured["frequency_khz"],
        frequencies_khz=measured["frequencies_khz"],
        bandwidth_hz=measured["bandwidth_hz"],
        modulation=measured["modulation"],
        kind_rule=measured["kind_rule"],
        kind_ml=kind_ml,
        ml_confidence=round(confidence, 3),
        snr_db=measured["snr_db"],
        noise_power=measured["noise_power"],
        start_ms=measured["start_ms"],
        duration_ms=measured["duration_ms"],
        doa="not measured",
        stable=stable,
        decision=decision,
        decision_reason=reason,
        hop_rows=measured["hop_rows"],
        burst_rows=measured["burst_rows"],
        features=measured["features"],
        test_accuracy=classifier.test_accuracy,
    )
