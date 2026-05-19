/**
 * openai-langchain.ts — ChatOpenAI through the Tessera proxy.
 *
 * Usage:
 *
 *   npm install @tessera-llm/langchain @langchain/openai @langchain/core
 *   export OPENAI_API_KEY=sk-...
 *   export TESSERA_API_KEY=tsr_...
 *   npx tsx openai-langchain.ts
 */

import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage, SystemMessage } from "@langchain/core/messages";

import { tesseraOpenAIConfig } from "@tessera-llm/langchain";

async function main(): Promise<void> {
  const openaiKey = process.env.OPENAI_API_KEY;
  const tesseraKey = process.env.TESSERA_API_KEY;
  if (!openaiKey || !tesseraKey) {
    throw new Error("Set OPENAI_API_KEY and TESSERA_API_KEY before running.");
  }

  const llm = new ChatOpenAI({
    model: "gpt-4o",
    apiKey: openaiKey,
    ...tesseraOpenAIConfig({ apiKey: tesseraKey }),
  });

  const response = await llm.invoke([
    new SystemMessage(
      "You are a senior platform engineer reviewing infrastructure decisions. " +
        "Answer in 3 concise bullets."
    ),
    new HumanMessage(
      "Compare a service mesh sidecar approach vs an eBPF-based approach " +
        "for east-west traffic policy enforcement."
    ),
  ]);

  console.log(response.content);
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
