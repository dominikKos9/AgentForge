import streamlit as st
import os
import uuid

from backend.main import run_agentforge


st.set_page_config(page_title="Glasovni opisivač", layout="centered")


st.markdown(
    "<h1 style='text-align:center; font-size:42px;'>"
    "Glasovni opisivač za slijepe i slabovidne osobe"
    "</h1>",
    unsafe_allow_html=True
)

st.write("")


if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "history" not in st.session_state:
    st.session_state.history = []


st.markdown(
    """
    <style>
    .uploadBox {
        display: flex;
        justify-content: center;
        margin-top: 40px;
    }

    .bigUpload {
        font-size: 20px;
        font-weight: 600;
    }

    .stFileUploader {
        width: 450px !important;
        transform: scale(1.2);
    }

    .detailedBox {
        display: flex;
        justify-content: center;
        margin-top: 30px;
        font-size: 22px;
    }

    .historyBox {
        margin-top: 50px;
        padding: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.markdown("<div class='uploadBox'><h2>Odaberi sliku</h2></div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"])


detailed = st.checkbox("Detaljan opis", value=False)


st.write("")
st.write("")


run = st.button("🔊 Generiraj opis", use_container_width=True)


if uploaded_file and run:

    session_id = st.session_state.session_id

    user_dir = f"data/{session_id}"
    os.makedirs(user_dir, exist_ok=True)

    image_path = os.path.join(user_dir, uploaded_file.name)

    with open(image_path, "wb") as f:
        f.write(uploaded_file.read())

    result = run_agentforge(
    image_path,
    session_id=session_id,
    detailed=detailed   
    )

   
    st.session_state.history.append({
        "image": image_path,
        "description": result.get("description"),
        "audio": result.get("audio_path")
    })

    st.session_state.history = st.session_state.history[-5:]


 
    if result.get("valid_image") is False:
        st.error(result.get("error"))
        st.stop()



    st.subheader("Opis slike")
    st.write(result.get("description"))

    if result.get("audio_path"):
        st.audio(result["audio_path"])



st.write("")
st.markdown("## 🕘 Zadnjih 5 opisa")

if len(st.session_state.history) == 0:
    st.write("Još nema spremljenih opisa.")

else:

    for i, item in enumerate(reversed(st.session_state.history)):

        col1, col2 = st.columns([1, 3])

        with col1:
            if os.path.exists(item["image"]):
                st.image(item["image"], width=140)

        with col2:

            preview = item["description"][:120] + "..."

            st.write(preview)

            if st.button(
                "🔊 Otvori opis",
                key=f"history_{i}"
            ):

                st.session_state.selected_history = item


if "selected_history" in st.session_state:

    item = st.session_state.selected_history

    st.markdown("---")
    st.subheader("📄 Spremljeni opis")

    if os.path.exists(item["image"]):
        st.image(item["image"], width=400)

    st.write(item["description"])

    if (
        item.get("audio")
        and os.path.exists(item["audio"])
    ):
        st.audio(item["audio"])