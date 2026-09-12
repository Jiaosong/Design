import type { KnowledgeReaderSnapshot } from "./types";

const CORE_LEVELS = new Set(["L4｜Framework", "L5｜Knowledge Object"]);
const EVIDENCE_ROLES = new Set(["SOURCE", "EVIDENCE", "CASE"]);
const PRACTICE_ROLES = new Set(["PRACTICE", "TOOL"]);

function isHistory(row: Record<string, unknown>): boolean {
  return row.effective_space === "PROVENANCE" || row.search_eligibility === "HISTORY_ONLY" || row.governance_state === "LEGACY";
}

function readerGroup(row: Record<string, unknown>): "current" | "methods" | "evidence" | "practice" | "history" {
  if (isHistory(row)) return "history";
  const role = String(row.knowledge_role ?? "");
  const level = String(row.content_level ?? "");
  if (role === "METHOD") return "methods";
  if (level === "L6｜Evidence / Case" || EVIDENCE_ROLES.has(role)) return "evidence";
  if (level === "L7｜Practice / Output" || PRACTICE_ROLES.has(role)) return "practice";
  return "current";
}

function cleanedSummary(value: unknown): string | undefined {
  if (typeof value !== "string") return undefined;
  const compact = value.replace(/\s+/g, " ").trim();
  return compact ? compact.slice(0, 520) : undefined;
}

export async function buildKnowledgeReaderSnapshot(db: D1Database): Promise<KnowledgeReaderSnapshot> {
  const [summary, roles, levels, documents] = await Promise.all([
    db.prepare(`
      SELECT
        COUNT(*) AS active,
        SUM(CASE WHEN effective_space='CURRENT' THEN 1 ELSE 0 END) AS explicit_current,
        SUM(CASE WHEN effective_space='SUPPORT' THEN 1 ELSE 0 END) AS support,
        SUM(CASE WHEN effective_space='PROVENANCE' THEN 1 ELSE 0 END) AS provenance,
        SUM(CASE WHEN index_state='INDEXED' THEN 1 ELSE 0 END) AS indexed,
        SUM(CASE WHEN content_level IN ('L4｜Framework','L5｜Knowledge Object')
                  AND governance_state='ACTIVE' AND relation_state='VALID'
                  AND COALESCE(effective_space,'')!='PROVENANCE'
                  AND COALESCE(search_eligibility,'')!='HISTORY_ONLY' THEN 1 ELSE 0 END) AS core,
        SUM(CASE WHEN content_level IN ('L4｜Framework','L5｜Knowledge Object')
                  AND governance_state='ACTIVE' AND relation_state='VALID'
                  AND effective_space='CURRENT' THEN 1 ELSE 0 END) AS core_current,
        SUM(CASE WHEN knowledge_role='METHOD'
                  AND COALESCE(effective_space,'')!='PROVENANCE'
                  AND COALESCE(search_eligibility,'')!='HISTORY_ONLY' THEN 1 ELSE 0 END) AS methods,
        SUM(CASE WHEN (content_level='L6｜Evidence / Case' OR knowledge_role IN ('SOURCE','EVIDENCE','CASE'))
                  AND COALESCE(effective_space,'')!='PROVENANCE'
                  AND COALESCE(search_eligibility,'')!='HISTORY_ONLY' THEN 1 ELSE 0 END) AS evidence,
        SUM(CASE WHEN (content_level='L7｜Practice / Output' OR knowledge_role IN ('PRACTICE','TOOL'))
                  AND COALESCE(effective_space,'')!='PROVENANCE'
                  AND COALESCE(search_eligibility,'')!='HISTORY_ONLY' THEN 1 ELSE 0 END) AS practice,
        SUM(CASE WHEN effective_space='PROVENANCE' OR search_eligibility='HISTORY_ONLY' OR governance_state='LEGACY' THEN 1 ELSE 0 END) AS history
      FROM documents WHERE active=1
    `).first<Record<string, number>>(),
    db.prepare(`
      SELECT COALESCE(knowledge_role,'UNCLASSIFIED') AS name, COUNT(*) AS value
      FROM documents
      WHERE active=1 AND COALESCE(effective_space,'')!='PROVENANCE' AND COALESCE(search_eligibility,'')!='HISTORY_ONLY'
      GROUP BY knowledge_role ORDER BY value DESC
    `).all<Record<string, unknown>>(),
    db.prepare(`
      SELECT COALESCE(content_level,'UNCLASSIFIED') AS name, COUNT(*) AS value
      FROM documents
      WHERE active=1 AND COALESCE(effective_space,'')!='PROVENANCE' AND COALESCE(search_eligibility,'')!='HISTORY_ONLY'
      GROUP BY content_level ORDER BY value DESC
    `).all<Record<string, unknown>>(),
    db.prepare(`
      SELECT d.page_id, d.canonical_id, d.title, d.notion_url, d.effective_space,
             d.search_eligibility, d.trust_state, d.governance_state, d.relation_state,
             d.content_level, d.knowledge_role, d.index_state, d.authority_reason,
             d.notion_last_edited_time, d.indexed_at,
             (SELECT substr(c.chunk_text,1,700) FROM chunks c
               WHERE c.page_id=d.page_id AND c.active=1 ORDER BY c.ordinal ASC LIMIT 1) AS summary
      FROM documents d
      WHERE d.active=1
      ORDER BY
        CASE WHEN d.effective_space='CURRENT' THEN 0 WHEN d.effective_space='SUPPORT' THEN 1 ELSE 2 END,
        COALESCE(d.indexed_at,d.observed_at) DESC,
        d.title ASC
    `).all<Record<string, unknown>>(),
  ]);

  const s = summary ?? {};
  const roleDistribution = (roles.results ?? []).slice(0, 8).map((r) => ({ name: String(r.name ?? "UNCLASSIFIED"), value: Number(r.value ?? 0) }));
  const evidenceDistribution = (roles.results ?? [])
    .filter((r) => EVIDENCE_ROLES.has(String(r.name ?? "")))
    .map((r) => ({ name: String(r.name), value: Number(r.value ?? 0) }));

  const items = (documents.results ?? []).map((row) => {
    const summaryText = cleanedSummary(row.summary);
    const tags = [row.trust_state, row.index_state, row.search_eligibility].filter((v): v is string => typeof v === "string" && Boolean(v));
    return {
      id: String(row.page_id),
      title: String(row.title ?? "Untitled"),
      ...(summaryText !== undefined ? { summary: summaryText } : {}),
      ...(row.canonical_id ? { canonicalId: String(row.canonical_id) } : {}),
      ...(row.knowledge_role ? { role: String(row.knowledge_role) } : {}),
      ...(row.content_level ? { level: String(row.content_level) } : {}),
      ...(row.effective_space ? { retrievalSpace: String(row.effective_space) } : {}),
      ...(row.governance_state ? { governanceState: String(row.governance_state) } : {}),
      ...(row.relation_state ? { relationState: String(row.relation_state) } : {}),
      group: readerGroup(row),
      ...(row.notion_url ? { url: String(row.notion_url) } : {}),
      ...(tags.length ? { tags } : {}),
      ...(row.authority_reason ? { limitations: [String(row.authority_reason)] } : {}),
    };
  });

  const defaultSelectedId = items.find((item) => item.group === "current" && item.retrievalSpace === "CURRENT")?.id ?? items[0]?.id;

  return {
    title: "Knowledge Reader｜知识阅读台",
    subtitle: "Live D1 readback. Notion remains canonical authority; this dashboard is a read-only derivative reader surface.",
    generatedAt: new Date().toISOString(),
    metrics: [
      { key: "core", label: "Core Knowledge", value: Number(s.core ?? 0), note: `${Number(s.core_current ?? 0)} explicit Current · L4/L5 ACTIVE + VALID` },
      { key: "methods", label: "Methods", value: Number(s.methods ?? 0), note: "Research + execution methods" },
      { key: "evidence", label: "Evidence", value: Number(s.evidence ?? 0), note: "L6 / SOURCE / EVIDENCE / CASE" },
      { key: "practice", label: "Practice", value: Number(s.practice ?? 0), note: "L7 / PRACTICE / TOOL" },
      { key: "history", label: "History", value: Number(s.history ?? 0), note: "PROVENANCE / HISTORY_ONLY / LEGACY" },
    ],
    migration: { done: Number(s.core_current ?? 0), total: Number(s.core ?? 0) },
    roleDistribution,
    evidenceDistribution,
    levelDistribution: (levels.results ?? []).map((r) => ({ name: String(r.name ?? "UNCLASSIFIED"), value: Number(r.value ?? 0) })),
    items,
    ...(defaultSelectedId !== undefined ? { defaultSelectedId } : {}),
    source: {
      authority: "Notion",
      derivative: "Cloudflare D1 / oleander-knowledge-manifest",
      activeDocuments: Number(s.active ?? 0),
      indexedDocuments: Number(s.indexed ?? 0),
      explicitCurrent: Number(s.explicit_current ?? 0),
      support: Number(s.support ?? 0),
      provenance: Number(s.provenance ?? 0),
    },
  };
}
