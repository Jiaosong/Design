DROP INDEX IF EXISTS idx_chunks_page_ordinal;
CREATE INDEX IF NOT EXISTS idx_chunks_page_ordinal_history ON chunks(page_id, ordinal, namespace, active);

CREATE TABLE IF NOT EXISTS runtime_state (
  state_key TEXT PRIMARY KEY,
  state_value TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
