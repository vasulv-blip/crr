#!/usr/bin/env python3
"""
Build Presentation Guide: How to present the Cognitive Radio Simulation
to Senior Defence Scientists. Strict numbered format only.
"""

from pathlib import Path

from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor

BASE = Path(__file__).resolve().parent
OUT_DOCX = BASE / "Cognitive_Radio_Simulation_Presentation_Guide_for_Defence_Scientists.docx"
OUT_DESK = Path.home() / "Desktop" / "proposals" / "Cognitive_Radio_Simulation_Presentation_Guide_for_Defence_Scientists.docx"

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


def add_num(doc, num, title, body, indent_in=0.32, space_after=5):
    """Strict numbered point: '1.1 Title: body'."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent_in)
    p.paragraph_format.first_line_indent = Inches(-indent_in)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    r_n = p.add_run(f"{num} ")
    set_run(r_n, size=10.5, bold=True, color=NAVY)
    if title:
        r_t = p.add_run(f"{title} ")
        set_run(r_t, size=10.5, bold=True, color=SLATE)
    r_b = p.add_run(body)
    set_run(r_b, size=10.5, bold=False, color=BODY)
    return p


def add_sub(doc, label, body, indent_in=0.32):
    """Unnumbered follow-on line under a numbered step (Say / Point to)."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent_in)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    r_t = p.add_run(f"{label} ")
    set_run(r_t, size=10.5, bold=True, color=SLATE)
    r_b = p.add_run(body)
    set_run(r_b, size=10.5, italic=("Say:" in label), color=BODY)
    return p


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
        "Reference: EAGE-CR-PRES-2026-001  |  Audience: Shri S. K. Sir & Senior Defence Scientists  |  September 2026",
        size=8.5,
        color=MUTED,
        space_after=8,
    )
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(10)
    p_div._element.get_or_add_pPr().append(
        parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="18" w:space="1" w:color="0B2A5B"/></w:pBdr>')
    )

    t = doc.add_paragraph()
    t.paragraph_format.space_after = Pt(3)
    set_run(t.add_run("HOW TO PRESENT THE COGNITIVE RADIO SIMULATION"), size=15, bold=True, color=NAVY)

    s = doc.add_paragraph()
    s.paragraph_format.space_after = Pt(4)
    set_run(
        s.add_run(
            "Practical presentation guide for live demonstration before senior defence scientists."
        ),
        size=10.5,
        bold=True,
        color=SLATE,
    )
    add_num(
        doc,
        "0.1",
        "Document format:",
        "This entire guide uses numbered points only. Action steps are numbered. Speaking lines sit under the same step without a separate number.",
    )

    # ------------------------------------------------------------------
    add_h1(doc, "1. Objective of This Presentation")
    add_num(
        doc,
        "1.1",
        "Primary goal:",
        "Show a closed Sense–Decide–Act Cognitive Radio loop that captures interference and adapts channel, power, or frequency hopping under hostile jamming.",
    )
    add_num(
        doc,
        "1.2",
        "Desired outcome:",
        "Reviewers should conclude that eAge has a clear, explainable software demonstrator of Cognitive EW decision logic that can later map onto eADM / SDR hardware.",
    )
    add_num(
        doc,
        "1.3",
        "Scope limit:",
        "This presentation is not a claim of certified airborne ML, and it is not a full field RF trial. State that clearly in the opening.",
    )
    add_num(
        doc,
        "1.4",
        "SK priorities to honour:",
        "Agreed look-and-feel; capturing interference; dynamic frequency hopping based on cognitive decisions.",
    )

    # ------------------------------------------------------------------
    add_h1(doc, "2. Before the Meeting — Preparation Checklist")
    add_num(doc, "2.1", "Start the application:", "From folder cognitive_radio_sim run: python -m streamlit run app.py --server.port 8501")
    add_num(doc, "2.2", "Open the browser:", "Go to http://localhost:8501 and confirm the hero title and eAge logo load correctly.")
    add_num(doc, "2.3", "Select preferred view:", "In the sidebar, choose System Architecture & Node View.")
    add_num(doc, "2.4", "Set recommended defaults:", "N = 8 channels; Decision engine = HYBRID; Cognitive / adaptive hopping = OFF initially; Appearance = Light if projecting in a bright room.")
    add_num(doc, "2.5", "Train the ML model:", "Train the ML recommender once before the audience arrives and confirm train accuracy is visible.")
    add_num(doc, "2.6", "Reset to clean state:", "Set jammer profile to NONE / clear jam so the opening screen shows a benign spectrum.")
    add_num(doc, "2.7", "Keep supporting documents ready:", "Scenarios Brief for SK Sir; ML Q&A Brief; this Presentation Guide.")
    add_num(doc, "2.8", "Check projector readability:", "Zoom the browser to 110–125 percent if needed so channel cards and rationale text remain readable from the back row.")
    add_num(doc, "2.9", "Plan the time budget:", "Aim for 20–25 minutes of demonstration plus 10–15 minutes of questions.")

    # ------------------------------------------------------------------
    add_h1(doc, "3. Opening Remarks")
    add_num(
        doc,
        "3.1",
        "Greeting:",
        "Sir, today we will demonstrate our Cognitive Radio software simulation for contested electronic warfare conditions. The purpose is to show how a friendly radio can sense interference, decide safely, and act by changing channel, power, or hop set.",
    )
    add_num(
        doc,
        "3.2",
        "Positioning statement:",
        "This is a PC software closed-loop demonstrator. The decision interfaces are designed so that later the channel simulator can be replaced by eADM / SDR sensing without changing the cognitive architecture.",
    )
    add_num(
        doc,
        "3.3",
        "Three live proofs:",
        "First, interference capture through ES sensing. Second, cognitive decision with hybrid ML safety. Third, dynamic frequency hopping driven by those decisions.",
    )
    add_num(
        doc,
        "3.4",
        "Invite interaction:",
        "Sir, please interrupt at any point if you wish us to change a jammer profile or decision mode.",
    )

    # ------------------------------------------------------------------
    add_h1(doc, "4. Screen Walkthrough — Look and Feel")
    add_num(doc, "4.1", "Action:", "Point to the top hero banner and eAge logo.")
    add_sub(doc, "Say:", "This is the Cognitive Radio Channel Selection demonstration under jamming.")
    add_num(doc, "4.2", "Action:", "Point to the red Jammer node.")
    add_sub(doc, "Say:", "This is the adversary ECM threat. We can generate Spot, Multi-Spot, Sweep, or Barrage interference.")
    add_num(doc, "4.3", "Action:", "Point to the blue Receiver node.")
    add_sub(doc, "Say:", "This is Electronic Support sensing. It measures SINR and classifies every channel as FREE, DEGRADED, or BLOCKED. This is how we capture interference.")
    add_num(doc, "4.4", "Action:", "Point to the Decision Engine panel.")
    add_sub(doc, "Say:", "This is the cognitive nucleus. It can run RULES, ML, or HYBRID. HYBRID means machine learning proposes and deterministic safety validates.")
    add_num(doc, "4.5", "Action:", "Point to the green Transmitter node.")
    add_sub(doc, "Say:", "This is the ECCM actuator. It retunes carrier, adjusts power, and executes adaptive hopping when enabled.")
    add_num(doc, "4.6", "Action:", "Point to the Explainability Trace.")
    add_sub(doc, "Say:", "Every decision is written here in stages so the reviewer can see why an action was taken.")

    # ------------------------------------------------------------------
    add_h1(doc, "5. Live Demonstration Sequence")

    add_h2(doc, "5.A Scene 1 — Benign Baseline")
    add_num(doc, "5.1", "Action:", "Ensure jammer is NONE / clear. Click Step once if needed.")
    add_sub(doc, "Say:", "Sir, with no ECM, all channels are FREE and the link runs on the best carrier at nominal power. This is our baseline.")
    add_num(doc, "5.2", "Point to on screen:", "Status OK; FREE channel count; active carrier gold border; high SINR.")

    add_h2(doc, "5.B Scene 2 — Capturing Interference (Spot Jam)")
    add_num(doc, "5.3", "Action:", "Set Decision engine = HYBRID. Apply Spot jam on the active carrier (for example CH0). Step the simulation.")
    add_sub(doc, "Say:", "Now the adversary spots our active channel. Watch the Receiver: that channel goes BLOCKED because SINR collapses. This is interference capture from measurements, not from an oracle jammer label.")
    add_num(doc, "5.4", "Point to on screen:", "Jammer EMITTING; Receiver BLOCKED count; spectrum tile turns red; Decision Engine recommends a clean FREE alternate; Transmitter retunes.")
    add_num(doc, "5.5", "Action:", "Open or scroll the explainability stages.")
    add_sub(doc, "Say:", "Stage 1 partitions usable versus blocked channels. Stage 2 shows the ML proposal and confidence. Stage 3 confirms safety did not allow a blocked hop.")

    add_h2(doc, "5.C Scene 3 — Multi-Spot Contestation")
    add_num(doc, "5.6", "Action:", "Switch to Multi-Spot on several channels (for example CH0, CH1, CH4). Step.")
    add_sub(doc, "Say:", "The adversary anticipates simple hopping by denying several carriers at once. The engine still finds a surviving FREE channel and avoids the blacklist.")
    add_num(doc, "5.7", "Point to on screen:", "Multiple red BLOCKED tiles; recommended clean channel; rationale listing blocked set.")

    add_h2(doc, "5.D Scene 4 — Dynamic FH Based on Cognitive Decisions")
    add_num(doc, "5.8", "Action:", "Enable Cognitive / adaptive hopping. Establish an initial hop set (for example CH0, CH1, CH2). Step once to show hopping active.")
    add_sub(doc, "Say:", "Sir, hopping is now cognitive, not blind. The hop pool is managed by the decision engine.")
    add_num(doc, "5.9", "Action:", "Jam one member of the active hop set. Step again.")
    add_sub(doc, "Say:", "The threatened hop is evicted from the Active Hop Set and a clean channel is filled in. That is dynamic FH based on cognitive decisions.")
    add_num(doc, "5.10", "Point to on screen:", "Active Hop Set card before and after; Trace Stage mentioning adapt_hop_set eviction and refill.")

    add_h2(doc, "5.E Scene 5 — Barrage and Power Advice")
    add_num(doc, "5.11", "Action:", "Optionally disable hopping for clarity. Set Barrage. Step.")
    add_sub(doc, "Say:", "Under full-band barrage, frequency agility alone is not enough. The engine advises a bounded transmit power increase to burn through, within P_max.")
    add_num(doc, "5.12", "Point to on screen:", "Status INCREASE_POWER; power advice value; falling headroom; rationale text.")

    add_h2(doc, "5.F Scene 6 — Machine Learning Assurance")
    add_num(doc, "5.13", "Action:", "Keep HYBRID selected and summarise the three decision modes.")
    add_sub(doc, "Say:", "For defence use we prefer HYBRID. Machine learning is advisory. Deterministic safety prevents hopping into BLOCKED channels or raising power beyond limits.")
    add_num(
        doc,
        "5.14",
        "If challenged on black-box risk:",
        "Show an override message if available, or explain that any unsafe ML proposal is rejected and logged as ML-SAFETY / safety override.",
    )

    # ------------------------------------------------------------------
    add_h1(doc, "6. Points to Emphasise for Senior Defence Scientists")
    add_num(doc, "6.1", "Measurement-based sensing:", "Decisions come from SINR, state, and jam power observations, not secret knowledge of jammer intent.")
    add_num(doc, "6.2", "Explainability:", "Every action has a human-readable rationale and staged trace.")
    add_num(doc, "6.3", "Safety containment of ML:", "Neural proposal cannot freely actuate RF; Hybrid Safety Gate enforces blacklist and headroom.")
    add_num(doc, "6.4", "Cognitive hopping:", "Hop set is regenerated from live contested conditions.")
    add_num(doc, "6.5", "Path to hardware:", "Same CRRequest / CRResponse contract can later ingest eADM / SDR telemetry.")
    add_num(doc, "6.6", "Honest positioning:", "Today this is a high-fidelity software twin for decision architecture, not a flight-cleared article.")

    # ------------------------------------------------------------------
    add_h1(doc, "7. Preferred Phrases")
    add_num(doc, "7.1", "Use this phrase:", "Sense–Decide–Act closed loop under Electronic Attack.")
    add_num(doc, "7.2", "Use this phrase:", "Interference capture through Electronic Support sensing.")
    add_num(doc, "7.3", "Use this phrase:", "Hybrid safety-gated machine learning recommender.")
    add_num(doc, "7.4", "Use this phrase:", "Cognitive adaptive frequency hopping / dynamic hop-pool management.")
    add_num(doc, "7.5", "Use this phrase:", "Mission assurance and explainable audit trail.")

    # ------------------------------------------------------------------
    add_h1(doc, "8. Phrases to Avoid")
    add_num(doc, "8.1", "Avoid this phrase:", "Fully autonomous lethal AI / unsupervised black-box control.")
    add_num(doc, "8.2", "Avoid this phrase:", "Already certified for airborne deployment.")
    add_num(doc, "8.3", "Avoid this phrase:", "Real-time RF hardware proof on this laptop alone.")
    add_num(doc, "8.4", "Avoid this phrase:", "100 percent jam-proof communications under every possible ECM.")

    # ------------------------------------------------------------------
    add_h1(doc, "9. Likely Questions and Answers")
    add_num(doc, "9.1", "Question:", "Is this real RF?")
    add_sub(doc, "Answer:", "This session is the software decision twin. Hardware mapping to eADM / SDR is the next integration step using the same interfaces.")
    add_num(doc, "9.2", "Question:", "Why machine learning?")
    add_sub(doc, "Answer:", "To learn non-linear mappings from multi-channel telemetry to channel or power advice, while RULES remain the safety baseline.")
    add_num(doc, "9.3", "Question:", "Can ML choose a jammed channel?")
    add_sub(doc, "Answer:", "It may propose one, but the safety gate vetoes BLOCKED recommendations and records the override.")
    add_num(doc, "9.4", "Question:", "How is hopping cognitive?")
    add_sub(doc, "Answer:", "adapt_hop_set removes blocked hop members and refills with clean usable channels from sensing.")
    add_num(doc, "9.5", "Question:", "What about look-and-feel?")
    add_sub(doc, "Answer:", "The modular node view mirrors the closed-loop architecture we discussed — threat, sensing, decision, actuation.")
    add_num(doc, "9.6", "Question:", "What is the timeline after this demo?")
    add_sub(doc, "Answer:", "Keep HYBRID decision core; connect live ES measurements from eADM / SDR; retain explainability and safety gate for laboratory trials.")

    # ------------------------------------------------------------------
    add_h1(doc, "10. Suggested 25-Minute Timeline")
    add_num(doc, "10.1", "Minutes 0 to 3:", "Opening remarks and positioning.")
    add_num(doc, "10.2", "Minutes 3 to 7:", "Look-and-feel architecture walkthrough.")
    add_num(doc, "10.3", "Minutes 7 to 11:", "Spot jam — interference capture and HYBRID decision.")
    add_num(doc, "10.4", "Minutes 11 to 15:", "Cognitive adaptive hopping demonstration.")
    add_num(doc, "10.5", "Minutes 15 to 18:", "Barrage and power advice.")
    add_num(doc, "10.6", "Minutes 18 to 20:", "ML assurance and explainability summary.")
    add_num(doc, "10.7", "Minutes 20 to 25:", "Questions from Shri S. K. Sir and the panel.")
    add_num(doc, "10.8", "If time is cut to 10 minutes:", "Present only Opening, Spot jam, Cognitive hopping, and Closing.")

    # ------------------------------------------------------------------
    add_h1(doc, "11. Closing Remarks")
    add_num(
        doc,
        "11.1",
        "Closing statement:",
        "Sir, to summarise: the simulation presents the agreed architecture look-and-feel; it captures interference through ES sensing; it decides with hybrid ML under deterministic safety; and it performs dynamic frequency hopping based on those cognitive decisions. We request your guidance on priorities for the next laboratory step toward eADM integration.",
    )
    add_num(
        doc,
        "11.2",
        "Offer supporting materials:",
        "Scenarios Brief, ML Q&A Brief, and this Presentation Guide are available for the panel.",
    )
    add_num(
        doc,
        "11.3",
        "End politely:",
        "Thank you, Sir. We are ready for questions.",
    )

    # ------------------------------------------------------------------
    add_h1(doc, "12. Presenter Emergency Notes")
    add_num(doc, "12.1", "If Streamlit freezes:", "Refresh the browser; if needed restart python -m streamlit run app.py --server.port 8501.")
    add_num(doc, "12.2", "If ML not trained message appears:", "Train from the sidebar, then re-run the jam scenario.")
    add_num(doc, "12.3", "If hop set does not change:", "Confirm Cognitive / adaptive hopping is ON and the jammed channel was actually inside the active hop set.")
    add_num(doc, "12.4", "If audience asks deep mathematics:", "Defer detail to Scenarios Brief Section 2, and keep the live demo on observable behaviour.")
    add_num(doc, "12.5", "If a control confuses the audience:", "Return to System Architecture & Node View and restate Sense–Decide–Act once.")

    add_p(doc, "")
    add_p(doc, "Prepared by: eAge Innovations Technical Engineering Team", size=9, bold=True, color=NAVY)
    add_p(doc, "For presentation to: Shri S. K. Sir & Senior Defence Scientists", size=9, color=BODY)

    doc.save(str(OUT_DOCX))
    print(f"Saved: {OUT_DOCX}")
    if OUT_DESK.parent.exists():
        doc.save(str(OUT_DESK))
        print(f"Copied: {OUT_DESK}")


if __name__ == "__main__":
    build()
