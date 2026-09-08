import os
from pathlib import Path
from unittest import mock

from catalog.translations import MODEL_PROVIDERS
from services.llm_service import HostedModels, PROVIDERS, bootstrap_providers, build_llm

TEMPLATE_SECRETS = Path(__file__).resolve().parents[1] / "template_secrets.env"
GROQ_MODELS = (
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
)
OPENROUTER_MODELS = (
    "openrouter/free",
    "google/gemma-4-31b-it:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "thinkingmachines/inkling:free",
)


def test_hosted_env_vars_in_template() -> None:
    text = TEMPLATE_SECRETS.read_text()
    for provider in PROVIDERS:
        if isinstance(provider.source, HostedModels):
            assert provider.source.env_var in text


def test_every_provider_in_every_language() -> None:
    ids = [provider.id for provider in PROVIDERS]
    for language, help_map in MODEL_PROVIDERS.items():
        for provider_id in ids:
            assert provider_id in help_map, f"{provider_id} missing from {language}"


def test_build_llm_groq_has_bind_tools() -> None:
    with mock.patch.dict(os.environ, {"GROQ_API_KEY": "dummy"}):
        llm = build_llm("Groq", "llama-3.3-70b-versatile")
    assert hasattr(llm, "bind_tools")


def test_unknown_provider_raises() -> None:
    try:
        build_llm("Nope", "x")
    except ValueError as exc:
        assert str(exc) == "Invalid provider: Nope"
        return
    raise AssertionError("expected ValueError")


def test_groq_available_when_key_set() -> None:
    with mock.patch.dict(os.environ, {"GROQ_API_KEY": "dummy"}):
        statuses = {status.id: status for status in bootstrap_providers()}
    groq = statuses["Groq"]
    assert groq.available
    assert groq.models == GROQ_MODELS


def test_groq_unavailable_when_key_absent() -> None:
    with mock.patch.dict(os.environ):
        os.environ.pop("GROQ_API_KEY", None)
        statuses = {status.id: status for status in bootstrap_providers()}
    groq = statuses["Groq"]
    assert groq.available is False
    assert groq.models == GROQ_MODELS


def test_build_llm_openrouter_has_bind_tools() -> None:
    with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "dummy"}):
        llm = build_llm("OpenRouter", "openrouter/free")
    assert hasattr(llm, "bind_tools")


def test_openrouter_available_when_key_set() -> None:
    with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "dummy"}):
        statuses = {status.id: status for status in bootstrap_providers()}
    openrouter = statuses["OpenRouter"]
    assert openrouter.available
    assert openrouter.models == OPENROUTER_MODELS


def test_openrouter_unavailable_when_key_absent() -> None:
    with mock.patch.dict(os.environ):
        os.environ.pop("OPENROUTER_API_KEY", None)
        statuses = {status.id: status for status in bootstrap_providers()}
    openrouter = statuses["OpenRouter"]
    assert openrouter.available is False
    assert openrouter.models == OPENROUTER_MODELS


if __name__ == "__main__":
    test_hosted_env_vars_in_template()
    test_every_provider_in_every_language()
    test_build_llm_groq_has_bind_tools()
    test_unknown_provider_raises()
    test_groq_available_when_key_set()
    test_groq_unavailable_when_key_absent()
    test_build_llm_openrouter_has_bind_tools()
    test_openrouter_available_when_key_set()
    test_openrouter_unavailable_when_key_absent()
    print("ok")
