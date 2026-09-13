import {
  latestReaderDocumentActivity,
  listExecutionLiveStatus,
  recentReaderSyncTasks,
  recentReaderWebhookEvents,
  schedulerTaskCounts,
} from "./manifest";

export type ReaderKnowledgeSyncState = "IDLE" | "SYNCING" | "DEGRADED" | "BLOCKED";

export function deriveReaderKnowledgeSyncState(counts: Record<string, number>): ReaderKnowledgeSyncState {
  const processing = counts.PROCESSING ?? 0;
  const pending = counts.PENDING ?? 0;
  const retry = counts.RETRY ?? 0;
  const blocked = counts.BLOCKED ?? 0;
  if (blocked > 0 && processing + pending + retry === 0) return "BLOCKED";
  if (blocked > 0 || retry > 0) return "DEGRADED";
  if (processing + pending > 0) return "SYNCING";
  return "IDLE";
}

function latestTimestamp(values: Array<string | null | undefined>): string | null {
  const valid = values
    .filter((value): value is string => Boolean(value) && Number.isFinite(Date.parse(value as string)))
    .sort((a, b) => Date.parse(b) - Date.parse(a));
  return valid[0] ?? null;
}

export async function buildReaderLiveStatus(db: D1Database, pageId: string | null = null, taskId: string | null = null) {
  const [taskCounts, recentTasks, recentWebhooks, documentActivity, executionStatuses] = await Promise.all([
    schedulerTaskCounts(db),
    recentReaderSyncTasks(db, pageId),
    recentReaderWebhookEvents(db, pageId),
    latestReaderDocumentActivity(db, pageId),
    listExecutionLiveStatus(db, taskId),
  ]);
  const openTasks =
    (taskCounts.PENDING ?? 0) +
    (taskCounts.PROCESSING ?? 0) +
    (taskCounts.RETRY ?? 0);
  const blockedTasks = taskCounts.BLOCKED ?? 0;
  const latestActivityAt = latestTimestamp([
    documentActivity.latest_indexed_at,
    documentActivity.latest_observed_at,
    ...recentTasks.map((task) => task.updated_at),
    ...recentWebhooks.map((event) => event.processed_at ?? event.queued_at ?? event.received_at),
  ]);

  return {
    version: "oleander-reader-live-status/v1" as const,
    generatedAt: new Date().toISOString(),
    scope: pageId ? { type: "PAGE" as const, pageId } : { type: "CORPUS" as const },
    projection: {
      source: "Cloudflare D1" as const,
      canonicalAuthority: "Notion" as const,
      authorityCeiling: "DERIVATIVE_RUNTIME_READBACK_ONLY" as const,
      finalityRule: "SYNC_ACTIVITY_DOES_NOT_EQUAL_CANONICAL_OR_EXECUTION_COMPLETION" as const,
    },
    knowledgeSync: {
      state: deriveReaderKnowledgeSyncState(taskCounts),
      openTasks,
      blockedTasks,
      taskCounts,
      latestActivityAt,
      latestIndexedAt: documentActivity.latest_indexed_at,
      latestObservedAt: documentActivity.latest_observed_at,
      recentTasks,
      recentWebhooks,
    },
    execution: {
      state: executionStatuses.length > 0 ? "LIVE_PROJECTION" as const : "NO_LIVE_PROJECTION" as const,
      contract: "00-governance/runtime/OLEANDER_EXECUTION_RECEIPT_v1.0.json" as const,
      authorityCeiling: "OBSERVABILITY_ONLY" as const,
      finalityRule: "WORKER_OR_SKILL_PROGRESS_MUST_NOT_SELF_PROMOTE_TO_VERIFIED_CURRENT_OR_CLOSED" as const,
      recent: executionStatuses,
    },
  };
}
