import uuid
import streamlit as st
from catalog.translations import TRANSLATIONS
from config import LANGUAGE


def initialize_session():
    def initialize_key(key: str, default_value=None):
        if key not in st.session_state:
            st.session_state[key] = default_value

    initialize_key("start_page", True)
    initialize_key("session_id", uuid.uuid4())
    initialize_key("messages", [])
    initialize_key("available_languages", TRANSLATIONS.keys())
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


def save_session_message(author, content):
    st.session_state.messages.append({"role": author, "content": content})
