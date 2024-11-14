import uuid
import streamlit as st


def initialize_session():
    def initialize_key(key: str, default_value=None):
        if key not in st.session_state:
            st.session_state[key] = default_value

    initialize_key("session_id", uuid.uuid4())


def reset_session():
    st.session_state.clear()


def set_session_val(key: str, value=None, cache_obj=st.session_state):
    cache_obj[key] = value


def get_session_val(key: str, default=None, cache_obj=st.session_state):
    return cache_obj.get(key, default)
