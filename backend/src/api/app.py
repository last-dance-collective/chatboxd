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
from catalog.translations import LANGUAGE_NAMES, MODEL_PROVIDERS, NO_DB_TEXT, TRANSLATIONS
from config import LANGUAGE, MODELS
from data_ingestion.main import main as ingest_letterboxd
from enviroment_config import (
    configure_models_api_key,
    get_local_ollama_models,
    provider_available,
)
from paths import DB_PATH, SECRETS_PATH, USER_DATA_DIR
from services.daily_message_service import get_daily_message
from utils.logger_utils import logger

EXPECTED_FILENAMES = {"reviews.csv", "diary.csv"}


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
    models = {name: list(values) for name, values in MODELS.items()}
    available = [provider for provider in models if provider_available(provider)]
    if "Ollama" in available:
        models["Ollama"] = get_local_ollama_models()
    providers = [
        ProviderInfo(
            id=provider,
            available=provider in available,
            models=list(models.get(provider, [])),
        )
        for provider in models
    ]
    return BootstrapResponse(
        db_exists=DB_PATH.is_file(),
        default_language=LANGUAGE,
        languages=LANGUAGE_NAMES,
        providers=providers,
        translations=TRANSLATIONS,
        provider_help=MODEL_PROVIDERS,
        no_db_text=NO_DB_TEXT,
    )


@app.get("/api/daily-message", response_model=DailyMessageResponse)
def daily_message(language: str = LANGUAGE) -> DailyMessageResponse:
    if not DB_PATH.is_file():
        return DailyMessageResponse(message=None)
    return DailyMessageResponse(message=get_daily_message(language))


@app.post("/api/ingest", response_model=IngestResponse)
async def ingest(
    diary: UploadFile = File(...),
    reviews: UploadFile = File(...),
) -> IngestResponse:
    names = {diary.filename, reviews.filename}
    if names != EXPECTED_FILENAMES:
        raise HTTPException(
            status_code=400,
            detail="Upload both diary.csv and reviews.csv",
        )
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    for upload in (diary, reviews):
        if upload.filename is None:
            raise HTTPException(status_code=400, detail="Missing filename")
        dest = USER_DATA_DIR / upload.filename
        dest.write_bytes(await upload.read())
    try:
        ingest_letterboxd()
    except ValueError as exc:
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
