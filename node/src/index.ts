/**
 * @tessera-llm/langchain — drop-in cost optimization for LangChain.js ChatModels.
 *
 * Two API surfaces:
 *
 *   1. tesseraOpenAIConfig(apiKey) / tesseraAnthropicConfig(apiKey) / ...
 *      Returns the constructor options dict for the corresponding
 *      LangChain.js ChatModel. Pass-through pattern, recommended for
 *      new code paths.
 *
 *      Example:
 *        import { ChatOpenAI } from "@langchain/openai";
 *        import { tesseraOpenAIConfig } from "@tessera-llm/langchain";
 *
 *        const llm = new ChatOpenAI({
 *          model: "gpt-4o",
 *          apiKey: process.env.OPENAI_API_KEY,
 *          ...tesseraOpenAIConfig({ apiKey: process.env.TESSERA_API_KEY! }),
 *        });
 *
 *   2. wrapOpenAI(model, apiKey) / wrapAnthropic(model, apiKey) / ...
 *      Take an existing ChatModel instance and return a new one routed
 *      through Tessera. Convenience for retrofitting existing pipelines.
 *
 * See https://tesseraai.io/dev for the dashboard, free tier, and full
 * mechanic documentation.
 */

export const TESSERA_BASE_URL = "https://api.tesseraai.io";
export const VERSION = "0.1.0";

export type ProviderName =
  | "openai"
  | "anthropic"
  | "mistral"
  | "groq"
  | "cohere";

export interface TesseraConfigInput {
  apiKey: string;
  extraHeaders?: Record<string, string>;
  baseUrl?: string;
}

function validateApiKey(apiKey: string): string {
  if (typeof apiKey !== "string" || apiKey.length === 0) {
    throw new Error(
      "tessera*Config({ apiKey }) requires a non-empty string. " +
        "Get a free key from https://tesseraai.io/dev"
    );
  }
  return apiKey;
}

function proxyEndpoint(provider: ProviderName): string {
  return `${TESSERA_BASE_URL}/v1/${provider}`;
}

function buildHeaders(
  apiKey: string,
  extra?: Record<string, string>
): Record<string, string> {
  return { ...(extra ?? {}), "x-tessera-api-key": apiKey };
}

// ── Config functions (pass-through pattern) ─────────────────────────────

/**
 * Constructor options for ChatOpenAI to route through the Tessera proxy.
 */
export function tesseraOpenAIConfig(
  input: TesseraConfigInput
): {
  configuration: { baseURL: string; defaultHeaders: Record<string, string> };
} {
  const apiKey = validateApiKey(input.apiKey);
  return {
    configuration: {
      baseURL: input.baseUrl ?? proxyEndpoint("openai"),
      defaultHeaders: buildHeaders(apiKey, input.extraHeaders),
    },
  };
}

/**
 * Constructor options for ChatAnthropic to route through the Tessera proxy.
 */
export function tesseraAnthropicConfig(
  input: TesseraConfigInput
): {
  anthropicApiUrl: string;
  clientOptions: { defaultHeaders: Record<string, string> };
} {
  const apiKey = validateApiKey(input.apiKey);
  return {
    anthropicApiUrl: input.baseUrl ?? proxyEndpoint("anthropic"),
    clientOptions: {
      defaultHeaders: buildHeaders(apiKey, input.extraHeaders),
    },
  };
}

/**
 * Constructor options for ChatMistralAI to route through the Tessera proxy.
 */
export function tesseraMistralConfig(
  input: TesseraConfigInput
): {
  endpoint: string;
  defaultHeaders: Record<string, string>;
} {
  const apiKey = validateApiKey(input.apiKey);
  return {
    endpoint: input.baseUrl ?? proxyEndpoint("mistral"),
    defaultHeaders: buildHeaders(apiKey, input.extraHeaders),
  };
}

/**
 * Constructor options for ChatGroq to route through the Tessera proxy.
 */
export function tesseraGroqConfig(
  input: TesseraConfigInput
): {
  baseUrl: string;
  defaultHeaders: Record<string, string>;
} {
  const apiKey = validateApiKey(input.apiKey);
  return {
    baseUrl: input.baseUrl ?? proxyEndpoint("groq"),
    defaultHeaders: buildHeaders(apiKey, input.extraHeaders),
  };
}

/**
 * Constructor options for ChatCohere to route through the Tessera proxy.
 */
export function tesseraCohereConfig(
  input: TesseraConfigInput
): {
  clientOptions: { baseUrl: string; defaultHeaders: Record<string, string> };
} {
  const apiKey = validateApiKey(input.apiKey);
  return {
    clientOptions: {
      baseUrl: input.baseUrl ?? proxyEndpoint("cohere"),
      defaultHeaders: buildHeaders(apiKey, input.extraHeaders),
    },
  };
}

/**
 * Generic dispatcher — returns the right kwargs object for the given provider.
 * Useful when the provider is selected at runtime.
 */
export function tesseraConfig(
  provider: ProviderName,
  input: TesseraConfigInput
): Record<string, unknown> {
  switch (provider) {
    case "openai":
      return tesseraOpenAIConfig(input);
    case "anthropic":
      return tesseraAnthropicConfig(input);
    case "mistral":
      return tesseraMistralConfig(input);
    case "groq":
      return tesseraGroqConfig(input);
    case "cohere":
      return tesseraCohereConfig(input);
    default: {
      const _exhaustive: never = provider;
      throw new Error(
        `Unknown provider ${_exhaustive}. Supported: openai, anthropic, mistral, groq, cohere`
      );
    }
  }
}

// ── Wrap functions (convenience for existing instances) ─────────────────

/**
 * Minimal shape of a LangChain.js ChatModel instance we need to wrap.
 * Both classical (lc_kwargs) and modern (direct field) shapes are
 * supported; we read whichever fields are present and call the
 * constructor of the input's `constructor` with the merged overrides.
 */
interface ChatModelLike {
  // The constructor reference — we instantiate a new model via `new this.constructor(merged)`.
  constructor: new (fields: Record<string, unknown>) => unknown;
  // Any fields the LangChain ChatModel exposes; the wrap helpers do not
  // strictly type these because LangChain models differ per provider.
  [key: string]: unknown;
}

function mergeHeaders(
  existing: unknown,
  added: Record<string, string>
): Record<string, string> {
  const existingDict =
    existing && typeof existing === "object"
      ? (existing as Record<string, string>)
      : {};
  return { ...existingDict, ...added };
}

function rebuild<T extends ChatModelLike>(
  model: T,
  overrides: Record<string, unknown>
): T {
  // LangChain models are constructed from a plain object. We can clone by
  // spreading the visible fields + overrides into the same constructor.
  // This works for ChatOpenAI / ChatAnthropic / ChatMistralAI / ChatGroq /
  // ChatCohere because all of them accept their full options dict.
  const Ctor = model.constructor as new (fields: Record<string, unknown>) => T;
  const baseFields: Record<string, unknown> = {};
  for (const key of Object.keys(model)) {
    baseFields[key] = (model as Record<string, unknown>)[key];
  }
  return new Ctor({ ...baseFields, ...overrides });
}

export function wrapOpenAI<T extends ChatModelLike>(
  model: T,
  tesseraApiKey: string
): T {
  const cfg = tesseraOpenAIConfig({ apiKey: tesseraApiKey });
  return rebuild(model, {
    configuration: {
      ...((model.configuration as Record<string, unknown>) ?? {}),
      baseURL: cfg.configuration.baseURL,
      defaultHeaders: mergeHeaders(
        (model.configuration as { defaultHeaders?: unknown })?.defaultHeaders,
        cfg.configuration.defaultHeaders
      ),
    },
  });
}

export function wrapAnthropic<T extends ChatModelLike>(
  model: T,
  tesseraApiKey: string
): T {
  const cfg = tesseraAnthropicConfig({ apiKey: tesseraApiKey });
  return rebuild(model, {
    anthropicApiUrl: cfg.anthropicApiUrl,
    clientOptions: {
      ...((model.clientOptions as Record<string, unknown>) ?? {}),
      defaultHeaders: mergeHeaders(
        (model.clientOptions as { defaultHeaders?: unknown })?.defaultHeaders,
        cfg.clientOptions.defaultHeaders
      ),
    },
  });
}

export function wrapMistral<T extends ChatModelLike>(
  model: T,
  tesseraApiKey: string
): T {
  const cfg = tesseraMistralConfig({ apiKey: tesseraApiKey });
  return rebuild(model, {
    endpoint: cfg.endpoint,
    defaultHeaders: mergeHeaders(model.defaultHeaders, cfg.defaultHeaders),
  });
}

export function wrapGroq<T extends ChatModelLike>(
  model: T,
  tesseraApiKey: string
): T {
  const cfg = tesseraGroqConfig({ apiKey: tesseraApiKey });
  return rebuild(model, {
    baseUrl: cfg.baseUrl,
    defaultHeaders: mergeHeaders(model.defaultHeaders, cfg.defaultHeaders),
  });
}

export function wrapCohere<T extends ChatModelLike>(
  model: T,
  tesseraApiKey: string
): T {
  const cfg = tesseraCohereConfig({ apiKey: tesseraApiKey });
  return rebuild(model, {
    clientOptions: {
      ...((model.clientOptions as Record<string, unknown>) ?? {}),
      baseUrl: cfg.clientOptions.baseUrl,
      defaultHeaders: mergeHeaders(
        (model.clientOptions as { defaultHeaders?: unknown })?.defaultHeaders,
        cfg.clientOptions.defaultHeaders
      ),
    },
  });
}
