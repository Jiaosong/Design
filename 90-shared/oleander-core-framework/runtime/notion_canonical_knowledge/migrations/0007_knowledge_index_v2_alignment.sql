-- OLEANDER Knowledge Index v2 alignment.
-- This extends the existing derivative D1 manifest only. Notion remains
-- canonical. New semantic fields default to NULL / [] / {} so the runtime
-- never manufactures knowledge classifications that are not explicitly bound.
--
-- Runtime/project dependency state (depends_on / stale_if / shared variables)
-- is intentionally not represented here as KNOWLEDGE_DEPENDENCY.

ALTER TABLE documents ADD COLUMN object_plane TEXT NOT NULL DEFAULT 'KNOWLEDGE';
ALTER TABLE documents ADD COLUMN information_role TEXT;
ALTER TABLE documents ADD COLUMN secondary_semantics_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN topic_ids_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN claim_ids_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN evidence_ids_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN capability_links_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN function_links_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN information_entity_links_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN interface_links_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN work_medium_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN design_scale_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN artifact_type TEXT;
ALTER TABLE documents ADD COLUMN symptom_tags_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN affected_relation_tags_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN tool_capability_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN readback_method_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN evidence_grade TEXT;
ALTER TABLE documents ADD COLUMN freshness_state TEXT;
ALTER TABLE documents ADD COLUMN authority_class TEXT;
ALTER TABLE documents ADD COLUMN aliases_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN source_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE documents ADD COLUMN lifecycle_json TEXT NOT NULL DEFAULT '{}';

ALTER TABLE lineage_edges ADD COLUMN relation_family TEXT;

CREATE INDEX IF NOT EXISTS idx_documents_evidence_grade ON documents(evidence_grade, active);
CREATE INDEX IF NOT EXISTS idx_documents_freshness_state ON documents(freshness_state, active);
CREATE INDEX IF NOT EXISTS idx_documents_authority_class ON documents(authority_class, active);
CREATE INDEX IF NOT EXISTS idx_lineage_relation_family ON lineage_edges(relation_family, relation_type);
