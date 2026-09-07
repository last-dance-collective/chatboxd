from __future__ import annotations

import importlib.metadata as metadata
import inspect
import sys
from pathlib import Path

PACKAGES = [
    "langchain",
    "langchain-core",
    "langchain-openai",
    "langchain-ollama",
    "langchain-google-genai",
    "langchain-groq",
    "langgraph",
    "fastapi",
    "sqlalchemy",
    "pydantic",
]


def versions() -> dict[str, str]:
    out: dict[str, str] = {}
    for name in PACKAGES:
        try:
            out[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            out[name] = "MISSING"
    return out


def import_graph() -> None:
    from langgraph.checkpoint import memory as checkpoint_memory
    from langgraph.graph import START, StateGraph
    from langgraph.prebuilt import ToolNode, tools_condition
    from langchain_core.messages import HumanMessage, RemoveMessage, SystemMessage
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_groq import ChatGroq
    from langchain_ollama import ChatOllama
    from langchain_openai import ChatOpenAI

    from api.app import app
    from services.langgraph_service import ChatboxdAgent

    savers = [
        name
        for name in ("MemorySaver", "InMemorySaver")
        if hasattr(checkpoint_memory, name)
    ]
    print(f"checkpointers={','.join(savers)}")
    print(f"app={app.title}")
    print(f"start={START}")
    print(
        "chat_models="
        + ",".join(
            cls.__name__
            for cls in (
                ChatGoogleGenerativeAI,
                ChatGroq,
                ChatOllama,
                ChatOpenAI,
            )
        )
    )
    print(
        "graph="
        + ",".join(
            (
                StateGraph.__name__,
                ToolNode.__name__,
                tools_condition.__name__,
                HumanMessage.__name__,
                RemoveMessage.__name__,
                SystemMessage.__name__,
            )
        )
    )
    run_async = inspect.signature(ChatboxdAgent.run_async)
    print(f"run_async{run_async}")


def main() -> int:
    src = Path(__file__).resolve().parents[1] / "src"
    sys.path.insert(0, str(src))
    for name, version in versions().items():
        print(f"{name}={version}")
    import_graph()
    print("import_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
