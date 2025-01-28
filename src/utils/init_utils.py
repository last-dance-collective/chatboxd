import streamlit as st

from utils.session_utils import initialize_session, get_session_val, set_session_val
from utils.frame_utils import display_interface
from services.langgraph_service import ChatboxdAgent
from services.llm_service import ollama_model, openai_model
from config import OLLAMA_MODEL, OPENAI_MODEL


def initialize_app():
    initialize_session()
    setup_page()
    display_interface()
    if not get_session_val("start_page"):
        try:
            setup_agent()
        except Exception:
            st.error(
                get_session_val("texts")["keys_not_set"],
            )
            st.stop()


def setup_page():
    if get_session_val("start_page"):
        layout = "centered"
    else:
        layout = "wide"
    st.set_page_config(
        page_title="Chatboxd",
        page_icon="public/favicon.png",
        layout=layout,
        initial_sidebar_state="expanded",
    )


def setup_agent():
    if not get_session_val("agent"):
        provider = get_session_val("provider")
        if provider.lower() == "ollama":
            llm = ollama_model(OLLAMA_MODEL)
        elif provider.lower() == "openai":
            llm = openai_model(OPENAI_MODEL)
        else:
            raise Exception("Invalid provider")

        set_session_val("agent", ChatboxdAgent(llm=llm))
