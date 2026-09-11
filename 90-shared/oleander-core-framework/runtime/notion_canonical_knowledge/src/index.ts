import {
  SCHEDULED_SYNC_BATCH_SIZE,
  SCHEDULED_SYNC_MAX_ATTEMPTS,
  SCHEDULED_SYNC_STALE_PROCESSING_MS,
} from "./config";
import { sha256Hex } from "./hash";
import {
  beginSyncRun,
  claimDueSyncTasks,
  completeSyncRun,
  deleteRuntimeState,
  failSyncRun,
  getRuntimeState,
  markWebhookFallbackFailure,
  markWebhookFallbackScheduled,
  markWebhookProcessed,
  markWebhookQueued,
  markWebhookQueueError,
  putRuntimeState,
  recordSyncMessageReceipt,
  recordWebhookReceived,
  refreshSyncRunStatus,
  requeueStaleSyncTasks,
  stageSyncMessages,
  syncRunReadback,
} from "./manifest";
import { listNotesPages } from "./notion";
import { decryptSetupSecret, encryptSetupSecret, isAuthorized, verifyNotionSignature } from "./security";
import { knowledgePackByCanonicalId, knowledgeSearch } from "./search";
import { syncPage } from "./sync";
import type { Env, IngestMessage, NotionWebhookEvent, SearchRequest } from "./types";

function json(data: unknown, status = 200): Response {
  return Response.json(data, { status, headers: { "Cache-Control": "no-store" } });
}

function errorJson(error: unknown, status = 500): Response {
  const message = error instanceof Error ? error.message : String(error);
  return json({ ok: false, error: message }, status);
}

async function handleWebhook(request: Request, env: Env): Promise<Response> {
  const rawBody = await request.text();
  let payload: NotionWebhookEvent;
  try {
    payload = JSON.parse(rawBody) as NotionWebhookEvent;
  } catch {
    return json({ ok: false, error: "invalid_json" }, 400);
  }

  // One-time subscription handshake. The token is intentionally never echoed back.
  if (payload.verification_token) {
    if (env.OLEANDER_API_TOKEN) {
      const encrypted = await encryptSetupSecret(payload.verification_token, env.OLEANDER_API_TOKEN);
      await putRuntimeState(env.MANIFEST, "pending_notion_webhook_verification_token", encrypted);
    }
    return json({
      ok: true,
      verification_received: true,
      instruction: "Retrieve the pending token through the bearer-protected /v1/webhook-setup-token endpoint, store it as NOTION_WEBHOOK_VERIFICATION_TOKEN, then DELETE that endpoint state.",
    });
  }

  const valid = await verifyNotionSignature(
    rawBody,
    env.NOTION_WEBHOOK_VERIFICATION_TOKEN,
    request.headers.get("X-Notion-Signature"),
  );
  if (!valid) return json({ ok: false, error: "invalid_signature" }, 401);

  const eventId = payload.id;
  const eventType = payload.type;
  const entityId = payload.entity?.id;
  if (!eventId || !eventType) return json({ ok: false, error: "missing_event_identity" }, 400);

  const record = await recordWebhookReceived(env.MANIFEST, {
    id: eventId,
    type: eventType,
    entityId: entityId ?? null,
    timestamp: payload.timestamp ?? null,
  });
  if (!entityId || !eventType.startsWith("page.")) {
    return json({ ok: true, ignored: true, reason: "non_page_event_or_missing_entity", event_id: eventId });
  }
  if (!record.inserted && record.status !== "QUEUE_ERROR" && record.status !== "RECEIVED") {
    return json({ ok: true, duplicate: true, event_id: eventId });
  }

  const message: IngestMessage = {
    kind: "notion-page-sync",
    page_id: entityId,
    cause_id: eventId,
    cause_type: "webhook",
    event_type: eventType,
    ...(payload.timestamp ? { event_timestamp: payload.timestamp } : {}),
  };
  try {
    await env.INGEST_QUEUE.send(message, { contentType: "json" });
    await markWebhookQueued(env.MANIFEST, eventId);
    return json({ ok: true, queued: true, event_id: eventId }, 202);
  } catch (error) {
    const queueError = error instanceof Error ? error.message : String(error);
    try {
      await stageSyncMessages(env.MANIFEST, [message]);
      await markWebhookFallbackScheduled(env.MANIFEST, eventId, queueError);
      return json({ ok: true, queued: false, fallback_scheduled: true, event_id: eventId }, 202);
    } catch (fallbackError) {
      await markWebhookQueueError(
        env.MANIFEST,
        eventId,
        `queue=${queueError}; fallback=${fallbackError instanceof Error ? fallbackError.message : String(fallbackError)}`,
      );
      return errorJson(fallbackError, 503);
    }
  }
}

async function handleReconcile(request: Request, env: Env): Promise<Response> {
  if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
  const body = (await request.json().catch(() => ({}))) as { page_id?: string; limit?: number };
  const limit = Number.isFinite(body.limit) ? Math.max(1, Math.min(1000, Math.floor(body.limit as number))) : undefined;
  const runId = crypto.randomUUID();
  const mode = body.page_id ? "MANUAL_PAGE" : limit ? "BOUNDED_NOTES_RECONCILE" : "FULL_NOTES_RECONCILE";
  await beginSyncRun(env.MANIFEST, runId, mode);
  let count = 0;
  try {
    if (body.page_id) {
      const cause = `reconcile:${runId}:${body.page_id}`;
      await stageSyncMessages(env.MANIFEST, [
        { kind: "notion-page-sync", page_id: body.page_id, cause_id: cause, cause_type: "manual" },
      ]);
      count = 1;
    } else {
      const messages: IngestMessage[] = [];
      for await (const pageId of listNotesPages(env)) {
        messages.push({ kind: "notion-page-sync", page_id: pageId, cause_id: `reconcile:${runId}:${pageId}`, cause_type: "reconcile" });
        if (limit && count + messages.length >= limit) break;
        if (messages.length >= 100) {
          await stageSyncMessages(env.MANIFEST, messages);
          count += messages.length;
          messages.length = 0;
        }
      }
      if (messages.length) {
        await stageSyncMessages(env.MANIFEST, messages);
        count += messages.length;
      }
    }
    await completeSyncRun(env.MANIFEST, runId, count);
    return json({ ok: true, run_id: runId, mode, limit: limit ?? null, pages_scheduled: count, scheduler: "D1_CRON" }, 202);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    await failSyncRun(env.MANIFEST, runId, count, message);
    throw error;
  }
}

async function handleRequest(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  if (request.method === "GET" && url.pathname === "/health") {
    return json({ ok: true, service: "oleander-notion-canonical-knowledge", version: "0.1.0" });
  }
  if (request.method === "POST" && url.pathname === "/webhooks/notion") return handleWebhook(request, env);
  if (request.method === "POST" && url.pathname === "/v1/reconcile") return handleReconcile(request, env);

  if (request.method === "POST" && url.pathname === "/v1/drain-once") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    await drainScheduledSync(env);
    return json({ ok: true, drained: true, batch_size: SCHEDULED_SYNC_BATCH_SIZE });
  }

  if (request.method === "GET" && url.pathname === "/v1/reconcile-status") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    const runId = url.searchParams.get("run_id");
    if (!runId) return json({ ok: false, error: "run_id_required" }, 400);
    const readback = await syncRunReadback(env.MANIFEST, runId);
    return readback ? json({ ok: true, run: readback }) : json({ ok: false, error: "not_found" }, 404);
  }

  if (request.method === "GET" && url.pathname === "/v1/queue-metrics") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    const [ingest, dlq] = await Promise.all([env.INGEST_QUEUE.metrics(), env.INGEST_DLQ.metrics()]);
    return json({
      ok: true,
      ingest: {
        queue: "oleander-notion-ingest",
        backlog_count: ingest.backlogCount,
        backlog_bytes: ingest.backlogBytes,
        oldest_message_timestamp: ingest.oldestMessageTimestamp?.toISOString() ?? null,
      },
      dlq: {
        queue: "oleander-notion-ingest-dlq",
        backlog_count: dlq.backlogCount,
        backlog_bytes: dlq.backlogBytes,
        oldest_message_timestamp: dlq.oldestMessageTimestamp?.toISOString() ?? null,
      },
    });
  }

  if (url.pathname === "/v1/webhook-setup-token") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    if (request.method === "GET") {
      const pending = await getRuntimeState(env.MANIFEST, "pending_notion_webhook_verification_token");
      if (!pending) return json({ ok: false, error: "not_found" }, 404);
      return json({
        ok: true,
        verification_token: await decryptSetupSecret(pending.value, env.OLEANDER_API_TOKEN),
        captured_at: pending.updated_at,
        instruction: "Set this value as NOTION_WEBHOOK_VERIFICATION_TOKEN, then DELETE /v1/webhook-setup-token.",
      });
    }
    if (request.method === "DELETE") {
      await deleteRuntimeState(env.MANIFEST, "pending_notion_webhook_verification_token");
      return json({ ok: true, cleared: true });
    }
  }

  if (request.method === "POST" && url.pathname === "/v1/search") {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    try {
      const body = (await request.json()) as SearchRequest;
      return json(await knowledgeSearch(env, body));
    } catch (error) {
      return errorJson(error, 400);
    }
  }

  const canonicalMatch = /^\/v1\/knowledge-pack\/([^/]+)$/.exec(url.pathname);
  if (request.method === "GET" && canonicalMatch) {
    if (!isAuthorized(request, env.OLEANDER_API_TOKEN)) return json({ ok: false, error: "unauthorized" }, 401);
    const canonicalId = decodeURIComponent(canonicalMatch[1] ?? "");
    const pack = await knowledgePackByCanonicalId(env, canonicalId);
    return pack ? json(pack) : json({ ok: false, error: "not_found" }, 404);
  }
  return json({ ok: false, error: "not_found" }, 404);
}

function retryDelaySeconds(attempts: number): number {
  return Math.min(3600, 60 * 2 ** Math.max(0, attempts - 1));
}

async function seedOperatorRequestedReconcile(env: Env): Promise<boolean> {
  const request = await getRuntimeState(env.MANIFEST, "scheduled_reconcile_request");
  if (!request || !request.value.startsWith("REQUESTED")) return false;

  const [, requestedLimit] = request.value.split(":", 2);
  const parsedLimit = requestedLimit ? Number.parseInt(requestedLimit, 10) : Number.NaN;
  const limit = Number.isFinite(parsedLimit) ? Math.max(1, Math.min(1000, parsedLimit)) : undefined;
  const runId = crypto.randomUUID();
  const mode = limit ? "OPERATOR_BOUNDED_RECONCILE" : "OPERATOR_FULL_RECONCILE";
  await putRuntimeState(env.MANIFEST, "scheduled_reconcile_request", `CLAIMED:${runId}`);
  await beginSyncRun(env.MANIFEST, runId, mode);

  let count = 0;
  try {
    const messages: IngestMessage[] = [];
    for await (const pageId of listNotesPages(env)) {
      messages.push({ kind: "notion-page-sync", page_id: pageId, cause_id: `reconcile:${runId}:${pageId}`, cause_type: "reconcile" });
      if (limit && count + messages.length >= limit) break;
      if (messages.length >= 100) {
        await stageSyncMessages(env.MANIFEST, messages);
        count += messages.length;
        messages.length = 0;
      }
    }
    if (messages.length) {
      await stageSyncMessages(env.MANIFEST, messages);
      count += messages.length;
    }
    await completeSyncRun(env.MANIFEST, runId, count);
    await putRuntimeState(
      env.MANIFEST,
      "scheduled_reconcile_last_run",
      JSON.stringify({ run_id: runId, mode, pages_scheduled: count, scheduled_at: new Date().toISOString() }),
    );
    await deleteRuntimeState(env.MANIFEST, "scheduled_reconcile_request");
    return true;
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    await failSyncRun(env.MANIFEST, runId, count, message);
    await putRuntimeState(env.MANIFEST, "scheduled_reconcile_request", `ERROR:${runId}:${message.slice(0, 1000)}`);
    throw error;
  }
}

async function drainScheduledSync(env: Env): Promise<void> {
  // Seeding a full reconcile can enumerate >1k Notion rows and persist >1k D1
  // tasks. Do not also process a page in that same Free-plan Cron invocation.
  if (await seedOperatorRequestedReconcile(env)) return;
  const staleBefore = new Date(Date.now() - SCHEDULED_SYNC_STALE_PROCESSING_MS).toISOString();
  await requeueStaleSyncTasks(env.MANIFEST, staleBefore);
  const tasks = await claimDueSyncTasks(env.MANIFEST, SCHEDULED_SYNC_BATCH_SIZE);
  const touchedRuns = new Set<string>();

  for (const task of tasks) {
    const message: IngestMessage = {
      kind: "notion-page-sync",
      page_id: task.page_id,
      cause_id: task.cause_id,
      cause_type: task.cause_type,
      ...(task.event_type ? { event_type: task.event_type } : {}),
    };
    if (task.run_id) touchedRuns.add(task.run_id);
    try {
      await syncPage(env, message);
      await recordSyncMessageReceipt(env.MANIFEST, {
        causeId: task.cause_id,
        pageId: task.page_id,
        causeType: task.cause_type,
        eventType: task.event_type,
        status: "PROCESSED",
        attempts: task.attempts,
      });
      if (task.cause_type === "webhook") await markWebhookProcessed(env.MANIFEST, task.cause_id);
    } catch (error) {
      const messageText = error instanceof Error ? error.message : String(error);
      const blocked = task.attempts >= SCHEDULED_SYNC_MAX_ATTEMPTS;
      const nextAttemptAt = blocked
        ? null
        : new Date(Date.now() + retryDelaySeconds(task.attempts) * 1000).toISOString();
      await recordSyncMessageReceipt(env.MANIFEST, {
        causeId: task.cause_id,
        pageId: task.page_id,
        causeType: task.cause_type,
        eventType: task.event_type,
        status: blocked ? "BLOCKED" : "RETRY",
        attempts: task.attempts,
        error: messageText,
        nextAttemptAt,
      });
      if (task.cause_type === "webhook") {
        await markWebhookFallbackFailure(env.MANIFEST, task.cause_id, messageText, blocked);
      }
      console.error("scheduled_knowledge_ingest_failed", {
        cause_id: task.cause_id,
        page_id: task.page_id,
        attempts: task.attempts,
        blocked,
        next_attempt_at: nextAttemptAt,
        error: messageText,
        fingerprint: await sha256Hex(`${task.page_id}:${task.cause_id}`),
      });
    }
  }

  for (const runId of touchedRuns) await refreshSyncRunStatus(env.MANIFEST, runId);
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    try {
      return await handleRequest(request, env);
    } catch (error) {
      return errorJson(error);
    }
  },

  async queue(batch: MessageBatch<IngestMessage>, env: Env): Promise<void> {
    for (const message of batch.messages) {
      try {
        if (message.body.kind !== "notion-page-sync") {
          message.ack();
          continue;
        }
        await syncPage(env, message.body);
        if (message.body.cause_id.startsWith("reconcile:")) {
          await recordSyncMessageReceipt(env.MANIFEST, {
            causeId: message.body.cause_id,
            pageId: message.body.page_id,
            causeType: message.body.cause_type,
            eventType: message.body.event_type ?? null,
            status: "PROCESSED",
            attempts: message.attempts,
          });
        }
        if (message.body.cause_type === "webhook") await markWebhookProcessed(env.MANIFEST, message.body.cause_id);
        message.ack();
      } catch (error) {
        if (message.body.cause_id.startsWith("reconcile:")) {
          await recordSyncMessageReceipt(env.MANIFEST, {
            causeId: message.body.cause_id,
            pageId: message.body.page_id,
            causeType: message.body.cause_type,
            eventType: message.body.event_type ?? null,
            status: "RETRY",
            attempts: message.attempts,
            error: error instanceof Error ? error.message : String(error),
          });
        }
        console.error("knowledge_ingest_failed", {
          queue_message_id: message.id,
          cause_id: message.body.cause_id,
          page_id: message.body.page_id,
          attempts: message.attempts,
          error: error instanceof Error ? error.message : String(error),
          fingerprint: await sha256Hex(`${message.body.page_id}:${message.body.cause_id}`),
        });
        message.retry({ delaySeconds: Math.min(900, 2 ** Math.min(message.attempts, 9)) });
      }
    }
  },

  async scheduled(controller: ScheduledController, env: Env, _ctx: ExecutionContext): Promise<void> {
    const startedAt = new Date().toISOString();
    await putRuntimeState(
      env.MANIFEST,
      "scheduled_cron_last_seen",
      JSON.stringify({
        started_at: startedAt,
        scheduled_time: new Date(controller.scheduledTime).toISOString(),
        cron: controller.cron,
      }),
    );
    try {
      await drainScheduledSync(env);
      await putRuntimeState(
        env.MANIFEST,
        "scheduled_cron_last_result",
        JSON.stringify({ ok: true, started_at: startedAt, completed_at: new Date().toISOString() }),
      );
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      await putRuntimeState(
        env.MANIFEST,
        "scheduled_cron_last_result",
        JSON.stringify({ ok: false, started_at: startedAt, failed_at: new Date().toISOString(), error: message.slice(0, 1000) }),
      );
      throw error;
    }
  },
} satisfies ExportedHandler<Env, IngestMessage>;
