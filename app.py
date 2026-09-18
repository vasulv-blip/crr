"""
Cognitive Radio Software Simulation — professional demonstration UI.

Supports Light Mode and Dark Mode.
Run from this directory:
    python -m streamlit run app.py
"""

from __future__ import annotations

import base64
import html
import time
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
div[role="radiogroup"] label,
div[role="radiogroup"] label span,
div[role="radiogroup"] p,
div[role="radiogroup"] [data-testid="stMarkdownContainer"] p,
.stRadio [data-testid="stMarkdownContainer"] p {{
  color: {t['text']} !important;
  -webkit-text-fill-color: {t['text']} !important;
  opacity: 1 !important;
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
  padding: 1.25rem 1.45rem;
  margin-top: 0.75rem;
  margin-bottom: 1.15rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
  box-shadow: {"0 2px 10px rgba(0, 0, 0, 0.04)" if not dark else "0 4px 16px rgba(0, 0, 0, 0.35)"};
}}
.hero-content {{
  flex: 1 1 auto;
  min-width: 0;
  overflow: hidden;
  padding-right: 0.25rem;
}}
.hero-title {{
  color: {t['hero_title']};
  font-size: 1.55rem;
  font-weight: 650;
  margin: 0;
  line-height: 1.25;
}}
.hero-sub {{
  color: {t['hero_sub']};
  margin-top: 0.40rem;
  font-size: 0.78rem;
  line-height: 1.45;
  white-space: nowrap;
}}
.hero-brand {{
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}}
.hero-logo-card {{
  background: #ffffff;
  padding: 0.35rem 0.7rem;
  border-radius: 8px;
  border: 1px solid {"#d5dee7" if not dark else "rgba(255, 255, 255, 0.22)"};
  box-shadow: {"0 2px 8px rgba(0, 0, 0, 0.06)" if not dark else "0 4px 16px rgba(0, 0, 0, 0.45)"};
  display: flex;
  align-items: center;
  justify-content: center;
}}
.hero-logo-img {{
  display: block;
  height: 34px;
  width: auto;
  object-fit: contain;
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
  border: 1.5px solid {"rgba(51, 65, 85, 0.40)" if not dark else "rgba(148, 163, 184, 0.30)"} !important;
  border-top: 4px solid {"#334155" if not dark else "#94a3b8"} !important;
  border-radius: 9px !important;
  background-color: {t['panel']} !important;
  box-shadow: 0 4px 14px {"rgba(30, 41, 59, 0.08)" if not dark else "rgba(0, 0, 0, 0.4)"} !important;
  overflow: hidden !important;
}}

/* Subsystem Banners */
.node-banner {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.85rem;
  padding: 0.65rem 0.85rem;
  border-radius: 7px;
  margin-bottom: 0.75rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  min-width: 0;
  box-sizing: border-box;
}}
.node-banner-main {{
  display: flex;
  align-items: center;
  gap: 0.65rem;
  flex: 1 1 auto;
  min-width: 0;
}}
.node-banner-text {{
  flex: 1 1 auto;
  min-width: 0;
}}
.node-banner-badge {{
  flex: 0 0 auto;
  white-space: nowrap !important;
  align-self: center;
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
  background: {"linear-gradient(135deg, rgba(51, 65, 85, 0.12) 0%, rgba(30, 41, 59, 0.04) 100%)" if not dark else "linear-gradient(135deg, rgba(51, 65, 85, 0.40) 0%, rgba(15, 23, 42, 0.70) 100%)"};
  border: 1px solid {"#cbd5e1" if not dark else "#334155"};
  border-left: 5px solid {"#334155" if not dark else "#94a3b8"};
}}

.node-banner-title {{
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 0.90rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  line-height: 1.25;
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
  color: {"#0f172a" if not dark else "#f8fafc"};
}}

.node-icon-badge {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 8px;
  flex-shrink: 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}}
.node-icon-badge svg,
.node-icon-badge img {{
  display: block;
}}
.node-icon-badge-jam {{
  background: {"rgba(192, 57, 43, 0.14)" if not dark else "rgba(231, 76, 60, 0.25)"};
  color: {"#c0392b" if not dark else "#f1948a"};
  border: 1.5px solid {"rgba(192, 57, 43, 0.35)" if not dark else "rgba(231, 76, 60, 0.45)"};
}}
.node-icon-badge-rx {{
  background: {"rgba(41, 128, 185, 0.14)" if not dark else "rgba(52, 152, 219, 0.25)"};
  color: {"#2980b9" if not dark else "#85c1e9"};
  border: 1.5px solid {"rgba(41, 128, 185, 0.35)" if not dark else "rgba(52, 152, 219, 0.45)"};
}}
.node-icon-badge-tx {{
  background: {"rgba(39, 174, 96, 0.14)" if not dark else "rgba(46, 204, 113, 0.25)"};
  color: {"#27ae60" if not dark else "#82e0aa"};
  border: 1.5px solid {"rgba(39, 174, 96, 0.35)" if not dark else "rgba(46, 204, 113, 0.45)"};
}}
.node-icon-badge-decision {{
  background: {"rgba(51, 65, 85, 0.12)" if not dark else "rgba(148, 163, 184, 0.18)"};
  color: {"#1e293b" if not dark else "#e2e8f0"};
  border: 1.5px solid {"rgba(51, 65, 85, 0.35)" if not dark else "rgba(148, 163, 184, 0.38)"};
}}

.node-banner-subtitle {{
  font-size: 0.71rem;
  color: {t['text_muted']};
  font-weight: 500;
  margin-top: 0.12rem;
  letter-spacing: 0.02em;
  line-height: 1.2;
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
  border-top: 4px solid {"#334155" if not dark else "#94a3b8"};
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
/* Expanders: remove default white header; match panel theme */
div[data-testid="stExpander"],
details[data-testid="stExpander"] {{
  background: {t['panel']} !important;
  border: 1px solid {t['panel_border']} !important;
  border-radius: 8px !important;
  overflow: hidden !important;
}}
div[data-testid="stExpander"] > details,
details[data-testid="stExpander"] {{
  background: {t['panel']} !important;
  border: none !important;
}}
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] [data-testid="stExpanderDetails"],
details[data-testid="stExpander"] > summary,
.streamlit-expanderHeader {{
  background: {t['btn_bg']} !important;
  color: {t['text_strong']} !important;
  border: none !important;
  border-radius: 0 !important;
}}
div[data-testid="stExpander"] summary:hover,
.streamlit-expanderHeader:hover {{
  background: {t['btn_hover']} !important;
  color: {t['text_strong']} !important;
}}
div[data-testid="stExpander"] summary p,
div[data-testid="stExpander"] summary span,
div[data-testid="stExpander"] summary svg,
.streamlit-expanderHeader p,
.streamlit-expanderHeader span,
.streamlit-expanderHeader svg {{
  color: {t['text_strong']} !important;
  fill: {t['text_strong']} !important;
}}
div[data-testid="stExpander"] [data-testid="stExpanderDetails"],
div[data-testid="stExpander"] .streamlit-expanderContent,
details[data-testid="stExpander"] > div {{
  background: {t['panel']} !important;
  border-top: 1px solid {t['panel_border']} !important;
  color: {t['text']} !important;
}}
section[data-testid="stSidebar"] div[data-testid="stExpander"],
section[data-testid="stSidebar"] details[data-testid="stExpander"] {{
  background: {t['input_bg']} !important;
  border: 1px solid {t['input_border']} !important;
}}
section[data-testid="stSidebar"] div[data-testid="stExpander"] summary,
section[data-testid="stSidebar"] .streamlit-expanderHeader {{
  background: {t['btn_bg']} !important;
  color: {t['text_strong']} !important;
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
.theme-right-anchor {{
  display: none;
}}
div[data-testid="column"]:has(.theme-right-anchor) {{
  display: flex !important;
  justify-content: flex-end !important;
}}
div[data-testid="column"]:has(.theme-right-anchor) [data-testid="stRadio"] {{
  width: max-content !important;
  min-width: 11rem !important;
  margin-left: auto !important;
  text-align: right !important;
}}
div[data-testid="column"]:has(.theme-right-anchor) [data-testid="stWidgetLabel"] {{
  justify-content: flex-end !important;
}}
div[data-testid="column"]:has(.theme-right-anchor) div[role="radiogroup"] {{
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  align-items: center !important;
  justify-content: flex-end !important;
  gap: 0.75rem !important;
}}
div[data-testid="column"]:has(.theme-right-anchor) div[role="radiogroup"] > label,
div[data-testid="column"]:has(.theme-right-anchor) div[role="radiogroup"] > div {{
  margin: 0 !important;
  white-space: nowrap !important;
}}
div[data-testid="column"]:has(.theme-right-anchor) [data-testid="stRadio"] label,
div[data-testid="column"]:has(.theme-right-anchor) [data-testid="stRadio"] label span,
div[data-testid="column"]:has(.theme-right-anchor) [data-testid="stRadio"] p,
div[data-testid="column"]:has(.theme-right-anchor) [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p,
div[data-testid="column"]:has(.theme-right-anchor) div[role="radiogroup"] label,
div[data-testid="column"]:has(.theme-right-anchor) div[role="radiogroup"] label span,
div[data-testid="column"]:has(.theme-right-anchor) div[role="radiogroup"] p {{
  color: {t['text']} !important;
  -webkit-text-fill-color: {t['text']} !important;
  opacity: 1 !important;
}}
.logout-banner {{
  border: 1px solid {t['ok_bd']};
  background: {t['ok_bg']};
  color: {t['ok_fg']};
  border-radius: 8px;
  padding: 0.65rem 0.85rem;
  margin: 0.35rem 0 0.75rem;
  font-family: 'IBM Plex Sans', sans-serif;
  font-weight: 650;
  font-size: 0.95rem;
  text-align: center;
}}
/* Compact centred logout modal (st.dialog) */
div[data-testid="stDialog"] {{
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}}
div[data-testid="stDialog"] > div {{
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 100% !important;
  height: 100% !important;
}}
div[data-testid="stDialog"] div[role="dialog"] {{
  position: relative !important;
  top: auto !important;
  left: auto !important;
  transform: none !important;
  width: 280px !important;
  max-width: 280px !important;
  margin: 0 auto !important;
  padding: 0.85rem 0.95rem 0.75rem !important;
}}
div[data-testid="stDialog"] [data-testid="stVerticalBlock"] {{
  gap: 0.35rem !important;
}}
div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] p {{
  margin: 0.15rem 0 0.35rem !important;
  font-size: 0.92rem !important;
}}
div[data-testid="stDialog"] div.stButton {{
  display: flex !important;
  justify-content: center !important;
}}
div[data-testid="stDialog"] div.stButton > button {{
  min-width: 72px !important;
  width: auto !important;
  padding: 0.35rem 1.1rem !important;
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


# Simple demo credentials for the defence presentation login gate.
DEMO_USERNAME = "pocuser"
DEMO_PASSWORD = "poc123"
# Audience organisations shown on the login screen. Add more names later as needed.
DEMO_AUDIENCE_ORGS = ["Defense Labs"]


def _init_auth_state() -> None:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "logout_notice" not in st.session_state:
        st.session_state.logout_notice = False
    if "login_error" not in st.session_state:
        st.session_state.login_error = ""
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "Dark"


def _init_state() -> None:
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "Dark"
    if "ui_view" not in st.session_state:
        st.session_state.ui_view = "System Architecture & Node View"
    if "orch" not in st.session_state:
        cfg = SimConfig(n_channels=8, decision_mode=DecisionMode.HYBRID, hop_enabled=False)
        orch = Orchestrator(cfg)
        # Fewer samples on first boot so Streamlit Community Cloud cold-starts stay responsive.
        with st.spinner("Training ML recommender (first load)..."):
            orch.train_ml(400)
        st.session_state.orch = orch
        st.session_state.last = orch.step()
        st.session_state.log = []


def _login_css(mode: str) -> str:
    dark = mode == "Dark"
    if dark:
        app_bg = "linear-gradient(180deg, #0a1520 0%, #0f1f2e 45%, #122433 100%)"
        hero_bg = "linear-gradient(135deg, #102032 0%, #163047 100%)"
        hero_border = "#2a4256"
        hero_title = "#f5f8fa"
        hero_sub = "#b7c7d4"
        hero_shadow = "0 4px 16px rgba(0, 0, 0, 0.35)"
        logo_border = "rgba(255, 255, 255, 0.22)"
        logo_shadow = "0 4px 16px rgba(0, 0, 0, 0.45)"
        panel_bg = "#132536"
        panel_border = "#2a4256"
        brief = "#5ec8ff"
        indigenous_fg = "#0b1c2c"
        indigenous_bd = "rgba(255, 255, 255, 0.35)"
        indigenous_bg = "linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%)"
        footer = "#7f94a5"
        chrome_border = "#243647"
        logout_bg = "#163528"
        logout_fg = "#7dcea0"
        logout_bd = "#2f6b4f"
        input_bg = "#132536"
        input_border = "#2a4256"
        input_text = "#e6edf2"
        label = "#e6edf2"
        btn_bg = "#2a5f7a"
        btn_border = "#3d7ea0"
    else:
        app_bg = "linear-gradient(180deg, #f4f7fa 0%, #eef3f7 45%, #e8eef4 100%)"
        hero_bg = "linear-gradient(135deg, #ffffff 0%, #eef4f8 100%)"
        hero_border = "#cfdbe6"
        hero_title = "#0b2a5b"
        hero_sub = "#3d5266"
        hero_shadow = "0 2px 10px rgba(0, 0, 0, 0.04)"
        logo_border = "#d5dee7"
        logo_shadow = "0 2px 8px rgba(0, 0, 0, 0.06)"
        panel_bg = "#ffffff"
        panel_border = "#d0dbe6"
        brief = "#0b6e99"
        indigenous_fg = "#0b1c2c"
        indigenous_bd = "#8fa6b8"
        indigenous_bg = "linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%)"
        footer = "#6a7f92"
        chrome_border = "#d5dee7"
        logout_bg = "#e7f5ec"
        logout_fg = "#1b6b3a"
        logout_bd = "#8fc9a5"
        input_bg = "#ffffff"
        input_border = "#c5d0db"
        input_text = "#1a2b3c"
        label = "#1a2b3c"
        btn_bg = "#1e4f68"
        btn_border = "#1e4f68"

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');
html, body, [class*="css"] {{
  font-family: 'IBM Plex Sans', sans-serif;
  color: {label};
}}
.stApp {{
  background: {app_bg};
}}
section[data-testid="stSidebar"] {{ display: none !important; }}
div[data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}
.block-container {{
  padding-top: 1.2rem !important;
  padding-bottom: 5.5rem !important;
  max-width: 1100px !important;
  min-height: 100vh !important;
}}
.hero {{
  border: 1px solid {hero_border};
  background: {hero_bg};
  border-radius: 8px;
  padding: 1.1rem 1.3rem;
  margin-top: 0.2rem;
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.25rem;
  box-shadow: {hero_shadow};
}}
.hero-content {{
  flex: 1 1 auto;
  min-width: 0;
  overflow: hidden;
  padding-right: 0.25rem;
}}
.hero-title {{
  color: {hero_title};
  font-size: 1.35rem;
  font-weight: 650;
  margin: 0;
  line-height: 1.25;
}}
.hero-sub {{
  color: {hero_sub};
  margin-top: 0.35rem;
  font-size: 0.76rem;
  line-height: 1.45;
  white-space: nowrap;
}}
.hero-brand {{
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}}
.hero-logo-card {{
  background: #ffffff;
  padding: 0.35rem 0.7rem;
  border-radius: 8px;
  border: 1px solid {logo_border};
  box-shadow: {logo_shadow};
  display: flex;
  align-items: center;
  justify-content: center;
}}
.hero-logo-img {{
  display: block;
  height: 34px;
  width: auto;
  object-fit: contain;
}}
.login-spacer {{
  height: clamp(0.85rem, 5vh, 3rem);
}}
.indigenous-badge {{
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.55rem;
  width: 100%;
  margin: 0.85rem auto 0;
  padding: 0.5rem 0.85rem;
  border: 1px solid {indigenous_bd};
  border-radius: 999px;
  background: {indigenous_bg};
  box-shadow: {hero_shadow};
  box-sizing: border-box;
}}
.indigenous-mark {{
  display: none;
}}
.indigenous-text {{
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.01em;
  color: {indigenous_fg};
  line-height: 1.2;
  text-align: center;
  white-space: nowrap;
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.35);
}}
.login-panel {{
  border: 1px solid {panel_border};
  background: {panel_bg};
  border-radius: 8px 8px 0 0;
  border-bottom: none;
  padding: 1.15rem 1.25rem 0.7rem;
  margin: 0 auto;
  text-align: center;
}}
.login-brief {{
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 0.95rem;
  line-height: 1.45;
  color: {brief};
  margin: 0;
  font-weight: 600;
  letter-spacing: 0.02em;
}}
.login-brief b {{
  color: {brief};
  font-weight: 700;
}}
div[data-testid="stForm"] {{
  border: 1px solid {panel_border} !important;
  border-top: 1px solid {panel_border} !important;
  border-radius: 0 0 8px 8px !important;
  background: {panel_bg} !important;
  padding: 0.65rem 1.25rem 1.15rem !important;
  margin-top: 0 !important;
}}
.logout-banner {{
  border: 1px solid {logout_bd};
  background: {logout_bg};
  color: {logout_fg};
  border-radius: 8px;
  padding: 0.55rem 0.75rem;
  margin-bottom: 0.7rem;
  font-family: 'IBM Plex Sans', sans-serif;
  font-weight: 650;
  font-size: 0.9rem;
  text-align: center;
}}
.footer-note {{
  position: fixed !important;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 40;
  color: {footer};
  font-size: 0.78rem;
  border-top: 1px solid {chrome_border};
  margin: 0 !important;
  padding: 0.7rem 1.5rem 0.85rem !important;
  line-height: 1.45;
  background: {"rgba(10, 21, 32, 0.96)" if dark else "rgba(244, 247, 250, 0.97)"};
}}
div[data-testid="stHorizontalBlock"]:has(.theme-right-anchor) {{
  justify-content: flex-end !important;
}}
.theme-right-anchor {{
  display: none;
}}
div[data-testid="column"]:has(.theme-right-anchor) {{
  display: flex !important;
  justify-content: flex-end !important;
}}
div[data-testid="column"]:has(.theme-right-anchor) [data-testid="stRadio"] {{
  width: max-content !important;
  min-width: 11rem !important;
  margin-left: auto !important;
  text-align: right !important;
}}
div[data-testid="column"]:has(.theme-right-anchor) [data-testid="stWidgetLabel"] {{
  justify-content: flex-end !important;
}}
div[data-testid="column"]:has(.theme-right-anchor) div[role="radiogroup"] {{
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  align-items: center !important;
  justify-content: flex-end !important;
  gap: 0.75rem !important;
}}
div[data-testid="column"]:has(.theme-right-anchor) div[role="radiogroup"] > label,
div[data-testid="column"]:has(.theme-right-anchor) div[role="radiogroup"] > div {{
  margin: 0 !important;
  white-space: nowrap !important;
}}
.stTextInput label,
.stRadio label,
.stRadio [data-testid="stWidgetLabel"] p,
.stRadio [data-testid="stMarkdownContainer"] p,
div[role="radiogroup"] label,
div[role="radiogroup"] label span,
div[role="radiogroup"] p {{
  color: {label} !important;
  -webkit-text-fill-color: {label} !important;
  opacity: 1 !important;
}}
div[data-baseweb="radio"] label,
div[data-baseweb="radio"] span {{
  color: {label} !important;
  -webkit-text-fill-color: {label} !important;
}}
div[data-baseweb="input"] > div,
div[data-baseweb="base-input"],
.stTextInput input {{
  background-color: {input_bg} !important;
  color: {input_text} !important;
  border-color: {input_border} !important;
}}
button[kind="primary"],
button[data-testid="baseButton-primary"],
button[data-testid="stBaseButton-primary"],
div.stButton > button[kind="primary"] {{
  background-color: {btn_bg} !important;
  border: 1px solid {btn_border} !important;
  color: #ffffff !important;
}}
button[kind="primary"] *,
button[data-testid="baseButton-primary"] *,
button[data-testid="stBaseButton-primary"] * {{
  color: #ffffff !important;
}}
</style>
"""


def _audience_brief_html() -> str:
    """Build login audience line from DEMO_AUDIENCE_ORGS (extend that list to add orgs)."""
    orgs = [str(o).strip() for o in DEMO_AUDIENCE_ORGS if str(o).strip()]
    if not orgs:
        return "Demo for defence organisations"
    if len(orgs) == 1:
        return f'Demo for <b>{html.escape(orgs[0])}</b>'
    if len(orgs) == 2:
        return f'Demo for <b>{html.escape(orgs[0])}</b> and <b>{html.escape(orgs[1])}</b>'
    listed = ", ".join(f"<b>{html.escape(o)}</b>" for o in orgs[:-1])
    return f"Demo for {listed}, and <b>{html.escape(orgs[-1])}</b>"


def render_login_screen() -> None:
    """Simple branded login gate before the Cognitive Radio demo."""
    theme_mode = st.session_state.theme_mode
    st.markdown(
        f'<div id="cr-theme-root" data-theme="{theme_mode.lower()}"></div>',
        unsafe_allow_html=True,
    )
    st.markdown(_login_css(theme_mode), unsafe_allow_html=True)

    _theme_spacer, theme_col = st.columns([5, 2])
    with theme_col:
        st.markdown('<div class="theme-right-anchor"></div>', unsafe_allow_html=True)
        theme_mode = st.radio(
            "Theme",
            options=["Light", "Dark"],
            index=0 if st.session_state.theme_mode == "Light" else 1,
            horizontal=True,
            key="login_theme_radio",
            label_visibility="collapsed",
        )
        if theme_mode != st.session_state.theme_mode:
            st.session_state.theme_mode = theme_mode
            st.rerun()

    logo_uri = _get_logo_data_uri()
    logo_brand_html = (
        f"""<div class="hero-brand">
          <div class="hero-logo-card">
            <img src="{logo_uri}" alt="eAge" class="hero-logo-img" />
          </div>
        </div>"""
        if logo_uri
        else ""
    )

    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-content">
            <div class="hero-title">Cognitive Radio Channel Selection under Jamming</div>
            <div class="hero-sub">
              Channel simulation · measurement-based receiver · CR decision (rules / ML / hybrid) · adaptive hopping · power advice
            </div>
          </div>
          {logo_brand_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="login-spacer"></div>', unsafe_allow_html=True)

    left, mid, right = st.columns([1.35, 1.2, 1.35])
    with mid:
        st.markdown(
            f"""
            <div class="login-panel">
              <div class="login-brief">{_audience_brief_html()}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.form("cr_login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Login", type="primary", use_container_width=True)

        if submitted:
            if username.strip() == DEMO_USERNAME and password == DEMO_PASSWORD:
                st.session_state.authenticated = True
                st.session_state.login_error = ""
                st.session_state.logout_notice = False
                st.rerun()
            else:
                st.session_state.login_error = "Invalid username or password."

        if st.session_state.login_error:
            st.error(st.session_state.login_error)

        st.markdown(
            """
            <div class="indigenous-badge">
              <div class="indigenous-mark" aria-hidden="true"></div>
              <div class="indigenous-text">Indigenously&nbsp;made&nbsp;for&nbsp;Indian&nbsp;Defence&nbsp;Labs</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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


def do_logout() -> None:
    """Open Logged out modal on the post-login screen, then return to login."""
    st.session_state.logout_notice = True
    st.session_state.login_error = ""
    st.rerun()


def logged_out_dialog() -> None:
    """Compact centred logout modal on the post-login screen, then return to login."""
    dark = st.session_state.theme_mode == "Dark"
    card_bg = "#132536" if dark else "#ffffff"
    card_bd = "#2a4256" if dark else "#d0dbe6"
    title_c = "#f5f8fa" if dark else "#0b2a5b"
    body_c = "#b7c7d4" if dark else "#3d5266"
    btn_bg = "#1a3348" if dark else "#d8e4ee"
    btn_bd = "#3d5a70" if dark else "#8fa6b8"
    btn_fg = "#eef4f8" if dark else "#0b1c2c"
    st.markdown(
        f"""
<style>
.cr-logout-overlay {{
  position: fixed;
  inset: 0;
  background: rgba(5, 12, 20, 0.55);
  z-index: 10050;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.cr-logout-card {{
  background: {card_bg};
  border: 2px solid {card_bd};
  border-radius: 10px;
  width: 340px;
  max-width: 90vw;
  height: 148px;
  box-sizing: border-box;
  padding: 1.35rem 1.2rem 0;
  box-shadow: 0 14px 40px rgba(0, 0, 0, 0.35);
  text-align: center;
}}
.cr-logout-card p {{
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: {title_c};
  font-family: 'IBM Plex Sans', sans-serif;
}}
.st-key-logout_ok_btn {{
  position: fixed !important;
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, 22px) !important;
  z-index: 10060 !important;
  width: 96px !important;
}}
.st-key-logout_ok_btn div.stButton > button,
.st-key-logout_ok_btn div.stButton > button[kind="secondary"],
.st-key-logout_ok_btn div.stButton > button[kind="primary"] {{
  width: 96px !important;
  min-height: 2rem !important;
  padding: 0.28rem 0.7rem !important;
  background-color: {btn_bg} !important;
  background-image: none !important;
  border: 1px solid {btn_bd} !important;
  color: {btn_fg} !important;
}}
.st-key-logout_ok_btn div.stButton > button *,
.st-key-logout_ok_btn div.stButton > button[kind="primary"] * {{
  color: {btn_fg} !important;
  -webkit-text-fill-color: {btn_fg} !important;
}}
</style>
<div class="cr-logout-overlay">
  <div class="cr-logout-card">
    <p>You have been logged out.</p>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("OK", key="logout_ok_btn"):
        st.session_state.logout_notice = False
        st.session_state.authenticated = False
        st.rerun()


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


def _svg_data_uri(svg_code: str) -> str:
    b64 = base64.b64encode(svg_code.strip().encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{b64}"


def _get_logo_data_uri() -> str:
    candidates = [
        ROOT / "assets" / "eage_logo_hires.png",
        ROOT / "assets" / "eage_logo_cropped.png",
        ROOT / "assets" / "eage_logo.png",
    ]
    for p in candidates:
        if p.exists():
            data = p.read_bytes()
            b64 = base64.b64encode(data).decode("ascii")
            return f"data:image/png;base64,{b64}"
    return ""


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

    # Professional defense/aero-grade vector SVG icons
    clr_jam = "#c0392b" if not dark else "#f1948a"
    clr_rx = "#2980b9" if not dark else "#85c1e9"
    clr_tx = "#27ae60" if not dark else "#82e0aa"
    clr_decision = "#1e293b" if not dark else "#e2e8f0"

    svg_jam = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" '
        f'stroke="{clr_jam}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="M4.93 4.93a10 10 0 0 1 14.14 0"/>'
        f'<path d="M7.76 7.76a6 6 0 0 1 8.48 0"/>'
        f'<circle cx="12" cy="12" r="2.5" fill="{clr_jam}"/>'
        f'<line x1="2" y1="2" x2="22" y2="22"/>'
        f'</svg>'
    )
    svg_rx = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" '
        f'stroke="{clr_rx}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="M4 10a7.31 7.31 0 0 0 10 10Z"/>'
        f'<path d="m9 15 3-3 1 1-3 3Z"/>'
        f'<path d="M17 13a6 6 0 0 0-6-6"/>'
        f'<path d="M21 13A10 10 0 0 0 11 3"/>'
        f'</svg>'
    )
    svg_tx = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" '
        f'stroke="{clr_tx}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="M4.9 16.1C1 12.2 1 5.8 4.9 1.9"/>'
        f'<path d="M7.8 13.2a6 6 0 0 1 0-8.5"/>'
        f'<circle cx="12" cy="9" r="2" fill="{clr_tx}"/>'
        f'<path d="M16.2 4.8a6 6 0 0 1 0 8.5"/>'
        f'<path d="M19.1 1.9a10 10 0 0 1 0 14.2"/>'
        f'<path d="M12 11v11"/>'
        f'<path d="M9 22h6"/>'
        f'</svg>'
    )
    svg_ml = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" '
        f'stroke="{clr_tx}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        f'<rect x="4" y="4" width="16" height="16" rx="2"/>'
        f'<rect x="9" y="9" width="6" height="6"/>'
        f'<path d="M15 2v2M9 2v2M15 20v2M9 20v2M2 15h2M2 9h2M20 15h2M20 9h2"/>'
        f'</svg>'
    )
    svg_decision = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" '
        f'stroke="{clr_decision}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        f'<rect width="18" height="18" x="3" y="3" rx="2"/>'
        f'<path d="M11 9h4a2 2 0 0 0 2-2V3"/>'
        f'<circle cx="9" cy="9" r="2"/>'
        f'<path d="M7 21v-4a2 2 0 0 1 2-2h4"/>'
        f'<circle cx="15" cy="15" r="2"/>'
        f'</svg>'
    )

    icon_jam = f'<span class="node-icon-badge node-icon-badge-jam"><img width="22" height="22" style="display:block;" src="{_svg_data_uri(svg_jam)}" alt="Jammer"/></span>'
    icon_rx = f'<span class="node-icon-badge node-icon-badge-rx"><img width="22" height="22" style="display:block;" src="{_svg_data_uri(svg_rx)}" alt="Receiver"/></span>'
    icon_tx = f'<span class="node-icon-badge node-icon-badge-tx"><img width="22" height="22" style="display:block;" src="{_svg_data_uri(svg_tx)}" alt="Transmitter"/></span>'
    icon_ml = f'<span class="node-icon-badge node-icon-badge-tx" style="width:28px;height:28px;border-radius:6px;"><img width="15" height="15" style="display:block;" src="{_svg_data_uri(svg_ml)}" alt="ML"/></span>'
    icon_decision = f'<span class="node-icon-badge node-icon-badge-decision"><img width="22" height="22" style="display:block;" src="{_svg_data_uri(svg_decision)}" alt="Decision Engine"/></span>'

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
              <div class="node-banner-main">
                {icon_jam}
                <div class="node-banner-text">
                  <div class="node-banner-title">Jammer (ECM Threat Node)</div>
                  <div class="node-banner-subtitle">Adversary Electronic Attack & Interference</div>
                </div>
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

            with st.expander("Quick Threat Presets (optional)", expanded=False):
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
              <div class="node-banner-main">
                {icon_rx}
                <div class="node-banner-text">
                  <div class="node-banner-title">Receiver (ES Sensing Node)</div>
                  <div class="node-banner-subtitle">Electronic Support Spectrum Surveillance</div>
                </div>
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
              <div class="node-banner-main">
                {icon_tx}
                <div class="node-banner-text">
                  <div class="node-banner-title">Transmitter (ECCM Actuator)</div>
                  <div class="node-banner-subtitle">Adaptive RF Radiator & Attached Recommender</div>
                </div>
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
                <div class="ml-attached-title" style="margin-bottom:0;color:#27ae60;display:flex;align-items:center;gap:0.45rem;">
                  {icon_ml}
                  <span>Attached ML Policy (MLP Recommender)</span>
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
          <div class="node-banner-main">
            {icon_decision}
            <div class="node-banner-text">
              <div class="node-banner-title">Cognitive Decision Engine — Full Explainability Trace</div>
              <div class="node-banner-subtitle">Autonomous Closed-Loop Sense &rarr; Recommend &rarr; Safety Gate &rarr; Actuate</div>
            </div>
          </div>
          <div class="node-banner-badge" style="display:flex;align-items:center;gap:0.4rem;">
            <span class="status-pill status-{status}">{status}</span>
            <span class="node-badge-info" style="border-color:{'#334155' if not dark else '#64748b'};color:{'#0f172a' if not dark else '#e2e8f0'};background:{'rgba(51, 65, 85, 0.10)' if not dark else 'rgba(148, 163, 184, 0.14)'};font-weight:700;letter-spacing:0.04em;">ENGINE: {html.escape(engine)}</span>
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
          <div style="background:{t['panel']};border:1px solid {t['panel_border']};border-left:3px solid {'#334155' if not dark else '#94a3b8'};border-radius:6px;padding:0.5rem 0.65rem;">
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
    _init_auth_state()
    if not st.session_state.authenticated:
        render_login_screen()
        return

    _init_state()
    orch: Orchestrator = st.session_state.orch

    with st.sidebar:
        st.markdown("### User")
        st.caption(f"Signed in as `{DEMO_USERNAME}`")
        if st.button("Logout", use_container_width=True, key="sidebar_logout_btn"):
            do_logout()

        st.markdown("---")
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

    dark = st.session_state.theme_mode == "Dark"
    tokens = get_theme_tokens(st.session_state.theme_mode)

    st.markdown(
        f'<div id="cr-theme-root" data-theme="{st.session_state.theme_mode.lower()}"></div>',
        unsafe_allow_html=True,
    )
    st.markdown(theme_css(st.session_state.theme_mode), unsafe_allow_html=True)

    if st.session_state.logout_notice:
        logged_out_dialog()

    _theme_spacer, theme_col = st.columns([5, 2])
    with theme_col:
        st.markdown('<div class="theme-right-anchor"></div>', unsafe_allow_html=True)
        theme_mode = st.radio(
            "Theme",
            options=["Light", "Dark"],
            index=0 if st.session_state.theme_mode == "Light" else 1,
            horizontal=True,
            key="main_theme_radio",
            label_visibility="collapsed",
            help="Switch between light mode and dark mode.",
        )
        if theme_mode != st.session_state.theme_mode:
            st.session_state.theme_mode = theme_mode
            st.rerun()

    logo_uri = _get_logo_data_uri()
    logo_brand_html = (
        f"""<div class="hero-brand">
          <div class="hero-logo-card">
            <img src="{logo_uri}" alt="eAge Innovations" class="hero-logo-img" />
          </div>
        </div>"""
        if logo_uri
        else ""
    )

    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-content">
            <div class="hero-title">Cognitive Radio Channel Selection under Jamming</div>
            <div class="hero-sub">
              Channel simulation · measurement-based receiver · CR decision (rules / ML / hybrid) · adaptive hopping · power advice
            </div>
          </div>
          {logo_brand_html}
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
        seed = int(orch.config.seed)
        with st.expander("Seed / reproducibility (optional)", expanded=False):
            seed = int(
                st.number_input(
                    "Seed",
                    min_value=0,
                    max_value=999999,
                    value=int(orch.config.seed),
                    step=1,
                    key="sidebar_seed_input",
                )
            )

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
