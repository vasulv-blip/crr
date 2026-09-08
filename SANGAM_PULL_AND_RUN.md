# Instructions for Sangam — Pull and Run the Cognitive Radio Simulation

Follow these steps in order.

---

## 1. Get the latest code from GitLab

1. Open a terminal (PowerShell or Command Prompt).
2. Go to your local copy of the repository:

```bash
cd C:\work\projectx\embdeeded\proposalprojects
```

If you do not have the repo yet:

```bash
cd C:\work\projectx\embdeeded
git clone https://gitlab.com/eagerd1/proposalprojects.git
cd proposalprojects
```

3. Fetch and check out the lab branch:

```bash
git fetch origin
git checkout lab/eadm-sdr-lab
git pull origin lab/eadm-sdr-lab
```

4. Confirm the simulation folder exists:

```bash
dir cognitive_radio_sim
```

You should see `app.py`, `requirements.txt`, `USER_GUIDE.md`, and the `cr_sim` folder.

---

## 2. Which files to refer to

| File | Purpose |
|------|---------|
| `cognitive_radio_sim/USER_GUIDE.md` | Quick markdown guide (scenarios) |
| `cognitive_radio_sim/Cognitive_Radio_Simulation_User_Guide.docx` | **Main numbered step-by-step Word guide — use this to operate the software** |
| `cognitive_radio_sim/README.md` | Short overview of the project |
| `cognitive_radio_sim/app.py` | Application entry point (do not need to edit to run) |
| `cognitive_radio_sim/requirements.txt` | Python packages to install |

**Primary document for operating the demo:**  
`cognitive_radio_sim/Cognitive_Radio_Simulation_User_Guide.docx`

---

## 3. How to run the application

1. Go into the simulation folder:

```bash
cd cognitive_radio_sim
```

2. Install dependencies (first time only):

```bash
python -m pip install -r requirements.txt
```

3. Start the app:

```bash
python -m streamlit run app.py
```

4. Open the browser at:

**http://localhost:8501**

5. To stop the app: press `Ctrl+C` in the terminal.

---

## 4. What to do after it opens

1. Open **Cognitive_Radio_Simulation_User_Guide.docx**.
2. Follow **Section 8 — Step-by-step demonstration script** (numbered scenarios).
3. Start with Scenario 1 (Clear jam → Single step), then jam scenarios.

---

## 5. If something fails

| Problem | Action |
|---------|--------|
| Branch or folder not found | Ask the team to confirm `cognitive_radio_sim` was committed and pushed to `lab/eadm-sdr-lab` |
| `streamlit` not recognised | Use `python -m streamlit run app.py` |
| Page blank / not loading | Open http://localhost:8501 manually |
| Settings not applying | Click **Apply configuration** in the sidebar after changes |

---

## 6. One-line summary for Sangam

```text
git checkout lab/eadm-sdr-lab → git pull → cd cognitive_radio_sim →
python -m pip install -r requirements.txt →
python -m streamlit run app.py → open http://localhost:8501 →
follow Cognitive_Radio_Simulation_User_Guide.docx
```
