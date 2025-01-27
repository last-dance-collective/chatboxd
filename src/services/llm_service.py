from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI

from config import OLLAMA_MODEL, OPENAI_MODEL
from enviroment_config import configure_openai_api_key
from utils.logger_utils import logger


def ollama_model(model: str = OLLAMA_MODEL, temperature: int = 0) -> ChatOllama:
    """Returns the Ollama LLM object for the specified model.
    Ollama must be running in background using the command `ollama serve`
    """
    logger.info("🦙 Using Ollama")
    return ChatOllama(
        model=model,
        temperature=temperature,
    )


def openai_model(model: str = OPENAI_MODEL, temperature: int = 0) -> AzureChatOpenAI:
    """Returns the OpenAI LLM object for the specified model."""
    configure_openai_api_key()
    logger.info("⚙️  Using OpenAI")
    return AzureChatOpenAI(
        model=model,
        temperature=temperature,
    )
