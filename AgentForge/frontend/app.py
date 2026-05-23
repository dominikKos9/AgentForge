import streamlit as st
import os

from backend.main import run_agentforge

st.title("AgentForge")


uploaded_file = st.file_uploader(
    "Upload image",
    type=["png", "jpg", "jpeg"]
)


if uploaded_file:

    # keep original extension
    file_ext = uploaded_file.name.split(".")[-1]
    temp_path = f"temp.{file_ext}"

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())


    result = run_agentforge(temp_path)


    # -------------------
    # ERROR HANDLING
    # -------------------
    if result.get("valid_image") is False:
        st.error(result.get("error", "Invalid image"))
        st.stop()


    # -------------------
    # OUTPUT
    # -------------------
    if result.get("description"):
        st.subheader("Description")
        st.write(result["description"])


    if result.get("audio_path") and os.path.exists(result["audio_path"]):
        st.subheader("Audio")
        st.audio(result["audio_path"])