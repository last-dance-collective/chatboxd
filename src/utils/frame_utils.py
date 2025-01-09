import streamlit as st
import pandas as pd

from utils.session_utils import reset_session, get_session_val, set_session_val
from services.sqlite_service import Database, Operator
from services.daily_message_service import get_daily_message


def display_interface():
    display_header()

    if get_session_val("language"):
        st.logo("public/chatboxd.png", size="large")
        display_daily_message()
        reset_conversation()
        display_chat_input()
    else:
        display_start_page()


def display_start_page():
    st.markdown("# Welcome to Chatboxd!\n\nLorem ipsum sit amet 🚬")


def reset_conversation():
    texts = get_session_val("texts")
    with st.sidebar:
        st.button(
            texts["reset_chat"],
            icon="🔄",
            on_click=reset_session,
            use_container_width=True,
        )


def display_chat_input():
    texts = get_session_val("texts")
    st.chat_input(
        placeholder=texts["chat_placeholder"],
        key="chat_input",
    )


def display_header():
    n_cols = 3
    cols = st.columns(n_cols)
    texts = get_session_val("texts")
    with cols[n_cols // 2]:
        st.image("public/chatboxd.png", width=220)
    st.caption(texts["header_caption"])


def display_daily_message():
    daily_message = get_daily_message()
    if daily_message:
        st.info(daily_message, icon="📅")


def return_img_preview(
    og_image: str, og_title: str, og_url: str, plot: str, ratings: list
):
    badges_html = get_ratings_badges(ratings)
    styles_css = """
        <head>
            <style>
                .card {
                    max-width: 80%;
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
                    height: 200px;
                    object-fit: cover;
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
                    font-size: 1.7em;
                    color: #ffffff;
                    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
                    font-weight: bold;
                    line-height: 1.1;
                }
                .card a {
                    text-decoration: none;
                    color: #fff;
                }
                .card-body p {
                    color: #ccdbe9;
                    font-style: italic;
                }
                .ratings {
                    width: 50%;
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 1rem;
                }
                .badge {
                    display: inline-block;
                    padding: 0.5em;
                    font-size: 90%;
                    font-weight: bold;
                    line-height: 1;
                    text-align: center;
                    white-space: nowrap;
                    vertical-align: baseline;
                    border-radius: 0.25rem;
                }
                .badge-primary {
                    color: #fff;
                    background-color: #d69e02;
                }
                .badge-secondary {
                    color: #fff;
                    background-color: #a31702;
                }
                .badge-terciary {
                    color: #fff;
                    background-color: #212121;
                }
                @media (min-width: 1440px) {
                    .card {
                        max-width: 800px;
                        margin: 20px auto;
                    }
                    .card-img {
                        height: 325px;
                    }
                }
            </style>
        </head>

    """
    tarjeta_html = f"""
        <div class="card">
                <a
                    href="{og_url}"
                    target="_blank"
                >
                    <img
                        class="card-img"
                        src="{og_image}"
                        alt="{og_title}"
                    />
                </a>
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
                <div class="ratings">
                    {badges_html}
                </div>
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


def get_ratings_badges(ratings: list):
    if len(ratings) == 0:
        return ""
    elif len(ratings) == 1:
        return f"<span class='badge badge-primary'>IMDB: {ratings[0]["Value"]}</span>"
    elif len(ratings) == 2:
        return f"<span class='badge badge-primary'>IMDB: {ratings[0]["Value"]}</span><span class='badge badge-secondary'>RT: {ratings[1]["Value"]}</span>"
    else:
        return f"<span class='badge badge-primary'>IMDB: {ratings[0]["Value"]}</span><span class='badge badge-secondary'>RT: {ratings[1]["Value"]}</span><span class='badge badge-terciary'>MC: {ratings[2]["Value"]}</span>"
