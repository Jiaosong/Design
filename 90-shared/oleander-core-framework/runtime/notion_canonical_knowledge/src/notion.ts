import {
  FIELDS,
  MAX_UNKNOWN_BLOCK_FETCHES,
  NOTION_MAX_FETCH_ATTEMPTS,
  NOTION_MIN_REQUEST_INTERVAL_MS,
  VALID_ELIGIBILITY,
  VALID_EXPLICIT_SPACES,
} from "./config";
import type { Env, NotionPage, PageMarkdown } from "./types";

export class NotionHttpError extends Error {
  constructor(
    public readonly status: number,
    public readonly body: string,
  ) {
    super(`Notion API ${status}: ${body.slice(0, 500)}`);
  }
}

function headers(env: Env): HeadersInit {
  return {
    Authorization: `Bearer ${env.NOTION_TOKEN}`,
    "Notion-Version": env.NOTION_VERSION,
    "Content-Type": "application/json",
  };
}

async function notionFetch<T>(env: Env, path: string, init: RequestInit = {}): Promise<T> {
  for (let attempt = 0; attempt < NOTION_MAX_FETCH_ATTEMPTS; attempt += 1) {
    await new Promise((resolve) => setTimeout(resolve, NOTION_MIN_REQUEST_INTERVAL_MS));
    const response = await fetch(`https://api.notion.com${path}`, {
      ...init,
      headers: { ...headers(env), ...(init.headers ?? {}) },
    });
    if (response.ok) return (await response.json()) as T;

    const body = await response.text();
    const retryable = response.status === 429 || [500, 502, 503, 504].includes(response.status);
    if (!retryable || attempt === NOTION_MAX_FETCH_ATTEMPTS - 1) {
      throw new NotionHttpError(response.status, body);
    }

    const retryAfter = Number.parseInt(response.headers.get("Retry-After") ?? "", 10);
    const delayMs = response.status === 429 && Number.isFinite(retryAfter) && retryAfter > 0
      ? retryAfter * 1000
      : Math.min(8_000, 500 * 2 ** attempt);
    await new Promise((resolve) => setTimeout(resolve, delayMs));
  }

  throw new Error("Notion fetch retry loop exhausted unexpectedly");
}

export async function fetchPage(env: Env, pageId: string): Promise<NotionPage> {
  return notionFetch<NotionPage>(env, `/v1/pages/${encodeURIComponent(pageId)}`);
}

export interface GovernanceScalarUpdates {
  canonical_id?: string | null;
  retrieval_space?: string | null;
  search_eligibility?: string | null;
  governance_state?: string | null;
  relation_state?: string | null;
}

export interface AcademicPageInput {
  title: string;
  canonical_id: string;
  markdown: string;
  retrieval_space?: string;
  search_eligibility?: string;
  trust_state?: string;
  governance_state?: string;
  relation_state?: string;
  content_level?: string;
  knowledge_role?: string;
  source_page_ids?: string[];
  replaced_page_ids?: string[];
}

interface NotionDataSource {
  object: "data_source";
  id: string;
  properties?: Record<string, Record<string, unknown>>;
}

interface NotionView {
  object: "view";
  id: string;
  name?: string;
  type?: string;
}

const GOVERNANCE_FIELDS = {
  canonical_id: FIELDS.canonicalId,
  retrieval_space: FIELDS.retrievalSpace,
  search_eligibility: FIELDS.searchEligibility,
  governance_state: FIELDS.governanceState,
  relation_state: FIELDS.relationState,
} as const;

const VALID_GOVERNANCE_STATES = new Set(["ACTIVE", "ARCHIVED", "HOLD", "LEGACY", "REVIEW"]);
const VALID_RELATION_STATES = new Set(["REVIEW", "VALID"]);

function propertyMutation(property: Record<string, unknown> | undefined, value: string | null): Record<string, unknown> {
  if (!property || typeof property.type !== "string") throw new Error("Target Notion property is missing or has no type");
  if (property.type === "rich_text") {
    return { rich_text: value === null ? [] : [{ type: "text", text: { content: value } }] };
  }
  if (property.type === "title") {
    return { title: value === null ? [] : [{ type: "text", text: { content: value } }] };
  }
  if (property.type === "select") return { select: value === null ? null : { name: value } };
  if (property.type === "status") return { status: value === null ? null : { name: value } };
  throw new Error(`Unsupported governance property type: ${property.type}`);
}

function relationMutation(property: Record<string, unknown> | undefined, ids: string[]): Record<string, unknown> {
  if (!property || property.type !== "relation") throw new Error("Target Notion relation property is missing or not a relation");
  return { relation: ids.map((id) => ({ id })) };
}

export function buildGovernancePropertyPatch(
  page: NotionPage,
  updates: GovernanceScalarUpdates,
): Record<string, Record<string, unknown>> {
  if (updates.retrieval_space !== undefined && updates.retrieval_space !== null && !VALID_EXPLICIT_SPACES.has(updates.retrieval_space)) {
    throw new Error(`Invalid retrieval_space: ${updates.retrieval_space}`);
  }
  if (
    updates.search_eligibility !== undefined &&
    updates.search_eligibility !== null &&
    !VALID_ELIGIBILITY.has(updates.search_eligibility)
  ) {
    throw new Error(`Invalid search_eligibility: ${updates.search_eligibility}`);
  }
  if (
    updates.governance_state !== undefined &&
    updates.governance_state !== null &&
    !VALID_GOVERNANCE_STATES.has(updates.governance_state)
  ) {
    throw new Error(`Invalid governance_state: ${updates.governance_state}`);
  }
  if (
    updates.relation_state !== undefined &&
    updates.relation_state !== null &&
    !VALID_RELATION_STATES.has(updates.relation_state)
  ) {
    throw new Error(`Invalid relation_state: ${updates.relation_state}`);
  }
  const properties = page.properties ?? {};
  const patch: Record<string, Record<string, unknown>> = {};
  for (const [key, value] of Object.entries(updates) as Array<[keyof GovernanceScalarUpdates, string | null | undefined]>) {
    if (value === undefined) continue;
    const notionField = GOVERNANCE_FIELDS[key];
    patch[notionField] = propertyMutation(properties[notionField], value);
  }
  if (Object.keys(patch).length === 0) throw new Error("No governance updates supplied");
  return patch;
}

export async function updatePageGovernanceFields(
  env: Env,
  pageId: string,
  updates: GovernanceScalarUpdates,
): Promise<NotionPage> {
  const before = await fetchPage(env, pageId);
  const properties = buildGovernancePropertyPatch(before, updates);
  return notionFetch<NotionPage>(env, `/v1/pages/${encodeURIComponent(pageId)}`, {
    method: "PATCH",
    body: JSON.stringify({ properties }),
  });
}

export async function retrieveNotesDataSource(env: Env): Promise<NotionDataSource> {
  return notionFetch<NotionDataSource>(env, `/v1/data_sources/${encodeURIComponent(env.NOTION_NOTES_DATA_SOURCE_ID)}`);
}

export async function createAcademicPage(env: Env, input: AcademicPageInput): Promise<NotionPage> {
  const dataSource = await retrieveNotesDataSource(env);
  const schema = dataSource.properties ?? {};
  const properties: Record<string, Record<string, unknown>> = {
    [FIELDS.title]: propertyMutation(schema[FIELDS.title], input.title),
    [FIELDS.canonicalId]: propertyMutation(schema[FIELDS.canonicalId], input.canonical_id),
    [FIELDS.retrievalSpace]: propertyMutation(schema[FIELDS.retrievalSpace], input.retrieval_space ?? "CURRENT"),
    [FIELDS.searchEligibility]: propertyMutation(schema[FIELDS.searchEligibility], input.search_eligibility ?? "DEFAULT"),
    [FIELDS.trustState]: propertyMutation(schema[FIELDS.trustState], input.trust_state ?? "UNVERIFIED"),
    [FIELDS.governanceState]: propertyMutation(schema[FIELDS.governanceState], input.governance_state ?? "ACTIVE"),
    [FIELDS.relationState]: propertyMutation(schema[FIELDS.relationState], input.relation_state ?? "REVIEW"),
    [FIELDS.contentLevel]: propertyMutation(schema[FIELDS.contentLevel], input.content_level ?? "L5｜Knowledge Object"),
    [FIELDS.knowledgeRole]: propertyMutation(schema[FIELDS.knowledgeRole], input.knowledge_role ?? "THEORY"),
  };
  if (input.source_page_ids?.length) {
    properties[FIELDS.sourceRelations] = relationMutation(schema[FIELDS.sourceRelations], input.source_page_ids);
  }
  if (input.replaced_page_ids?.length) {
    properties[FIELDS.replacedDocuments] = relationMutation(schema[FIELDS.replacedDocuments], input.replaced_page_ids);
  }

  return notionFetch<NotionPage>(env, "/v1/pages", {
    method: "POST",
    body: JSON.stringify({
      parent: { type: "data_source_id", data_source_id: env.NOTION_NOTES_DATA_SOURCE_ID },
      properties,
      markdown: input.markdown,
    }),
  });
}

export async function createReaderPage(env: Env): Promise<NotionPage> {
  return notionFetch<NotionPage>(env, "/v1/pages", {
    method: "POST",
    body: JSON.stringify({
      parent: { type: "page_id", page_id: env.NOTION_ROOT_PAGE_ID },
      properties: {
        title: { title: [{ type: "text", text: { content: "知识阅读台｜Knowledge Reader" } }] },
      },
      markdown: [
        "# 知识阅读台｜Knowledge Reader",
        "",
        "> 这是给人阅读的入口，不是后台治理数据库。日常阅读优先从 Current 开始；需要方法、案例或来源时再进入 Support；HOLD / REVIEW / PROVENANCE 属于治理与历史层，不作为默认阅读材料。",
        "",
        "## 阅读原则",
        "",
        "1. **Current**：当前可直接调用的核心知识与来源。",
        "2. **Curated Support**：已显式进入 SUPPORT / SCOPED 的方法、理论、案例与证据。",
        "3. **Review Queue**：只用于整理，不代表内容成立。",
        "",
        "后台 1184 页 Canonical corpus 继续保留；这里仅改变阅读入口，不删除历史。",
      ].join("\n"),
    }),
  });
}

export async function createLinkedNotesView(
  env: Env,
  parentPageId: string,
  input: { name: string; type: "list" | "table"; filter: Record<string, unknown>; sorts?: Array<Record<string, unknown>> },
): Promise<NotionView> {
  return notionFetch<NotionView>(env, "/v1/views", {
    method: "POST",
    body: JSON.stringify({
      create_database: { parent: { type: "page_id", page_id: parentPageId } },
      data_source_id: env.NOTION_NOTES_DATA_SOURCE_ID,
      name: input.name,
      type: input.type,
      filter: input.filter,
      ...(input.sorts?.length ? { sorts: input.sorts } : {}),
    }),
  });
}

async function fetchMarkdownNode(env: Env, id: string): Promise<PageMarkdown> {
  return notionFetch<PageMarkdown>(env, `/v1/pages/${encodeURIComponent(id)}/markdown`);
}

export async function fetchCompleteMarkdown(env: Env, pageId: string): Promise<PageMarkdown> {
  const root = await fetchMarkdownNode(env, pageId);
  if (!root.truncated || root.unknown_block_ids.length === 0) return root;

  const queue = [...root.unknown_block_ids];
  const seen = new Set<string>();
  const recovered: string[] = [];
  const unresolved: string[] = [];

  while (queue.length > 0 && seen.size < MAX_UNKNOWN_BLOCK_FETCHES) {
    const blockId = queue.shift();
    if (!blockId || seen.has(blockId)) continue;
    seen.add(blockId);
    try {
      const block = await fetchMarkdownNode(env, blockId);
      recovered.push(block.markdown);
      for (const child of block.unknown_block_ids) if (!seen.has(child)) queue.push(child);
    } catch (error) {
      if (error instanceof NotionHttpError && error.status === 404) {
        unresolved.push(blockId);
        continue;
      }
      throw error;
    }
  }

  unresolved.push(...queue);
  return {
    ...root,
    markdown: [root.markdown, ...recovered].filter(Boolean).join("\n\n"),
    truncated: unresolved.length > 0,
    unknown_block_ids: [...new Set(unresolved)],
  };
}

interface QueryDataSourceResponse {
  results: Array<{ object?: string; id?: string }>;
  has_more: boolean;
  next_cursor: string | null;
}

export async function* listNotesPages(env: Env): AsyncGenerator<string> {
  let cursor: string | undefined;
  do {
    const payload: Record<string, unknown> = { page_size: 100, result_type: "page" };
    if (cursor) payload.start_cursor = cursor;
    const result = await notionFetch<QueryDataSourceResponse>(
      env,
      `/v1/data_sources/${encodeURIComponent(env.NOTION_NOTES_DATA_SOURCE_ID)}/query`,
      { method: "POST", body: JSON.stringify(payload) },
    );
    for (const item of result.results) {
      if (item.object === "page" && item.id) yield item.id;
    }
    cursor = result.has_more && result.next_cursor ? result.next_cursor : undefined;
  } while (cursor);
}
