#!/usr/bin/env python3
"""Build PDF for Video Demo Script for Defence Scientists."""

from pathlib import Path

from fpdf import FPDF

BASE = Path(__file__).resolve().parent
OUT = BASE / "Cognitive_Radio_Simulation_Video_Demo_Script.pdf"
DESK = Path.home() / "Desktop" / "proposals" / "Cognitive_Radio_Simulation_Video_Demo_Script.pdf"

NAVY = (11, 42, 91)
SLATE = (30, 41, 59)
BODY = (31, 41, 55)
MUTED = (100, 116, 139)


def clean(text: str) -> str:
    return (
        text.replace("—", "-")
        .replace("–", "-")
        .replace("…", "...")
        .replace("×", "x")
        .replace("→", "->")
        .replace("·", "|")
        .replace("“", '"')
        .replace("”", '"')
        .replace("‘", "'")
        .replace("’", "'")
        .replace("**", "")
        .replace("`", "")
    )


class PDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")


def heading(pdf: PDF, text: str, size: int = 12):
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", size)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(0, 6, clean(text))
    pdf.ln(1)


def subhead(pdf: PDF, text: str):
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*SLATE)
    pdf.multi_cell(0, 5, clean(text))
    pdf.ln(0.5)


def body(pdf: PDF, text: str):
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*BODY)
    pdf.multi_cell(0, 5, clean(text))
    pdf.ln(0.5)


def bullet(pdf: PDF, text: str, indent: float = 4):
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*BODY)
    x = pdf.get_x()
    pdf.set_x(x + indent)
    pdf.multi_cell(0, 5, clean(f"- {text}"))
    pdf.ln(0.2)


def numbered(pdf: PDF, n: int, text: str, indent: float = 4):
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*BODY)
    x = pdf.get_x()
    pdf.set_x(x + indent)
    pdf.multi_cell(0, 5, clean(f"{n}. {text}"))
    pdf.ln(0.2)


def build():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_page()
    pdf.set_margins(16, 14, 16)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 6, "eAge Innovations - Defence SDR & Electronic Warfare Lab", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*MUTED)
    pdf.cell(
        0,
        5,
        "Reference: EAGE-CR-VIDEO-SCRIPT-2026-001  |  Audience: Defence Scientists / DRDO Labs  |  September 2026",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(2)
    pdf.set_draw_color(*NAVY)
    pdf.set_line_width(0.6)
    y = pdf.get_y()
    pdf.line(16, y, 194, y)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(0, 7, "COGNITIVE RADIO SIMULATION - VIDEO DEMO SCRIPT")
    pdf.ln(1)
    body(
        pdf,
        "Factual, balanced talking track for recording a demonstration. "
        "Covers what the software does today, without over-claiming.",
    )
    bullet(pdf, "Software: eAge Cognitive Radio Channel Selection under Jamming (Streamlit PC demo)")
    bullet(pdf, "Login (if shown): Username pocuser | Password poc123")
    bullet(pdf, "Suggested length: about 8-12 minutes")

    heading(pdf, "Before you start (30 seconds)")
    for t in [
        "Confirm the app is running and you are logged in.",
        "Use Dark theme if that matches the rest of your recording.",
        "Prefer System Architecture & Node View first; switch to Operator Spectrum View only if you want a denser map.",
        "Start with no jam so the map shows a calm FREE baseline, then inject jam.",
    ]:
        bullet(pdf, t)

    heading(pdf, "Stage 1 - Opening and scope (about 1 minute)")
    subhead(pdf, "Say:")
    for i, t in enumerate(
        [
            "This is a software-only Cognitive Radio simulation for technical review.",
            "It does not radiate RF; it is a PC demonstration of sensing, decision, and actuation logic.",
            "It is prepared as a demo for DRDO Labs and related defence technical audiences.",
            "The goal is to show how a link can observe channel quality, decide (rules / ML / hybrid), and act (channel change, hop set, or power advice) under jamming profiles.",
        ],
        1,
    ):
        numbered(pdf, i, t)
    subhead(pdf, "Do not claim:")
    for t in [
        "Live EW deployment readiness",
        "Real I/Q capture from field radios in this build",
        "Formal certified train/test ML metrics beyond what the UI shows",
    ]:
        bullet(pdf, t)

    heading(pdf, "Stage 2 - Screen layout (about 1-1.5 minutes)")
    subhead(pdf, "Point to the header:")
    for i, t in enumerate(
        [
            "Title: channel selection under jamming.",
            "Short capability line: channel simulation, measurement-based receiver judgement, Cognitive Radio decision, adaptive hopping, power advice.",
            "eAge branding on the right.",
        ],
        1,
    ):
        numbered(pdf, i, t)
    subhead(pdf, "Sidebar - keep it practical:")
    for i, t in enumerate(
        [
            "User - signed-in session; Logout ends the demo session.",
            "Display View - Architecture/Node view vs Operator Spectrum view.",
            "Theme - Light / Dark (top-right on the main canvas).",
            "Configuration - number of channels (N), decision engine, hopping toggle, SINR thresholds, max TX power.",
            "Run control - single step, auto steps, reset.",
        ],
        1,
    ):
        numbered(pdf, i, t)
    subhead(pdf, "Architecture view (if visible):")
    for i, t in enumerate(
        [
            "Separate nodes for jammer, transmitter, receiver / sensing, and Cognitive Radio decision.",
            "Useful when explaining the closed loop as blocks, not only as a colour map.",
        ],
        1,
    ):
        numbered(pdf, i, t)

    heading(pdf, "Stage 3 - Benign baseline (about 1 minute)")
    subhead(pdf, "Do:")
    for i, t in enumerate(
        [
            "Ensure jam is clear / profile NONE.",
            "Run Single step once or twice if needed.",
            "Show the channel map: FREE / DEGRADED / BLOCKED, with the active TX channel marked.",
        ],
        1,
    ):
        numbered(pdf, i, t)
    subhead(pdf, "Say:")
    for i, t in enumerate(
        [
            "With no ECM applied, the simulator gives a benign baseline - active carrier in a usable (FREE) condition for the demo.",
            "Receiver judgement is measurement-based on simulated SINR and jam power, not a hand-tuned storyboard.",
            "States are simple and readable for review: FREE, DEGRADED, BLOCKED.",
        ],
        1,
    ):
        numbered(pdf, i, t)

    heading(pdf, "Stage 4 - Inject jamming (about 2 minutes)")
    subhead(pdf, "Do (pick 2-3; do not rush all):")
    for i, t in enumerate(
        [
            "Spot - jam one channel (ideally the current TX channel) -> Apply jam -> Single step.",
            "Multi-spot - jam two channels -> Apply -> Step.",
            "Optionally Sweep or Barrage briefly to show wider pressure.",
        ],
        1,
    ):
        numbered(pdf, i, t)
    subhead(pdf, "Say:")
    for i, t in enumerate(
        [
            "Jam profiles are controlled scenarios inside the software: Spot, Multi-spot, Sweep, Barrage (and clear).",
            "After apply, the map and metrics update: SINR drops where jam is present; states move toward DEGRADED / BLOCKED as appropriate.",
            "This is how we exercise the Cognitive Radio loop under contested spectrum in simulation.",
        ],
        1,
    ):
        numbered(pdf, i, t)
    body(pdf, "If Architecture view: use the Jammer node controls; mention sidebar jam controls appear in Operator view.")

    heading(pdf, "Stage 5 - Decision engines (about 2 minutes)")
    subhead(pdf, "RULES")
    for i, t in enumerate(
        [
            "Deterministic baseline: prefer free channels; fall back by policy when needed.",
            "Transparent for scientists who want an explainable non-ML reference.",
        ],
        1,
    ):
        numbered(pdf, i, t)
    subhead(pdf, "ML")
    for i, t in enumerate(
        [
            "Supervised MLP recommender (small network, e.g. 64x32) trained on synthetic observation vectors from this same simulator.",
            "Features include per-channel SINR, state encoding, jam power, TX power, and power headroom (for N=8 this is a 26-length style vector as shown in the UI).",
            "Output is a classification action: recommend a channel, or advise INCREASE_POWER.",
            "Training accuracy shown in the UI is primarily on the synthetic training set; a formal held-out test split is a known next hardening item - do not oversell generalisation.",
        ],
        1,
    ):
        numbered(pdf, i, t)
    subhead(pdf, "HYBRID (recommended for demo)")
    for i, t in enumerate(
        [
            "ML proposes; safety rules can override unsafe suggestions (e.g. blocked channels).",
            "This is the balance we emphasise for defence review: learning proposal with containment.",
        ],
        1,
    ):
        numbered(pdf, i, t)
    subhead(pdf, "Do:")
    for i, t in enumerate(
        [
            "Set Decision engine to HYBRID.",
            "With jam on the active channel, Single step and point to the decision / ML proposal / dispatched action on screen.",
            "If a safety override message appears, explain it calmly as intentional containment.",
        ],
        1,
    ):
        numbered(pdf, i, t)

    heading(pdf, "Stage 6 - Hopping and power (about 1-1.5 minutes)")
    subhead(pdf, "Do:")
    for i, t in enumerate(
        [
            "Enable Cognitive / adaptive hopping if you want to show hop-set behaviour; Apply configuration if required.",
            "Step again under jam and point to hop-related UI / Stage trace if shown.",
            "Under heavy pressure (e.g. Barrage), note INCREASE_POWER advice when headroom remains - still within configured max TX power.",
        ],
        1,
    ):
        numbered(pdf, i, t)
    subhead(pdf, "Say:")
    for i, t in enumerate(
        [
            "Hopping here means the software builds / uses an adaptive hop set from sensed conditions - simulation logic, not a live frequency hopper on air.",
            "Power advice is bounded by the configured maximum TX power in the demo.",
        ],
        1,
    ):
        numbered(pdf, i, t)

    heading(pdf, "Stage 7 - Explainability trace (about 1 minute)")
    subhead(pdf, "Do:")
    bullet(pdf, "Open or scroll the staged explainability / Stage 1-5 style panel if visible in Architecture view.")
    subhead(pdf, "Say (keep short):")
    for i, t in enumerate(
        [
            "Stage flow is meant to be reviewable: sense -> decide (rules/ML/hybrid) -> safety -> hop synthesis -> actuator command.",
            "This supports technical discussion without treating the neural net as a black box for the whole system.",
        ],
        1,
    ):
        numbered(pdf, i, t)

    heading(pdf, "Stage 8 - Closing (about 1 minute)")
    subhead(pdf, "Say:")
    for i, t in enumerate(
        [
            "Summary: configurable multi-channel simulation, measurement-based states, rules / ML / hybrid decisions, optional hopping, power advice, under Spot / Multi / Sweep / Barrage scenarios.",
            "Interfaces are structured so a later path toward eADM / SDR integration can reuse the decision pattern - that is a roadmap statement, not a claim that this PC build is already connected to field hardware.",
            "Happy to take questions on thresholds, jam models, ML features, or hybrid safety behaviour.",
        ],
        1,
    ):
        numbered(pdf, i, t)
    subhead(pdf, "Optional logout (5-10 seconds):")
    for i, t in enumerate(
        [
            "Sidebar Logout -> confirm dialog -> return to login.",
            "Only if you want to show session control; otherwise end on the live demo screen.",
        ],
        1,
    ):
        numbered(pdf, i, t)

    heading(pdf, "Suggested on-screen sequence (checklist)")
    rows = [
        ("1", "Login (if needed)", "Demo access for the review session"),
        ("2", "Show header + views", "Scope: software simulation"),
        ("3", "Clear jam, step", "FREE baseline"),
        ("4", "Spot jam on TX CH", "Contested channel"),
        ("5", "HYBRID + step", "ML + safety"),
        ("6", "Multi-spot or Barrage", "Different ECM pressure"),
        ("7", "Hopping / power (optional)", "Actuation options"),
        ("8", "Explainability stages", "Reviewability"),
        ("9", "Close", "Honest limits + next steps"),
    ]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*NAVY)
    pdf.cell(18, 6, "Step", border=1)
    pdf.cell(70, 6, "Action", border=1)
    pdf.cell(0, 6, "Speak about", border=1, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*BODY)
    for a, b, c in rows:
        pdf.cell(18, 6, a, border=1)
        pdf.cell(70, 6, clean(b), border=1)
        pdf.cell(0, 6, clean(c), border=1, new_x="LMARGIN", new_y="NEXT")

    heading(pdf, "Phrases to prefer / avoid")
    subhead(pdf, "Prefer")
    for t in [
        'In this simulation...',
        "Measurement-based within the model...",
        "Synthetic training data for the demonstrator...",
        "Hybrid mode keeps a safety gate around the ML proposal...",
        "Structured for later eADM connection without redesigning the decision interface...",
    ]:
        bullet(pdf, t)
    subhead(pdf, "Avoid")
    for t in [
        "Operational EW system / field-proven / real-time RF warfare",
        "Fully trained / validated ML for deployment",
        "Detects any jammer automatically in theatre",
        "Absolute performance guarantees (BER, range, classification % in the field)",
    ]:
        bullet(pdf, t)

    heading(pdf, "One-line closing (optional)")
    body(
        pdf,
        "This demonstration shows a closed-loop Cognitive Radio decision path under jamming in software - "
        "sensing, rules and ML with hybrid safety, and bounded actuation - as a technical baseline for further defence evaluation.",
    )

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 5, "Prepared by: eAge Innovations Technical Engineering Team", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*BODY)
    pdf.cell(0, 5, "For scientific evaluation by: Defence Scientists / DRDO Labs", new_x="LMARGIN", new_y="NEXT")

    pdf.output(str(OUT))
    print(f"Saved PDF: {OUT}")
    if DESK.parent.exists():
        try:
            pdf.output(str(DESK))
            print(f"Copied PDF: {DESK}")
        except Exception as e:
            print(f"Desktop PDF skip: {e}")


if __name__ == "__main__":
    build()
