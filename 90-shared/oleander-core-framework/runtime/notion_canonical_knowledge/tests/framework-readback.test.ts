import { afterEach, describe, expect, it, vi } from "vitest";
import { fetchRelationReadback, NotionReadbackBudgetError, queryDomainRegistryPages, queryProjectRegistryPages } from "../src/notion";
import { normalizePage, propertyMultiSelectNames } from "../src/normalize";
import { hydrateKnowledgeReaderFramework, methodFamilyReadback, primaryDomainRoutingReadiness, safeRelationReadback } from "../src/reader";
import type { Env, KnowledgeReaderDetail, KnowledgeReaderFrameworkObjectRef, NotionPage, NotionProperty } from "../src/types";

describe("framework readback normalization", () => {
  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  it("reads Method Family from the canonical multi-select without semantic inference", () => {
    const property: NotionProperty = {
      type: "multi_select",
      multi_select: [{ id: "a", name: "研究取证" }, { id: "b", name: "评估验证" }],
    };
    expect(propertyMultiSelectNames(property)).toEqual(["研究取证", "评估验证"]);
  });

  it("fails closed when Method Family is missing or no longer a multi-select", () => {
    const missing: NotionPage = { object: "page", id: "page-missing", properties: {} };
    const retagged: NotionPage = {
      object: "page",
      id: "page-retagged",
      properties: { "方法家族": { type: "rich_text", rich_text: [] } },
    };
    expect(methodFamilyReadback(missing)).toEqual({ names: [], complete: false });
    expect(methodFamilyReadback(retagged)).toEqual({ names: [], complete: false });
  });

  it("keeps Canonical hierarchy distinct from Source and Method relations", () => {
    const page: NotionPage = {
      object: "page",
      id: "page-1",
      properties: {
        Name: { type: "title", title: [{ plain_text: "Method object" }] },
        "Canonical Parent｜层级上位": { type: "relation", relation: [{ id: "parent-1" }] },
        "Canonical Children｜层级子级": { type: "relation", relation: [{ id: "child-1" }, { id: "child-2" }] },
        "方法家族": { type: "multi_select", multi_select: [{ name: "分析建模" }] },
        "来源文档": { type: "relation", relation: [{ id: "source-1" }] },
        "引用方法": { type: "relation", relation: [{ id: "method-1" }] },
      },
    };
    const normalized = normalizePage(page);
    expect(normalized.canonicalParentIds).toEqual(["parent-1"]);
    expect(normalized.canonicalChildrenIds).toEqual(["child-1", "child-2"]);
    expect(normalized.methodFamilies).toEqual(["分析建模"]);
    expect(normalized.sourceRelationIds).toEqual(["source-1"]);
    expect(normalized.methodRelationIds).toEqual(["method-1"]);
  });

  it("keeps semantic Related and Project-use relations distinct from hierarchy and lineage", async () => {
    const page: NotionPage = {
      object: "page",
      id: "page-1",
      properties: {
        "相关笔记": { type: "relation", relation: [{ id: "related-note-1" }] },
        "主项目": { type: "relation", relation: [{ id: "project-main" }] },
        "关联项目": { type: "relation", relation: [{ id: "project-related" }] },
        "来源文档": { type: "relation", relation: [{ id: "source-1" }] },
        "引用方法": { type: "relation", relation: [{ id: "method-1" }] },
        "Canonical Parent｜层级上位": { type: "relation", relation: [{ id: "parent-1" }] },
      },
    };
    const env = {} as Env;
    await expect(safeRelationReadback(env, page, "相关笔记")).resolves.toEqual({ ids: ["related-note-1"], complete: true });
    await expect(safeRelationReadback(env, page, "主项目")).resolves.toEqual({ ids: ["project-main"], complete: true });
    await expect(safeRelationReadback(env, page, "关联项目")).resolves.toEqual({ ids: ["project-related"], complete: true });
    expect(normalizePage(page).sourceRelationIds).toEqual(["source-1"]);
    expect(normalizePage(page).methodRelationIds).toEqual(["method-1"]);
    expect(normalizePage(page).canonicalParentIds).toEqual(["parent-1"]);
  });

  it("fails closed when an expected relation field is missing or retagged", async () => {
    const page: NotionPage = {
      object: "page",
      id: "page-1",
      properties: {
        "主领域": { type: "rich_text", rich_text: [] },
      },
    };
    const env = {} as Env;
    await expect(fetchRelationReadback(env, page, "主领域")).resolves.toEqual({ ids: [], complete: false });
    await expect(fetchRelationReadback(env, page, "关联领域")).resolves.toEqual({ ids: [], complete: false });
  });

  it("paginates a truncated relation through next_cursor and returns the complete ID set", async () => {
    vi.useFakeTimers();
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(JSON.stringify({
        object: "list",
        results: [{ object: "property_item", relation: { id: "child-1" } }],
        has_more: true,
        next_cursor: "cursor-1",
      }), { status: 200, headers: { "Content-Type": "application/json" } }))
      .mockResolvedValueOnce(new Response(JSON.stringify({
        object: "list",
        results: [{ object: "property_item", relation: { id: "child-2" } }],
        has_more: false,
        next_cursor: null,
      }), { status: 200, headers: { "Content-Type": "application/json" } }));
    const page: NotionPage = {
      object: "page",
      id: "page-1",
      properties: {
        "Canonical Children｜层级子级": {
          id: "children-prop",
          type: "relation",
          relation: [{ id: "embedded-child" }],
          has_more: true,
        },
      },
    };
    const promise = fetchRelationReadback({ NOTION_TOKEN: "test", NOTION_VERSION: "test" } as Env, page, "Canonical Children｜层级子级");
    await vi.runAllTimersAsync();
    await expect(promise).resolves.toEqual({ ids: ["child-1", "child-2"], complete: true });
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(String(fetchMock.mock.calls[1]?.[0])).toContain("start_cursor=cursor-1");
  });

  it("fails closed on a repeated relation cursor instead of looping", async () => {
    vi.useFakeTimers();
    vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(JSON.stringify({
        object: "list",
        results: [{ object: "property_item", relation: { id: "child-1" } }],
        has_more: true,
        next_cursor: "repeat",
      }), { status: 200, headers: { "Content-Type": "application/json" } }))
      .mockResolvedValueOnce(new Response(JSON.stringify({
        object: "list",
        results: [{ object: "property_item", relation: { id: "child-2" } }],
        has_more: true,
        next_cursor: "repeat",
      }), { status: 200, headers: { "Content-Type": "application/json" } }));
    const page: NotionPage = {
      object: "page",
      id: "page-1",
      properties: {
        children: { id: "children-prop", type: "relation", relation: [], has_more: true },
      },
    };
    const promise = fetchRelationReadback({ NOTION_TOKEN: "test", NOTION_VERSION: "test" } as Env, page, "children");
    await vi.runAllTimersAsync();
    await expect(promise).resolves.toEqual({ ids: ["child-1", "child-2"], complete: false });
  });

  it("fails closed when a relation claims more pages but omits next_cursor", async () => {
    vi.useFakeTimers();
    vi.spyOn(globalThis, "fetch").mockResolvedValueOnce(new Response(JSON.stringify({
      object: "list",
      results: [{ object: "property_item", relation: { id: "child-1" } }],
      has_more: true,
      next_cursor: null,
    }), { status: 200, headers: { "Content-Type": "application/json" } }));
    const page: NotionPage = {
      object: "page",
      id: "page-1",
      properties: {
        children: { id: "children-prop", type: "relation", relation: [{ id: "embedded-child" }], has_more: true },
      },
    };
    const promise = fetchRelationReadback({ NOTION_TOKEN: "test", NOTION_VERSION: "test" } as Env, page, "children");
    await vi.runAllTimersAsync();
    await expect(promise).resolves.toEqual({ ids: ["child-1"], complete: false });
  });

  it("preserves embedded relation IDs as partial fallback when the property API fails", async () => {
    vi.useFakeTimers();
    vi.spyOn(globalThis, "fetch").mockResolvedValueOnce(new Response("bad relation request", { status: 400 }));
    const page: NotionPage = {
      object: "page",
      id: "page-1",
      properties: {
        children: { id: "children-prop", type: "relation", relation: [{ id: "embedded-child" }], has_more: true },
      },
    };
    const promise = safeRelationReadback({ NOTION_TOKEN: "test", NOTION_VERSION: "test" } as Env, page, "children");
    await vi.runAllTimersAsync();
    await expect(promise).resolves.toEqual({ ids: ["embedded-child"], complete: false });
  });

  it("fails closed when relation pagination exceeds the hard page budget", async () => {
    vi.useFakeTimers();
    let call = 0;
    const fetchMock = vi.spyOn(globalThis, "fetch").mockImplementation(async () => {
      call += 1;
      return new Response(JSON.stringify({
        object: "list",
        results: [{ object: "property_item", relation: { id: `child-${call}` } }],
        has_more: true,
        next_cursor: `cursor-${call}`,
      }), { status: 200, headers: { "Content-Type": "application/json" } });
    });
    const page: NotionPage = {
      object: "page",
      id: "page-1",
      properties: { children: { id: "children-prop", type: "relation", relation: [], has_more: true } },
    };
    const promise = fetchRelationReadback({ NOTION_TOKEN: "test", NOTION_VERSION: "test" } as Env, page, "children");
    await vi.runAllTimersAsync();
    const result = await promise;
    expect(result.complete).toBe(false);
    expect(result.ids).toHaveLength(20);
    expect(fetchMock).toHaveBeenCalledTimes(20);
  });

  it("enforces the shared Notion readback deadline across retries", async () => {
    vi.useFakeTimers();
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response("retry", { status: 500 }));
    const page: NotionPage = {
      object: "page",
      id: "page-1",
      properties: { children: { id: "children-prop", type: "relation", relation: [], has_more: true } },
    };
    const promise = fetchRelationReadback(
      { NOTION_TOKEN: "test", NOTION_VERSION: "test" } as Env,
      page,
      "children",
      Date.now() + 1_000,
    );
    const rejection = expect(promise).rejects.toBeInstanceOf(NotionReadbackBudgetError);
    await vi.runAllTimersAsync();
    await rejection;
  });

  it("keeps the Notion deadline active while a response body is still being consumed", async () => {
    vi.useFakeTimers();
    vi.spyOn(globalThis, "fetch").mockImplementation(async (_input, init) => {
      const signal = init?.signal as AbortSignal | undefined;
      return {
        ok: true,
        json: () => new Promise((_, reject) => {
          if (!signal) return;
          signal.addEventListener("abort", () => reject(new DOMException("Aborted", "AbortError")), { once: true });
        }),
      } as Response;
    });
    const page: NotionPage = {
      object: "page",
      id: "page-1",
      properties: { children: { id: "children-prop", type: "relation", relation: [], has_more: true } },
    };
    const promise = fetchRelationReadback(
      { NOTION_TOKEN: "test", NOTION_VERSION: "test" } as Env,
      page,
      "children",
      Date.now() + 600,
    );
    const rejection = expect(promise).rejects.toBeInstanceOf(NotionReadbackBudgetError);
    await vi.runAllTimersAsync();
    await rejection;
  });

  it("queries the configured Domain registry with bounded cursor pagination", async () => {
    vi.useFakeTimers();
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(JSON.stringify({
        results: [{ object: "page", id: "domain-1", properties: {} }],
        has_more: true,
        next_cursor: "domain-cursor",
      }), { status: 200, headers: { "Content-Type": "application/json" } }))
      .mockResolvedValueOnce(new Response(JSON.stringify({
        results: [{ object: "page", id: "domain-2", properties: {} }],
        has_more: false,
        next_cursor: null,
      }), { status: 200, headers: { "Content-Type": "application/json" } }));
    const promise = queryDomainRegistryPages({
      NOTION_TOKEN: "test",
      NOTION_VERSION: "test",
      NOTION_DOMAINS_DATA_SOURCE_ID: "domains-current",
    } as Env);
    await vi.runAllTimersAsync();
    const result = await promise;
    expect(result.complete).toBe(true);
    expect(result.pages.map((page) => page.id)).toEqual(["domain-1", "domain-2"]);
    expect(String(fetchMock.mock.calls[0]?.[0])).toContain("/v1/data_sources/domains-current/query");
  });

  it("fails closed on a repeated Domain registry cursor", async () => {
    vi.useFakeTimers();
    vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(JSON.stringify({
        results: [{ object: "page", id: "domain-1", properties: {} }],
        has_more: true,
        next_cursor: "repeat",
      }), { status: 200, headers: { "Content-Type": "application/json" } }))
      .mockResolvedValueOnce(new Response(JSON.stringify({
        results: [{ object: "page", id: "domain-2", properties: {} }],
        has_more: true,
        next_cursor: "repeat",
      }), { status: 200, headers: { "Content-Type": "application/json" } }));
    const promise = queryDomainRegistryPages({
      NOTION_TOKEN: "test",
      NOTION_VERSION: "test",
      NOTION_DOMAINS_DATA_SOURCE_ID: "domains-current",
    } as Env);
    await vi.runAllTimersAsync();
    const result = await promise;
    expect(result.complete).toBe(false);
    expect(result.pages.map((page) => page.id)).toEqual(["domain-1", "domain-2"]);
  });

  it("fails closed when Domain registry pagination exceeds the hard page budget", async () => {
    vi.useFakeTimers();
    let call = 0;
    const fetchMock = vi.spyOn(globalThis, "fetch").mockImplementation(async () => {
      call += 1;
      return new Response(JSON.stringify({
        results: [{ object: "page", id: `domain-${call}`, properties: {} }],
        has_more: true,
        next_cursor: `domain-cursor-${call}`,
      }), { status: 200, headers: { "Content-Type": "application/json" } });
    });
    const promise = queryDomainRegistryPages({
      NOTION_TOKEN: "test",
      NOTION_VERSION: "test",
      NOTION_DOMAINS_DATA_SOURCE_ID: "domains-current",
    } as Env);
    await vi.runAllTimersAsync();
    const result = await promise;
    expect(result.complete).toBe(false);
    expect(result.pages).toHaveLength(20);
    expect(fetchMock).toHaveBeenCalledTimes(20);
  });

  it("queries the configured Project registry with bounded cursor pagination", async () => {
    vi.useFakeTimers();
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(JSON.stringify({
        results: [{ object: "page", id: "project-1", properties: {} }],
        has_more: true,
        next_cursor: "project-cursor",
      }), { status: 200, headers: { "Content-Type": "application/json" } }))
      .mockResolvedValueOnce(new Response(JSON.stringify({
        results: [{ object: "page", id: "project-2", properties: {} }],
        has_more: false,
        next_cursor: null,
      }), { status: 200, headers: { "Content-Type": "application/json" } }));
    const promise = queryProjectRegistryPages({
      NOTION_TOKEN: "test",
      NOTION_VERSION: "test",
      NOTION_PROJECTS_DATA_SOURCE_ID: "projects-current",
    } as Env);
    await vi.runAllTimersAsync();
    const result = await promise;
    expect(result.complete).toBe(true);
    expect(result.pages.map((page) => page.id)).toEqual(["project-1", "project-2"]);
    expect(String(fetchMock.mock.calls[0]?.[0])).toContain("/v1/data_sources/projects-current/query");
  });

  it("hydrates semantic Related plus main/related Project identity without using them as owner inputs", async () => {
    vi.useFakeTimers();
    const notePage: NotionPage = {
      object: "page",
      id: "note-1",
      parent: { type: "data_source_id", data_source_id: "notes-current" },
      last_edited_time: "2026-09-13T00:00:00.000Z",
      properties: {
        Name: { type: "title", title: [{ plain_text: "Knowledge object" }] },
        "Canonical ID": { type: "rich_text", rich_text: [{ plain_text: "KN-TEST-001" }] },
        "知识角色": { type: "select", select: { name: "THEORY" } },
        "方法家族": { type: "multi_select", multi_select: [] },
        "主领域": { type: "relation", relation: [] },
        "关联领域": { type: "relation", relation: [] },
        "Canonical Parent｜层级上位": { type: "relation", relation: [] },
        "Canonical Children｜层级子级": { type: "relation", relation: [] },
        "相关笔记": { type: "relation", relation: [{ id: "related-note-1" }] },
        "来源文档": { type: "relation", relation: [{ id: "source-note-1" }] },
        "引用方法": { type: "relation", relation: [{ id: "method-note-1" }] },
        "替代文档": { type: "relation", relation: [{ id: "replacement-note-1" }] },
        "被替代文档": { type: "relation", relation: [{ id: "replaced-note-1" }] },
        "主项目": { type: "relation", relation: [{ id: "project-main" }] },
        "关联项目": { type: "relation", relation: [{ id: "project-related" }] },
      },
    };
    const project = (id: string, projectId: string, level: string): NotionPage => ({
      object: "page",
      id,
      parent: { type: "data_source_id", data_source_id: "projects-current" },
      last_edited_time: "2026-09-12T00:00:00.000Z",
      properties: {
        Name: { type: "title", title: [{ plain_text: projectId }] },
        "Project ID｜项目ID": { type: "rich_text", rich_text: [{ plain_text: projectId }] },
        "项目层级": { type: "select", select: { name: level } },
        "治理状态": { type: "select", select: { name: "ACTIVE" } },
        "关系状态": { type: "select", select: { name: "VALID" } },
        "项目路径": { type: "rich_text", rich_text: [{ plain_text: `Portfolio/${projectId}` }] },
      },
    });
    vi.spyOn(globalThis, "fetch").mockImplementation(async (input) => {
      const url = String(input);
      if (url.includes("/v1/pages/note-1")) {
        return new Response(JSON.stringify(notePage), { status: 200, headers: { "Content-Type": "application/json" } });
      }
      if (url.includes("/v1/data_sources/domains-current/query")) {
        return new Response(JSON.stringify({ results: [], has_more: false, next_cursor: null }), { status: 200, headers: { "Content-Type": "application/json" } });
      }
      if (url.includes("/v1/data_sources/projects-current/query")) {
        return new Response(JSON.stringify({
          results: [
            project("project-main", "C04", "P2｜Project"),
            project("project-related", "C04-WS-01", "P3｜Workstream"),
          ],
          has_more: false,
          next_cursor: null,
        }), { status: 200, headers: { "Content-Type": "application/json" } });
      }
      throw new Error(`unexpected Notion URL: ${url}`);
    });
    const noteRows = [
      ["related-note-1", "KN-RELATED-001", "Related note", "THEORY"],
      ["source-note-1", "SRC-TEST-001", "Source note", "SOURCE"],
      ["method-note-1", "MTH-TEST-001", "Method note", "METHOD"],
      ["replacement-note-1", "KN-REPLACEMENT-001", "Replacement note", "THEORY"],
      ["replaced-note-1", "KN-REPLACED-001", "Replaced note", "THEORY"],
    ].map(([page_id, canonical_id, title, knowledge_role]) => ({
      page_id,
      canonical_id,
      title,
      effective_space: "CURRENT",
      governance_state: "ACTIVE",
      relation_state: "VALID",
      content_level: "L5｜Knowledge Object",
      knowledge_role,
      in_trash: 0,
    }));
    const manifest = {
      prepare: () => ({
        bind: (...pageIds: string[]) => ({
          all: async () => ({
            results: noteRows.filter((row) => typeof row.page_id === "string" && pageIds.includes(row.page_id)),
          }),
        }),
      }),
    } as unknown as D1Database;
    const detail: KnowledgeReaderDetail = {
      version: "oleander-knowledge-reader-detail/v1",
      generatedAt: "2026-09-13T00:00:00.000Z",
      id: "note-1",
      title: "Knowledge object",
      canonicalId: "KN-TEST-001",
      notionLastEditedTime: "2026-09-13T00:00:00.000Z",
      primaryDomainIds: [],
      relatedDomainIds: [],
      review: {
        contentComplete: true,
        markdownTruncated: false,
        chunkCount: 0,
        tokenEstimate: 0,
        unknownBlockIds: [],
        relationReadback: {
          declared: { primaryDomain: 0, relatedDomain: 0, source: 0, method: 0, replacement: 0, replacedDocument: 0 },
          indexedOutgoing: { source: 0, method: 0, replacement: 0, replacedDocument: 0 },
          unresolvedTargets: [],
          missingManifestEdges: [],
        },
      },
      sections: [],
      relations: [],
    };
    const promise = hydrateKnowledgeReaderFramework({
      MANIFEST: manifest,
      NOTION_TOKEN: "test",
      NOTION_VERSION: "test",
      NOTION_NOTES_DATA_SOURCE_ID: "notes-current",
      NOTION_DOMAINS_DATA_SOURCE_ID: "domains-current",
      NOTION_PROJECTS_DATA_SOURCE_ID: "projects-current",
    } as Env, detail, Date.now() + 8_000);
    await vi.runAllTimersAsync();
    const result = await promise;
    expect(result.source.state).toBe("HYDRATED");
    expect(result.dedicatedRelations.semanticRelated.items).toMatchObject([
      { registry: "notes", pageId: "related-note-1", canonicalId: "KN-RELATED-001" },
    ]);
    expect(result.dedicatedRelations.lineage.source).toMatchObject({
      declaredIds: ["source-note-1"],
      relationComplete: true,
      unresolvedPageIds: [],
      items: [{ registry: "notes", pageId: "source-note-1", canonicalId: "SRC-TEST-001" }],
    });
    expect(result.dedicatedRelations.lineage.method).toMatchObject({
      declaredIds: ["method-note-1"],
      relationComplete: true,
      unresolvedPageIds: [],
      items: [{ registry: "notes", pageId: "method-note-1", canonicalId: "MTH-TEST-001" }],
    });
    expect(result.dedicatedRelations.lineage.replacement).toMatchObject({
      declaredIds: ["replacement-note-1"],
      relationComplete: true,
      unresolvedPageIds: [],
      items: [{ registry: "notes", pageId: "replacement-note-1", canonicalId: "KN-REPLACEMENT-001" }],
    });
    expect(result.dedicatedRelations.lineage.replacedDocument).toMatchObject({
      declaredIds: ["replaced-note-1"],
      relationComplete: true,
      unresolvedPageIds: [],
      items: [{ registry: "notes", pageId: "replaced-note-1", canonicalId: "KN-REPLACED-001" }],
    });
    expect(result.dedicatedRelations.projects.primary).toMatchObject([
      { registry: "projects", pageId: "project-main", projectId: "C04", projectLevel: "P2｜Project" },
    ]);
    expect(result.dedicatedRelations.projects.related).toMatchObject([
      { registry: "projects", pageId: "project-related", projectId: "C04-WS-01", projectLevel: "P3｜Workstream" },
    ]);
    expect(result.executionOwner.state).toBe("NOT_HYDRATED");
    if (result.executionOwner.state !== "NOT_HYDRATED") throw new Error("expected unhydrated execution owner");
    expect(result.executionOwner.blockingInputs).toContain("authoritative_execution_owner_resolver_runtime_readback");
  });

  it("keeps primary Domain routing unresolved when the root revision drifts", () => {
    const ref: KnowledgeReaderFrameworkObjectRef = {
      registry: "domains",
      metadataSource: "NOTION_LIVE",
      pageId: "domain-1",
      governanceState: "ACTIVE",
      domainLevel: "L2｜Architecture",
      inTrash: false,
    };
    expect(primaryDomainRoutingReadiness(true, true, ["domain-1"], [ref], true)).toEqual({ ready: true, issues: [] });
    expect(primaryDomainRoutingReadiness(true, true, ["domain-1"], [ref], false)).toEqual({
      ready: false,
      issues: ["framework_revision_incoherent"],
    });
  });
});
