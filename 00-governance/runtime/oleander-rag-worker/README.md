# OLEANDER Authority-aware RAG Worker v0.1

Cloudflare-based derived retrieval infrastructure for OLEANDER.

This Worker is **not** a knowledge authority. It is rebuildable from canonical sources and must follow `OLEANDER_AUTHORITY_AWARE_RAG_CONTRACT_v0.1.md`.

## Architecture

```text
Notion canonical knowledge
  -> Webhook
  -> Worker signature verification
  -> Cloudflare Queue
  -> Notion API fetch latest
  -> structure-aware normalize/chunk
  -> Workers AI embedding
  -> Vectorize namespaces
  -> D1 manifest / lineage / audit

OLEANDER Agent
  -> POST /v1/retrieve
  -> Current namespace + authority metadata prefilter
  -> vector search
  -> D1 source/lineage readback
  -> canonical dedupe
  -> Knowledge Pack
  -> existing OLEANDER Resolver / Skill / Project flow

Notion MCP remains side-mounted for source verification and authorized write-back.
```

## Free / browser-first constraint

The implementation uses Cloudflare Workers, Queues, D1, Workers AI and Vectorize. It introduces no paid local software requirement. Do not enable a paid dependency solely to satisfy this adapter; stop at free-plan limits and preserve the existing direct-source retrieval fallback.

## Required Cloudflare resources

1. Worker: `oleander-authority-aware-rag`
2. D1: `oleander-rag-manifest`
3. Queue: `oleander-rag-sync`
4. Vectorize index: `oleander-bgem3-v1`
5. Workers AI binding: `AI`

Do not backfill vectors before metadata indexes exist.

Recommended Vectorize metadata indexes:

```text
retrieval_space
search_eligibility
governance_state
trust_state
freshness_state
evidence_grade
authority_class
project_id
domain_id
knowledge_role
```

If hard ACL filtering becomes required, `access_scope` replaces a lower-priority retrieval optimization field.

## Required secrets

- `NOTION_API_TOKEN`: minimum-permission Notion internal integration used only for canonical readback.
- `NOTION_WEBHOOK_SECRET`: Notion webhook signing secret.
- `RETRIEVAL_API_TOKEN`: service-to-service bearer token for `/v1/retrieve`.

Never commit secrets.

## D1 setup

Apply `schema.sql` to the `oleander-rag-manifest` database before enabling webhook ingestion.

## API

### `GET /health`

Returns derived-index object counts. This endpoint is diagnostic only.

### `POST /webhooks/notion`

- verifies Notion HMAC signature;
- deduplicates by event ID;
- records a bounded event receipt;
- queues the page for latest-state readback;
- returns 202 before embedding work.

### `POST /v1/retrieve`

Example:

```json
{
  "query": "OLEANDER 默认建模方式是什么",
  "project_id": "GLOBAL",
  "domain_id": "SPATIAL",
  "top_k": 20,
  "include_unverified": true,
  "history_intent": false
}
```

Default search is `prod-current` only. SUPPORT and PROVENANCE expansion are intentionally not automatic in v0.1.

## Shadow migration

Do not bulk-enable the entire Notion corpus at once.

1. Create resources and all metadata indexes.
2. Seed D1 schema.
3. Backfill `CURRENT + DEFAULT` only.
4. Run `golden-set.v0.1.jsonl` and record Recall@10 / Precision@5 / authority violations.
5. Add `CURRENT + SCOPED` only after the first gate passes.
6. Add SUPPORT in `prod-support` after separate evaluation.
7. Add PROVENANCE last and require explicit `history_intent`.
8. Compare RAG results against existing direct Notion retrieval before changing default routing.

Objects with incomplete lifecycle metadata are not guessed into Current. They remain UNKNOWN/SCOPED or outside default production retrieval until governance resolves them.

## Current implementation boundary

v0.1 implements:

- webhook signature verification and event dedupe;
- queue-based latest-state Notion fetch;
- canonical collision fail-closed check;
- Notion field alias mapping for existing OLEANDER knowledge metadata;
- structure-aware page/block flattening;
- text-hash comparison;
- no-re-embed path for metadata-only updates when existing vector values can be read;
- three retrieval namespaces;
- pre-vector authority filter;
- exact Canonical/title lookup + vector retrieval;
- typed Knowledge Pack;
- D1 lineage/audit receipts.

Not yet claimed in v0.1:

- production BM25/lexical index;
- cross-encoder rerank;
- query rewriting;
- GraphRAG relation expansion;
- automatic SUPPORT fallback;
- production ACL/multi-user policy;
- production deployment PASS;
- complete Notion corpus migration;
- promotion to default OLEANDER retrieval.

Those remain gated by Golden Set results and actual Cloudflare deployment readback.
