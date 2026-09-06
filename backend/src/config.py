LANGUAGE = "ES"

MODELS = {
    # "Ollama": [],
    "OpenAI": [
        "gpt-4o-mini",
        "gpt-4o",
    ],
    "Google": [
        "gemini-3.6-flash",
        "gemini-2.5-flash",
    ],
}

OLLAMA_SUPPORTED_MODELS = [
    "llama3.3",
    "llama3.1",
    "mistral",
    "qwen2.5",
]

CONVERS_TURNS = 6
