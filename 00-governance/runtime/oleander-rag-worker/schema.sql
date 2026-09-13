PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS knowledge_object (
  canonical_id TEXT PRIMARY KEY,
  source_kind TEXT NOT NULL,
  source_locator TEXT NOT NULL,
  notion_page_id TEXT,
  title TEXT NOT NULL,
  retrieval_space TEXT NOT NULL,
  search_eligibility TEXT NOT NULL,
  governance_state TEXT NOT NULL,
  trust_state TEXT NOT NULL,
  freshness_state TEXT NOT NULL,
  evidence_grade TEXT,
  authority_class TEXT NOT NULL,
  project_id TEXT NOT NULL DEFAULT 'GLOBAL',
  domain_id TEXT NOT NULL DEFAULT 'GLOBAL',
  knowledge_role TEXT NOT NULL DEFAULT 'UNKNOWN',
  object_type TEXT NOT NULL DEFAULT 'UNKNOWN',
  last_edited_at TEXT,
  last_verified_at TEXT,
  verification_due TEXT,
  content_hash TEXT NOT NULL,
  indexed_content_hash TEXT,
  embedding_model TEXT,
  schema_version TEXT NOT NULL,
  vector_namespace TEXT,
  vector_mutation_id TEXT,
  indexed_at TEXT,
  tombstoned_at TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_knowledge_object_source_locator
  ON knowledge_object(source_locator);
CREATE INDEX IF NOT EXISTS idx_knowledge_object_retrieval
  ON knowledge_object(retrieval_space, search_eligibility, governance_state, trust_state, freshness_state);
CREATE INDEX IF NOT EXISTS idx_knowledge_object_scope
  ON knowledge_object(project_id, domain_id, knowledge_role);
CREATE INDEX IF NOT EXISTS idx_knowledge_object_notion_page
  ON knowledge_object(notion_page_id);

CREATE TABLE IF NOT EXISTS knowledge_alias (
  alias TEXT NOT NULL,
  canonical_id TEXT NOT NULL,
  alias_kind TEXT NOT NULL DEFAULT 'EXACT',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(alias, canonical_id),
  FOREIGN KEY(canonical_id) REFERENCES knowledge_object(canonical_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_knowledge_alias_alias ON knowledge_alias(alias);

CREATE TABLE IF NOT EXISTS knowledge_chunk (
  chunk_id TEXT PRIMARY KEY,
  canonical_id TEXT NOT NULL,
  chunk_ordinal INTEGER NOT NULL,
  section_path TEXT,
  normalized_text TEXT NOT NULL,
  chunk_hash TEXT NOT NULL,
  vector_id TEXT NOT NULL UNIQUE,
  vector_namespace TEXT NOT NULL,
  active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(canonical_id) REFERENCES knowledge_object(canonical_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_knowledge_chunk_canonical
  ON knowledge_chunk(canonical_id, active, chunk_ordinal);

CREATE TABLE IF NOT EXISTS sync_event (
  event_id TEXT PRIMARY KEY,
  notion_page_id TEXT,
  event_type TEXT NOT NULL,
  event_timestamp TEXT,
  delivery_attempt INTEGER,
  raw_hash TEXT NOT NULL,
  received_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  processed_at TEXT,
  status TEXT NOT NULL DEFAULT 'RECEIVED',
  error_code TEXT,
  error_detail TEXT
);
CREATE INDEX IF NOT EXISTS idx_sync_event_page_status
  ON sync_event(notion_page_id, status, received_at);

CREATE TABLE IF NOT EXISTS retrieval_audit (
  query_id TEXT PRIMARY KEY,
  authority_policy TEXT NOT NULL,
  project_id TEXT,
  domain_id TEXT,
  history_intent INTEGER NOT NULL DEFAULT 0,
  top_k INTEGER NOT NULL,
  candidate_count INTEGER NOT NULL DEFAULT 0,
  result_count INTEGER NOT NULL DEFAULT 0,
  conflict_count INTEGER NOT NULL DEFAULT 0,
  support_expansion_used INTEGER NOT NULL DEFAULT 0,
  latency_ms INTEGER,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
