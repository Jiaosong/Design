import { describe, expect, it } from "vitest";
import { FRAMEWORK_TYPES, PRIMARY_KNOWLEDGE_ROLES, RELATION_FAMILIES, RETRIEVAL_PIPELINE_VERSION } from "../src/config";
import { mergeAndDedupeCandidates } from "../src/search";
import type { KnowledgeHit, SearchRequest } from "../src/types";

function hit(overrides: Partial<KnowledgeHit> = {}): KnowledgeHit {
  return {
    vector_id: "v1",
    score: 0.7,
    namespace: "CURRENT",
    page_id: "page-1",
    canonical_id: "KN-TEST-001",
    title: "Test object",
    heading_path: "",
    text: "body",
    content_hash: "hash",
    knowledge_role: "METHOD",
    content_level: "L5｜Knowledge Object",
    framework_type: null,
    trust_state: "VERIFIED",
    primary_domain_ids: ["domain-a"],
    topic_ids: [],
    secondary_semantics: [],
    candidate_sources: ["VECTOR"],
    ...overrides,
  };
}

describe("knowledge index v2 alignment", () => {
  it("keeps the canonical role and L4 framework vocabularies closed at the current contracts", () => {
    expect(PRIMARY_KNOWLEDGE_ROLES).toEqual([
      "INDEX", "THEORY", "METHOD", "TOOL", "SOURCE", "EVIDENCE", "CASE", "PRACTICE",
    ]);
    expect(FRAMEWORK_TYPES).toHaveLength(11);
    expect(FRAMEWORK_TYPES).toContain("HISTORICAL_COMPARATIVE_SYNTHESIS");
    expect(FRAMEWORK_TYPES).not.toContain("MECHANISM");
    expect(RETRIEVAL_PIPELINE_VERSION).toBe("oleander-knowledge-pack/v2");
  });

  it("keeps exactly the six canonical relation families", () => {
    expect(RELATION_FAMILIES).toEqual([
      "STRUCTURAL_HIERARCHY",
      "DOMAIN_PLACEMENT",
      "KNOWLEDGE_DEPENDENCY",
      "EVIDENCE_SUPPORT",
      "APPLICATION_USE",
      "LIFECYCLE_LINEAGE",
    ]);
  });

  it("dedupes candidate carriers by canonical identity while preserving candidate provenance", () => {
    const vector = hit({ score: 0.72, candidate_sources: ["VECTOR"] });
    const lexical = hit({
      vector_id: "v2",
      score: 0.95,
      lexical_score: 0.95,
      candidate_sources: ["EXACT", "LEXICAL"],
      text: "exact lexical carrier",
    });
    const result = mergeAndDedupeCandidates([vector, lexical], { query: "KN-TEST-001" }, 8);
    expect(result).toHaveLength(1);
    expect(result[0]?.text).toBe("exact lexical carrier");
    expect(new Set(result[0]?.candidate_sources)).toEqual(new Set(["VECTOR", "EXACT", "LEXICAL"]));
  });

  it("applies role and secondary-semantic rerank only from explicit request hints", () => {
    const diagnostic = hit({
      page_id: "page-diagnostic",
      canonical_id: "KN-DIAG-001",
      score: 0.70,
      secondary_semantics: ["DIAGNOSTIC_TEST"],
    });
    const generic = hit({
      page_id: "page-generic",
      canonical_id: "KN-GENERIC-001",
      score: 0.75,
      secondary_semantics: [],
    });
    const noHints = mergeAndDedupeCandidates([diagnostic, generic], { query: "test" }, 8);
    expect(noHints[0]?.canonical_id).toBe("KN-GENERIC-001");

    const withHints: SearchRequest = { query: "test", knowledge_roles: ["METHOD"], secondary_semantics: ["DIAGNOSTIC_TEST"] };
    const reranked = mergeAndDedupeCandidates([diagnostic, generic], withHints, 8);
    expect(reranked[0]?.canonical_id).toBe("KN-DIAG-001");
  });

  it("narrows domain/topic only when caller supplies explicit filters", () => {
    const a = hit({ canonical_id: "A", page_id: "a", primary_domain_ids: ["domain-a"] });
    const b = hit({ canonical_id: "B", page_id: "b", primary_domain_ids: ["domain-b"] });
    expect(mergeAndDedupeCandidates([a, b], { query: "x" }, 8)).toHaveLength(2);
    expect(mergeAndDedupeCandidates([a, b], { query: "x", domain_ids: ["domain-b"] }, 8)
      .map((item) => item.canonical_id)).toEqual(["B"]);
  });
});
