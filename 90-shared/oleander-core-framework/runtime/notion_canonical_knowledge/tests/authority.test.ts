import { describe, expect, it } from "vitest";
import { resolveAuthority } from "../src/authority";
import type { NormalizedPage } from "../src/types";

function page(overrides: Partial<NormalizedPage> = {}): NormalizedPage {
  return {
    pageId: "page-1",
    canonicalId: "MTH-TEST-001",
    title: "Test",
    url: null,
    lastEditedTime: null,
    inTrash: false,
    parentDataSourceId: "notes",
    retrievalSpace: null,
    searchEligibility: "DEFAULT",
    trustState: "VERIFIED",
    governanceState: "ACTIVE",
    relationState: "VALID",
    contentLevel: "L5｜Knowledge Object",
    knowledgeRole: "METHOD",
    primaryDomainIds: [],
    relatedDomainIds: [],
    sourceRelationIds: [],
    methodRelationIds: [],
    replacementIds: [],
    replacedDocumentIds: [],
    ...overrides,
  };
}

describe("resolveAuthority", () => {
  it("never infers CURRENT when Retrieval Space is missing", () => {
    expect(resolveAuthority(page()).effectiveSpace).toBe("SUPPORT");
  });

  it("keeps explicit CURRENT when no safety boundary conflicts", () => {
    expect(resolveAuthority(page({ retrievalSpace: "CURRENT" }))).toEqual({
      index: true,
      effectiveSpace: "CURRENT",
      reason: "EXPLICIT_NOTION_CURRENT",
      conflict: false,
    });
  });

  it("downgrades legacy CURRENT to PROVENANCE", () => {
    const result = resolveAuthority(page({ retrievalSpace: "CURRENT", governanceState: "LEGACY" }));
    expect(result.effectiveSpace).toBe("PROVENANCE");
    expect(result.conflict).toBe(true);
  });

  it("blocks explicitly blocked pages", () => {
    expect(resolveAuthority(page({ retrievalSpace: "CURRENT", searchEligibility: "BLOCKED" })).index).toBe(false);
  });

  it("forces HISTORY_ONLY to PROVENANCE", () => {
    expect(resolveAuthority(page({ retrievalSpace: "SUPPORT", searchEligibility: "HISTORY_ONLY" })).effectiveSpace).toBe("PROVENANCE");
  });
});
