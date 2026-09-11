"""
Cognitive Radio Software Simulation — professional demonstration UI.

Supports Light Mode and Dark Mode.
Run from this directory:
    python -m streamlit run app.py
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


def theme_css(mode: str) -> str:
    """Return CSS for light or dark mode."""
    dark = mode == "Dark"

    if dark:
        t = {
            "text": "#e6edf2",
            "text_muted": "#9bb0c0",
            "text_strong": "#f2f6f9",
            "app_bg": "linear-gradient(180deg, #0a1520 0%, #0f1f2e 45%, #122433 100%)",
            "chrome": "#0b1824",
            "chrome_border": "#243647",
            "panel": "#132536",
            "panel_border": "#2a4256",
            "input_bg": "#132536",
            "input_border": "#2a4256",
            "btn_bg": "#1a3348",
            "btn_border": "#3d5a70",
            "btn_text": "#eef4f8",
            "btn_hover": "#244560",
            "btn_primary": "#2a5f7a",
            "btn_primary_border": "#3d7ea0",
            "hero_bg": "linear-gradient(135deg, #102032 0%, #163047 100%)",
            "hero_border": "#2a4256",
            "hero_kicker": "#8fa6b8",
            "hero_title": "#f5f8fa",
            "hero_sub": "#b7c7d4",
            "message_bg": "#0e1c28",
            "message_text": "#dce7ef",
            "meta": "#a7bac8",
            "footer": "#7f94a5",
            "metric_value": "#f4f8fb",
            "ok_bg": "#163528",
            "ok_fg": "#7dcea0",
            "ok_bd": "#2f6b4f",
            "deg_bg": "#3a2f14",
            "deg_fg": "#e0c36a",
            "deg_bd": "#7a6528",
            "pwr_bg": "#3a2414",
            "pwr_fg": "#e0a06a",
            "pwr_bd": "#7a4a28",
            "blk_bg": "#3a1616",
            "blk_fg": "#e08a8a",
            "blk_bd": "#7a3030",
            "hold_bg": "#1d2a38",
            "hold_fg": "#a9bccb",
            "hold_bd": "#3a5166",
        }
    else:
        t = {
            "text": "#1a2b3c",
            "text_muted": "#5a6f82",
            "text_strong": "#0b1c2c",
            "app_bg": "linear-gradient(180deg, #f4f7fa 0%, #eef3f7 45%, #e8eef4 100%)",
            "chrome": "#ffffff",
            "chrome_border": "#d5dee7",
            "panel": "#ffffff",
            "panel_border": "#d0dbe6",
            "input_bg": "#ffffff",
            "input_border": "#c5d0db",
            "btn_bg": "#d8e4ee",
            "btn_border": "#8fa6b8",
            "btn_text": "#0b1c2c",
            "btn_hover": "#c5d6e4",
            "btn_primary": "#1e4f68",
            "btn_primary_border": "#1e4f68",
            "hero_bg": "linear-gradient(135deg, #ffffff 0%, #eef4f8 100%)",
            "hero_border": "#cfdbe6",
            "hero_kicker": "#5a7084",
            "hero_title": "#0b2a5b",
            "hero_sub": "#3d5266",
            "message_bg": "#f3f7fa",
            "message_text": "#1a2b3c",
            "meta": "#3d5266",
            "footer": "#6a7f92",
            "metric_value": "#0b1c2c",
            "ok_bg": "#e7f5ec",
            "ok_fg": "#1b6b3a",
            "ok_bd": "#8fc9a5",
            "deg_bg": "#f8f1de",
            "deg_fg": "#7a5b12",
            "deg_bd": "#e0c36a",
            "pwr_bg": "#f7ebe3",
            "pwr_fg": "#8a4b1c",
            "pwr_bd": "#e0a06a",
            "blk_bg": "#f7e6e6",
            "blk_fg": "#8a3030",
            "blk_bd": "#e08a8a",
            "hold_bg": "#eef2f6",
            "hold_fg": "#3d5266",
            "hold_bd": "#b7c7d6",
        }

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{
  font-family: 'IBM Plex Sans', sans-serif;
  color: {t['text']};
}}
.stApp {{
  background: {t['app_bg']};
  color: {t['text']};
}}
header[data-testid="stHeader"] {{
  background: {t['chrome']} !important;
  border-bottom: 1px solid {t['chrome_border']};
}}
header[data-testid="stHeader"] * {{
  color: {t['text']} !important;
}}
div[data-testid="stToolbar"],
div[data-testid="stDecoration"] {{
  background: {t['chrome']} !important;
}}
section[data-testid="stAppViewContainer"] > .main {{
  background: transparent;
}}
.block-container {{
  padding-top: 2.4rem;
  padding-bottom: 2rem;
  max-width: 1400px;
}}
section[data-testid="stSidebar"] {{
  background: {t['chrome']} !important;
  border-right: 1px solid {t['chrome_border']};
}}
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {{
  color: {t['text']} !important;
}}
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] label span {{
  color: {t['text']} !important;
}}
/* Do not force sidebar text colour onto buttons */
section[data-testid="stSidebar"] div.stButton span {{
  color: inherit !important;
}}
h1, h2, h3, h4, .stSubheader {{
  font-family: 'IBM Plex Sans', sans-serif !important;
  letter-spacing: 0.02em;
  color: {t['text_strong']} !important;
}}
.stCaption, [data-testid="stCaptionContainer"] {{
  color: {t['text_muted']} !important;
}}
div[data-testid="stMetric"] {{
  background: {t['panel']};
  border: 1px solid {t['panel_border']};
  border-radius: 6px;
  padding: 0.45rem 0.65rem;
}}
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricLabel"] {{
  color: {t['text_muted']} !important;
  font-size: 0.72rem !important;
}}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
  color: {t['metric_value']} !important;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1.05rem !important;
  line-height: 1.2 !important;
}}
div.stButton > button,
button[kind="secondary"],
button[data-testid="baseButton-secondary"],
button[data-testid="stBaseButton-secondary"],
section[data-testid="stSidebar"] div.stButton > button {{
  background-color: {t['btn_bg']} !important;
  background-image: none !important;
  color: {t['btn_text']} !important;
  border: 1px solid {t['btn_border']} !important;
  border-radius: 6px !important;
  opacity: 1 !important;
}}
div.stButton > button *,
button[kind="secondary"] *,
button[data-testid="baseButton-secondary"] *,
button[data-testid="stBaseButton-secondary"] *,
section[data-testid="stSidebar"] div.stButton > button * {{
  color: {t['btn_text']} !important;
  fill: {t['btn_text']} !important;
}}
div.stButton > button:hover,
button[kind="secondary"]:hover,
section[data-testid="stSidebar"] div.stButton > button:hover {{
  background-color: {t['btn_hover']} !important;
  color: {t['text_strong']} !important;
  border-color: {t['btn_border']} !important;
}}
div.stButton > button:hover * {{
  color: {t['text_strong']} !important;
}}
button[kind="primary"],
button[data-testid="baseButton-primary"],
button[data-testid="stBaseButton-primary"],
div.stButton > button[kind="primary"] {{
  background-color: {t['btn_primary']} !important;
  background-image: none !important;
  border: 1px solid {t['btn_primary_border']} !important;
  color: #ffffff !important;
}}
button[kind="primary"] *,
button[data-testid="baseButton-primary"] *,
button[data-testid="stBaseButton-primary"] *,
div.stButton > button[kind="primary"] * {{
  color: #ffffff !important;
  fill: #ffffff !important;
}}
/* Light-mode secondary: ensure dark ink on pale surface */
[data-theme="light"] div.stButton > button:not([kind="primary"]) {{
  color: #0b1c2c !important;
}}
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="base-input"],
.stNumberInput input,
.stTextInput input,
.stMultiSelect [data-baseweb="select"] > div {{
  background-color: {t['input_bg']} !important;
  color: {t['text']} !important;
  border-color: {t['input_border']} !important;
}}
div[data-baseweb="popover"],
div[data-baseweb="menu"] li,
ul[role="listbox"] li {{
  background-color: {t['input_bg']} !important;
  color: {t['text']} !important;
}}
.stSlider label, .stSelectbox label, .stMultiSelect label, .stToggle label, .stRadio label {{
  color: {t['text']} !important;
}}
div[data-testid="stDataFrame"],
div[data-testid="stDataFrame"] > div,
div[data-testid="stDataFrameResizable"],
[data-testid="stTable"] {{
  background-color: {t['panel']} !important;
  border: 1px solid {t['panel_border']} !important;
  border-radius: 6px;
  color: {t['text']} !important;
}}
div[data-testid="stDataFrame"] *,
div[data-testid="stDataFrame"] [role="grid"],
div[data-testid="stDataFrame"] [role="row"],
div[data-testid="stDataFrame"] [role="gridcell"],
div[data-testid="stDataFrame"] [role="columnheader"] {{
  background-color: {t['panel']} !important;
  color: {t['text']} !important;
  border-color: {t['panel_border']} !important;
}}
.hero {{
  border: 1px solid {t['hero_border']};
  background: {t['hero_bg']};
  border-radius: 8px;
  padding: 1.55rem 1.35rem 1.25rem 1.35rem;
  margin-top: 0.75rem;
  margin-bottom: 1.15rem;
}}
.hero-kicker {{
  color: {t['hero_kicker']};
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  margin: 0 0 0.55rem 0;
}}
.hero-title {{
  color: {t['hero_title']};
  font-size: 1.55rem;
  font-weight: 650;
  margin: 0;
}}
.hero-sub {{
  color: {t['hero_sub']};
  margin-top: 0.35rem;
  font-size: 0.95rem;
}}
.panel {{
  background: {t['panel']};
  border: 1px solid {t['panel_border']};
  border-radius: 8px;
  padding: 0.95rem 1rem;
  margin-bottom: 0.85rem;
}}
.panel-title {{
  color: {t['text_muted']};
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 0.55rem;
}}
.status-pill {{
  display: inline-block;
  padding: 0.28rem 0.7rem;
  border-radius: 4px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid transparent;
}}
.status-OK {{ background: {t['ok_bg']}; color: {t['ok_fg']}; border-color: {t['ok_bd']}; }}
.status-DEGRADED_OK {{ background: {t['deg_bg']}; color: {t['deg_fg']}; border-color: {t['deg_bd']}; }}
.status-INCREASE_POWER {{ background: {t['pwr_bg']}; color: {t['pwr_fg']}; border-color: {t['pwr_bd']}; }}
.status-ALL_BLOCKED {{ background: {t['blk_bg']}; color: {t['blk_fg']}; border-color: {t['blk_bd']}; }}
.status-HOLD {{ background: {t['hold_bg']}; color: {t['hold_fg']}; border-color: {t['hold_bd']}; }}
.message-box {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.9rem;
  color: {t['message_text']};
  background: {t['message_bg']};
  border: 1px solid {t['panel_border']};
  border-radius: 6px;
  padding: 0.75rem 0.85rem;
  min-height: 3.2rem;
}}
.ch-meta {{
  margin-top: 0.45rem;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  color: {t['meta']};
  line-height: 1.35;
}}
.detail-text {{
  font-size: 0.86rem;
  line-height: 1.7;
  color: {t['meta']};
}}
.footer-note {{
  color: {t['footer']};
  font-size: 0.8rem;
  border-top: 1px solid {t['chrome_border']};
  margin-top: 1.2rem;
  padding-top: 0.8rem;
}}
{'' if dark else '''
/* Light mode: dark labels on secondary; white labels on primary (navy) */
div.stButton > button,
div.stButton > button *,
section[data-testid="stSidebar"] div.stButton > button,
section[data-testid="stSidebar"] div.stButton > button * {
  color: #0b1c2c !important;
  -webkit-text-fill-color: #0b1c2c !important;
}
div.stButton > button[kind="primary"],
div.stButton > button[kind="primary"] *,
div.stButton > button[data-testid="baseButton-primary"],
div.stButton > button[data-testid="baseButton-primary"] *,
div.stButton > button[data-testid="stBaseButton-primary"],
div.stButton > button[data-testid="stBaseButton-primary"] *,
section[data-testid="stSidebar"] div.stButton > button[kind="primary"],
section[data-testid="stSidebar"] div.stButton > button[kind="primary"] *,
section[data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-primary"],
section[data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-primary"] *,
section[data-testid="stSidebar"] div.stButton > button[data-testid="stBaseButton-primary"],
section[data-testid="stSidebar"] div.stButton > button[data-testid="stBaseButton-primary"] * {
  color: #ffffff !important;
  -webkit-text-fill-color: #ffffff !important;
}
'''}
</style>
"""


def _init_state() -> None:
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "Light"
    if "orch" not in st.session_state:
        cfg = SimConfig(n_channels=8, decision_mode=DecisionMode.HYBRID, hop_enabled=False)
        orch = Orchestrator(cfg)
        orch.train_ml(800)
        st.session_state.orch = orch
        st.session_state.last = orch.step()
        st.session_state.log = []


def _card_style(state: str, active: bool, dark: bool) -> str:
    if dark:
        bg = {
            "FREE": "linear-gradient(180deg,#143226 0%,#102231 75%)",
            "DEGRADED": "linear-gradient(180deg,#332b14 0%,#102231 75%)",
            "BLOCKED": "linear-gradient(180deg,#331818 0%,#102231 75%)",
        }.get(state, "#102231")
        border = {"FREE": "#2f6b4f", "DEGRADED": "#7a6528", "BLOCKED": "#7a3030"}.get(state, "#314859")
        title = "#f0f5f8"
        meta = "#a7bac8"
    else:
        bg = {
            "FREE": "linear-gradient(180deg,#e8f6ee 0%,#ffffff 75%)",
            "DEGRADED": "linear-gradient(180deg,#f8f1de 0%,#ffffff 75%)",
            "BLOCKED": "linear-gradient(180deg,#f8e8e8 0%,#ffffff 75%)",
        }.get(state, "#ffffff")
        border = {"FREE": "#8fc9a5", "DEGRADED": "#e0c36a", "BLOCKED": "#e08a8a"}.get(state, "#c5d0db")
        title = "#0b1c2c"
        meta = "#3d5266"
    if active:
        border = "#b8923f" if not dark else "#c4a35a"
    shadow = f"inset 0 0 0 2px {border};" if active else ""
    return (
        f"background:{bg};border:1px solid {border};{shadow}"
        f"border-radius:6px;padding:0.7rem 0.65rem;min-height:108px;"
        f"--card-title:{title};--card-meta:{meta};"
    )


def _state_color(state: str, dark: bool) -> str:
    if dark:
        return {"FREE": "#7dcea0", "DEGRADED": "#e0c36a", "BLOCKED": "#e08a8a"}.get(state, "#d5e1ea")
    return {"FREE": "#1b6b3a", "DEGRADED": "#7a5b12", "BLOCKED": "#8a3030"}.get(state, "#1a2b3c")


def render_channel_map(observations: list[dict], tx_channel: int, dark: bool) -> None:
    st.caption("FREE · DEGRADED · BLOCKED · gold border = active TX")
    per_row = 4
    for row_start in range(0, len(observations), per_row):
        row = observations[row_start : row_start + per_row]
        cols = st.columns(len(row))
        for col, o in zip(cols, row):
            state = o["state"]
            active = o["channel_id"] == tx_channel
            tx_line = "TX ACTIVE" if active else ""
            title_c = "#f0f5f8" if dark else "#0b1c2c"
            meta_c = "#a7bac8" if dark else "#3d5266"
            card = (
                f'<div style="{_card_style(state, active, dark)}">'
                f'<div style="font-family:IBM Plex Mono,monospace;font-weight:600;color:{title_c};">'
                f'CH{o["channel_id"]:02d}</div>'
                f'<div style="margin-top:0.35rem;font-size:0.78rem;font-weight:650;letter-spacing:0.06em;'
                f'color:{_state_color(state, dark)};">{state}</div>'
                f'<div style="margin-top:0.45rem;font-family:IBM Plex Mono,monospace;font-size:0.72rem;'
                f'color:{meta_c};line-height:1.35;">SINR {o["sinr_db"]:.1f} dB<br/>Jam {o["jam_power"]:.1f}<br/>{tx_line}</div>'
                f"</div>"
            )
            with col:
                if hasattr(st, "html"):
                    st.html(card)
                else:
                    st.markdown(card, unsafe_allow_html=True)


def _html_block(content: str) -> None:
    compact = " ".join(line.strip() for line in content.splitlines() if line.strip())
    if hasattr(st, "html"):
        st.html(compact)
    else:
        st.markdown(compact, unsafe_allow_html=True)


def main() -> None:
    _init_state()
    orch: Orchestrator = st.session_state.orch

    with st.sidebar:
        st.markdown("### Appearance")
        theme_mode = st.radio(
            "Theme",
            options=["Light", "Dark"],
            index=0 if st.session_state.theme_mode == "Light" else 1,
            horizontal=True,
            help="Switch between light mode and dark mode.",
        )
        if theme_mode != st.session_state.theme_mode:
            st.session_state.theme_mode = theme_mode
            st.rerun()

    dark = st.session_state.theme_mode == "Dark"
    st.markdown(
        f'<div id="cr-theme-root" data-theme="{st.session_state.theme_mode.lower()}"></div>',
        unsafe_allow_html=True,
    )
    st.markdown(theme_css(st.session_state.theme_mode), unsafe_allow_html=True)

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
        render_channel_map(last.observations, last.tx_channel, dark)

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
              <div class="detail-text">
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
              <div class="detail-text">
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
