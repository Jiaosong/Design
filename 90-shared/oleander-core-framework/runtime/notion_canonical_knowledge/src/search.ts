import { embedTexts } from "./embedding";
import { fetchManifestHits, getDocumentByCanonicalId, lineageForPage } from "./manifest";
import type { Env, KnowledgeHit, RetrievalSpace, SearchRequest } from "./types";

function clampTopK(value: number | undefined, fallback: number): number {
  const candidate = Number.isFinite(value) ? Math.floor(value as number) : fallback;
  return Math.max(1, Math.min(50, candidate));
}

async function queryNamespace(
  env: Env,
  vector: number[],
  namespace: RetrievalSpace,
  topK: number,
  canonicalId?: string,
  allowScoped = false,
): Promise<KnowledgeHit[]> {
  const result = await env.KNOWLEDGE_INDEX.query(vector, {
    topK,
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
    hits.push({
      vector_id: match.id,
      score: match.score,
      namespace,
      page_id: String(row.page_id),
      canonical_id: row.canonical_id ? String(row.canonical_id) : null,
      title: String(row.title ?? ""),
      heading_path: String(row.heading_path ?? ""),
      text: String(row.chunk_text ?? ""),
      content_hash: String(row.content_hash ?? ""),
      knowledge_role: row.knowledge_role ? String(row.knowledge_role) : null,
      content_level: row.content_level ? String(row.content_level) : null,
      trust_state: row.trust_state ? String(row.trust_state) : null,
    });
  }
  return hits;
}

export async function knowledgeSearch(env: Env, request: SearchRequest): Promise<Record<string, unknown>> {
  const query = request.query?.trim();
  if (!query) throw new Error("query is required");
  const defaultTopK = Number.parseInt(env.API_DEFAULT_TOP_K || "8", 10) || 8;
  const topK = clampTopK(request.top_k, defaultTopK);
  const [vector] = await embedTexts(env, [query]);
  if (!vector) throw new Error("No query embedding returned");
  const allowScoped = request.include_scoped === true || Boolean(request.canonical_id);

  const current = await queryNamespace(env, vector, "CURRENT", topK, request.canonical_id, allowScoped);
  const support = request.include_support === false
    ? []
    : await queryNamespace(env, vector, "SUPPORT", topK, request.canonical_id, allowScoped);
  const provenance = request.include_provenance === true
    ? await queryNamespace(env, vector, "PROVENANCE", topK, request.canonical_id, allowScoped)
    : [];

  return {
    version: "oleander-knowledge-pack/v1",
    query,
    generated_at: new Date().toISOString(),
    authority_root_page_id: env.NOTION_ROOT_PAGE_ID,
    authority_policy: {
      precedence: ["CURRENT", "SUPPORT", "PROVENANCE"],
      current_is_explicit_only: true,
      provenance_requires_opt_in: true,
      scoped_requires_opt_in_or_canonical_id: true,
      vector_hits_require_d1_manifest_readback: true,
    },
    current,
    support,
    provenance,
    counts: { current: current.length, support: support.length, provenance: provenance.length },
  };
}

export async function knowledgePackByCanonicalId(env: Env, canonicalId: string): Promise<Record<string, unknown> | null> {
  const document = await getDocumentByCanonicalId(env.MANIFEST, canonicalId);
  if (!document) return null;
  const pageId = String(document.page_id);
  return {
    version: "oleander-knowledge-pack/v1",
    authority_root_page_id: env.NOTION_ROOT_PAGE_ID,
    document,
    lineage: await lineageForPage(env.MANIFEST, pageId),
  };
}
