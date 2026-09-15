#!/usr/bin/env python3
"""
Build Comprehensive Word Document for Shri S. K. Sir and Senior Defence Scientists:
Cognitive Radio Channel Selection Under Contested Electronic Warfare (EW) Scenarios.
Operational, Algorithmic, and Mathematical Breakdown of Jammer, Receiver, ML Policy, and Transmitter.
Strict decimal hierarchical numbering throughout (No bullet points).
"""

import os
from pathlib import Path
import docx
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "eage_logo_hires.png"
DIAGRAM_PATH = ASSETS_DIR / "system_architecture_block_diagram.png"
OUT_DOCX = BASE_DIR / "Cognitive_Radio_Simulation_Scenarios_Brief_for_SK_Sir.docx"

# Palette definitions (Professional Defence / C2 Style)
NAVY_PRIMARY = RGBColor(0x0B, 0x2A, 0x5B)     # #0B2A5B Deep Strategic Navy
SLATE_TITLE  = RGBColor(0x1E, 0x29, 0x3B)     # #1E293B Slate 800
BODY_DARK    = RGBColor(0x1F, 0x29, 0x37)     # #1F2937 Neutral Body Dark
GRAY_MUTED   = RGBColor(0x64, 0x74, 0x8B)     # #64748B Slate Muted
RED_JAM      = RGBColor(0xB9, 0x1C, 0x1C)     # #B91C1C Jammer Threat
BLUE_RX      = RGBColor(0x03, 0x69, 0xA1)     # #0369A1 Receiver Sensing
GREEN_TX     = RGBColor(0x15, 0x80, 0x3D)     # #15803D Transmitter Actuation
PURPLE_C2    = RGBColor(0x33, 0x41, 0x55)     # #334155 Decision Engine


def set_run_font(run, size_pt=10.5, bold=False, italic=False, color=BODY_DARK, font_name="Calibri"):
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color


def add_p(doc, text="", size_pt=10.5, bold=False, italic=False, color=BODY_DARK, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if text:
        r = p.add_run(text)
        set_run_font(r, size_pt=size_pt, bold=bold, italic=italic, color=color)
    return p


def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, size_pt=13.5, bold=True, color=NAVY_PRIMARY)
    return p


def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, size_pt=11.5, bold=True, color=SLATE_TITLE)
    return p


def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, size_pt=10.5, bold=True, color=RGBColor(0x33, 0x41, 0x55))
    return p


def add_numbered_clause(doc, num_str, title_str="", text_str="", size_pt=10.0, num_bold=True, num_color=NAVY_PRIMARY, title_color=SLATE_TITLE, indent_in=0.35):
    """Clean hanging indent numbered clause for military specifications."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent_in)
    p.paragraph_format.first_line_indent = Inches(-indent_in)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    
    r_num = p.add_run(f"{num_str} ")
    set_run_font(r_num, size_pt=size_pt, bold=num_bold, color=num_color)
    
    if title_str:
        r_title = p.add_run(f"{title_str} ")
        set_run_font(r_title, size_pt=size_pt, bold=True, color=title_color)
        
    if text_str:
        r_text = p.add_run(text_str)
        set_run_font(r_text, size_pt=size_pt, bold=False, color=BODY_DARK)
    return p


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("w:top", top), ("w:bottom", bottom), ("w:left", left), ("w:right", right)]:
        node = OxmlElement(m)
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def add_callout_box(doc, text, title="DEFENCE SCIENTIFIC TAKEAWAY", border_color="0B2A5B", bg_color="F8FAFC"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    set_cell_shading(cell, bg_color)
    
    # Left border thick, others none
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="30" w:color="{border_color}"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if title:
        r_title = p.add_run(f"[{title}] ")
        set_run_font(r_title, size_pt=9.5, bold=True, color=NAVY_PRIMARY)
    r_text = p.add_run(text)
    set_run_font(r_text, size_pt=9.5, bold=False, italic=False, color=BODY_DARK)
    
    # Spacing after table
    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(4)


def build_document():
    doc = Document()
    
    # Page setup: Standard A4 / Letter margins (0.75" top/bottom, 0.8" left/right)
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # ---------------------------------------------------------
    # HEADER BANNER WITH EAGE LOGO & METADATA
    # ---------------------------------------------------------
    header_table = doc.add_table(rows=1, cols=2)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_table.autofit = False
    header_table.columns[0].width = Inches(5.1)
    header_table.columns[1].width = Inches(1.7)
    
    left_cell = header_table.cell(0, 0)
    right_cell = header_table.cell(0, 1)
    set_cell_margins(left_cell, top=50, bottom=50, left=0, right=100)
    set_cell_margins(right_cell, top=50, bottom=50, left=50, right=0)
    
    p_org = left_cell.paragraphs[0]
    p_org.paragraph_format.space_after = Pt(2)
    r_org = p_org.add_run("eAge Innovations — Defence SDR & Electronic Warfare Lab")
    set_run_font(r_org, size_pt=10, bold=True, color=NAVY_PRIMARY)
    
    p_meta = left_cell.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(0)
    r_meta = p_meta.add_run("Reference: EAGE-CR-EW-2026-DOC-004 | Target: Shri S. K. Sir & Defence Scientists | September 2026")
    set_run_font(r_meta, size_pt=8.5, bold=False, color=GRAY_MUTED)

    if LOGO_PATH.exists():
        p_logo = right_cell.paragraphs[0]
        p_logo.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_logo.paragraph_format.space_after = Pt(0)
        p_logo.add_run().add_picture(str(LOGO_PATH), width=Inches(1.5))

    # Divider line
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(4)
    p_div.paragraph_format.space_after = Pt(12)
    p_div_border = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="18" w:space="1" w:color="0B2A5B"/></w:pBdr>')
    p_div._element.get_or_add_pPr().append(p_div_border)

    # Document Main Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(3)
    r_title = p_title.add_run("COGNITIVE RADIO CHANNEL SELECTION UNDER HOSTILE JAMMING")
    set_run_font(r_title, size_pt=17, bold=True, color=NAVY_PRIMARY)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("Comprehensive Scenario Operational Breakdown: Jammer Dynamics, ES Sensing, Neural Recommender (ML) Decision Logic, and Agile ECCM Transmitter Actuation")
    set_run_font(r_sub, size_pt=11, bold=True, color=SLATE_TITLE)

    # Note to Reviewers
    add_callout_box(
        doc,
        "This technical document has been authored specifically for Shri S. K. Sir and distinguished defence scientists. "
        "It provides a rigorous, hierarchically numbered scenario-by-scenario analysis of the closed-loop Cognitive Radio (CR) software demonstrator developed by eAge Innovations. "
        "For each operational scenario, the document strictly details: (1) what the ECM Jammer generates, (2) what the ES Receiver senses, (3) how the transmitter-attached "
        "ML Recommender derives its candidate decision and passes through the deterministic safety gate, and (4) what the agile ECCM Transmitter actuates to maintain "
        "uninterrupted military communications.",
        title="SPECIAL BRIEFING FOR SHRI S. K. SIR & SENIOR DEFENCE SCIENTISTS",
        border_color="0B2A5B",
        bg_color="F0F4F8"
    )

    # ---------------------------------------------------------
    # SECTION 1: SYSTEM ARCHITECTURAL BLOCK DIAGRAM & OVERALL SCENARIO
    # ---------------------------------------------------------
    add_heading_1(doc, "1. Overall System Architecture & Closed-Loop Operational Cycle")
    
    add_p(
        doc,
        "Modern Electronic Warfare (EW) environments are characterized by rapid, dynamic, and adaptive Electronic Attack (EA). "
        "Legacy military transceivers rely on pre-planned fixed frequency allocations or static pseudo-random frequency-hopping (PRFH) sequences. "
        "When an adversary deploys intelligent, reactive, or wideband sweeping ECM, pre-programmed hopping patterns quickly suffer packet collision "
        "and catastrophic communication denial. The eAge Cognitive Radio system achieves mission resilience by closing an autonomous, real-time "
        "Sense-Decide-Act-Learn loop without human-in-the-loop latency."
    )

    # Embed Architecture Block Diagram
    if DIAGRAM_PATH.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(str(DIAGRAM_PATH), width=Inches(6.8))

        p_caption = doc.add_paragraph()
        p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_caption.paragraph_format.space_after = Pt(12)
        r_cap = p_caption.add_run("Figure 1: High-Fidelity Closed-Loop Cognitive Radio Architecture under Hostile Electronic Contestation.")
        set_run_font(r_cap, size_pt=9, bold=True, italic=True, color=GRAY_MUTED)

    add_heading_2(doc, "1.1 Core Subsystems and Information Flow")
    add_p(
        doc,
        "As depicted in Figure 1, the demonstrator comprises five tightly coupled functional subsystems interacting over a contested electromagnetic medium:"
    )

    add_numbered_clause(doc, "1.1.1", "Jammer (ECM Threat Node — Red Identity):", "Simulates the adversary electronic attack entity. Generates parametrized jamming waveforms (Spot, Multi-Spot, Swept Chirp, and Barrage noise) injecting localized or wideband interference power J_k into targeted radio slots.")
    add_numbered_clause(doc, "1.1.2", "Contested RF Propagation Medium:", "Simulates physical RF propagation across N discrete channels (N in {4, 6, 8, 12, 16}) under thermal AWGN noise floor N_0, slow fading path gains g_k, and superposed ECM interference I_k = N_0 + J_k.")
    add_numbered_clause(doc, "1.1.3", "Receiver (ES Sensing Node — Blue Identity):", "Performs Electronic Support (ES) spectrum surveillance via channelized energy detection. Measures received friendly signal power P_rx,k and total interference I_k to evaluate instantaneous SINR_k. Categorizes channels into FREE, DEGRADED, and BLOCKED states and packages observations into a standardized CRRequest object.")
    add_numbered_clause(doc, "1.1.4", "Cognitive Decision Engine & Attached ML Policy (Slate Steel Identity):", "The core reasoning nucleus. Implements a multi-stage arbitration pipeline consisting of: (a) Sensing evidence parsing, (b) Transmitter-attached Neural Policy inference (64x32 ReLU Multi-Layer Perceptron), (c) Softmax confidence quantification, (d) Deterministic Stage-3 Hybrid Safety Gating, and (e) Cognitive Adaptive Hop-Set synthesis.")
    add_numbered_clause(doc, "1.1.5", "Transmitter (ECCM Actuator — Green Identity):", "The friendly communications radiator. Tunes its agile fast-lock Local Oscillator (LO) to the approved carrier frequency, regulates RF output power amplifier (PA) levels, executes adaptive frequency hopping, and radiates the friendly waveform back into the RF channel to close the operational loop.")

    # ---------------------------------------------------------
    # SECTION 2: MATHEMATICAL & ALGORITHMIC FORMULATION
    # ---------------------------------------------------------
    add_heading_1(doc, "2. Mathematical and Algorithmic Formulation")

    add_p(
        doc,
        "To provide senior defense scientists with complete technical rigor, the underlying mathematical equations and signal models "
        "implemented in the codebase are detailed below."
    )

    add_heading_2(doc, "2.1 RF Channel Propagation and Interference Physics")
    add_p(
        doc,
        "The physical electromagnetic environment models N discrete logical channels. For any channel k in {0, 1, ..., N-1}, "
        "the received friendly signal power P_{rx,k} (in linear units) is governed by the transmitter power P_{tx} and the channel path gain g_k:"
    )
    
    add_p(doc, "    P_{rx,k} = P_{tx,lin} · g_k,    where P_{tx,lin} = 10^(P_{tx,dB} / 10)", size_pt=9.5, bold=True, color=NAVY_PRIMARY)
    add_p(
        doc,
        "Here g_k accounts for distance-based geometric path attenuation and time-variant fading. In each discrete time step, "
        "g_k undergoes Rayleigh / log-normal perturbation: g_k(t+1) = clip(g_k(t) · [1.0 + 0.08 · N(0, 1)], 0.4, 1.6). "
        "Simultaneously, the adversary jammer injects linear interference power J_k. The total impairment power I_k in slot k is:"
    )
    add_p(doc, "    I_k = N_0 + J_k", size_pt=9.5, bold=True, color=NAVY_PRIMARY)
    add_p(
        doc,
        "where N_0 is the thermal background noise floor (default N_0 = 1.0 linear a.u.), and J_k >= 0 represents the ECM power injected into channel k. "
        "The instantaneous Signal-to-Interference-plus-Noise Ratio (SINR) measured in decibels is rigorously expressed as:"
    )
    add_p(doc, "    SINR_k (dB) = 10 · log10( P_{rx,k} / (N_0 + J_k) )", size_pt=9.5, bold=True, color=NAVY_PRIMARY)

    add_heading_2(doc, "2.2 ES Receiver Tri-State Channel Classification Logic")
    add_p(
        doc,
        "Rather than relying on unachievable omniscient knowledge of the jammer's identity or intent, the ES Receiver assesses each channel "
        "strictly from measurable RF telemetry against calibrated defence operational thresholds (T_good and T_bad):"
    )

    add_numbered_clause(doc, "2.2.1", "FREE State (ChannelState.FREE):", "SINR_k >= T_good (default 10.0 dB). Channel provides high link fidelity, nominal bit error rate (BER), and excellent communications throughput. Recommended for immediate carrier allocation.")
    add_numbered_clause(doc, "2.2.2", "DEGRADED State (ChannelState.DEGRADED):", "T_bad <= SINR_k < T_good (default 3.0 dB <= SINR_k < 10.0 dB). Link exhibits moderate noise or edge ECM spillover. Forward Error Correction (FEC) can sustain degraded voice/data, but link margin is constrained.")
    add_numbered_clause(doc, "2.2.3", "BLOCKED State (ChannelState.BLOCKED):", "SINR_k < T_bad (default < 3.0 dB). Strong adversary ECM or severe attenuation. Bit error rate exceeds demodulator threshold; zero reliable communication is possible.")

    add_heading_2(doc, "2.3 Transmitter-Attached Neural Policy (MLP Classifier Architecture)")
    add_p(
        doc,
        "The machine learning subsystem is engineered as a Multi-Layer Perceptron (MLP) neural classifier attached directly to the transmitter "
        "subsystem. It maps an instantaneous multidimensional spectral observation vector x into a recommended frequency channel or a power-boost action."
    )
    add_p(
        doc,
        "Feature Vector Construction (x in R^(3N + 2)): For an N-channel system, the feature extractor forms an input vector consisting of "
        "3N spectral features plus 2 transmitter state features:"
    )
    add_p(
        doc,
        "    x = [ SINR_0, S_0, J_0,  SINR_1, S_1, J_1,  ...,  SINR_{N-1}, S_{N-1}, J_{N-1},  P_{tx},  (P_{max} - P_{tx}) ]^T",
        size_pt=9.5, bold=True, color=NAVY_PRIMARY
    )
    add_p(
        doc,
        "where SINR_k is the channel signal-to-noise ratio in dB, S_k in {2.0 (FREE), 1.0 (DEGRADED), 0.0 (BLOCKED)} is the discrete state encoding, "
        "J_k is the measured jammer interference, P_{tx} is the current transmitter power in dB, and (P_{max} - P_{tx}) represents the available power headroom."
    )
    add_p(
        doc,
        "Neural Network Topology: The network comprises an input layer of dimension (3N+2), followed by a 64-neuron fully-connected hidden layer, "
        "a 32-neuron secondary hidden layer, and an output layer of (N+1) classes (channels 0 to N-1, plus class -1 representing INCREASE_POWER). "
        "Hidden activations utilize the Rectified Linear Unit (ReLU: f(z) = max(0, z)). The output logits z are converted to normalized class probabilities "
        "via the Softmax activation function:"
    )
    add_p(
        doc,
        "    P(y = c | x) = exp(z_c) / SUM_{j=1}^{N+1} exp(z_j),    with Confidence = max_c P(y = c | x)",
        size_pt=9.5, bold=True, color=NAVY_PRIMARY
    )

    add_heading_2(doc, "2.4 Multi-Stage Hybrid Safety Gate Engine")
    add_p(
        doc,
        "A foundational principle stressed to defense scientists: In lethal and contested military operations, an unconstrained neural network "
        "must NEVER be permitted unchecked authority to steer RF transmitters. Machine learning models can hallucinate, overfit, or produce aberrant "
        "proposals when faced with out-of-distribution ECM waveforms. eAge Innovations addresses this by embedding a deterministic Hybrid Safety Gate "
        "that enforces three inviolable operational invariants:"
    )
    add_numbered_clause(doc, "2.4.1", "Safety Invariant 1 (Strict Blacklist Enforcement):", "If the neural model proposes channel CH_p, the safety gate cross-checks CH_p against the live BLOCKED set. If CH_p in {BLOCKED}, the proposal is instantly vetoed and overridden by deterministic fallback logic.")
    add_numbered_clause(doc, "2.4.2", "Safety Invariant 2 (Headroom-Bound Power Boost):", "If the model recommends INCREASE_POWER, the safety gate confirms that P_{current} + delta_P <= P_{max}. If headroom is depleted, power increase is suppressed to prevent transmitter thermal damage.")
    add_numbered_clause(doc, "2.4.3", "Safety Invariant 3 (Full Explainability Ledger):", "Every single decision records its primary driver (RULES, ML, HYBRID, or ML-SAFETY), the raw model confidence score, the exact verification path, and a human-readable military rationale string into an immutable audit trace.")

    add_heading_2(doc, "2.5 Cognitive Adaptive Frequency Hopping (adapt_hop_set Algorithm)")
    add_p(
        doc,
        "When cognitive hopping is enabled, the transmitter does not follow a blind, static frequency list. Instead, the engine dynamically manages "
        "an active hop pool H = {f_1, f_2, ..., f_M} (default M=3 channels). At each transmission epoch, the adapt_hop_set algorithm executes:"
    )
    add_p(
        doc,
        "    Step 1. Threat Eviction: H_kept = { c in H | c not in BLOCKED }\n"
        "    Step 2. Dynamic Pool Refill: For c in { Usable Channels ranked descending by SINR }:\n"
        "                If c not in H_kept and c not in BLOCKED:\n"
        "                    H_kept.append(c)\n"
        "                If len(H_kept) >= M: break\n"
        "    Step 3. Hop Execution: Carrier = H_kept[ SHA-256(seed:step) mod len(H_kept) ]",
        size_pt=9.0, bold=True, color=NAVY_PRIMARY
    )

    # ---------------------------------------------------------
    # SECTION 3: NUMBERED SCENARIO-BY-SCENARIO BREAKDOWN
    # ---------------------------------------------------------
    add_heading_1(doc, "3. Comprehensive Scenario-by-Scenario Operational Breakdown")

    add_p(
        doc,
        "The following sections provide a rigorous, hierarchically numbered examination of each primary operational scenario demonstrable within the software. "
        "For each scenario, the four critical operational dimensions are systematically analyzed: Jammer Action, Receiver Sensing, ML Decision Logic, "
        "and Transmitter Actuation."
    )

    # ---------------------------------------------------------
    # SCENARIO 1: BENIGN SPECTRUM
    # ---------------------------------------------------------
    add_heading_2(doc, "3.1 Scenario 1: Baseline Benign Spectrum (Clear RF Environment, Zero ECM)")

    add_numbered_clause(doc, "3.1.1", "Operational Context:", "Initial link establishment or operating in an uncontested, peacetime electromagnetic environment. Serves as the performance and telemetry baseline for the simulation.")
    add_numbered_clause(doc, "3.1.2", "Jammer Action (What does the Jammer do?):", "The Jammer is in STANDBY / BENIGN status (profile = NONE). Jamming emission power is zero across all bands (J_k = 0 for all k in {0, ..., N-1}). The adversary radiates no RF denial energy.")
    add_numbered_clause(doc, "3.1.3", "Receiver Sensing (What does the Receiver sense?):", "The ES Receiver surveys all N channels. Because J_k = 0, total interference is purely the thermal noise floor (I_k = N_0 = 1.0). On the active carrier, received power P_rx >> N_0 produces high SINR (typically +18 dB to +22 dB). On non-active carriers, sensing proxy confirms ambient SINR >> 10 dB. All N channels are classified as FREE (0 DEGRADED, 0 BLOCKED).")
    add_numbered_clause(doc, "3.1.4", "Machine Learning Inference (How does the ML arrive at a conclusion?):", "The observation vector x contains high positive SINRs across all elements and zero jam entries (J_k = 0). The MLP forward pass computes dominant logits for the top-ranked FREE channel (e.g., CH0 or CH1). The Softmax confidence score peaks at 0.98 to 1.00. The Stage 3 Hybrid Safety Gate verifies that the recommended channel is FREE and unthreatened, approving it without override. Dispatches action USE_CHANNELS.")
    add_numbered_clause(doc, "3.1.5", "Transmitter Actuation (What does the Transmitter do?):", "The Transmitter maintains transmission on the recommended carrier at nominal baseline power (0.0 dB). Power headroom is maximum (20.0 dB available). If hopping is active, it steps sequentially across the initial hop set {CH0, CH1, CH2} without encountering any degraded hops.")
    add_numbered_clause(doc, "3.1.6", "Operational Outcome & Screen Manifestation:", "Status Pill: OK (Green). Status Badge: STANDBY / BENIGN. Telemetry displays: N FREE Channels, 0 BLOCKED. Rationale Log: 'Channel 0 is FREE with best SINR; recommend CH0.'")

    # ---------------------------------------------------------
    # SCENARIO 2: SPOT JAMMING ON ACTIVE CARRIER
    # ---------------------------------------------------------
    add_heading_2(doc, "3.2 Scenario 2: Single-Carrier Spot Jamming on Active Carrier (Targeted Narrowband EA)")

    add_numbered_clause(doc, "3.2.1", "Operational Context:", "The adversary electronic intelligence (ELINT) detects friendly tactical emissions on carrier CH0 and focuses an agile high-power spot jammer directly onto that frequency slot to break the communications link.")
    add_numbered_clause(doc, "3.2.2", "Jammer Action (What does the Jammer do?):", "The Jammer switches to profile SPOT, targeting channel 0 with concentrated RF power J_0 = 40.0 linear a.u. (all other channels J_k = 0). It executes an intense narrowband denial attack intended to overwhelm the friendly link budget on that specific frequency.")
    add_numbered_clause(doc, "3.2.3", "Receiver Sensing (What does the Receiver sense?):", "On channel CH0, the total interference spikes to I_0 = N_0 + J_0 = 1.0 + 40.0 = 41.0 a.u. The measured SINR collapses from +20 dB to approximately -3.0 dB to -5.0 dB, far below T_bad (3.0 dB). CH0 is immediately re-classified as BLOCKED. The remaining channels (CH1 to CH_N-1) remain unaffected with clean SINR >= 10 dB (FREE).")
    add_numbered_clause(doc, "3.2.4", "Machine Learning Inference (How does the ML arrive at a conclusion?):", "The feature vector x reflects an extreme localized impairment on CH0 (SINR_0 < 0, State_0 = 0.0, Jam_0 = 40.0). The trained MLP neural network recognizes this localized spot-jam pattern. The output layer suppresses CH0 and activates the highest-ranked usable channel (CH1 or CH2). The Softmax confidence is high (0.95 to 0.99). The Stage 3 Safety Gate validates that CH_recommended not in {CH0 (BLOCKED)}, confirming link safety and generating action USE_CHANNELS.")
    add_numbered_clause(doc, "3.2.5", "Transmitter Actuation (What does the Transmitter do?):", "The Transmitter LO actuator rapidly retunes its synthesizer from CH0 to the recommended clean carrier (CH1). Transmit power is maintained at 0.0 dB because headroom is abundant and the new channel is clean. Friendly communication is seamlessly restored within a single decision step.")
    add_numbered_clause(doc, "3.2.6", "Operational Outcome & Screen Manifestation:", "Status Pill: OK (Green). Subsystem Banners: Jammer shows EMITTING ECM (Red), Receiver shows 1 BLOCKED, N-1 FREE. Spectrum Grid: CH0 turns bright Red (BLOCKED), CH1 turns Green (FREE, gold border = active carrier).")

    # ---------------------------------------------------------
    # SCENARIO 3: MULTI-SPOT COORDINATED JAMMING
    # ---------------------------------------------------------
    add_heading_2(doc, "3.3 Scenario 3: Multi-Spot Coordinated Jamming (Simultaneous Multi-Carrier Attack)")

    add_numbered_clause(doc, "3.3.1", "Operational Context:", "The adversary attempts to anticipate frequency agility by splitting its jamming transmitter resources across multiple frequencies simultaneously (e.g., CH0, CH1, and CH4).")
    add_numbered_clause(doc, "3.3.2", "Jammer Action (What does the Jammer do?):", "The Jammer activates profile MULTI_SPOT, distributing jamming power J_k = 40.0 a.u. across a designated subset of channels (e.g., targets = {0, 1, 4}). It attempts to deny both the active channel and the most obvious alternate hop candidates.")
    add_numbered_clause(doc, "3.3.3", "Receiver Sensing (What does the Receiver sense?):", "The ES Receiver registers severe interference on all targeted channels: I_0 = I_1 = I_4 = 41.0. Channels CH0, CH1, and CH4 drop below 3.0 dB and are marked BLOCKED. The remaining channels (CH2, CH3, CH5, CH6, CH7) report clean spectrum (SINR >= 10.0 dB, FREE). The telemetry card reflects 3 BLOCKED, (N-3) FREE.")
    add_numbered_clause(doc, "3.3.4", "Machine Learning Inference (How does the ML arrive at a conclusion?):", "The 3N-dimensional feature vector contains multiple zeros in state indicators (S_0=0, S_1=0, S_4=0) and high jam values. The MLP network processes the complex spatial distribution of interference. Rather than hunting sequentially, the neural forward pass immediately directs probability mass to the cleanest unattacked channel (e.g., CH2). Softmax confidence typically registers between 0.92 and 0.98. The Safety Gate cross-examines the prediction against the blacklist {0, 1, 4} and ratifies the choice.")
    add_numbered_clause(doc, "3.3.5", "Transmitter Actuation (What does the Transmitter do?):", "The Transmitter LO tunes to CH2. If adaptive hopping is engaged, the hopping engine evicts channels 0, 1, and 4 from the active hopping pool, synthesizing an updated pool composed exclusively of surviving free frequencies {CH2, CH3, CH5}.")
    add_numbered_clause(doc, "3.3.6", "Operational Outcome & Screen Manifestation:", "Spectrum Map: CH0, CH1, and CH4 illuminate in Red (BLOCKED); CH2 displays gold border (active TX, FREE). Explainability Trace logs: 'Stage 1: 3 channels partitioned as BLOCKED... Stage 2: Neural Proposal Recommend CH2... Stage 3: Approved without override.'")

    # ---------------------------------------------------------
    # SCENARIO 4: FAST AGILE FREQUENCY-SWEEPING JAMMER
    # ---------------------------------------------------------
    add_heading_2(doc, "3.4 Scenario 4: Fast Agile Frequency-Sweeping Jammer (Chirp / Swept ECM Waveform)")

    add_numbered_clause(doc, "3.4.1", "Operational Context:", "The adversary employs a dynamic, sweeping jamming transmitter that cyclically scans across the entire operational bandwidth, stepping frequency at each cycle with adjacent channel spectral bleed-through.")
    add_numbered_clause(doc, "3.4.2", "Jammer Action (What does the Jammer do?):", "The Jammer operates in SWEEP mode with power J_sweep = 40.0 a.u. At step t, it injects full power into channel k_sweep = (t mod N), while emitting 15% spectral sidelobe bleed (J = 6.0 a.u.) into adjacent flank channels (k_sweep - 1) mod N and (k_sweep + 1) mod N. The threat is time-variant and non-stationary.")
    add_numbered_clause(doc, "3.4.3", "Receiver Sensing (What does the Receiver sense?):", "At any step, the receiver detects a moving threat window: the center channel k_sweep is BLOCKED (SINR < 3 dB), the two adjacent channels suffer spectral bleed and degrade to DEGRADED (3 dB <= SINR < 10 dB), while channels on the opposite side of the spectrum remain FREE. As steps advance, the blocked/degraded window visibly shifts across the channel map.")
    add_numbered_clause(doc, "3.4.4", "Machine Learning Inference (How does the ML arrive at a conclusion?):", "The MLP recommender continuously evaluates the full spectral topography. It identifies channels that are geographically/spectrally distant from the current center of the sweep pulse (maximizing frequency separation Delta f from the jammer). Softmax confidence ranges from 0.88 to 0.96. The safety gate ensures that neither the swept center nor the degraded sidebands are selected if a fully FREE distant channel is available.")
    add_numbered_clause(doc, "3.4.5", "Transmitter Actuation (What does the Transmitter do?):", "The Transmitter steers communications to the distant free channel (e.g., if sweep is at CH0, transmitter tunes to CH4 or CH5). It outmaneuvers the cyclic sweep, maintaining continuous throughput without getting caught in the jammer's path.")
    add_numbered_clause(doc, "3.4.6", "Operational Outcome & Screen Manifestation:", "UI Telemetry pill displays 'CHk (Sweep ±15%)'. Successive single steps in the UI show the Red/Orange pattern marching across the Spectrum Grid, with the green active carrier hopping dynamically to stay clear of the jammer's sweep front.")

    # ---------------------------------------------------------
    # SCENARIO 5: FULL-BAND HIGH-POWER BARRAGE NOISE JAMMING
    # ---------------------------------------------------------
    add_heading_2(doc, "3.5 Scenario 5: Full-Band High-Power Barrage Noise Jamming (Complete Spectral Denial & Power Adaptation)")

    add_numbered_clause(doc, "3.5.1", "Operational Context:", "The adversary abandons frequency agility and unloads massive broadband noise jamming across the entire RF band simultaneously, attempting total communications blackout.")
    add_numbered_clause(doc, "3.5.2", "Jammer Action (What does the Jammer do?):", "The Jammer operates in BARRAGE mode. It spreads its maximum interference power J_k = J_barrage = 40.0 a.u. uniformly across all N channels simultaneously (J_k = jp for all k in {0, ..., N-1}). No frequency slot is left unjammed.")
    add_numbered_clause(doc, "3.5.3", "Receiver Sensing (What does the Receiver sense?):", "Every single channel experiences I_k = N_0 + 40.0 = 41.0. At nominal transmitter power (0.0 dB), received friendly signal power cannot achieve 10 dB SINR against 41.0 a.u. noise. Depending on path gain g_k, all channels register as either DEGRADED (e.g., 4 to 6 dB) or BLOCKED. Number of FREE channels drops to 0. The ES receiver detects total spectral impairment.")
    add_numbered_clause(doc, "3.5.4", "Machine Learning Inference (How does the ML arrive at a conclusion?):", "The feature vector indicates zero FREE channels across the entire spectrum. The MLP neural network recognizes that frequency hopping alone cannot bypass full-band barrage noise. The network activates its power-advice output neuron (class = -1 / POWER_LABEL). The Softmax distribution assigns highest probability to INCREASE_POWER. The Stage 3 Safety Gate checks transmitter headroom: P_{current} (0.0 dB) < P_{max} (20.0 dB). Headroom of 20 dB exists; therefore, the safety gate approves action INCREASE_POWER with advice P_{advice} = min(P_{max}, P_{current} + 2.0 dB).")
    add_numbered_clause(doc, "3.5.5", "Transmitter Actuation (What does the Transmitter do?):", "Rather than futilely shifting frequency across jammed bands, the Transmitter Power Amplifier (PA) ramps up its output power by +2.0 dB (from 0.0 dB to 2.0 dB, and subsequently higher if barrage persists). This burns through the adversary noise floor (ECCM burn-through), elevating received power P_{rx} and restoring the active channel's SINR above the operational threshold.")
    add_numbered_clause(doc, "3.5.6", "Operational Outcome & Screen Manifestation:", "Status Pill turns Orange: INCREASE_POWER. Action card displays INCREASE_POWER. Power Advice card displays: '2.0 dB'. Rationale log reads: 'All channels blocked/degraded at current power; suggest increase transmit power.' Transmitter telemetry shows Transmit Power rising and Power Headroom decreasing accordingly.")

    # ---------------------------------------------------------
    # SCENARIO 6: COGNITIVE ADAPTIVE HOPPING
    # ---------------------------------------------------------
    add_heading_2(doc, "3.6 Scenario 6: Cognitive Adaptive Frequency Hopping (Threat Eviction & Dynamic Hop Pool Refill)")

    add_numbered_clause(doc, "3.6.1", "Operational Context:", "Communications operate in anti-jam frequency-hopping mode. The adversary attempts to disrupt communications by intermittently jamming individual members of the active hop pool.")
    add_numbered_clause(doc, "3.6.2", "Jammer Action (What does the Jammer do?):", "The Jammer emits spot or multi-spot interference on specific frequencies that happen to belong to the transmitter's current hop pool (e.g., hop set H = {CH0, CH1, CH2}, with Jammer attacking CH0).")
    add_numbered_clause(doc, "3.6.3", "Receiver Sensing (What does the Receiver sense?):", "The receiver evaluates all channels during the sensing interval. It discovers that channel CH0 has dropped to -4.0 dB SINR and is BLOCKED, whereas channels CH1, CH2, CH3, and CH4 remain FREE. It flags CH0 as poisoned.")
    add_numbered_clause(doc, "3.6.4", "Machine Learning & Decision Engine Logic (How does the Engine arrive at a conclusion?):", "The hybrid engine notes that hopping is enabled (hop_enabled = True). It executes the adapt_hop_set routine: (1) It examines current hop pool {0, 1, 2}, (2) Channel 0 is found in the BLOCKED blacklist and is immediately evicted, leaving {1, 2}, (3) The algorithm inspects the surviving channels ranked descending by SINR (CH3 has SINR 19.5 dB), (4) It recruits CH3 into the pool to restore target cardinality M=3, synthesizing new pool H_new = {1, 2, 3}. All members of H_new are certified FREE.")
    add_numbered_clause(doc, "3.6.5", "Transmitter Actuation (What does the Transmitter do?):", "The Transmitter updates its internal hopping table to {CH1, CH2, CH3}. In subsequent transmission epochs, the pseudo-random generator hops exclusively across channels 1, 2, and 3. The poisoned channel CH0 is completely excised from the hopping sequence, maintaining pristine Anti-Jam (AJ) communications.")
    add_numbered_clause(doc, "3.6.6", "Operational Outcome & Screen Manifestation:", "Telemetry card Active Hop Set updates in real time from 'CH0, CH1, CH2' to 'CH1, CH2, CH3'. Trace Box Stage 4 explicitly logs: 'Cognitive Adaptive Hopping is ENABLED. adapt_hop_set evicted BLOCKED channel 0; refilled pool with clean channel 3.'")

    # ---------------------------------------------------------
    # SCENARIO 7: COMPARATIVE ENGINE ANALYSIS (RULES vs ML vs HYBRID)
    # ---------------------------------------------------------
    add_heading_2(doc, "3.7 Scenario 7: Comparative Engine Analysis (RULES vs. ML vs. Safety-Gated HYBRID)")

    add_numbered_clause(doc, "3.7.1", "Operational Context:", "Demonstrating to defense officials why neither pure deterministic rules nor unconstrained machine learning alone represent a sufficient military solution, and why eAge's HYBRID architecture is the required doctrine.")
    add_numbered_clause(doc, "3.7.2", "Deterministic RULES Engine:", "Fast, predictable, and provably bounded. Operates via greedy ranking: picks max(SINR) from FREE; if none, picks max(SINR) from DEGRADED; if none, requests power increase. Limitation: Purely reactive; lacks pattern recognition, cannot predict sweeping jammer trajectories or non-linear multi-band interference distributions.")
    add_numbered_clause(doc, "3.7.3", "Pure ML Neural Engine:", "Highly adaptive; extracts non-linear correlations across all 3N+2 features simultaneously. Can learn adversary ECM patterns and anticipate optimal channels. Vulnerability: In rare out-of-distribution ECM situations or borderline training cases, a pure neural model can output a low-confidence or erroneous channel that may coincide with a newly jammed frequency.")
    add_numbered_clause(doc, "3.7.4", "eAge HYBRID Engine (Mission-Assurance Architecture):", "Combines the predictive intelligence of machine learning with the inviolable safety of deterministic rules. The ML model proposes the candidate channel with its associated Softmax confidence score. The Stage 3 Hybrid Safety Gate verifies the candidate against hard constraints: if the proposed channel is BLOCKED, the safety gate executes an immediate override, falling back to deterministic safe selection and logging 'ML suggested CH_p but safety rules overrode.'")
    add_numbered_clause(doc, "3.7.5", "Tactical Value for Defence Reviewers:", "Guarantees 100% mission safety and airworthiness compliance while exploiting the superior feature extraction of deep neural networks. Senior scientists can inspect the exact rationale and confidence behind every single hop.")

    # ---------------------------------------------------------
    # SCENARIO 8: CATASTROPHIC WORST-CASE CONTESTATION
    # ---------------------------------------------------------
    add_heading_2(doc, "3.8 Scenario 8: Catastrophic Worst-Case Contestation (Full Denial at Maximum Power Limit)")

    add_numbered_clause(doc, "3.8.1", "Operational Context:", "The worst-case edge scenario. The adversary operates massive barrage or multi-spot jamming exceeding the maximum physical power limits of the friendly Power Amplifier.")
    add_numbered_clause(doc, "3.8.2", "Jammer Action (What does the Jammer do?):", "The Jammer emits overwhelming power (e.g., J_k = 80.0 a.u.) across all frequencies. The adversary's Effective Radiated Power (ERP) completely dominates the propagation medium.")
    add_numbered_clause(doc, "3.8.3", "Receiver Sensing (What does the Receiver sense?):", "All N channels drop to deeply negative SINRs (e.g., -8 dB to -12 dB). All N channels are categorized as BLOCKED. Number of FREE = 0, DEGRADED = 0, BLOCKED = N.")
    add_numbered_clause(doc, "3.8.4", "Engine Logic (How does the Engine arrive at a conclusion?):", "The engine checks the transmitter status and discovers that the transmitter has already stepped to its maximum authorized power P_{current} = P_{max} = 20.0 dB (Headroom = 0.0 dB). Power can no longer be increased. The engine detects that no mathematical solution exists within authorized hardware parameters. It dispatches status_code = ALL_BLOCKED with action = NO_SOLUTION / HOLD.")
    add_numbered_clause(doc, "3.8.5", "Transmitter Actuation (What does the Transmitter do?):", "The Transmitter executes fail-safe containment (HOLD). It does not blindly burn out its Power Amplifier or blast futile RF energy that would disclose its emitter coordinates to adversary anti-radiation homing missiles. It maintains silent hold while the C2 ledger alerts operators to total spectral saturation.")
    add_numbered_clause(doc, "3.8.6", "Operational Outcome & Screen Manifestation:", "Status Pill turns Red: ALL_BLOCKED. Dispatched Action shows: NO_SOLUTION. Engine Rationale logs: 'All channels blocked and maximum power already reached; no solution within limits.'")

    # ---------------------------------------------------------
    # SECTION 4: MASTER COMPARISON MATRIX TABLE
    # ---------------------------------------------------------
    add_heading_1(doc, "4. Master Scenario Comparison Matrix for Defence Scientists")

    add_p(
        doc,
        "Table 1 synthesizes the operational parameters, sensing outcomes, cognitive reasoning, and physical actuations across all eight scenarios."
    )

    matrix_table = doc.add_table(rows=9, cols=6)
    matrix_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    matrix_table.autofit = False
    set_table_borders(matrix_table, color="B0C4DE", sz="6", val="single")

    col_widths = [Inches(1.0), Inches(1.1), Inches(1.1), Inches(1.2), Inches(1.2), Inches(1.2)]
    for row in matrix_table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    headers = ["Scenario", "Jammer Profile & Power", "ES Receiver Classification", "ML / Hybrid Reasoning", "Transmitter Actuation", "Link Outcome"]
    hdr_row = matrix_table.rows[0]
    for idx, text in enumerate(headers):
        cell = hdr_row.cells[idx]
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        set_cell_shading(cell, "0B2A5B")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(text)
        set_run_font(r, size_pt=8.5, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))

    scenario_rows = [
        ("3.1 Benign Baseline", "NONE\nJ_k = 0", "N FREE\n0 BLK\nSINR ~20 dB", "Picks best FREE (CH0)\nConf: 0.99\nSafety: Verified", "Tuning: CH0\nP_tx: 0.0 dB\nHeadroom: 20 dB", "Optimal Fidelity\nLink Margins Max"),
        ("3.2 Spot Jam Active", "SPOT (CH0)\nJ_0 = 40 a.u.", "1 BLK (CH0)\nN-1 FREE\nSINR_0 = -3 dB", "Identifies CH0 hit\nProposes CH1\nSafety: Ratified", "Tuning: Retunes CH1\nP_tx: 0.0 dB\nHop away from CH0", "Uninterrupted\nSeamless Handoff"),
        ("3.3 Multi-Spot EA", "MULTI_SPOT\nTargets {0,1,4}\nJ = 40 a.u.", "3 BLK {0,1,4}\nN-3 FREE\nSelective denial", "Rejects hit channels\nRecommends CH2\nSafety: Filtered", "Tuning: CH2\nEvicts {0,1,4}\nRefills clean hop pool", "Adaptive Resilience\nHostile Avoidance"),
        ("3.4 Swept Chirp EA", "SWEEP (Cyclic)\nJ = 40 a.u.\n±15% bleed", "1 BLK (Center)\n2 DEGRADED\nN-3 FREE", "Tracks jam front\nPicks distant FREE\nSafety: Validated", "Tuning: Outmaneuvers\nHops to safe sector\nP_tx: Nominal", "Dynamic AJ\nSweep Tracking"),
        ("3.5 Barrage Noise", "BARRAGE\nAll N channels\nJ = 40 a.u.", "0 FREE\nAll DEGRADED or\nBLOCKED", "Detects full denial\nAdvise: +2 dB Pwr\nConf: 0.95", "Tuning: Stable\nP_tx: Ramps +2 dB\nHeadroom: Decreases", "Burn-Through\nSINR Restored"),
        ("3.6 Adaptive Hopping", "Targeted on\nActive Hop Set\n(e.g., CH0)", "Hop member CH0\nbecomes BLOCKED\nRemaining FREE", "Engine: adapt_hop_set\nEvicts CH0\nRecruits clean CH3", "Hop Set: {1,2,3}\nPRNG skips CH0\nP_tx: 0.0 dB", "AJ Integrity Kept\nPool Regenerated"),
        ("3.7 Engine Comparison", "Variable Contested\nTest Profiles", "Mixed Multi-State\nChannel Map", "RULES: Reactive\nML: Predictive\nHYBRID: AI + Safety", "Transmitter tracks\nsafe hybrid command\nwith audit proof", "Zero Hallucination\nDefense Assurance"),
        ("3.8 Worst-Case Limit", "Extreme Barrage\nJ = 80 a.u.\nOverwhelming", "All N channels\nBLOCKED\nSINR < -5 dB", "Detects zero headroom\nP_tx = P_max\nDispatches NO_SOLN", "Transmitter: HOLD\nSuppresses RF pulse\nPrevents burn-out", "Safe Containment\nOperator Alert"),
    ]

    for r_idx, data in enumerate(scenario_rows, start=1):
        row = matrix_table.rows[r_idx]
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(data):
            cell = row.cells[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            set_cell_shading(cell, bg)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 5] else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            set_run_font(r, size_pt=8.0, bold=(c_idx == 0), color=BODY_DARK)

    # ---------------------------------------------------------
    # SECTION 5: TACTICAL SIGNIFICANCE & ROADMAP FOR EADM
    # ---------------------------------------------------------
    add_heading_1(doc, "5. Tactical Significance & Roadmap to Embedded Autonomous Decision Module (eADM)")

    add_p(
        doc,
        "The software architecture demonstrated in this project was deliberately designed not as an ephemeral simulation toy, "
        "but as an architecturally faithful digital twin for embedded defence avionics and SDR electronic counter-countermeasures (ECCM)."
    )

    add_heading_2(doc, "5.1 Loose Coupling via Standardized Interfaces")
    add_p(
        doc,
        "The sensing interface (CRRequest) and the actuation interface (CRResponse) are fully decoupled from the physical simulation channel. "
        "In a fielded deployment, the software channel simulator is unplugged and replaced with real-time digitized I/Q streams from an SDR front-end "
        "(e.g., AD9361 / Zynq UltraScale+ RFSoC). The ES Receiver block maps directly onto FPGA-accelerated Fast Fourier Transform (FFT) channelized "
        "energy detectors. The Cognitive Radio Decision Engine code executes without syntactic modification on an embedded ARM Cortex-A53/A72 "
        "running real-time Linux or Integrity RTOS."
    )

    add_heading_2(doc, "5.2 Compliance with Military Airworthiness & Mission Assurance")
    add_p(
        doc,
        "Defence acquisition boards often raise valid concerns regarding the unexplainable 'black-box' nature of deep learning. "
        "The eAge demonstrator provides a definitive architectural solution through three certified design principles:"
    )
    add_numbered_clause(doc, "5.2.1", "Deterministic Containment:", "The neural network functions solely as an advisory recommender; it does not possess direct actuation control over the RF hardware. The Stage 3 Hybrid Safety Gate acts as a certified deterministic boundary.")
    add_numbered_clause(doc, "5.2.2", "Mathematical Traceability:", "Every single decision generates a comprehensive audit payload containing the input observation vector, the Softmax probability distribution, the safety verification outcome, and human-readable operational rationale.")
    add_numbered_clause(doc, "5.2.3", "Incremental Certification:", "Military certification bodies (e.g., CEMILAC / DGA / FAA DO-178C) can certify the deterministic safety baseline first, enabling progressive deployment of neural capabilities under strict bounding wrappers.")

    # ---------------------------------------------------------
    # SIGN-OFF BLOCK
    # ---------------------------------------------------------
    add_p(doc, "")
    sign_table = doc.add_table(rows=2, cols=2)
    sign_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sign_table.autofit = False
    sign_table.columns[0].width = Inches(3.4)
    sign_table.columns[1].width = Inches(3.4)
    set_table_borders(sign_table, color="CBD5E1", sz="4", val="single")

    cell_prep = sign_table.cell(0, 0)
    cell_appr = sign_table.cell(0, 1)
    set_cell_margins(cell_prep, top=100, bottom=100, left=120, right=120)
    set_cell_margins(cell_appr, top=100, bottom=100, left=120, right=120)
    set_cell_shading(cell_prep, "F8FAFC")
    set_cell_shading(cell_appr, "F8FAFC")

    p1 = cell_prep.paragraphs[0]
    p1.paragraph_format.space_after = Pt(2)
    r1 = p1.add_run("PREPARED & SUBMITTED BY:\n")
    set_run_font(r1, size_pt=8.5, bold=True, color=NAVY_PRIMARY)
    r1_sub = p1.add_run("eAge Innovations Technical Engineering Team\nEmbedded SDR & Cognitive EW Systems Group\nDate: September 12, 2026")
    set_run_font(r1_sub, size_pt=8.0, color=BODY_DARK)

    p2 = cell_appr.paragraphs[0]
    p2.paragraph_format.space_after = Pt(2)
    r2 = p2.add_run("SUBMITTED FOR SCIENTIFIC EVALUATION TO:\n")
    set_run_font(r2, size_pt=8.5, bold=True, color=NAVY_PRIMARY)
    r2_sub = p2.add_run("Shri S. K. Sir & Senior Defence Scientists\nDirectorate of Electronic Warfare & Tactical Comms\nDefence Scientific Review Panel")
    set_run_font(r2_sub, size_pt=8.0, color=BODY_DARK)

    # Save Document
    doc.save(str(OUT_DOCX))
    print(f"Document successfully created and saved at: {OUT_DOCX}")
    print(f"File size: {os.path.getsize(OUT_DOCX)} bytes")

    # Also save copy to Desktop/proposals if directory exists
    desk_dir = Path.home() / "Desktop" / "proposals"
    if desk_dir.exists():
        out_desk = desk_dir / "Cognitive_Radio_Simulation_Scenarios_Brief_for_SK_Sir.docx"
        doc.save(str(out_desk))
        print(f"Copied to Desktop proposals: {out_desk}")


if __name__ == "__main__":
    build_document()
