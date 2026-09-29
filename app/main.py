# ============================================================
# APLICAÇÃO PRINCIPAL
# ============================================================
# Este módulo é o ponto de entrada da interface Streamlit
# do Memorial Inteligente.
#
# Ele coordena:
# - configuração da interface;
# - carregamento dos estilos;
# - gerenciamento do estado da sessão;
# - upload dos memoriais;
# - ingestão dos documentos;
# - extração dos parâmetros;
# - apresentação dos resultados;
# - interação com o chatbot.

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


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
# Define as principais configurações da interface Streamlit,
# incluindo título, ícone e disposição dos elementos na página.

st.set_page_config(
    page_title="Memorial Inteligente",
    page_icon="📄",
    layout="wide"
)



# ============================================================
# CARREGAMENTO DOS ESTILOS
# ============================================================
# Carrega os estilos visuais utilizados pela aplicação.

load_css()


# ============================================================
# ESTADO DA SESSÃO
# ============================================================
# O Streamlit executa novamente o script a cada interação.
# O session_state é utilizado para preservar informações
# importantes entre essas execuções.
#
# São armazenados:
# - histórico das mensagens do chatbot;
# - indicação de documento carregado;
# - parâmetros extraídos;
# - nome do documento atualmente processado.


if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_loaded" not in st.session_state:
    st.session_state.document_loaded = False

if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None


# ============================================================
# SIDEBAR
# ============================================================
# Renderiza a barra lateral da aplicação e disponibiliza
# o componente utilizado para seleção do memorial.

uploaded_file = render_sidebar()


# ============================================================
# CABEÇALHO PRINCIPAL
# ============================================================
# Apresenta o título e o subtítulo da aplicação na interface.

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


# ============================================================
# PROCESSAMENTO DO DOCUMENTO
# ============================================================
# Verifica se existe um arquivo selecionado pelo usuário.
#
# Quando nenhum documento está selecionado, os dados
# associados ao documento anterior são limpos.

if uploaded_file is None:

    st.session_state.document_loaded = False
    st.session_state.extracted_data = None
    st.session_state.document_name = None
    st.session_state.document_signature = None


else:

    # ========================================================
    # IDENTIFICAÇÃO DO DOCUMENTO
    # ========================================================
    # Cria uma assinatura do arquivo utilizando seu nome e
    # tamanho.
    #
    # Essa informação é utilizada para identificar se o arquivo
    # selecionado é diferente daquele processado anteriormente.

    document_signature = (
        uploaded_file.name,
        uploaded_file.size
    )

    # Verifica se o documento selecionado é diferente do
    # documento registrado anteriormente na sessão.

    new_document = (
        document_signature
        != st.session_state.document_signature
    )

    # ========================================================
    # PROCESSAMENTO DE UM NOVO DOCUMENTO
    # ========================================================
    # Quando um novo memorial é identificado, os dados do
    # documento anterior são limpos antes do processamento.

    if new_document:

        # Limpa o histórico de mensagens e os resultados
        # associados ao documento anterior.
        st.session_state.messages = []
        st.session_state.extracted_data = None
        st.session_state.document_loaded = False

        file_path = os.path.join(
            UPLOAD_FOLDER,
            uploaded_file.name
        )

        # Salva o arquivo enviado pelo usuário no diretório
        # configurado para os uploads.

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # ====================================================
        # PROCESSAMENTO DO MEMORIAL
        # ====================================================
        # Executa as etapas de ingestão e extração enquanto
        # apresenta uma mensagem de processamento na interface.

        with st.spinner("Processando memorial..."):

            # ------------------------------------------------
            # INGESTÃO DO DOCUMENTO
            # ------------------------------------------------
            # Extrai o conteúdo, gera os chunks, cria os
            # embeddings e armazena as informações no banco
            # vetorial.

            ingest_document(
                file_path,
                uploaded_file.name
            )

            # ------------------------------------------------
            # EXTRAÇÃO DOS PARÂMETROS
            # ------------------------------------------------
            # Após a ingestão, executa a extração dos parâmetros
            # definidos para a versão atual da aplicação.

            extracted_data = extract_all_parameters(
                uploaded_file.name
            )

            # ------------------------------------------------
            # ATUALIZAÇÃO DO ESTADO
            # ------------------------------------------------
            # Armazena os resultados e informações do documento
            # na sessão do Streamlit.

            st.session_state.extracted_data = extracted_data
            st.session_state.document_loaded = True
            st.session_state.document_name = uploaded_file.name
            st.session_state.document_signature = document_signature

        st.success("Memorial processado com sucesso!")


# ============================================================
# PARÂMETROS EXTRAÍDOS
# ============================================================
# Quando existem resultados de extração, eles são apresentados
# em um componente expansível da interface.

if st.session_state.extracted_data:

    with st.expander("📌 Parâmetros Extraídos"):

        st.json(
            st.session_state.extracted_data
        )


# ============================================================
# HISTÓRICO DO CHAT
# ============================================================
# Renderiza as mensagens anteriores da conversa armazenadas
# no estado da sessão.

render_chat(
    st.session_state.messages
)


# ============================================================
# ENTRADA DO CHAT
# ============================================================
# Disponibiliza o campo para que o usuário faça perguntas
# sobre o memorial carregado.

user_question = st.chat_input(
    "Faça uma pergunta sobre o memorial..."
)

# ============================================================
# PROCESSAMENTO DA PERGUNTA
# ============================================================
# Executa o fluxo de perguntas somente quando o usuário
# envia uma mensagem.

if user_question:

    # Impede perguntas antes que um memorial tenha sido
    # carregado e processado.

    if not st.session_state.document_loaded:

        st.warning(
            "Envie um memorial antes de realizar perguntas."
        )

    else:

        # ----------------------------------------------------
        # REGISTRO DA PERGUNTA
        # ----------------------------------------------------
        # Adiciona a pergunta do usuário ao histórico da sessão.

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        # ----------------------------------------------------
        # GERAÇÃO DA RESPOSTA
        # ----------------------------------------------------
        # Encaminha a pergunta e o documento atualmente
        # carregado para o chatbot.
        #
        # O chatbot realiza a recuperação dos trechos
        # relevantes e solicita ao modelo de linguagem
        # a geração da resposta.

        with st.spinner("Pensando..."):
            response = ask_question(
                user_question,
                st.session_state.document_name
            )

        # ----------------------------------------------------
        # REGISTRO DA RESPOSTA
        # ----------------------------------------------------
        # Armazena a resposta do assistente no histórico
        # da conversa.

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        # Atualiza a interface para apresentar a nova
        # mensagem no histórico do chat.

        st.rerun()