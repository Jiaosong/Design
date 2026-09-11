import { estimateTokens } from "./chunker";
import { EMBEDDING_BATCH_MAX_ESTIMATED_TOKENS } from "./config";
import type { Env } from "./types";

interface EmbeddingResponse {
  data?: number[][];
  shape?: number[];
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
    const response = (await env.AI.run(env.EMBEDDING_MODEL as keyof AiModels, { text: batch })) as EmbeddingResponse;
    if (!Array.isArray(response.data) || response.data.length !== batch.length) {
      throw new Error(`Embedding response mismatch: expected ${batch.length}, received ${response.data?.length ?? 0}`);
    }
    for (const vector of response.data) {
      if (!Array.isArray(vector) || vector.length !== expectedDimensions) {
        throw new Error(`Embedding dimension mismatch: expected ${expectedDimensions}, received ${vector?.length ?? 0}`);
      }
      vectors.push(vector);
    }
  }
  if (vectors.length !== texts.length) {
    throw new Error(`Embedding aggregate mismatch: expected ${texts.length}, received ${vectors.length}`);
  }
  return vectors;
}
