# ============================================================
# ESTILOS DA INTERFACE
# ============================================================
# Define o CSS utilizado para personalizar a interface do Streamlit.

import streamlit as st

# Injeta os estilos CSS personalizados na aplicação.
def load_css():

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #0f1117;
            color: white;
        }

        section[data-testid="stSidebar"] {
            background-color: #161a23;
        }

        .main-title {
            font-size: 42px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .subtitle {
            font-size: 18px;
            color: #b0b3b8;
            margin-bottom: 30px;
        }

        .chat-box {
            background-color: #1e2430;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 15px;
        }

        .user-message {
            background-color: #2563eb;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 10px;
        }

        .assistant-message {
            background-color: #1f2937;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )