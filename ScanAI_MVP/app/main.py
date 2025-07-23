
import streamlit as st
import requests
import io

DEEPWARE_API_KEY = st.secrets["DEEPWARE_API_KEY"]

def deepware_scan_video(file_obj):
    url = "https://api.deepware.ai/api/v1/video/scan"
    headers = {"X-Deepware-Authentication": DEEPWARE_API_KEY}
    files = {"video": ("upload.mp4", file_obj, "video/mp4")}
    res = requests.post(url, headers=headers, files=files)
    if res.status_code != 200:
        st.error(f"Scan failed: {res.status_code} - {res.text}")
        return None
    return res.json()

def deepware_get_report(report_id):
    url = f"https://api.deepware.ai/api/v1/report/{report_id}"
    headers = {"X-Deepware-Authentication": DEEPWARE_API_KEY}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        st.error(f"Report fetch failed: {res.status_code} - {res.text}")
        return None
    return res.json()

st.set_page_config(page_title="ScanAI - Deepfake Detector", layout="centered")
st.title("🎭 ScanAI (Deepware)")
st.subheader("Upload a video to check for deepfakes")

uploaded_file = st.file_uploader("Upload a video (MP4, MOV)", type=["mp4", "mov"])

if uploaded_file:
    file_bytes = uploaded_file.read()
    st.video(io.BytesIO(file_bytes))
    scan_result = deepware_scan_video(io.BytesIO(file_bytes))
    if scan_result and "report-id" in scan_result:
        report_id = scan_result["report-id"]
        st.success(f"Scan started. Report ID: {report_id}")
        st.info("Waiting ~30–60 seconds before report becomes available.")
        st.markdown(f"🔗 Manually check your report here: https://scanner.deepware.ai/report/{report_id}")
    else:
        st.error("Deepware scan failed.")
