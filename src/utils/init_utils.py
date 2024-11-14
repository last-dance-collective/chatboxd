import streamlit as st

from utils.session_utils import initialize_session
from utils.frame_utils import display_interface


def initialize_app():
    initialize_session()
    setup_page()
    display_interface()


def setup_page():
    st.set_page_config(
        page_title="Chatboxd",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="expanded",
    )
