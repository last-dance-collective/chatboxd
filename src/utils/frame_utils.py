import streamlit as st

from utils.session_utils import reset_session


def display_interface():
    st.logo("public/logo.jpg", size="large")
    display_header()
    reset_conversation()
    display_chat_input()


def reset_conversation():
    with st.sidebar:
        st.button(
            "Reset Conversation",
            icon="🔄",
            on_click=reset_session,
            use_container_width=True,
        )


def display_chat_input():
    st.chat_input(
        placeholder="Type your message here...",
        key="chat_input",
    )


def display_header():
    st.header("Chatboxd")
    st.caption("Chatboxd allows you to chat with your LetterBoxd stats!")
