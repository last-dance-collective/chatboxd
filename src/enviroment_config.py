import os
from dotenv import load_dotenv
from pathlib import Path
import subprocess

import streamlit as st

from config import OLLAMA_SUPPORTED_MODELS
from utils.logger_utils import logger


def provider_available(provider_name):
    if provider_name.lower() == "ollama":
        return ollama_available()
    elif provider_name.lower() == "openai":
        return openai_available()
    else:
        logger.warning("Provider `{provider_name}` unknown")
        return False


def openai_available():
    available = os.environ.get("OPENAI_API_KEY")
    if not available:
        logger.warning("OpenAI is not available")

    return available


def configure_openai_api_key():
    env_path = Path(".") / "secrets.env"
    load_dotenv(dotenv_path=env_path)

    if os.environ.get("OPENAI_API_KEY"):
        logger.info("🔑 Model env variables are loaded")
    else:
        logger.error("🔑🔴 Model env variables not loaded")


def ollama_available():
    result = subprocess.run(
        ["ollama", "--version"], capture_output=True, text=True, check=True
    )
    output = result.stdout

    available = output.lower().startswith("ollama")

    if not available:
        logger.warning("Ollama is not available")

    return available


def get_local_ollama_models(only_supported=True):
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, check=True
        )
        output = result.stdout.splitlines()

        if only_supported:
            ollama_models = [
                line.split()[0]
                for line in output[1:]
                if line.split(":")[0] in OLLAMA_SUPPORTED_MODELS
            ]

        else:
            ollama_models = [line.split()[0] for line in output[1:] if line]

        return ollama_models

    except subprocess.CalledProcessError as e:
        logger.error(f"Error found while running ollama list: {e}")
        return []

    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return []
