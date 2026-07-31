import streamlit as st


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