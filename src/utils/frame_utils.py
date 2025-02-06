import itertools
import random
import streamlit as st
import pandas as pd

from utils.session_utils import reset_session, get_session_val, set_session_val
from catalog.translations import LANGUAGE_NAMES, MODEL_PROVIDERS
from services.sqlite_service import Database, Operator
from services.daily_message_service import get_daily_message
from catalog.styles import card_css
from config import MODELS


def display_interface():
    display_header()

    if get_session_val("start_page"):
        display_start_page()
    else:
        st.logo("public/chatboxd.png", size="large")
        display_daily_message()
        display_suggest_labels()
        reset_conversation()
        display_chat_input()


def display_start_page():
    st.markdown(get_session_val("texts")["start_page_markdown"])

    st.caption(get_session_val("texts")["select_language"])
    selected_language = st.selectbox(
        label="Selecciona tu idioma",
        label_visibility="collapsed",
        options=get_session_val("available_languages"),
        format_func=lambda x: LANGUAGE_NAMES.get(x),
    )

    if selected_language != get_session_val("language"):
        set_session_val("language", selected_language)
        st.rerun()

    display_provider_selection()

    if st.button(
        get_session_val("texts")["continue"], disabled=not get_session_val("provider")
    ):
        set_session_val("start_page", False)
        st.rerun()


def display_provider_selection():
    st.caption(get_session_val("texts")["select_provider"])

    providers = MODELS.keys()  # MODELS = {provider: model_list}
    all_models = list(itertools.chain(*MODELS.values()))

    cols = st.columns(len(all_models), gap="medium")
    col_i = 0
    for provider in providers:
        for model in MODELS[provider]:
            is_current_model = get_session_val("model") == model
            with cols[col_i]:
                emoji = "🔘" if not is_current_model else "🟢"
                st.image(
                    "public/" + provider.lower() + ".png",
                    use_container_width=True,
                )
                if st.button(
                    model,
                    icon=emoji,
                    key=f"{provider}_{model}",
                    use_container_width=True,
                ):
                    set_session_val("provider", provider)
                    set_session_val("model", model)
                    st.rerun()
            col_i += 1

    st.markdown(
        MODEL_PROVIDERS.get(get_session_val("language"), MODEL_PROVIDERS["ES"])[
            get_session_val("provider")
        ]
    )


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
    cols = (
        st.columns([1, 5, 1])
        if get_session_val("start_page")
        else st.columns([1, 1, 1])
    )
    # texts = get_session_val("texts")
    with cols[n_cols // 2]:
        st.image("public/banner.png", use_container_width=True)
    # st.caption(texts["header_caption"])


def display_daily_message():
    daily_message = get_daily_message()
    if daily_message:
        st.info(daily_message, icon="📅")


def return_img_preview(
    og_image: str, og_title: str, og_url: str, plot: str, ratings: list
) -> str:
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


def compose_extra_details(plot: str, ratings: list):
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


def get_ratings_badges(ratings: list) -> str:
    if len(ratings) == 0:
        return ""
    elif len(ratings) == 1:
        return f"<span class='badge badge-primary'>IMDB: {ratings[0]['Value']}</span>"
    elif len(ratings) == 2:
        return f"<span class='badge badge-primary'>IMDB: {ratings[0]['Value']}</span><span class='badge badge-secondary'>RT: {ratings[1]['Value']}</span>"
    else:
        return f"<span class='badge badge-primary'>IMDB: {ratings[0]['Value']}</span><span class='badge badge-secondary'>RT: {ratings[1]['Value']}</span><span class='badge badge-terciary'>MC: {ratings[2]['Value']}</span>"


def display_suggest_labels():
    texts = get_session_val("texts")
    three_random_suggestions = random.sample(texts["suggestions_list"], 3)
    cols = st.columns([1, 8, 1])
    if not get_session_val("suggestions") and not get_session_val("chat_input"):
        with cols[3 // 2]:
            st.pills(
                texts["suggestions_label"],
                three_random_suggestions,
                key="suggestions",
                selection_mode="single",
            )
