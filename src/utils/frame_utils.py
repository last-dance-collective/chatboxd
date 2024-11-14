import streamlit as st
import pandas as pd

from utils.session_utils import reset_session
from services.sqlite_service import Database, Operator


def display_interface():
    st.logo("public/logo.jpg", size="large")
    display_header()
    reset_conversation()
    display_chat_input()
    display_table()


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


def display_table():
    db = Database("letterboxd.db")
    last_month_entries = db.filter_diary_entries([{"column": "watched_date", "operator": Operator.EQUAL, "value": "2019-03-15"}])
    df = pd.DataFrame(last_month_entries)
    st.dataframe(df, use_container_width=True)
