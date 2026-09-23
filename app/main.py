# ============================================================
# APLICAÇÃO PRINCIPAL
# ============================================================
# Ponto de entrada da interface Streamlit do Memorial Inteligente.
# Coordena upload, ingestão, extração dos parâmetros e interação por chat.

import os

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
    page_title="Memorial Inteligente",
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

if "document_name" not in st.session_state:
    st.session_state.document_name = None


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
        📄 Memorial Inteligente
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

# Se nenhum arquivo estiver selecionado,
# limpa o estado do documento atual
if uploaded_file is None:

    st.session_state.document_loaded = False
    st.session_state.extracted_data = None
    st.session_state.document_name = None
    st.session_state.document_signature = None


else:

    # Cria uma identificação única para o arquivo
    # usando nome e tamanho
    document_signature = (
        uploaded_file.name,
        uploaded_file.size
    )

    # Verifica se é um documento novo
    new_document = (
        document_signature
        != st.session_state.document_signature
    )

    if new_document:

        # Limpa dados do memorial anterior
        st.session_state.messages = []
        st.session_state.extracted_data = None
        st.session_state.document_loaded = False

        file_path = os.path.join(
            UPLOAD_FOLDER,
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Processando memorial..."):

            # Ingestão do novo memorial
            ingest_document(
                file_path,
                uploaded_file.name
            )

            # Extração dos parâmetros
            extracted_data = extract_all_parameters(
                uploaded_file.name
            )

            # Atualiza o estado
            st.session_state.extracted_data = extracted_data
            st.session_state.document_loaded = True
            st.session_state.document_name = uploaded_file.name
            st.session_state.document_signature = document_signature

        st.success("Memorial processado com sucesso!")


# =========================
# PARAMETERS
# =========================

if st.session_state.extracted_data:

    with st.expander("📌 Parâmetros Extraídos"):

        st.json(
            st.session_state.extracted_data
        )


# =========================
# CHAT HISTORY
# =========================

render_chat(
    st.session_state.messages
)


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
            response = ask_question(
                user_question,
                st.session_state.document_name
            )


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()