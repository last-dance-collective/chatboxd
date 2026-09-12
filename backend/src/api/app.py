from __future__ import annotations

import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from api.events import done_event, error_event, events_from_langgraph
from api.registry import registry
from api.schemas import (
    BootstrapResponse,
    ChatRequest,
    DailyMessageResponse,
    HealthResponse,
    IngestResponse,
    ProviderInfo,
    ResetRequest,
)
from catalog.translations import LANGUAGE_NAMES, MODEL_PROVIDERS, TRANSLATIONS
from config import LANGUAGE
from data_ingestion.export_archive import ExportError, materialize_export
from paths import DB_PATH, SECRETS_PATH, USER_DATA_DIR
from services.daily_message_service import get_daily_message
from services.letterboxd_store import LetterboxdStore
from services.llm_service import bootstrap_providers, configure_models_api_key
from utils.logger_utils import logger


@asynccontextmanager
async def lifespan(_app: FastAPI):
    load_dotenv(SECRETS_PATH)
    configure_models_api_key()
    yield


app = FastAPI(title="Chatboxd", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/api/bootstrap", response_model=BootstrapResponse)
def bootstrap() -> BootstrapResponse:
    configure_models_api_key()
    providers = [
        ProviderInfo(
            id=status.id,
            available=status.available,
            models=list(status.models),
        )
        for status in bootstrap_providers()
    ]
    return BootstrapResponse(
        db_exists=DB_PATH.is_file(),
        default_language=LANGUAGE,
        languages=LANGUAGE_NAMES,
        providers=providers,
        translations=TRANSLATIONS,
        provider_help=MODEL_PROVIDERS,
        no_db_text=_no_db_text(LANGUAGE),
    )


@app.get("/api/daily-message", response_model=DailyMessageResponse)
def daily_message(language: str = LANGUAGE) -> DailyMessageResponse:
    if not DB_PATH.is_file():
        return DailyMessageResponse(message=None)
    return DailyMessageResponse(message=get_daily_message(language))


@app.post("/api/ingest", response_model=IngestResponse)
async def ingest(export: UploadFile = File(...)) -> IngestResponse:
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        files = materialize_export(await export.read(), USER_DATA_DIR)
        LetterboxdStore(DB_PATH).ingest(
            files.diary_csv,
            files.reviews_csv,
            files.username,
        )
    except (ExportError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.error(f"Data ingestion failed: {exc}")
        raise HTTPException(status_code=500, detail="Data ingestion failed") from exc
    return IngestResponse(ok=True, db_exists=DB_PATH.is_file())


@app.post("/api/session/reset")
def reset_session(body: ResetRequest) -> dict[str, bool]:
    registry.reset(body.session_id)
    return {"ok": True}


@app.post("/api/chat")
async def chat(body: ChatRequest) -> StreamingResponse:
    try:
        agent = registry.get_or_create(
            body.session_id, body.provider, body.model, body.language
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.error(f"Failed to start agent: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Failed to initialize agent. Check secrets.env.",
        ) from exc

    async def event_stream() -> AsyncIterator[str]:
        try:
            async for raw in agent.run_async(body.message, body.session_id):
                for mapped in events_from_langgraph(raw, body.language):
                    yield _sse(mapped.model_dump())
            yield _sse(done_event().model_dump())
        except Exception as exc:
            logger.error(f"Chat stream failed: {exc}")
            yield _sse(error_event(str(exc)).model_dump())
            yield _sse(done_event().model_dump())

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


def _sse(payload: dict) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


def _no_db_text(language: str) -> str:
    bundle = TRANSLATIONS.get(language) or TRANSLATIONS["EN"]
    text = bundle.get("no_db_text")
    if isinstance(text, str) and text.strip():
        return text
    return str(TRANSLATIONS["EN"]["no_db_text"])
