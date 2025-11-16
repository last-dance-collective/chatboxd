LANGUAGE = "ES"

MODELS = {
    # "Ollama": [],
    "OpenAI": [
        "gpt-4o-mini",
        "gpt-4o",
    ],
    "Google": [
        "gemini-2.5-flash",
        # "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
        # "gemini-2.0-flash-lite",
    ],
}

OLLAMA_SUPPORTED_MODELS = [
    "llama3.3",
    "llama3.1",
    "mistral",
    "qwen2.5",
]

CONVERS_TURNS = 6
