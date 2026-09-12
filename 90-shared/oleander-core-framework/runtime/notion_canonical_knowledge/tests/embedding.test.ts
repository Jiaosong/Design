import { describe, expect, it, vi } from "vitest";
import { estimateTokens } from "../src/chunker";
import { EMBEDDING_BATCH_MAX_ESTIMATED_TOKENS } from "../src/config";
import { embeddingBatches, embedTexts } from "../src/embedding";
import type { Env } from "../src/types";

describe("embedding batching", () => {
  it("splits request-level context while preserving every input", () => {
    const oneTokenLike = "a".repeat(4);
    const texts = Array.from({ length: EMBEDDING_BATCH_MAX_ESTIMATED_TOKENS + 10 }, () => oneTokenLike);
    const batches = embeddingBatches(texts);
    expect(batches.length).toBe(2);
    expect(batches.flat()).toEqual(texts);
  });

  it("keeps every estimated batch below the conservative request budget", () => {
    const texts = Array.from({ length: 300 }, (_, index) => `标题${index}:${"混合Text内容".repeat(80)}`);
    const batches = embeddingBatches(texts);
    for (const batch of batches) {
      const estimated = batch.reduce((sum, text) => sum + estimateTokens(text), 0);
      expect(estimated).toBeLessThanOrEqual(EMBEDDING_BATCH_MAX_ESTIMATED_TOKENS);
    }
    expect(batches.flat()).toEqual(texts);
  });

  it("preserves vector order across multiple AI calls", async () => {
    let offset = 0;
    const run = vi.fn(async (_model: unknown, input: { text: string[] }) => {
      const data = input.text.map(() => {
        const value = offset++;
        return [value, value + 0.5];
      });
      return { data };
    });
    const env = {
      AI: { run },
      EMBEDDING_MODEL: "@cf/baai/bge-m3",
      EMBEDDING_DIMENSIONS: "2",
    } as unknown as Env;
    const large = "中".repeat(23_000);
    const texts = [large, large, "tail"];
    const vectors = await embedTexts(env, texts);
    expect(run).toHaveBeenCalledTimes(2);
    expect(vectors).toEqual([
      [0, 0.5],
      [1, 1.5],
      [2, 2.5],
    ]);
  });

  it("recursively splits a provider-rejected context batch without dropping order", async () => {
    let offset = 0;
    const run = vi.fn(async (_model: unknown, input: { text: string[] }) => {
      if (input.text.length > 2) throw new Error("3030: Max context reached 83804 tokens but model supports only 60000");
      return {
        data: input.text.map(() => {
          const value = offset++;
          return [value, value + 0.5];
        }),
      };
    });
    const env = {
      AI: { run },
      EMBEDDING_MODEL: "@cf/baai/bge-m3",
      EMBEDDING_DIMENSIONS: "2",
    } as unknown as Env;
    const vectors = await embedTexts(env, ["a", "b", "c", "d", "e"]);
    expect(run.mock.calls.length).toBeGreaterThan(1);
    expect(vectors).toEqual([
      [0, 0.5],
      [1, 1.5],
      [2, 2.5],
      [3, 3.5],
      [4, 4.5],
    ]);
  });
});
