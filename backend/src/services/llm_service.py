from __future__ import annotations

import os
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_openrouter import ChatOpenRouter

from paths import SECRETS_PATH
from utils.logger_utils import logger

TEMPERATURE = 0

OLLAMA_SUPPORTED_MODELS = (
    "qwen3.8",
    "deepseek-r1",
    "llama3.1",
    "gemma4",
    "mistral",
    "llama3.3",
    "gpt-oss",
)


@dataclass(frozen=True)
class HostedModels:
    env_var: str
    catalog: tuple[str, ...]

    def available(self) -> bool:
        return bool(os.environ.get(self.env_var))

    def models(self) -> tuple[str, ...]:
        return self.catalog


@dataclass(frozen=True)
class LocalModels:
    probe: Callable[[], bool]
    installed: Callable[[], tuple[str, ...]]

    def available(self) -> bool:
        return self.probe()

    def models(self) -> tuple[str, ...]:
        return self.installed()


@dataclass(frozen=True)
class Provider:
    id: str
    source: HostedModels | LocalModels
    build: Callable[[str], BaseChatModel]

    def status(self) -> ProviderStatus:
        return ProviderStatus(
            self.id,
            self.source.available(),
            self.source.models(),
        )


@dataclass(frozen=True)
class ProviderStatus:
    id: str
    available: bool
    models: tuple[str, ...]


def _ollama_available() -> bool:
    try:
        result = subprocess.run(
            ["ollama", "--version"], capture_output=True, text=True, check=True
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        logger.warning("Ollama is not available")
        return False
    available = result.stdout.lower().startswith("ollama")
    if not available:
        logger.warning("Ollama is not available")
    return available


def _local_ollama_models() -> tuple[str, ...]:
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, check=True
        )
        output = result.stdout.splitlines()
        return tuple(
            line.split()[0]
            for line in output[1:]
            if line.split(":")[0] in OLLAMA_SUPPORTED_MODELS
        )
    except FileNotFoundError:
        return ()
    except subprocess.CalledProcessError as e:
        logger.error(f"Error found while running ollama list: {e}")
        return ()
    except Exception as e:
        logger.error(f"Unexpected error listing ollama models: {e}")
        return ()


def _google(model: str) -> BaseChatModel:
    logger.info("🧪  Using Gemini")
    return ChatGoogleGenerativeAI(model=model, temperature=TEMPERATURE)


def _openai(model: str) -> BaseChatModel:
    logger.info("⚙️  Using OpenAI")
    return ChatOpenAI(model=model, temperature=TEMPERATURE)


def _ollama(model: str) -> BaseChatModel:
    logger.info("🦙 Using Ollama")
    return ChatOllama(model=model, temperature=TEMPERATURE)


def _groq(model: str) -> BaseChatModel:
    logger.info("⚡ Using Groq")
    return ChatGroq(model=model, temperature=TEMPERATURE)


def _openrouter(model: str) -> BaseChatModel:
    logger.info("Using OpenRouter")
    return ChatOpenRouter(model=model, temperature=TEMPERATURE)


PROVIDERS: tuple[Provider, ...] = (
    Provider(
        id="Google",
        source=HostedModels(
            env_var="GOOGLE_API_KEY",
            catalog=(
                "gemini-3.8-flash",
                "gemini-3.7-flash",
                "gemini-3.6-flash",
            ),
        ),
        build=_google,
    ),
    Provider(
        id="OpenAI",
        source=HostedModels(
            env_var="OPENAI_API_KEY",
            catalog=(
                "gpt-5.6-terra",
                "gpt-5.6-luna ",
                "gpt-5.4-nano",
            ),
        ),
        build=_openai,
    ),
    Provider(
        id="Ollama",
        source=LocalModels(probe=_ollama_available, installed=_local_ollama_models),
        build=_ollama,
    ),
    Provider(
        id="Groq",
        source=HostedModels(
            env_var="GROQ_API_KEY",
            catalog=(
                "qwen/qwen3.8-27b",
                "qwen/qwen3.6-27b",
                "openai/gpt-oss-20b",
                "openai/gpt-oss-120b",
            ),
        ),
        build=_groq,
    ),
    Provider(
        id="OpenRouter",
        source=HostedModels(
            env_var="OPENROUTER_API_KEY",
            catalog=("openrouter/free",),
        ),
        build=_openrouter,
    ),
)


def configure_models_api_key(env_path: Path | None = None) -> None:
    load_dotenv(dotenv_path=env_path or SECRETS_PATH)
    for provider in PROVIDERS:
        source = provider.source
        if not isinstance(source, HostedModels):
            continue
        if os.environ.get(source.env_var):
            logger.info(f"{provider.id} Model env variables are loaded")
        else:
            logger.warning(f"{provider.id} Model env variables not loaded")


def bootstrap_providers() -> list[ProviderStatus]:
    return [provider.status() for provider in PROVIDERS]


def build_llm(provider: str, model: str) -> BaseChatModel:
    key = provider.casefold()
    for row in PROVIDERS:
        if row.id.casefold() == key:
            return row.build(model)
    raise ValueError(f"Invalid provider: {provider}")
