ALTER TABLE documents ADD COLUMN notion_seen_at TEXT;
ALTER TABLE documents ADD COLUMN index_revision TEXT;

UPDATE documents
SET notion_seen_at = COALESCE(observed_at, indexed_at),
    index_revision = 'knowledge-index-v1'
WHERE notion_seen_at IS NULL OR index_revision IS NULL;

CREATE INDEX IF NOT EXISTS idx_documents_notion_seen
  ON documents(active, notion_seen_at, observed_at);

CREATE INDEX IF NOT EXISTS idx_documents_index_revision
  ON documents(index_revision, active, index_state);
