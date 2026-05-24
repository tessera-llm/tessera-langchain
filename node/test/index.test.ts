import { describe, it, expect } from "vitest";
import {
  TESSERA_BASE_URL,
  tesseraOpenAIConfig,
  tesseraAnthropicConfig,
  tesseraMistralConfig,
  tesseraGroqConfig,
  tesseraCohereConfig,
  tesseraConfig,
  wrapOpenAI,
  wrapAnthropic,
  wrapMistral,
  wrapGroq,
  wrapCohere,
} from "../src/index.js";

describe("tesseraOpenAIConfig", () => {
  it("returns the OpenAI proxy configuration", () => {
    const cfg = tesseraOpenAIConfig({ apiKey: "tk_test" });
    expect(cfg.configuration.baseURL).toBe(`${TESSERA_BASE_URL}/v1/openai`);
    expect(cfg.configuration.defaultHeaders).toEqual({
      "x-tessera-api-key": "tk_test",
    });
  });

  it("merges extra headers", () => {
    const cfg = tesseraOpenAIConfig({
      apiKey: "tk_test",
      extraHeaders: { "x-trace": "abc" },
    });
    expect(cfg.configuration.defaultHeaders).toEqual({
      "x-trace": "abc",
      "x-tessera-api-key": "tk_test",
    });
  });

  it("accepts a custom base URL override", () => {
    const cfg = tesseraOpenAIConfig({
      apiKey: "tk_test",
      baseUrl: "https://staging.tesseraai.io/v1/openai",
    });
    expect(cfg.configuration.baseURL).toBe(
      "https://staging.tesseraai.io/v1/openai"
    );
  });
});

describe("tesseraAnthropicConfig", () => {
  it("returns the Anthropic proxy configuration", () => {
    const cfg = tesseraAnthropicConfig({ apiKey: "tk_test" });
    expect(cfg.anthropicApiUrl).toBe(`${TESSERA_BASE_URL}/v1/anthropic`);
    expect(cfg.clientOptions.defaultHeaders).toEqual({
      "x-tessera-api-key": "tk_test",
    });
  });
});

describe("tesseraMistralConfig", () => {
  it("returns the Mistral proxy configuration", () => {
    const cfg = tesseraMistralConfig({ apiKey: "tk_test" });
    expect(cfg.endpoint).toBe(`${TESSERA_BASE_URL}/v1/mistral`);
    expect(cfg.defaultHeaders).toEqual({ "x-tessera-api-key": "tk_test" });
  });
});

describe("tesseraGroqConfig", () => {
  it("returns the Groq proxy configuration", () => {
    const cfg = tesseraGroqConfig({ apiKey: "tk_test" });
    expect(cfg.baseUrl).toBe(`${TESSERA_BASE_URL}/v1/groq`);
    expect(cfg.defaultHeaders).toEqual({ "x-tessera-api-key": "tk_test" });
  });
});

describe("tesseraCohereConfig", () => {
  it("returns the Cohere proxy configuration", () => {
    const cfg = tesseraCohereConfig({ apiKey: "tk_test" });
    expect(cfg.clientOptions.baseUrl).toBe(`${TESSERA_BASE_URL}/v1/cohere`);
    expect(cfg.clientOptions.defaultHeaders).toEqual({
      "x-tessera-api-key": "tk_test",
    });
  });
});

describe("tesseraConfig (generic dispatcher)", () => {
  it("routes openai", () => {
    const cfg = tesseraConfig("openai", { apiKey: "tk_test" }) as ReturnType<
      typeof tesseraOpenAIConfig
    >;
    expect(cfg.configuration.baseURL).toBe(`${TESSERA_BASE_URL}/v1/openai`);
  });

  it("routes anthropic", () => {
    const cfg = tesseraConfig("anthropic", { apiKey: "tk_test" }) as ReturnType<
      typeof tesseraAnthropicConfig
    >;
    expect(cfg.anthropicApiUrl).toBe(`${TESSERA_BASE_URL}/v1/anthropic`);
  });

  it("rejects unknown provider", () => {
    expect(() =>
      // @ts-expect-error — intentional invalid provider
      tesseraConfig("unknown", { apiKey: "tk_test" })
    ).toThrow(/Unknown provider/);
  });
});

describe("input validation", () => {
  it("rejects empty apiKey", () => {
    expect(() => tesseraOpenAIConfig({ apiKey: "" })).toThrow(/non-empty/);
  });

  it("rejects non-string apiKey", () => {
    expect(() =>
      // @ts-expect-error — intentional invalid input
      tesseraOpenAIConfig({ apiKey: null })
    ).toThrow(/non-empty/);
  });
});

// ── Wrap helpers ────────────────────────────────────────────────────────

class StubOpenAILike {
  modelName: string;
  configuration?: { baseURL?: string; defaultHeaders?: Record<string, string> };

  constructor(fields: Record<string, unknown> = {}) {
    this.modelName = (fields.modelName as string) ?? "gpt-4o";
    this.configuration = fields.configuration as
      | { baseURL?: string; defaultHeaders?: Record<string, string> }
      | undefined;
  }
}

class StubAnthropicLike {
  modelName: string;
  anthropicApiUrl?: string;
  clientOptions?: { defaultHeaders?: Record<string, string> };

  constructor(fields: Record<string, unknown> = {}) {
    this.modelName = (fields.modelName as string) ?? "claude-sonnet-4-5";
    this.anthropicApiUrl = fields.anthropicApiUrl as string | undefined;
    this.clientOptions = fields.clientOptions as
      | { defaultHeaders?: Record<string, string> }
      | undefined;
  }
}

class StubMistralLike {
  modelName: string;
  endpoint?: string;
  defaultHeaders?: Record<string, string>;

  constructor(fields: Record<string, unknown> = {}) {
    this.modelName = (fields.modelName as string) ?? "mistral-large";
    this.endpoint = fields.endpoint as string | undefined;
    this.defaultHeaders = fields.defaultHeaders as
      | Record<string, string>
      | undefined;
  }
}

class StubGroqLike {
  modelName: string;
  baseUrl?: string;
  defaultHeaders?: Record<string, string>;

  constructor(fields: Record<string, unknown> = {}) {
    this.modelName = (fields.modelName as string) ?? "llama-3.3-70b";
    this.baseUrl = fields.baseUrl as string | undefined;
    this.defaultHeaders = fields.defaultHeaders as
      | Record<string, string>
      | undefined;
  }
}

class StubCohereLike {
  modelName: string;
  clientOptions?: { baseUrl?: string; defaultHeaders?: Record<string, string> };

  constructor(fields: Record<string, unknown> = {}) {
    this.modelName = (fields.modelName as string) ?? "command-r-plus";
    this.clientOptions = fields.clientOptions as
      | { baseUrl?: string; defaultHeaders?: Record<string, string> }
      | undefined;
  }
}

describe("wrapOpenAI", () => {
  it("overrides baseURL and injects header", () => {
    const base = new StubOpenAILike() as unknown as Parameters<typeof wrapOpenAI>[0];
    const wrapped = wrapOpenAI(base, "tk_test");
    const cfg = (wrapped as unknown as StubOpenAILike).configuration;
    expect(cfg?.baseURL).toBe(`${TESSERA_BASE_URL}/v1/openai`);
    expect(cfg?.defaultHeaders).toEqual({ "x-tessera-api-key": "tk_test" });
  });

  it("merges existing default headers", () => {
    const base = new StubOpenAILike({
      configuration: { defaultHeaders: { "x-app": "my-app" } },
    }) as unknown as Parameters<typeof wrapOpenAI>[0];
    const wrapped = wrapOpenAI(base, "tk_test");
    const cfg = (wrapped as unknown as StubOpenAILike).configuration;
    expect(cfg?.defaultHeaders).toEqual({
      "x-app": "my-app",
      "x-tessera-api-key": "tk_test",
    });
  });
});

describe("wrapAnthropic", () => {
  it("overrides anthropicApiUrl and injects header", () => {
    const base = new StubAnthropicLike() as unknown as Parameters<
      typeof wrapAnthropic
    >[0];
    const wrapped = wrapAnthropic(base, "tk_test");
    const w = wrapped as unknown as StubAnthropicLike;
    expect(w.anthropicApiUrl).toBe(`${TESSERA_BASE_URL}/v1/anthropic`);
    expect(w.clientOptions?.defaultHeaders).toEqual({
      "x-tessera-api-key": "tk_test",
    });
  });
});

describe("wrapMistral", () => {
  it("overrides endpoint and injects header", () => {
    const base = new StubMistralLike() as unknown as Parameters<
      typeof wrapMistral
    >[0];
    const wrapped = wrapMistral(base, "tk_test");
    const w = wrapped as unknown as StubMistralLike;
    expect(w.endpoint).toBe(`${TESSERA_BASE_URL}/v1/mistral`);
    expect(w.defaultHeaders).toEqual({ "x-tessera-api-key": "tk_test" });
  });
});

describe("wrapGroq", () => {
  it("overrides baseUrl and injects header", () => {
    const base = new StubGroqLike() as unknown as Parameters<typeof wrapGroq>[0];
    const wrapped = wrapGroq(base, "tk_test");
    const w = wrapped as unknown as StubGroqLike;
    expect(w.baseUrl).toBe(`${TESSERA_BASE_URL}/v1/groq`);
    expect(w.defaultHeaders).toEqual({ "x-tessera-api-key": "tk_test" });
  });
});

describe("wrapCohere", () => {
  it("overrides baseUrl in clientOptions", () => {
    const base = new StubCohereLike() as unknown as Parameters<
      typeof wrapCohere
    >[0];
    const wrapped = wrapCohere(base, "tk_test");
    const w = wrapped as unknown as StubCohereLike;
    expect(w.clientOptions?.baseUrl).toBe(`${TESSERA_BASE_URL}/v1/cohere`);
  });
});
