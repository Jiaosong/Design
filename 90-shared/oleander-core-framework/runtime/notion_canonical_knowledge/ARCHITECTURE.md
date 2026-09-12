# OLEANDER Notion Canonical Knowledge Runtime v0.1

Status: **NOTION BOUND / FULL BASELINE COMPLETE / CLOUD INCREMENTAL SYNC + ANTI-ENTROPY INVENTORY**

Upstream authority: **Notion Current Root Authority + live registries**

Purpose: materialize a searchable, authority-aware derivative index without creating a parallel knowledge authority.

## Runtime chain

```text
Notion Canonical Knowledge
        ↓ webhook signal
Cloudflare Worker /webhooks/notion
        ↓ D1 event-id dedupe
Cloudflare Queue
        ↓ webhook fast path / consumer always fetches latest
        ├──────── queue-write failure ────────┐
        │                                     ↓
        │                               D1 durable scheduler
        │                                     ↑
        │                         delta / inventory / repair
        │                                     ↓
        │                              Cron scheduled drain
        └─────────────────────────────────────┘
                                              ↓
Notion API 2026-03-11
  POST /v1/data_sources/:id/query
      ↳ last_edited_time delta watermark
      ↳ daily ID/edit-time inventory
  GET /v1/pages/:id
  GET /v1/pages/:id/markdown
        ↓
Normalize exact OLEANDER registry fields
        ↓
Authority gate + structure-aware chunk
        ↓
┌────────────────────────────┬──────────────────────────┐
│ D1 Manifest                │ Workers AI               │
│ page/chunk hash            │ @cf/baai/bge-m3          │
│ authority decision         │ 1024-d embedding         │
│ lineage + active state     │                          │
└────────────────────────────┴──────────────┬───────────┘
                                            ↓
                                      Vectorize V2
                           CURRENT / SUPPORT / PROVENANCE
                              isolated by namespace
                                            ↓
                                   Authority-aware API
                                            ↓
                               Knowledge Pack → OLEANDER
```

## Authority rules

1. **Notion remains canonical.** D1 and Vectorize are derivative read models only.
2. `Retrieval Space｜检索空间` is the primary explicit retrieval-space authority.
3. **CURRENT is never inferred.** Missing metadata fails closed to SUPPORT or PROVENANCE.
4. `BLOCKED` and `EXCLUDED` are not indexed.
5. `HISTORY_ONLY`, `LEGACY`, and `ARCHIVED` are forced to PROVENANCE.
6. `CONFLICT` or `ORPHAN` may downgrade an explicit CURRENT to SUPPORT until governance is repaired.
7. Vectorize results are not accepted directly. Every hit must read back against active D1 chunk + document manifest rows before entering a Knowledge Pack.
8. PROVENANCE is excluded from default search and must be explicitly requested.

## D1 responsibilities

- webhook event idempotency and queue status;
- Notion page manifest and last observed authority state;
- content/structure hashes;
- chunk text + hash + Vectorize ID mapping;
- lineage edges for Source / Method / replacement relations;
- active/inactive/tombstone state;
- reconcile run receipts.
- durable bulk/fallback sync task state (`PENDING / PROCESSING / RETRY / PROCESSED / BLOCKED`).
- delta watermark / cursor state and daily inventory receipts in `runtime_state`.
- last Notion inventory observation (`notion_seen_at`) and index-pipeline revision per document.

D1 does **not** decide Canonical ID, L0–L7 identity, hierarchy, role, domain or promotion.

## Structure-aware chunking

- source is Notion enhanced Markdown, not HTML scraping;
- H1–H6 path is retained as chunk context;
- signed URL query material is normalized before hashing to avoid false churn;
- multilingual token estimate is CJK-aware;
- target maximum is 320 estimated tokens with a 40-token tail overlap, leaving conservative headroom for title / Canonical ID / role / level / heading metadata;
- the embedding string includes title, Canonical ID, role, level and heading path;
- unknown/truncated Notion blocks are recursively fetched up to a bounded limit; unresolved IDs remain recorded in D1 rather than silently treated as complete.

## API contract

### `POST /webhooks/notion`
Public endpoint. Validates `X-Notion-Signature` after the one-time subscription handshake. Dedupe key is Notion event `id`.

The one-time `verification_token` is not echoed or logged. During setup it is AES-GCM encrypted with a key derived from the already-configured `OLEANDER_API_TOKEN`, stored temporarily in D1, and exposed only through bearer-protected `GET /v1/webhook-setup-token`. Delete that temporary state after storing the value as the Worker secret `NOTION_WEBHOOK_VERIFICATION_TOKEN`.

### `POST /v1/reconcile`
Bearer-protected repair path. Empty body enumerates the current Notes data source and enqueues every page. `{ "page_id": "..." }` enqueues one page. Routine operation must prefer webhook + delta + inventory and should not repeatedly run full reconcile.

### `POST /v1/incremental-sync`
Bearer-protected operator trigger for one page of the timestamp-watermarked delta scan. The automatic path runs from the existing Cron only while durable page work is idle. The scan uses a bounded `[watermark-overlap, scan-start]` window and advances the watermark only after pagination completes.

### `POST /v1/inventory-sync`
Bearer-protected operator trigger for one page of the daily anti-entropy inventory. The inventory reads IDs / edit timestamps, stamps `notion_seen_at`, and schedules only stale or missing candidates. Missing candidates are verified through `syncPage`; no inventory pass directly hard-deletes canonical or derivative records.

### `POST /v1/search`
Bearer-protected.

```json
{
  "query": "R06 节点的构造证据和边界条件",
  "top_k": 8,
  "include_support": true,
  "include_provenance": false,
  "include_scoped": false,
  "canonical_id": null
}
```

Response is an `oleander-knowledge-pack/v1` object with physically separate `current`, `support`, and `provenance` arrays.

`Search Eligibility｜检索资格 = SCOPED` is excluded from general search unless `include_scoped=true` or a specific `canonical_id` is supplied. `HISTORY_ONLY` can only surface through the explicitly requested PROVENANCE namespace.

### `GET /v1/knowledge-pack/:canonicalId`
Returns D1 manifest + lineage for one Canonical ID. It does not synthesize a new knowledge object.

## Failure semantics

- Notion 404 / lost sharing: deactivate prior vectors, preserving D1 history.
- moved outside Notes Registry: deactivate prior vectors.
- deleted/trash: deactivate prior vectors.
- queue failure: webhook event remains `QUEUE_ERROR`; Notion retry can re-enqueue it.
- embedding or Notion transient failure: individual queue message retries with bounded exponential delay; Cloudflare consumer DLQ is configured after max retries.
- DLQ containment is fail-closed: dead-lettered messages are not automatically replayed into the ingest queue, preventing an unbounded poison-message loop. Re-drive requires an explicit bounded repair action and a new readback receipt.
- bulk reconcile never depends on Queue capacity. D1 persists the worklist and Cron drains one page per Free-plan invocation; a full-reconcile seeding invocation does not also process a page. Stale `PROCESSING` claims are recovered to `RETRY` and bounded failures end in `BLOCKED`.
- normal anti-drift does not enumerate and re-embed the corpus: a ten-minute `last_edited_time` delta sweep stages only stale rows; a daily inventory compares IDs/edit timestamps without fetching Markdown for unchanged pages.
- delta watermarks advance only after complete pagination; a failed/partial inventory cannot deactivate unseen pages.
- unchanged live pages short-circuit before Markdown fetch / Workers AI embedding when Notion edit time and index revision match D1. Explicit repair reconcile is the only routine path that forces a rebuild of unchanged pages.
- webhook Queue-write failure falls back to the same durable D1 scheduler and remains visible in `webhook_events`; it is not silently treated as a successful Queue delivery.
- stale Vectorize result: rejected when D1 does not confirm the vector and document as active and in the same authority namespace.

## Does not prove

- Notion content is correct;
- a METHOD is validated;
- evidence is sufficient;
- a candidate is promoted;
- Design PASS, field truth, engineering/manufacturing approval or rights clearance.
