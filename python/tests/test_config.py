"""Unit tests for tessera_langchain._config — the provider config helpers.

These tests run without LangChain installed. They verify the returned
kwargs dicts have the right shape for each provider's ChatModel.
"""

from __future__ import annotations

import pytest

from tessera_langchain import (
    TESSERA_BASE_URL,
    tessera_openai_config,
    tessera_anthropic_config,
    tessera_mistral_config,
    tessera_groq_config,
    tessera_cohere_config,
    tessera_config,
)


class TestOpenAI:
    def test_default(self):
        cfg = tessera_openai_config(api_key="tk_test")
        assert cfg["openai_api_base"] == f"{TESSERA_BASE_URL}/v1/openai"
        assert cfg["default_headers"] == {"x-tessera-api-key": "tk_test"}

    def test_extra_headers_merge(self):
        cfg = tessera_openai_config(
            api_key="tk_test",
            extra_headers={"x-custom": "value"},
        )
        assert cfg["default_headers"] == {
            "x-tessera-api-key": "tk_test",
            "x-custom": "value",
        }

    def test_custom_base_url_override(self):
        cfg = tessera_openai_config(
            api_key="tk_test",
            base_url="https://staging.tesseraai.io/v1/openai",
        )
        assert cfg["openai_api_base"] == "https://staging.tesseraai.io/v1/openai"


class TestAnthropic:
    def test_default(self):
        cfg = tessera_anthropic_config(api_key="tk_test")
        assert cfg["anthropic_api_url"] == f"{TESSERA_BASE_URL}/v1/anthropic"
        assert cfg["default_headers"] == {"x-tessera-api-key": "tk_test"}


class TestMistral:
    def test_default(self):
        cfg = tessera_mistral_config(api_key="tk_test")
        assert cfg["endpoint"] == f"{TESSERA_BASE_URL}/v1/mistral"
        assert cfg["default_headers"] == {"x-tessera-api-key": "tk_test"}


class TestGroq:
    def test_default(self):
        cfg = tessera_groq_config(api_key="tk_test")
        assert cfg["groq_api_base"] == f"{TESSERA_BASE_URL}/v1/groq"
        assert cfg["default_headers"] == {"x-tessera-api-key": "tk_test"}


class TestCohere:
    def test_default(self):
        cfg = tessera_cohere_config(api_key="tk_test")
        assert cfg["base_url"] == f"{TESSERA_BASE_URL}/v1/cohere"
        assert cfg["default_headers"] == {"x-tessera-api-key": "tk_test"}


class TestGenericDispatcher:
    @pytest.mark.parametrize(
        "provider,base_url_key",
        [
            ("openai", "openai_api_base"),
            ("anthropic", "anthropic_api_url"),
            ("mistral", "endpoint"),
            ("groq", "groq_api_base"),
            ("cohere", "base_url"),
        ],
    )
    def test_provider_routing(self, provider, base_url_key):
        cfg = tessera_config(provider=provider, api_key="tk_test")
        assert cfg[base_url_key] == f"{TESSERA_BASE_URL}/v1/{provider}"
        assert cfg["default_headers"] == {"x-tessera-api-key": "tk_test"}

    def test_unknown_provider_raises(self):
        with pytest.raises(ValueError, match="Unknown provider"):
            tessera_config(provider="not-a-provider", api_key="tk_test")  # type: ignore[arg-type]


class TestValidation:
    def test_empty_api_key_raises(self):
        with pytest.raises(ValueError, match="non-empty string"):
            tessera_openai_config(api_key="")

    def test_non_string_api_key_raises(self):
        with pytest.raises(ValueError, match="non-empty string"):
            tessera_openai_config(api_key=None)  # type: ignore[arg-type]
