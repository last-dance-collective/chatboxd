from typing import Literal
import streamlit as st

from utils.session_utils import get_session_val, set_session_val, save_session_message
from utils.agent_utils import extract_image_data, get_df
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
            col1, col2 = st.columns(2)
            text_placeholder = st.empty()
            with col1:
                text_placeholder_col1 = st.empty()
            with col2:
                card_placeholder = st.empty()
            async for event in agent_call:
                kind = event["event"]

                if kind == "on_tool_start":
                    display_tool_call_info(event)

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
                        text_placeholder.write(stream)
                        save_session_message("assistant", stream)

                if (
                    kind == "on_tool_end"
                    and event["name"] == "get_letterboxd_film_details"
                ):
                    movie_detail = extract_image_data(event)
                    card = return_img_preview(
                        movie_detail.get("image_url", ""),
                        movie_detail.get("title", ""),
                        movie_detail.get("url", ""),
                        movie_detail.get("plot", ""),
                    )
                    card_placeholder.markdown(card, unsafe_allow_html=True)

            # text_placeholder.markdown(stream)
            save_session_message("assistant", stream)


def display_tool_call_info(event):
    tool_name = event["name"]
    tool_args = event["data"]["input"]

    if tool_name == "get_movies":
        name = tool_args.get("name")
        from_watched_date = tool_args.get("from_watched_date")
        to_watched_date = tool_args.get("to_watched_date", "hoy")
        from_rating = tool_args.get("from_rating", 0)
        to_rating = tool_args.get("to_rating", 5)
        rewatch = tool_args.get("rewatch")
        year = tool_args.get("year")

        description_str = "Buscando películas con los siguientes filtros:\n"
        if name:
            description_str += f"* Título: {name.title()}\n"
        if from_watched_date or to_watched_date:
            description_str += (
                f"* Vistas desde {from_watched_date} hasta {to_watched_date}\n"
            )
        if from_rating or to_rating:
            description_str += (
                f"* Rango de puntuaciones: De {from_rating} a {to_rating} estrellas\n"
            )
        if year:
            description_str += f"* Año de lanzamiento: {year}\n"
        if rewatch:
            description_str += f"* Rewatch: {rewatch}\n"

        st.info(description_str, icon="🔎")
