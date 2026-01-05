import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Pneumonia Detection System",
    page_icon="🫁"
)

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("pneumonia_model.h5")

model = load_model()

st.title("🫁 Pneumonia Detection System (AI Powered)")
st.write("Upload a chest X-ray image to detect Pneumonia.")

def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

uploaded_file = st.file_uploader(
    "Upload Chest X-ray Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded X-ray", use_column_width=True)

    if st.button("Detect Pneumonia"):
        with st.spinner("Analyzing X-ray..."):
            img = preprocess_image(image)
            prediction = model.predict(img)[0][0]

            if prediction >= 0.5:
                st.error("🩺 Pneumonia Detected")
                st.write(f"Confidence: {prediction*100:.2f}%")
            else:
                st.success("✅ Normal Lungs")
                st.write(f"Confidence: {(1-prediction)*100:.2f}%")
