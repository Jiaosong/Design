import type { Env } from "./types";

interface EmbeddingResponse {
  data?: number[][];
  shape?: number[];
}

export async function embedTexts(env: Env, texts: string[]): Promise<number[][]> {
  if (texts.length === 0) return [];
  const response = (await env.AI.run(env.EMBEDDING_MODEL as keyof AiModels, { text: texts })) as EmbeddingResponse;
  if (!Array.isArray(response.data) || response.data.length !== texts.length) {
    throw new Error(`Embedding response mismatch: expected ${texts.length}, received ${response.data?.length ?? 0}`);
  }
  const expectedDimensions = Number.parseInt(env.EMBEDDING_DIMENSIONS, 10);
  for (const vector of response.data) {
    if (!Array.isArray(vector) || vector.length !== expectedDimensions) {
      throw new Error(`Embedding dimension mismatch: expected ${expectedDimensions}, received ${vector?.length ?? 0}`);
    }
  }
  return response.data;
}
