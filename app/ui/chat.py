# ============================================================
# INTERFACE DE CHAT
# ============================================================
# Renderiza no Streamlit o histórico de mensagens do usuário e do assistente.
import streamlit as st

# Exibe as mensagens armazenadas na sessão da aplicação.

def render_chat(messages):

    for message in messages:

        if message["role"] == "user":

            st.markdown(
                f"""
                <div class="user-message">
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="assistant-message">
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )