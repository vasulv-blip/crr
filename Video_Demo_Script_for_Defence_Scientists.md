# Cognitive Radio Simulation — Video Demo Script

**Audience:** Defence scientists / DRDO Labs technical review  
**Software:** eAge Cognitive Radio Channel Selection under Jamming (Streamlit PC demo)  
**Tone:** Factual, balanced — what the software does today, without over-claiming  

**Login (if shown):** Username `pocuser` · Password `poc123`  

**Suggested total length:** about 8–12 minutes  

---

## Before you start (30 seconds, off-camera or brief)

- Confirm the app is running and you are logged in.
- Use **Dark** theme if that matches the rest of your recording.
- Prefer **System Architecture & Node View** first; switch to **Operator Spectrum View** only if you want a denser map.
- Start with **no jam** so the map shows a calm FREE baseline, then inject jam.

---

## Stage 1 — Opening and scope (about 1 minute)

**Say:**

1. This is a **software-only** Cognitive Radio simulation for technical review.
2. It does **not** radiate RF; it is a PC demonstration of sensing, decision, and actuation logic.
3. It is prepared as a demo for **DRDO Labs** and related defence technical audiences.
4. The goal is to show how a link can **observe channel quality**, **decide** (rules / ML / hybrid), and **act** (channel change, hop set, or power advice) under jamming profiles.

**Do not claim:**

- Live EW deployment readiness  
- Real I/Q capture from field radios in this build  
- Formal certified train/test ML metrics beyond what the UI shows  

---

## Stage 2 — Screen layout (about 1–1.5 minutes)

**Point to the header:**

1. Title: channel selection under jamming.
2. Short capability line: channel simulation, measurement-based receiver judgement, Cognitive Radio decision, adaptive hopping, power advice.
3. eAge branding on the right.

**Sidebar — keep it practical:**

1. **User** — signed-in session; **Logout** ends the demo session.
2. **Display View** — Architecture/Node view vs Operator Spectrum view.
3. **Theme** — Light / Dark (top-right on the main canvas).
4. **Configuration** — number of channels (N), decision engine, hopping toggle, SINR thresholds, max TX power.
5. **Run control** — single step, auto steps, reset.

**Architecture view (if visible):**

1. Separate nodes for jammer, transmitter, receiver / sensing, and Cognitive Radio decision.
2. Useful when explaining the closed loop as blocks, not only as a colour map.

---

## Stage 3 — Benign baseline (about 1 minute)

**Do:**

1. Ensure jam is clear / profile NONE.
2. Run **Single step** once or twice if needed.
3. Show the channel map: **FREE / DEGRADED / BLOCKED**, with the active TX channel marked.

**Say:**

1. With no ECM applied, the simulator gives a **benign baseline** — active carrier in a usable (FREE) condition for the demo.
2. Receiver judgement is **measurement-based** on simulated SINR and jam power, not a hand-tuned storyboard.
3. States are simple and readable for review: FREE, DEGRADED, BLOCKED.

---

## Stage 4 — Inject jamming (about 2 minutes)

**Do (pick 2–3; do not rush all):**

1. **Spot** — jam one channel (ideally the current TX channel) → Apply jam → Single step.  
2. **Multi-spot** — jam two channels → Apply → Step.  
3. Optionally **Sweep** or **Barrage** briefly to show wider pressure.

**Say:**

1. Jam profiles are **controlled scenarios** inside the software: Spot, Multi-spot, Sweep, Barrage (and clear).
2. After apply, the map and metrics update: SINR drops where jam is present; states move toward DEGRADED / BLOCKED as appropriate.
3. This is how we exercise the Cognitive Radio loop under contested spectrum **in simulation**.

**If Architecture view:** use the **Jammer node** controls; mention sidebar jam controls appear in Operator view.

---

## Stage 5 — Decision engines (about 2 minutes)

**Show / say for each mode (honest wording):**

### RULES

1. Deterministic baseline: prefer free channels; fall back by policy when needed.
2. Transparent for scientists who want an explainable non-ML reference.

### ML

1. Supervised **MLP** recommender (small network, e.g. 64×32) trained on **synthetic** observation vectors from this same simulator.
2. Features include per-channel SINR, state encoding, jam power, TX power, and power headroom (for N=8 this is a 26-length style vector as shown in the UI).
3. Output is a **classification** action: recommend a channel, or advise **INCREASE_POWER**.
4. Training accuracy shown in the UI is primarily on the synthetic training set; a formal held-out test split is a known next hardening item — do not oversell generalisation.

### HYBRID (recommended for demo)

1. ML proposes; **safety rules** can override unsafe suggestions (e.g. blocked channels).
2. This is the balance we emphasise for defence review: learning proposal **with** containment.

**Do:**

1. Set Decision engine to **HYBRID**.
2. With jam on the active channel, **Single step** and point to the decision / ML proposal / dispatched action on screen.
3. If a safety override message appears, explain it calmly as intentional containment.

---

## Stage 6 — Hopping and power (about 1–1.5 minutes)

**Do:**

1. Enable **Cognitive / adaptive hopping** if you want to show hop-set behaviour; Apply configuration if required.
2. Step again under jam and point to hop-related UI / Stage trace if shown.
3. Under heavy pressure (e.g. Barrage), note **INCREASE_POWER** advice when headroom remains — still within configured max TX power.

**Say:**

1. Hopping here means the software builds / uses an adaptive hop set from sensed conditions — simulation logic, not a live frequency hopper on air.
2. Power advice is bounded by the configured maximum TX power in the demo.

---

## Stage 7 — Explainability trace (about 1 minute)

**Do:** Open or scroll the staged explainability / Stage 1–5 style panel if visible in Architecture view.

**Say (keep short):**

1. Stage flow is meant to be reviewable: sense → decide (rules/ML/hybrid) → safety → hop synthesis → actuator command.
2. This supports technical discussion without treating the neural net as a black box for the whole system.

---

## Stage 8 — Closing (about 1 minute)

**Say:**

1. Summary: configurable multi-channel simulation, measurement-based states, rules / ML / hybrid decisions, optional hopping, power advice, under Spot / Multi / Sweep / Barrage scenarios.
2. Interfaces are structured so a later path toward **eADM / SDR** integration can reuse the decision pattern — that is a roadmap statement, not a claim that this PC build is already connected to field hardware.
3. Happy to take questions on thresholds, jam models, ML features, or hybrid safety behaviour.

**Optional logout (5–10 seconds):**

1. Sidebar **Logout** → confirm dialog → return to login.  
2. Only if you want to show session control; otherwise end on the live demo screen.

---

## Suggested on-screen sequence (checklist)

| Step | Action | Speak about |
|------|--------|-------------|
| 1 | Login (if needed) | Demo access for the review session |
| 2 | Show header + views | Scope: software simulation |
| 3 | Clear jam, step | FREE baseline |
| 4 | Spot jam on TX CH | Contested channel |
| 5 | HYBRID + step | ML + safety |
| 6 | Multi-spot or Barrage | Different ECM pressure |
| 7 | Hopping / power (optional) | Actuation options |
| 8 | Explainability stages | Reviewability |
| 9 | Close | Honest limits + next steps |

---

## Phrases to prefer / avoid

**Prefer**

- “In this simulation…”  
- “Measurement-based within the model…”  
- “Synthetic training data for the demonstrator…”  
- “Hybrid mode keeps a safety gate around the ML proposal…”  
- “Structured for later eADM connection without redesigning the decision interface…”  

**Avoid**

- “Operational EW system” / “field-proven” / “real-time RF warfare”  
- “Fully trained / validated ML for deployment”  
- “Detects any jammer automatically in theatre”  
- Absolute performance guarantees (BER, range, classification % in the field)

---

## One-line closing (optional)

> This demonstration shows a closed-loop Cognitive Radio decision path under jamming in software — sensing, rules and ML with hybrid safety, and bounded actuation — as a technical baseline for further defence evaluation.
