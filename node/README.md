# @tessera-llm/langchain

[![npm version](https://img.shields.io/npm/v/@tessera-llm/langchain.svg)](https://www.npmjs.com/package/@tessera-llm/langchain)

**Drop-in cost optimization for LangChain.js ChatModels.** One line of config in your existing `ChatOpenAI` / `ChatAnthropic` / `ChatMistralAI` / `ChatGroq` / `ChatCohere` constructor routes your traffic through the [Tessera](https://tesseraai.io) proxy — auto-route, exact + provider-prompt-cache hits, per-role compression, output-length ceiling, batch arbitrage. Free Dev tier: **60M tokens/month, no card**. Production: **20% of measured savings, $0 if we save you nothing**.

Companion package to [`@tessera-llm/sdk`](https://www.npmjs.com/package/@tessera-llm/sdk) — same proxy, LangChain-shaped API.

## Install

```bash
npm install @tessera-llm/langchain
```

## Quickstart

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { tesseraOpenAIConfig } from "@tessera-llm/langchain";

const llm = new ChatOpenAI({
  model: "gpt-4o",
  apiKey: process.env.OPENAI_API_KEY!,
  ...tesseraOpenAIConfig({ apiKey: process.env.TESSERA_API_KEY! }),
});

// Existing LangChain code (chains, agents, tools, streaming) runs unchanged.
const response = await llm.invoke("Summarize a Kubernetes operator architecture in 3 bullets.");
```

Same pattern for the other providers — `tesseraAnthropicConfig`, `tesseraMistralConfig`, `tesseraGroqConfig`, `tesseraCohereConfig`.

Or wrap an existing instance:

```typescript
import { wrapOpenAI } from "@tessera-llm/langchain";

const llm = wrapOpenAI(myExistingChatOpenAI, process.env.TESSERA_API_KEY!);
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
