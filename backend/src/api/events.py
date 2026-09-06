from __future__ import annotations

import json
from typing import Any

from api.schemas import (
    ChatEvent,
    DoneEvent,
    ErrorEvent,
    GraphEvent,
    MovieCard,
    MovieCardEvent,
    StatusEvent,
    TokenEvent,
)
from catalog.translations import TRANSLATIONS


def texts_for(language: str) -> dict[str, Any]:
    return TRANSLATIONS.get(language, TRANSLATIONS["EN"])


def chunk_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
            elif hasattr(block, "text"):
                parts.append(str(block.text))
        return "".join(parts)
    return str(content)


def parse_jsonish(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    if hasattr(value, "content"):
        return parse_jsonish(value.content)
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def movie_from_tool_output(output: Any) -> MovieCard | None:
    parsed = parse_jsonish(output)
    payload: Any = parsed
    if isinstance(parsed, (list, tuple)) and len(parsed) >= 2:
        payload = parsed[1]
    if isinstance(payload, dict) and "movies" in payload:
        payload = payload["movies"]
    if not isinstance(payload, dict):
        return None
    title = payload.get("title")
    url = payload.get("url")
    image_url = payload.get("image_url")
    if not title or not url or not image_url:
        return None
    ratings = payload.get("ratings") or []
    if not isinstance(ratings, list):
        ratings = []
    return MovieCard(
        title=str(title),
        url=str(url),
        image_url=str(image_url),
        plot=str(payload.get("plot") or ""),
        ratings=ratings,
    )


def graph_from_tool_output(output: Any) -> list[float] | None:
    parsed = parse_jsonish(output)
    if isinstance(parsed, dict) and parsed.get("obj_type") == "graph":
        data = parsed.get("data") or []
        try:
            return [float(v) for v in data]
        except (TypeError, ValueError):
            return None
    return None


def status_for_tool(name: str, tool_args: dict[str, Any], language: str) -> str | None:
    texts = texts_for(language)
    if name == "get_reviews":
        filter_str = _title_info(tool_args, texts)
        filter_str += _review_id_info(tool_args, texts)
        initial = texts["reviews_filter_loading"] if filter_str else texts["reviews_loading"]
        return initial + filter_str
    if name == "get_movies":
        filter_str = _title_info(tool_args, texts)
        filter_str += _watched_date_info(tool_args, texts)
        filter_str += _rating_info(tool_args, texts)
        filter_str += _release_year_info(tool_args, texts)
        filter_str += _rewatch_info(tool_args, texts)
        initial = texts["film_filter_loading"] if filter_str else texts["film_loading"]
        return initial + filter_str
    return None


def events_from_langgraph(event: dict[str, Any], language: str) -> list[ChatEvent]:
    kind = event.get("event")
    name = event.get("name") or ""
    data = event.get("data") or {}
    emitted: list[ChatEvent] = []

    if kind == "on_tool_start":
        tool_args = data.get("input") or {}
        if not isinstance(tool_args, dict):
            tool_args = {}
        status = status_for_tool(name, tool_args, language)
        if status:
            emitted.append(StatusEvent(message=status))

    elif kind == "on_tool_end":
        output = data.get("output")
        if name in ("get_movie_details", "get_movie_details_extended"):
            movie = movie_from_tool_output(output)
            if movie:
                emitted.append(MovieCardEvent(movie=movie))
        elif name == "get_graph":
            graph_data = graph_from_tool_output(output)
            if graph_data is not None:
                emitted.append(GraphEvent(data=graph_data))

    elif kind == "on_chat_model_stream":
        chunk = data.get("chunk")
        content = getattr(chunk, "content", None) if chunk is not None else None
        text = chunk_text(content)
        if text:
            emitted.append(TokenEvent(text=text))

    return emitted


def done_event() -> DoneEvent:
    return DoneEvent()


def error_event(message: str) -> ErrorEvent:
    return ErrorEvent(message=message)


def _title_info(tool_args: dict[str, Any], texts: dict[str, Any]) -> str:
    name = tool_args.get("name")
    return texts["title_filter"].format(name=name) if name else ""


def _review_id_info(tool_args: dict[str, Any], texts: dict[str, Any]) -> str:
    review_id = tool_args.get("review_id")
    return texts["title_filter"].format(name=review_id) if review_id else ""


def _watched_date_info(tool_args: dict[str, Any], texts: dict[str, Any]) -> str:
    from_date = tool_args.get("from_watched_date")
    to_date = tool_args.get("to_watched_date")
    if not from_date and not to_date:
        return ""
    to_date = to_date or "hoy"
    if from_date:
        return texts["date_range_filter"].format(from_date=from_date, to_date=to_date)
    return texts["date_to_filter"].format(to_date=to_date)


def _rating_info(tool_args: dict[str, Any], texts: dict[str, Any]) -> str:
    from_rating = tool_args.get("from_rating")
    to_rating = tool_args.get("to_rating")
    if from_rating is None and to_rating is None:
        return ""
    from_rating = from_rating if from_rating is not None else 0
    to_rating = to_rating if to_rating is not None else 5
    if from_rating != to_rating:
        return texts["rating_range_filter"].format(
            from_rating=from_rating, to_rating=to_rating
        )
    return texts["rating_filter"].format(from_rating=from_rating)


def _release_year_info(tool_args: dict[str, Any], texts: dict[str, Any]) -> str:
    year = tool_args.get("year")
    return texts["year_filter"].format(year=year) if year else ""


def _rewatch_info(tool_args: dict[str, Any], texts: dict[str, Any]) -> str:
    return texts["rewatch"] if tool_args.get("rewatch") else ""
