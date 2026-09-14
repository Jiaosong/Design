import { describe, expect, it } from "vitest";
import { buildGovernancePropertyPatch, buildGraphPropertyPatch, inspectFrameworkTypeSchema, validateLevelRoleCompatibility } from "../src/notion";
import type { NotionPage } from "../src/types";

function page(): NotionPage {
  return {
    object: "page",
    id: "p1",
    properties: {
      "Canonical ID": { type: "rich_text", rich_text: [{ plain_text: "OLD" }] },
      "Retrieval Space｜检索空间": { type: "select", select: { name: "PROVENANCE" } },
      "Search Eligibility｜检索资格": { type: "select", select: { name: "HISTORY_ONLY" } },
      "治理状态": { type: "select", select: { name: "REVIEW" } },
      "关系状态": { type: "select", select: { name: "REVIEW" } },
      "内容层级": { type: "select", select: { name: "L4｜Framework" } },
      "知识角色": { type: "select", select: { name: "INDEX" } },
      "Framework Type｜框架类型": { type: "select", select: null },
      "主领域": { type: "relation", relation: [{ id: "domain-old" }] },
      "关联领域": { type: "relation", relation: [] },
      "Canonical Parent｜层级上位": { type: "relation", relation: [] },
      "Canonical Children｜层级子级": { type: "relation", relation: [{ id: "child-old" }] },
      "相关笔记": { type: "relation", relation: [] },
      "主项目": { type: "relation", relation: [] },
      "关联项目": { type: "relation", relation: [] },
      "来源文档": { type: "relation", relation: [] },
      "引用方法": { type: "relation", relation: [] },
      "替代文档": { type: "relation", relation: [] },
      "被替代文档": { type: "relation", relation: [] },
    },
  };
}

describe("governance property patch", () => {
  it("builds bounded rich-text/select updates", () => {
    expect(
      buildGovernancePropertyPatch(page(), {
        canonical_id: "LEGACY-OLD",
        retrieval_space: "PROVENANCE",
        search_eligibility: "HISTORY_ONLY",
        governance_state: "HOLD",
        relation_state: "REVIEW",
      }),
    ).toEqual({
      "Canonical ID": { rich_text: [{ type: "text", text: { content: "LEGACY-OLD" } }] },
      "Retrieval Space｜检索空间": { select: { name: "PROVENANCE" } },
      "Search Eligibility｜检索资格": { select: { name: "HISTORY_ONLY" } },
      "治理状态": { select: { name: "HOLD" } },
      "关系状态": { select: { name: "REVIEW" } },
    });
  });

  it("rejects retrieval/search values outside the runtime contract", () => {
    expect(() => buildGovernancePropertyPatch(page(), { retrieval_space: "MAYBE" })).toThrow(/Invalid retrieval_space/);
    expect(() => buildGovernancePropertyPatch(page(), { search_eligibility: "PUBLIC" })).toThrow(/Invalid search_eligibility/);
    expect(() => buildGovernancePropertyPatch(page(), { governance_state: "DONE" })).toThrow(/Invalid governance_state/);
    expect(() => buildGovernancePropertyPatch(page(), { relation_state: "BROKEN" })).toThrow(/Invalid relation_state/);
  });

  it("can clear an allowlisted property without touching other fields", () => {
    expect(buildGovernancePropertyPatch(page(), { canonical_id: null })).toEqual({ "Canonical ID": { rich_text: [] } });
  });

  it("builds one bounded graph mutation and forces REVIEW during the write", () => {
    expect(buildGraphPropertyPatch(page(), {
      content_level: "L5｜Knowledge Object",
      knowledge_role: "METHOD",
      primary_domain_ids: ["domain-l2"],
      canonical_parent_ids: ["framework-l4"],
      canonical_children_ids: [],
      method_relation_ids: ["method-1"],
    })).toEqual({
      "关系状态": { select: { name: "REVIEW" } },
      "内容层级": { select: { name: "L5｜Knowledge Object" } },
      "知识角色": { select: { name: "METHOD" } },
      "主领域": { relation: [{ id: "domain-l2" }] },
      "Canonical Parent｜层级上位": { relation: [{ id: "framework-l4" }] },
      "Canonical Children｜层级子级": { relation: [] },
      "引用方法": { relation: [{ id: "method-1" }] },
    });
  });

  it("rejects incompatible Level×Role combinations before Notion mutation", () => {
    expect(validateLevelRoleCompatibility("L4｜Framework", "SOURCE")).toBe(false);
    expect(validateLevelRoleCompatibility("L5｜Knowledge Object", "METHOD")).toBe(true);
    expect(() => buildGraphPropertyPatch(page(), { content_level: "L5｜Knowledge Object", knowledge_role: "SOURCE" })).toThrow(/Incompatible Level×Role/);
  });

  it("enforces single primary-domain and primary-project cardinality", () => {
    expect(() => buildGraphPropertyPatch(page(), { primary_domain_ids: ["d1", "d2"] })).toThrow(/at most one/);
    expect(() => buildGraphPropertyPatch(page(), { primary_project_ids: ["p1", "p2"] })).toThrow(/at most one/);
  });

  it("keeps Framework Type independent from Role and rejects it outside L4", () => {
    expect(buildGraphPropertyPatch(page(), { framework_type: "PROFESSIONAL_SYSTEM_MAP" })["Framework Type｜框架类型"])
      .toEqual({ select: { name: "PROFESSIONAL_SYSTEM_MAP" } });
    expect(() => buildGraphPropertyPatch(page(), {
      content_level: "L5｜Knowledge Object",
      knowledge_role: "INDEX",
      framework_type: "NAVIGATION_MAP",
    })).toThrow(/requires projected L4/);
  });

  it("detects Framework Type schema readiness without inventing options", () => {
    expect(inspectFrameworkTypeSchema({ object: "data_source", id: "notes", properties: {} })).toMatchObject({ state: "MISSING" });
    const result = inspectFrameworkTypeSchema({
      object: "data_source",
      id: "notes",
      properties: {
        "Framework Type｜框架类型": {
          id: "fwtype",
          type: "select",
          select: { options: [{ id: "one", name: "NAVIGATION_MAP", color: "default" }] },
        },
      },
    });
    expect(result.state).toBe("OPTIONS_INCOMPLETE");
    expect(result.option_names).toEqual(["NAVIGATION_MAP"]);
    expect(result.missing_options).toContain("CONCEPTUAL_MODEL");
  });
});
