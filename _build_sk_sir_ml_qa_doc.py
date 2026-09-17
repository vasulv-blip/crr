#!/usr/bin/env python3
"""
Build Q&A briefing for Cognitive Radio Simulation — focus on Machine Learning.
Strict numbered points only (no bullets). For Shri S. K. Sir / demo readiness.
"""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor

BASE = Path(__file__).resolve().parent
OUT_DOCX = BASE / "Cognitive_Radio_Simulation_ML_QA_Brief.docx"
OUT_DESK = Path.home() / "Desktop" / "proposals" / "Cognitive_Radio_Simulation_ML_QA_Brief.docx"

NAVY = RGBColor(0x0B, 0x2A, 0x5B)
SLATE = RGBColor(0x1E, 0x29, 0x3B)
BODY = RGBColor(0x1F, 0x29, 0x37)
MUTED = RGBColor(0x64, 0x74, 0x8B)


def set_run(run, size=10.5, bold=False, italic=False, color=BODY):
    run.font.name = "Calibri"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color


def add_p(doc, text="", size=10.5, bold=False, italic=False, color=BODY, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if text:
        r = p.add_run(text)
        set_run(r, size=size, bold=bold, italic=italic, color=color)
    return p


def add_h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    set_run(r, size=13, bold=True, color=NAVY)
    return p


def add_h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    set_run(r, size=11.5, bold=True, color=SLATE)
    return p


def add_num(doc, num, title, body, indent_in=0.28):
    """Hanging-indent numbered clause: '1.1 Title: body'."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent_in)
    p.paragraph_format.first_line_indent = Inches(-indent_in)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    r_n = p.add_run(f"{num} ")
    set_run(r_n, size=10.5, bold=True, color=NAVY)
    r_t = p.add_run(f"{title} ")
    set_run(r_t, size=10.5, bold=True, color=SLATE)
    r_b = p.add_run(body)
    set_run(r_b, size=10.5, bold=False, color=BODY)
    return p


def add_answer(doc, answer, indent_in=0.28):
    """Unnumbered answer belonging to the preceding numbered question."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent_in)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.15
    r_t = p.add_run("Answer: ")
    set_run(r_t, size=10.5, bold=True, color=SLATE)
    r_b = p.add_run(answer)
    set_run(r_b, size=10.5, bold=False, color=BODY)
    return p


def add_qa(doc, q_num, question, answer):
    """Number the question only; answer sits under the same question without a number."""
    add_num(doc, q_num, "Question:", question)
    add_answer(doc, answer)


def build():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(0.75)
        s.bottom_margin = Inches(0.75)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    add_p(doc, "eAge Innovations — Defence SDR & Electronic Warfare Lab", size=10, bold=True, color=NAVY, space_after=2)
    add_p(
        doc,
        "Reference: EAGE-CR-ML-QA-2026-001  |  Audience: Shri S. K. Sir & Demo Reviewers  |  September 2026",
        size=8.5,
        color=MUTED,
        space_after=8,
    )
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(10)
    p_div._element.get_or_add_pPr().append(
        parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="18" w:space="1" w:color="0B2A5B"/></w:pBdr>')
    )

    title = doc.add_paragraph()
    title.paragraph_format.space_after = Pt(3)
    set_run(title.add_run("COGNITIVE RADIO SIMULATION — QUESTION & ANSWER BRIEF"), size=15, bold=True, color=NAVY)

    sub = doc.add_paragraph()
    sub.paragraph_format.space_after = Pt(10)
    set_run(
        sub.add_run(
            "Prepared answers for live demonstration review, with primary emphasis on Machine Learning, "
            "safety gating, interference sensing, and cognitive dynamic frequency hopping. "
            "Numbered points only."
        ),
        size=10.5,
        bold=True,
        color=SLATE,
    )

    # ------------------------------------------------------------------
    add_h1(doc, "1. Purpose of this Q&A")
    add_num(
        doc,
        "1.1",
        "Intent:",
        "This brief lists likely reviewer questions and the exact answers the demonstration team should give, "
        "especially on machine learning.",
    )
    add_num(
        doc,
        "1.2",
        "Scope:",
        "Covers overall simulation, ML model design, training, confidence, HYBRID safety, interference capture, "
        "and dynamic frequency hopping (FH) based on cognitive decisions.",
    )
    add_num(
        doc,
        "1.3",
        "Format rule:",
        "Only questions are numbered. The answer under each question has no separate number; it belongs to that same question.",
    )

    # ------------------------------------------------------------------
    add_h1(doc, "2. Overall Simulation — Core Q&A")

    add_qa(
        doc,
        "2.1",
        "What does this Cognitive Radio simulation demonstrate?",
        "It demonstrates a closed Sense–Decide–Act loop under hostile jamming: the Receiver senses channel "
        "conditions including interference, the Cognitive Decision Engine recommends an action (channel, power, "
        "or hop-set update), and the Transmitter actuates that decision.",
    )
    add_qa(
        doc,
        "2.2",
        "What problem is being solved for defence communications?",
        "When an adversary jams selected or wideband frequencies, a fixed plan or blind hop list fails. "
        "The simulation shows how a cognitive radio can sense interference and adapt carrier / hopping / power "
        "to keep the friendly link usable.",
    )
    add_qa(
        doc,
        "2.3",
        "What are the main blocks in the simulation?",
        "There are five blocks: Jammer (ECM threat), Contested RF Medium, Receiver (ES sensing), Cognitive "
        "Decision Engine with ML recommender, and Transmitter (ECCM actuator).",
    )
    add_qa(
        doc,
        "2.4",
        "Does the simulation use real RF hardware today?",
        "This PC software demonstration uses a physics-style channel simulator. The same CRRequest / CRResponse "
        "interfaces are designed so a later eADM / SDR front-end can replace the simulator without changing the "
        "decision architecture.",
    )
    add_qa(
        doc,
        "2.5",
        "What does 'capturing interference' mean in this demo?",
        "It means the Receiver measures and reports interference effects per channel through jam power and SINR, "
        "then classifies each channel as FREE, DEGRADED, or BLOCKED. The cognitive engine never receives an "
        "oracle jammer identity; it decides from measured evidence only.",
    )
    add_qa(
        doc,
        "2.6",
        "What does 'dynamic FH based on cognitive decisions' mean?",
        "Frequency hopping is not a fixed pre-planned list. When hopping is enabled, the engine adapts the hop "
        "pool: jammed (BLOCKED) members are evicted and clean usable channels are filled in, then hopping "
        "continues only over the updated cognitive hop set.",
    )

    # ------------------------------------------------------------------
    add_h1(doc, "3. Machine Learning — Primary Q&A (Focus Section)")

    add_h2(doc, "3.A What ML is used and why")
    add_qa(
        doc,
        "3.1",
        "Is machine learning mandatory for every decision?",
        "No. The simulation provides three modes: RULES (deterministic), ML (learned recommender with safety), "
        "and HYBRID (ML proposes, safety rules validate). RULES alone is a valid baseline; ML shows the same "
        "interface can be driven by a learned policy.",
    )
    add_qa(
        doc,
        "3.2",
        "Which machine learning model is used?",
        "A supervised Multi-Layer Perceptron (MLP) classifier from scikit-learn. Hidden layers are 64 and 32 "
        "neurons with ReLU activation. The solver is Adam. Training uses a fixed random seed for repeatability.",
    )
    add_qa(
        doc,
        "3.3",
        "Why was an MLP classifier chosen instead of deep learning spectrogram models?",
        "The decision is naturally multi-class classification over N channels plus an INCREASE_POWER class. "
        "Inputs are compact numeric telemetry, not images. An MLP trains quickly on a workstation, produces "
        "class probabilities for confidence display, and can be retrained when N changes — suitable for a "
        "transparent software demonstration.",
    )
    add_qa(
        doc,
        "3.4",
        "Is this reinforcement learning?",
        "No. The present demonstrator uses supervised classification. Labels are generated from simulator "
        "observations using an expert-style labelling rule (prefer best FREE, else best DEGRADED, else increase "
        "power). Reinforcement learning can be a later research extension; it is not required for this demo.",
    )

    add_h2(doc, "3.B Inputs, outputs, and confidence")
    add_qa(
        doc,
        "3.5",
        "What does the ML model take as input?",
        "A feature vector of length 3N+2. For each channel it includes SINR (dB), a state encoding "
        "(FREE=2, DEGRADED=1, BLOCKED=0), and measured jam power. It also includes current transmit power "
        "and remaining power headroom (P_max − P_current).",
    )
    add_qa(
        doc,
        "3.6",
        "What does the ML model output?",
        "One discrete class: a recommended channel id (0 … N−1), or a special class labelled −1 meaning "
        "INCREASE_POWER. Softmax-style class probabilities are used to report confidence as the maximum "
        "class probability.",
    )
    add_qa(
        doc,
        "3.7",
        "What does ML confidence mean on the screen?",
        "Confidence is the model's highest class probability for the chosen action. High confidence (for "
        "example 0.95–1.00) means the network strongly prefers one action; lower confidence means the "
        "distribution is more spread and the safety gate becomes especially important.",
    )
    add_qa(
        doc,
        "3.8",
        "How is the model trained?",
        "On first use in ML or HYBRID mode, the app trains on about 1200 synthetic labelled cases generated "
        "inside the same channel simulator across jam profiles (NONE, SPOT, MULTI_SPOT, SWEEP, BARRAGE) and "
        "random power settings. Features are standardised with StandardScaler before MLP training.",
    )
    add_qa(
        doc,
        "3.9",
        "Where do the training labels come from?",
        "Labels are produced by an expert labelling function on each synthetic observation: choose the best "
        "FREE channel by SINR; if none, choose the best DEGRADED; if none and headroom remains, label "
        "INCREASE_POWER; otherwise stay on the best available SINR channel. This creates supervised targets "
        "without requiring recorded field packets.",
    )

    add_h2(doc, "3.C Safety, HYBRID, and trustworthiness")
    add_qa(
        doc,
        "3.10",
        "Can the neural network freely command the transmitter?",
        "No. In ML and HYBRID modes the proposal always passes through a deterministic safety gate. If ML "
        "recommends a BLOCKED channel, or an unusable channel when usable ones exist, or a power increase "
        "when headroom is already zero, safety overrides and falls back to rule logic.",
    )
    add_qa(
        doc,
        "3.11",
        "What is the difference between ML mode and HYBRID mode?",
        "Both use the MLP proposal plus safety checks. HYBRID emphasises mission assurance: ML proposes, "
        "rules validate, and the engine tag / rationale shows when safety overrode the neural suggestion. "
        "This is the preferred mode for defence reviewers who require explainable containment of ML.",
    )
    add_qa(
        doc,
        "3.12",
        "What happens if the ML model is not trained yet?",
        "The engine automatically uses the RULES baseline and states in the message that ML is not trained "
        "yet. The operator can train from the sidebar; after training, ML or HYBRID uses the learned model.",
    )
    add_qa(
        doc,
        "3.13",
        "How do you prove to a defence scientist that ML did not 'hallucinate' a jammed channel?",
        "Show the Explainability / rationale trace: Stage 2 shows the ML proposal and confidence; Stage 3 "
        "shows safety verification. If ML suggested a blocked channel, the message explicitly records "
        "'ML suggested CHx but safety rules overrode' and the final action is the safe alternative.",
    )
    add_qa(
        doc,
        "3.14",
        "Is the ML model certified for airborne deployment today?",
        "No. This is a software demonstrator and digital twin of the decision architecture. The design "
        "principle for later certification is incremental: certify deterministic safety containment first, "
        "then bound neural recommendations under that gate (for example CEMILAC / DO-178C style progressive "
        "assurance). The demo shows that architecture, not a certified flight article.",
    )

    add_h2(doc, "3.D ML behaviour under jam scenarios")
    add_qa(
        doc,
        "3.15",
        "What should ML do under single-carrier spot jamming on the active channel?",
        "It should suppress the jammed channel and recommend a clean FREE channel with high confidence. "
        "Safety must reject any proposal that lands back on the blocked spot-jammed carrier.",
    )
    add_qa(
        doc,
        "3.16",
        "What should ML do under full-band barrage jamming?",
        "When no FREE channel remains at current power, ML should favour INCREASE_POWER (burn-through) if "
        "headroom exists. The transmitter then raises PA power by a bounded step (typically +2 dB), subject "
        "to P_max.",
    )
    add_qa(
        doc,
        "3.17",
        "What should ML / the engine do when all channels are blocked and power is already at maximum?",
        "Dispatch NO_SOLUTION / HOLD. Do not keep raising power or hopping blindly. Report ALL_BLOCKED with "
        "a clear rationale that limits are exhausted.",
    )
    add_qa(
        doc,
        "3.18",
        "How does ML relate to cognitive adaptive frequency hopping?",
        "ML (or rules) selects the safe action and usable channel set from sensing. When hop_enabled is true, "
        "adapt_hop_set then rebuilds the hop pool by removing BLOCKED members and refilling with clean "
        "usable channels. Dynamic FH is therefore driven by cognitive decisions, not by a static PRFH table.",
    )

    # ------------------------------------------------------------------
    add_h1(doc, "4. Interference Capture and Dynamic FH — Supporting Q&A")

    add_qa(
        doc,
        "4.1",
        "How is interference captured in numbers the ML can use?",
        "Each channel observation carries jam_power and sinr_db. Total impairment is modelled as I_k = N0 + J_k. "
        "SINR_k = 10·log10(P_rx,k / I_k). Thresholds map SINR into FREE (≥10 dB), DEGRADED (3–10 dB), "
        "BLOCKED (<3 dB). Those values become part of the 3N+2 ML feature vector.",
    )
    add_qa(
        doc,
        "4.2",
        "Does the Receiver know the jammer profile name?",
        "Operationally, no. Sensing is measurement-based. Spot / Multi-Spot / Sweep / Barrage are scenario "
        "controls for generating interference. The decision path sees only observation telemetry, matching "
        "realistic ES conditions.",
    )
    add_qa(
        doc,
        "4.3",
        "How do we show dynamic FH live during a demo?",
        "Enable Cognitive Adaptive Hopping, jam one member of the active hop set, then step the simulation. "
        "The Active Hop Set card should drop the blocked channel and add a clean replacement. The rationale "
        "trace should state that adapt_hop_set evicted the blocked member and refilled the pool.",
    )
    add_qa(
        doc,
        "4.4",
        "What is the difference between blind FH and cognitive FH in one sentence?",
        "Blind FH repeats a pre-agreed sequence even if some hops are jammed; cognitive FH updates the hop "
        "set from live sensing and decision logic so threatened hops are removed.",
    )

    # ------------------------------------------------------------------
    add_h1(doc, "5. Demo-Facing Short Answers (30-second replies)")

    add_num(
        doc,
        "5.1",
        "If asked 'Where is ML?':",
        "Select Decision engine = ML or HYBRID, train if needed, run a jam scenario, and point to ML "
        "recommendation, confidence, and safety/rationale stages.",
    )
    add_num(
        doc,
        "5.2",
        "If asked 'Is ML safe?':",
        "Yes for this architecture: neural net proposes; deterministic blacklist and headroom checks veto "
        "unsafe acts; every override is logged in plain language.",
    )
    add_num(
        doc,
        "5.3",
        "If asked 'What is learned?':",
        "A mapping from multi-channel SINR/state/jam/power features to the preferred channel or power-increase "
        "action, trained on synthetic contested cases.",
    )
    add_num(
        doc,
        "5.4",
        "If asked 'What is next after PC sim?':",
        "Replace the channel simulator with eADM / SDR I/Q sensing while keeping the same CRRequest / "
        "CRResponse cognitive interface and safety gate.",
    )
    add_num(
        doc,
        "5.5",
        "If asked about SK focus (look-and-feel + interference + cognitive FH):",
        "The demo presents the agreed modular look-and-feel, shows interference capture via ES sensing and "
        "channel states, and shows dynamic FH updated from cognitive decisions through adapt_hop_set.",
    )

    # ------------------------------------------------------------------
    add_h1(doc, "6. Recommended Live Demo Sequence for ML Questions")
    add_num(doc, "6.1", "Step 1:", "Open System Architecture & Node View; identify Jammer, Receiver, Decision Engine, Transmitter.")
    add_num(doc, "6.2", "Step 2:", "Set Decision engine to HYBRID; ensure ML is trained; note train accuracy if shown.")
    add_num(doc, "6.3", "Step 3:", "Run Spot jam on active carrier; show CH blocked, ML/hybrid recommends alternate FREE channel with confidence.")
    add_num(doc, "6.4", "Step 4:", "Enable cognitive hopping; jam a hop-set member; show hop pool eviction and refill.")
    add_num(doc, "6.5", "Step 5:", "Run Barrage; show INCREASE_POWER advice when FREE channels disappear and headroom remains.")
    add_num(doc, "6.6", "Step 6:", "Open explainability trace and read Stage 2 (ML) and Stage 3 (Safety) aloud.")

    # ------------------------------------------------------------------
    add_h1(doc, "7. Closing Statement for Reviewers")
    add_num(
        doc,
        "7.1",
        "Positioning:",
        "This simulation is a transparent Cognitive Radio decision demonstrator: interference is captured as "
        "measurable evidence, ML provides a learned channel/power recommender, and deterministic safety plus "
        "cognitive hopping convert that recommendation into mission-safe actuation.",
    )
    add_num(
        doc,
        "7.2",
        "Key assurance message:",
        "Machine learning is used as an advisory recommender inside a hybrid safety architecture — never as "
        "an unchecked black-box actuator.",
    )

    add_p(doc, "")
    add_p(doc, "Prepared by: eAge Innovations Technical Engineering Team", size=9, bold=True, color=NAVY)
    add_p(doc, "For scientific evaluation by: Shri S. K. Sir & Senior Defence Scientists", size=9, color=BODY)

    doc.save(str(OUT_DOCX))
    print(f"Saved: {OUT_DOCX}")
    if OUT_DESK.parent.exists():
        doc.save(str(OUT_DESK))
        print(f"Copied: {OUT_DESK}")


if __name__ == "__main__":
    build()
