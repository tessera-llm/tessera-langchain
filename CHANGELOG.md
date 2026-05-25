# Changelog

All notable changes to `tessera-langchain` (Python) and `@tessera-llm/langchain` (Node / TypeScript) will be documented here.

This file follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The Python and Node packages share a single CHANGELOG and are versioned together — same release tag triggers both PyPI and npm publishes.

## [Unreleased]

## [0.1.1] -- 2026-05-25

### Fixed
- Consolidated API key prefix to `tk_` across documentation and test fixtures.
- Aligned free-tier terminology on `Free Sandbox`.
- Blog cross-link slug 38 -> 48 .

### Changed
- Companion-cross-link block refreshed for 4 new sibling repos.
### Added

- `examples/mistral-langchain.py`, `examples/groq-langchain.py`,
  `examples/cohere-langchain.py` — fills the coverage gap (only OpenAI +
  Anthropic had examples before).
- `node/LICENSE` — Apache-2.0 verbatim alongside `node/package.json`
  files-array entry (per Apache §4.1 redistribution requirement).
- `.github/dependabot.yml`, `.github/ISSUE_TEMPLATE/bug_report.yml` +
  `feature_request.yml`, `.github/PULL_REQUEST_TEMPLATE.md` — mirrored
  from `tessera-sdk` canonical templates.

### Changed

- README cross-link block extended to include all 7 sibling packages
  (added `tessera-mastra`, `tessera-pydantic-ai`, `tessera-crewai`,
  `tessera-autogen` — bringing the roster to 7 framework surfaces).
  Monorepo packages link to PyPI / npm registry pages rather than
  non-existent GitHub repos.
- README mechanic-table rows referring to bare `M9` / `M2` / `M6`
  M-codes in prose softened to descriptive labels per the diagnostic-
  vocab discipline. `<sub>(m1)</sub>` reference tags in the technical
  table preserved (audit-log reconciliation surface, allowed per
  hybrid-policy).

### Fixed

- README "Security" line stripped the stale `(TODO)` marker now that
  `SECURITY.md` exists alongside CODE_OF_CONDUCT + CONTRIBUTING (added
  earlier in this session, commit `c81d0f7`).

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
- Same proxy + mechanic stack as the main [`tessera-sdk`](https://github.com/tessera-llm/tessera-sdk). Same `tk_…` API key works across both packages; same billing record.
- No LangChain dependency in the package itself. The config helpers return plain dicts / objects that you pass into the LangChain ChatModel constructor of your choice. This keeps the install lightweight and lets us support new LangChain provider classes without lock-step releases.

### Companion releases

- `tessera-llm-proxy` / `@tessera-llm/sdk` v0.1.1 (the main Tessera SDK)
- Tessera proxy worker `0.42.0-m3-chars-capture` live at `api.tesseraai.io`
- Quality canary floor: 0.95 (per-stack), Composition cap: max 2 content-mutators per request

[Unreleased]: https://github.com/tessera-llm/tessera-langchain/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/tessera-llm/tessera-langchain/releases/tag/v0.1.0
