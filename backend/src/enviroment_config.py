import os
from pathlib import Path
import subprocess

from dotenv import load_dotenv

from config import OLLAMA_SUPPORTED_MODELS
from paths import SECRETS_PATH
from utils.logger_utils import logger


def provider_available(provider_name: str) -> bool:
    name = provider_name.lower()
    if name == "ollama":
        return ollama_available()
    if name == "openai":
        return openai_available()
    if name == "google":
        return google_available()
    logger.warning(f"Provider `{provider_name}` unknown")
    return False


def openai_available() -> bool:
    available = bool(os.environ.get("OPENAI_API_KEY"))
    if not available:
        logger.warning("OpenAI is not available")
    return available


def google_available() -> bool:
    available = bool(os.environ.get("GOOGLE_API_KEY"))
    if not available:
        logger.warning("Google is not available")
    return available


def configure_models_api_key(env_path: Path | None = None) -> None:
    load_dotenv(dotenv_path=env_path or SECRETS_PATH)
    if os.environ.get("OPENAI_API_KEY"):
        logger.info("OpenAI Model env variables are loaded")
    else:
        logger.error("OpenAI Model env variables not loaded")
    if os.environ.get("GOOGLE_API_KEY"):
        logger.info("Google Model env variables are loaded")
    else:
        logger.error("Google Model env variables not loaded")


def ollama_available() -> bool:
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


def get_local_ollama_models(only_supported: bool = True) -> list[str]:
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, check=True
        )
        output = result.stdout.splitlines()
        if only_supported:
            return [
                line.split()[0]
                for line in output[1:]
                if line.split(":")[0] in OLLAMA_SUPPORTED_MODELS
            ]
        return [line.split()[0] for line in output[1:] if line]
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        logger.error(f"Error found while running ollama list: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error listing ollama models: {e}")
        return []
