import type {
  AuthorityDecision,
  IngestMessage,
  ManifestChunkRow,
  NormalizedPage,
  RetrievalSpace,
  SyncTaskRow,
  SyncTaskStatus,
} from "./types";

const now = () => new Date().toISOString();

export async function recordWebhookReceived(
  db: D1Database,
  event: { id: string; type: string; entityId: string | null; timestamp: string | null },
): Promise<{ inserted: boolean; status: string | null }> {
  const receivedAt = now();
  const result = await db
    .prepare(
      `INSERT OR IGNORE INTO webhook_events
       (event_id, event_type, entity_id, event_timestamp, received_at, status)
       VALUES (?, ?, ?, ?, ?, 'RECEIVED')`,
    )
    .bind(event.id, event.type, event.entityId, event.timestamp, receivedAt)
    .run();
  const row = await db.prepare("SELECT status FROM webhook_events WHERE event_id = ?").bind(event.id).first<{ status: string }>();
  return { inserted: (result.meta.changes ?? 0) > 0, status: row?.status ?? null };
}

export async function markWebhookQueued(db: D1Database, eventId: string): Promise<void> {
  await db.prepare("UPDATE webhook_events SET status='QUEUED', queued_at=?, error=NULL WHERE event_id=?").bind(now(), eventId).run();
}

export async function markWebhookQueueError(db: D1Database, eventId: string, error: string): Promise<void> {
  await db.prepare("UPDATE webhook_events SET status='QUEUE_ERROR', error=? WHERE event_id=?").bind(error.slice(0, 2000), eventId).run();
}

export async function markWebhookFallbackScheduled(db: D1Database, eventId: string, error: string): Promise<void> {
  await db
    .prepare("UPDATE webhook_events SET status='FALLBACK_SCHEDULED', error=? WHERE event_id=?")
    .bind(error.slice(0, 2000), eventId)
    .run();
}

export async function markWebhookFallbackFailure(
  db: D1Database,
  eventId: string,
  error: string,
  blocked: boolean,
): Promise<void> {
  await db
    .prepare("UPDATE webhook_events SET status=?, error=? WHERE event_id=?")
    .bind(blocked ? "FALLBACK_BLOCKED" : "FALLBACK_RETRY", error.slice(0, 2000), eventId)
    .run();
}

export async function markWebhookProcessed(db: D1Database, eventId: string): Promise<void> {
  await db.prepare("UPDATE webhook_events SET status='PROCESSED', processed_at=?, error=NULL WHERE event_id=?").bind(now(), eventId).run();
}

export async function getActiveVectorIds(db: D1Database, pageId: string): Promise<string[]> {
  const rows = await db.prepare("SELECT vector_id FROM chunks WHERE page_id=? AND active=1").bind(pageId).all<{ vector_id: string }>();
  return rows.results.map((row) => row.vector_id);
}

export async function deactivatePage(db: D1Database, pageId: string, reason: string): Promise<string[]> {
  const ids = await getActiveVectorIds(db, pageId);
  await db.batch([
    db.prepare("UPDATE chunks SET active=0, updated_at=? WHERE page_id=? AND active=1").bind(now(), pageId),
    db
      .prepare("UPDATE documents SET active=0, index_state='INACTIVE', authority_reason=?, observed_at=? WHERE page_id=?")
      .bind(reason, now(), pageId),
  ]);
  return ids;
}

function relations(page: NormalizedPage): Array<{ type: string; target: string }> {
  return [
    ...page.sourceRelationIds.map((target) => ({ type: "SOURCE", target })),
    ...page.methodRelationIds.map((target) => ({ type: "METHOD", target })),
    ...page.replacementIds.map((target) => ({ type: "REPLACEMENT", target })),
    ...page.replacedDocumentIds.map((target) => ({ type: "REPLACED_DOCUMENT", target })),
  ];
}

export async function saveDocumentAndChunks(
  db: D1Database,
  input: {
    page: NormalizedPage;
    authority: AuthorityDecision;
    contentHash: string;
    structureHash: string;
    truncated: boolean;
    unknownBlockIds: string[];
    chunks: ManifestChunkRow[];
  },
): Promise<void> {
  const observedAt = now();
  const indexedAt = observedAt;
  const p = input.page;
  const statements: D1PreparedStatement[] = [
    db
      .prepare(
        `INSERT INTO documents (
          page_id, canonical_id, title, notion_url, notion_last_edited_time,
          retrieval_space, effective_space, search_eligibility, trust_state,
          governance_state, relation_state, content_level, knowledge_role,
          primary_domain_ids_json, related_domain_ids_json, source_relation_ids_json,
          method_relation_ids_json, replacement_ids_json, replaced_document_ids_json,
          content_hash, structure_hash, markdown_truncated, unknown_block_ids_json,
          index_state, authority_reason, in_trash, active, observed_at, indexed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'INDEXED', ?, ?, 1, ?, ?)
        ON CONFLICT(page_id) DO UPDATE SET
          canonical_id=excluded.canonical_id, title=excluded.title, notion_url=excluded.notion_url,
          notion_last_edited_time=excluded.notion_last_edited_time, retrieval_space=excluded.retrieval_space,
          effective_space=excluded.effective_space, search_eligibility=excluded.search_eligibility,
          trust_state=excluded.trust_state, governance_state=excluded.governance_state,
          relation_state=excluded.relation_state, content_level=excluded.content_level,
          knowledge_role=excluded.knowledge_role, primary_domain_ids_json=excluded.primary_domain_ids_json,
          related_domain_ids_json=excluded.related_domain_ids_json, source_relation_ids_json=excluded.source_relation_ids_json,
          method_relation_ids_json=excluded.method_relation_ids_json, replacement_ids_json=excluded.replacement_ids_json,
          replaced_document_ids_json=excluded.replaced_document_ids_json, content_hash=excluded.content_hash,
          structure_hash=excluded.structure_hash, markdown_truncated=excluded.markdown_truncated,
          unknown_block_ids_json=excluded.unknown_block_ids_json, index_state='INDEXED',
          authority_reason=excluded.authority_reason, in_trash=excluded.in_trash, active=1,
          observed_at=excluded.observed_at, indexed_at=excluded.indexed_at`,
      )
      .bind(
        p.pageId,
        p.canonicalId,
        p.title,
        p.url,
        p.lastEditedTime,
        p.retrievalSpace,
        input.authority.effectiveSpace,
        p.searchEligibility,
        p.trustState,
        p.governanceState,
        p.relationState,
        p.contentLevel,
        p.knowledgeRole,
        JSON.stringify(p.primaryDomainIds),
        JSON.stringify(p.relatedDomainIds),
        JSON.stringify(p.sourceRelationIds),
        JSON.stringify(p.methodRelationIds),
        JSON.stringify(p.replacementIds),
        JSON.stringify(p.replacedDocumentIds),
        input.contentHash,
        input.structureHash,
        input.truncated ? 1 : 0,
        JSON.stringify(input.unknownBlockIds),
        input.authority.reason,
        p.inTrash ? 1 : 0,
        observedAt,
        indexedAt,
      ),
    db.prepare("UPDATE chunks SET active=0, updated_at=? WHERE page_id=?").bind(observedAt, p.pageId),
    db.prepare("DELETE FROM lineage_edges WHERE source_page_id=?").bind(p.pageId),
  ];

  for (const chunk of input.chunks) {
    statements.push(
      db
        .prepare(
          `INSERT INTO chunks (
            vector_id, page_id, ordinal, namespace, heading_path, token_estimate,
            text_hash, content_hash, chunk_text, metadata_json, active, created_at, updated_at
          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
          ON CONFLICT(vector_id) DO UPDATE SET
            page_id=excluded.page_id, ordinal=excluded.ordinal, namespace=excluded.namespace,
            heading_path=excluded.heading_path, token_estimate=excluded.token_estimate,
            text_hash=excluded.text_hash, content_hash=excluded.content_hash,
            chunk_text=excluded.chunk_text, metadata_json=excluded.metadata_json,
            active=1, updated_at=excluded.updated_at`,
        )
        .bind(
          chunk.vector_id,
          chunk.page_id,
          chunk.ordinal,
          chunk.namespace,
          chunk.heading_path,
          chunk.token_estimate,
          chunk.text_hash,
          chunk.content_hash,
          chunk.chunk_text,
          chunk.metadata_json,
          observedAt,
          observedAt,
        ),
    );
  }

  for (const edge of relations(p)) {
    statements.push(
      db
        .prepare("INSERT OR REPLACE INTO lineage_edges (source_page_id, relation_type, target_page_id, observed_at) VALUES (?, ?, ?, ?)")
        .bind(p.pageId, edge.type, edge.target, observedAt),
    );
  }
  await db.batch(statements);
}

export async function fetchManifestHits(
  db: D1Database,
  vectorIds: string[],
  namespace: RetrievalSpace,
  canonicalId?: string,
  allowScoped = false,
): Promise<Map<string, ManifestChunkRow & Record<string, unknown>>> {
  if (vectorIds.length === 0) return new Map();
  const placeholders = vectorIds.map(() => "?").join(",");
  let sql = `SELECT c.*, d.canonical_id, d.title, d.knowledge_role, d.content_level,
                    d.trust_state, d.effective_space, d.index_state, d.active AS document_active
             FROM chunks c JOIN documents d ON d.page_id=c.page_id
             WHERE c.vector_id IN (${placeholders})
               AND c.active=1 AND d.active=1 AND d.index_state='INDEXED'
               AND c.namespace=? AND d.effective_space=?
               AND (
                 d.search_eligibility IS NULL OR d.search_eligibility='DEFAULT'
                 OR (d.search_eligibility='HISTORY_ONLY' AND ?='PROVENANCE')
                 OR (d.search_eligibility='SCOPED' AND ?=1)
               )`;
  const binds: unknown[] = [...vectorIds, namespace, namespace, namespace, allowScoped ? 1 : 0];
  if (canonicalId) {
    sql += " AND d.canonical_id=?";
    binds.push(canonicalId);
  }
  const rows = await db.prepare(sql).bind(...binds).all<ManifestChunkRow & Record<string, unknown>>();
  return new Map(rows.results.map((row) => [row.vector_id, row]));
}

export async function getDocumentByCanonicalId(db: D1Database, canonicalId: string): Promise<Record<string, unknown> | null> {
  return db
    .prepare("SELECT * FROM documents WHERE canonical_id=? AND active=1 ORDER BY indexed_at DESC LIMIT 1")
    .bind(canonicalId)
    .first<Record<string, unknown>>();
}

export async function lineageForPage(db: D1Database, pageId: string): Promise<Array<Record<string, unknown>>> {
  const result = await db
    .prepare("SELECT relation_type, target_page_id, observed_at FROM lineage_edges WHERE source_page_id=? ORDER BY relation_type, target_page_id")
    .bind(pageId)
    .all<Record<string, unknown>>();
  return result.results;
}

export async function beginSyncRun(db: D1Database, runId: string, runType: string): Promise<void> {
  await db
    .prepare("INSERT INTO sync_runs (run_id, run_type, started_at, status) VALUES (?, ?, ?, 'RUNNING')")
    .bind(runId, runType, now())
    .run();
}

export async function completeSyncRun(db: D1Database, runId: string, count: number): Promise<void> {
  await db
    .prepare("UPDATE sync_runs SET completed_at=?, pages_enqueued=?, status='SCHEDULED', error=NULL WHERE run_id=?")
    .bind(now(), count, runId)
    .run();
}

export async function failSyncRun(db: D1Database, runId: string, count: number, error: string): Promise<void> {
  await db
    .prepare("UPDATE sync_runs SET completed_at=?, pages_enqueued=?, status='FAILED', error=? WHERE run_id=?")
    .bind(now(), count, error.slice(0, 2000), runId)
    .run();
}

function runIdFromCause(causeId: string): string | null {
  const match = /^reconcile:([^:]+):/.exec(causeId);
  return match?.[1] ?? null;
}

export async function stageSyncMessages(db: D1Database, messages: IngestMessage[]): Promise<void> {
  for (let i = 0; i < messages.length; i += 100) {
    const stagedAt = now();
    const statements = messages.slice(i, i + 100).map((message) =>
      db
        .prepare(
          `INSERT OR IGNORE INTO sync_message_receipts
           (cause_id, run_id, page_id, cause_type, event_type, status, attempts, error,
            next_attempt_at, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, 'PENDING', 0, NULL, NULL, ?, ?)`,
        )
        .bind(
          message.cause_id,
          runIdFromCause(message.cause_id),
          message.page_id,
          message.cause_type,
          message.event_type ?? null,
          stagedAt,
          stagedAt,
        ),
    );
    if (statements.length) await db.batch(statements);
  }
}

export async function requeueStaleSyncTasks(db: D1Database, staleBefore: string): Promise<number> {
  const result = await db
    .prepare(
      `UPDATE sync_message_receipts
       SET status='RETRY', error=COALESCE(error, 'STALE_PROCESSING_RECOVERED'), next_attempt_at=NULL, updated_at=?
       WHERE status='PROCESSING' AND updated_at < ?`,
    )
    .bind(now(), staleBefore)
    .run();
  return result.meta.changes ?? 0;
}

export async function claimDueSyncTasks(db: D1Database, limit: number): Promise<SyncTaskRow[]> {
  const claimedAt = now();
  const result = await db
    .prepare(
      `UPDATE sync_message_receipts
       SET status='PROCESSING', attempts=attempts+1, updated_at=?
       WHERE cause_id IN (
         SELECT cause_id FROM sync_message_receipts
         WHERE status IN ('PENDING', 'RETRY')
           AND (next_attempt_at IS NULL OR next_attempt_at <= ?)
         ORDER BY COALESCE(next_attempt_at, created_at, updated_at), updated_at, cause_id
         LIMIT ?
       )
       RETURNING cause_id, run_id, page_id, cause_type, event_type, status, attempts,
                 error, next_attempt_at, created_at, updated_at`,
    )
    .bind(claimedAt, claimedAt, Math.max(1, Math.min(100, Math.floor(limit))))
    .all<SyncTaskRow>();
  return result.results;
}

export async function recordSyncMessageReceipt(
  db: D1Database,
  input: {
    causeId: string;
    pageId: string;
    status: SyncTaskStatus;
    attempts: number;
    causeType?: IngestMessage["cause_type"];
    eventType?: string | null;
    error?: string | null;
    nextAttemptAt?: string | null;
  },
): Promise<void> {
  const runId = runIdFromCause(input.causeId);
  const updatedAt = now();
  await db
    .prepare(
      `INSERT INTO sync_message_receipts
       (cause_id, run_id, page_id, cause_type, event_type, status, attempts, error,
        next_attempt_at, created_at, updated_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
       ON CONFLICT(cause_id) DO UPDATE SET
         run_id=excluded.run_id,
         page_id=excluded.page_id,
         cause_type=COALESCE(excluded.cause_type, sync_message_receipts.cause_type),
         event_type=COALESCE(excluded.event_type, sync_message_receipts.event_type),
         status=excluded.status,
         attempts=excluded.attempts,
         error=excluded.error,
         next_attempt_at=excluded.next_attempt_at,
         updated_at=excluded.updated_at`,
    )
    .bind(
      input.causeId,
      runId,
      input.pageId,
      input.causeType ?? "reconcile",
      input.eventType ?? null,
      input.status,
      input.attempts,
      input.error ? input.error.slice(0, 2000) : null,
      input.nextAttemptAt ?? null,
      updatedAt,
      updatedAt,
    )
    .run();
}

export async function syncRunReadback(db: D1Database, runId: string): Promise<Record<string, unknown> | null> {
  const run = await db.prepare("SELECT * FROM sync_runs WHERE run_id=?").bind(runId).first<Record<string, unknown>>();
  if (!run) return null;
  const counts = await db
    .prepare("SELECT status, COUNT(*) AS count FROM sync_message_receipts WHERE run_id=? GROUP BY status")
    .bind(runId)
    .all<{ status: string; count: number }>();
  return {
    ...run,
    task_counts: Object.fromEntries(counts.results.map((row) => [row.status, row.count])),
  };
}

export async function refreshSyncRunStatus(db: D1Database, runId: string): Promise<void> {
  const counts = await db
    .prepare("SELECT status, COUNT(*) AS count FROM sync_message_receipts WHERE run_id=? GROUP BY status")
    .bind(runId)
    .all<{ status: string; count: number }>();
  const byStatus = new Map(counts.results.map((row) => [row.status, row.count]));
  const processed = byStatus.get("PROCESSED") ?? 0;
  const blocked = byStatus.get("BLOCKED") ?? 0;
  const open = (byStatus.get("PENDING") ?? 0) + (byStatus.get("RETRY") ?? 0) + (byStatus.get("PROCESSING") ?? 0);
  const total = counts.results.reduce((sum, row) => sum + row.count, 0);
  if (total === 0 || open > 0) {
    await db.prepare("UPDATE sync_runs SET status='DRAINING' WHERE run_id=? AND status!='FAILED'").bind(runId).run();
    return;
  }
  if (processed === total) {
    await db.prepare("UPDATE sync_runs SET status='COMPLETE', completed_at=?, error=NULL WHERE run_id=?").bind(now(), runId).run();
    return;
  }
  if (blocked > 0) {
    await db
      .prepare("UPDATE sync_runs SET status='PARTIAL_BLOCKED', completed_at=?, error=? WHERE run_id=?")
      .bind(now(), `${blocked} scheduled sync task(s) blocked after bounded retries`, runId)
      .run();
  }
}

export async function putRuntimeState(db: D1Database, key: string, value: string): Promise<void> {
  await db
    .prepare(
      `INSERT INTO runtime_state (state_key, state_value, updated_at) VALUES (?, ?, ?)
       ON CONFLICT(state_key) DO UPDATE SET state_value=excluded.state_value, updated_at=excluded.updated_at`,
    )
    .bind(key, value, now())
    .run();
}

export async function getRuntimeState(db: D1Database, key: string): Promise<{ value: string; updated_at: string } | null> {
  const row = await db
    .prepare("SELECT state_value, updated_at FROM runtime_state WHERE state_key=?")
    .bind(key)
    .first<{ state_value: string; updated_at: string }>();
  return row ? { value: row.state_value, updated_at: row.updated_at } : null;
}

export async function deleteRuntimeState(db: D1Database, key: string): Promise<void> {
  await db.prepare("DELETE FROM runtime_state WHERE state_key=?").bind(key).run();
}
