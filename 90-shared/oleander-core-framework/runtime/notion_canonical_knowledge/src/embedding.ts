import { estimateTokens } from "./chunker";
import { EMBEDDING_BATCH_MAX_ESTIMATED_TOKENS } from "./config";
import type { Env } from "./types";

interface EmbeddingResponse {
  data?: number[][];
  shape?: number[];
}

function isContextLimitError(error: unknown): boolean {
  const message = error instanceof Error ? error.message : String(error);
  return /(?:3030:)?\s*Max context reached|model supports only \d+/i.test(message);
}

async function embedBatch(env: Env, batch: string[], expectedDimensions: number): Promise<number[][]> {
  try {
    const response = (await env.AI.run(env.EMBEDDING_MODEL as keyof AiModels, { text: batch })) as EmbeddingResponse;
    if (!Array.isArray(response.data) || response.data.length !== batch.length) {
      throw new Error(`Embedding response mismatch: expected ${batch.length}, received ${response.data?.length ?? 0}`);
    }
    for (const vector of response.data) {
      if (!Array.isArray(vector) || vector.length !== expectedDimensions) {
        throw new Error(`Embedding dimension mismatch: expected ${expectedDimensions}, received ${vector?.length ?? 0}`);
      }
    }
    return response.data;
  } catch (error) {
    if (!isContextLimitError(error) || batch.length <= 1) throw error;
    const midpoint = Math.ceil(batch.length / 2);
    const left = await embedBatch(env, batch.slice(0, midpoint), expectedDimensions);
    const right = await embedBatch(env, batch.slice(midpoint), expectedDimensions);
    return [...left, ...right];
  }
}

export function embeddingBatches(texts: string[]): string[][] {
  const batches: string[][] = [];
  let current: string[] = [];
  let currentTokens = 0;

  for (const text of texts) {
    const estimatedTokens = estimateTokens(text);
    if (current.length > 0 && currentTokens + estimatedTokens > EMBEDDING_BATCH_MAX_ESTIMATED_TOKENS) {
      batches.push(current);
      current = [];
      currentTokens = 0;
    }
    current.push(text);
    currentTokens += estimatedTokens;
  }
  if (current.length > 0) batches.push(current);
  return batches;
}

export async function embedTexts(env: Env, texts: string[]): Promise<number[][]> {
  if (texts.length === 0) return [];
  const expectedDimensions = Number.parseInt(env.EMBEDDING_DIMENSIONS, 10);
  const vectors: number[][] = [];
  for (const batch of embeddingBatches(texts)) {
    vectors.push(...(await embedBatch(env, batch, expectedDimensions)));
  }
  if (vectors.length !== texts.length) {
    throw new Error(`Embedding aggregate mismatch: expected ${texts.length}, received ${vectors.length}`);
  }
  return vectors;
}
