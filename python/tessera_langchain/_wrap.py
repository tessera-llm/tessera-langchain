"""Wrappers that take an existing LangChain ChatModel instance and return a
new instance pointed at the Tessera proxy.

These are convenience helpers for users who already have a configured
ChatModel and want to retrofit Tessera routing without rebuilding the
constructor call. Internally each wrap_* function copies the relevant
fields from the input and overrides the base URL + default headers.

For new code paths, prefer the cleaner pattern via tessera_*_config(...)
passed directly to the constructor — see tessera_langchain._config.
"""

from __future__ import annotations

from typing import Any, TypeVar

from tessera_langchain._config import (
    tessera_openai_config,
    tessera_anthropic_config,
    tessera_mistral_config,
    tessera_groq_config,
    tessera_cohere_config,
)

ChatModelT = TypeVar("ChatModelT")


def _copy_with_overrides(model: Any, **overrides: Any) -> Any:
    """Return a copy of `model` with the given fields overridden.

    LangChain ChatModels are pydantic BaseModels with `.model_copy(update={...})`
    on pydantic v2, falling back to `.copy(update={...})` on v1. We try both
    in order; if neither exists we raise a clear error.
    """
    if hasattr(model, "model_copy"):
        return model.model_copy(update=overrides)
    if hasattr(model, "copy"):
        return model.copy(update=overrides)
    raise TypeError(
        f"Cannot wrap object of type {type(model).__name__}: it does not "
        "expose `.model_copy(...)` or `.copy(update=...)`. "
        "Make sure you are passing a LangChain ChatModel instance."
    )


def wrap_openai(chat_model: ChatModelT, tessera_api_key: str) -> ChatModelT:
    """Return a copy of `chat_model` routed through the Tessera OpenAI endpoint.

    Example::

        from langchain_openai import ChatOpenAI
        from tessera_langchain import wrap_openai

        base = ChatOpenAI(model="gpt-4o", openai_api_key="sk-...")
        llm = wrap_openai(base, tessera_api_key="tsr_...")
    """
    cfg = tessera_openai_config(api_key=tessera_api_key)
    merged_headers = {
        **(getattr(chat_model, "default_headers", None) or {}),
        **cfg["default_headers"],
    }
    return _copy_with_overrides(
        chat_model,
        openai_api_base=cfg["openai_api_base"],
        default_headers=merged_headers,
    )


def wrap_anthropic(chat_model: ChatModelT, tessera_api_key: str) -> ChatModelT:
    """Return a copy of `chat_model` routed through the Tessera Anthropic endpoint."""
    cfg = tessera_anthropic_config(api_key=tessera_api_key)
    merged_headers = {
        **(getattr(chat_model, "default_headers", None) or {}),
        **cfg["default_headers"],
    }
    return _copy_with_overrides(
        chat_model,
        anthropic_api_url=cfg["anthropic_api_url"],
        default_headers=merged_headers,
    )


def wrap_mistral(chat_model: ChatModelT, tessera_api_key: str) -> ChatModelT:
    """Return a copy of `chat_model` routed through the Tessera Mistral endpoint."""
    cfg = tessera_mistral_config(api_key=tessera_api_key)
    merged_headers = {
        **(getattr(chat_model, "default_headers", None) or {}),
        **cfg["default_headers"],
    }
    return _copy_with_overrides(
        chat_model,
        endpoint=cfg["endpoint"],
        default_headers=merged_headers,
    )


def wrap_groq(chat_model: ChatModelT, tessera_api_key: str) -> ChatModelT:
    """Return a copy of `chat_model` routed through the Tessera Groq endpoint."""
    cfg = tessera_groq_config(api_key=tessera_api_key)
    merged_headers = {
        **(getattr(chat_model, "default_headers", None) or {}),
        **cfg["default_headers"],
    }
    return _copy_with_overrides(
        chat_model,
        groq_api_base=cfg["groq_api_base"],
        default_headers=merged_headers,
    )


def wrap_cohere(chat_model: ChatModelT, tessera_api_key: str) -> ChatModelT:
    """Return a copy of `chat_model` routed through the Tessera Cohere endpoint."""
    cfg = tessera_cohere_config(api_key=tessera_api_key)
    merged_headers = {
        **(getattr(chat_model, "default_headers", None) or {}),
        **cfg["default_headers"],
    }
    return _copy_with_overrides(
        chat_model,
        base_url=cfg["base_url"],
        default_headers=merged_headers,
    )
