import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.title("📄 Memorial AI")

        st.markdown("---")

        uploaded_file = st.file_uploader(
            "Upload Memorial",
            type=["pdf", "docx"]
        )

        st.markdown("---")

        st.markdown("### 📌 Informações")

        st.markdown("""
        - IA Documental
        - RAG
        - Embeddings
        - Busca Semântica
        """)

        return uploaded_file