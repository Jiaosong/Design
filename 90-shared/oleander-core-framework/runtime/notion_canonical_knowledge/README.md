# OLEANDER Notion Canonical Knowledge

Cloudflare Worker runtime that turns the live OLEANDER Notion Notes Registry into an authority-aware derivative retrieval index.

It deliberately does **not** create a second Notion taxonomy or a second Current authority.

## Components

- Notion connection webhook receiver + HMAC validation
- D1 webhook dedupe / document manifest / chunk manifest / lineage
- Cloudflare Queue ingestion worker
- Notion API latest-page + enhanced-Markdown fetch
- structure-aware multilingual chunking
- Workers AI embeddings (`@cf/baai/bge-m3`, 1024 dimensions)
- Vectorize namespaces: `CURRENT`, `SUPPORT`, `PROVENANCE`
- D1-readback guarded search API
- `oleander-knowledge-pack/v1` response contract

## Local verification

```powershell
npm install
npm run check
./scripts/provision-cloudflare.ps1
```

The provisioning script is **dry-run by default**. It only creates Cloudflare resources when called with `-Apply`.

## Cloudflare provisioning

Current remote state (2026-09-12): Cloudflare D1, Queue + DLQ, Vectorize and Worker are provisioned. The Notion internal connection and webhook verification are bound, and the runtime is in **FULL RECONCILE / READBACK PENDING** rather than ingestion hold. A partial full-run snapshot reached 194 indexed documents out of 1,184 enumerated Notes objects; this is not a full-sync claim. See `OLEANDER_RUNTIME_RECEIPT_v0.3.md` plus the subsequent queue/readback receipt before promotion.

Current Worker URL:

```text
https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev
```

To bind the remaining Notion API secret without writing it to Git:

```powershell
./scripts/bind-notion-secrets.ps1 -Deploy
```

The commands below remain the reproducible from-zero provisioning path.

After reviewing account/cost implications:

```powershell
./scripts/provision-cloudflare.ps1 -Apply
```

Then copy the returned D1 `database_id` into `wrangler.jsonc`, apply migrations, and set secrets:

```powershell
npx wrangler d1 migrations apply oleander-knowledge-manifest --remote
npx wrangler secret put NOTION_TOKEN
npx wrangler secret put NOTION_WEBHOOK_VERIFICATION_TOKEN
npx wrangler secret put OLEANDER_API_TOKEN
```

Deploy:

```powershell
npx wrangler deploy
```

Set the resulting HTTPS URL plus `/webhooks/notion` as the Notion connection webhook endpoint, complete the one-time verification, and subscribe at minimum to page create/content/property/move/delete/undelete events.

For the one-time Notion subscription token, configure `OLEANDER_API_TOKEN` first. The Worker stores the incoming verification token encrypted in D1 rather than printing it to logs. Retrieve it once using:

```text
GET /v1/webhook-setup-token
Authorization: Bearer <OLEANDER_API_TOKEN>
```

Set the returned value as `NOTION_WEBHOOK_VERIFICATION_TOKEN`, then clear the temporary ciphertext:

```text
DELETE /v1/webhook-setup-token
Authorization: Bearer <OLEANDER_API_TOKEN>
```

Initial full reconcile after deployment:

```text
POST /v1/reconcile
Authorization: Bearer <OLEANDER_API_TOKEN>
{}
```

For first-bind validation, use a bounded reconcile before the full run:

```json
{ "limit": 1 }
```

The repository helper keeps the bearer token in gitignored `.dev.vars` and never prints it:

```powershell
node scripts/run-reconcile.mjs bounded 1
node scripts/run-search.mjs --scoped "your validation query"
node scripts/run-reconcile.mjs full
```

`limit` is clamped to `1..1000`. Omitting both `page_id` and `limit` preserves the full Notes reconcile behavior.

Queue safety defaults are deliberately conservative: one-message consumer batches, concurrency `1`, bounded retries, and a dead-letter queue. The DLQ is **containment**, not an automatic replay loop; failed messages must remain inspectable until a bounded repair/re-drive action is explicitly authorized.

Bulk reconcile no longer spends Queue operations. `POST /v1/reconcile` persists page-sync tasks in D1, and the `* * * * *` Cron Trigger drains **one page per invocation** directly through `syncPage`. This deliberately matches the proven one-page Queue consumer CPU profile because Workers Free Cron invocations have a very small CPU budget. A Cron invocation that seeds a full reconcile does not also drain a page. Queue remains the low-latency webhook fast path; if Queue write fails, the webhook is persisted into the same D1 scheduler instead of being dropped. `GET /v1/reconcile-status?run_id=<id>` is the readback gate for a reconcile run.

For explicit operator verification/recovery, `POST /v1/drain-once` is bearer-protected and executes exactly the same bounded D1 drain path as the Cron handler. The repository helper `node scripts/run-drain-once.mjs` reads the token only from gitignored `.dev.vars` and does not print it. This endpoint is not a parallel scheduler; it is a manual trigger for the same durable task state machine.

`GET /v1/scheduler-status` is bearer-protected and reports the Cron heartbeat, last scheduled result, durable task counts, and whether a secondary scheduler should activate. A missing or older-than-three-minutes Cron heartbeat is considered stale only while open durable tasks still exist.

`.github/workflows/oleander-notion-scheduler-fallback.yml` is the cross-provider fallback scheduler. It checks scheduler health every five minutes and remains idle while Cloudflare Cron is healthy. When the primary heartbeat is stale, it performs five serialized one-page drains with spacing so recovery stays close to the intended one-page-per-minute cadence. D1 task claiming remains the single concurrency authority.

For operator recovery when the bearer token must not be read into a shell, a single D1 runtime-state request may be set to `scheduled_reconcile_request=REQUESTED` (full) or `REQUESTED:<1..1000>` (bounded). The Cron handler claims it once, creates a normal `sync_runs` record, persists the tasks, writes `scheduled_reconcile_last_run`, and deletes the request. This is an emergency control-plane trigger only; it does not create a second knowledge authority.

See `ARCHITECTURE.md` for authority and failure semantics.
