from typing import Literal
import streamlit as st

from utils.session_utils import get_session_val, save_session_message


def process_user_input():
    user_input = get_session_val("chat_input")
    if user_input:
        save_session_message("user", user_input)
    display_history_messages()
    return get_session_val("chat_input")


def display_history_messages():
    for message in get_session_val("messages"):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def display_chat_msg(msg: str, author: Literal["user", "assistant", "ai", "human"]):
    st.chat_message(author).write(msg)
    save_session_message(author, msg)
