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

export class NotionReadbackBudgetError extends Error {
  constructor() {
    super("Notion framework readback deadline exceeded");
  }
}

async function waitWithinDeadline(delayMs: number, deadlineAtMs?: number): Promise<void> {
  if (deadlineAtMs === undefined) {
    await new Promise((resolve) => setTimeout(resolve, delayMs));
    return;
  }
  const remainingMs = deadlineAtMs - Date.now();
  if (remainingMs <= 0) throw new NotionReadbackBudgetError();
  if (delayMs >= remainingMs) {
    await new Promise((resolve) => setTimeout(resolve, remainingMs));
    throw new NotionReadbackBudgetError();
  }
  await new Promise((resolve) => setTimeout(resolve, delayMs));
}

async function notionFetch<T>(
  env: Env,
  path: string,
  init: RequestInit = {},
  deadlineAtMs?: number,
): Promise<T> {
  for (let attempt = 0; attempt < NOTION_MAX_FETCH_ATTEMPTS; attempt += 1) {
    await waitWithinDeadline(NOTION_MIN_REQUEST_INTERVAL_MS, deadlineAtMs);
    const remainingMs = deadlineAtMs === undefined ? null : deadlineAtMs - Date.now();
    if (remainingMs !== null && remainingMs <= 0) throw new NotionReadbackBudgetError();
    const controller = deadlineAtMs === undefined ? null : new AbortController();
    const timeout = controller && remainingMs !== null
      ? setTimeout(() => controller.abort(), remainingMs)
      : null;
    let delayMs: number | null = null;
    try {
      const response = await fetch(`https://api.notion.com${path}`, {
        ...init,
        headers: { ...headers(env), ...(init.headers ?? {}) },
        ...(controller ? { signal: controller.signal } : {}),
      });
      // Keep the same AbortController alive through body consumption. Fetch can
      // resolve as soon as headers arrive; clearing the timer before json/text
      // parsing would let a stalled response body escape the Reader deadline.
      if (response.ok) return (await response.json()) as T;

      const body = await response.text();
      const retryable = response.status === 429 || [500, 502, 503, 504].includes(response.status);
      if (!retryable || attempt === NOTION_MAX_FETCH_ATTEMPTS - 1) {
        throw new NotionHttpError(response.status, body);
      }

      const retryAfter = Number.parseInt(response.headers.get("Retry-After") ?? "", 10);
      delayMs = response.status === 429 && Number.isFinite(retryAfter) && retryAfter > 0
        ? retryAfter * 1000
        : Math.min(8_000, 500 * 2 ** attempt);
    } catch (error) {
      if (controller?.signal.aborted) throw new NotionReadbackBudgetError();
      throw error;
    } finally {
      if (timeout !== null) clearTimeout(timeout);
    }
    if (delayMs === null) throw new Error("Notion retry delay missing unexpectedly");
    await waitWithinDeadline(delayMs, deadlineAtMs);
  }

  throw new Error("Notion fetch retry loop exhausted unexpectedly");
}

export async function fetchPage(env: Env, pageId: string, deadlineAtMs?: number): Promise<NotionPage> {
  return notionFetch<NotionPage>(env, `/v1/pages/${encodeURIComponent(pageId)}`, {}, deadlineAtMs);
}

interface NotionPropertyItemListResponse {
  object: "list";
  results: Array<Record<string, unknown>>;
  has_more?: boolean;
  next_cursor?: string | null;
}

export interface NotionRelationReadback {
  ids: string[];
  complete: boolean;
}

const NOTION_RELATION_READBACK_MAX_PAGES = 20;
const NOTION_DOMAIN_INVENTORY_MAX_PAGES = 20;

function relationIdsFromPageProperty(property: Record<string, unknown> | undefined): string[] {
  if (!property || property.type !== "relation" || !Array.isArray(property.relation)) return [];
  return property.relation
    .map((item) => (item && typeof item === "object" ? (item as Record<string, unknown>).id : null))
    .filter((id): id is string => typeof id === "string");
}

/**
 * Read a relation exactly as declared on the live Notion page. Notion can
 * truncate relation values embedded in a page response and mark `has_more`;
 * when that happens, walk the page-property endpoint rather than silently
 * treating the partial array as complete.
 */
export async function fetchRelationReadback(
  env: Env,
  page: NotionPage,
  fieldName: string,
  deadlineAtMs?: number,
): Promise<NotionRelationReadback> {
  const property = page.properties?.[fieldName];
  // Missing/retagged fields are schema drift, not an authoritative empty
  // relation. Fail closed so the Reader can distinguish "empty" from
  // "not successfully read as the expected relation property".
  if (!property || property.type !== "relation") return { ids: [], complete: false };
  const initialIds = relationIdsFromPageProperty(property);
  if (property.has_more !== true) return { ids: [...new Set(initialIds)], complete: true };

  const propertyId = typeof property.id === "string" ? property.id : null;
  if (!propertyId) return { ids: [...new Set(initialIds)], complete: false };

  const ids: string[] = [];
  let cursor: string | null = null;
  const seenCursors = new Set<string>();
  for (let pageNumber = 0; pageNumber < NOTION_RELATION_READBACK_MAX_PAGES; pageNumber += 1) {
    const params = new URLSearchParams({ page_size: "100" });
    if (cursor) params.set("start_cursor", cursor);
    const response = await notionFetch<NotionPropertyItemListResponse>(
      env,
      `/v1/pages/${encodeURIComponent(page.id)}/properties/${encodeURIComponent(propertyId)}?${params.toString()}`,
      {},
      deadlineAtMs,
    );
    for (const result of response.results) {
      const relation = result.relation;
      if (!relation || typeof relation !== "object") continue;
      const id = (relation as Record<string, unknown>).id;
      if (typeof id === "string") ids.push(id);
    }
    if (!response.has_more) return { ids: [...new Set(ids)], complete: true };
    if (!response.next_cursor) return { ids: [...new Set(ids.length ? ids : initialIds)], complete: false };
    if (seenCursors.has(response.next_cursor)) {
      return { ids: [...new Set(ids.length ? ids : initialIds)], complete: false };
    }
    seenCursors.add(response.next_cursor);
    cursor = response.next_cursor;
  }
  return { ids: [...new Set(ids.length ? ids : initialIds)], complete: false };
}

interface DomainRegistryQueryResponse {
  results: NotionPage[];
  has_more: boolean;
  next_cursor: string | null;
}

export interface DomainRegistryReadback {
  pages: NotionPage[];
  complete: boolean;
}

/**
 * Query the authoritative Current Domain data source as one bounded inventory
 * instead of issuing one live page request per related Domain. This both
 * verifies registry membership and keeps Reader detail latency bounded.
 */
export async function queryDomainRegistryPages(env: Env, deadlineAtMs?: number): Promise<DomainRegistryReadback> {
  const pages: NotionPage[] = [];
  let cursor: string | null = null;
  const seenCursors = new Set<string>();
  for (let pageNumber = 0; pageNumber < NOTION_DOMAIN_INVENTORY_MAX_PAGES; pageNumber += 1) {
    const payload: Record<string, unknown> = { page_size: 100, result_type: "page" };
    if (cursor) payload.start_cursor = cursor;
    const response = await notionFetch<DomainRegistryQueryResponse>(
      env,
      `/v1/data_sources/${encodeURIComponent(env.NOTION_DOMAINS_DATA_SOURCE_ID)}/query`,
      { method: "POST", body: JSON.stringify(payload) },
      deadlineAtMs,
    );
    pages.push(...response.results.filter((page) => page.object === "page" && typeof page.id === "string"));
    if (!response.has_more) return { pages, complete: true };
    if (!response.next_cursor || seenCursors.has(response.next_cursor)) return { pages, complete: false };
    seenCursors.add(response.next_cursor);
    cursor = response.next_cursor;
  }
  return { pages, complete: false };
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

export interface NotionDataSource {
  object: "data_source";
  id: string;
  properties?: Record<string, Record<string, unknown>>;
}

export interface NotionView {
  object: "view";
  id: string;
  name?: string;
  type?: string;
  url?: string;
  data_source_id?: string | null;
  parent?: { type?: string; database_id?: string };
  filter?: Record<string, unknown> | null;
  sorts?: Array<Record<string, unknown>> | null;
  configuration?: Record<string, unknown> | null;
  dashboard_view_id?: string | null;
}

interface NotionViewListResponse {
  object: "list";
  results: Array<NotionView | { object?: string; id?: string; view?: NotionView }>;
  has_more?: boolean;
  next_cursor?: string | null;
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

export async function updatePageMarkdownContent(
  env: Env,
  pageId: string,
  oldStr: string,
  newStr: string,
): Promise<void> {
  if (!oldStr.trim() || !newStr.trim()) throw new Error("old_str and new_str must be non-empty");
  if (oldStr === newStr) throw new Error("old_str and new_str must differ");
  await notionFetch<unknown>(env, `/v1/pages/${encodeURIComponent(pageId)}/markdown`, {
    method: "PATCH",
    body: JSON.stringify({
      type: "update_content",
      update_content: {
        content_updates: [{ old_str: oldStr, new_str: newStr }],
      },
    }),
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
        "> 这是给人阅读的入口，不是后台治理数据库。第一层先以 L4/L5 + ACTIVE + VALID 形成迁移期的 Core Knowledge；方法、证据、实践分开阅读；HOLD / REVIEW / PROVENANCE 属于治理与历史层，不作为默认阅读材料。",
        "",
        "## 阅读原则",
        "",
        "1. **Core Knowledge**：L4/L5 的稳定框架、理论与知识对象，先读结论与论证。",
        "2. **Methods**：回答“怎么做”，不与理论、证据卡混在同一列表。",
        "3. **Evidence / Practice**：需要查证或看真实执行时再进入。",
        "4. **History**：只用于追溯，不与当前阅读竞争注意力。",
        "",
        "后台 Canonical corpus 继续保留；这里仅改变阅读入口，不删除历史。随着 Retrieval Space 迁移完成，再增加严格 CURRENT / DEFAULT 的第一视图。",
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

export async function retrieveView(env: Env, viewId: string): Promise<NotionView> {
  return notionFetch<NotionView>(env, `/v1/views/${encodeURIComponent(viewId)}`);
}

export async function listDatabaseViews(env: Env, databaseId: string): Promise<NotionView[]> {
  const response = await notionFetch<NotionViewListResponse>(
    env,
    `/v1/views?database_id=${encodeURIComponent(databaseId)}`,
  );
  const views = response.results
    .map((entry) => ("view" in entry && entry.view ? entry.view : entry as NotionView))
    .filter((entry) => Boolean(entry?.id));
  const hydrated: NotionView[] = [];
  for (const view of views) {
    hydrated.push(view.name && view.type ? view : await retrieveView(env, view.id));
  }
  return hydrated;
}

export async function updateView(
  env: Env,
  viewId: string,
  updates: {
    name?: string;
    filter?: Record<string, unknown> | null;
    sorts?: Array<Record<string, unknown>> | null;
    quick_filters?: Record<string, unknown> | null;
    configuration?: Record<string, unknown> | null;
  },
): Promise<NotionView> {
  return notionFetch<NotionView>(env, `/v1/views/${encodeURIComponent(viewId)}`, {
    method: "PATCH",
    body: JSON.stringify(updates),
  });
}

export async function createViewOnDatabase(
  env: Env,
  input: {
    database_id: string;
    data_source_id: string;
    name: string;
    type: "list" | "table" | "gallery" | "chart" | "board" | "dashboard";
    filter?: Record<string, unknown> | null;
    sorts?: Array<Record<string, unknown>> | null;
    configuration?: Record<string, unknown> | null;
    position?: Record<string, unknown>;
  },
): Promise<NotionView> {
  return notionFetch<NotionView>(env, "/v1/views", {
    method: "POST",
    body: JSON.stringify({
      database_id: input.database_id,
      data_source_id: input.data_source_id,
      name: input.name,
      type: input.type,
      ...(input.filter ? { filter: input.filter } : {}),
      ...(input.sorts?.length ? { sorts: input.sorts } : {}),
      ...(input.configuration ? { configuration: input.configuration } : {}),
      ...(input.position ? { position: input.position } : {}),
    }),
  });
}

export async function createDashboardWidgetView(
  env: Env,
  input: {
    dashboard_view_id: string;
    data_source_id: string;
    name: string;
    type: "list" | "table" | "gallery" | "chart" | "board";
    filter?: Record<string, unknown> | null;
    sorts?: Array<Record<string, unknown>> | null;
    configuration?: Record<string, unknown> | null;
    placement?: { type: "new_row"; row_index?: number } | { type: "existing_row"; row_index: number };
  },
): Promise<NotionView> {
  return notionFetch<NotionView>(env, "/v1/views", {
    method: "POST",
    body: JSON.stringify({
      view_id: input.dashboard_view_id,
      data_source_id: input.data_source_id,
      name: input.name,
      type: input.type,
      ...(input.filter ? { filter: input.filter } : {}),
      ...(input.sorts?.length ? { sorts: input.sorts } : {}),
      ...(input.configuration ? { configuration: input.configuration } : {}),
      ...(input.placement ? { placement: input.placement } : {}),
    }),
  });
}

export async function replaceReaderIntroMarkdown(env: Env, pageId: string, newIntro: string): Promise<void> {
  const current = await fetchCompleteMarkdown(env, pageId);
  const firstDatabase = current.markdown.indexOf("<database ");
  if (firstDatabase < 0) throw new Error("Reader page does not contain linked database blocks");
  const oldIntro = current.markdown.slice(0, firstDatabase).trim();
  if (!oldIntro) throw new Error("Reader page intro is empty");

  await notionFetch<unknown>(env, `/v1/pages/${encodeURIComponent(pageId)}/markdown`, {
    method: "PATCH",
    body: JSON.stringify({
      type: "update_content",
      update_content: {
        content_updates: [{ old_str: oldIntro, new_str: newIntro.trim() }],
      },
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
  results: Array<{ object?: string; id?: string; last_edited_time?: string; in_trash?: boolean }>;
  has_more: boolean;
  next_cursor: string | null;
}

export interface NotesPageRef {
  id: string;
  lastEditedTime: string | null;
  inTrash: boolean;
}

export interface NotesDeltaPage {
  pages: NotesPageRef[];
  hasMore: boolean;
  nextCursor: string | null;
}

export function buildNotesDeltaQueryPayload(
  fromInclusive: string,
  throughInclusive: string,
  startCursor?: string | null,
): Record<string, unknown> {
  const payload: Record<string, unknown> = {
    page_size: 100,
    result_type: "page",
    filter: {
      and: [
        {
          timestamp: "last_edited_time",
          last_edited_time: { on_or_after: fromInclusive },
        },
        {
          timestamp: "last_edited_time",
          last_edited_time: { on_or_before: throughInclusive },
        },
      ],
    },
    sorts: [{ timestamp: "last_edited_time", direction: "ascending" }],
  };
  if (startCursor) payload.start_cursor = startCursor;
  return payload;
}

export async function queryNotesPagesEditedBetween(
  env: Env,
  fromInclusive: string,
  throughInclusive: string,
  startCursor?: string | null,
): Promise<NotesDeltaPage> {
  const result = await notionFetch<QueryDataSourceResponse>(
    env,
    `/v1/data_sources/${encodeURIComponent(env.NOTION_NOTES_DATA_SOURCE_ID)}/query`,
    {
      method: "POST",
      body: JSON.stringify(buildNotesDeltaQueryPayload(fromInclusive, throughInclusive, startCursor)),
    },
  );
  return {
    pages: result.results
      .filter((item) => item.object === "page" && typeof item.id === "string")
      .map((item) => ({
        id: item.id as string,
        lastEditedTime: typeof item.last_edited_time === "string" ? item.last_edited_time : null,
        inTrash: item.in_trash === true,
      })),
    hasMore: result.has_more,
    nextCursor: result.has_more ? result.next_cursor : null,
  };
}

export async function queryNotesInventoryPage(
  env: Env,
  startCursor?: string | null,
): Promise<NotesDeltaPage> {
  const payload: Record<string, unknown> = {
    page_size: 100,
    result_type: "page",
    sorts: [{ timestamp: "last_edited_time", direction: "ascending" }],
  };
  if (startCursor) payload.start_cursor = startCursor;
  const result = await notionFetch<QueryDataSourceResponse>(
    env,
    `/v1/data_sources/${encodeURIComponent(env.NOTION_NOTES_DATA_SOURCE_ID)}/query`,
    { method: "POST", body: JSON.stringify(payload) },
  );
  return {
    pages: result.results
      .filter((item) => item.object === "page" && typeof item.id === "string")
      .map((item) => ({
        id: item.id as string,
        lastEditedTime: typeof item.last_edited_time === "string" ? item.last_edited_time : null,
        inTrash: item.in_trash === true,
      })),
    hasMore: result.has_more,
    nextCursor: result.has_more ? result.next_cursor : null,
  };
}

export async function* listNotesPages(env: Env): AsyncGenerator<string> {
  let cursor: string | undefined;
  do {
    const result = await queryNotesInventoryPage(env, cursor);
    for (const item of result.pages) yield item.id;
    cursor = result.hasMore && result.nextCursor ? result.nextCursor : undefined;
  } while (cursor);
}
