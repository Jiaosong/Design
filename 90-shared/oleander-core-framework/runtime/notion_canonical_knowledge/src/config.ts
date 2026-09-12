export const FIELDS = {
  title: "Name",
  canonicalId: "Canonical ID",
  retrievalSpace: "Retrieval Space｜检索空间",
  searchEligibility: "Search Eligibility｜检索资格",
  trustState: "Trust State｜可信状态",
  governanceState: "治理状态",
  relationState: "关系状态",
  contentLevel: "内容层级",
  knowledgeRole: "知识角色",
  primaryDomain: "主领域",
  relatedDomains: "关联领域",
  canonicalParent: "Canonical Parent｜层级上位",
  canonicalChildren: "Canonical Children｜层级子级",
  methodFamily: "方法家族",
  sourceRelations: "来源文档",
  methodRelations: "引用方法",
  replacements: "替代文档",
  replacedDocuments: "被替代文档",
} as const;

// These are existing Current Domain registry fields. The Reader consumes their
// live values as identity/readback facts; it does not maintain a UUID→semantic
// name map or create a second domain taxonomy.
export const DOMAIN_FIELDS = {
  title: "Name",
  level: "层级深度",
  frameworkPath: "框架路径",
  governanceState: "治理状态",
} as const;

export const VALID_EXPLICIT_SPACES = new Set(["CURRENT", "SUPPORT", "PROVENANCE", "EXCLUDED"]);
export const VALID_ELIGIBILITY = new Set(["DEFAULT", "SCOPED", "HISTORY_ONLY", "BLOCKED"]);

export const VECTOR_NAMESPACES = ["CURRENT", "SUPPORT", "PROVENANCE"] as const;

// Conservative against the 512-token embedding contract used by Cloudflare AI Search
// so OLEANDER metadata (title/id/role/path) still fits around the chunk body.
export const CHUNK_MAX_ESTIMATED_TOKENS = 320;
export const CHUNK_OVERLAP_ESTIMATED_TOKENS = 40;
// Workers AI embedding models enforce a request-level context ceiling across
// the entire text array. The local CJK-aware estimate is deliberately cheap
// and can under-count the provider tokenizer by roughly 1.5x on mixed pages.
// Keep the request budget at 32k estimated tokens so even that observed ratio
// remains comfortably below bge-m3's 60k-token ceiling without dropping chunks.
export const EMBEDDING_BATCH_MAX_ESTIMATED_TOKENS = 32_000;
export const MAX_UNKNOWN_BLOCK_FETCHES = 100;

// Notion documents an average limit of ~3 requests/second per connection.
// With Queue max_concurrency=1, 400ms between outbound Notion requests keeps
// the canonical ingest path below that average while still allowing progress.
export const NOTION_MIN_REQUEST_INTERVAL_MS = 400;
export const NOTION_MAX_FETCH_ATTEMPTS = 5;

// Full reconciles use D1 as a durable scheduler rather than Cloudflare Queues.
// This keeps bulk maintenance independent from the Queues Free-plan operation
// budget while leaving Queue available as the low-latency webhook fast path.
// Workers Free Cron invocations have a 10 ms CPU budget. Keep each scheduled
// drain to one page so the CPU profile matches the already-proven one-page
// Queue consumer path; network/storage wait time does not count as CPU time.
export const SCHEDULED_SYNC_BATCH_SIZE = 1;
export const SCHEDULED_SYNC_MAX_ATTEMPTS = 8;
export const SCHEDULED_SYNC_STALE_PROCESSING_MS = 15 * 60 * 1000;

// Webhooks remain the primary near-real-time path. The incremental sweep is a
// cloud-side safety net for missed/delayed webhook delivery and therefore runs
// much less often than the one-minute durable-task drain. Each sweep page is
// bounded to one Notion data-source query (100 rows) per invocation.
export const INCREMENTAL_SYNC_INTERVAL_MS = 10 * 60 * 1000;
export const INCREMENTAL_SYNC_OVERLAP_MS = 2 * 60 * 1000;
export const INVENTORY_SYNC_INTERVAL_MS = 24 * 60 * 60 * 1000;

// This revision describes the indexing semantics, not the orchestration code.
// Bump it only when authority/chunk/embedding semantics change and a rebuild is
// actually required. Migration 0005 backfills the existing production corpus
// to this same revision because this change only alters sync orchestration.
export const INDEX_PIPELINE_REVISION = "knowledge-index-v1";
