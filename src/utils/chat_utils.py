from typing import Literal
import streamlit as st

from utils.session_utils import get_session_val, set_session_val, save_session_message
from utils.agent_utils import extract_image_data
from utils.frame_utils import return_img_preview
from utils.agent_utils import display_graph

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
        with st.spinner(get_session_val("texts")["chat_loading"]):
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

                if kind == "on_tool_end" and (
                    event["name"] == "get_movie_details"
                    or event["name"] == "get_movie_details_extended"
                ):
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
        display_graph(event)


def display_tool_call_info(event, info_container):
    kind = event["event"]
    tool_name = event["name"]
    tool_args = event["data"].get("input", {})

    if tool_name == "get_movies" and kind == "on_tool_start":
        get_movies_tool_info(tool_args, info_container)
    elif tool_name == "get_reviews" and kind == "on_tool_start":
        get_reviews_tool_info(tool_args, info_container)


def get_reviews_tool_info(tool_args, info_container):
    filter_str = title_info(tool_args)
    filter_str += review_id_info(tool_args)
    texts = get_session_val("texts")

    initial_str = (
        texts["reviews_filter_loading"] if filter_str else texts["reviews_loading"]
    )

    info_container.info(initial_str + filter_str, icon="🔎")


def get_movies_tool_info(tool_args, info_container):
    filter_str = title_info(tool_args)
    filter_str += watched_date_info(tool_args)
    filter_str += rating_info(tool_args)
    filter_str += release_year_info(tool_args)
    filter_str += rewatch_info(tool_args)
    texts = get_session_val("texts")

    initial_str = texts["film_filter_loading"] if filter_str else texts["film_loading"]

    info_container.info(initial_str + filter_str, icon="🔎")


def review_id_info(tool_args):
    review_id = tool_args.get("review_id")
    texts = get_session_val("texts")
    info_str = texts["title_filter"].format(name=review_id) if review_id else ""
    return info_str


def title_info(tool_args):
    name = tool_args.get("name")
    texts = get_session_val("texts")
    info_str = texts["title_filter"].format(name=name) if name else ""
    return info_str


def watched_date_info(tool_args):
    from_date = tool_args.get("from_watched_date")
    to_date = tool_args.get("to_watched_date")
    texts = get_session_val("texts")
    info_str = ""

    if from_date or to_date:
        to_date = to_date or "hoy"
        info_str += (
            texts["date_range_filter"].format(from_date=from_date, to_date=to_date)
            if from_date
            else texts["date_to_filter"].format(to_date=to_date)
        )

    return info_str


def rating_info(tool_args):
    from_rating = tool_args.get("from_rating")
    to_rating = tool_args.get("to_rating")
    texts = get_session_val("texts")
    info_str = ""

    if from_rating or to_rating:
        from_rating = from_rating or 0
        to_rating = to_rating or 5
        info_str = (
            texts["rating_range_filter"].format(
                from_rating=from_rating, to_rating=to_rating
            )
            if from_rating != to_rating
            else texts["rating_filter"].format(from_rating=from_rating)
        )

    return info_str


def release_year_info(tool_args):
    year = tool_args.get("year")
    texts = get_session_val("texts")
    info_str = texts["year_filter"].format(year=year) if year else ""
    return info_str


def rewatch_info(tool_args):
    rewatch = tool_args.get("rewatch")
    texts = get_session_val("texts")
    info_str = texts["rewatch"] if rewatch else ""
    return info_str
