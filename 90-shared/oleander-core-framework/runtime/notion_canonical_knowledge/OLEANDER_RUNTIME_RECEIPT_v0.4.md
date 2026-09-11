# OLEANDER Notion Canonical Knowledge Runtime Receipt v0.4

Date: 2026-09-12

Status: **RUNTIME HARDENING DEPLOYED / WEBHOOK FALLBACK READBACK PASS / FULL RECONCILE CRON READBACK PENDING / CORPUS NOT SYNCED**

## 1. Authority Boundary

- Notion remains the canonical knowledge and lifecycle authority.
- GitHub remains runtime / artifact version authority.
- D1 + Vectorize remain derivative, rebuildable retrieval infrastructure.
- A successful Worker deploy is not equivalent to a successful knowledge sync.
- A reconcile run may be promoted to `SYNCED` only after durable task receipts and target readback close the run.

## 2. GitHub / CI Receipt

- Branch: `agent/oleander-notion-canonical-knowledge-v01-20260911`
- PR: `#521` (`feat(knowledge): Notion canonical retrieval runtime v0.1`)
- Hardening commits:
  - `b213bd73` — queue/rate-limit/readback hardening and fail-closed DLQ containment
  - `dd42eee0` — bulk reconcile moved to D1 durable scheduler + Cron
  - `ff643ed0` — Free-plan CPU boundary: one page per Cron invocation; reconcile seeding isolated from page processing
- Latest PR checks at `ff643ed0`: AI Governance PASS / Anti-Pollution PASS / Vercel PASS.
- PR remains draft until scheduled production readback proves Cron consumption. Do not force-merge only because CI is green.

## 3. Production Deployment Receipt

- D1 migration `0004_durable_sync_scheduler.sql`: APPLIED.
- Worker version: `7543082e-77c8-445f-b3ba-ac0f2fbeba96`.
- Trigger: `* * * * *` deployed.
- Production secret names read back present without exposing values:
  - `NOTION_TOKEN`
  - `NOTION_WEBHOOK_VERIFICATION_TOKEN`
  - `OLEANDER_API_TOKEN`
- Main Queue consumer remains constrained to one-message batches and concurrency `1`.
- DLQ has no automatic replay consumer; it is containment only.

## 4. Root Cause Readback

The first full reconcile enumerated 1,184 Notes objects but stopped at a verified D1 snapshot of 194 indexed documents. Production webhook events then returned:

`You have exceeded the daily write operations limit in Queues free tier (10253)`

This is a Queue-capacity failure, not evidence that Notion itself is blocked.

The old architecture used Queue as both low-latency event transport and bulk worklist. Retries amplify Queue read operations, so a bulk reconcile can consume the Free-plan daily operation budget even when batching is used.

## 5. Current Architecture

```text
Notion webhook
    -> Queue fast path
    -> if Queue write fails: D1 durable scheduler fallback

Full / bounded reconcile
    -> enumerate Notes
    -> D1 durable tasks
    -> Cron every minute
    -> one due page per invocation
    -> syncPage -> D1 manifest + Vectorize

Failures
    -> bounded RETRY with next_attempt_at
    -> stale PROCESSING recovery
    -> BLOCKED after bounded attempts
    -> no silent success
```

The one-page Cron drain is intentional. Workers Free Cron CPU is a hard design boundary; network/D1/AI wait time does not count as CPU, but local parsing/chunking/hash work does.

## 6. Production Webhook Fallback Readback

After deploying the D1 fallback, new real Notion edits were received while Queue was still over daily quota. Production D1 recorded `FALLBACK_SCHEDULED` rather than `QUEUE_ERROR`, including:

- `f8fd5153-198d-412e-94e6-6c41af7076c7` — `page.content_updated`
- `b6a3644c-93ba-41d8-9908-b401841c81f8` — `page.content_updated`
- `908830d1-da32-48bb-a9a3-e7600267d604` — `page.properties_updated`

Two earlier `QUEUE_ERROR` events that had already been manually persisted as D1 fallback tasks were normalized to the same fallback state. This proves the **incremental failover write path** in production.

## 7. Scheduled Reconcile State

- One-time operator request is persisted as `scheduled_reconcile_request=REQUESTED`.
- The request intentionally contains no secret.
- Cloudflare documents that new/changed Cron Triggers can take several minutes, up to 15 minutes, to propagate globally.
- Until production Cron claims the request and creates a durable full-run task set, status remains **CRON READBACK PENDING**.
- A remote preview `scheduled()` smoke test reached the scheduler code path but lacked the production Notion secret in the preview environment. That run was relabeled `REMOTE_PREVIEW_SCHEDULER_TEST` and must not be interpreted as a production credential failure.

## 8. Corpus Boundary

Last verified corpus snapshot before the durable scheduler starts draining:

- Notes enumerated by prior full reconcile: `1,184`
- D1 indexed documents: `194`
- Corpus status: **PARTIAL**

Do not report `NOTION SYNCED`, `1184/1184`, or equivalent until the new full run reaches a closed task readback with no unresolved `PENDING / PROCESSING / RETRY / BLOCKED` items.

## 9. Promotion Gate

Runtime implementation may be promoted only after:

1. production Cron claims `scheduled_reconcile_request`;
2. `scheduled_reconcile_last_run` is written;
3. at least one production scheduled task transitions to `PROCESSED`;
4. PR #521 remains CI-green after the latest commit;
5. Notion lifecycle page and GitHub runtime receipt agree on the same state.

Corpus promotion is a separate later gate and requires full reconcile closure.
