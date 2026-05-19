# Contributing to tessera-langchain

Thanks for your interest. The package is Apache-2.0 licensed and PRs are welcome.

For the canonical contributing rules (style, what we want, what we don't want,
PR review expectations) see
[`tessera-llm/tessera-sdk/CONTRIBUTING.md`](https://github.com/tessera-llm/tessera-sdk/blob/main/CONTRIBUTING.md).
This file documents the package-specific bits.

## Reporting bugs

Open an issue at
[github.com/tessera-llm/tessera-langchain/issues](https://github.com/tessera-llm/tessera-langchain/issues)
with:

- Package version (`pip show tessera-langchain` for Python, `npm list @tessera-llm/langchain` for Node)
- LangChain version (`pip show langchain langchain-openai langchain-anthropic` etc.)
- Language runtime version
- Minimum reproduction snippet
- Expected vs. actual behaviour

For security vulnerabilities, see [`SECURITY.md`](./SECURITY.md) — please do
not file public issues.

## Development setup

This repo carries two parallel implementations — Python and Node — sharing
the same wire format against the Tessera proxy.

### Python

```bash
cd python
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

### Node / TypeScript

```bash
cd node
npm install
npm test
npm run build
```

The CI workflow under `.github/workflows/` runs the same checks on every
push and pull request — keep it green.

## Package-specific scope

LangChain ships many integration packages (`langchain-openai`,
`langchain-anthropic`, `langchain-mistralai`, `langchain-groq`,
`langchain-cohere` on Python; `@langchain/openai` etc. on Node). The
Tessera wrapper exposes a single `with_tessera(...)` helper that
patches a chat model with the proxy base URL + Tessera key header.
Keep new chat-model wrappers tiny — one helper per upstream provider,
no business logic inside the wrapper.

## Contact

- Bug reports: GitHub Issues.
- Security: [security@tesseraai.io](mailto:security@tesseraai.io).
- Code of Conduct enforcement: [conduct@tesseraai.io](mailto:conduct@tesseraai.io).
- General: [founder@tesseraai.io](mailto:founder@tesseraai.io).
