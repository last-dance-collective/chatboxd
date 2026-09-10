from __future__ import annotations

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
from services.agent_tools import GraphArtifact, bundle_for


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


def events_from_langgraph(event: dict[str, Any], language: str) -> list[ChatEvent]:
    kind = event.get("event")
    name = event.get("name") or ""
    data = event.get("data") or {}
    emitted: list[ChatEvent] = []

    if kind == "on_tool_start":
        tool_args = data.get("input") or {}
        if not isinstance(tool_args, dict):
            tool_args = {}
        bundle = bundle_for(name)
        if bundle is None or bundle.status_from_args is None:
            return emitted
        status = bundle.status_from_args(tool_args, language)
        if status:
            emitted.append(StatusEvent(message=status))

    elif kind == "on_tool_end":
        bundle = bundle_for(name)
        if bundle is None or bundle.artifacts_from_result is None:
            return emitted
        artifact = bundle.artifacts_from_result(data.get("output"))
        if isinstance(artifact, MovieCard):
            emitted.append(MovieCardEvent(movie=artifact))
        elif isinstance(artifact, GraphArtifact):
            emitted.append(GraphEvent(data=artifact.data))

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
