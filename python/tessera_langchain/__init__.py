# ruff: noqa: RUF002
# (U+00D7 MULTIPLICATION SIGN in docstrings is intentional branding glyph, not letter x.)
"""Tessera × LangChain integration — drop-in cost optimization for any LangChain ChatModel.

Usage (most common):

    from langchain_openai import ChatOpenAI
    from tessera_langchain import tessera_openai_config

    llm = ChatOpenAI(
        model="gpt-4o",
        openai_api_key="sk-...",
        **tessera_openai_config(api_key="tk_..."),
    )

    # Existing code runs unchanged. Requests now route through
    # api.tesseraai.io and get auto-routed / auto-cached / auto-compressed.

Or wrap an existing ChatModel instance:

    base_llm = ChatOpenAI(model="gpt-4o", openai_api_key="sk-...")
    llm = wrap_openai(base_llm, tessera_api_key="tk_...")

See https://tesseraai.io/dev for the dashboard, free tier, and full
mechanic documentation.
"""

from tessera_langchain._config import (
    TESSERA_BASE_URL,
    tessera_anthropic_config,
    tessera_cohere_config,
    tessera_config,
    tessera_groq_config,
    tessera_mistral_config,
    tessera_openai_config,
)
from tessera_langchain._version import __version__
from tessera_langchain._wrap import (
    wrap_anthropic,
    wrap_cohere,
    wrap_groq,
    wrap_mistral,
    wrap_openai,
)

__all__ = [
    'TESSERA_BASE_URL',
    '__version__',
    'tessera_anthropic_config',
    'tessera_cohere_config',
    'tessera_config',
    'tessera_groq_config',
    'tessera_mistral_config',
    'tessera_openai_config',
    'wrap_anthropic',
    'wrap_cohere',
    'wrap_groq',
    'wrap_mistral',
    'wrap_openai',
]
