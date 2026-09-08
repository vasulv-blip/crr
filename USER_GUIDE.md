# Cognitive Radio Simulation — User Guide

Simple guide to run the software demonstration and walk through the main scenarios.

---

## 1. How to run

1. Open a terminal (PowerShell or Command Prompt).
2. Go to the application folder:

```bash
cd C:\work\projectx\embdeeded\proposalprojects\cognitive_radio_sim
```

3. Install dependencies (first time only):

```bash
python -m pip install -r requirements.txt
```

4. Start the application:

```bash
python -m streamlit run app.py
```

5. Open the browser at:

- **http://localhost:8501**

If the browser does not open automatically, paste that address into Chrome / Edge.

To stop the app: press `Ctrl+C` in the terminal.

---

## 2. What you see on the screen

| Area | Meaning |
|------|---------|
| **Channel map** | All channels. Green = FREE, amber = DEGRADED, red = BLOCKED. Gold border = active transmit channel. |
| **Cognitive Radio response** | Status code + human-readable message. |
| **Decision detail** | Engine used (RULES / ML / HYBRID), action, recommended channels, power advice, hop set. |
| **Left sidebar** | Configuration, jam injection, and run controls. |
| **Recent decision history** | Last decisions for review. |

---

## 3. Recommended first walkthrough (5–7 minutes)

### Step A — Clean spectrum (no jam)

1. In the sidebar, click **Clear jam**.
2. Click **Single step** once or twice.
3. **Expected:** Most/all channels FREE. Status usually `OK`. Active TX on a free channel.

### Step B — Spot / multi-spot jam

1. Set **Jam profile** to `MULTI_SPOT`.
2. Select target channels, e.g. `0` and `1`.
3. Click **Apply jam**, then **Single step**.
4. **Expected:** CH0 and CH1 turn BLOCKED (red). CR recommends another free channel (e.g. CH4). Transmitter moves off the jammed channels.

### Step C — Sweep jam

1. Set **Jam profile** to `SWEEP`.
2. Click **Apply jam**.
3. Click **Run auto steps** (e.g. 5–10 steps).
4. **Expected:** The blocked channel moves over time. CR keeps recommending a usable channel as the jam sweeps.

### Step D — Barrage (all channels stressed)

1. Set **Jam profile** to `BARRAGE`.
2. Click **Apply jam**, then **Single step** a few times.
3. **Expected:** Many/all channels BLOCKED. Status becomes `INCREASE_POWER` (if power can still rise) or `ALL_BLOCKED` (if already at maximum).
4. Watch **TX power** increase when `INCREASE_POWER` is returned.

### Step E — Cognitive / adaptive hopping

1. Turn **Cognitive / adaptive hopping** ON.
2. Click **Apply configuration** (re-trains ML for current settings).
3. Apply `SWEEP` or `MULTI_SPOT` jam.
4. Run several auto steps.
5. **Expected:** Hop set is shown in Decision detail; jammed members can be dropped and clean channels added.

### Step F — Compare RULES vs ML vs HYBRID

1. Set **Decision engine** to `RULES` → **Apply configuration** → inject jam → step.
2. Repeat with `ML`, then `HYBRID`.
3. **Expected:** Same response format every time (status + message + channels / power advice). HYBRID uses ML with safety rules.

---

## 4. Scenario checklist for review

Use this table during a formal demonstration.

| # | Scenario | Actions | What to look for |
|---|----------|---------|------------------|
| 1 | No jam | Clear jam → Single step | All/mostly FREE; `OK` |
| 2 | Spot jam | Profile `SPOT`, one channel → Apply jam | One red cell; CR switches away |
| 3 | Multi-spot | Profile `MULTI_SPOT`, 2+ channels → Apply jam | Several red cells; CR picks free channel |
| 4 | Sweep | Profile `SWEEP` → Auto steps | Blocked marker moves; CR adapts |
| 5 | Barrage + power | Profile `BARRAGE` → several steps | `INCREASE_POWER` then possible recovery |
| 6 | Max power exhausted | Barrage at max TX power | `ALL_BLOCKED` message |
| 7 | Adaptive hopping | Hopping ON + sweep/multi-spot | Hop set updates; TX follows hop set |
| 8 | ML path | Engine `ML` or `HYBRID` + jam | Message mentions ML / confidence; same API fields |
| 9 | Quick toggle | Use **Quick jam toggle** buttons CH0… | Instant jam on/off for live demo |

---

## 5. Useful sidebar controls

| Control | Use |
|---------|-----|
| **Number of channels (N)** | Try 4, 8, or 16. Click **Apply configuration** after changing. |
| **Decision engine** | `RULES`, `ML`, or `HYBRID`. |
| **Cognitive / adaptive hopping** | Enable for hop-set demo. |
| **Jam power** | Higher = harder blockage. |
| **SINR thresholds** | Adjust FREE / BLOCKED sensitivity if needed. |
| **Single step** | One closed-loop update. |
| **Run auto steps** | Multiple updates for sweep / power demos. |
| **Reset simulation** | Return to a clean starting point. |

**Important:** After changing N, decision mode, hopping, thresholds, or seed, click **Apply configuration**.

---

## 6. How to read the status codes

| Status code | Meaning |
|-------------|---------|
| `OK` | At least one FREE channel recommended |
| `DEGRADED_OK` | No FREE channel; a usable DEGRADED channel recommended |
| `INCREASE_POWER` | All blocked at current power; raise TX power |
| `ALL_BLOCKED` | Still blocked at maximum allowed power |
| `HOLD` | Keep current allocation (if used) |

---

## 7. Tips for presenting to reviewers

1. Start with **Clear jam** so the map is green.
2. Inject jam live so the audience sees FREE → BLOCKED change.
3. Point to the **message + status code** every time (inspectable decision).
4. Show **barrage → increase power** to demonstrate the “all blocked” path.
5. Optionally switch **RULES → HYBRID** to show ML behind the same interface.
6. Reminder for the audience: this is **software-only** (no radiated RF).

---

## 8. Troubleshooting

| Problem | What to try |
|---------|-------------|
| `streamlit` not recognised | Use `python -m streamlit run app.py` |
| Page does not load | Confirm terminal shows Local URL; open http://localhost:8501 |
| Map does not change | Click **Single step** after applying jam |
| Settings seem ignored | Click **Apply configuration** after sidebar changes |
| ML message says not trained | Click **Apply configuration** or **Reset simulation** (both retrain) |
| Need a clean start | Click **Clear jam**, then **Reset simulation** |

---

## 9. One-page demo script (optional)

1. Open app → show green map (no jam).  
2. Jam CH0 + CH1 → show red cells → CR recommends another channel → TX moves.  
3. Sweep jam → auto steps → blocked cell moves.  
4. Barrage → `INCREASE_POWER` → power rises.  
5. Enable hopping → show hop set adaptation.  
6. Close: same CR API for rules and ML; ready for later eADM connection.

---

*Software demonstration for technical review — eAge Innovations*
