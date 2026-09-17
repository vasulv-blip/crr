# Cognitive Radio Simulation — UI Options Guide

**Audience:** Demo presenters and reviewers (including Shri S. K. Sir / senior defence scientists)  
**App:** Cognitive Radio Channel Selection under Jamming  
**Location:** `cognitive_radio_sim/` (Streamlit app at `http://localhost:8501`)

This note collects the meanings of the main on-screen options discussed so far. Use numbered points only.

---

## 1. How to start the simulation

1. From folder `cognitive_radio_sim`, run: `python -m streamlit run app.py --server.port 8501`
2. Open the browser at: `http://localhost:8501`
3. Prefer view: **System Architecture & Node View** for senior-scientist demos

---

## 2. Top-level view selection (sidebar)

1. **System Architecture & Node View**  
   Shows the modular Jammer / Receiver / Transmitter panels plus the Cognitive Decision Engine explainability trace. This is the agreed look-and-feel for defence presentation.
2. **Operator Spectrum View**  
   Shows a more operator-style spectrum / metrics layout. Jammer controls appear mainly in the sidebar for this view.

---

## 3. Sidebar — Configuration

### 3.1 Number of channels (N)

1. Selects how many discrete channels the simulator uses (for example 4, 6, 8, 12, 16).
2. Larger N gives a wider spectrum map and a larger ML feature vector.
3. After changing N, click **Apply configuration** so the engine and ML retrain for the new size.

### 3.2 Decision engine

1. **RULES** — deterministic baseline (prefer best FREE, else best DEGRADED, else increase power).
2. **ML** — supervised MLP recommender with safety checks.
3. **HYBRID** — ML proposes; deterministic safety validates or overrides (preferred for defence demos).

### 3.3 Cognitive / adaptive hopping

1. When **Off**: radio operates as single-carrier (or without live hop-pool rebuild). This is the usual opening state for a clean baseline demo.
2. When **On**: after decisions, the hop pool can be updated by `adapt_hop_set` — jammed (BLOCKED) hop members are evicted and clean usable channels are filled in.
3. This is the control that demonstrates **dynamic frequency hopping based on cognitive decisions**.

### 3.4 Jam power (linear a.u.)

1. Visible mainly in Operator Spectrum View sidebar (in Architecture view, jam power is set inside the Jammer node).
2. Sets relative jammer interference strength on the same linear scale as the noise model.
3. Higher values produce stronger interference and more BLOCKED / DEGRADED channels.

### 3.5 SINR FREE threshold (dB)

1. Default typically **10.00 dB** — keep this; it is a good operational “good link” bar.
2. Channels with SINR **≥ this value** are classified **FREE** (green).
3. Raising the threshold makes the system stricter (fewer FREE channels).
4. Lowering it makes more channels appear FREE (not recommended just to force a green startup).

### 3.6 SINR BLOCKED threshold (dB)

1. Default typically **3.00 dB** — keep this; it is a good operational “denied link” bar.
2. Channels with SINR **< this value** are classified **BLOCKED**.
3. Channels between BLOCKED and FREE thresholds are **DEGRADED**.
4. Raising this threshold marks more channels as blocked; lowering it is more tolerant of interference.

### 3.7 Maximum TX power (dB)

1. Default typically **20.00 dB**.
2. Upper limit for transmitter power / burn-through advice.
3. Under barrage-like denial, the engine may recommend **INCREASE_POWER**, but only within this ceiling.
4. Power headroom = Maximum TX power − current TX power.
5. Benign startup TX power defaults to about **12 dB** (between min 0 and max 20) so the first screen is green FREE before jam; jamming then turns tiles DEGRADED / BLOCKED.

### 3.8 Seed / reproducibility (optional expander)

1. **Hidden by default** — open the expander only if needed.
2. Sets the random seed used for repeatable simulation / training behaviour.
3. Default seed is typically **42** when left unchanged.
4. Change this only when you need a controlled, reproducible experiment.

### 3.9 Apply configuration

1. Applies the sidebar settings to the live simulator.
2. Resets the orchestration config and retrains the ML recommender for the current N.
3. Takes a fresh step so the UI reflects the new configuration.

---

## 4. Run control (sidebar)

### 4.1 Single step

1. Runs **one** full Sense–Decide–Act cycle.
2. In one step: interference is applied / updated → Receiver senses → Decision Engine recommends → Transmitter acts.
3. Best control for live scientific presentation (show one change at a time).

### 4.2 Auto steps

1. Number only (typically 1–50). Example value: **5**.
2. Does nothing by itself.
3. Defines how many cycles **Run auto steps** will execute.

### 4.3 Run auto steps

1. Repeats the full cycle N times (the Auto steps value), then refreshes the UI.
2. Useful for Sweep jamming or adaptive hopping, where behaviour evolves over several steps.
3. Less suitable than Single step when explaining each transition to a panel.

### 4.4 Reset simulation

1. Clears the current run and returns to a fresh start.
2. Retrains ML and takes an initial step.
3. Use between demo scenes so the screen is clean again.

---

## 5. Jammer node (Architecture view)

These controls create the **adversary Electronic Attack (ECM)** in the simulation.  
They do **not** change friendly radio settings directly; they inject interference into the contested RF medium so the Receiver and Decision Engine must react.

### 5.0 On-screen jammer controls (quick meaning)

1. **ECM Threat Profile** — chooses the jammer pattern: NONE, SPOT, MULTI_SPOT, SWEEP, or BARRAGE. Changing the dropdown only selects the mode; jamming starts when you press Emit Jam (or a Quick Threat Preset).
2. **Jam power (linear a.u.)** — sets how strong the interference is (example 40.00). Higher power makes SINR worse and more channels DEGRADED / BLOCKED. This is jammer strength, not friendly TX power.
3. **Emit Jam** — turns the selected threat on with the chosen profile + power (+ targets if Spot/Multi), then runs one Sense–Decide–Act step so Receiver / Decision Engine / Transmitter update immediately.
4. **Silence Jam** — turns jamming off / clears the threat, then runs one step so the UI refreshes and channels can recover.
5. **Typical demo flow** — start with NONE (baseline) → set SPOT and power 40 → Emit Jam → show Receiver BLOCKED and cognitive response → Silence Jam when finished.

### 5.1 ECM Threat Profile

1. This dropdown chooses **what kind of jamming waveform / pattern** the adversary will use.
2. **NONE** — no active ECM. Jammer is standby / benign. Use this for the clean baseline before a contested demo.
3. **SPOT** — concentrates jam power on one (or selected) channel. Typical demo: jam the active friendly carrier so that channel becomes BLOCKED and the cognitive radio must hop away.
4. **MULTI_SPOT** — jams several selected channels at once. Shows that the radio must avoid more than one denied frequency.
5. **SWEEP** — moves the jam energy across channels over successive steps (with adjacent bleed in the model). Best shown with Single step / Auto steps so the blocked window marches across the spectrum map.
6. **BARRAGE** — spreads strong interference across the whole band. Often forces power advice (INCREASE_POWER) when no FREE channel remains.
7. Changing the dropdown alone does **not** always start jamming until you press **Emit Jam** (or use a Quick Threat Preset).

### 5.2 Jam power (linear a.u.)

1. Sets **how strong** the jammer interference is, in linear arbitrary units (same scale family as the noise model).
2. Higher values (for example 40, 60, 80) make SINR worse on targeted channels and increase the chance of DEGRADED / BLOCKED classifications.
3. Lower values make milder interference (channels may stay DEGRADED instead of BLOCKED).
4. This value is applied when you **Emit Jam** (or use a preset that emits).
5. It is **not** the friendly transmitter power; friendly TX power is controlled separately (Transmitter panel / Maximum TX power).

### 5.3 Target channels (when shown)

1. Appears for Spot / Multi-Spot style profiles.
2. Lets you choose which channel IDs receive the jam power.
3. Example: target CH0 to deny the usual baseline carrier.

### 5.4 Emit Jam

1. **Applies** the selected ECM Threat Profile, jam power, and target channels into the simulator.
2. Then advances **one** Sense–Decide–Act step so Receiver, Decision Engine, and Transmitter update immediately.
3. Use this button to start a contested scenario during presentation.
4. After Emit Jam, point to the Receiver spectrum map to show **interference capture**.

### 5.5 Silence Jam

1. **Turns off / clears** active jamming and returns the threat toward a clear / benign state.
2. Then advances one step so the UI refreshes (channels can recover toward FREE depending on conditions).
3. Use this to end a jam scenario or return to baseline without a full Reset.

### 5.6 Typical presenter sequence for these four controls

1. Leave profile **NONE**, confirm benign baseline.
2. Set profile to **SPOT**, set jam power (for example **40**), choose target if needed.
3. Click **Emit Jam** — show Receiver BLOCKED / Decision Engine response / Transmitter retune.
4. Click **Silence Jam** when you want the threat cleared again.
5. For barrage / sweep demos, change profile accordingly, then Emit Jam again.

### 5.7 Quick Threat Presets (optional expander)

1. **Hidden by default** — open only when one-click scenarios are useful.
2. **Spot CH0** — spot jam on channel 0.
3. **Multi CH0,1** — multi-spot jam on channels 0 and 1.
4. **Sweep Jam** — start sweep-profile jamming.
5. **Barrage Jam** — start full-band barrage jamming.
6. These are shortcuts; the same effects can be created manually with profile + jam power + Emit Jam.

---

## 6. Receiver node (Architecture view) — what the readings mean

This panel is the **Electronic Support (ES) sensing** view.  
It shows how the friendly system **captures interference** from measurements (SINR / channel state), not from an oracle jammer label.

### 6.0 On-screen Receiver panel (quick meaning)

1. **RECEIVER (ES SENSING NODE)** — title of the sensing subsystem that surveys the contested spectrum.
2. **Electronic Support Spectrum Surveillance** — short role description: measure link quality across channels.
3. **CONTINUOUS SENSING** — badge meaning sensing is active every simulation step (always watching the band in this demo).
4. **FREE Links** — how many channels currently meet the FREE SINR rule (good / preferred for communication).
5. **DEGRADED Links** — how many channels are impaired but not fully blocked (usable only if nothing better exists).
6. **BLOCKED Links** — how many channels are too jammed / too weak to use safely.
7. **Spectrum Scope (N = 8 CH)** — total number of channels being monitored (here 8).
8. **Cleanest Link** — best current channel by SINR (example CH0 at 0.0 dB).
9. **Worst Impaired** — poorest current channel by SINR (example CH1 at −3.0 dB).
10. **Applied Criteria** — the classification thresholds currently in force from the sidebar:
    1. FREE if SINR ≥ 10.0 dB
    2. BLOCKED if SINR < 3.0 dB
    3. otherwise DEGRADED (between those two limits)

### 6.1 Header area

1. **Icon + title** identify this as the Receiver / ES node (blue identity in the modular look-and-feel).
2. **CONTINUOUS SENSING** means the demo is continuously evaluating all N channels each step; there is no separate “start sensing” button.

### 6.2 FREE / DEGRADED / BLOCKED counts

1. These three counts are the live result of **interference capture**.
2. Example from a contested screen: FREE = 0, DEGRADED = 7, BLOCKED = 1, Scope = 8.
3. That means: out of 8 monitored channels, none are fully clean, seven are partially impaired, and one is denied.
4. The Cognitive Decision Engine uses this partition to avoid BLOCKED channels and prefer FREE (or best DEGRADED if needed).

### 6.3 Spectrum Scope

1. Shows **N**, the configured number of channels (sidebar: Number of channels).
2. Example **N = 8 CH** means the Receiver is classifying CH0 … CH7.

### 6.4 Cleanest Link and Worst Impaired

1. **Cleanest Link** highlights the best measured SINR among current observations.
2. **Worst Impaired** highlights the poorest measured SINR.
3. Important: “cleanest” is relative. If the whole band is contested, the cleanest channel may still be DEGRADED (for example 0.0 dB), not FREE.
4. Use these two lines when explaining to scientists that sensing is quantitative, not just colour labels.

### 6.5 Applied Criteria

1. Shows the active decision thresholds coming from sidebar controls:
    1. **SINR FREE threshold** (default 10.0 dB)
    2. **SINR BLOCKED threshold** (default 3.0 dB)
2. Changing those sidebar sliders and clicking **Apply configuration** changes how FREE / DEGRADED / BLOCKED are assigned.
3. Formula reminder used in the model: SINR depends on received friendly power versus noise + jam power.

### 6.6 Channel Spectrum State Map (below this panel on the full screen)

1. Each tile is one channel with state colour and SINR value.
2. Green-style = FREE, amber-style = DEGRADED, red-style = BLOCKED.
3. This map is the clearest visual for “we captured interference on these frequencies.”

### 6.7 How to narrate this panel in a demo

1. Point to FREE / DEGRADED / BLOCKED counts after Emit Jam.
2. Say: “This is interference capture — the Receiver classifies channels from measured SINR.”
3. Point to Applied Criteria to show the thresholds are configurable and transparent.
4. Then point to Decision Engine / Transmitter to show the cognitive response to this sensing picture.

---

## 7. Transmitter node (Architecture view) — what the readings mean

1. **Active Carrier** — channel currently used for friendly transmission.
2. **Transmit Power** — current TX power in dB.
3. **Power Headroom** — remaining room up to Maximum TX power.
4. **Hopping Mode** — Single Carrier vs Adaptive (when cognitive hopping is enabled).
5. **Active Hop Pool** — current hop-set members when hopping is enabled; otherwise disabled.

### 7.0 Attached Neural Coprocessor / Attached ML Policy (quick meaning)

This green card is the **machine-learning recommender attached to the Transmitter**.  
It proposes a channel or power action from sensing features. In HYBRID mode, a safety gate still validates before actuation.

1. **ATTACHED NEURAL COPROCESSOR** — presentation label for the on-board / attached ML decision helper (software twin of a neural recommender).
2. **ATTACHED ML POLICY (MLP RECOMMENDER)** — the actual model type: a Multi-Layer Perceptron classifier used as a channel / power recommender.
3. **NEURAL ENGINE** — badge meaning the ML path is the active recommender engine for this proposal (as opposed to pure RULES-only wording).
4. **Architecture: Feed-Forward MLP (64 × 32, ReLU, Adam)**  
   1. Feed-forward MLP = standard neural classifier (not reinforcement learning in this demo).  
   2. **64 × 32** = two hidden layers with 64 and 32 neurons.  
   3. **ReLU** = activation function inside hidden layers.  
   4. **Adam** = training optimiser used when the model is trained on synthetic cases.
5. **Input Vector: 26 normalized sensing features**  
   1. For N = 8 channels, feature length is **3N + 2 = 26**.  
   2. Per channel: SINR, state encoding (FREE/DEGRADED/BLOCKED), jam power.  
   3. Plus current TX power and remaining power headroom.  
   4. “Normalized” means features are scaled (StandardScaler) before the MLP sees them.
6. **Neural Proposal: Recommend CH1** — the model’s chosen class / recommendation right now (use channel 1).
7. **Softmax Confidence: 1.00 (99%)** — how strongly the model prefers that proposal (highest class probability). Near 1.00 means very high certainty for this step.
8. **Dispatched Action: USE_CHANNELS** — the action actually sent for actuation after decision/safety processing (use the recommended channel set / carrier). Other possible actions include INCREASE_POWER or no-solution / hold style outcomes in harder cases.

### 7.1 How to narrate this card to defence scientists

1. Say: “This is the transmitter-attached ML recommender.”
2. Point to Architecture / Input Vector to show it is a small inspectable MLP on sensing telemetry, not a black-box vision model.
3. Point to Neural Proposal + Confidence as the ML suggestion for this step.
4. Point to Dispatched Action as what was actually executed after hybrid safety (in HYBRID / ML modes).
5. Remind: ML is **advisory inside safety containment**; it does not freely command unsafe BLOCKED hops.

### 7.2 Related Transmitter ML note

1. If Decision engine = RULES, behaviour is deterministic baseline (ML card may still show structure, but RULES drives the decision path).
2. If Decision engine = ML or HYBRID, this proposal path is used, with safety checks.
3. Confidence is useful for explanation; safety still overrides unsafe proposals even at high confidence.

---

## 8. Cognitive Decision Engine — explainability stages (summary)

The Decision Engine trace shows the closed-loop decision in numbered stages so a reviewer can see **why** an action was taken.

1. **Stage 1** — sensing evidence / usable vs blocked partitioning (FREE / DEGRADED / BLOCKED sets from Receiver observations).
2. **Stage 2** — Transmitter-attached ML policy inference (neural proposal + Softmax confidence). See 8.1 below.
3. **Stage 3** — hybrid safety gate (for example veto hops into BLOCKED; check power headroom).
4. **Stage 4** — cognitive adaptive hop-set update when hopping is enabled.
5. **Stage 5** — final dispatched action and human-readable rationale.

### 8.1 Stage 2: Transmitter-Attached ML Policy Inference (what it means)

1. Stage 2 is the **machine-learning recommendation step**.
2. It means: the Transmitter-attached MLP has read the current sensing state and produced a **proposal**.
3. **26-dimensional state vector** — for N = 8, input length is 3N+2 = 26 (SINR, state, jam per channel + TX power + headroom), standardized before inference.
4. **Softmax probabilities across 8 channel classes + power-increase class** — the network scores every possible action class (CH0…CH7 and INCREASE_POWER) and converts scores to probabilities.
5. **Neural Model Proposal: Recommend CH1** — the class with the highest probability right now is “use channel 1”.
6. **Softmax confidence 1.00 (99%)** — that highest probability is essentially 1.0, so the model is highly certain about CH1 for this step.
7. Important: Stage 2 is the **proposal**, not yet the final hardened command. Stage 3 safety still checks whether that proposal is allowed.
8. Demo line to say: “Stage 2 is the neural recommender’s suggestion and confidence. Next, Stage 3 verifies it against safety rules.”

---

## 9. Recommended demo mapping to SK priorities

1. **Agreed look-and-feel** — use System Architecture & Node View (Jammer / Receiver / Transmitter / Decision Engine).
2. **Capturing interference** — point to Receiver FREE / DEGRADED / BLOCKED map after Emit Jam / Spot.
3. **Dynamic FH based on cognitive decisions** — turn **Cognitive / adaptive hopping** On, jam a hop-set member, Single step, and show Active Hop Pool eviction / refill.

---

## 10. Quick presenter cheat sheet

1. Baseline: Decision engine = HYBRID, hopping Off, jammer NONE, then Single step.
2. Interference capture: Spot / Emit Jam on active carrier, then Single step; show Receiver BLOCKED tile.
3. Cognitive hopping: enable Cognitive / adaptive hopping; jam a hop member; Single step; show hop pool change.
4. Barrage / power: Barrage Jam; Single step; show INCREASE_POWER if headroom remains.
5. Between scenes: Reset simulation.
6. Seed and Quick Threat Presets stay collapsed unless specifically needed.

---

## 11. Related documents

1. `Cognitive_Radio_Simulation_Presentation_Guide_for_Defence_Scientists.docx` — how to present the demo.
2. `Cognitive_Radio_Simulation_Presentation_for_Defence_Scientists.pptx` — slide deck with architecture and UI figures.
3. `Cognitive_Radio_Simulation_ML_QA_Brief.docx` — ML-focused Q&A.
4. `Cognitive_Radio_Simulation_Scenarios_Brief_for_SK_Sir.docx` — scenario-by-scenario technical brief.

---

*Prepared for eAge Innovations Cognitive Radio software demonstration use.*
