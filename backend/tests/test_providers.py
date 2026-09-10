import os
from pathlib import Path
from unittest import mock

from catalog.translations import MODEL_PROVIDERS
from services.llm_service import HostedModels, PROVIDERS, bootstrap_providers, build_llm

TEMPLATE_SECRETS = Path(__file__).resolve().parents[1] / "template_secrets.env"
HOSTED = [provider for provider in PROVIDERS if isinstance(provider.source, HostedModels)]


def test_hosted_env_vars_in_template() -> None:
    text = TEMPLATE_SECRETS.read_text()
    for provider in HOSTED:
        assert provider.source.env_var in text


def test_every_provider_in_every_language() -> None:
    ids = [provider.id for provider in PROVIDERS]
    for language, help_map in MODEL_PROVIDERS.items():
        for provider_id in ids:
            assert provider_id in help_map, f"{provider_id} missing from {language}"


def test_hosted_catalog_comes_from_the_table() -> None:
    env = {provider.source.env_var: "dummy" for provider in HOSTED}
    with mock.patch.dict(os.environ, env):
        statuses = {status.id: status for status in bootstrap_providers()}
    for provider in HOSTED:
        status = statuses[provider.id]
        assert status.available
        assert status.models == provider.source.catalog


def test_hosted_unavailable_without_key() -> None:
    with mock.patch.dict(os.environ):
        for provider in HOSTED:
            os.environ.pop(provider.source.env_var, None)
        statuses = {status.id: status for status in bootstrap_providers()}
    for provider in HOSTED:
        status = statuses[provider.id]
        assert status.available is False
        assert status.models == provider.source.catalog


def test_hosted_build_has_bind_tools() -> None:
    for provider in HOSTED:
        with mock.patch.dict(os.environ, {provider.source.env_var: "dummy"}):
            llm = build_llm(provider.id, provider.source.catalog[0])
        assert hasattr(llm, "bind_tools")


def test_unknown_provider_raises() -> None:
    try:
        build_llm("Nope", "x")
    except ValueError as exc:
        assert str(exc) == "Invalid provider: Nope"
        return
    raise AssertionError("expected ValueError")


if __name__ == "__main__":
    test_hosted_env_vars_in_template()
    test_every_provider_in_every_language()
    test_hosted_catalog_comes_from_the_table()
    test_hosted_unavailable_without_key()
    test_hosted_build_has_bind_tools()
    test_unknown_provider_raises()
    print("ok")
