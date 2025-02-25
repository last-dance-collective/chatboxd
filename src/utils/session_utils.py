import uuid
import os
import streamlit as st
from catalog.translations import TRANSLATIONS, NO_DB_TEXT
from config import LANGUAGE


def initialize_session():
    def initialize_key(key: str, default_value=None):
        if key not in st.session_state:
            st.session_state[key] = default_value

    initialize_key("is_db_created", check_database())
    initialize_key("start_page", True)
    initialize_key("session_id", uuid.uuid4())
    initialize_key("messages", [])
    initialize_key("available_languages", TRANSLATIONS.keys())
    initialize_key("start_page_markdown_no_db", NO_DB_TEXT)
    set_language()


def set_language():
    set_session_val("texts", TRANSLATIONS[get_session_val("language", LANGUAGE)])


def reset_session():
    keys = ["messages", "session_id"]
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]
    initialize_session()


def set_session_val(key: str, value=None, cache_obj=st.session_state):
    cache_obj[key] = value


def get_session_val(key: str, default=None, cache_obj=st.session_state):
    return cache_obj.get(key, default)


def save_session_message(author: str, content: str):
    st.session_state.messages.append({"role": author, "content": content})


def open_settings():
    set_session_val("start_page", True)
    set_session_val("settings", True)


def check_database():
    return os.path.isfile(os.path.join(os.getcwd(), "letterboxd.db"))
