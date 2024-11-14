# chatboxd

## UV Basics

Install [uv](https://docs.astral.sh/uv/getting-started/installation/):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

# or
brew install uv
```

Run a script (it also checks the dependencies, dont worry):
```bash
uv run src/main.py
```

Add a dependency:
```bash
uv add requests

# Specify a version constraint
uv add 'requests==2.31.0'
```

## Ollama Models

To run LLMs locally, first install [ollama](https://ollama.com/download/linux):
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Then, you must pull the LLM you want to use. For example, `llama3.2:3b`:
```bash
ollama pull llama3.2:3b
```

Finally, the ollama service must be started:
```bash
ollama serve
```

The service must keep running in background in order to access the LLM in the application.
