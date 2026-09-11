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
  sourceRelations: "来源文档",
  methodRelations: "引用方法",
  replacements: "替代文档",
  replacedDocuments: "被替代文档",
} as const;

export const VALID_EXPLICIT_SPACES = new Set(["CURRENT", "SUPPORT", "PROVENANCE", "EXCLUDED"]);
export const VALID_ELIGIBILITY = new Set(["DEFAULT", "SCOPED", "HISTORY_ONLY", "BLOCKED"]);

export const VECTOR_NAMESPACES = ["CURRENT", "SUPPORT", "PROVENANCE"] as const;

// Conservative against the 512-token embedding contract used by Cloudflare AI Search
// so OLEANDER metadata (title/id/role/path) still fits around the chunk body.
export const CHUNK_MAX_ESTIMATED_TOKENS = 320;
export const CHUNK_OVERLAP_ESTIMATED_TOKENS = 40;
export const MAX_UNKNOWN_BLOCK_FETCHES = 100;

// Notion documents an average limit of ~3 requests/second per connection.
// With Queue max_concurrency=1, 400ms between outbound Notion requests keeps
// the canonical ingest path below that average while still allowing progress.
export const NOTION_MIN_REQUEST_INTERVAL_MS = 400;
export const NOTION_MAX_FETCH_ATTEMPTS = 5;
