CREATE TABLE IF NOT EXISTS sync_message_receipts (
  cause_id TEXT PRIMARY KEY,
  run_id TEXT,
  page_id TEXT NOT NULL,
  status TEXT NOT NULL,
  attempts INTEGER NOT NULL DEFAULT 0,
  error TEXT,
  updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sync_message_receipts_run_status
  ON sync_message_receipts(run_id, status, updated_at);
