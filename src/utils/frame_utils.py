import streamlit as st
import pandas as pd

from utils.session_utils import reset_session
from services.sqlite_service import Database, Operator


def display_interface():
    st.logo("public/chatboxd.png", size="large")
    display_header()
    reset_conversation()
    display_chat_input()
    #display_table()


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
    n_cols = 5
    cols = st.columns(n_cols)
    with cols[n_cols // 2]:
        st.image("public/chatboxd.png", width=220)
    st.caption("Chatboxd allows you to chat with your LetterBoxd stats!")


def return_img_preview(og_image: str, og_title: str, og_url: str):
    tarjeta_html = f"""
        <div style="
            display: flex;
            align-items: flex-start;
            border: 1px solid #CCDBE9;
            border-radius: 4px;
            overflow: hidden;
            max-width: 700px;
            margin: 10px 0;
            background-color: #445566;
        ">
            <div style="flex-shrink: 0; width: 40%;">
                <img src="{og_image}" alt="{og_title}" style="width: 100%; height: auto; display: block;">
            </div>
            <div style="
                padding: 10px;
                flex-grow: 1;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <h3 style="
                    margin: 0;
                    font-size: 1.1em;
                    color: #CCDBE9;
                    line-height: 1.4;
                ">
                    <a href="{og_url}" target="_blank" style="text-decoration: none; color: inherit;">
                        {og_title}
                    </a>
                </h3>
            </div>
        </div>
    """
    return tarjeta_html


def display_table():
    db = Database("letterboxd.db")
    last_month_entries = db.filter_diary_entries(
        [
            {
                "column": "watched_date",
                "operator": Operator.EQUAL,
                "value": "2021-07-04",
            }
        ]
    )
    df = pd.DataFrame(last_month_entries)
    st.dataframe(df, use_container_width=True)
