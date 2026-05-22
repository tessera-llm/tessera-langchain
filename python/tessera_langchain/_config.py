"""Provider-specific config dicts for Tessera proxy routing.

Each `tessera_<provider>_config(api_key=...)` returns a dict of kwargs that
can be unpacked into the constructor of the corresponding LangChain
ChatModel. The kwargs change two things: the upstream base URL (to
api.tesseraai.io) and the auth header (the Tessera API key alongside
the existing provider key).

No LangChain import is required by this module — the kwargs are plain
dicts that LangChain ChatModels accept via their public init signatures.
"""

from __future__ import annotations

from typing import Any, Literal

TESSERA_BASE_URL = 'https://api.tesseraai.io'

ProviderName = Literal['openai', 'anthropic', 'mistral', 'groq', 'cohere']


def _validate_api_key(api_key: str) -> str:
    if not isinstance(api_key, str) or not api_key:
        raise ValueError(
            'tessera_*_config(api_key=...) requires a non-empty string. '
            'Get a free key from https://tesseraai.io/dev'
        )
    return api_key


def _proxy_endpoint(provider: ProviderName) -> str:
    return f'{TESSERA_BASE_URL}/v1/{provider}'


def _headers(api_key: str, extra: dict[str, str] | None = None) -> dict[str, str]:
    headers = {'x-tessera-api-key': api_key}
    if extra:
        headers.update(extra)
    return headers


def tessera_openai_config(
    api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Kwargs for `langchain_openai.ChatOpenAI(...)` to route through Tessera.

    Example::

        from langchain_openai import ChatOpenAI
        from tessera_langchain import tessera_openai_config

        llm = ChatOpenAI(
            model="gpt-4o",
            openai_api_key="sk-...",
            **tessera_openai_config(api_key="tsr_..."),
        )
    """
    api_key = _validate_api_key(api_key)
    endpoint = base_url or _proxy_endpoint('openai')
    return {
        'openai_api_base': endpoint,
        'default_headers': _headers(api_key, extra_headers),
    }


def tessera_anthropic_config(
    api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Kwargs for `langchain_anthropic.ChatAnthropic(...)` to route through Tessera."""
    api_key = _validate_api_key(api_key)
    endpoint = base_url or _proxy_endpoint('anthropic')
    return {
        'anthropic_api_url': endpoint,
        'default_headers': _headers(api_key, extra_headers),
    }


def tessera_mistral_config(
    api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Kwargs for `langchain_mistralai.ChatMistralAI(...)` to route through Tessera."""
    api_key = _validate_api_key(api_key)
    endpoint = base_url or _proxy_endpoint('mistral')
    return {
        'endpoint': endpoint,
        'default_headers': _headers(api_key, extra_headers),
    }


def tessera_groq_config(
    api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Kwargs for `langchain_groq.ChatGroq(...)` to route through Tessera."""
    api_key = _validate_api_key(api_key)
    endpoint = base_url or _proxy_endpoint('groq')
    return {
        'groq_api_base': endpoint,
        'default_headers': _headers(api_key, extra_headers),
    }


def tessera_cohere_config(
    api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Kwargs for `langchain_cohere.ChatCohere(...)` to route through Tessera."""
    api_key = _validate_api_key(api_key)
    endpoint = base_url or _proxy_endpoint('cohere')
    return {
        'base_url': endpoint,
        'default_headers': _headers(api_key, extra_headers),
    }


def tessera_config(
    provider: ProviderName,
    api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Generic dispatcher — returns the right kwargs dict for the given provider.

    Equivalent to calling `tessera_<provider>_config(...)` directly. Useful when
    the provider is parameterized at runtime.
    """
    mapping = {
        'openai': tessera_openai_config,
        'anthropic': tessera_anthropic_config,
        'mistral': tessera_mistral_config,
        'groq': tessera_groq_config,
        'cohere': tessera_cohere_config,
    }
    if provider not in mapping:
        raise ValueError(f'Unknown provider {provider!r}. Supported: {list(mapping)}')
    return mapping[provider](api_key=api_key, extra_headers=extra_headers, base_url=base_url)
