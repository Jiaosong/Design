import { describe, expect, it } from "vitest";
import { fetchRelationReadback } from "../src/notion";
import { normalizePage, propertyMultiSelectNames } from "../src/normalize";
import type { Env, NotionPage, NotionProperty } from "../src/types";

describe("framework readback normalization", () => {
  it("reads Method Family from the canonical multi-select without semantic inference", () => {
    const property: NotionProperty = {
      type: "multi_select",
      multi_select: [{ id: "a", name: "研究取证" }, { id: "b", name: "评估验证" }],
    };
    expect(propertyMultiSelectNames(property)).toEqual(["研究取证", "评估验证"]);
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
});
