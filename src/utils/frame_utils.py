import streamlit as st
import pandas as pd

from utils.session_utils import reset_session, get_session_val
from services.sqlite_service import Database, Operator
from services.daily_message_service import get_daily_message
from catalog.styles import card_css


def display_interface():
    st.logo("public/chatboxd.png", size="large")
    display_header()
    display_daily_message()
    reset_conversation()
    display_chat_input()
    # display_table()


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
    n_cols = 5
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
    details = compose_extra_details(plot, ratings)

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
                </h3>{details}
            </div>
        </div>
    """
    return card_css + tarjeta_html


def compose_extra_details(plot, ratings):
    details_html = ""
    if (ratings is not None) and (len(ratings) > 0):
        details_html = f"""
            <div class="ratings">
                {get_ratings_badges(ratings)}
            </div>
        """.strip()

    if plot != "":
        details_html = (
            details_html
            + f"""
            <p>
                {plot}
            </p>
        """.strip()
        )

    return details_html


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
        return f"<span class='badge badge-primary'>IMDB: {ratings[0]['Value']}</span>"
    elif len(ratings) == 2:
        return f"<span class='badge badge-primary'>IMDB: {ratings[0]['Value']}</span><span class='badge badge-secondary'>RT: {ratings[1]['Value']}</span>"
    else:
        return f"<span class='badge badge-primary'>IMDB: {ratings[0]['Value']}</span><span class='badge badge-secondary'>RT: {ratings[1]['Value']}</span><span class='badge badge-terciary'>MC: {ratings[2]['Value']}</span>"
