import { describe, expect, it } from "vitest";
import { chunkMarkdown, estimateTokens, normalizeMarkdownForHash } from "../src/chunker";

describe("structure-aware chunker", () => {
  it("preserves heading paths", () => {
    const chunks = chunkMarkdown("# A\nIntro\n\n## B\nDetail\n\n### C\nMore");
    expect(chunks.map((chunk) => chunk.headingPath.join(" > "))).toEqual(["A", "A > B", "A > B > C"]);
  });

  it("bounds estimated chunk size", () => {
    const text = `# 中文测试\n\n${"这是一个用于分片测试的长段落。".repeat(160)}`;
    const chunks = chunkMarkdown(text);
    expect(chunks.length).toBeGreaterThan(1);
    expect(Math.max(...chunks.map((chunk) => chunk.tokenEstimate))).toBeLessThanOrEqual(320);
  });

  it("uses a CJK-aware token estimate", () => {
    expect(estimateTokens("测试中文" )).toBeGreaterThanOrEqual(4);
  });

  it("removes rotating AWS signature material from hash-normalized markdown", () => {
    const a = "![x](https://example.com/a.png?X-Amz-Date=1&X-Amz-Signature=aaa)";
    const b = "![x](https://example.com/a.png?X-Amz-Date=2&X-Amz-Signature=bbb)";
    expect(normalizeMarkdownForHash(a)).toBe(normalizeMarkdownForHash(b));
  });
});
