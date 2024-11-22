from typing import Literal
import streamlit as st

from utils.session_utils import get_session_val, set_session_val, save_session_message
from utils.agent_utils import extract_image_data
from utils.frame_utils import return_img_preview

set_session_val("print_response", True)


def process_user_input():
    user_input = get_session_val("chat_input")
    if user_input:
        save_session_message("user", user_input)
    display_history_messages()
    return get_session_val("chat_input")


def display_history_messages():
    for message in get_session_val("messages"):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def display_chat_msg(msg: str, author: Literal["user", "assistant", "ai", "human"]):
    st.chat_message(author).write(msg)
    save_session_message(author, msg)


async def display_agent_response(agent_call):
    with st.chat_message("assistant"):
        with st.spinner("Generando respuesta..."):
            stream = ""
            is_card = False
            info_container = st.empty()
            text_placeholder = st.empty()
            col1, col2 = st.columns(2)
            with col1:
                text_placeholder_col1 = st.empty()
            with col2:
                card_placeholder = st.empty()

            async for event in agent_call:
                kind = event["event"]

                display_tool_call_info(event, info_container)

                if kind == "on_tool_end" and event["name"] == "get_movie_details":
                    is_card = True
                    movie_detail = extract_image_data(event)
                    card = return_img_preview(
                        movie_detail.get("image_url", ""),
                        movie_detail.get("title", ""),
                        movie_detail.get("url", ""),
                        movie_detail.get("plot", ""),
                        movie_detail.get("ratings", []),
                    )
                    card_placeholder.markdown(card, unsafe_allow_html=True)
                    
                elif kind == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        stream += content
                        if is_card:
                            text_placeholder_col1.write(stream + "| ")
                        else:
                            text_placeholder.write(stream + "| ")

                if kind == "on_chat_model_end":
                    if stream:
                        if is_card:
                            text_placeholder_col1.markdown(stream)
                        else:
                            text_placeholder.markdown(stream)
                        save_session_message("assistant", stream)


def display_tool_call_info(event, info_container):
    kind = event["event"]
    tool_name = event["name"]
    tool_args = event["data"].get("input", {})

    if tool_name == "get_movies" and kind == "on_tool_start":
        get_movies_tool_info(tool_args, info_container)


def get_movies_tool_info(tool_args, info_container):
    filter_str = title_info(tool_args)
    filter_str += watched_date_info(tool_args)
    filter_str += rating_info(tool_args)
    filter_str += release_year_info(tool_args)
    filter_str += rewatch_info(tool_args)

    initial_str = ("Buscando películas con los siguientes filtros:\n" 
                    if filter_str else "Buscando películas...\n")
    
    info_container.info(initial_str + filter_str, icon="🔎")


def title_info(tool_args):
    name = tool_args.get("name")
    info_str = f"* Título: {name.title()}\n" if name else ""
    return info_str


def watched_date_info(tool_args):
    from_date = tool_args.get("from_watched_date")
    to_date = tool_args.get("to_watched_date")
    info_str = ""

    if from_date or to_date: 
        to_date = to_date or "hoy"
        info_str += (
            f"* Vistas desde **{from_date}** hasta **{to_date}**\n"
            if from_date else 
            f"* Vistas antes de **{to_date}**\n"
        )

    return info_str


def rating_info(tool_args):
    from_rating = tool_args.get("from_rating")
    to_rating = tool_args.get("to_rating")
    info_str = ""

    if from_rating or to_rating:
        from_rating = from_rating or 0
        to_rating = to_rating or 5
        info_str = (
            f"* Puntuadas entre **{from_rating}** y **{to_rating} estrellas**\n"
            if from_rating != to_rating else 
            f"* Puntuadas con **{from_rating} estrellas**\n"
        )
     
    return info_str


def release_year_info(tool_args):
    year = tool_args.get("year")
    info_str = f"* Lanzadas en el año **{year}**\n" if year else ""
    return info_str


def rewatch_info(tool_args):
    rewatch = tool_args.get("rewatch")
    info_str = "* 🔁 Rewatch\n" if rewatch else ""
    return info_str

