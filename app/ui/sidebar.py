import streamlit as st


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