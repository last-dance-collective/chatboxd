import streamlit as st

from utils.session_utils import initialize_session, get_session_val, set_session_val
from utils.frame_utils import display_interface
from services.langgraph_service import ChatboxdAgent
from services.llm_service import ollama_model


def initialize_app():
    initialize_session()
    setup_page()
    display_interface()
    setup_agent()


def setup_page():
    st.set_page_config(
        page_title="Chatboxd",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def setup_agent():
    if not get_session_val("agent"):
        llm = ollama_model(model="llama3.2:3b")
        set_session_val("agent", ChatboxdAgent(llm=llm))
