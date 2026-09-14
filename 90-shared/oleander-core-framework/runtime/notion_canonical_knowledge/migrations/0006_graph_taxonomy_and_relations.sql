-- Persist the revised Level × Role × Framework Type taxonomy and the full
-- typed knowledge-graph relation surface in the derivative manifest.
-- Notion remains canonical; these columns support bounded readback/fallback.

ALTER TABLE documents ADD COLUMN framework_type TEXT;
ALTER TABLE documents ADD COLUMN canonical_parent_ids_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN canonical_children_ids_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN semantic_related_ids_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN primary_project_ids_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN related_project_ids_json TEXT NOT NULL DEFAULT '[]';

CREATE INDEX IF NOT EXISTS idx_documents_framework_type ON documents(framework_type, active);
