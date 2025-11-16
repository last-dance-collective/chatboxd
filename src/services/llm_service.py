from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from utils.logger_utils import logger


def ollama_model(model: str, temperature: int = 0) -> ChatOllama:
    """Returns the Ollama LLM object for the specified model.
    Ollama must be running in background using the command `ollama serve`
    """
    logger.info("🦙 Using Ollama")
    return ChatOllama(
        model=model,
        temperature=temperature,
    )


def openai_model(model: str, temperature: int = 0) -> ChatOpenAI:
    """Returns the OpenAI LLM object for the specified model."""
    logger.info("⚙️  Using OpenAI")
    return ChatOpenAI(
        model=model,
        temperature=temperature,
    )


def gemini_model(model: str, temperature: int = 0) -> ChatGoogleGenerativeAI:
    """Returns the Gemini LLM object for the specified model."""
    logger.info("🧪  Using Gemini")
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature,
    )
