"""IQ Analysis screen. Separate from the cognitive-radio channel mission."""

from __future__ import annotations

import html

import altair as alt
import pandas as pd
import streamlit as st

from cr_sim.iq_analysis import analyse_capture, picture, synthesize, train_emission_classifier

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


def _stable_hops(rows: list[dict]) -> list[dict]:
    """Drop one-hit spectral splatter. Keep a lone peak when nothing repeats."""
    kept = [row for row in rows if int(row["hits"]) >= 2]
    if kept:
        return kept
    return rows[:1]


def _chips(values: list[str]) -> str:
    if not values:
        return "<span class='iq-empty'>None</span>"
    return "".join(f"<span class='iq-chip'>{html.escape(value)}</span>" for value in values)


def _table(headers: list[str], rows: list[list[str]], numeric: set[int]) -> str:
    head = "".join(
        f"<th class='{'num' if i in numeric else 'txt'}'>{html.escape(name)}</th>"
        for i, name in enumerate(headers)
    )
    body = []
    for row in rows:
        cells = []
        for index, value in enumerate(row):
            align = "num" if index in numeric else "txt"
            cells.append(f"<td class='{align}'>{value}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    return (
        "<table class='iq-table'><thead><tr>"
        + head
        + "</tr></thead><tbody>"
        + "".join(body)
        + "</tbody></table>"
    )


def _card(title: str, body: str) -> str:
    return (
        "<div class='iq-card'>"
        f"<div class='iq-card-title'>{html.escape(title)}</div>"
        f"<div class='iq-card-body'>{body}</div>"
        "</div>"
    )


def _css(dark: bool) -> str:
    if dark:
        card, banner, text, line, chip_bg, zebra, note = (
            "#132536",
            "#1a3348",
            "#e8eef3",
            "#2a4256",
            "#1e3d56",
            "rgba(255,255,255,0.04)",
            "#d5e2ec",
        )
    else:
        card, banner, text, line, chip_bg, zebra, note = (
            "#ffffff",
            "#e7eef5",
            "#102033",
            "#d0dbe6",
            "#e3edf6",
            "#f4f8fb",
            "#1c3348",
        )
    return f"""
    <style>
    .iq-card {{
      background: {card};
      border: 1px solid {line};
      border-radius: 10px;
      margin: 0.35rem 0 0.8rem 0;
      overflow: hidden;
    }}
    .iq-card-title {{
      background: {banner};
      color: {text};
      font-weight: 700;
      font-size: 0.98rem;
      letter-spacing: 0.01em;
      padding: 0.55rem 0.85rem;
      border-bottom: 1px solid {line};
    }}
    .iq-card-body {{ padding: 0.65rem 0.85rem 0.8rem 0.85rem; color: {text}; }}
    .iq-table {{ width: 100%; border-collapse: collapse; font-size: 0.92rem; color: {text}; }}
    .iq-table th {{
      text-align: left;
      font-weight: 700;
      padding: 0.4rem 0.45rem;
      border-bottom: 1px solid {line};
      color: {text};
    }}
    .iq-table th.num {{ text-align: right; }}
    .iq-table td {{ padding: 0.38rem 0.45rem; border-bottom: 1px solid {line}; vertical-align: top; }}
    .iq-table tbody tr:nth-child(even) {{ background: {zebra}; }}
    .iq-table td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
    .iq-table td.txt {{ text-align: left; }}
    .iq-chip {{
      display: inline-block;
      margin: 0.12rem 0.28rem 0.12rem 0;
      padding: 0.12rem 0.45rem;
      border-radius: 999px;
      background: {chip_bg};
      border: 1px solid {line};
      color: {text};
      font-size: 0.86rem;
    }}
    .iq-empty {{ color: {note}; }}
    .iq-note {{ color: {note}; font-size: 0.92rem; line-height: 1.45; margin: 0; }}
    </style>
    """


def _charts(picture_data: dict, known_khz: list[float], dark: bool) -> tuple[alt.Chart, alt.Chart]:
    fg = "#e8eef3" if dark else "#102033"
    grid = "#2a4256" if dark else "#d0dbe6"
    spectrum = pd.DataFrame(
        {"Frequency (kHz)": picture_data["freq_khz"], "Power (dB)": picture_data["spectrum_db"]}
    )
    spec = (
        alt.Chart(spectrum)
        .mark_area(line={"color": "#3d8bfd"}, color="rgba(61, 139, 253, 0.35)")
        .encode(
            x=alt.X("Frequency (kHz):Q", title="Frequency (kHz)"),
            y=alt.Y("Power (dB):Q", title="Power (dB above noise)"),
        )
        .properties(height=220, title="Spectrum")
    )
    if known_khz:
        rules = pd.DataFrame({"Frequency (kHz)": known_khz})
        spec = spec + alt.Chart(rules).mark_rule(color="#e25b45", strokeDash=[4, 3]).encode(
            x="Frequency (kHz):Q"
        )
    times = picture_data["time_ms"]
    freqs = picture_data["freq_khz"]
    image = picture_data["image_db"]
    # Keep the strip readable: one row per FFT bin, one column per time step.
    strip_rows = []
    for t_i, t_ms in enumerate(times):
        for f_i, f_khz in enumerate(freqs):
            strip_rows.append(
                {"Time (ms)": float(t_ms), "Frequency (kHz)": float(f_khz), "Power (dB)": float(image[t_i, f_i])}
            )
    strip = (
        alt.Chart(pd.DataFrame(strip_rows))
        .mark_rect()
        .encode(
            x=alt.X("Time (ms):Q", title="Time (ms)"),
            y=alt.Y("Frequency (kHz):Q", title="Frequency (kHz)"),
            color=alt.Color(
                "Power (dB):Q",
                title="Power (dB)",
                scale=alt.Scale(scheme="inferno", domain=[0, 30]),
            ),
            tooltip=["Time (ms)", "Frequency (kHz)", "Power (dB)"],
        )
        .properties(height=220, title="Frequency over time")
    )
    themed = []
    for chart in (spec, strip):
        themed.append(
            chart.configure(background="transparent")
            .configure_axis(labelColor=fg, titleColor=fg, gridColor=grid, labelFontSize=11, titleFontSize=12)
            .configure_title(color=fg, fontSize=14, anchor="start")
            .configure_legend(labelColor=fg, titleColor=fg)
            .configure_view(strokeWidth=0)
        )
    return themed[0], themed[1]


def _spectrum_and_strip(picture_data: dict, known_khz: list[float], dark: bool) -> None:
    spectrum, strip = _charts(picture_data, known_khz, dark)
    left, right = st.columns(2)
    with left:
        st.altair_chart(spectrum, use_container_width=True)
    with right:
        st.altair_chart(strip, use_container_width=True)


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

    if run or st.session_state.get("iq_signature") != signature or "iq_picture" not in st.session_state:
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
        st.session_state.iq_picture = picture(capture.iq, capture.fs_hz)

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

    dark = st.session_state.get("theme_mode", "Dark") == "Dark"
    _spectrum_and_strip(st.session_state.iq_picture, truth.frequencies_khz, dark)

    hops = _stable_hops(estimate.hop_rows)
    known_freqs = [f"{value:.2f}" for value in truth.frequencies_khz]
    est_freqs = [f"{row['frequency_khz']:.2f}" for row in hops]

    def _pair(label: str, known: str, estimated: str, numeric: bool) -> list[str]:
        kind = "num" if numeric else "txt"
        return [
            f"<td class='txt'>{html.escape(label)}</td>",
            f"<td class='{kind}'>{known}</td>",
            f"<td class='{kind}'>{estimated}</td>",
        ]

    threat_rows = [
        _pair("Class", html.escape(truth.kind), html.escape(estimate.kind_rule), False),
        _pair("Frequency (kHz)", _chips(known_freqs), _chips(est_freqs), False),
        _pair("Bandwidth (Hz)", f"{truth.bandwidth_hz:.0f}", f"{estimate.bandwidth_hz:.0f}", True),
        _pair("Modulation", html.escape(truth.modulation), html.escape(estimate.modulation), False),
        _pair("SNR (dB)", f"{truth.snr_db:.1f}", f"{estimate.snr_db:.1f}", True),
        _pair("Start (ms)", f"{truth.start_ms:.2f}", f"{estimate.start_ms:.2f}", True),
        _pair("Duration (ms)", f"{truth.duration_ms:.2f}", f"{estimate.duration_ms:.2f}", True),
        _pair("DOA", "Not measured", "Not measured", False),
    ]
    threat_html = (
        "<table class='iq-table'><thead><tr>"
        "<th>Field</th><th>Known Capture</th><th>Estimate</th>"
        "</tr></thead><tbody>"
        + "".join("<tr>" + "".join(cells) + "</tr>" for cells in threat_rows)
        + "</tbody></table>"
    )

    recommend = ""
    if estimate.decision == "RECOMMEND":
        recommend = (
            "<p class='iq-note'>"
            f"Recommendation record: {estimate.frequency_khz:.2f} kHz, "
            f"bandwidth {estimate.bandwidth_hz:.0f} Hz, "
            f"from {estimate.start_ms:.2f} ms for {estimate.duration_ms:.2f} ms. "
            "This is a record only. Nothing is transmitted."
            "</p>"
        )

    if hops:
        hop_html = _table(
            ["Frequency (kHz)", "Hits", "Dwell (ms)", "Last (ms)"],
            [
                [
                    f"{row['frequency_khz']:.2f}",
                    str(int(row["hits"])),
                    f"{row['dwell_ms']:.2f}",
                    f"{row['last_ms']:.2f}",
                ]
                for row in hops
            ],
            {0, 1, 2, 3},
        )
    else:
        hop_html = "<p class='iq-note'>No occupied frequencies.</p>"

    if estimate.burst_rows:
        burst_html = _table(
            ["Start (ms)", "Duration (ms)", "Frequency (kHz)", "Bandwidth (Hz)"],
            [
                [
                    f"{row['start_ms']:.2f}",
                    f"{row['duration_ms']:.2f}",
                    f"{row['frequency_khz']:.2f}",
                    f"{row['bandwidth_hz']:.0f}",
                ]
                for row in estimate.burst_rows
            ],
            {0, 1, 2, 3},
        )
    else:
        burst_html = "<p class='iq-note'>No burst runs.</p>"

    st.markdown(_css(dark), unsafe_allow_html=True)
    st.markdown(_card("Threat Record", threat_html + recommend), unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        st.markdown(_card("Hop Set", hop_html), unsafe_allow_html=True)
    with right:
        st.markdown(_card("Bursts", burst_html), unsafe_allow_html=True)

    with st.expander("About this measurement"):
        st.markdown(
            "The IQ classifier is trained only on these synthetic captures, and the accuracy figure is from a held-out split. "
            "It is not the cognitive-radio channel network. "
            "A high score means these three synthetic families are easy to separate. It does not mean a field modulation classifier is finished. "
            "Frequency is reported on a 1.56 kHz grid. One-hit bins are left out of the frequency tags so noise splatter is not listed as a hop. "
            "Direction of arrival is not measured on a single channel. No exciter is armed."
        )
