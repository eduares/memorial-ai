import os
import streamlit as st

from ingestion import ingest_document
from extractor_json import extract_all_parameters
from chatbot import ask_question

from config import UPLOAD_FOLDER

from ui.styles import load_css
from ui.sidebar import render_sidebar
from ui.chat import render_chat


# =========================
# CONFIG PAGE
# =========================

st.set_page_config(
    page_title="Memorial AI",
    page_icon="📄",
    layout="wide"
)

# =========================
# LOAD CSS
# =========================

load_css()

# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_loaded" not in st.session_state:
    st.session_state.document_loaded = False

if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None

# =========================
# SIDEBAR
# =========================

uploaded_file = render_sidebar()

# =========================
# MAIN HEADER
# =========================

st.markdown(
    """
    <div class="main-title">
        📄 Memorial AI
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Assistente Inteligente para Orçamentos
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# PROCESS DOCUMENT
# =========================

if uploaded_file is not None and not st.session_state.document_loaded:

    file_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Processando memorial..."):

        ingest_document(
            file_path,
            uploaded_file.name
        )

        extracted_data = extract_all_parameters()

        st.session_state.extracted_data = extracted_data
        st.session_state.document_loaded = True

    st.success("Memorial processado com sucesso!")

# =========================
# PARAMETERS
# =========================

if st.session_state.extracted_data:

    with st.expander("📌 Parâmetros Extraídos"):

        st.json(st.session_state.extracted_data)

# =========================
# CHAT HISTORY
# =========================

render_chat(st.session_state.messages)

# =========================
# CHAT INPUT
# =========================

user_question = st.chat_input(
    "Faça uma pergunta sobre o memorial..."
)

if user_question:

    if not st.session_state.document_loaded:

        st.warning(
            "Envie um memorial antes de realizar perguntas."
        )

    else:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        with st.spinner("Pensando..."):

            response = ask_question(user_question)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()