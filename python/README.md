# tessera-langchain

[![PyPI version](https://img.shields.io/pypi/v/tessera-langchain.svg)](https://pypi.org/project/tessera-langchain/) [![Python](https://img.shields.io/pypi/pyversions/tessera-langchain.svg)](https://pypi.org/project/tessera-langchain/)

**Drop-in cost optimization for LangChain ChatModels.** One line of config in your existing `ChatOpenAI` / `ChatAnthropic` / `ChatMistralAI` / `ChatGroq` / `ChatCohere` constructor routes your traffic through the [Tessera](https://tesseraai.io) proxy — auto-route, exact + provider-prompt-cache hits, per-role compression, output-length ceiling, batch arbitrage. Free Dev tier: **60M tokens/month, no card**. Production: **20% of measured savings, $0 if we save you nothing**.

Companion package to [`tessera-llm-proxy`](https://pypi.org/project/tessera-llm-proxy/) — same proxy, LangChain-shaped API.

## Install

```bash
pip install tessera-langchain
```

## Quickstart

```python
from langchain_openai import ChatOpenAI
from tessera_langchain import tessera_openai_config

llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key="sk-...",                      # your OpenAI key, unchanged
    **tessera_openai_config(api_key="tsr_..."),   # one line, routes through Tessera
)

# Existing LangChain code (agents, chains, tools, streaming) runs unchanged.
response = llm.invoke("Summarize a Kubernetes operator architecture in 3 bullets.")
```

Same pattern for the other providers — `tessera_anthropic_config`, `tessera_mistral_config`, `tessera_groq_config`, `tessera_cohere_config`.

Or wrap an existing instance:

```python
from tessera_langchain import wrap_openai

llm = wrap_openai(my_existing_ChatOpenAI, tessera_api_key="tsr_...")
```

## Free key

Get a free API key (60M tokens/mo, no card) at **[tesseraai.io/dev](https://tesseraai.io/dev)** — sign-up takes ~30 seconds and returns an instant `tsr_…` key plus magic-link dashboard access.

## Documentation

Full README with worked-numbers example ($24k → $9.4k OpenAI bill cut), mechanic table, FAQ, and architecture notes:

→ **[github.com/tessera-llm/tessera-langchain](https://github.com/tessera-llm/tessera-langchain)**

Tessera platform:

→ **[tesseraai.io](https://tesseraai.io)**

## License

Apache-2.0. The SDK is open source; the optimization proxy at `api.tesseraai.io` is closed. Wire format is open; mechanic implementations are not.
