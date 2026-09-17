# Deploy on Streamlit Community Cloud

This app is ready to deploy from GitHub: **https://github.com/vasulv-blip/crr**

## One-time deploy steps

1. Open **https://share.streamlit.io** and sign in with the **same GitHub** account that owns `vasulv-blip/crr`.
2. Click **Create app**.
3. Choose **Yup, I have an app** (existing GitHub repo).
4. Fill in:
   - **Repository:** `vasulv-blip/crr`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Optional: set a custom subdomain (e.g. `crr-demo` → `https://crr-demo.streamlit.app`).
6. **Advanced settings** (recommended):
   - Python version: **3.12** (default is fine)
7. Click **Deploy**.

Wait a few minutes for dependency install + first boot (ML trains once per session after login).

## After deploy

- Public URL looks like: `https://<your-subdomain>.streamlit.app`
- Login: `pocuser` / `poc123`
- To update the live app: push to `crr` `main` on GitHub; Cloud usually redeploys automatically (or use **Reboot** in app settings).

## Local check before redeploy

```bash
git clone https://github.com/vasulv-blip/crr.git
cd crr
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- Repo root already has `app.py`, `requirements.txt`, and `.streamlit/config.toml` (what Community Cloud expects).
- First load after login trains a small ML model; a spinner is shown.
- Do not commit secrets; demo login is intentional for the defence demo.
