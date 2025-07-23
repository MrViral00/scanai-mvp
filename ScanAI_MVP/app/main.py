
import streamlit as st
import requests
import io
from PIL import Image
import random
import matplotlib.pyplot as plt
import numpy as np

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

def fake_image_detection(file_bytes):
    return {
        "ai_generated": random.choice([True, False]),
        "confidence": round(random.uniform(87, 99), 2),
        "detected_by": "Simulated GAN Classifier"
    }

def display_color_bar(score):
    fig, ax = plt.subplots(figsize=(6, 1.2))
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap('RdYlGn'), extent=[0, 100, 0, 1])
    ax.axvline(score, color='black', linewidth=2)
    ax.set_yticks([])
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_title(f"Originality Score: {score:.2f}%", fontsize=10)
    ax.set_xlim(0, 100)
    st.pyplot(fig)

st.set_page_config(page_title="ScanAI – Universal AI Detector", layout="centered")
st.title("🧠 ScanAI")
st.subheader("Detect AI-generated Content in Video, Image, Audio, and Text")

option = st.selectbox("What do you want to scan?", ["Video", "Image", "Audio", "Text"])

if option == "Video":
    uploaded_file = st.file_uploader("Upload a video (MP4, MOV)", type=["mp4", "mov"])
    if uploaded_file:
        file_bytes = uploaded_file.read()
        st.video(io.BytesIO(file_bytes))
        scan_result = deepware_scan_video(io.BytesIO(file_bytes))
        if scan_result and "report-id" in scan_result:
            report_id = scan_result["report-id"]
            st.success(f"Scan started. Report ID: {report_id}")
            st.info("Waiting ~30–60 seconds before report becomes available.")
            st.markdown(f"🔗 [View Report on Deepware](https://scanner.deepware.ai/report/{report_id})")
        else:
            st.error("Deepware scan failed.")

elif option == "Image":
    uploaded_image = st.file_uploader("Upload an image (JPG, PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        file_bytes = uploaded_image.read()
        st.image(Image.open(io.BytesIO(file_bytes)), caption="Uploaded Image", use_container_width=True)
        scan_result = fake_image_detection(file_bytes)
        originality = 100 - scan_result["confidence"] if scan_result["ai_generated"] else scan_result["confidence"]
        st.subheader("🧪 Image Originality Score (Simulated)")
        display_color_bar(originality)

elif option == "Audio":
    uploaded_audio = st.file_uploader("Upload audio (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"])
    if uploaded_audio:
        st.audio(uploaded_audio)
        st.warning("⚠️ Audio deepfake detection not yet connected.")

elif option == "Text":
    input_text = st.text_area("Paste text to check if it was written by AI")
    if input_text:
        st.warning("⚠️ Text AI detection not yet connected.")
