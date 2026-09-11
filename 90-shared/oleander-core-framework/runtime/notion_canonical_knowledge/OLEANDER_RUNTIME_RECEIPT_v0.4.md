# OLEANDER Notion Canonical Knowledge Runtime Receipt v0.4

Date: 2026-09-12

Status: **RUNTIME CONSUMPTION READBACK PASS / FULL RECONCILE DRAINING / AUTOMATIC CRON READBACK PENDING / CORPUS NOT SYNCED**

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
  - `9d7dafe1` — bearer-protected `drain-once` operator trigger for the same durable state machine
- Latest PR checks at `9d7dafe1`: AI Governance PASS / Anti-Pollution PASS / Vercel PASS.
- PR remains draft until automatic Cron continuation is read back. Do not force-merge only because CI and manual operator drain are green.

## 3. Production Deployment Receipt

- D1 migration `0004_durable_sync_scheduler.sql`: APPLIED.
- Worker version: `64ebe2ee-7dd8-417b-9197-04c687b2051e`.
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

Two earlier `QUEUE_ERROR` events that had already been manually persisted as D1 fallback tasks were normalized to the same fallback state.

Production `drain-once` readback then processed all seven persisted fallback events through the same D1 scheduler. Their durable task state is now `PROCESSED`, and the corresponding webhook lifecycle closes to `PROCESSED`. This proves both the **incremental failover write path** and the **durable recovery consumption path** in production.

## 7. Scheduled Reconcile State

- The full reconcile was started through the production bearer-protected `/v1/reconcile` path rather than waiting for Cron propagation to seed the worklist.
- Run id: `9b40de03-96d5-40b1-be84-0f137e7d248e`.
- Pages scheduled durably in D1: `1,184`.
- The obsolete one-time `scheduled_reconcile_request` was deleted after the direct production seed to prevent a duplicate 1,184-page run when Cron propagation completes.
- The protected `/v1/drain-once` operator trigger executes exactly the same one-page D1 drain function as `scheduled()`. Production readback has processed one full-reconcile task to `PROCESSED`; the run therefore moved from `SCHEDULED` to `DRAINING`.
- A remote preview `scheduled()` smoke test reached the scheduler code path but lacked the production Notion secret in the preview environment. That run was relabeled `REMOTE_PREVIEW_SCHEDULER_TEST` and must not be interpreted as a production credential failure.
- Automatic Cron continuation remains a separate readback gate: after propagation it must consume at least one additional task without an operator trigger.

## 8. Corpus Boundary

Current verified corpus snapshot after production durable draining began:

- Notes scheduled by current full reconcile: `1,184`
- Durable task state: `8 PROCESSED / 1,183 PENDING` across webhook fallback + full reconcile tasks.
- Current full reconcile task proof: first run-owned page is `PROCESSED` with `attempts=1` and no error.
- D1 indexed documents: `197` (up from the pre-hardening snapshot of `194`).
- Corpus status: **PARTIAL**

Do not report `NOTION SYNCED`, `1184/1184`, or equivalent until the new full run reaches a closed task readback with no unresolved `PENDING / PROCESSING / RETRY / BLOCKED` items.

## 9. Promotion Gate

Runtime implementation may be promoted only after:

1. production durable worklist is created without Queue dependency — **PASS**;
2. real webhook fallback tasks transition to `PROCESSED` — **PASS**;
3. at least one current full-reconcile task transitions to `PROCESSED` — **PASS**;
4. automatic Cron consumes at least one additional due task without operator trigger — **PENDING**;
5. PR #521 remains CI-green after the latest receipt update — **PENDING RECHECK**;
6. Notion lifecycle page and GitHub runtime receipt agree on the same state — **Notion page was updated through the deployed scheduler milestone; final automatic-Cron state must still be reflected after gate 4**.

Corpus promotion is a separate later gate and requires full reconcile closure.
