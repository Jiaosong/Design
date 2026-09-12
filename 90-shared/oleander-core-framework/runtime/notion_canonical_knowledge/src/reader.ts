import type {
  KnowledgeReaderDetail,
  KnowledgeReaderDetailRelation,
  KnowledgeReaderDetailSection,
  KnowledgeReaderSnapshot,
} from "./types";

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

function optionalString(value: unknown): string | undefined {
  return typeof value === "string" && value.length > 0 ? value : undefined;
}

function stringArray(value: unknown): string[] {
  if (typeof value !== "string" || !value.trim()) return [];
  try {
    const parsed = JSON.parse(value);
    return Array.isArray(parsed) ? parsed.filter((entry): entry is string => typeof entry === "string") : [];
  } catch {
    return [];
  }
}

function removeChunkOverlap(previous: string, next: string): string {
  const max = Math.min(previous.length, next.length, 8000);
  for (let length = max; length >= 32; length -= 1) {
    if (previous.slice(-length) === next.slice(0, length)) {
      return next.slice(length).replace(/^\s+/, "");
    }
  }
  return next;
}

export function mergeReaderChunks(
  rows: Array<{ ordinal: number; heading_path: string; chunk_text: string; token_estimate: number }>,
): KnowledgeReaderDetailSection[] {
  const sections: KnowledgeReaderDetailSection[] = [];
  for (const row of rows) {
    const headingPath = row.heading_path.split(" > ").map((part) => part.trim()).filter(Boolean);
    const headingKey = headingPath.join(" > ");
    const previous = sections.at(-1);
    if (previous && previous.headingPath.join(" > ") === headingKey) {
      const delta = removeChunkOverlap(previous.text, row.chunk_text);
      if (delta) previous.text = `${previous.text}\n\n${delta}`.trim();
      previous.chunkOrdinals.push(row.ordinal);
      previous.tokenEstimate += Number(row.token_estimate || 0);
      continue;
    }
    sections.push({
      key: `${row.ordinal}:${headingKey || "root"}`,
      headingPath,
      text: row.chunk_text.trim(),
      chunkOrdinals: [row.ordinal],
      tokenEstimate: Number(row.token_estimate || 0),
    });
  }
  return sections;
}

function relationFromRow(
  row: Record<string, unknown>,
  direction: "outgoing" | "incoming",
): KnowledgeReaderDetailRelation {
  return {
    direction,
    relationType: String(row.relation_type ?? "RELATED"),
    pageId: String(row.page_id ?? ""),
    ...(optionalString(row.canonical_id) ? { canonicalId: String(row.canonical_id) } : {}),
    ...(optionalString(row.title) ? { title: String(row.title) } : {}),
    ...(optionalString(row.knowledge_role) ? { role: String(row.knowledge_role) } : {}),
    ...(optionalString(row.content_level) ? { level: String(row.content_level) } : {}),
    ...(optionalString(row.effective_space) ? { retrievalSpace: String(row.effective_space) } : {}),
    ...(optionalString(row.governance_state) ? { governanceState: String(row.governance_state) } : {}),
    ...(optionalString(row.relation_state) ? { relationState: String(row.relation_state) } : {}),
  };
}

export async function buildKnowledgeReaderDetail(db: D1Database, pageId: string): Promise<KnowledgeReaderDetail | null> {
  const document = await db.prepare(`
    SELECT page_id, canonical_id, title, notion_url, notion_last_edited_time,
           effective_space, search_eligibility, trust_state, governance_state,
           relation_state, content_level, knowledge_role, index_state,
           authority_reason, markdown_truncated, unknown_block_ids_json, indexed_at,
           primary_domain_ids_json, related_domain_ids_json,
           source_relation_ids_json, method_relation_ids_json,
           replacement_ids_json, replaced_document_ids_json
      FROM documents
     WHERE page_id=? AND active=1
     LIMIT 1
  `).bind(pageId).first<Record<string, unknown>>();
  if (!document) return null;

  const [chunksResult, outgoingResult, incomingResult] = await Promise.all([
    db.prepare(`
      SELECT ordinal, heading_path, chunk_text, token_estimate
        FROM chunks
       WHERE page_id=? AND active=1
       ORDER BY ordinal ASC
    `).bind(pageId).all<{ ordinal: number; heading_path: string; chunk_text: string; token_estimate: number }>(),
    db.prepare(`
      SELECT e.relation_type, e.target_page_id AS page_id,
             d.canonical_id, d.title, d.knowledge_role, d.content_level,
             d.effective_space, d.governance_state, d.relation_state
        FROM lineage_edges e
        LEFT JOIN documents d ON d.page_id=e.target_page_id AND d.active=1
       WHERE e.source_page_id=?
       ORDER BY e.relation_type, d.title, e.target_page_id
    `).bind(pageId).all<Record<string, unknown>>(),
    db.prepare(`
      SELECT e.relation_type, e.source_page_id AS page_id,
             d.canonical_id, d.title, d.knowledge_role, d.content_level,
             d.effective_space, d.governance_state, d.relation_state
        FROM lineage_edges e
        LEFT JOIN documents d ON d.page_id=e.source_page_id AND d.active=1
       WHERE e.target_page_id=?
       ORDER BY e.relation_type, d.title, e.source_page_id
    `).bind(pageId).all<Record<string, unknown>>(),
  ]);

  const chunkRows = chunksResult.results ?? [];
  const sections = mergeReaderChunks(chunkRows);
  const unknownBlockIds = stringArray(document.unknown_block_ids_json);
  const markdownTruncated = Number(document.markdown_truncated ?? 0) !== 0;
  const tokenEstimate = chunkRows.reduce((sum, row) => sum + Number(row.token_estimate || 0), 0);
  const relations = [
    ...(outgoingResult.results ?? []).map((row) => relationFromRow(row, "outgoing")),
    ...(incomingResult.results ?? []).map((row) => relationFromRow(row, "incoming")),
  ];
  const primaryDomainIds = stringArray(document.primary_domain_ids_json);
  const relatedDomainIds = stringArray(document.related_domain_ids_json);
  const declaredRelationIds = {
    SOURCE: stringArray(document.source_relation_ids_json),
    METHOD: stringArray(document.method_relation_ids_json),
    REPLACEMENT: stringArray(document.replacement_ids_json),
    REPLACED_DOCUMENT: stringArray(document.replaced_document_ids_json),
  } as const;
  const outgoing = relations.filter((relation) => relation.direction === "outgoing");
  const outgoingKeys = new Set(outgoing.map((relation) => `${relation.relationType}:${relation.pageId}`));
  const missingManifestEdges = Object.entries(declaredRelationIds).flatMap(([relationType, ids]) =>
    ids
      .filter((id) => !outgoingKeys.has(`${relationType}:${id}`))
      .map((id) => ({ relationType, pageId: id })),
  );
  const unresolvedTargets = outgoing
    .filter((relation) => !relation.title && !relation.canonicalId)
    .map((relation) => ({ relationType: relation.relationType, pageId: relation.pageId }));
  const indexedOutgoing = {
    source: outgoing.filter((relation) => relation.relationType === "SOURCE").length,
    method: outgoing.filter((relation) => relation.relationType === "METHOD").length,
    replacement: outgoing.filter((relation) => relation.relationType === "REPLACEMENT").length,
    replacedDocument: outgoing.filter((relation) => relation.relationType === "REPLACED_DOCUMENT").length,
  };

  return {
    version: "oleander-knowledge-reader-detail/v1",
    generatedAt: new Date().toISOString(),
    id: String(document.page_id),
    title: String(document.title ?? "Untitled"),
    ...(optionalString(document.canonical_id) ? { canonicalId: String(document.canonical_id) } : {}),
    ...(optionalString(document.notion_url) ? { url: String(document.notion_url) } : {}),
    ...(optionalString(document.knowledge_role) ? { role: String(document.knowledge_role) } : {}),
    ...(optionalString(document.content_level) ? { level: String(document.content_level) } : {}),
    ...(optionalString(document.effective_space) ? { retrievalSpace: String(document.effective_space) } : {}),
    ...(optionalString(document.search_eligibility) ? { searchEligibility: String(document.search_eligibility) } : {}),
    ...(optionalString(document.trust_state) ? { trustState: String(document.trust_state) } : {}),
    ...(optionalString(document.governance_state) ? { governanceState: String(document.governance_state) } : {}),
    ...(optionalString(document.relation_state) ? { relationState: String(document.relation_state) } : {}),
    ...(optionalString(document.index_state) ? { indexState: String(document.index_state) } : {}),
    ...(optionalString(document.authority_reason) ? { authorityReason: String(document.authority_reason) } : {}),
    ...(optionalString(document.notion_last_edited_time) ? { notionLastEditedTime: String(document.notion_last_edited_time) } : {}),
    ...(optionalString(document.indexed_at) ? { indexedAt: String(document.indexed_at) } : {}),
    primaryDomainIds,
    relatedDomainIds,
    review: {
      contentComplete: !markdownTruncated && unknownBlockIds.length === 0 && sections.length > 0,
      markdownTruncated,
      chunkCount: chunkRows.length,
      tokenEstimate,
      unknownBlockIds,
      relationReadback: {
        declared: {
          primaryDomain: primaryDomainIds.length,
          relatedDomain: relatedDomainIds.length,
          source: declaredRelationIds.SOURCE.length,
          method: declaredRelationIds.METHOD.length,
          replacement: declaredRelationIds.REPLACEMENT.length,
          replacedDocument: declaredRelationIds.REPLACED_DOCUMENT.length,
        },
        indexedOutgoing,
        unresolvedTargets,
        missingManifestEdges,
      },
    },
    sections,
    relations,
  };
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
      ...(row.search_eligibility ? { searchEligibility: String(row.search_eligibility) } : {}),
      ...(row.trust_state ? { trustState: String(row.trust_state) } : {}),
      ...(row.governance_state ? { governanceState: String(row.governance_state) } : {}),
      ...(row.relation_state ? { relationState: String(row.relation_state) } : {}),
      ...(row.index_state ? { indexState: String(row.index_state) } : {}),
      ...(row.authority_reason ? { authorityReason: String(row.authority_reason) } : {}),
      ...(row.notion_last_edited_time ? { notionLastEditedTime: String(row.notion_last_edited_time) } : {}),
      ...(row.indexed_at ? { indexedAt: String(row.indexed_at) } : {}),
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
