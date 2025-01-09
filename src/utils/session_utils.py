import uuid
import streamlit as st
from catalog.translations import TRANSLATIONS
from config import LANGUAGE


def initialize_session():
    def initialize_key(key: str, default_value=None):
        if key not in st.session_state:
            st.session_state[key] = default_value

    initialize_key("language")
    initialize_key("session_id", uuid.uuid4())
    initialize_key("texts", TRANSLATIONS[LANGUAGE])
    initialize_key("messages", [])


def reset_session():
    st.session_state.clear()


def set_session_val(key: str, value=None, cache_obj=st.session_state):
    cache_obj[key] = value


def get_session_val(key: str, default=None, cache_obj=st.session_state):
    return cache_obj.get(key, default)


def save_session_message(author, content):
    st.session_state.messages.append({"role": author, "content": content})
