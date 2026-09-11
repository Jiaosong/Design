import { MAX_UNKNOWN_BLOCK_FETCHES, NOTION_MAX_FETCH_ATTEMPTS, NOTION_MIN_REQUEST_INTERVAL_MS } from "./config";
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
