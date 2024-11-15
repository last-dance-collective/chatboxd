import os
import json
from utils.logger_utils import logger

keys_cache = {}


def get_open_ai_dict_model(model):
    return keys_cache["OPEN_AI_API_DICT"][model]


def load_env_config(env_path):
    try:
        with open(env_path, "r") as archivo:
            datos = json.load(archivo)
        return datos
    except Exception as e:
        logger.error(f"🔑🔴 Error loading credentials: {e}")
        return None


def load_credentials():
    if os.environ.get("CREDENTIALS_FILE_PATH"):
        logger.info("🔑 Credentials file found")

    else:
        logger.error("🔑🔴 Credentials file not found")

    return load_env_config(os.environ.get("CREDENTIALS_FILE_PATH"))


keys_json = load_credentials()


if keys_json:
    keys_cache["OPEN_AI_API_DICT"] = keys_json.get("open_ai_dict")

    logger.info("🔑 Credentials loaded")
else:
    logger.error("🔑🔴 Credentials not loaded")


def configure_openai_api_key(model):
    os.environ["AZURE_OPENAI_ENDPOINT"] = get_open_ai_dict_model(model)["endpoint"]
    os.environ["OPENAI_API_VERSION"] = get_open_ai_dict_model(model)["api_version"]
    os.environ["OPENAI_API_KEY"] = get_open_ai_dict_model(model)["key"]
