# ============================================================
# BARRA LATERAL
# ============================================================
# Disponibiliza o componente de upload dos memoriais descritivos.
import streamlit as st

# Cria a barra lateral e retorna o arquivo selecionado pelo usuário.
def render_sidebar():

    with st.sidebar:

        st.title("📄 Memorial Inteligente")

        st.markdown("---")

        uploaded_file = st.file_uploader(
            "Upload Memorial",
            type=["pdf", "docx"]
        )

        st.markdown("---")

        return uploaded_file