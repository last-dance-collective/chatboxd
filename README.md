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