# Changelog

All notable changes to `tessera-langchain` (Python) and `@tessera-llm/langchain` (Node / TypeScript) will be documented here.

This file follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The Python and Node packages share a single CHANGELOG and are versioned together — same release tag triggers both PyPI and npm publishes.

## [Unreleased]

## [0.1.0] — 2026-05-19 — first public release

### Added

- **Python:** `tessera-langchain` package on PyPI.
  - `tessera_openai_config(api_key=...)` — kwargs for `ChatOpenAI(...)` constructor.
  - `tessera_anthropic_config(api_key=...)` — kwargs for `ChatAnthropic(...)`.
  - `tessera_mistral_config(api_key=...)` — kwargs for `ChatMistralAI(...)`.
  - `tessera_groq_config(api_key=...)` — kwargs for `ChatGroq(...)`.
  - `tessera_cohere_config(api_key=...)` — kwargs for `ChatCohere(...)`.
  - `tessera_config(provider, api_key=...)` — generic dispatcher.
  - `wrap_openai(model, tessera_api_key)` / `wrap_anthropic` / `wrap_mistral` / `wrap_groq` / `wrap_cohere` — convenience helpers that return a new ChatModel instance routed through Tessera.
  - Optional `extra_headers` and `base_url` parameters on every config function (custom Tessera deployments, staging endpoints).
- **Node / TypeScript:** `@tessera-llm/langchain` package on npm.
  - `tesseraOpenAIConfig` / `tesseraAnthropicConfig` / `tesseraMistralConfig` / `tesseraGroqConfig` / `tesseraCohereConfig` — constructor options for the corresponding LangChain.js ChatModel.
  - `tesseraConfig(provider, input)` — generic dispatcher.
  - `wrapOpenAI` / `wrapAnthropic` / `wrapMistral` / `wrapGroq` / `wrapCohere` — convenience helpers.
- **Examples** under `examples/` showing OpenAI + Anthropic LangChain pipelines in Python and TypeScript.
- **Tests:** Python tests use a minimal stub model (no LangChain install needed for CI). Node tests use vitest with the same pattern.
- **Type stubs:** `py.typed` marker for PEP 561 `mypy --strict` recognition.
- **License:** Apache-2.0.

### Architecture notes

- This package is a thin client. Every mechanic decision (route, cache, compress, prompt-cache headers, output-length cap, batch arbitrage) runs in the closed-source Tessera Cloudflare Worker proxy at `api.tesseraai.io`. The split is intentional: the wire format is open and auditable; the mechanic implementations are closed because that's the asymmetric IP.
- Same proxy + mechanic stack as the main [`tessera-sdk`](https://github.com/tessera-llm/tessera-sdk). Same `tsr_…` API key works across both packages; same billing record.
- No LangChain dependency in the package itself. The config helpers return plain dicts / objects that you pass into the LangChain ChatModel constructor of your choice. This keeps the install lightweight and lets us support new LangChain provider classes without lock-step releases.

### Companion releases

- `tessera-llm-proxy` / `@tessera-llm/sdk` v0.1.1 (the main Tessera SDK)
- Tessera proxy worker `0.42.0-m3-chars-capture` live at `api.tesseraai.io`
- Quality canary floor: 0.95 (per-stack), Composition cap: max 2 content-mutators per request

[Unreleased]: https://github.com/tessera-llm/tessera-langchain/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/tessera-llm/tessera-langchain/releases/tag/v0.1.0
