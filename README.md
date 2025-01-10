![image](https://github.com/user-attachments/assets/e2f778f5-8ae4-465f-9362-250b8914c7ba)

----

Chatboxd is a web application that allows you to easily interact with your LeeterBoxd statistics thanks to the power of GenAI.

It is multi-language, allows the use of several LLM models and contains many other features.

## Contents

1. [Execution](#execution)
   - [Environment Variables](#environment-variables)
   - [Load Data](#load-data)
   - [Run App](#run-app)
     
2. [How It Works](#how-it-works)
   - [Agent](#agent)
   - [Tools](#tools)
   - [BBDD](#bbdd)

## Execution

### Environment Variables

### Load Data

### Run App

## How It Works

### Agent

### Tools

### BBDD

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
