from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str
    message: str
    language: str
    provider: str
    model: str


class ResetRequest(BaseModel):
    session_id: str


class MovieCard(BaseModel):
    title: str
    url: str
    image_url: str
    plot: str = ""
    ratings: list[dict[str, Any]] = Field(default_factory=list)


class ProviderInfo(BaseModel):
    id: str
    available: bool
    models: list[str]


class BootstrapResponse(BaseModel):
    db_exists: bool
    default_language: str
    languages: dict[str, str]
    providers: list[ProviderInfo]
    translations: dict[str, dict[str, Any]]
    provider_help: dict[str, dict[str, str]]
    no_db_text: str


class DailyMessageResponse(BaseModel):
    message: str | None


class IngestResponse(BaseModel):
    ok: bool
    db_exists: bool


class HealthResponse(BaseModel):
    status: Literal["ok"]


class TokenEvent(BaseModel):
    type: Literal["token"] = "token"
    text: str


class StatusEvent(BaseModel):
    type: Literal["status"] = "status"
    message: str


class MovieCardEvent(BaseModel):
    type: Literal["movie_card"] = "movie_card"
    movie: MovieCard


class GraphEvent(BaseModel):
    type: Literal["graph"] = "graph"
    data: list[float]


class ErrorEvent(BaseModel):
    type: Literal["error"] = "error"
    message: str


class DoneEvent(BaseModel):
    type: Literal["done"] = "done"


ChatEvent = TokenEvent | StatusEvent | MovieCardEvent | GraphEvent | ErrorEvent | DoneEvent
