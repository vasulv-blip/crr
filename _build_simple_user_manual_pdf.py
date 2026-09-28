#!/usr/bin/env python3
"""Build a simple numbered scenario user manual PDF for the CR simulation."""

from pathlib import Path

from fpdf import FPDF

BASE = Path(__file__).resolve().parent
OUT = BASE / "docs" / "Cognitive_Radio_Simple_User_Manual.pdf"

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
        .replace("≥", ">=")
        .replace("≤", "<=")
        .replace("“", '"')
        .replace("”", '"')
        .replace("‘", "'")
        .replace("’", "'")
    )


class PDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 8, f"Page {self.page_no()}  |  eAge Innovations - Simple User Manual", align="C")


def title_block(pdf: PDF):
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 6, "eAge Innovations", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*MUTED)
    pdf.cell(
        0,
        5,
        "Cognitive Radio Channel Selection under Jamming  |  Simple Operator Manual  |  September 2026",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(2)
    pdf.set_draw_color(*NAVY)
    pdf.set_line_width(0.6)
    y = pdf.get_y()
    pdf.line(16, y, 194, y)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(0, 7, clean("SIMPLE USER MANUAL - HOW TO OPERATE THE SOFTWARE"))
    pdf.ln(1)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*BODY)
    pdf.multi_cell(
        0,
        5,
        clean(
            "This short guide shows how to log in, configure the demo, and run the main operating scenarios."
        ),
    )
    pdf.ln(2)


def h1(pdf: PDF, text: str):
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(0, 6, clean(text))
    pdf.ln(1)


def clause(pdf: PDF, num: str, text: str, bold_lead: bool = False):
    """Print '1.1  text' with hanging indent."""
    pdf.set_text_color(*BODY)
    label = f"{num}  "
    label_w = pdf.get_string_width(label) + 1
    x0 = pdf.l_margin
    usable = pdf.w - pdf.l_margin - pdf.r_margin

    pdf.set_x(x0)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(label_w, 5, clean(label))
    pdf.set_font("Helvetica", "B" if bold_lead else "", 10)
    pdf.multi_cell(usable - label_w, 5, clean(text))
    pdf.ln(0.6)


def figure(pdf: PDF, path: Path, caption: str):
    """Place a screenshot and a one-line caption. Start a new page if the image would be cramped."""
    if not path.is_file():
        clause(pdf, "-", f"Figure missing: {path.name}")
        return
    usable = pdf.w - pdf.l_margin - pdf.r_margin
    if pdf.get_y() > 150:
        pdf.add_page()
    pdf.image(str(path), x=pdf.l_margin, w=usable)
    pdf.ln(1)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 4.5, clean(caption))
    pdf.ln(2)


def build():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_page()
    pdf.set_margins(16, 14, 16)
    title_block(pdf)

    # ------------------------------------------------------------------
    h1(pdf, "1. Start and log in")
    clause(pdf, "1.1", "Open the application in a browser (local PC or Streamlit Community Cloud URL).")
    clause(pdf, "1.2", "On the login screen, enter Username: pocuser")
    clause(pdf, "1.3", "Enter Password: poc123")
    clause(pdf, "1.4", "Click Login.")
    clause(pdf, "1.5", "Optional: use Light / Dark at the top right to match the room lighting.")
    clause(pdf, "1.6", "After login you should see the title Cognitive Radio Channel Selection under Jamming.")

    # ------------------------------------------------------------------
    h1(pdf, "2. Understand the screen layout")
    clause(pdf, "2.1", "Left sidebar = user, display view, configuration, and run controls.")
    clause(pdf, "2.2", "Main area (Architecture view) shows three nodes: Jammer, Receiver, Transmitter.")
    clause(
        pdf,
        "2.3",
        "Jammer (red) = adversary ECM threat. Choose profile and power, then Emit Jam or Silence Jam.",
    )
    clause(
        pdf,
        "2.4",
        "Receiver (blue) = sensing node. Shows FREE / DEGRADED / BLOCKED counts and the channel spectrum map.",
    )
    clause(
        pdf,
        "2.5",
        "Transmitter (green) = ECCM actuator. Shows active carrier, TX power, hopping, and neural / hybrid decision.",
    )
    clause(
        pdf,
        "2.6",
        "Colour meaning on the map: green = FREE, amber = DEGRADED, red = BLOCKED.",
    )

    # ------------------------------------------------------------------
    h1(pdf, "3. Recommended starting configuration")
    clause(pdf, "3.1", "In Display View, select System Architecture & Node View.")
    clause(pdf, "3.2", "Set Number of channels (N) to 8.")
    clause(pdf, "3.3", "Set Decision engine to HYBRID.")
    clause(pdf, "3.4", "Leave Cognitive / adaptive hopping OFF for the first scenarios (turn ON later in Scenario 8).")
    clause(pdf, "3.5", "Leave SINR FREE threshold at about 10 dB and SINR BLOCKED threshold at about 3 dB.")
    clause(pdf, "3.6", "Leave Maximum TX power at 30 dB unless you are demonstrating power limits.")
    clause(pdf, "3.7", "Click Apply configuration and wait if ML training is shown.")
    clause(pdf, "3.8", "Important rule: after changing N, engine, hopping, or thresholds, always click Apply configuration.")

    # ------------------------------------------------------------------
    h1(pdf, "4. Scenario - Clean spectrum (no jamming)")
    clause(pdf, "4.1", "Purpose: show a quiet spectrum before any ECM threat.")
    clause(pdf, "4.2", "In the Jammer node, click Silence Jam.")
    clause(pdf, "4.3", "In the sidebar under Run control, click Single step once or twice.")
    clause(pdf, "4.4", "Look at the Receiver channel spectrum map.")
    clause(
        pdf,
        "4.5",
        "Expected result: most or all channels are FREE (green). Transmitter shows an active carrier on a usable channel.",
    )

    # ------------------------------------------------------------------
    h1(pdf, "5. Scenario - Spot jam on one channel")
    clause(pdf, "5.1", "Purpose: show the radio leaving one jammed channel.")
    clause(pdf, "5.2", "In the Jammer node, set ECM Threat Profile to SPOT.")
    clause(pdf, "5.3", "If target-channel controls are shown, select one channel (for example the current active carrier).")
    clause(pdf, "5.4", "Set Jam power (linear a.u.) to about 40.")
    clause(pdf, "5.5", "Click Emit Jam.")
    clause(pdf, "5.6", "If needed, click Single step once more so the map refreshes.")
    clause(
        pdf,
        "5.7",
        "Expected result: the jammed channel turns BLOCKED (red). Cognitive Radio recommends another FREE channel. Transmitter retunes away from the jammed channel.",
    )

    # ------------------------------------------------------------------
    h1(pdf, "6. Scenario - Multi-spot jam on several channels")
    clause(pdf, "6.1", "Purpose: show avoidance when more than one channel is attacked.")
    clause(pdf, "6.2", "Set ECM Threat Profile to MULTI_SPOT.")
    clause(pdf, "6.3", "Select two or more target channels (for example CH0 and CH1).")
    clause(pdf, "6.4", "Click Emit Jam, then Single step if needed.")
    clause(
        pdf,
        "6.5",
        "Expected result: selected channels are BLOCKED. Receiver free-link count drops. Transmitter moves to a remaining FREE or usable channel.",
    )

    # ------------------------------------------------------------------
    h1(pdf, "7. Scenario - Sweep jam over time")
    clause(pdf, "7.1", "Purpose: show the cognitive loop adapting as the jam moves.")
    clause(pdf, "7.2", "Set ECM Threat Profile to SWEEP.")
    clause(pdf, "7.3", "Click Emit Jam.")
    clause(pdf, "7.4", "In Run control, set Auto steps to 5 or 10.")
    clause(pdf, "7.5", "Click Run auto steps and watch the Receiver map.")
    clause(
        pdf,
        "7.6",
        "Expected result: the BLOCKED channel moves over time. The Cognitive Radio keeps recommending a usable channel as conditions change.",
    )

    # ------------------------------------------------------------------
    h1(pdf, "8. Scenario - Barrage jam and increase power")
    clause(pdf, "8.1", "Purpose: show the all-channels-stressed path and power advice.")
    clause(pdf, "8.2", "Set ECM Threat Profile to BARRAGE.")
    clause(pdf, "8.3", "Set Jam power high (for example 40).")
    clause(pdf, "8.4", "Click Emit Jam.")
    clause(pdf, "8.5", "Click Single step several times.")
    clause(pdf, "8.6", "Watch Transmitter TX power and the neural / hybrid decision card.")
    clause(
        pdf,
        "8.7",
        "Expected result: many or all channels are BLOCKED. Decision often becomes INCREASE_POWER while headroom remains, and TX power rises.",
    )
    clause(
        pdf,
        "8.8",
        "If TX power is already at Maximum TX power, expected status is ALL_BLOCKED.",
    )

    # ------------------------------------------------------------------
    h1(pdf, "9. Scenario - Cognitive / adaptive hopping")
    clause(pdf, "9.1", "Purpose: show hop-set adaptation under changing interference.")
    clause(pdf, "9.2", "In Configuration, turn Cognitive / adaptive hopping ON.")
    clause(pdf, "9.3", "Click Apply configuration and wait for ML training if shown.")
    clause(pdf, "9.4", "Emit a SWEEP or MULTI_SPOT jam.")
    clause(pdf, "9.5", "Run several auto steps.")
    clause(pdf, "9.6", "Look at Transmitter Hopping Mode and Active Hop Pool.")
    clause(
        pdf,
        "9.7",
        "Expected result: hop pool is shown; jammed members can be dropped and cleaner channels added. Transmitter follows the hop set.",
    )

    # ------------------------------------------------------------------
    h1(pdf, "10. Scenario - Compare RULES, ML, and HYBRID")
    clause(pdf, "10.1", "Purpose: show the same operator interface with different decision engines.")
    clause(pdf, "10.2", "Set Decision engine to RULES, click Apply configuration, emit a MULTI_SPOT jam, then Single step.")
    clause(pdf, "10.3", "Note the status / action and recommended channel.")
    clause(pdf, "10.4", "Change Decision engine to ML, Apply configuration, repeat the same jam and step.")
    clause(pdf, "10.5", "Change Decision engine to HYBRID and repeat once more.")
    clause(
        pdf,
        "10.6",
        "Expected result: response style stays inspectable (status, message, channel / power advice). HYBRID uses ML with a safety gate.",
    )

    # ------------------------------------------------------------------
    h1(pdf, "11. Scenario - Switch to Operator Spectrum View")
    clause(pdf, "11.1", "Purpose: use the classic spectrum map and measurement table.")
    clause(pdf, "11.2", "In Display View, select Operator Spectrum View.")
    clause(pdf, "11.3", "Use sidebar Jam injection (Apply jam / Clear jam) in this view.")
    clause(pdf, "11.4", "Click Single step or Run auto steps as needed.")
    clause(
        pdf,
        "11.5",
        "Expected result: channel cards, metrics, and decision history update in the spectrum-oriented layout.",
    )

    # ------------------------------------------------------------------
    h1(pdf, "12. Scenario - Reset and log out")
    clause(pdf, "12.1", "To clear the threat: click Silence Jam (Architecture view) or Clear jam (Spectrum view).")
    clause(pdf, "12.2", "To restart cleanly: click Reset simulation, then wait for retraining if prompted.")
    clause(pdf, "12.3", "To leave the session: click Logout in the sidebar.")
    clause(pdf, "12.4", "Expected result: simulation returns to a clean start, or the login screen appears after logout.")

    # ------------------------------------------------------------------
    h1(pdf, "13. How to read common status codes")
    clause(pdf, "13.1", "OK - at least one FREE channel is recommended.")
    clause(pdf, "13.2", "DEGRADED_OK - no FREE channel; a usable DEGRADED channel is recommended.")
    clause(pdf, "13.3", "INCREASE_POWER - all blocked at current power; raise TX power.")
    clause(pdf, "13.4", "ALL_BLOCKED - still blocked at maximum allowed power.")
    clause(pdf, "13.5", "HOLD - keep the current allocation (if shown).")

    # ------------------------------------------------------------------
    h1(pdf, "14. Short presenter checklist")
    clause(pdf, "14.1", "Log in -> show clean spectrum (Silence Jam -> Single step).")
    clause(pdf, "14.2", "Spot or Multi-spot Emit Jam -> show red BLOCKED tiles -> show Transmitter retune.")
    clause(pdf, "14.3", "Sweep + auto steps -> show blocked cell moving.")
    clause(pdf, "14.4", "Barrage -> show INCREASE_POWER and rising TX power.")
    clause(pdf, "14.5", "Optional: enable hopping; optional: compare RULES vs HYBRID.")
    clause(pdf, "14.6", "Remind the audience: this is a software-only demonstration; no radiated RF.")

    # ------------------------------------------------------------------
    h1(pdf, "15. Quick troubleshooting")
    clause(pdf, "15.1", "Map does not change after Emit Jam -> click Single step.")
    clause(pdf, "15.2", "Settings seem ignored -> click Apply configuration after changing them.")
    clause(pdf, "15.3", "ML not trained message -> Apply configuration or Reset simulation.")
    clause(pdf, "15.4", "Need a clean demo again -> Silence / Clear jam, then Reset simulation.")
    clause(pdf, "15.5", "Local start command (if running on a PC): python -m streamlit run app.py then open http://localhost:8501")

    # ------------------------------------------------------------------
    h1(pdf, "16. IQ Analysis screen")
    clause(
        pdf,
        "16.1",
        "IQ means In-phase and Quadrature. A radio sample is stored as two numbers at each instant: the in-phase part and the quadrature part, ninety degrees apart. Together they are one complex sample. This screen reads a short recording of those samples. It does not retune our transmitter, and it does not arm an exciter.",
    )
    clause(
        pdf,
        "16.2",
        "How to open it: after login, in the sidebar under Display View, select IQ Analysis. The other two views remain the cognitive-radio demonstration. This view is a separate mission: describe the emission in the recording.",
    )
    clause(
        pdf,
        "16.3",
        "Sidebar controls. Known capture chooses the recording: Fixed tone (one steady frequency), 1 ms burst (energy for about one millisecond), or Hopper (the tone steps through 6, 14, 22 and 30 kHz). Capture seed repeats the same recording. True SNR (dB) is the signal-to-noise ratio written into that recording. Confidence threshold is the minimum score required before a recommendation is allowed. Protected frequencies (kHz) is a comma-separated list; a match within 2 kHz forces HOLD. Analyse capture runs the measurement again.",
    )
    clause(
        pdf,
        "16.4",
        "The pictures below are the Hopper example. Read the top of the screen first, then the Threat Record, then the Hop Set and Bursts.",
    )
    figure(
        pdf,
        BASE / "docs" / "figures" / "iq_analysis_screen_top.png",
        "Figure 1. IQ Analysis, Hopper example: decision banner, four summary boxes, spectrum, frequency over time, and the Threat Record.",
    )
    clause(
        pdf,
        "16.5",
        "Green RECOMMEND banner. The class from the rules and the class from the classifier agree, and the confidence is above the threshold. The banner states that nothing is transmitted. RECOMMEND here means 'write down this emission'. It does not mean 'transmit'.",
    )
    clause(
        pdf,
        "16.6",
        "If the banner is amber HOLD, do not treat the row as a firm identification. HOLD appears when the two class answers disagree, when confidence is below the threshold, or when the frequency is on the protected list. If the banner is blue TRACK, no emission rose clearly above the noise.",
    )
    clause(
        pdf,
        "16.7",
        "Rule class is the answer from energy, bandwidth, and how often the frequency changes. No neural net is used for this box. In the picture it says HOPPER because several frequencies are occupied for most of the recording.",
    )
    clause(
        pdf,
        "16.8",
        "IQ classifier is a separate small network trained only on these three synthetic families. The number in brackets (0.99 in the picture) is its confidence in this one recording. It is not the cognitive-radio channel network used on the other screens.",
    )
    clause(
        pdf,
        "16.9",
        "Held-out test accuracy (1.00 in the picture) is the score on synthetic recordings that were not used to train that small network. A perfect score means these three families are easy to tell apart. It does not mean a field modulation classifier is finished.",
    )
    clause(
        pdf,
        "16.10",
        "Direction of arrival says 'not measured' on purpose. One recording has no antenna array, so the screen cannot give a bearing.",
    )
    clause(
        pdf,
        "16.11",
        "Spectrum (left plot). Horizontal axis is frequency in kHz. Vertical axis is power above the noise, in dB. Each hump is energy at that frequency. The red dashed lines are the known frequencies of this capture (6, 14, 22 and 30 kHz). The measured humps sit on those lines, within one frequency bin. A fixed tone shows one hump. A hopper shows one hump per frequency it visited.",
    )
    clause(
        pdf,
        "16.12",
        "Frequency over time (right plot). Horizontal axis is time in milliseconds, from 0 to about 40. Vertical axis is frequency in kHz. Colour is power: brighter colour is stronger energy, dark purple is the noise floor. A fixed tone is one bright horizontal line. A hopper is a staircase, stepping from one frequency to the next. A 1 ms burst is a short bright mark, with the rest of the time dark. Hover a cell to read time, frequency, and power. A dark cell, such as 43.75 kHz at the end of the recording, is noise, not a hop.",
    )
    clause(
        pdf,
        "16.13",
        "Threat Record compares the known capture with the estimate. Known Capture is the truth we wrote into the file. Estimate is what the measurement recovered. Class should match (HOPPER). Frequency tags are the same set, reported on a 1.56 kHz grid, so 6.00 appears as 6.25, 22.00 as 21.88, and 30.00 as 29.69. One-hit noise bins are left off those tags.",
    )
    clause(
        pdf,
        "16.14",
        "Bandwidth (Hz) is how wide each tone looks. The known value, 1562 Hz, is one frequency bin. The estimate, 3125 Hz, is about two bins, which is normal for a short window. Modulation 'unmodulated tone' means a single steady tone, not a voice or a data constellation. SNR (dB) is signal-to-noise ratio: 15.0 was written in, 14.1 was measured. Start and Duration say the energy runs for the whole 40 ms capture. DOA is Not measured on both sides.",
    )
    clause(
        pdf,
        "16.15",
        "The line under the table is the recommendation record: one frequency, one bandwidth, and a time span. In the picture that is 21.88 kHz, 3125 Hz, from 0.00 ms for 39.68 ms. It is the strongest measured tone, written down for a scientist. Nothing is transmitted.",
    )
    figure(
        pdf,
        BASE / "docs" / "figures" / "iq_analysis_screen_bottom.png",
        "Figure 2. Hop Set, Bursts, and the note 'About this measurement', for the same Hopper capture.",
    )
    clause(
        pdf,
        "16.16",
        "Hop Set lists each frequency that was occupied more than once. Hits is how many time slices fell on that frequency. Dwell (ms) is how long the energy stayed there, added up. Last (ms) is the latest time that frequency was seen. The four rows are the four hopper frequencies, on the 1.56 kHz grid. The table is capped at 1000 frequencies. Numbers are right-aligned so the decimals line up.",
    )
    clause(
        pdf,
        "16.17",
        "Bursts lists uninterrupted stretches of energy. For this hopper the transmitter never goes quiet, so there is one row from 0.00 ms for 39.68 ms. The frequency on that row is only the first slice, not the whole hop list. Use the Hop Set, not this single burst row, to see every frequency. For the '1 ms burst' capture you should instead see a short duration, about 1 ms, and a quiet recording on either side.",
    )
    clause(
        pdf,
        "16.18",
        "About this measurement repeats the limits in one place: synthetic training only, held-out score, not the cognitive-radio network, 1.56 kHz grid, red lines are the known frequencies, one-hit bins are omitted, no direction of arrival, and no exciter.",
    )
    clause(
        pdf,
        "16.19",
        "What to try while simulating. Select Fixed tone and confirm one hump and one frequency tag. Select 1 ms burst and confirm a short mark in time and a duration near 1 ms. Select Hopper and confirm four humps and four hop-set rows. Type one of the known frequencies into Protected frequencies and confirm the banner changes to HOLD.",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
