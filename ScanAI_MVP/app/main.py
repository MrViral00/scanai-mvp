
import streamlit as st
from PIL import Image
import requests
import io

HIVE_API_KEY = st.secrets["HIVE_API_KEY"]
DEEPWARE_API_KEY = st.secrets["DEEPWARE_API_KEY"]

def hive_detect_image(file_bytes):
    url = "https://api.thehive.ai/v1/moderation/detect/ai-generated-image-and-video"
    headers = {"Authorization": HIVE_API_KEY}
    files = {"media": ("upload.jpg", file_bytes, "image/jpeg")}
    res = requests.post(url, headers=headers, files=files)

    st.write("Hive response status:", res.status_code)
    st.write("Hive raw response text:", res.text)  # Add this line

    return res.json()  # This line might still crash, but now you'll know why

def deepware_scan_video(file_obj):
    url = "https://api.deepware.ai/api/v1/video/scan"
    headers = {"X-Deepware-Authentication": DEEPWARE_API_KEY}
    files = {"video": ("upload.mp4", file_obj, "video/mp4")}
    return requests.post(url, headers=headers, files=files).json()

st.set_page_config(page_title="ScanAI", layout="centered")
st.title("🔍 ScanAI")
st.subheader("Spot the Fake. Trust the Real.")

uploaded_file = st.file_uploader("Upload an image or video", type=["jpg", "jpeg", "png", "mp4", "mov"])

if uploaded_file:
    file_bytes = uploaded_file.read()
    if uploaded_file.type.startswith("image"):
        st.image(Image.open(io.BytesIO(file_bytes)), caption="Uploaded Image")
        result = hive_detect_image(file_bytes)
        st.markdown("### 🧠 Scan Results (Image):")
        st.write(result)
    elif uploaded_file.type.startswith("video"):
        st.video(io.BytesIO(file_bytes))
        result = deepware_scan_video(io.BytesIO(file_bytes))
        st.markdown("### 🧠 Scan Results (Video):")
        st.write(result)
