import os
from utils.logger_utils import logger

keys_cache = {}

# These variables are meant to place the openai values
# if you don't want to use the env variables
OPEN_AI_CONFIG = {
    "AZURE_OPENAI_ENDPOINT": None,
    "OPENAI_API_VERSION": None,
    "OPENAI_API_KEY": None,
}


def configure_openai_api_key():
    load_openai_env_vars()
    if (
        os.environ.get("AZURE_OPENAI_ENDPOINT")
        and os.environ.get("OPENAI_API_VERSION")
        and os.environ.get("OPENAI_API_KEY")
    ):
        logger.info("🔑 Model env variables are loaded")
    else:
        logger.error("🔑🔴 Model env variables not loaded")


def load_openai_env_vars():
    load_env_var("AZURE_OPENAI_ENDPOINT")
    load_env_var("OPENAI_API_VERSION")
    load_env_var("OPENAI_API_KEY")


def load_env_var(name):
    if not os.environ.get(name):
        os.environ[name] = OPEN_AI_CONFIG[name]
