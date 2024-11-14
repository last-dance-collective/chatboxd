from langchain_ollama import ChatOllama

def ollama_model(model, temperature=0):
    """Returns the Ollama LLM object for the specified model.
    Ollama must be running in background using the command `ollama serve`
    """
    return ChatOllama(
        model=model,
        temperature=temperature,
    )