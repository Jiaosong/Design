# OLEANDER Authority-aware RAG Contract v0.1

Status: CANDIDATE IMPLEMENTATION CONTRACT / NOT A NEW SOURCE OF TRUTH

## 1. Purpose

This contract defines a derived retrieval plane for OLEANDER knowledge. It does not replace, duplicate, or promote any Source Authority, Project Current, Knowledge Current, Skill Current, or GitHub installed Current.

Canonical truth remains in the existing OLEANDER authority chain. The RAG layer may cache, normalize, chunk, embed, filter, rank, and return references, but it must always preserve a reversible locator to the canonical source and must be rebuildable from canonical sources.

## 2. Non-authority boundary

The retrieval plane is strictly DERIVED_INFRASTRUCTURE.

- Notion remains the canonical knowledge source for Notion-owned knowledge objects.
- GitHub remains canonical for installed runtime/skill/governance artifacts where existing OLEANDER policy says so.
- Vectorize is a semantic index, not truth.
- D1 is a manifest/control layer, not truth.
- R2 is an optional normalized snapshot/archive carrier, not truth.
- Workers AI output never becomes authority merely because it was generated, embedded, reranked, or summarized.
- MCP is an interactive source inspection/write-back adapter, not the continuous replication log.

## 3. Retrieval precedence

Semantic similarity may never outrank authority legality.

Default retrieval order:

1. Resolve exact Canonical ID / exact owner / explicit alias when available.
2. Resolve intended project/domain/task scope.
3. Select legal retrieval namespace.
4. Apply authority/lifecycle metadata prefilter.
5. Run vector retrieval inside the legal set.
6. Run lexical/exact-term retrieval.
7. Fuse candidate sets.
8. Optionally rerank.
9. Canonical-dedupe and run conflict gate.
10. Return a structured Knowledge Pack.
11. Fetch canonical original through Notion/GitHub only when source verification, conflict resolution, high-stakes validation, or write-back is required.

Default CURRENT retrieval must not mix CURRENT and PROVENANCE in one ranking pool.

## 4. Required governance fields

Every indexed knowledge object must preserve at least:

- canonical_id
- source_locator
- source_kind
- retrieval_space
- search_eligibility
- governance_state
- trust_state
- freshness_state
- evidence_grade
- authority_class
- project_id
- domain_id
- knowledge_role
- object_type
- last_edited_at
- last_verified_at when available
- verification_due when available
- content_hash
- schema_version

Unknown values are not auto-guessed. Unknown lifecycle/authority values remain UNKNOWN/SCOPED or are excluded from default Current retrieval according to policy.

## 5. Vectorize layout

Recommended production namespaces:

- prod-current
- prod-support
- prod-provenance

EXCLUDED/BLOCKED content is normally not inserted into a default-queryable namespace.

Recommended indexed metadata fields, subject to current Vectorize account limits:

1. retrieval_space
2. search_eligibility
3. governance_state
4. trust_state
5. freshness_state
6. evidence_grade
7. authority_class
8. project_id
9. domain_id
10. knowledge_role

If access control requires a hard indexed field, `access_scope` takes precedence over a retrieval-optimization field.

## 6. Synchronization model

Primary sync path:

Notion webhook -> verify signature -> enqueue/coalesce -> fetch latest canonical state through Notion API -> normalize -> hash diff -> structure-aware chunk -> embed changed text -> upsert Vectorize -> commit D1 manifest state.

Webhook payloads are treated as change signals, not canonical page state.

MCP is reserved for interactive fetch-original, human/agent validation, conflict resolution, and authorized write-back.

A periodic reconciliation job must detect missed/out-of-order webhook events and rebuild derived state from canonical sources.

## 7. Chunking rules

- Never concatenate unrelated pages into one chunk.
- Prefer page heading/semantic section/block boundaries.
- Preserve complete rule/definition/schema blocks where practical.
- Tables retain headers with their row groups.
- Code/schema blocks remain whole when practical.
- Default prose target: ~350-700 tokens.
- Practice/case target: ~300-600 tokens.
- Optional prose overlap: 10-15%.
- Do not summarize with an LLM before embedding by default.

Embedding text may include title, canonical ID, domain, section label, and normalized canonical prose. Governance states must remain hard metadata, not prompt-like text inserted to bias similarity.

## 8. Retrieval API output

The API returns a Knowledge Pack, not an untyped list of chunks.

Minimum response fields:

```json
{
  "query_id": "...",
  "authority_policy": "CURRENT_DEFAULT",
  "results": [
    {
      "canonical_id": "...",
      "source_locator": "...",
      "status": {
        "retrieval_space": "CURRENT",
        "trust_state": "VERIFIED",
        "freshness_state": "FRESH"
      },
      "score": {
        "vector": 0.0,
        "lexical": 0.0,
        "rerank": 0.0
      },
      "chunks": []
    }
  ],
  "conflicts": [],
  "support_expansion_used": false
}
```

## 9. Workers AI policy

- Embedding: required for semantic retrieval.
- Query rewrite: conditional only for ambiguous/follow-up queries.
- Rerank: recommended when candidate count/score proximity justifies it.
- LLM generation: not part of the mandatory retrieval path.

Retrieval correctness must not depend on a generation model deciding which source is authoritative after the fact.

## 10. Anti-pollution gates

Hard failures include:

- canonical collision with two simultaneous Current owners;
- CURRENT/PROVENANCE mixed by default ranking;
- UNKNOWN authority silently promoted to CURRENT;
- vector/index content without a canonical source locator;
- source hash drift with stale derived chunks presented as fresh;
- write-back from derived output without canonical readback;
- LLM summary replacing canonical text as the only retained carrier;
- second Project State / Skill / Method / Framework created solely for this retrieval plane.

## 11. Migration rule

Migration is Current-first and shadow-first:

1. Freeze schema v0.1.
2. Create metadata indexes before backfill.
3. Backfill CURRENT + DEFAULT only.
4. Evaluate against a Golden Retrieval Set.
5. Add CURRENT + SCOPED.
6. Add SUPPORT in a separate namespace.
7. Add PROVENANCE last.
8. Run dual-read comparison against existing direct Notion retrieval.
9. Cut over to RAG-first only after authority and recall gates pass.
10. Keep MCP/source fetch as verification/write-back path.

## 12. Initial acceptance targets

These are engineering targets, not vendor SLAs:

- Authority cross-contamination: 0 known CURRENT/PROVENANCE violations.
- Canonical collision: 0 unresolved collisions returned as normal results.
- Recall@10 on legal Current golden set: >= 0.90 target.
- Precision@5 on legal Current golden set: >= 0.85 target.
- Retrieval P95 target: <= 1.5 s with rerank enabled; <= 0.8 s target without rerank.
- Sync freshness target: median <= 2 min, P95 <= 5 min from canonical change to queryable derived state, subject to Notion delivery envelope.
- No material text change => no re-embedding.

## 13. Flow Completion

A retrieval implementation may be marked production-ready only after:

READ -> REUSE -> DEFINE -> BENCHMARK -> MAKE -> TEST -> JUDGE -> REPAIR -> RETEST -> DISTILL -> UPDATE -> REAPPLY -> REGRESSION-PROTECT -> FLOW COMPLETION

Machine PASS does not grant Knowledge Current, Design KEEP, Project Current, or Authority promotion.
