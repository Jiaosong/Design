PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS webhook_events (
  event_id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  entity_id TEXT,
  event_timestamp TEXT,
  received_at TEXT NOT NULL,
  queued_at TEXT,
  processed_at TEXT,
  status TEXT NOT NULL,
  error TEXT
);

CREATE TABLE IF NOT EXISTS documents (
  page_id TEXT PRIMARY KEY,
  canonical_id TEXT,
  title TEXT NOT NULL DEFAULT '',
  notion_url TEXT,
  notion_last_edited_time TEXT,
  retrieval_space TEXT,
  effective_space TEXT,
  search_eligibility TEXT,
  trust_state TEXT,
  governance_state TEXT,
  relation_state TEXT,
  content_level TEXT,
  knowledge_role TEXT,
  primary_domain_ids_json TEXT NOT NULL DEFAULT '[]',
  related_domain_ids_json TEXT NOT NULL DEFAULT '[]',
  source_relation_ids_json TEXT NOT NULL DEFAULT '[]',
  method_relation_ids_json TEXT NOT NULL DEFAULT '[]',
  replacement_ids_json TEXT NOT NULL DEFAULT '[]',
  replaced_document_ids_json TEXT NOT NULL DEFAULT '[]',
  content_hash TEXT,
  structure_hash TEXT,
  markdown_truncated INTEGER NOT NULL DEFAULT 0,
  unknown_block_ids_json TEXT NOT NULL DEFAULT '[]',
  index_state TEXT NOT NULL DEFAULT 'PENDING',
  authority_reason TEXT,
  in_trash INTEGER NOT NULL DEFAULT 0,
  active INTEGER NOT NULL DEFAULT 1,
  observed_at TEXT NOT NULL,
  indexed_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_documents_canonical_id ON documents(canonical_id);
CREATE INDEX IF NOT EXISTS idx_documents_effective_space ON documents(effective_space, active);
CREATE INDEX IF NOT EXISTS idx_documents_index_state ON documents(index_state, active);

CREATE TABLE IF NOT EXISTS chunks (
  vector_id TEXT PRIMARY KEY,
  page_id TEXT NOT NULL,
  ordinal INTEGER NOT NULL,
  namespace TEXT NOT NULL,
  heading_path TEXT NOT NULL DEFAULT '',
  token_estimate INTEGER NOT NULL,
  text_hash TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  chunk_text TEXT NOT NULL,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(page_id) REFERENCES documents(page_id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_chunks_page_ordinal ON chunks(page_id, ordinal, namespace);
CREATE INDEX IF NOT EXISTS idx_chunks_page_active ON chunks(page_id, active);
CREATE INDEX IF NOT EXISTS idx_chunks_namespace_active ON chunks(namespace, active);

CREATE TABLE IF NOT EXISTS lineage_edges (
  source_page_id TEXT NOT NULL,
  relation_type TEXT NOT NULL,
  target_page_id TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  PRIMARY KEY(source_page_id, relation_type, target_page_id)
);

CREATE INDEX IF NOT EXISTS idx_lineage_target ON lineage_edges(target_page_id, relation_type);

CREATE TABLE IF NOT EXISTS sync_runs (
  run_id TEXT PRIMARY KEY,
  run_type TEXT NOT NULL,
  started_at TEXT NOT NULL,
  completed_at TEXT,
  pages_enqueued INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL,
  error TEXT
);
