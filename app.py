"""
Cognitive Radio Software Simulation — professional demonstration UI.

Run from this directory:
    streamlit run app.py
"""

from __future__ import annotations

import html
from pathlib import Path
import sys

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cr_sim.models import DecisionMode, JamProfile, SimConfig
from cr_sim.orchestrator import Orchestrator

st.set_page_config(
    page_title="Cognitive Radio Simulation | eAge Innovations",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"]  {
  font-family: 'IBM Plex Sans', sans-serif;
  color: #e6edf2;
}
.stApp {
  background: linear-gradient(180deg, #0a1520 0%, #0f1f2e 45%, #122433 100%);
  color: #e6edf2;
}

/* Top Streamlit chrome */
header[data-testid="stHeader"] {
  background: #0b1824 !important;
  border-bottom: 1px solid #243647;
}
header[data-testid="stHeader"] * {
  color: #d7e2ea !important;
}
div[data-testid="stToolbar"] {
  background: #0b1824 !important;
}
div[data-testid="stDecoration"] {
  background: #0b1824 !important;
}
section[data-testid="stAppViewContainer"] > .main {
  background: transparent;
}
.block-container {
  padding-top: 2.4rem;
  padding-bottom: 2rem;
  max-width: 1400px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: #0b1824 !important;
  border-right: 1px solid #243647;
}
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
  color: #d7e2ea !important;
}

h1, h2, h3, h4, .stSubheader, .stCaption {
  font-family: 'IBM Plex Sans', sans-serif !important;
  letter-spacing: 0.02em;
  color: #f2f6f9 !important;
}
.stCaption, [data-testid="stCaptionContainer"] {
  color: #9bb0c0 !important;
}

/* Metrics */
div[data-testid="stMetric"] {
  background: #132536;
  border: 1px solid #2a4256;
  border-radius: 6px;
  padding: 0.45rem 0.65rem;
}
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
  color: #9bb0c0 !important;
  font-size: 0.72rem !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
  color: #f4f8fb !important;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.05rem !important;
  line-height: 1.2 !important;
}
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
  font-size: 0.7rem !important;
}

/* Buttons — dark surface, light text (fixes white-on-white) */
div.stButton > button,
button[kind="secondary"],
button[kind="primary"],
button[data-testid="baseButton-secondary"],
button[data-testid="baseButton-primary"] {
  background-color: #1a3348 !important;
  color: #eef4f8 !important;
  border: 1px solid #3d5a70 !important;
  border-radius: 6px !important;
}
div.stButton > button:hover,
button[kind="secondary"]:hover,
button[data-testid="baseButton-secondary"]:hover {
  background-color: #244560 !important;
  color: #ffffff !important;
  border-color: #5a84a0 !important;
}
button[kind="primary"],
button[data-testid="baseButton-primary"],
div.stButton > button[kind="primary"] {
  background-color: #2a5f7a !important;
  border: 1px solid #3d7ea0 !important;
  color: #ffffff !important;
}
section[data-testid="stSidebar"] div.stButton > button {
  background-color: #1a3348 !important;
  color: #eef4f8 !important;
  border: 1px solid #3d5a70 !important;
}

/* Inputs / selects / sliders */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="base-input"],
.stNumberInput input,
.stTextInput input,
.stMultiSelect [data-baseweb="select"] > div {
  background-color: #132536 !important;
  color: #e6edf2 !important;
  border-color: #2a4256 !important;
}
div[data-baseweb="popover"] {
  background-color: #132536 !important;
}
div[data-baseweb="menu"] li,
ul[role="listbox"] li {
  background-color: #132536 !important;
  color: #e6edf2 !important;
}
.stSlider label, .stSelectbox label, .stMultiSelect label, .stToggle label {
  color: #d7e2ea !important;
}

/* Dataframes / tables */
div[data-testid="stDataFrame"],
div[data-testid="stDataFrame"] > div,
div[data-testid="stDataFrameResizable"],
[data-testid="stTable"] {
  background-color: #132536 !important;
  border: 1px solid #2a4256 !important;
  border-radius: 6px;
  color: #e6edf2 !important;
}
div[data-testid="stDataFrame"] * {
  color: #e6edf2 !important;
}
div[data-testid="stDataFrame"] [role="grid"],
div[data-testid="stDataFrame"] [role="row"],
div[data-testid="stDataFrame"] [role="gridcell"],
div[data-testid="stDataFrame"] [role="columnheader"] {
  background-color: #132536 !important;
  color: #e6edf2 !important;
  border-color: #2a4256 !important;
}
iframe[title="st.data_editor.DataFrame"],
iframe[title="dataframe"] {
  background: #132536 !important;
}

.hero {
  border: 1px solid #2a4256;
  background: linear-gradient(135deg, #102032 0%, #163047 100%);
  border-radius: 8px;
  padding: 1.55rem 1.35rem 1.25rem 1.35rem;
  margin-top: 0.75rem;
  margin-bottom: 1.15rem;
}
.hero-kicker {
  color: #8fa6b8;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  margin: 0 0 0.55rem 0;
}
.hero-title {
  color: #f5f8fa;
  font-size: 1.55rem;
  font-weight: 650;
  margin: 0;
}
.hero-sub {
  color: #b7c7d4;
  margin-top: 0.35rem;
  font-size: 0.95rem;
}
.panel {
  background: #132536;
  border: 1px solid #2a4256;
  border-radius: 8px;
  padding: 0.95rem 1rem;
  margin-bottom: 0.85rem;
}
.panel-title {
  color: #9bb0c0;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 0.55rem;
}
.status-pill {
  display: inline-block;
  padding: 0.28rem 0.7rem;
  border-radius: 4px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid transparent;
}
.status-OK { background: #163528; color: #7dcea0; border-color: #2f6b4f; }
.status-DEGRADED_OK { background: #3a2f14; color: #e0c36a; border-color: #7a6528; }
.status-INCREASE_POWER { background: #3a2414; color: #e0a06a; border-color: #7a4a28; }
.status-ALL_BLOCKED { background: #3a1616; color: #e08a8a; border-color: #7a3030; }
.status-HOLD { background: #1d2a38; color: #a9bccb; border-color: #3a5166; }
.message-box {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.9rem;
  color: #dce7ef;
  background: #0e1c28;
  border: 1px solid #2a4256;
  border-radius: 6px;
  padding: 0.75rem 0.85rem;
  min-height: 3.2rem;
}
.ch-meta {
  margin-top: 0.45rem;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  color: #a7bac8;
  line-height: 1.35;
}
.footer-note {
  color: #7f94a5;
  font-size: 0.8rem;
  border-top: 1px solid #243647;
  margin-top: 1.2rem;
  padding-top: 0.8rem;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def _init_state() -> None:
    if "orch" not in st.session_state:
        cfg = SimConfig(n_channels=8, decision_mode=DecisionMode.HYBRID, hop_enabled=False)
        orch = Orchestrator(cfg)
        orch.train_ml(800)
        st.session_state.orch = orch
        st.session_state.last = orch.step()
        st.session_state.log = []


def _card_style(state: str, active: bool) -> str:
    bg = {
        "FREE": "linear-gradient(180deg,#143226 0%,#102231 75%)",
        "DEGRADED": "linear-gradient(180deg,#332b14 0%,#102231 75%)",
        "BLOCKED": "linear-gradient(180deg,#331818 0%,#102231 75%)",
    }.get(state, "#102231")
    border = {
        "FREE": "#2f6b4f",
        "DEGRADED": "#7a6528",
        "BLOCKED": "#7a3030",
    }.get(state, "#314859")
    if active:
        border = "#c4a35a"
    shadow = "inset 0 0 0 2px #c4a35a;" if active else ""
    return f"background:{bg};border:1px solid {border};{shadow}border-radius:6px;padding:0.7rem 0.65rem;min-height:108px;"


def _state_color(state: str) -> str:
    return {"FREE": "#7dcea0", "DEGRADED": "#e0c36a", "BLOCKED": "#e08a8a"}.get(state, "#d5e1ea")


def render_channel_map(observations: list[dict], tx_channel: int) -> None:
    """Render channel cards with Streamlit columns (avoids markdown HTML breakage)."""
    st.caption("FREE · DEGRADED · BLOCKED · gold border = active TX")
    per_row = 4
    for row_start in range(0, len(observations), per_row):
        row = observations[row_start : row_start + per_row]
        cols = st.columns(len(row))
        for col, o in zip(cols, row):
            state = o["state"]
            active = o["channel_id"] == tx_channel
            tx_line = "TX ACTIVE" if active else ""
            card = (
                f'<div style="{_card_style(state, active)}">'
                f'<div style="font-family:IBM Plex Mono,monospace;font-weight:600;color:#f0f5f8;">'
                f'CH{o["channel_id"]:02d}</div>'
                f'<div style="margin-top:0.35rem;font-size:0.78rem;font-weight:650;letter-spacing:0.06em;'
                f'color:{_state_color(state)};">{state}</div>'
                f'<div style="margin-top:0.45rem;font-family:IBM Plex Mono,monospace;font-size:0.72rem;'
                f'color:#a7bac8;line-height:1.35;">SINR {o["sinr_db"]:.1f} dB<br/>Jam {o["jam_power"]:.1f}<br/>{tx_line}</div>'
                f"</div>"
            )
            with col:
                if hasattr(st, "html"):
                    st.html(card)
                else:
                    st.markdown(card, unsafe_allow_html=True)


def _html_block(content: str) -> None:
    """Render a compact HTML block without markdown blank-line breakage."""
    compact = " ".join(line.strip() for line in content.splitlines() if line.strip())
    if hasattr(st, "html"):
        st.html(compact)
    else:
        st.markdown(compact, unsafe_allow_html=True)

def main() -> None:
    _init_state()
    orch: Orchestrator = st.session_state.orch

    st.markdown(
        """
        <div class="hero">
          <div class="hero-kicker">eAge Innovations — Software Demonstration</div>
          <div class="hero-title">Cognitive Radio Channel Selection under Jamming</div>
          <div class="hero-sub">
            Configurable channel simulation · measurement-based receiver judgement ·
            Cognitive Radio decision (rules / ML / hybrid) · adaptive hopping · power advice
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### Configuration")
        n_channels = st.select_slider("Number of channels (N)", options=[4, 6, 8, 12, 16], value=orch.config.n_channels)
        decision_mode = st.selectbox(
            "Decision engine",
            options=[m.value for m in DecisionMode],
            index=[m.value for m in DecisionMode].index(orch.config.decision_mode.value),
            help="RULES = deterministic baseline. ML = trained MLP. HYBRID = ML with safety rules.",
        )
        hop_enabled = st.toggle("Cognitive / adaptive hopping", value=orch.config.hop_enabled)
        jam_power = st.slider("Jam power", 5.0, 80.0, float(orch.config.jam_power), 1.0)
        t_good = st.slider("SINR FREE threshold (dB)", 5.0, 20.0, float(orch.config.t_good_db), 0.5)
        t_bad = st.slider("SINR BLOCKED threshold (dB)", -5.0, 8.0, float(orch.config.t_bad_db), 0.5)
        max_power = st.slider("Maximum TX power (dB)", 5.0, 30.0, float(orch.config.max_power_db), 1.0)
        seed = st.number_input("Seed", min_value=0, max_value=999999, value=int(orch.config.seed), step=1)

        apply_cfg = st.button("Apply configuration", use_container_width=True)
        if apply_cfg:
            cfg = SimConfig(
                n_channels=int(n_channels),
                jam_power=float(jam_power),
                t_good_db=float(t_good),
                t_bad_db=float(t_bad),
                max_power_db=float(max_power),
                seed=int(seed),
                hop_enabled=bool(hop_enabled),
                decision_mode=DecisionMode(decision_mode),
            )
            orch.reset(cfg)
            with st.spinner("Training ML recommender for current N..."):
                metrics = orch.train_ml(1000)
            st.session_state.last = orch.step()
            st.session_state.log = [f"Configuration applied. ML train accuracy={metrics.get('train_accuracy')}"]
            st.rerun()

        st.markdown("---")
        st.markdown("### Jam injection")
        profile = st.selectbox(
            "Jam profile",
            options=[p.value for p in JamProfile],
            index=0,
        )
        jam_channels = st.multiselect(
            "Target channels (spot / multi-spot)",
            options=list(range(orch.config.n_channels)),
            default=[0, 1] if orch.config.n_channels > 1 else [0],
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Apply jam", use_container_width=True):
                orch.set_jam(JamProfile(profile), jam_channels)
                st.session_state.last = orch.step()
                st.rerun()
        with c2:
            if st.button("Clear jam", use_container_width=True):
                orch.clear_jam()
                st.session_state.last = orch.step()
                st.rerun()

        st.markdown("---")
        st.markdown("### Run control")
        if st.button("Single step", type="primary", use_container_width=True):
            st.session_state.last = orch.step()
            st.rerun()
        n_auto = st.number_input("Auto steps", min_value=1, max_value=50, value=5, step=1)
        if st.button("Run auto steps", use_container_width=True):
            for _ in range(int(n_auto)):
                st.session_state.last = orch.step()
            st.rerun()
        if st.button("Reset simulation", use_container_width=True):
            orch.reset()
            orch.train_ml(800)
            st.session_state.last = orch.step()
            st.rerun()

    last = st.session_state.last
    resp = last.response

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Simulation step", f"{last.step}")
    m2.metric("Active TX channel", f"CH{last.tx_channel}")
    m3.metric("TX power", f"{last.tx_power_db:.1f} dB")
    m4.metric("Channels (N)", f"{orch.config.n_channels}")
    m5.metric("Jam profile", last.jam_profile)

    left, right = st.columns([1.35, 1.0], gap="large")

    with left:
        st.subheader("Channel map")
        render_channel_map(last.observations, last.tx_channel)

        df = pd.DataFrame(last.observations)[
            ["channel_id", "state", "sinr_db", "jam_power", "path_gain", "is_active_tx"]
        ].rename(
            columns={
                "channel_id": "Channel",
                "state": "State",
                "sinr_db": "SINR (dB)",
                "jam_power": "Jam power",
                "path_gain": "Path gain",
                "is_active_tx": "TX active",
            }
        )
        st.dataframe(df, use_container_width=True, hide_index=True, height=260)

    with right:
        status = html.escape(resp["status_code"])
        msg = html.escape(resp["message"])
        engine = html.escape(resp.get("engine", ""))
        action = html.escape(resp.get("action", ""))
        channels = ", ".join(f"CH{c}" for c in resp.get("channels", [])) or "—"
        hop = ", ".join(f"CH{c}" for c in last.hop_set) if orch.config.hop_enabled else "Disabled"
        power_advice = resp.get("power_advice_db")
        advice_txt = f"{power_advice:.1f} dB" if power_advice is not None else "—"

        _html_block(
            f"""
            <div class="panel">
              <div class="panel-title">Cognitive Radio response</div>
              <div style="margin-bottom:0.65rem;">
                <span class="status-pill status-{status}">{status}</span>
              </div>
              <div class="message-box">{msg}</div>
            </div>
            """
        )

        _html_block(
            f"""
            <div class="panel">
              <div class="panel-title">Decision detail</div>
              <div class="ch-meta" style="font-size:0.86rem; line-height:1.7; color:#d5e1ea;">
                <b>Engine</b>: {engine}<br/>
                <b>Action</b>: {action}<br/>
                <b>Recommended channels</b>: {html.escape(channels)}<br/>
                <b>Power advice</b>: {html.escape(advice_txt)}<br/>
                <b>Hop set</b>: {html.escape(hop)}<br/>
                <b>Decision mode</b>: {html.escape(orch.config.decision_mode.value)}
              </div>
            </div>
            """
        )

        _html_block(
            """
            <div class="panel">
              <div class="panel-title">Closed-loop sequence</div>
              <div class="ch-meta" style="font-size:0.86rem; line-height:1.7; color:#d5e1ea;">
                1. Channel model applies noise / jam / fade<br/>
                2. Receiver measures and labels FREE / DEGRADED / BLOCKED<br/>
                3. Cognitive Radio returns status, message, channels / power advice<br/>
                4. Transmitter applies recommendation<br/>
                5. Display updates for operator review
              </div>
            </div>
            """
        )

        ml = orch.engine.ml_metrics
        if ml:
            st.caption(
                f"ML recommender trained on {ml.get('samples')} samples · "
                f"train accuracy {ml.get('train_accuracy')} · "
                f"classes {ml.get('classes')}"
            )

    # Quick channel jam toggles
    st.markdown("#### Quick jam toggle")
    per_row = 8
    for row_start in range(0, orch.config.n_channels, per_row):
        row_ids = list(range(row_start, min(row_start + per_row, orch.config.n_channels)))
        cols = st.columns(len(row_ids))
        for col, i in zip(cols, row_ids):
            with col:
                if st.button(f"CH{i}", key=f"jam_{i}", use_container_width=True):
                    orch.toggle_jam_channel(i)
                    st.session_state.last = orch.step()
                    st.rerun()

    hist = orch.history[-20:]
    if hist:
        hdf = pd.DataFrame(
            [
                {
                    "Step": h.step,
                    "TX": h.tx_channel,
                    "Power (dB)": round(h.tx_power_db, 1),
                    "Status": h.response["status_code"],
                    "Engine": h.response.get("engine"),
                    "Channels": ",".join(map(str, h.response.get("channels", []))),
                    "Jam": h.jam_profile,
                }
                for h in hist
            ]
        )
        st.markdown("#### Recent decision history")
        st.dataframe(hdf, use_container_width=True, hide_index=True)

    st.markdown(
        """
        <div class="footer-note">
          Software-only demonstration for technical review. No radiated RF. Receiver judgement is measurement-based.
          ML uses a supervised MLP behind the same Cognitive Radio interface, with rule-based safety overrides.
          Interfaces are structured for later eADM connection without redesigning the decision engine.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
