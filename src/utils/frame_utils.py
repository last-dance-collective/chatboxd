import random
import streamlit as st
import pandas as pd

from utils.session_utils import (
    reset_session,
    get_session_val,
    set_session_val,
    open_settings,
)
from enviroment_config import (
    get_local_ollama_models,
    provider_available,
    configure_openai_api_key,
)
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
        configure_app()
        display_chat_input()


def display_start_page():
    if not get_session_val("settings"):
        st.markdown(get_session_val("texts")["start_page_markdown"])
    else:
        st.markdown("# " + get_session_val("texts")["configure_app"])

    st.caption(get_session_val("texts")["select_language"])

    available_languages = get_session_val("available_languages")
    current_lang = get_session_val("language")
    lang_index = list(available_languages).index(current_lang) if current_lang else 0

    selected_language = st.selectbox(
        label="Selecciona tu idioma",
        label_visibility="collapsed",
        options=available_languages,
        format_func=lambda x: LANGUAGE_NAMES.get(x),
        index=lang_index,
    )

    if selected_language != current_lang:
        set_session_val("language", selected_language)
        st.rerun()

    display_provider_selection()

    if st.button(
        get_session_val("texts")["continue"], disabled=not get_session_val("provider")
    ):
        set_session_val("start_page", False)
        st.rerun()


def display_provider_selection():
    st.caption(get_session_val("texts")["select_model"])

    # The provider-model list must be set in the config file.
    # It follows the format: MODELS = {provider: model_list}

    providers = MODELS.keys()

    configure_openai_api_key()

    available_providers = [
        provider for provider in providers if provider_available(provider)
    ]

    if "Ollama" in available_providers:
        MODELS["Ollama"] = get_local_ollama_models()

    available_models = sorted(
        [model for provider in available_providers for model in MODELS[provider]]
    )

    if len(available_models) > 5:
        display_model_dropdown(available_providers)
    elif available_models:
        display_model_buttons(available_models, available_providers)

    for provider in providers:
        expander_text = (
            get_session_val("texts")["available_provider"]
            if provider in available_providers
            else get_session_val("texts")["not_available_provider"]
        )

        with st.expander(expander_text.format(provider=provider)):
            st.markdown(
                MODEL_PROVIDERS.get(get_session_val("language"), MODEL_PROVIDERS["ES"])[
                    provider
                ]
            )


def display_model_buttons(available_models, available_providers):
    if len(available_models) == 1:
        col_i = 2
    elif len(available_models) < 4:
        col_i = 1
    else:
        col_i = 0

    cols = st.columns(2 * col_i + len(available_models), gap="medium")

    for provider in available_providers:
        models = MODELS[provider]
        for model in models:
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


def display_model_dropdown(available_providers):
    model_providers = {
        model: provider
        for provider in available_providers
        for model in sorted(MODELS[provider])
    }

    model = st.selectbox(
        label=get_session_val("texts")["select_model"],
        label_visibility="collapsed",
        placeholder=get_session_val("texts")["select_model"],
        options=model_providers.keys(),
        format_func=lambda x: f"{model_providers.get(x)} - {x}",
    )

    if model != get_session_val("model"):
        set_session_val("model", model)
        set_session_val("provider", model_providers.get(model))
        st.rerun()


def reset_conversation():
    texts = get_session_val("texts")
    with st.sidebar:
        st.button(
            texts["reset_chat"],
            icon="🔄",
            on_click=reset_session,
            use_container_width=True,
        )


def configure_app():
    text = get_session_val("texts")
    with st.sidebar:
        st.button(
            text["configure_app"],
            icon="⚙️",
            on_click=open_settings,
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
