"""IQ Analysis screen. Separate from the cognitive-radio channel mission."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from cr_sim.iq_analysis import analyse_capture, synthesize, train_emission_classifier

SCENARIOS = {
    "Fixed tone": "FIXED",
    "1 ms burst": "BURST",
    "Hopper": "HOPPER",
}


@st.cache_resource(show_spinner=False)
def _classifier():
    return train_emission_classifier(n_per_class=16, seed=7)


def _protected_list(text: str) -> list[float]:
    out: list[float] = []
    for part in text.replace(";", ",").split(","):
        part = part.strip()
        if not part:
            continue
        try:
            out.append(float(part))
        except ValueError:
            continue
    return out


def render_iq_analysis() -> None:
    st.sidebar.markdown("### IQ capture")
    st.sidebar.caption(
        "Offline complex baseband at 200 kHz. This is not an 80 MHz live stream, and it does not arm an exciter."
    )
    scenario = st.sidebar.radio("Known capture", list(SCENARIOS), key="iq_scenario")
    seed = int(st.sidebar.number_input("Capture seed", min_value=0, max_value=999999, value=1, step=1, key="iq_seed"))
    snr = float(st.sidebar.slider("True SNR (dB)", 8.0, 20.0, 15.0, 1.0, key="iq_snr"))
    threshold = float(
        st.sidebar.slider("Confidence threshold", 0.5, 0.95, 0.70, 0.05, key="iq_threshold")
    )
    protected_text = st.sidebar.text_input(
        "Protected frequencies (kHz)",
        value="",
        help="Comma-separated. A match within 2 kHz forces HOLD.",
        key="iq_protected",
    )
    run = st.sidebar.button("Analyse capture", type="primary", use_container_width=True, key="iq_run")
    signature = (scenario, seed, snr, threshold, protected_text.strip())

    if run or st.session_state.get("iq_signature") != signature:
        with st.spinner("Measuring this capture. The IQ classifier is trained once per session on a held-out split."):
            clf = _classifier()
            capture = synthesize(SCENARIOS[scenario], seed=seed, snr_db=snr)
            estimate = analyse_capture(
                capture,
                clf,
                protected_khz=_protected_list(protected_text),
                confidence_threshold=threshold,
            )
        st.session_state.iq_signature = signature
        st.session_state.iq_estimate = estimate
        st.session_state.iq_truth = capture.truth

    estimate = st.session_state.iq_estimate
    truth = st.session_state.iq_truth

    if estimate.decision == "RECOMMEND":
        st.success(f"RECOMMEND — {estimate.decision_reason}")
    elif estimate.decision == "HOLD":
        st.warning(f"HOLD — {estimate.decision_reason}")
    else:
        st.info(f"TRACK — {estimate.decision_reason}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rule class", estimate.kind_rule)
    c2.metric("IQ classifier", f"{estimate.kind_ml} ({estimate.ml_confidence:.2f})")
    c3.metric("Held-out test accuracy", f"{estimate.test_accuracy:.2f}")
    c4.metric("Direction of arrival", estimate.doa)

    if estimate.kind_rule != estimate.kind_ml:
        st.error("The rule baseline and the IQ classifier disagree. The gate holds.")

    st.markdown("**Threat record against the known capture**")
    record = pd.DataFrame(
        [
            {
                "Field": "Class",
                "Known capture": truth.kind,
                "Estimate": estimate.kind_rule,
            },
            {
                "Field": "Frequency (kHz)",
                "Known capture": ", ".join(str(f) for f in truth.frequencies_khz),
                "Estimate": ", ".join(str(f) for f in estimate.frequencies_khz) or "none",
            },
            {
                "Field": "Bandwidth (Hz)",
                "Known capture": f"{truth.bandwidth_hz:.0f}",
                "Estimate": f"{estimate.bandwidth_hz:.0f}",
            },
            {
                "Field": "Modulation",
                "Known capture": truth.modulation,
                "Estimate": estimate.modulation,
            },
            {
                "Field": "SNR (dB)",
                "Known capture": f"{truth.snr_db:.1f}",
                "Estimate": f"{estimate.snr_db:.1f}",
            },
            {
                "Field": "Start (ms)",
                "Known capture": f"{truth.start_ms:.2f}",
                "Estimate": f"{estimate.start_ms:.2f}",
            },
            {
                "Field": "Duration (ms)",
                "Known capture": f"{truth.duration_ms:.2f}",
                "Estimate": f"{estimate.duration_ms:.2f}",
            },
            {
                "Field": "DOA",
                "Known capture": "not measured",
                "Estimate": estimate.doa,
            },
        ]
    )
    st.dataframe(record, use_container_width=True, hide_index=True)

    if estimate.decision == "RECOMMEND":
        st.markdown(
            f"**Recommendation record:** {estimate.frequency_khz:.2f} kHz, "
            f"bandwidth {estimate.bandwidth_hz:.0f} Hz, "
            f"from {estimate.start_ms:.2f} ms for {estimate.duration_ms:.2f} ms. "
            "This is a record only. Nothing is transmitted."
        )

    left, right = st.columns(2)
    with left:
        st.markdown("**Hop set** (capped at 1000)")
        if estimate.hop_rows:
            st.dataframe(pd.DataFrame(estimate.hop_rows), use_container_width=True, hide_index=True)
        else:
            st.caption("No occupied frequencies.")
    with right:
        st.markdown("**Bursts**")
        if estimate.burst_rows:
            st.dataframe(pd.DataFrame(estimate.burst_rows), use_container_width=True, hide_index=True)
        else:
            st.caption("No burst runs.")

    st.caption(
        "The IQ classifier is trained only on these synthetic captures, with a held-out test split. "
        "It is not the cognitive-radio channel network. "
        "A perfect score here means the three synthetic families are easy to separate, not that a field modulation classifier is finished. "
        "Frequency is reported on a 1.56 kHz FFT grid."
    )
