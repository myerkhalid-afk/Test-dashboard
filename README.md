# Token & Usage Dashboard

A Streamlit dashboard for tracking AI token usage, estimated costs, cached-token savings, and context pressure.

## Run locally

```powershell
cd C:\Users\Myer\Documents\Storage
& 'C:\Users\Myer\AppData\Local\Python\bin\python.exe' -m streamlit run streamlit_app.py --server.port 8502
```

## Deploy on Streamlit Community Cloud

Use these settings:

- Repository: your GitHub repo containing these files
- Branch: `main`
- Main file path: `streamlit_app.py`
- Python version: default is fine

The app uses manual inputs and optional CSV upload. It does not connect to private billing APIs by default.

