import { RETRIEVAL_PIPELINE_VERSION } from "./config";
import { embedTexts } from "./embedding";
import {
  fetchLexicalManifestHits,
  fetchManifestHits,
  getDocumentByCanonicalId,
  lineageForPage,
  relationsForPages,
} from "./manifest";
import type { Env, KnowledgeHit, RetrievalSpace, SearchRequest } from "./types";

function clampTopK(value: number | undefined, fallback: number): number {
  const candidate = Number.isFinite(value) ? Math.floor(value as number) : fallback;
  return Math.max(1, Math.min(50, candidate));
}

function stringArray(value: unknown): string[] {
  if (Array.isArray(value)) return value.filter((item): item is string => typeof item === "string");
  if (typeof value !== "string" || !value.trim()) return [];
  try {
    const parsed = JSON.parse(value) as unknown;
    return Array.isArray(parsed) ? parsed.filter((item): item is string => typeof item === "string") : [];
  } catch {
    return [];
  }
}

function rowToHit(
  row: Record<string, unknown>,
  namespace: RetrievalSpace,
  score: number,
  sources: Array<"EXACT" | "VECTOR" | "LEXICAL">,
): KnowledgeHit {
  return {
    vector_id: String(row.vector_id ?? ""),
    score,
    namespace,
    page_id: String(row.page_id ?? ""),
    canonical_id: row.canonical_id ? String(row.canonical_id) : null,
    title: String(row.title ?? ""),
    heading_path: String(row.heading_path ?? ""),
    text: String(row.chunk_text ?? ""),
    content_hash: String(row.content_hash ?? ""),
    knowledge_role: row.knowledge_role ? String(row.knowledge_role) : null,
    content_level: row.content_level ? String(row.content_level) : null,
    framework_type: row.framework_type ? String(row.framework_type) : null,
    trust_state: row.trust_state ? String(row.trust_state) : null,
    governance_state: row.governance_state ? String(row.governance_state) : null,
    relation_state: row.relation_state ? String(row.relation_state) : null,
    search_eligibility: row.search_eligibility ? String(row.search_eligibility) : null,
    evidence_grade: row.evidence_grade ? String(row.evidence_grade) : null,
    freshness_state: row.freshness_state ? String(row.freshness_state) : null,
    authority_class: row.authority_class ? String(row.authority_class) : null,
    primary_domain_ids: stringArray(row.primary_domain_ids_json),
    topic_ids: stringArray(row.topic_ids_json),
    secondary_semantics: stringArray(row.secondary_semantics_json),
    claim_ids: stringArray(row.claim_ids_json),
    evidence_ids: stringArray(row.evidence_ids_json),
    candidate_sources: sources,
    lexical_score: typeof row.lexical_score === "number" ? row.lexical_score : undefined,
    authority_reason: row.authority_reason ? String(row.authority_reason) : null,
  };
}

async function queryVectorNamespace(
  env: Env,
  vector: number[],
  namespace: RetrievalSpace,
  topK: number,
  canonicalId?: string,
  allowScoped = false,
): Promise<KnowledgeHit[]> {
  const result = await env.KNOWLEDGE_INDEX.query(vector, {
    topK: Math.min(50, topK * 3),
    namespace,
    returnValues: false,
    returnMetadata: "all",
  });
  const ids = result.matches.map((match) => match.id);
  const rows = await fetchManifestHits(env.MANIFEST, ids, namespace, canonicalId, allowScoped);
  const hits: KnowledgeHit[] = [];
  for (const match of result.matches) {
    const row = rows.get(match.id);
    if (!row) continue; // stale or authority-mismatched Vectorize result: fail closed.
    hits.push(rowToHit(row, namespace, match.score, ["VECTOR"]));
  }
  return hits;
}

async function queryLexicalNamespace(
  env: Env,
  query: string,
  namespace: RetrievalSpace,
  topK: number,
  canonicalId?: string,
  allowScoped = false,
): Promise<KnowledgeHit[]> {
  const rows = await fetchLexicalManifestHits(env.MANIFEST, query, namespace, topK, canonicalId, allowScoped);
  return rows.map((row) => {
    const lexicalScore = typeof row.lexical_score === "number" ? row.lexical_score : 0.55;
    const sources: Array<"EXACT" | "VECTOR" | "LEXICAL"> =
      lexicalScore >= 0.95 ? ["EXACT", "LEXICAL"] : ["LEXICAL"];
    return rowToHit(row, namespace, lexicalScore, sources);
  });
}

function intersects(actual: string[] | undefined, requested: string[] | undefined): boolean {
  if (!requested?.length) return true;
  const set = new Set(actual ?? []);
  return requested.some((value) => set.has(value));
}

function explicitNarrowing(hits: KnowledgeHit[], request: SearchRequest): KnowledgeHit[] {
  return hits.filter((hit) =>
    intersects(hit.primary_domain_ids, request.domain_ids) &&
    intersects(hit.topic_ids, request.topic_ids)
  );
}

function rerankScore(hit: KnowledgeHit, request: SearchRequest): number {
  let score = hit.score;
  if (request.knowledge_roles?.length && hit.knowledge_role && request.knowledge_roles.includes(hit.knowledge_role)) {
    score += 0.12;
  }
  if (request.secondary_semantics?.length) {
    const semantics = new Set(hit.secondary_semantics ?? []);
    if (request.secondary_semantics.some((value) => semantics.has(value))) score += 0.12;
  }
  return score;
}

export function mergeAndDedupeCandidates(hits: KnowledgeHit[], request: SearchRequest, topK: number): KnowledgeHit[] {
  const narrowed = explicitNarrowing(hits, request);
  const byCanonical = new Map<string, KnowledgeHit>();
  for (const hit of narrowed) {
    const key = `${hit.namespace}:${hit.canonical_id || hit.page_id}`;
    const existing = byCanonical.get(key);
    if (!existing) {
      byCanonical.set(key, { ...hit, score: rerankScore(hit, request) });
      continue;
    }
    const existingSources = new Set(existing.candidate_sources ?? []);
    for (const source of hit.candidate_sources ?? []) existingSources.add(source);
    const candidateScore = rerankScore(hit, request);
    if (candidateScore > existing.score) {
      byCanonical.set(key, {
        ...hit,
        score: candidateScore,
        candidate_sources: [...existingSources],
      });
    } else {
      existing.candidate_sources = [...existingSources];
      existing.lexical_score = Math.max(existing.lexical_score ?? 0, hit.lexical_score ?? 0) || undefined;
    }
  }
  return [...byCanonical.values()]
    .sort((a, b) => b.score - a.score || a.title.localeCompare(b.title))
    .slice(0, topK);
}

function conflictGate(groups: KnowledgeHit[][]): Record<string, unknown> {
  const hits = groups.flat();
  const issues: Array<Record<string, unknown>> = [];
  const spacesByCanonical = new Map<string, Set<string>>();
  for (const hit of hits) {
    if (hit.canonical_id) {
      const spaces = spacesByCanonical.get(hit.canonical_id) ?? new Set<string>();
      spaces.add(hit.namespace);
      spacesByCanonical.set(hit.canonical_id, spaces);
    }
    if (hit.relation_state === "CONFLICT" || hit.relation_state === "ORPHAN") {
      issues.push({
        type: "RELATION_STATE",
        canonical_id: hit.canonical_id,
        page_id: hit.page_id,
        state: hit.relation_state,
      });
    }
    if (hit.freshness_state === "STALE" || hit.freshness_state === "EXPIRED") {
      issues.push({
        type: "FRESHNESS_STATE",
        canonical_id: hit.canonical_id,
        page_id: hit.page_id,
        state: hit.freshness_state,
      });
    }
  }
  for (const [canonicalId, spaces] of spacesByCanonical) {
    if (spaces.size > 1) {
      issues.push({
        type: "CROSS_SPACE_CANONICAL_COLLISION",
        canonical_id: canonicalId,
        spaces: [...spaces].sort(),
      });
    }
  }
  return {
    state: issues.length ? "ATTENTION" : "CLEAR",
    issues,
    rule: "CONFLICT_GATE_REPORTS_EXPLICIT_DERIVATIVE_CONDITIONS_AND_DOES_NOT_PROMOTE_OR_REJECT_CANONICAL_KNOWLEDGE",
  };
}

async function expandRelations(
  env: Env,
  groups: KnowledgeHit[][],
): Promise<Record<string, Array<Record<string, unknown>>>> {
  const pageIds = groups.flat().map((hit) => hit.page_id);
  return relationsForPages(env.MANIFEST, pageIds);
}

function claimEvidenceExpansion(groups: KnowledgeHit[][]): Record<string, unknown> {
  const byPage: Record<string, { claim_ids: string[]; evidence_ids: string[] }> = {};
  for (const hit of groups.flat()) {
    byPage[hit.page_id] = {
      claim_ids: hit.claim_ids ?? [],
      evidence_ids: hit.evidence_ids ?? [],
    };
  }
  const bound = Object.values(byPage).some((entry) => entry.claim_ids.length || entry.evidence_ids.length);
  return {
    state: bound ? "MANIFEST_IDS_BOUND" : "NOT_BOUND_OR_EMPTY",
    by_page: byPage,
    no_inference: true,
  };
}

export async function knowledgeSearch(env: Env, request: SearchRequest): Promise<Record<string, unknown>> {
  const query = request.query?.trim();
  if (!query) throw new Error("query is required");
  const defaultTopK = Number.parseInt(env.API_DEFAULT_TOP_K || "8", 10) || 8;
  const topK = clampTopK(request.top_k, defaultTopK);
  const allowScoped = request.include_scoped === true || Boolean(request.canonical_id);

  const [vector] = await embedTexts(env, [query]);
  if (!vector) throw new Error("No query embedding returned");

  const collect = async (namespace: RetrievalSpace, enabled: boolean): Promise<KnowledgeHit[]> => {
    if (!enabled) return [];
    const [vectorHits, lexicalHits] = await Promise.all([
      queryVectorNamespace(env, vector, namespace, topK, request.canonical_id, allowScoped),
      queryLexicalNamespace(env, query, namespace, topK, request.canonical_id, allowScoped),
    ]);
    return mergeAndDedupeCandidates([...vectorHits, ...lexicalHits], request, topK);
  };

  const [current, support, provenance] = await Promise.all([
    collect("CURRENT", true),
    collect("SUPPORT", request.include_support !== false),
    collect("PROVENANCE", request.include_provenance === true),
  ]);
  const groups = [current, support, provenance];
  const relationExpansion = await expandRelations(env, groups);

  return {
    version: RETRIEVAL_PIPELINE_VERSION,
    query,
    generated_at: new Date().toISOString(),
    authority_root_page_id: env.NOTION_ROOT_PAGE_ID,
    authority_policy: {
      precedence: ["CURRENT", "SUPPORT", "PROVENANCE"],
      current_is_explicit_only: true,
      provenance_requires_opt_in: true,
      scoped_requires_opt_in_or_canonical_id: true,
      vector_hits_require_d1_manifest_readback: true,
      vector_is_candidate_generation_only: true,
      d1_manifest_is_derivative_read_model: true,
    },
    pipeline: {
      stages: [
        "INTENT_CURRENT_CONTEXT",
        "EXACT_CANONICAL_ALIAS",
        "NAMESPACE_HARD_AUTHORITY_FILTER",
        "DOMAIN_TOPIC_NARROWING",
        "VECTOR_LEXICAL_CANDIDATE_GENERATION",
        "CANONICAL_DEDUPE",
        "PRIMARY_ROLE_SECONDARY_SEMANTIC_RERANK",
        "KNOWLEDGE_RELATION_EXPANSION",
        "CLAIM_EVIDENCE_EXPANSION",
        "CONFLICT_GATE",
        "KNOWLEDGE_PACK_V2",
      ],
      coverage: {
        intent_context: "CALLER_SUPPLIED_QUERY_AND_OPTIONAL_FILTERS_ONLY",
        exact_canonical: "BOUND_THROUGH_CANONICAL_ID_AND_EXACT_LEXICAL_MATCH",
        aliases: "UNBOUND_NO_LIVE_ALIAS_FIELD_NO_INFERENCE",
        domain_topic_narrowing: request.domain_ids?.length || request.topic_ids?.length ? "APPLIED" : "NOT_REQUESTED",
        role_semantic_rerank: request.knowledge_roles?.length || request.secondary_semantics?.length
          ? "EXPLICIT_FILTER_HINTS_APPLIED"
          : "NO_INTENT_INFERENCE",
        lexical: "D1_MANIFEST_CONTAINS_MATCH",
        vector: "VECTORIZE_CANDIDATE_GENERATION_WITH_D1_READBACK",
        relation_expansion: "D1_TYPED_EDGES",
        claim_evidence_expansion: "MANIFEST_IDS_ONLY_NO_INFERENCE",
      },
    },
    current,
    support,
    provenance,
    relation_expansion: relationExpansion,
    claim_evidence_expansion: claimEvidenceExpansion(groups),
    conflict_gate: conflictGate(groups),
    counts: { current: current.length, support: support.length, provenance: provenance.length },
  };
}

export async function knowledgePackByCanonicalId(env: Env, canonicalId: string): Promise<Record<string, unknown> | null> {
  const document = await getDocumentByCanonicalId(env.MANIFEST, canonicalId);
  if (!document) return null;
  const pageId = String(document.page_id);
  return {
    version: RETRIEVAL_PIPELINE_VERSION,
    authority_root_page_id: env.NOTION_ROOT_PAGE_ID,
    document,
    relation_expansion: await lineageForPage(env.MANIFEST, pageId),
    claim_evidence_expansion: {
      claim_ids: stringArray(document.claim_ids_json),
      evidence_ids: stringArray(document.evidence_ids_json),
      no_inference: true,
    },
    implementation_boundary: {
      runtime_graph_separate: true,
      d1_is_derivative: true,
      does_not_prove_design_acceptance: true,
    },
  };
}
