export interface Env {
  AI: Ai;
  OLEANDER_KNOWLEDGE: VectorizeIndex;
  RAG_DB: D1Database;
  SYNC_QUEUE: Queue<SyncMessage>;
  NOTION_API_TOKEN: string;
  NOTION_WEBHOOK_SECRET: string;
  RETRIEVAL_API_TOKEN?: string;
  NOTION_API_VERSION: string;
  EMBEDDING_MODEL: string;
  RAG_SCHEMA_VERSION: string;
  DEFAULT_TOP_K: string;
}

type RetrievalSpace = "CURRENT" | "SUPPORT" | "PROVENANCE" | "EXCLUDED" | "UNKNOWN";

type SyncMessage = {
  eventId: string;
  eventType: string;
  eventTimestamp?: string;
  deliveryAttempt?: number;
  notionPageId: string;
};

type KnowledgeMeta = {
  canonical_id: string;
  source_locator: string;
  source_kind: "NOTION";
  title: string;
  retrieval_space: RetrievalSpace;
  search_eligibility: string;
  governance_state: string;
  trust_state: string;
  freshness_state: string;
  evidence_grade: string;
  authority_class: string;
  project_id: string;
  domain_id: string;
  knowledge_role: string;
  object_type: string;
  last_edited_at: string | null;
  last_verified_at: string | null;
  verification_due: string | null;
};

type Chunk = {
  chunkId: string;
  ordinal: number;
  sectionPath: string;
  text: string;
  hash: string;
};

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body, null, 2), {
    status,
    headers: { "content-type": "application/json; charset=utf-8" },
  });

function hex(buffer: ArrayBuffer): string {
  return [...new Uint8Array(buffer)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function sha256(text: string): Promise<string> {
  return hex(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text)));
}

async function verifyNotionSignature(raw: string, signature: string | null, secret: string): Promise<boolean> {
  if (!signature || !secret) return false;
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const expected = hex(await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(raw)));
  const supplied = signature.replace(/^sha256=/i, "").toLowerCase();
  if (supplied.length !== expected.length) return false;
  let diff = 0;
  for (let i = 0; i < supplied.length; i++) diff |= supplied.charCodeAt(i) ^ expected.charCodeAt(i);
  return diff === 0;
}

function bearerAuthorized(request: Request, token?: string): boolean {
  if (!token) return true;
  return request.headers.get("authorization") === `Bearer ${token}`;
}

async function notionFetch(env: Env, path: string): Promise<any> {
  const response = await fetch(`https://api.notion.com/v1${path}`, {
    headers: {
      authorization: `Bearer ${env.NOTION_API_TOKEN}`,
      "notion-version": env.NOTION_API_VERSION,
      accept: "application/json",
    },
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`NOTION_${response.status}:${detail.slice(0, 500)}`);
  }
  return response.json();
}

async function fetchAllBlockChildren(env: Env, blockId: string): Promise<any[]> {
  const out: any[] = [];
  let cursor: string | undefined;
  do {
    const params = new URLSearchParams({ page_size: "100" });
    if (cursor) params.set("start_cursor", cursor);
    const data = await notionFetch(env, `/blocks/${blockId}/children?${params}`);
    for (const block of data.results ?? []) {
      out.push(block);
      if (block.has_children) {
        block._children = await fetchAllBlockChildren(env, block.id);
      }
    }
    cursor = data.has_more ? data.next_cursor : undefined;
  } while (cursor);
  return out;
}

function richTextPlain(items: any[] | undefined): string {
  return (items ?? []).map((item) => item.plain_text ?? item.text?.content ?? "").join("");
}

function propertyText(prop: any): string {
  if (!prop) return "";
  if (prop.type === "title") return richTextPlain(prop.title);
  if (prop.type === "rich_text") return richTextPlain(prop.rich_text);
  if (prop.type === "select") return prop.select?.name ?? "";
  if (prop.type === "status") return prop.status?.name ?? "";
  if (prop.type === "multi_select") return (prop.multi_select ?? []).map((x: any) => x.name).join(",");
  if (prop.type === "formula") return String(prop.formula?.string ?? prop.formula?.number ?? "");
  if (prop.type === "url") return prop.url ?? "";
  if (prop.type === "date") return prop.date?.start ?? "";
  if (prop.type === "checkbox") return prop.checkbox ? "true" : "false";
  return "";
}

function pickProperty(properties: Record<string, any>, aliases: string[], fallback = ""): string {
  for (const key of aliases) {
    if (properties[key]) {
      const value = propertyText(properties[key]).trim();
      if (value) return value;
    }
  }
  return fallback;
}

function normalizeRetrievalSpace(raw: string): RetrievalSpace {
  const upper = raw.trim().toUpperCase();
  if (["CURRENT", "SUPPORT", "PROVENANCE", "EXCLUDED"].includes(upper)) return upper as RetrievalSpace;
  return "UNKNOWN";
}

function deriveKnowledgeMeta(page: any): KnowledgeMeta {
  const p = page.properties ?? {};
  const canonical = pickProperty(p, ["Canonical ID", "Canonical ID｜规范ID", "对象ID", "ID"]);
  if (!canonical) throw new Error("HOLD_MISSING_CANONICAL_ID");

  const retrievalSpace = normalizeRetrievalSpace(
    pickProperty(p, ["Retrieval Space｜检索空间", "Retrieval Space"], "UNKNOWN"),
  );
  const trust = pickProperty(p, ["Trust State｜可信状态", "Trust State"], "UNKNOWN").toUpperCase();
  const eligibility = pickProperty(p, ["Search Eligibility｜检索资格", "Search Eligibility"], "SCOPED").toUpperCase();
  const governance = pickProperty(p, ["治理状态", "Governance State"], "UNKNOWN").toUpperCase();
  const freshness = pickProperty(p, ["时效状态", "Freshness State"], "UNKNOWN").toUpperCase();
  const evidence = pickProperty(p, ["证据状态", "Evidence Grade", "Evidence State"], "UNKNOWN").toUpperCase();
  const projectId = pickProperty(p, ["Project ID｜项目ID", "Project ID", "项目编号"], "GLOBAL");
  const domainId = pickProperty(p, ["主领域", "Domain ID", "Domain"], "GLOBAL");
  const role = pickProperty(p, ["知识角色", "Knowledge Role"], "UNKNOWN").toUpperCase();
  const objectType = pickProperty(p, ["内容层级", "Knowledge Type｜知识类型", "Object Type"], "UNKNOWN").toUpperCase();
  const title = pickProperty(p, ["Name", "名称", "title", "Title"], page.url ?? canonical);
  const lastVerified = pickProperty(p, ["date:最近核验:start", "最近核验", "Last Verified"], "") || null;
  const verificationDue = pickProperty(p, ["date:Verification Due｜复核到期:start", "Verification Due｜复核到期", "Verification Due"], "") || null;

  return {
    canonical_id: canonical,
    source_locator: `notion://${page.id}`,
    source_kind: "NOTION",
    title,
    retrieval_space: retrievalSpace,
    search_eligibility: eligibility,
    governance_state: governance,
    trust_state: trust,
    freshness_state: freshness,
    evidence_grade: evidence,
    authority_class: retrievalSpace === "CURRENT" ? "CURRENT_CANONICAL" : `${retrievalSpace}_DERIVED`,
    project_id: projectId || "GLOBAL",
    domain_id: domainId || "GLOBAL",
    knowledge_role: role || "UNKNOWN",
    object_type: objectType || "UNKNOWN",
    last_edited_at: page.last_edited_time ?? null,
    last_verified_at: lastVerified,
    verification_due: verificationDue,
  };
}

function blockText(block: any): string {
  const type = block.type;
  const payload = block[type] ?? {};
  if (["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item", "quote", "callout", "toggle", "code"].includes(type)) {
    return richTextPlain(payload.rich_text).trim();
  }
  if (type === "table_row") {
    return (payload.cells ?? []).map((cell: any[]) => richTextPlain(cell)).join(" | ").trim();
  }
  if (type === "child_page") return payload.title ?? "";
  return "";
}

function flattenBlocks(blocks: any[], headingStack: string[] = []): Array<{ section: string; text: string }> {
  const out: Array<{ section: string; text: string }> = [];
  const stack = [...headingStack];
  for (const block of blocks) {
    const text = blockText(block);
    if (block.type === "heading_1") {
      stack.splice(0, stack.length, text);
    } else if (block.type === "heading_2") {
      stack.splice(1, stack.length, text);
    } else if (block.type === "heading_3") {
      stack.splice(2, stack.length, text);
    } else if (text) {
      out.push({ section: stack.filter(Boolean).join(" / "), text });
    }
    if (block._children?.length) out.push(...flattenBlocks(block._children, stack));
  }
  return out;
}

async function makeChunks(meta: KnowledgeMeta, blocks: any[]): Promise<Chunk[]> {
  const units = flattenBlocks(blocks);
  const targetChars = 2600;
  const chunks: Chunk[] = [];
  let current: string[] = [];
  let section = "";

  const flush = async () => {
    const body = current.join("\n").trim();
    if (!body) return;
    const ordinal = chunks.length;
    const text = `Title: ${meta.title}\nCanonical: ${meta.canonical_id}\nDomain: ${meta.domain_id}\nSection: ${section || "ROOT"}\n\n${body}`;
    const hash = await sha256(text);
    chunks.push({
      chunkId: `${meta.canonical_id}:${ordinal}:${hash.slice(0, 12)}`,
      ordinal,
      sectionPath: section,
      text,
      hash,
    });
    current = [];
  };

  for (const unit of units) {
    const projected = current.join("\n").length + unit.text.length;
    if (current.length && (unit.section !== section || projected > targetChars)) await flush();
    section = unit.section;
    current.push(unit.text);
  }
  await flush();

  if (!chunks.length) {
    const text = `Title: ${meta.title}\nCanonical: ${meta.canonical_id}\nDomain: ${meta.domain_id}`;
    const hash = await sha256(text);
    chunks.push({ chunkId: `${meta.canonical_id}:0:${hash.slice(0, 12)}`, ordinal: 0, sectionPath: "ROOT", text, hash });
  }
  return chunks;
}

function namespaceFor(space: RetrievalSpace): string | null {
  if (space === "CURRENT") return "prod-current";
  if (space === "SUPPORT") return "prod-support";
  if (space === "PROVENANCE") return "prod-provenance";
  return null;
}

function legallyIndexable(meta: KnowledgeMeta): boolean {
  if (!namespaceFor(meta.retrieval_space)) return false;
  if (!["DEFAULT", "SCOPED"].includes(meta.search_eligibility)) return false;
  if (!["ACTIVE", "CURRENT", "VALID"].includes(meta.governance_state)) return false;
  if (meta.trust_state === "UNKNOWN") return false;
  if (meta.freshness_state === "EXPIRED") return false;
  return true;
}

async function embeddings(env: Env, texts: string[]): Promise<number[][]> {
  const result: any = await env.AI.run(env.EMBEDDING_MODEL as any, { text: texts });
  const data = result?.data ?? result?.result?.data;
  if (!Array.isArray(data) || data.length !== texts.length) throw new Error("EMBEDDING_SHAPE_MISMATCH");
  return data;
}

function vectorMetadata(meta: KnowledgeMeta): Record<string, string> {
  return {
    retrieval_space: meta.retrieval_space,
    search_eligibility: meta.search_eligibility,
    governance_state: meta.governance_state,
    trust_state: meta.trust_state,
    freshness_state: meta.freshness_state,
    evidence_grade: meta.evidence_grade,
    authority_class: meta.authority_class,
    project_id: meta.project_id,
    domain_id: meta.domain_id,
    knowledge_role: meta.knowledge_role,
    canonical_id: meta.canonical_id,
  };
}

async function upsertObjectManifest(env: Env, meta: KnowledgeMeta, contentHash: string, namespace: string | null): Promise<void> {
  const existing = await env.RAG_DB.prepare(
    "SELECT canonical_id, source_locator FROM knowledge_object WHERE canonical_id = ?",
  ).bind(meta.canonical_id).first<{ canonical_id: string; source_locator: string }>();
  if (existing && existing.source_locator !== meta.source_locator) {
    throw new Error(`HOLD_CANONICAL_COLLISION:${meta.canonical_id}`);
  }

  await env.RAG_DB.prepare(`
    INSERT INTO knowledge_object (
      canonical_id, source_kind, source_locator, notion_page_id, title,
      retrieval_space, search_eligibility, governance_state, trust_state,
      freshness_state, evidence_grade, authority_class, project_id, domain_id,
      knowledge_role, object_type, last_edited_at, last_verified_at,
      verification_due, content_hash, schema_version, vector_namespace, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(canonical_id) DO UPDATE SET
      title=excluded.title,
      retrieval_space=excluded.retrieval_space,
      search_eligibility=excluded.search_eligibility,
      governance_state=excluded.governance_state,
      trust_state=excluded.trust_state,
      freshness_state=excluded.freshness_state,
      evidence_grade=excluded.evidence_grade,
      authority_class=excluded.authority_class,
      project_id=excluded.project_id,
      domain_id=excluded.domain_id,
      knowledge_role=excluded.knowledge_role,
      object_type=excluded.object_type,
      last_edited_at=excluded.last_edited_at,
      last_verified_at=excluded.last_verified_at,
      verification_due=excluded.verification_due,
      content_hash=excluded.content_hash,
      schema_version=excluded.schema_version,
      vector_namespace=excluded.vector_namespace,
      updated_at=CURRENT_TIMESTAMP
  `).bind(
    meta.canonical_id,
    meta.source_kind,
    meta.source_locator,
    meta.source_locator.replace("notion://", ""),
    meta.title,
    meta.retrieval_space,
    meta.search_eligibility,
    meta.governance_state,
    meta.trust_state,
    meta.freshness_state,
    meta.evidence_grade,
    meta.authority_class,
    meta.project_id,
    meta.domain_id,
    meta.knowledge_role,
    meta.object_type,
    meta.last_edited_at,
    meta.last_verified_at,
    meta.verification_due,
    contentHash,
    env.RAG_SCHEMA_VERSION,
    namespace,
  ).run();
}

async function syncNotionPage(env: Env, pageId: string): Promise<{ status: string; canonicalId?: string }> {
  const page = await notionFetch(env, `/pages/${pageId}`);
  if (page.archived || page.in_trash) {
    const existing = await env.RAG_DB.prepare("SELECT canonical_id FROM knowledge_object WHERE notion_page_id = ?")
      .bind(pageId).first<{ canonical_id: string }>();
    if (existing) await tombstoneObject(env, existing.canonical_id);
    return { status: "TOMBSTONED", canonicalId: existing?.canonical_id };
  }

  const meta = deriveKnowledgeMeta(page);
  const blocks = await fetchAllBlockChildren(env, pageId);
  const chunks = await makeChunks(meta, blocks);
  const contentHash = await sha256(chunks.map((c) => c.hash).join("|"));
  const namespace = namespaceFor(meta.retrieval_space);

  const prior = await env.RAG_DB.prepare(
    "SELECT content_hash, indexed_content_hash, vector_namespace FROM knowledge_object WHERE canonical_id = ?",
  ).bind(meta.canonical_id).first<{ content_hash: string; indexed_content_hash: string | null; vector_namespace: string | null }>();

  await upsertObjectManifest(env, meta, contentHash, namespace);

  if (!legallyIndexable(meta)) {
    await removeObjectVectors(env, meta.canonical_id);
    return { status: "MANIFEST_ONLY_NOT_QUERYABLE", canonicalId: meta.canonical_id };
  }

  const oldRows = await env.RAG_DB.prepare(
    "SELECT vector_id FROM knowledge_chunk WHERE canonical_id = ? AND active = 1 ORDER BY chunk_ordinal",
  ).bind(meta.canonical_id).all<{ vector_id: string }>();
  const oldIds = (oldRows.results ?? []).map((row) => row.vector_id);

  const contentChanged = prior?.indexed_content_hash !== contentHash;
  const namespaceChanged = prior?.vector_namespace !== namespace;

  if (!contentChanged && !namespaceChanged && oldIds.length) {
    // No material text delta: do not re-embed. Refresh metadata in-place using stored vector values.
    const oldVectors: any[] = await (env.OLEANDER_KNOWLEDGE as any).getByIds(oldIds);
    if (Array.isArray(oldVectors) && oldVectors.length === oldIds.length) {
      await env.OLEANDER_KNOWLEDGE.upsert(oldVectors.map((v: any) => ({
        id: v.id,
        values: v.values,
        namespace,
        metadata: vectorMetadata(meta),
      })));
      await env.RAG_DB.prepare("UPDATE knowledge_object SET indexed_at=CURRENT_TIMESTAMP WHERE canonical_id = ?")
        .bind(meta.canonical_id).run();
      return { status: "METADATA_REFRESH_NO_REEMBED", canonicalId: meta.canonical_id };
    }
  }

  const vectors = await embeddings(env, chunks.map((c) => c.text));
  const vectorRecords = chunks.map((chunk, i) => ({
    id: chunk.chunkId,
    values: vectors[i],
    namespace: namespace!,
    metadata: vectorMetadata(meta),
  }));
  const mutation: any = await env.OLEANDER_KNOWLEDGE.upsert(vectorRecords);

  const statements = [
    env.RAG_DB.prepare("UPDATE knowledge_chunk SET active = 0, updated_at=CURRENT_TIMESTAMP WHERE canonical_id = ?")
      .bind(meta.canonical_id),
    ...chunks.map((chunk) => env.RAG_DB.prepare(`
      INSERT INTO knowledge_chunk (
        chunk_id, canonical_id, chunk_ordinal, section_path, normalized_text,
        chunk_hash, vector_id, vector_namespace, active, updated_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, CURRENT_TIMESTAMP)
      ON CONFLICT(chunk_id) DO UPDATE SET
        section_path=excluded.section_path,
        normalized_text=excluded.normalized_text,
        chunk_hash=excluded.chunk_hash,
        vector_id=excluded.vector_id,
        vector_namespace=excluded.vector_namespace,
        active=1,
        updated_at=CURRENT_TIMESTAMP
    `).bind(chunk.chunkId, meta.canonical_id, chunk.ordinal, chunk.sectionPath, chunk.text, chunk.hash, chunk.chunkId, namespace)),
    env.RAG_DB.prepare(`
      UPDATE knowledge_object
      SET indexed_content_hash=?, embedding_model=?, vector_mutation_id=?, indexed_at=CURRENT_TIMESTAMP
      WHERE canonical_id=?
    `).bind(contentHash, env.EMBEDDING_MODEL, String(mutation?.mutationId ?? mutation?.mutation_id ?? "UNKNOWN"), meta.canonical_id),
  ];
  await env.RAG_DB.batch(statements);

  const newIds = new Set(chunks.map((c) => c.chunkId));
  const obsolete = oldIds.filter((id) => !newIds.has(id));
  if (obsolete.length) await env.OLEANDER_KNOWLEDGE.deleteByIds(obsolete);

  return { status: "INDEXED", canonicalId: meta.canonical_id };
}

async function removeObjectVectors(env: Env, canonicalId: string): Promise<void> {
  const rows = await env.RAG_DB.prepare("SELECT vector_id FROM knowledge_chunk WHERE canonical_id = ? AND active = 1")
    .bind(canonicalId).all<{ vector_id: string }>();
  const ids = (rows.results ?? []).map((r) => r.vector_id);
  if (ids.length) await env.OLEANDER_KNOWLEDGE.deleteByIds(ids);
  await env.RAG_DB.batch([
    env.RAG_DB.prepare("UPDATE knowledge_chunk SET active=0, updated_at=CURRENT_TIMESTAMP WHERE canonical_id = ?").bind(canonicalId),
    env.RAG_DB.prepare("UPDATE knowledge_object SET indexed_content_hash=NULL, vector_namespace=NULL, indexed_at=NULL WHERE canonical_id = ?").bind(canonicalId),
  ]);
}

async function tombstoneObject(env: Env, canonicalId: string): Promise<void> {
  await removeObjectVectors(env, canonicalId);
  await env.RAG_DB.prepare("UPDATE knowledge_object SET tombstoned_at=CURRENT_TIMESTAMP, governance_state='DELETED' WHERE canonical_id = ?")
    .bind(canonicalId).run();
}

function currentFilter(body: any): Record<string, unknown> {
  const clauses: Record<string, unknown>[] = [
    { retrieval_space: "CURRENT" },
    { search_eligibility: { $in: ["DEFAULT", "SCOPED"] } },
    { governance_state: { $in: ["ACTIVE", "CURRENT", "VALID"] } },
    { freshness_state: { $nin: ["EXPIRED"] } },
    { trust_state: body.include_unverified === false ? "VERIFIED" : { $in: ["VERIFIED", "UNVERIFIED"] } },
  ];
  if (body.project_id) clauses.push({ project_id: { $in: ["GLOBAL", String(body.project_id)] } });
  if (body.domain_id) clauses.push({ domain_id: { $in: ["GLOBAL", String(body.domain_id)] } });
  return { $and: clauses };
}

async function exactLookup(env: Env, query: string): Promise<any[]> {
  const result = await env.RAG_DB.prepare(`
    SELECT ko.* FROM knowledge_object ko
    WHERE ko.canonical_id = ?
       OR ko.canonical_id IN (SELECT canonical_id FROM knowledge_alias WHERE alias = ?)
       OR lower(ko.title) = lower(?)
    LIMIT 5
  `).bind(query, query, query).all();
  return result.results ?? [];
}

async function retrieve(env: Env, body: any): Promise<Response> {
  const started = Date.now();
  const query = String(body.query ?? "").trim();
  if (!query) return json({ error: "QUERY_REQUIRED" }, 400);
  const topK = Math.min(Math.max(Number(body.top_k ?? env.DEFAULT_TOP_K ?? 20), 1), 50);
  const queryId = crypto.randomUUID();

  const exact = await exactLookup(env, query);
  const embedded = await embeddings(env, [query]);
  const matches: any = await env.OLEANDER_KNOWLEDGE.query(embedded[0], {
    topK,
    namespace: "prod-current",
    filter: currentFilter(body) as any,
    returnMetadata: "indexed",
  });
  const rawMatches: any[] = matches?.matches ?? [];

  const vectorIds = rawMatches.map((m) => m.id);
  let rows: any[] = [];
  if (vectorIds.length) {
    const placeholders = vectorIds.map(() => "?").join(",");
    const result = await env.RAG_DB.prepare(`
      SELECT kc.vector_id, kc.normalized_text, kc.section_path, kc.chunk_ordinal,
             ko.canonical_id, ko.title, ko.source_locator, ko.retrieval_space,
             ko.search_eligibility, ko.governance_state, ko.trust_state,
             ko.freshness_state, ko.project_id, ko.domain_id, ko.knowledge_role
      FROM knowledge_chunk kc
      JOIN knowledge_object ko ON ko.canonical_id = kc.canonical_id
      WHERE kc.active = 1 AND kc.vector_id IN (${placeholders})
    `).bind(...vectorIds).all();
    rows = result.results ?? [];
  }

  const scoreById = new Map(rawMatches.map((m) => [m.id, Number(m.score ?? 0)]));
  const byCanonical = new Map<string, any>();
  for (const row of rows) {
    const item = {
      ...row,
      vector_score: scoreById.get(row.vector_id) ?? 0,
    };
    const prior = byCanonical.get(row.canonical_id);
    if (!prior || item.vector_score > prior.vector_score) byCanonical.set(row.canonical_id, item);
  }

  for (const item of exact) {
    if (item.retrieval_space !== "CURRENT") continue;
    if (!["DEFAULT", "SCOPED"].includes(item.search_eligibility)) continue;
    const existing = byCanonical.get(item.canonical_id);
    if (!existing) byCanonical.set(item.canonical_id, { ...item, vector_score: 1.0, exact_match: true });
    else existing.exact_match = true;
  }

  const current = [...byCanonical.values()].sort((a, b) => {
    if (a.exact_match && !b.exact_match) return -1;
    if (!a.exact_match && b.exact_match) return 1;
    return Number(b.vector_score) - Number(a.vector_score);
  }).slice(0, Math.min(topK, 10));

  const conflicts: string[] = [];
  const latency = Date.now() - started;
  await env.RAG_DB.prepare(`
    INSERT INTO retrieval_audit (
      query_id, authority_policy, project_id, domain_id, history_intent,
      top_k, candidate_count, result_count, conflict_count,
      support_expansion_used, latency_ms
    ) VALUES (?, 'CURRENT_DEFAULT', ?, ?, ?, ?, ?, ?, ?, 0, ?)
  `).bind(
    queryId,
    body.project_id ?? null,
    body.domain_id ?? null,
    body.history_intent ? 1 : 0,
    topK,
    rawMatches.length,
    current.length,
    conflicts.length,
    latency,
  ).run();

  return json({
    query_id: queryId,
    authority_policy: "CURRENT_DEFAULT",
    results: current.map((item) => ({
      canonical_id: item.canonical_id,
      title: item.title,
      source_locator: item.source_locator,
      status: {
        retrieval_space: item.retrieval_space,
        search_eligibility: item.search_eligibility,
        governance_state: item.governance_state,
        trust_state: item.trust_state,
        freshness_state: item.freshness_state,
      },
      score: {
        exact: Boolean(item.exact_match),
        vector: Number(item.vector_score ?? 0),
        lexical: null,
        rerank: null,
      },
      chunk: item.normalized_text ?? null,
      section: item.section_path ?? null,
    })),
    conflicts,
    support_expansion_used: false,
    latency_ms: latency,
  });
}

async function webhook(request: Request, env: Env): Promise<Response> {
  const raw = await request.text();
  const valid = await verifyNotionSignature(raw, request.headers.get("x-notion-signature"), env.NOTION_WEBHOOK_SECRET);
  if (!valid) return json({ error: "INVALID_NOTION_SIGNATURE" }, 401);

  const event: any = JSON.parse(raw);
  const eventId = String(event.id ?? event.event_id ?? "");
  const eventType = String(event.type ?? "unknown");
  const pageId = String(event.entity?.id ?? event.data?.page_id ?? event.page_id ?? "");
  if (!eventId || !pageId) return json({ error: "UNSUPPORTED_NOTION_EVENT" }, 400);

  const rawHash = await sha256(raw);
  const existing = await env.RAG_DB.prepare("SELECT event_id FROM sync_event WHERE event_id = ?")
    .bind(eventId).first();
  if (existing) return json({ status: "DUPLICATE_ACK", event_id: eventId }, 202);

  await env.RAG_DB.prepare(`
    INSERT INTO sync_event (event_id, notion_page_id, event_type, event_timestamp, delivery_attempt, raw_hash)
    VALUES (?, ?, ?, ?, ?, ?)
  `).bind(eventId, pageId, eventType, event.timestamp ?? null, event.delivery_attempt ?? null, rawHash).run();

  await env.SYNC_QUEUE.send({
    eventId,
    eventType,
    eventTimestamp: event.timestamp,
    deliveryAttempt: event.delivery_attempt,
    notionPageId: pageId,
  });
  return json({ status: "QUEUED", event_id: eventId }, 202);
}

async function health(env: Env): Promise<Response> {
  const counts = await env.RAG_DB.prepare(`
    SELECT
      COUNT(*) AS objects,
      SUM(CASE WHEN retrieval_space='CURRENT' THEN 1 ELSE 0 END) AS current_objects,
      SUM(CASE WHEN indexed_content_hash IS NOT NULL THEN 1 ELSE 0 END) AS indexed_objects,
      SUM(CASE WHEN trust_state='UNKNOWN' THEN 1 ELSE 0 END) AS unknown_trust
    FROM knowledge_object
    WHERE tombstoned_at IS NULL
  `).first();
  return json({ status: "ok", schema: env.RAG_SCHEMA_VERSION, counts });
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === "/health" && request.method === "GET") return health(env);
    if (url.pathname === "/webhooks/notion" && request.method === "POST") return webhook(request, env);
    if (url.pathname === "/v1/retrieve" && request.method === "POST") {
      if (!bearerAuthorized(request, env.RETRIEVAL_API_TOKEN)) return json({ error: "UNAUTHORIZED" }, 401);
      return retrieve(env, await request.json());
    }
    return json({ error: "NOT_FOUND" }, 404);
  },

  async queue(batch: MessageBatch<SyncMessage>, env: Env): Promise<void> {
    for (const message of batch.messages) {
      try {
        const result = await syncNotionPage(env, message.body.notionPageId);
        await env.RAG_DB.prepare(`
          UPDATE sync_event SET status=?, processed_at=CURRENT_TIMESTAMP, error_code=NULL, error_detail=NULL
          WHERE event_id=?
        `).bind(result.status, message.body.eventId).run();
        message.ack();
      } catch (error) {
        const detail = error instanceof Error ? error.message : String(error);
        const code = detail.split(":", 1)[0].slice(0, 120);
        await env.RAG_DB.prepare(`
          UPDATE sync_event SET status='FAILED', error_code=?, error_detail=? WHERE event_id=?
        `).bind(code, detail.slice(0, 1000), message.body.eventId).run();
        message.retry();
      }
    }
  },
};
