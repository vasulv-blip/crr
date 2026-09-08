# Cognitive Radio Software Simulation

Professional PC demonstration of channel jamming simulation, measurement-based receiver judgement, and Cognitive Radio decisioning (rules / ML / hybrid).

## Run

```bash
cd cognitive_radio_sim
python -m pip install -r requirements.txt
streamlit run app.py
```

## What it demonstrates

- Configurable number of channels `N`
- Jam profiles: none, spot, multi-spot, sweep, barrage
- Receiver labels: FREE / DEGRADED / BLOCKED from SINR measurements
- Cognitive Radio response: status code, message, recommended channels, power advice
- Decision modes: RULES, ML (MLP), HYBRID (ML + safety rules)
- Cognitive / adaptive hopping
- Increase-power path when all channels are blocked

## Project layout

```
cognitive_radio_sim/
  app.py                 # Streamlit UI
  requirements.txt
  cr_sim/
    models.py
    channel.py
    receiver.py
    transmitter.py
    hopping.py
    ml_models.py
    cr_engine.py
    orchestrator.py
```

## Notes

- Software-only; no RF hardware required for this demo.
- Designed for technical review by defence scientists / programme reviewers.
