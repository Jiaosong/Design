import { describe, expect, it } from "vitest";
import { mergeReaderChunks } from "../src/reader";

describe("knowledge reader detail assembly", () => {
  it("merges contiguous chunks in the same section without repeating overlap", () => {
    const overlap = "shared overlap text that is intentionally long enough to match exactly";
    const sections = mergeReaderChunks([
      {
        ordinal: 0,
        heading_path: "Framework > Claim",
        chunk_text: `first paragraph\n\n${overlap}`,
        token_estimate: 40,
      },
      {
        ordinal: 1,
        heading_path: "Framework > Claim",
        chunk_text: `${overlap}\n\nsecond paragraph`,
        token_estimate: 35,
      },
      {
        ordinal: 2,
        heading_path: "Framework > Boundary",
        chunk_text: "boundary paragraph",
        token_estimate: 12,
      },
    ]);

    expect(sections).toHaveLength(2);
    expect(sections[0]?.headingPath).toEqual(["Framework", "Claim"]);
    expect(sections[0]?.chunkOrdinals).toEqual([0, 1]);
    expect(sections[0]?.text.match(new RegExp(overlap, "g"))).toHaveLength(1);
    expect(sections[0]?.text).toContain("second paragraph");
    expect(sections[1]?.headingPath).toEqual(["Framework", "Boundary"]);
  });
});
