# OLEANDER Notion Canonical Knowledge Runtime Receipt v0.2

Status: **REMOTE INFRASTRUCTURE PROVISIONED / NOTION INGESTION HOLD**

Promotion: **NOT REQUESTED / NOT GRANTED**

Date: 2026-09-11

## Scope

Provisioned and deployed the Cloudflare side of:

`Notion Canonical Knowledge → Webhook → Worker → Queue/Dedupe → Fetch Latest → Normalize/Chunk → D1 + Workers AI → Vectorize → Authority-aware API → Knowledge Pack → OLEANDER`.

This receipt extends `OLEANDER_RUNTIME_RECEIPT_v0.1.md`. It does not replace the local-validation receipt.

## Remote resources

- Worker: `oleander-notion-canonical-knowledge`
- Workers.dev route: `https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev`
- code deployment version: `1727f64b-46f1-42e4-a0cc-0773b5e895a9`
- active deployment after controlled API-secret rotation: `5fdb62c9-89b7-4659-9769-12ad0e433b6e`
- D1: `oleander-knowledge-manifest`
- D1 database id: `287de73b-8145-4299-a3f3-729b8c312b70`
- D1 location: APAC; remote readback served from SIN during validation
- ingest queue: `oleander-notion-ingest` / id `7a18a91652fc4370a9f270fbb4c0d2c4`
- dead-letter queue: `oleander-notion-ingest-dlq` / id `9be180e52c144b4a9426a22ec3b17e17`
- Vectorize: `oleander-knowledge-v1`, 1024 dimensions, cosine metric
- Workers AI embedding model: `@cf/baai/bge-m3`
- Notion API version target: `2026-03-11`

## Remote validation

**PASS — Cloudflare infrastructure and retrieval runtime.**

- Cloudflare OAuth authorization: PASS.
- D1 `0001_manifest.sql`: PASS remote.
- D1 `0002_history_and_setup_state.sql`: PASS remote.
- D1 table readback: `documents`, `chunks`, `lineage_edges`, `webhook_events`, `sync_runs`, `runtime_state` present.
- Queue readback: ingest queue has one producer and one consumer; DLQ exists.
- Vectorize readback: 1024 dimensions / cosine confirmed.
- Workers AI catalog readback: `@cf/baai/bge-m3` present.
- Worker deploy: PASS; Worker startup time reported as 5 ms.
- post-provision `npm run check`: PASS, 3 files / 11 tests.
- post-provision `wrangler deploy --dry-run`: PASS with AI, D1, Queue and Vectorize bindings.
- remote preview with Queue removed only for the preview limitation: `/health` = 200.
- remote preview authority search: `/v1/search` = 200 after a real Workers AI embedding + Vectorize query + D1 manifest readback; empty result sets are expected before Notion ingestion.
- D1 pre-ingest readback: `documents=0`, `active_chunks=0`, `webhook_events=0`, as expected before Notion binding.

## Network observation

Direct local access to the new `workers.dev` route could not be used as validation because the current machine/network resolves the route to `198.18.1.x` and TLS negotiation fails before HTTP. Cloudflare control-plane deployment/readback and Cloudflare remote preview were therefore used for remote validation. This network observation is not evidence of a Worker code failure.

## Upstream authority preserved

- Notion current root remains `9150e089-9a7d-4b29-b026-175fca3a41b3`.
- Notes data source remains `4668fc63-45a6-496e-a2cc-f9542928b9e8`.
- `Retrieval Space｜检索空间` remains upstream authority metadata.
- CURRENT remains explicit-only.
- Vectorize is retrieval acceleration only; D1 manifest readback remains mandatory before returning a hit.
- No Notion taxonomy, Canonical ID, Canonical Parent/Children or knowledge role was rewritten by provisioning.

## Security state

- `OLEANDER_API_TOKEN`: set as Cloudflare Worker secret and retained only in local gitignored `.dev.vars` for controlled administrative calls.
- `NOTION_TOKEN`: **NOT SET**. No token was found in the local environment and no connector credential was extracted or copied.
- `NOTION_WEBHOOK_VERIFICATION_TOKEN`: **NOT SET** pending creation of the Notion connection webhook subscription.
- webhook handler supports Notion one-time verification-token capture, encrypted D1 temporary storage, HMAC-SHA256 event validation, dedupe and Queue handoff.

## Remaining external binding

The runtime must remain **NOTION INGESTION HOLD** until all of the following are completed:

1. create/use a Notion internal connection or personal access token with read access to the Current root and live registries;
2. store that value as Cloudflare secret `NOTION_TOKEN`;
3. create a Notion connection webhook subscription pointing to `/webhooks/notion`, API version `2026-03-11`, for the required page/data-source events;
4. retrieve the one-time verification token through the bearer-protected setup endpoint and verify the subscription in Notion;
5. store the verification token as `NOTION_WEBHOOK_VERIFICATION_TOKEN` and clear the temporary D1 setup token;
6. run full `/v1/reconcile` and independently read back D1 document/chunk counts and Vectorize results;
7. test one real Notion edit → webhook → queue → latest fetch → reindex cycle.

Until those steps pass, **Cloudflare Runtime PASS ≠ Notion Sync PASS ≠ Knowledge Promotion**.
