import streamlit as st
import pandas as pd

from utils.session_utils import reset_session
from services.sqlite_service import Database, Operator


def display_interface():
    st.logo("public/chatboxd.png", size="large")
    display_header()
    reset_conversation()
    display_chat_input()
    # display_table()


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


def return_img_preview(og_image: str, og_title: str, og_url: str, plot: str):
    styles_css = """
        <head>
            <style>
                .card {
                    max-width: 700px;
                    margin-left: auto;
                    border: 1px solid #ccdbe9;
                    border-radius: 1rem;
                    overflow: hidden;
                    background-color: #445566;
                    padding: 1rem;
                    border-radius: 0.5rem;
                }
                .card:hover {
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.7);
                }
                .card-img {
                    width: 100%;
                    height: auto;
                    border-radius: 0.5rem;
                }
                .card-body {
                    padding: 10px;
                    flex-grow: 1;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    margin-top: 1rem;
                }
                .card-body h3 {
                    margin: 0;
                    font-size: 1.1em;
                    color: #ccdbe9;
                    line-height: 1.4;
                }
                .card-body a {
                    text-decoration: none;
                    color: inherit;
                }
            </style>
        </head>

    """
    tarjeta_html = f"""
        <div class="card">
            <a
            href="http://www.omdbapi.com/?apikey=afacdf8e&t=Avatar: The Way of Water"
            target="_blank"
        >
            <div style="flex-shrink: 0">
                <img
                    class="card-img"
                    src="{og_image}"
                    alt="{og_title}"
                />
            </div>
            <div class="card-body">
                <h3>
                    <a
                        href="{og_url}"
                        target="_blank"
                    >
                        {og_title}
                    </a>
                </h3>
                <p>
                {plot}
                </p>
            </div>
        </div>
    """
    return styles_css + tarjeta_html


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
