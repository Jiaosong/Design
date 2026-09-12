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
      "治理状态": { type: "select", select: { name: "REVIEW" } },
      "关系状态": { type: "select", select: { name: "REVIEW" } },
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
        governance_state: "HOLD",
        relation_state: "REVIEW",
      }),
    ).toEqual({
      "Canonical ID": { rich_text: [{ type: "text", text: { content: "LEGACY-OLD" } }] },
      "Retrieval Space｜检索空间": { select: { name: "PROVENANCE" } },
      "Search Eligibility｜检索资格": { select: { name: "HISTORY_ONLY" } },
      "治理状态": { select: { name: "HOLD" } },
      "关系状态": { select: { name: "REVIEW" } },
    });
  });

  it("rejects retrieval/search values outside the runtime contract", () => {
    expect(() => buildGovernancePropertyPatch(page(), { retrieval_space: "MAYBE" })).toThrow(/Invalid retrieval_space/);
    expect(() => buildGovernancePropertyPatch(page(), { search_eligibility: "PUBLIC" })).toThrow(/Invalid search_eligibility/);
    expect(() => buildGovernancePropertyPatch(page(), { governance_state: "DONE" })).toThrow(/Invalid governance_state/);
    expect(() => buildGovernancePropertyPatch(page(), { relation_state: "BROKEN" })).toThrow(/Invalid relation_state/);
  });

  it("can clear an allowlisted property without touching other fields", () => {
    expect(buildGovernancePropertyPatch(page(), { canonical_id: null })).toEqual({ "Canonical ID": { rich_text: [] } });
  });
});
