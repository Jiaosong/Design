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

Post-sync knowledge governance uses the bearer-protected `/v1/governance-page` route. `GET` reads the live Notion page plus markdown; `POST` is intentionally allowlisted to `canonical_id`, `retrieval_space`, `search_eligibility`, `governance_state`, and `relation_state`, with lifecycle/relation values restricted to states already used by the corpus. The route derives the correct Notion property payload from the live page schema, then immediately runs the normal `syncPage` path and returns before/after readback. It is not a bulk mutation API: operators must complete content review and a shadow decision before each write. Permanent deletion, arbitrary property writes, and relation-target rewrites are not exposed here.

The operator helper `node scripts/run-governance-page.mjs inspect <page_id>` performs protected live readback without printing the bearer token. After a documented content decision, `node scripts/run-governance-page.mjs set <page_id> key=value ...` can apply only the endpoint allowlist and prints the returned before/after + sync receipt.

Human reading is separated from governance storage. `POST /v1/reader-layer` creates one idempotent root-level `知识阅读台｜Knowledge Reader` backed by linked views of the existing Notes data source: Core Knowledge (`L4/L5 + ACTIVE + VALID`), Methods (`METHOD + ACTIVE + VALID`), Evidence (`L6 + ACTIVE + VALID`), Practice (`L7 + ACTIVE`), and History/Governance (`PROVENANCE` or `LEGACY/ARCHIVED/HOLD`). The reader layer does not duplicate the database and does not alter authority.

Paper-grade L4/L5 migrations use `POST /v1/academic-page`. New pages receive a clean reader-facing title while Canonical ID remains a property, can link to source/replaced pages, and are immediately indexed/read back. This path is deliberately additive: legacy source text is preserved and explicitly superseded rather than overwritten. L6 Source/Evidence and L7 Practice retain role-specific concise formats; they are not forced into essay prose.

`GET /v1/scheduler-status` is bearer-protected and reports the Cron heartbeat, last scheduled result, durable task counts, and whether a secondary scheduler should activate. A missing or older-than-three-minutes Cron heartbeat is considered stale only while open durable tasks still exist.

`.github/workflows/oleander-notion-scheduler-fallback.yml` is the cross-provider fallback scheduler. It is gated by the repository variable `OLEANDER_NOTION_FALLBACK_ENABLED=true` and requires the `OLEANDER_API_TOKEN` repository secret before activation; with the gate absent or false, scheduled runs do not start a runner. Once activated, it checks scheduler health every five minutes and remains idle while Cloudflare Cron is healthy. When the primary heartbeat is stale, it performs five serialized one-page drains with spacing so recovery stays close to the intended one-page-per-minute cadence. D1 task claiming remains the single concurrency authority.

For operator recovery when the bearer token must not be read into a shell, a single D1 runtime-state request may be set to `scheduled_reconcile_request=REQUESTED` (full) or `REQUESTED:<1..1000>` (bounded). The Cron handler claims it once, creates a normal `sync_runs` record, persists the tasks, writes `scheduled_reconcile_last_run`, and deletes the request. This is an emergency control-plane trigger only; it does not create a second knowledge authority.

See `ARCHITECTURE.md` for authority and failure semantics.
