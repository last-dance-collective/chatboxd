import os
from dotenv import load_dotenv
from pathlib import Path

from utils.logger_utils import logger


def configure_openai_api_key():
    env_path = Path(".") / "secrets.env"
    load_dotenv(dotenv_path=env_path)

    if (
        os.environ.get("AZURE_OPENAI_ENDPOINT")
        and os.environ.get("OPENAI_API_VERSION")
        and os.environ.get("OPENAI_API_KEY")
    ):
        logger.info("🔑 Model env variables are loaded")
    else:
        logger.error("🔑🔴 Model env variables not loaded")
        raise Exception
