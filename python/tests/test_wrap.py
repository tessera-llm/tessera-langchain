"""Unit tests for tessera_langchain._wrap — the model-wrapping helpers.

These tests do NOT import LangChain. They use a minimal stub class that
mimics the LangChain ChatModel surface relevant to the wrap_* functions:
a `.model_copy(update={...})` method (pydantic v2 shape) plus the
`default_headers` attribute.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Dict, Optional

import pytest

from tessera_langchain import (
    TESSERA_BASE_URL,
    wrap_openai,
    wrap_anthropic,
    wrap_mistral,
    wrap_groq,
    wrap_cohere,
)


@dataclass
class _StubModel:
    """Minimal LangChain-ChatModel shaped stub. Supports model_copy(update=...)."""

    model_name: str = "stub-model"
    default_headers: Optional[Dict[str, str]] = None
    openai_api_base: Optional[str] = None
    anthropic_api_url: Optional[str] = None
    endpoint: Optional[str] = None
    groq_api_base: Optional[str] = None
    base_url: Optional[str] = None

    def model_copy(self, update: Optional[Dict[str, Any]] = None) -> "_StubModel":
        if not update:
            return replace(self)
        return replace(self, **update)


class TestWrapOpenAI:
    def test_overrides_base_url(self):
        base = _StubModel(model_name="gpt-4o")
        wrapped = wrap_openai(base, tessera_api_key="tsr_test")
        assert wrapped.openai_api_base == f"{TESSERA_BASE_URL}/v1/openai"

    def test_injects_tessera_header(self):
        base = _StubModel(model_name="gpt-4o")
        wrapped = wrap_openai(base, tessera_api_key="tsr_test")
        assert wrapped.default_headers == {"x-tessera-api-key": "tsr_test"}

    def test_merges_existing_headers(self):
        base = _StubModel(
            model_name="gpt-4o",
            default_headers={"x-app": "my-app", "x-trace": "abc"},
        )
        wrapped = wrap_openai(base, tessera_api_key="tsr_test")
        assert wrapped.default_headers == {
            "x-app": "my-app",
            "x-trace": "abc",
            "x-tessera-api-key": "tsr_test",
        }

    def test_returns_new_instance(self):
        base = _StubModel(model_name="gpt-4o")
        wrapped = wrap_openai(base, tessera_api_key="tsr_test")
        assert wrapped is not base
        assert base.openai_api_base is None  # original untouched
        assert base.default_headers is None


class TestWrapAnthropic:
    def test_overrides_base_url(self):
        base = _StubModel(model_name="claude-sonnet-4-5")
        wrapped = wrap_anthropic(base, tessera_api_key="tsr_test")
        assert wrapped.anthropic_api_url == f"{TESSERA_BASE_URL}/v1/anthropic"


class TestWrapMistral:
    def test_overrides_endpoint(self):
        base = _StubModel(model_name="mistral-large")
        wrapped = wrap_mistral(base, tessera_api_key="tsr_test")
        assert wrapped.endpoint == f"{TESSERA_BASE_URL}/v1/mistral"


class TestWrapGroq:
    def test_overrides_base_url(self):
        base = _StubModel(model_name="llama-3.3-70b")
        wrapped = wrap_groq(base, tessera_api_key="tsr_test")
        assert wrapped.groq_api_base == f"{TESSERA_BASE_URL}/v1/groq"


class TestWrapCohere:
    def test_overrides_base_url(self):
        base = _StubModel(model_name="command-r-plus")
        wrapped = wrap_cohere(base, tessera_api_key="tsr_test")
        assert wrapped.base_url == f"{TESSERA_BASE_URL}/v1/cohere"


class TestWrapErrors:
    def test_rejects_non_chatmodel_object(self):
        class _NoCopyShape:
            pass

        with pytest.raises(TypeError, match="model_copy"):
            wrap_openai(_NoCopyShape(), tessera_api_key="tsr_test")

    def test_rejects_empty_api_key(self):
        base = _StubModel(model_name="gpt-4o")
        with pytest.raises(ValueError, match="non-empty string"):
            wrap_openai(base, tessera_api_key="")
