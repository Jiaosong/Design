# OLEANDER Notion Canonical Knowledge Runtime Receipt v0.3

Status: **NOTION BINDING PASS / FULL RECONCILE IN PROGRESS**

Promotion: **NOT REQUESTED / NOT GRANTED**

Date: 2026-09-11

## What changed

The live Notion internal connection and webhook subscription are now bound to the deployed Cloudflare runtime.

- `NOTION_TOKEN`: present as a Cloudflare Worker secret.
- `NOTION_WEBHOOK_VERIFICATION_TOKEN`: present as a Cloudflare Worker secret.
- `OLEANDER_API_TOKEN`: present as a Cloudflare Worker secret.
- one-time webhook verification ciphertext was captured by the Worker, converted into the production webhook secret, and removed from D1 after Notion verification.
- production `/health`: HTTP 200.

No secret value is stored in Git or in this receipt.

## Production runtime

- Worker: `oleander-notion-canonical-knowledge`
- route: `https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev`
- current validated deployment version: `0adc18bf-a47f-4c96-b6d8-7894869c4172`
- D1: `oleander-knowledge-manifest`
- Queue: `oleander-notion-ingest`
- DLQ: `oleander-notion-ingest-dlq`
- Vectorize: `oleander-knowledge-v1`
- embedding model: `@cf/baai/bge-m3`
- Notion API version: `2026-03-11`

## Live compatibility repair

The first bounded reconcile exposed a Notion API 2026-03-11 validation change: `POST /v1/data_sources/:id/query` rejects `in_trash: false` in the request body.

Repair:

- removed the obsolete `in_trash` request-body field;
- retained `page_size=100` and `result_type=page` pagination;
- added bounded reconcile `limit` for anti-pollution first-bind validation;
- added sync-run failure closure so reconcile exceptions write `FAILED + error` instead of leaving a false `RUNNING` receipt.

The pre-fix failed run was explicitly closed as `FAILED / NOTION_QUERY_VALIDATION_ERROR_PRE_FIX`.

## Bounded seed proof

Bounded run:

- run id: `b976bb33-b09d-4e92-a4be-459deb749fae`
- type: `BOUNDED_NOTES_RECONCILE`
- pages enqueued: `1`
- status: `QUEUED`

The seeded Notion object was indexed as:

- Canonical ID: `SRC-CMF-HUANG-CMF-HANDBOOK-2025-001`
- effective retrieval space: `SUPPORT`
- authority reason: `EXPLICIT_NOTION_SUPPORT`
- search eligibility: `SCOPED`
- trust state: `UNVERIFIED`
- governance state: `REVIEW`
- relation state: `REVIEW`
- level: `L6｜Evidence / Case`
- role: `SOURCE`
- active chunks: `14`

This is the expected fail-closed result. The runtime did not promote the source to CURRENT.

## Vectorize + authority readback proof

Vectorize readback after the bounded seed:

- index vector count: `14`
- processed mutation present;
- all 14 vector IDs visible through Vectorize list-vectors.

Default search returned zero hits because the source is `SCOPED`, which is correct.

The same query with `include_scoped=true` returned 5 SUPPORT hits. Highest observed similarity score was approximately `0.816`. Every returned hit passed D1 active/document/namespace/search-eligibility readback before entering the Knowledge Pack.

## Full reconcile

Full run:

- run id: `6818ffc2-0b2a-40d4-89e3-9956bed98f4d`
- type: `FULL_NOTES_RECONCILE`
- pages enumerated/enqueued: `1184`
- enqueue status: `QUEUED`
- enqueue error: none

The Queue consumer is actively processing this run. This receipt does **not** claim all 1184 pages are complete.

Progress snapshot during live readback:

- indexed documents: `194`
- active documents: `194`
- inactive documents: `0`
- CURRENT documents: `15`
- SUPPORT documents: `140`
- PROVENANCE documents: `39`
- CURRENT active chunks: `239`
- SUPPORT active chunks: `1704`
- PROVENANCE active chunks: `383`

The prior snapshot was 77 documents / 929 active chunks, so the consumer was measurably progressing rather than stalled.

## Webhook state

The Notion webhook subscription has completed its one-time verification and the HMAC verification secret is installed in Cloudflare.

`webhook_events` remains zero at this snapshot because no post-verification Notes page edit has yet been used as a production page-event test. Verification handshake traffic is intentionally not inserted into `webhook_events`.

Therefore:

**Notion connection binding PASS ≠ first page-event webhook lifecycle PASS.**

The next natural Notes edit should be used to verify:

`signed page event → webhook dedupe → Queue → Fetch Latest → authority re-evaluation → reindex → webhook status PROCESSED`.

## Authority conclusion

- Notion remains canonical.
- CURRENT remains explicit-only.
- SCOPED content remains absent from default search.
- SUPPORT and PROVENANCE remain physically separated Vectorize namespaces.
- Vectorize is not accepted as authority without D1 readback.
- no Notion hierarchy, Canonical ID, promotion state or knowledge role was rewritten by the Cloudflare binding.
- full reconcile is asynchronous and still processing at the time of this receipt.
