# `tessera-langchain`

**Drop-in cost optimization for LangChain.** One line of config routes your existing `ChatOpenAI` / `ChatAnthropic` / `ChatMistralAI` / `ChatGroq` / `ChatCohere` through the [Tessera](https://tesseraai.io) optimization proxy — auto-route to cheaper-equivalent models, exact + provider-prompt-cache hits, prompt compression with per-stack quality canary, batch arbitrage on async-tolerant calls. Free Dev tier: **60M tokens/month, no card**. Production: **20% of measured savings, $0 if we save you nothing**.

<!-- COMPANION-PACKAGES-START -->
Companion to [`tessera-sdk`](https://github.com/tessera-llm/tessera-sdk) (vanilla provider SDKs), [`tessera-vercel-ai`](https://github.com/tessera-llm/tessera-vercel-ai) (Vercel AI SDK integration), [`tessera-llamaindex`](https://github.com/tessera-llm/tessera-llamaindex) (LlamaIndex integration), [`tessera-mastra`](https://www.npmjs.com/package/@tessera-llm/mastra) (Mastra Agent framework integration), [`tessera-pydantic-ai`](https://pypi.org/project/tessera-pydantic-ai/) (Pydantic AI integration), [`tessera-crewai`](https://pypi.org/project/tessera-crewai/) (CrewAI multi-agent integration), and [`tessera-autogen`](https://pypi.org/project/tessera-autogen/) (AutoGen 0.4+ multi-agent integration). Same proxy, same mechanic stack, LangChain-shaped API.
<!-- COMPANION-PACKAGES-END -->

[![PyPI version](https://img.shields.io/pypi/v/tessera-langchain.svg)](https://pypi.org/project/tessera-langchain/) [![npm version](https://img.shields.io/npm/v/@tessera-llm/langchain.svg)](https://www.npmjs.com/package/@tessera-llm/langchain) [![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

---

## What it looks like

Worked example, customer-support agent on `gpt-4o`, 5B tokens/month:

| Stage | Cost / month | Saved |
|---|---:|---:|
| Baseline — OpenAI direct | $24,000 | — |
| + Tessera (route, cache, prompt-cache headers, compress, output-length ceiling, batch) | $9,400 | $14,600 |
| Tessera fee (20% × savings) | $2,920 | — |
| **You net pay** | **$12,320** | **$11,680 / mo saved** |

Quality canary across the full mechanic stack: mean-score 0.96 (floor 0.95) — 0.95 SLA held all 30 days. Full walkthrough on [`/blog/cut-openai-bill-38-percent-without-quality-regression`](https://tesseraai.io/blog/cut-openai-bill-38-percent-without-quality-regression).

---

## Install

```bash
pip install tessera-langchain          # Python
npm install @tessera-llm/langchain     # Node / TypeScript
```

Get a free API key (60M tokens/mo, no card) — [`tesseraai.io/dev`](https://tesseraai.io/dev). Sign-up takes about 30 seconds and returns an instant `tk_…` key plus magic-link dashboard access.

---

## Quickstart — Python

```python
from langchain_openai import ChatOpenAI
from tessera_langchain import tessera_openai_config

llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key="sk-...",                          # your OpenAI key, unchanged
    **tessera_openai_config(api_key="tk_..."),       # one line, routes through Tessera
)

# Existing LangChain code runs unchanged.
response = llm.invoke("Summarize the architecture of a Kubernetes operator in 3 bullets.")
```

Same pattern for the other providers:

```python
from langchain_anthropic import ChatAnthropic
from tessera_langchain import tessera_anthropic_config

llm = ChatAnthropic(
    model="claude-sonnet-4-5-20250929",
    anthropic_api_key="sk-ant-...",
    **tessera_anthropic_config(api_key="tk_..."),
)
```

Or wrap an existing ChatModel instance instead:

```python
from langchain_openai import ChatOpenAI
from tessera_langchain import wrap_openai

base = ChatOpenAI(model="gpt-4o", openai_api_key="sk-...")
llm = wrap_openai(base, tessera_api_key="tk_...")    # returns a new ChatOpenAI routed through Tessera
```

---

## Quickstart — TypeScript / Node

```ts
import { ChatOpenAI } from "@langchain/openai";
import { tesseraOpenAIConfig } from "@tessera-llm/langchain";

const llm = new ChatOpenAI({
  model: "gpt-4o",
  apiKey: process.env.OPENAI_API_KEY!,                // your OpenAI key, unchanged
  ...tesseraOpenAIConfig({ apiKey: process.env.TESSERA_API_KEY! }),
});

const response = await llm.invoke(
  "Summarize the architecture of a Kubernetes operator in 3 bullets."
);
```

Anthropic / Mistral / Groq / Cohere mirror the same shape — see `examples/`.

Wrap an existing instance:

```ts
import { ChatOpenAI } from "@langchain/openai";
import { wrapOpenAI } from "@tessera-llm/langchain";

const base = new ChatOpenAI({ model: "gpt-4o", apiKey: process.env.OPENAI_API_KEY! });
const llm = wrapOpenAI(base, process.env.TESSERA_API_KEY!);
```

---

## What Tessera does on every request

Same mechanic stack as the main [`tessera-sdk`](https://github.com/tessera-llm/tessera-sdk). Each mechanic is opt-in per workload, observable per request, and bypasses when its quality canary drops below the per-stack 0.95 floor.

| Mechanic | What it does | Typical savings |
|---|---|---|
| **Auto-route** <sub>(m1)</sub> | Route to a cheaper-equivalent model gated by a daily promptfoo canary on your eval set | 15–35% on routed calls |
| **Auto-cache** <sub>(m2)</sub> | sha256 cache on the canonical request body, 7-day TTL, Cloudflare edge KV | 5–40% depending on prompt repetition |
| **Auto-compress** <sub>(m3)</sub> | Per-role heuristic compression (system + user toggles independent). Preserves code fences and JSON shapes. | 5–15% on prompt tokens |
| **Prompt cache** <sub>(m6)</sub> | Inject provider-native cache headers — OpenAI cached-input (50% off), Anthropic `cache_control: ephemeral` (90% off cache reads) | 50–90% on cached prefixes |
| **Context prune** <sub>(m7)</sub> | Conservative trim on long conversations (system + last 8 turns; TF-IDF rerank on RAG attachments) | 5–25% on multi-turn workloads |
| **Output-length ceiling** <sub>(m9)</sub> | Daily compute fits p90 of completion length per workload, injects `max_tokens = p90 × 1.3` | 5–15% on completion cost |
| **Batch arbitrage** <sub>(m10)</sub> | Route async-tolerant calls to provider Batch APIs (OpenAI Batch + Anthropic Message Batches both 50% off) | 50% on batch-eligible traffic |
| **Per-provider circuit breaker** | (Reliability primitive, above the mechanics.) Rolling 5xx-rate state machine per upstream — when a provider degrades, auto-route skips its intra-provider alternative mappings until the half-open probe succeeds. [Details on /how-it-works](https://tesseraai.io/how-it-works). | n/a — keeps the savings stack honest |

---

## Supported providers

| Provider | LangChain class (Py) | LangChain.js class | Tessera proxy URL |
|---|---|---|---|
| OpenAI | `ChatOpenAI` | `ChatOpenAI` | `https://api.tesseraai.io/v1/openai` |
| Anthropic | `ChatAnthropic` | `ChatAnthropic` | `https://api.tesseraai.io/v1/anthropic` |
| Mistral | `ChatMistralAI` | `ChatMistralAI` | `https://api.tesseraai.io/v1/mistral` |
| Groq | `ChatGroq` | `ChatGroq` | `https://api.tesseraai.io/v1/groq` |
| Cohere | `ChatCohere` | `ChatCohere` | `https://api.tesseraai.io/v1/cohere` |

Other LangChain provider integrations can use the **OpenAI-compat** base URL by configuring `base_url=https://api.tesseraai.io/v1/openai` and `default_headers={"x-tessera-api-key": "tk_..."}` directly — works for anything that speaks the OpenAI wire format.

---

## Pricing

- **Free Dev** — 60M tokens/month, 30 requests/minute, all mechanics on, no card. Forever.
- **Production** — over 60M tokens/month or higher rate limit. **20% of measured savings only.** Zero savings, zero fee. Prepaid Stripe balance, $100 minimum top-up. No subscription, no commit, no minimum monthly.

Existing early customers of `tessera-sdk` keep their `rate_locked_pct` (25% Founding Pilot) on this package too — same `tk_…` key, same billing record.

---

## FAQ

### Q: How is this different from `tessera-sdk`?

Same proxy. Same mechanics. Same billing. `tessera-sdk` patches the underlying provider clients (OpenAI, Anthropic, Mistral, Groq, Cohere) directly. `tessera-langchain` plugs into the LangChain ChatModel constructor — useful when you're already on LangChain and want to keep the abstraction.

If you're on LangChain, install this one. If you're using the raw provider SDK without LangChain, install `tessera-sdk`. Both packages are safe to install side by side.

### Q: Does this break my existing eval / prompt template / RAG pipeline?

No. Your LangChain ChatModel object behaves identically — same `.invoke()`, same `.stream()`, same `.bind_tools()`, same `.with_structured_output()`. Only the upstream HTTP endpoint changes, and the response shape is the OpenAI / Anthropic / etc. wire format unchanged.

### Q: What happens if Tessera's proxy is down?

Your application gets HTTP errors instead of LLM responses. To passthrough on error, configure your LangChain `max_retries` to fall back to a non-Tessera client (we'll document this pattern explicitly in a future release). On the proxy side, a per-provider circuit breaker tracks rolling 5xx rates and skips degraded providers in auto-route decisions — cross-provider failover (re-routing to a different provider entirely when an upstream is down) is on the roadmap, not shipped yet.

### Q: What happens to my OpenAI / Anthropic rate limits?

They pass through. Tessera does not aggregate quotas across customers. Your provider rate limits apply normally; the proxy enforces only the Tessera tier limits (30 rpm Free Dev, 60 rpm Production by default — higher on request).

### Q: Are you storing my prompts and completions?

No. We log only token counts, cost deltas, mechanics_stack, and provider response status. Prompts and completions are never persisted. Full data handling on [`tesseraai.io/security`](https://tesseraai.io/security).

### Q: Can I see what each mechanic decided per request?

Yes — every request gets a row in `/portal/audit` showing the canonical mechanics_stack, the model that fired, the original vs actual cost, and the pricing_catalog snapshot id used. Export to CSV any time.

### Q: How do I disable a specific mechanic?

Per-workload in `/portal/settings`. Each mechanic has its own toggle. Per-role compression has independent toggles (compress system, compress user turns). Mechanics also auto-disable per-stack if the daily quality canary drops below 0.95 for the affected mechanic combination.

### Q: Is the LangChain integration officially supported by LangChain?

Tessera built and maintains this package. It uses public LangChain constructor APIs (no monkey-patching, no private imports). LangChain's own pluggability is what makes this clean.

---

## Examples

See `examples/`:

- [`openai-langchain.py`](./examples/openai-langchain.py) — ChatOpenAI through Tessera
- [`anthropic-langchain.py`](./examples/anthropic-langchain.py) — ChatAnthropic through Tessera
- [`openai-langchain.ts`](./examples/openai-langchain.ts) — TypeScript / LangChain.js

---

## Who this is for

- **AI-native teams** spending $5k+/month on OpenAI / Anthropic / Gemini and wanting that bill cut without re-architecting.
- **LangChain users** who do not want to swap to a different abstraction just to add an optimization proxy.
- **Production workloads** with eval sets — Tessera's mechanic stack only fires when the per-stack canary holds 0.95 quality. If you don't have an eval set yet, the Free Dev tier is the right place to start.

## Who this is NOT for

- Hobby projects under ~$500/month total bill — the Free Dev tier covers you; Production tier isn't worth the integration effort.
- Air-gapped / on-prem deployments — Tessera is hosted-only.
- Workloads with no repetition AND no stable prefix — exact cache and prompt-cache headers won't fire. Auto-route and batch arbitrage might still help; worth measuring on Free Dev first.
- High-latency-sensitivity workloads with <10ms p50 SLO — the proxy adds 15-25 ms p50 from the Cloudflare edge.

---

## Architecture

Open-source SDK ↔ closed-source proxy. This package is a thin client that adds one HTTP hop. The actual mechanic decisions (route, cache, compress, etc.) run inside the Tessera Cloudflare Worker proxy at `api.tesseraai.io`. The split is intentional: the wire format is open so you can audit what we send; the mechanic implementations are closed because that's the asymmetric IP. See the [`tessera-sdk` README's "Architecture" note](https://github.com/tessera-llm/tessera-sdk#architecture) for the longer explanation.

## License

Apache-2.0. See [LICENSE](LICENSE).

## Contributing

We accept PRs that:

- Add support for a new LangChain provider class (paste-and-mirror the existing config function shape)
- Improve typing precision (TypeScript strict, Python `mypy --strict`)
- Add concrete example scripts under `examples/` showing a real LangChain pipeline
- Improve tests or test infrastructure

We do **not** accept PRs that change the proxy's HTTP contract — that lives in the closed-source worker.

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) (TODO — same as `tessera-sdk` contributing guide).

## Versioning

Semver. Wire format compatibility committed across minor releases; breaking changes only on major bumps. Independent versioning from `tessera-sdk` (per-package CHANGELOG).

## Security

See [`SECURITY.md`](./SECURITY.md). Coordinated disclosure address: `security@tesseraai.io`.

---

## About Tessera

Tessera is the **substrate layer** for **LLM cost optimization**, also called the **Optimize Layer** in our product surface. A thin proxy that sits in your application's **request-path**, applies a conservative cascade of optimization mechanics, and measures every saved dollar against an **audit-immutable** baseline. We bill **20% of verified savings**, prepaid. Zero savings = zero fee. No per-token gateway fee, no subscription, no minimum monthly commitment; the category we operate in is "**success-fee LLM optimizer**," distinct from per-token **AI gateways** and observability dashboards.

Where observability tools tell you what you spent and AI gateways re-shape the request without measuring the cost delta, Tessera is the layer that does both, and only takes a cut when the measured savings are positive. The **verified-savings ledger** at [`ledger.tesseraai.io`](https://ledger.tesseraai.io) shows every original-vs-actual cost pair, snapshot-pinned to a `pricing_catalog` version captured at request time. Mid-contract price changes don't retroactively alter past savings. This is the **FinOps**-friendly model for AI inference: every line of the bill traces to a code-enforced rule.

Operated by Fintechagency OÜ (Tallinn, Estonia, registry code 16638667).

- Developer entry: [tesseraai.io/dev](https://tesseraai.io/dev)
- Mechanic reference: [tesseraai.io/how-it-works](https://tesseraai.io/how-it-works)
- Dashboard: [ledger.tesseraai.io](https://ledger.tesseraai.io)
- Engineering blog: [tesseraai.io/blog](https://tesseraai.io/blog)
