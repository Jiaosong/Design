ALTER TABLE sync_message_receipts ADD COLUMN cause_type TEXT NOT NULL DEFAULT 'reconcile';
ALTER TABLE sync_message_receipts ADD COLUMN event_type TEXT;
ALTER TABLE sync_message_receipts ADD COLUMN next_attempt_at TEXT;
ALTER TABLE sync_message_receipts ADD COLUMN created_at TEXT;

UPDATE sync_message_receipts
SET created_at = COALESCE(created_at, updated_at)
WHERE created_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_sync_message_receipts_due
  ON sync_message_receipts(status, next_attempt_at, updated_at);

CREATE INDEX IF NOT EXISTS idx_sync_message_receipts_run
  ON sync_message_receipts(run_id, status, updated_at);
