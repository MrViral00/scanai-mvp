
# ScanAI – Deepfake Detection with Deepware API

This version of ScanAI uses the Deepware API to detect deepfakes in videos.

## Setup

1. Add your Deepware API key in `.streamlit/secrets.toml`:
```toml
DEEPWARE_API_KEY = "your_deepware_key"
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app/main.py
```

## Upload Limit
- Max video size: 200MB (Streamlit Cloud default)

## Output
- Get report ID
- Manual report link provided
