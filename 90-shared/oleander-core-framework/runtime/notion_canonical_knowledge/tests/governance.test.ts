import { describe, expect, it } from "vitest";
import { buildGovernancePropertyPatch } from "../src/notion";
import type { NotionPage } from "../src/types";

function page(): NotionPage {
  return {
    object: "page",
    id: "p1",
    properties: {
      "Canonical ID": { type: "rich_text", rich_text: [{ plain_text: "OLD" }] },
      "Retrieval Space｜检索空间": { type: "select", select: { name: "PROVENANCE" } },
      "Search Eligibility｜检索资格": { type: "select", select: { name: "HISTORY_ONLY" } },
    },
  };
}

describe("governance property patch", () => {
  it("builds bounded rich-text/select updates", () => {
    expect(
      buildGovernancePropertyPatch(page(), {
        canonical_id: "LEGACY-OLD",
        retrieval_space: "PROVENANCE",
        search_eligibility: "HISTORY_ONLY",
      }),
    ).toEqual({
      "Canonical ID": { rich_text: [{ type: "text", text: { content: "LEGACY-OLD" } }] },
      "Retrieval Space｜检索空间": { select: { name: "PROVENANCE" } },
      "Search Eligibility｜检索资格": { select: { name: "HISTORY_ONLY" } },
    });
  });

  it("rejects retrieval/search values outside the runtime contract", () => {
    expect(() => buildGovernancePropertyPatch(page(), { retrieval_space: "MAYBE" })).toThrow(/Invalid retrieval_space/);
    expect(() => buildGovernancePropertyPatch(page(), { search_eligibility: "PUBLIC" })).toThrow(/Invalid search_eligibility/);
  });

  it("can clear an allowlisted property without touching other fields", () => {
    expect(buildGovernancePropertyPatch(page(), { canonical_id: null })).toEqual({ "Canonical ID": { rich_text: [] } });
  });
});
