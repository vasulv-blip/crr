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

from cr_sim.models import (
    ChannelObservation,
    ChannelState,
    DecisionMode,
    JamProfile,
    SimConfig,
)
from cr_sim.orchestrator import Orchestrator

st.set_page_config(
    page_title="Cognitive Radio Simulation | eAge Innovations",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_theme_tokens(mode: str) -> dict[str, str]:
    """Return styling tokens for light or dark mode."""
    dark = mode == "Dark"
    if dark:
        return {
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
    return {
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


def theme_css(mode: str) -> str:
    """Return CSS for light or dark mode."""
    dark = mode == "Dark"
    t = get_theme_tokens(mode)

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
/* Do not restyle dataframe grid internals — that blanks the table in Streamlit */
div[data-testid="stDataFrame"] {{
  border: 1px solid {t['panel_border']} !important;
  border-radius: 6px;
}}
div[data-testid="stTable"] table {{
  background-color: {t['panel']} !important;
  color: {t['text']} !important;
  border-collapse: collapse;
  width: 100%;
}}
div[data-testid="stTable"] th {{
  background-color: {t['btn_bg']} !important;
  color: {t['text_strong']} !important;
  border: 1px solid {t['panel_border']} !important;
  padding: 0.4rem 0.5rem !important;
}}
div[data-testid="stTable"] td {{
  background-color: {t['panel']} !important;
  color: {t['text']} !important;
  border: 1px solid {t['panel_border']} !important;
  padding: 0.35rem 0.5rem !important;
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
/* Modular Node Architecture cards & containers */
div[data-testid="stVerticalBlockBorderWrapper"]:has([data-node="jammer"]) {{
  border: 1.5px solid {"rgba(192, 57, 43, 0.45)" if not dark else "rgba(231, 76, 60, 0.4)"} !important;
  border-top: 4px solid #c0392b !important;
  border-radius: 9px !important;
  background-color: {t['panel']} !important;
  box-shadow: 0 4px 14px {"rgba(192, 57, 43, 0.08)" if not dark else "rgba(0, 0, 0, 0.4)"} !important;
  overflow: hidden !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has([data-node="receiver"]) {{
  border: 1.5px solid {"rgba(41, 128, 185, 0.45)" if not dark else "rgba(52, 152, 219, 0.4)"} !important;
  border-top: 4px solid #2980b9 !important;
  border-radius: 9px !important;
  background-color: {t['panel']} !important;
  box-shadow: 0 4px 14px {"rgba(41, 128, 185, 0.08)" if not dark else "rgba(0, 0, 0, 0.4)"} !important;
  overflow: hidden !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has([data-node="transmitter"]) {{
  border: 1.5px solid {"rgba(39, 174, 96, 0.45)" if not dark else "rgba(46, 204, 113, 0.4)"} !important;
  border-top: 4px solid #27ae60 !important;
  border-radius: 9px !important;
  background-color: {t['panel']} !important;
  box-shadow: 0 4px 14px {"rgba(39, 174, 96, 0.08)" if not dark else "rgba(0, 0, 0, 0.4)"} !important;
  overflow: hidden !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has([data-node="decision"]) {{
  border: 1.5px solid {"rgba(142, 68, 173, 0.45)" if not dark else "rgba(155, 89, 182, 0.4)"} !important;
  border-top: 4px solid #8e44ad !important;
  border-radius: 9px !important;
  background-color: {t['panel']} !important;
  box-shadow: 0 4px 14px {"rgba(142, 68, 173, 0.08)" if not dark else "rgba(0, 0, 0, 0.4)"} !important;
  overflow: hidden !important;
}}

/* Subsystem Banners */
.node-banner {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.85rem;
  padding: 0.65rem 0.85rem;
  border-radius: 7px;
  margin-bottom: 0.75rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  min-width: 0;
  box-sizing: border-box;
}}
.node-banner-text {{
  flex: 1 1 auto;
  min-width: 0;
}}
.node-banner-badge {{
  flex: 0 0 auto;
  white-space: nowrap !important;
  align-self: flex-start;
  margin-top: 0.1rem;
}}
.node-banner-jam {{
  background: {"linear-gradient(135deg, rgba(231, 76, 60, 0.16) 0%, rgba(192, 57, 43, 0.06) 100%)" if not dark else "linear-gradient(135deg, rgba(192, 57, 43, 0.35) 0%, rgba(35, 18, 22, 0.7) 100%)"};
  border: 1px solid {"#e08a8a" if not dark else "#7a3030"};
  border-left: 5px solid #c0392b;
}}
.node-banner-rx {{
  background: {"linear-gradient(135deg, rgba(52, 152, 219, 0.16) 0%, rgba(41, 128, 185, 0.06) 100%)" if not dark else "linear-gradient(135deg, rgba(41, 128, 185, 0.35) 0%, rgba(18, 28, 42, 0.7) 100%)"};
  border: 1px solid {"#9ec7e8" if not dark else "#2b5675"};
  border-left: 5px solid #2980b9;
}}
.node-banner-tx {{
  background: {"linear-gradient(135deg, rgba(46, 204, 113, 0.16) 0%, rgba(39, 174, 96, 0.06) 100%)" if not dark else "linear-gradient(135deg, rgba(39, 174, 96, 0.35) 0%, rgba(18, 36, 26, 0.7) 100%)"};
  border: 1px solid {"#8fc9a5" if not dark else "#2f6b4f"};
  border-left: 5px solid #27ae60;
}}
.node-banner-decision {{
  background: {"linear-gradient(135deg, rgba(155, 89, 182, 0.16) 0%, rgba(142, 68, 173, 0.06) 100%)" if not dark else "linear-gradient(135deg, rgba(142, 68, 173, 0.35) 0%, rgba(32, 18, 42, 0.7) 100%)"};
  border: 1px solid {"#d2b4de" if not dark else "#6c3483"};
  border-left: 5px solid #8e44ad;
}}

.node-banner-title {{
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 0.92rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  display: flex;
  align-items: center;
  gap: 0.45rem;
}}
.node-banner-jam .node-banner-title {{
  color: {"#922b21" if not dark else "#f1948a"};
}}
.node-banner-rx .node-banner-title {{
  color: {"#1f618d" if not dark else "#85c1e9"};
}}
.node-banner-tx .node-banner-title {{
  color: {"#1e8449" if not dark else "#82e0aa"};
}}
.node-banner-decision .node-banner-title {{
  color: {"#6c3483" if not dark else "#bb8fce"};
}}

.node-banner-subtitle {{
  font-size: 0.71rem;
  color: {t['text_muted']};
  font-weight: 500;
  margin-top: 0.12rem;
  letter-spacing: 0.02em;
}}

.node-card {{
  background: {t['panel']};
  border: 1px solid {t['panel_border']};
  border-radius: 8px;
  padding: 1.1rem 1.15rem;
  margin-bottom: 0.95rem;
}}
.node-card-jammer {{
  border-top: 4px solid #c0392b;
}}
.node-card-receiver {{
  border-top: 4px solid #2980b9;
}}
.node-card-transmitter {{
  border-top: 4px solid #27ae60;
}}
.node-card-decision {{
  border-top: 4px solid #8e44ad;
}}
.node-header-row {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
  padding-bottom: 0.55rem;
  border-bottom: 1px solid {t['panel_border']};
}}
.node-title {{
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 0.92rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: {t['text_strong']};
  display: flex;
  align-items: center;
}}
.node-badge-alert {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  background: {t['blk_bg']};
  color: {t['blk_fg']};
  border: 1px solid {t['blk_bd']};
  white-space: nowrap !important;
  flex-shrink: 0;
}}
.node-badge-ok {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  background: {t['ok_bg']};
  color: {t['ok_fg']};
  border: 1px solid {t['ok_bd']};
  white-space: nowrap !important;
  flex-shrink: 0;
}}
.node-badge-info {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  background: {t['message_bg']};
  color: {t['text_strong']};
  border: 1px solid {t['panel_border']};
  white-space: nowrap !important;
  flex-shrink: 0;
}}
.sleek-telemetry-grid {{
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 0.45rem;
  margin-bottom: 0.65rem;
  width: 100%;
  box-sizing: border-box;
}}
.telemetry-pill,
.telemetry-pill-jam,
.telemetry-pill-rx,
.telemetry-pill-tx {{
  min-width: 0 !important;
  max-width: 100% !important;
  overflow: hidden !important;
  box-sizing: border-box !important;
}}
.telemetry-pill {{
  background: {t['message_bg']};
  border: 1px solid {t['panel_border']};
  border-radius: 6px;
  padding: 0.45rem 0.6rem;
  display: flex;
  flex-direction: column;
}}
.telemetry-pill-jam {{
  background: {"rgba(192, 57, 43, 0.05)" if not dark else "rgba(192, 57, 43, 0.15)"};
  border: 1px solid {"#fadbd8" if not dark else "#5c2424"};
  border-left: 3.5px solid #c0392b;
  border-radius: 6px;
  padding: 0.45rem 0.6rem;
  display: flex;
  flex-direction: column;
}}
.telemetry-pill-jam .telemetry-label {{
  color: {"#c0392b" if not dark else "#e57373"};
}}
.telemetry-pill-rx {{
  background: {"rgba(41, 128, 185, 0.05)" if not dark else "rgba(41, 128, 185, 0.15)"};
  border: 1px solid {"#d4e6f1" if not dark else "#24425c"};
  border-left: 3.5px solid #2980b9;
  border-radius: 6px;
  padding: 0.45rem 0.6rem;
  display: flex;
  flex-direction: column;
}}
.telemetry-pill-rx .telemetry-label {{
  color: {"#2980b9" if not dark else "#64b5f6"};
}}
.telemetry-pill-tx {{
  background: {"rgba(39, 174, 96, 0.05)" if not dark else "rgba(39, 174, 96, 0.15)"};
  border: 1px solid {"#d5f5e3" if not dark else "#245c38"};
  border-left: 3.5px solid #27ae60;
  border-radius: 6px;
  padding: 0.45rem 0.6rem;
  display: flex;
  flex-direction: column;
}}
.telemetry-pill-tx .telemetry-label {{
  color: {"#27ae60" if not dark else "#81c784"};
}}
.telemetry-label {{
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: {t['text_muted']};
  margin-bottom: 0.15rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  min-width: 0;
}}
.telemetry-val {{
  font-size: 0.85rem;
  font-weight: 700;
  font-family: 'IBM Plex Mono', monospace;
  color: {t['text_strong']};
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  min-width: 0;
  max-width: 100%;
}}
.sleek-section-divider {{
  display: flex;
  align-items: center;
  text-align: center;
  margin: 0.65rem 0 0.55rem 0;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: {t['text_muted']};
}}
.sleek-section-divider::before,
.sleek-section-divider::after {{
  content: '';
  flex: 1;
  border-bottom: 1px solid {t['panel_border']};
}}
.sleek-section-divider:not(:empty)::before {{
  margin-right: .5em;
}}
.sleek-section-divider:not(:empty)::after {{
  margin-left: .5em;
}}
.sleek-section-divider-jam {{
  color: {"#c0392b" if not dark else "#e57373"};
  font-weight: 700;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  display: flex;
  align-items: center;
  text-align: center;
  margin: 0.65rem 0 0.55rem 0;
}}
.sleek-section-divider-jam::before, .sleek-section-divider-jam::after {{
  content: '';
  flex: 1;
  border-bottom: 1px solid {"#fadbd8" if not dark else "#7a3030"};
}}
.sleek-section-divider-jam:not(:empty)::before {{ margin-right: .5em; }}
.sleek-section-divider-jam:not(:empty)::after {{ margin-left: .5em; }}
.sleek-section-divider-rx {{
  color: {"#2980b9" if not dark else "#64b5f6"};
  font-weight: 700;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  display: flex;
  align-items: center;
  text-align: center;
  margin: 0.65rem 0 0.55rem 0;
}}
.sleek-section-divider-rx::before, .sleek-section-divider-rx::after {{
  content: '';
  flex: 1;
  border-bottom: 1px solid {"#d4e6f1" if not dark else "#2b5675"};
}}
.sleek-section-divider-rx:not(:empty)::before {{ margin-right: .5em; }}
.sleek-section-divider-rx:not(:empty)::after {{ margin-left: .5em; }}
.sleek-section-divider-tx {{
  color: {"#27ae60" if not dark else "#81c784"};
  font-weight: 700;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  display: flex;
  align-items: center;
  text-align: center;
  margin: 0.65rem 0 0.55rem 0;
}}
.sleek-section-divider-tx::before, .sleek-section-divider-tx::after {{
  content: '';
  flex: 1;
  border-bottom: 1px solid {"#d5f5e3" if not dark else "#2f6b4f"};
}}
.sleek-section-divider-tx:not(:empty)::before {{ margin-right: .5em; }}
.sleek-section-divider-tx:not(:empty)::after {{ margin-left: .5em; }}
/* Threat emitter primary button styling inside Jammer */
div:has([data-node="jammer"]) button[kind="primary"],
div:has([data-node="jammer"]) button[data-testid="baseButton-primary"],
div:has([data-node="jammer"]) button[data-testid="stBaseButton-primary"] {{
  background: linear-gradient(180deg, #c0392b 0%, #a93226 100%) !important;
  border-color: #922b21 !important;
  color: #ffffff !important;
  font-weight: 700 !important;
  box-shadow: 0 2px 8px rgba(192, 57, 43, 0.35) !important;
}}
.sleek-card-footer {{
  margin-top: 0.75rem;
  padding-top: 0.55rem;
  border-top: 1px solid {t['panel_border']};
  font-size: 0.75rem;
  color: {t['text_muted']};
  line-height: 1.4;
}}
.node-metric-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 0.84rem;
  margin-top: 0.25rem;
  margin-bottom: 0.45rem;
}}
.node-metric-table td {{
  padding: 0.32rem 0.15rem;
  vertical-align: middle;
  border-bottom: 1px solid {t['panel_border']};
}}
.node-metric-table td.label-col {{
  color: {t['text_muted']};
  font-weight: 500;
  width: 44%;
}}
.node-metric-table td.val-col {{
  color: {t['text_strong']};
  font-weight: 600;
  font-family: 'IBM Plex Mono', monospace;
}}
.ml-attached-card {{
  background: {t['message_bg']};
  border: 1px solid {t['btn_border']};
  border-left: 3px solid #27ae60;
  border-radius: 6px;
  padding: 0.75rem 0.85rem;
  margin-top: 0.65rem;
}}
.ml-attached-title {{
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: {t['hero_title']};
  margin-bottom: 0.45rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}}
.trace-step-box {{
  background: {t['message_bg']};
  border: 1px solid {t['panel_border']};
  border-radius: 6px;
  padding: 0.8rem 0.95rem;
  margin-bottom: 0.65rem;
  font-size: 0.87rem;
  line-height: 1.55;
  color: {t['text']};
}}
.trace-step-box b {{
  color: {t['text_strong']};
}}
.trace-num {{
  display: inline-block;
  background: {t['btn_bg']};
  color: {t['btn_text']};
  font-weight: 700;
  font-size: 0.74rem;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  text-align: center;
  line-height: 22px;
  margin-right: 0.5rem;
}}
/* Sleek widget margins inside architecture containers */
div[data-testid="stVerticalBlockBorderWrapper"]:has([data-node]) .stSelectbox,
div[data-testid="stVerticalBlockBorderWrapper"]:has([data-node]) .stSlider {{
  margin-bottom: 0.25rem;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has([data-node]) label p {{
  font-size: 0.76rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.03em !important;
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
    if "ui_view" not in st.session_state:
        st.session_state.ui_view = "System Architecture & Node View"
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
                f'color:{meta_c};line-height:1.35;">SINR {o["sinr_db"]:.1f} dB<br/>Jam {o["jam_power"]:.1f} a.u.<br/>{tx_line}</div>'
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


def _get_ml_prediction(orch: Orchestrator, last) -> tuple[int | None, bool, float]:
    """Extract or predict the recommendation from the transmitter-attached ML model."""
    try:
        obs_objs = [
            ChannelObservation(
                channel_id=int(o["channel_id"]),
                signal_power=float(o["signal_power"]),
                noise_power=float(o["noise_power"]),
                jam_power=float(o["jam_power"]),
                path_gain=float(o["path_gain"]),
                sinr_db=float(o["sinr_db"]),
                state=ChannelState(o["state"]),
                is_active_tx=bool(o["is_active_tx"]),
            )
            for o in last.observations
        ]
        pred = orch.engine.ml.predict(obs_objs, float(last.tx_power_db), float(orch.config.max_power_db))
        return pred.channel, pred.increase_power, float(pred.confidence)
    except Exception:
        conf = float(last.response.get("detail", {}).get("confidence", 1.0))
        ch = last.response.get("channels", [0])[0] if last.response.get("channels") else None
        inc = last.response.get("action") == "INCREASE_POWER"
        return ch, inc, conf


def render_operator_view(orch: Orchestrator, last, dark: bool) -> None:
    """Render the classic Operator Spectrum View with channel map, measurement table, and history."""
    resp = last.response
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
                "jam_power": "Jam power (a.u.)",
                "path_gain": "Path gain",
                "is_active_tx": "TX active",
            }
        )
        st.caption("Channel measurements (numeric table)")
        st.table(df)

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
    st.markdown("#### Recent decision history")
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
        st.table(hdf)
    else:
        st.info("No decisions recorded yet. Click Single step or Apply jam to build history.")


def render_architecture_view(orch: Orchestrator, last, dark: bool, t: dict) -> None:
    """Render the Modular System Architecture View:
    Three subsystem boxes (Jammer, Receiver, Transmitter with attached ML) + Decision Engine Explainability Trace.
    Excludes the channel measurement table, quick jam toggle row, and recent decision history table."""
    obs = last.observations
    resp = last.response
    n_ch = orch.config.n_channels
    status = resp["status_code"]
    engine = resp.get("engine", "HYBRID")
    action = resp.get("action", "USE_CHANNELS")
    channels = ", ".join(f"CH{c}" for c in resp.get("channels", [])) or "—"
    hop = ", ".join(f"CH{c}" for c in last.hop_set) if orch.config.hop_enabled else "Disabled"
    power_advice = resp.get("power_advice_db")
    advice_txt = f"{power_advice:.1f} dB" if power_advice is not None else "—"

    # Category breakdowns from observations
    free_obs = [o for o in obs if o["state"] == "FREE"]
    deg_obs = [o for o in obs if o["state"] == "DEGRADED"]
    blk_obs = [o for o in obs if o["state"] == "BLOCKED"]
    free_ids = [o["channel_id"] for o in free_obs]
    deg_ids = [o["channel_id"] for o in deg_obs]
    blk_ids = [o["channel_id"] for o in blk_obs]
    best_ch = max(obs, key=lambda o: o["sinr_db"])
    worst_ch = min(obs, key=lambda o: o["sinr_db"])

    # Jammer details
    jammed_obs = [o for o in obs if o["jam_power"] > 0.0]
    jammed_ids = [o["channel_id"] for o in jammed_obs]
    is_jamming = bool(last.jam_profile != "NONE" or jammed_obs)
    if last.jam_profile == "BARRAGE":
        target_short = f"CH0–CH{n_ch - 1} (Barrage)"
        target_full = f"All channels CH0–CH{n_ch - 1} (Full-band noise denial)"
    elif last.jam_profile == "SWEEP":
        curr_sw = orch.channel.sweep_index % n_ch
        target_short = f"CH{curr_sw} (Sweep ±15%)"
        target_full = f"CH{curr_sw} (Agile sweep with 15% neighbor bleed)"
    elif jammed_ids:
        target_full = ", ".join(f"CH{c}" for c in jammed_ids)
        if len(jammed_ids) <= 3:
            target_short = target_full
        else:
            target_short = ", ".join(f"CH{c}" for c in jammed_ids[:2]) + f" +{len(jammed_ids)-2}"
    else:
        target_short = "None (Clear)"
        target_full = "None (Spectrum clear)"

    threat_type_map = {
        "NONE": "Benign ambient noise (N0 = 1.0 a.u.)",
        "SPOT": "Targeted narrow-band carrier denial",
        "MULTI_SPOT": "Coordinated multi-carrier denial",
        "SWEEP": "Fast agile frequency-sweeping ECM",
        "BARRAGE": "Full-band high-power barrage denial",
    }
    threat_desc = threat_type_map.get(last.jam_profile, "Active ECM interference")

    # Attached ML Recommender prediction
    ml_pred_ch, ml_pred_inc, ml_conf = _get_ml_prediction(orch, last)
    ml_pred_text = f"Recommend CH{ml_pred_ch}" if ml_pred_ch is not None else ("Advise Increase Power" if ml_pred_inc else "Hold")

    # 3 Top Columns for the 3 Subsystems
    col_jam, col_rx, col_tx = st.columns(3, gap="medium")

    # ================= BOX 1: JAMMER (ECM THREAT NODE) =================
    with col_jam:
        with st.container(border=True):
            st.markdown('<div data-node="jammer" style="display:none;"></div>', unsafe_allow_html=True)
            jam_badge_class = "node-badge-alert" if is_jamming else "node-badge-ok"
            jam_badge_text = "EMITTING ECM" if is_jamming else "STANDBY / BENIGN"
            _html_block(f"""
            <div class="node-banner node-banner-jam">
              <div class="node-banner-text">
                <div class="node-banner-title">
                  <span>Jammer (ECM Threat Node)</span>
                </div>
                <div class="node-banner-subtitle">Adversary Electronic Attack & Interference</div>
              </div>
              <span class="node-banner-badge {jam_badge_class}" style="letter-spacing:0.04em;">{jam_badge_text}</span>
            </div>
            <div class="sleek-telemetry-grid">
              <div class="telemetry-pill-jam">
                <span class="telemetry-label">Active Profile</span>
                <span class="telemetry-val" style="color:{'#c0392b' if is_jamming else t['text_strong']};">{html.escape(last.jam_profile)}</span>
              </div>
              <div class="telemetry-pill-jam" title="{html.escape(target_full)}">
                <span class="telemetry-label">Target Bands</span>
                <span class="telemetry-val">{html.escape(target_short)}</span>
              </div>
              <div class="telemetry-pill-jam">
                <span class="telemetry-label">Active Jammed</span>
                <span class="telemetry-val" style="color:{t['blk_fg'] if jammed_ids else t['text_strong']};">{len(jammed_ids)} / {n_ch} Channels</span>
              </div>
              <div class="telemetry-pill-jam" title="{orch.config.jam_power:.1f} linear arbitrary units">
                <span class="telemetry-label">Jammer Power</span>
                <span class="telemetry-val">{orch.config.jam_power:.1f} a.u.</span>
              </div>
            </div>
            <div class="sleek-section-divider-jam">
              <span>Threat Controls & Emission</span>
            </div>
            """)

            profile_opts = [p.value for p in JamProfile]
            cur_prof_idx = profile_opts.index(last.jam_profile) if last.jam_profile in profile_opts else 0
            sel_profile = st.selectbox(
                "ECM Threat Profile",
                options=profile_opts,
                index=cur_prof_idx,
                key="arch_node_jam_profile",
                help="Select ECM jamming waveform/mode.",
            )

            if sel_profile in (JamProfile.SPOT.value, JamProfile.MULTI_SPOT.value):
                def_targets = list(orch.channel.manual_jammed) if orch.channel.manual_jammed else ([0] if sel_profile == JamProfile.SPOT.value else [0, 1])
                def_targets = [c for c in def_targets if c < n_ch]
                sel_targets = st.multiselect(
                    "Target channels (spot / multi-spot)",
                    options=list(range(n_ch)),
                    default=def_targets or [0],
                    key="arch_node_jam_targets",
                )
            else:
                sel_targets = None

            sel_jam_power = st.slider(
                "Jam power (linear a.u.)",
                min_value=5.0,
                max_value=80.0,
                value=float(orch.config.jam_power),
                step=1.0,
                key="arch_node_jam_power_slider",
                help="Relative linear jammer power in the channel model (same scale as noise).",
            )

            cj_btn1, cj_btn2 = st.columns(2)
            with cj_btn1:
                if st.button("Emit Jam", type="primary", use_container_width=True, key="arch_node_btn_emit"):
                    orch.config.jam_power = float(sel_jam_power)
                    orch.channel.config.jam_power = float(sel_jam_power)
                    orch.set_jam(JamProfile(sel_profile), sel_targets)
                    st.session_state.last = orch.step()
                    st.rerun()
            with cj_btn2:
                if st.button("Silence Jam", use_container_width=True, key="arch_node_btn_clear"):
                    orch.clear_jam()
                    st.session_state.last = orch.step()
                    st.rerun()

            _html_block("""
            <div class="sleek-section-divider-jam" style="margin-top:0.4rem;">
              <span>Quick Threat Presets</span>
            </div>
            """)
            pre_c1, pre_c2 = st.columns(2)
            with pre_c1:
                if st.button("Spot CH0", key="arch_node_pre_spot", use_container_width=True):
                    orch.config.jam_power = float(sel_jam_power)
                    orch.channel.config.jam_power = float(sel_jam_power)
                    orch.set_jam(JamProfile.SPOT, [0])
                    st.session_state.last = orch.step()
                    st.rerun()
                if st.button("Sweep Jam", key="arch_node_pre_sweep", use_container_width=True):
                    orch.config.jam_power = float(sel_jam_power)
                    orch.channel.config.jam_power = float(sel_jam_power)
                    orch.set_jam(JamProfile.SWEEP)
                    st.session_state.last = orch.step()
                    st.rerun()
            with pre_c2:
                if st.button("Multi CH0,1", key="arch_node_pre_multi", use_container_width=True):
                    orch.config.jam_power = float(sel_jam_power)
                    orch.channel.config.jam_power = float(sel_jam_power)
                    orch.set_jam(JamProfile.MULTI_SPOT, [0, 1] if n_ch > 1 else [0])
                    st.session_state.last = orch.step()
                    st.rerun()
                if st.button("Barrage Jam", key="arch_node_pre_barrage", use_container_width=True):
                    orch.config.jam_power = float(sel_jam_power)
                    orch.channel.config.jam_power = float(sel_jam_power)
                    orch.set_jam(JamProfile.BARRAGE)
                    st.session_state.last = orch.step()
                    st.rerun()

            _html_block(f"""
            <div class="sleek-card-footer">
              <b>Interference Physics</b>: Injects linear jam power Jk into targeted slots. Total interference per channel is Ik = N0 + Jk.
            </div>
            """)

    # ================= BOX 2: RECEIVER (ES SENSING NODE) =================
    with col_rx:
        with st.container(border=True):
            st.markdown('<div data-node="receiver" style="display:none;"></div>', unsafe_allow_html=True)
            pills_html = "".join(
                f"""<div style="background:{t['ok_bg'] if o['state'] == 'FREE' else (t['deg_bg'] if o['state'] == 'DEGRADED' else t['blk_bg'])};"""
                f"""border:1px solid {t['ok_bd'] if o['state'] == 'FREE' else (t['deg_bd'] if o['state'] == 'DEGRADED' else t['blk_bd'])};"""
                f"""border-radius:5px;padding:0.35rem 0.25rem;text-align:center;">"""
                f"""<div style="font-family:'IBM Plex Mono',monospace;font-weight:700;font-size:0.76rem;color:{t['ok_fg'] if o['state'] == 'FREE' else (t['deg_fg'] if o['state'] == 'DEGRADED' else t['blk_fg'])};">CH{o['channel_id']}</div>"""
                f"""<div style="font-size:0.62rem;font-weight:700;letter-spacing:0.02em;color:{t['ok_fg'] if o['state'] == 'FREE' else (t['deg_fg'] if o['state'] == 'DEGRADED' else t['blk_fg'])};margin-top:0.1rem;">{o['state']}</div>"""
                f"""<div style="font-family:'IBM Plex Mono',monospace;font-size:0.66rem;color:{t['text_muted']};margin-top:0.1rem;">{o['sinr_db']:.1f} dB</div>"""
                f"""</div>"""
                for o in obs
            )
            spectrum_grid_html = f"""<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.35rem;margin-bottom:0.65rem;">{pills_html}</div>"""
            rx_html = f"""
            <div class="node-banner node-banner-rx">
              <div class="node-banner-text">
                <div class="node-banner-title">
                  <span>Receiver (ES Sensing Node)</span>
                </div>
                <div class="node-banner-subtitle">Electronic Support Spectrum Surveillance</div>
              </div>
              <span class="node-banner-badge node-badge-info" style="border-color:#2980b9;color:#2980b9;background:rgba(41,128,185,0.12);letter-spacing:0.04em;">CONTINUOUS SENSING</span>
            </div>
            <div class="sleek-telemetry-grid">
              <div class="telemetry-pill-rx">
                <span class="telemetry-label">FREE Links</span>
                <span class="telemetry-val" style="color:{t['ok_fg']};">{len(free_ids)} {'Channel' if len(free_ids) == 1 else 'Channels'}</span>
              </div>
              <div class="telemetry-pill-rx">
                <span class="telemetry-label">DEGRADED Links</span>
                <span class="telemetry-val" style="color:{t['deg_fg']};">{len(deg_ids)} {'Channel' if len(deg_ids) == 1 else 'Channels'}</span>
              </div>
              <div class="telemetry-pill-rx">
                <span class="telemetry-label">BLOCKED Links</span>
                <span class="telemetry-val" style="color:{t['blk_fg']};">{len(blk_ids)} {'Channel' if len(blk_ids) == 1 else 'Channels'}</span>
              </div>
              <div class="telemetry-pill-rx">
                <span class="telemetry-label">Spectrum Scope</span>
                <span class="telemetry-val">N = {n_ch} CH</span>
              </div>
            </div>
            <table class="node-metric-table">
              <tr><td class="label-col">Cleanest Link</td><td class="val-col" style="color:{t['ok_fg']};">CH{best_ch['channel_id']} ({best_ch['sinr_db']:.1f} dB)</td></tr>
              <tr><td class="label-col">Worst Impaired</td><td class="val-col" style="color:{t['blk_fg'] if worst_ch['sinr_db'] < orch.config.t_bad_db else t['text_strong']};">CH{worst_ch['channel_id']} ({worst_ch['sinr_db']:.1f} dB)</td></tr>
              <tr><td class="label-col">Applied Criteria</td><td class="val-col">FREE &ge; {orch.config.t_good_db:.1f}dB &middot; BLK &lt; {orch.config.t_bad_db:.1f}dB</td></tr>
            </table>

            <div class="sleek-section-divider-rx">
              <span>Channel Spectrum State Map</span>
            </div>
            {spectrum_grid_html}

            <div class="sleek-card-footer">
              <b>ES Sensing Output</b>: Evaluates Signal, Noise, and Jam energy; packages normalized channel observations and current carrier context into <code>CRRequest</code> for cognitive arbitration.
            </div>
            """
            _html_block(rx_html)

    # ================= BOX 3: TRANSMITTER (WITH ATTACHED ML) =================
    with col_tx:
        with st.container(border=True):
            st.markdown('<div data-node="transmitter" style="display:none;"></div>', unsafe_allow_html=True)
            hop_status_text = "Adaptive" if orch.config.hop_enabled else "Single Carrier"
            tx_headroom = max(0.0, orch.config.max_power_db - last.tx_power_db)
            tx_html = f"""
            <div class="node-banner node-banner-tx">
              <div class="node-banner-text">
                <div class="node-banner-title">
                  <span>Transmitter (ECCM Actuator)</span>
                </div>
                <div class="node-banner-subtitle">Adaptive RF Radiator & Attached Recommender</div>
              </div>
              <span class="node-badge-ok node-banner-badge" style="border-color:#27ae60;color:#27ae60;background:rgba(39,174,96,0.12);letter-spacing:0.04em;">RF ACTIVE</span>
            </div>
            <div class="sleek-telemetry-grid">
              <div class="telemetry-pill-tx">
                <span class="telemetry-label">Active Carrier</span>
                <span class="telemetry-val" style="color:{t['hero_title']};">CH{last.tx_channel}</span>
              </div>
              <div class="telemetry-pill-tx">
                <span class="telemetry-label">Transmit Power</span>
                <span class="telemetry-val">{last.tx_power_db:.1f} dB</span>
              </div>
              <div class="telemetry-pill-tx">
                <span class="telemetry-label">Power Headroom</span>
                <span class="telemetry-val">{tx_headroom:.1f} dB</span>
              </div>
              <div class="telemetry-pill-tx">
                <span class="telemetry-label">Hopping Mode</span>
                <span class="telemetry-val">{hop_status_text}</span>
              </div>
            </div>

            <table class="node-metric-table">
              <tr><td class="label-col">Power Range</td><td class="val-col">{orch.config.min_power_db:.1f} dB to {orch.config.max_power_db:.1f} dB</td></tr>
              <tr><td class="label-col">Active Hop Pool</td><td class="val-col">{html.escape(hop)}</td></tr>
            </table>

            <div class="sleek-section-divider-tx">
              <span>Attached Neural Coprocessor</span>
            </div>

            <div class="ml-attached-card" style="border:1.5px solid rgba(39,174,96,0.45);border-left:4px solid #27ae60;border-radius:8px;padding:0.75rem 0.85rem;background:{'rgba(39,174,96,0.06)' if not dark else 'rgba(39,174,96,0.12)'};margin-top:0.4rem;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.45rem;">
                <div class="ml-attached-title" style="margin-bottom:0;color:#27ae60;">
                  Attached ML Policy (MLP Recommender)
                </div>
                <span style="font-family:'IBM Plex Mono',monospace;font-size:0.65rem;padding:0.15rem 0.45rem;border-radius:3px;background:rgba(39,174,96,0.15);color:#27ae60;font-weight:700;border:1px solid rgba(39,174,96,0.35);">
                  NEURAL ENGINE
                </span>
              </div>
              <div style="font-size:0.8rem;line-height:1.55;color:{t['text']};">
                <b>Architecture</b>: Feed-Forward MLP (64 &times; 32, ReLU, Adam)<br/>
                <b>Input Vector</b>: {n_ch * 3 + 2} normalized sensing features<br/>
                <b>Neural Proposal</b>: <span style="font-family:'IBM Plex Mono',monospace;font-weight:700;color:{t['hero_title']};">{ml_pred_text}</span><br/>
                <b>Softmax Confidence</b>: <span style="font-family:'IBM Plex Mono',monospace;font-weight:700;">{ml_conf:.2f} ({int(ml_conf * 100)}%)</span>
                <div style="background:{t['panel_border']};height:5px;border-radius:3px;overflow:hidden;margin:0.35rem 0 0.45rem 0;">
                  <div style="background:linear-gradient(90deg, #27ae60 0%, #2ecc71 100%);width:{int(ml_conf * 100)}%;height:100%;"></div>
                </div>
                <b>Dispatched Action</b>: <span style="font-family:'IBM Plex Mono',monospace;font-weight:600;">{html.escape(action)}</span>
              </div>
            </div>

            <div class="sleek-card-footer">
              <b>ECCM Actuation</b>: Tunes the agile local oscillator to the approved carrier; regulates PA power output and steps hopping phase.
            </div>
            """
            _html_block(tx_html)

    # ================= BOX 4: COMPLETE DECISION EXPLAINABILITY TRACE =================
    st.markdown("---")

    step1_reasoning = (
        f"The ES Receiver evaluated all {n_ch} channels under physical noise, jamming, and path fading. "
        f"Channels were classified against operational thresholds (T_good={orch.config.t_good_db:.1f} dB, T_bad={orch.config.t_bad_db:.1f} dB). "
        f"<b>Resulting state breakdown</b>: {len(free_ids)} FREE channels (highest SINR: CH{best_ch['channel_id']}), "
        f"{len(deg_ids)} DEGRADED channels, and {len(blk_ids)} BLOCKED channels. "
        f"Blocked channels ({', '.join(f'CH{c}' for c in blk_ids) or 'None'}) were flagged as unusable link candidates."
    )

    step2_reasoning = (
        f"The Transmitter's attached Multi-Layer Perceptron (MLP) evaluated the standardized {n_ch * 3 + 2}-dimensional state vector. "
        f"The neural policy computed Softmax probabilities across all {n_ch} channel classes and the power-increase class. "
        f"<b>Neural Model Proposal</b>: <b>{ml_pred_text}</b> with a Softmax confidence score of <b>{ml_conf:.2f} ({int(ml_conf * 100)}%)</b>."
    )

    if engine == "RULES":
        step3_reasoning = (
            f"Decision mode is set to <b>RULES</b>. The engine bypassed neural inference and applied deterministic preference ordering: "
            f"selected the highest-SINR FREE channel (or degraded channel if no free channels exist, or power increase if all blocked)."
        )
    elif "SAFETY" in engine:
        step3_reasoning = (
            f"<b>Safety Override Triggered!</b> The attached ML model proposed an action that violated physical safety constraints "
            f"(such as selecting a channel classified as BLOCKED). The deterministic safety gate intercepted the command and safely substituted "
            f"the highest-SINR usable channel ({channels}). Engine logged as <b>{engine}</b> for audit transparency."
        )
    else:
        step3_reasoning = (
            f"<b>Safety Verified — Approved without override</b>. The ML model's proposed channel ({channels}) was checked against the receiver's BLOCKED list. "
            f"Because the proposed channel is verified usable ({status}) and operating within permissible limits, the safety gate approved the neural recommendation. "
            f"Engine logged as <b>{engine}</b>."
        )

    if orch.config.hop_enabled:
        step4_reasoning = (
            f"Cognitive Adaptive Hopping is <b>ENABLED</b>. The <code>adapt_hop_set</code> routine examined the previous hop pool. "
            f"Any members currently BLOCKED by ECM jamming were evicted from the pool. Vacant slots were refilled with the top-ranked usable channels "
            f"to maintain a balanced target pool of 3 hopping channels. "
            f"<b>Active Hop Pool</b>: <b>{hop}</b>."
        )
    else:
        step4_reasoning = (
            f"Cognitive Frequency Hopping is <b>DISABLED</b>. The transmitter operates on fixed single-carrier allocation. "
            f"No hop-set adaptation was necessary; the transmitter directly tracks the single recommended carrier."
        )

    step5_reasoning = (
        f"The confirmed recommendation was dispatched to the ECCM Transmitter actuator. "
        f"<b>Action Executed</b>: <code>{action}</code> &rarr; Carrier tuned to <b>CH{last.tx_channel}</b> at <b>{last.tx_power_db:.1f} dB</b> output power. "
        f"Decision parameters recorded into the system audit ledger for step {last.step}."
    )

    with st.container(border=True):
        st.markdown('<div data-node="decision" style="display:none;"></div>', unsafe_allow_html=True)
        trace_html = f"""
        <div class="node-banner node-banner-decision">
          <div class="node-banner-text">
            <div class="node-banner-title">
              <span>Cognitive Decision Engine — Full Explainability Trace</span>
            </div>
            <div class="node-banner-subtitle">Autonomous Closed-Loop Sense &rarr; Recommend &rarr; Safety Gate &rarr; Actuate</div>
          </div>
          <div class="node-banner-badge" style="display:flex;align-items:center;gap:0.4rem;">
            <span class="status-pill status-{status}">{status}</span>
            <span class="node-badge-info" style="border-color:#8e44ad;color:#8e44ad;background:rgba(142,68,173,0.12);font-weight:700;">ENGINE: {html.escape(engine)}</span>
          </div>
        </div>

        <div class="message-box" style="margin-bottom:0.9rem;">
          <b>Engine Rationale</b>: {html.escape(resp['message'])}
        </div>

        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:0.55rem;margin-bottom:1rem;">
          <div style="background:{t['panel']};border:1px solid {t['panel_border']};border-left:3px solid #2980b9;border-radius:6px;padding:0.5rem 0.65rem;">
            <div style="color:{t['text_muted']};font-size:0.7rem;text-transform:uppercase;font-weight:600;">Recommended Channel</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:1.05rem;font-weight:700;color:{t['hero_title']};">{html.escape(channels)}</div>
          </div>
          <div style="background:{t['panel']};border:1px solid {t['panel_border']};border-left:3px solid #27ae60;border-radius:6px;padding:0.5rem 0.65rem;">
            <div style="color:{t['text_muted']};font-size:0.7rem;text-transform:uppercase;font-weight:600;">Dispatched Action</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:1.05rem;font-weight:700;color:{t['text_strong']};">{html.escape(action)}</div>
          </div>
          <div style="background:{t['panel']};border:1px solid {t['panel_border']};border-left:3px solid #e0a06a;border-radius:6px;padding:0.5rem 0.65rem;">
            <div style="color:{t['text_muted']};font-size:0.7rem;text-transform:uppercase;font-weight:600;">Power Advice</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:1.05rem;font-weight:700;color:{t['text_strong']};">{html.escape(advice_txt)}</div>
          </div>
          <div style="background:{t['panel']};border:1px solid {t['panel_border']};border-left:3px solid #8e44ad;border-radius:6px;padding:0.5rem 0.65rem;">
            <div style="color:{t['text_muted']};font-size:0.7rem;text-transform:uppercase;font-weight:600;">Active Hop Set</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:1.05rem;font-weight:700;color:{t['text_strong']};">{html.escape(hop)}</div>
          </div>
        </div>

        <div class="trace-step-box">
          <span class="trace-num">1</span><b>Stage 1: Sensing Evidence & Channel Partitioning</b><br/>
          {step1_reasoning}
        </div>

        <div class="trace-step-box">
          <span class="trace-num">2</span><b>Stage 2: Transmitter-Attached ML Policy Inference</b><br/>
          {step2_reasoning}
        </div>

        <div class="trace-step-box">
          <span class="trace-num">3</span><b>Stage 3: Hybrid Safety Gate Verification</b><br/>
          {step3_reasoning}
        </div>

        <div class="trace-step-box">
          <span class="trace-num">4</span><b>Stage 4: Cognitive Adaptive Hop Set Synthesis</b><br/>
          {step4_reasoning}
        </div>

        <div class="trace-step-box">
          <span class="trace-num">5</span><b>Stage 5: Closed-Loop Actuator Command Dispatched</b><br/>
          {step5_reasoning}
        </div>
        """
        _html_block(trace_html)


def main() -> None:
    _init_state()
    orch: Orchestrator = st.session_state.orch

    with st.sidebar:
        st.markdown("### Display View")
        view_opts = ["System Architecture & Node View", "Operator Spectrum View"]
        side_idx = 0 if st.session_state.ui_view == view_opts[0] else 1
        side_view = st.radio(
            "Interface layout",
            options=view_opts,
            index=side_idx,
            key="view_selector_side",
        )
        if side_view != st.session_state.ui_view:
            st.session_state.ui_view = side_view
            st.rerun()

        st.markdown("---")
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
    tokens = get_theme_tokens(st.session_state.theme_mode)

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

    is_arch_view = st.session_state.ui_view == "System Architecture & Node View"

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

        if not is_arch_view:
            jam_power = st.slider(
                "Jam power (linear a.u.)",
                5.0,
                80.0,
                float(orch.config.jam_power),
                1.0,
                help="Relative linear jammer power in the channel model (same scale as noise). Higher values produce stronger interference.",
            )
        else:
            jam_power = float(orch.config.jam_power)

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

        if not is_arch_view:
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
        else:
            st.markdown("---")
            st.caption("**Jammer controls** (profile, power, target channels, and triggers) are integrated directly inside the **Jammer Node**.")

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

    if st.session_state.ui_view == "Operator Spectrum View":
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Simulation step", f"{last.step}")
        m2.metric("Active TX channel", f"CH{last.tx_channel}")
        m3.metric("TX power", f"{last.tx_power_db:.1f} dB")
        m4.metric("Channels (N)", f"{orch.config.n_channels}")
        m5.metric("Jam profile", last.jam_profile)
        render_operator_view(orch, last, dark)
    else:
        render_architecture_view(orch, last, dark, tokens)

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
