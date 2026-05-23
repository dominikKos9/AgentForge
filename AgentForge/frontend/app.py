import streamlit as st

from backend.main import run_agentforge

st.title("AgentForge")

uploaded_file = st.file_uploader(
    "Upload image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.read())

    result = run_agentforge("temp.jpg")

    st.write(result["description"])

    st.audio(result["audio_path"])