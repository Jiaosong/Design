import { describe, expect, it } from "vitest";
import { activeL2DomainRows, domainRegistrySurfaceRows } from "../src/domain-registry";
import type { NotionPage } from "../src/types";

function textProperty(type: "title" | "rich_text", text: string) {
  return { type, [type]: [{ plain_text: text }] };
}

function selectProperty(name: string) {
  return { type: "select", select: { name } };
}

function page(id: string, title: string, level: string, frameworkPath: string, governanceState: string, inTrash = false): NotionPage {
  return {
    object: "page",
    id,
    in_trash: inTrash,
    last_edited_time: "2026-09-14T00:00:00.000Z",
    properties: {
      Name: textProperty("title", title),
      "层级深度": textProperty("rich_text", level),
      "框架路径": textProperty("rich_text", frameworkPath),
      "治理状态": selectProperty(governanceState),
    },
  } as unknown as NotionPage;
}

describe("domain registry readback surface", () => {
  it("returns scrubbed registry metadata and filters only active non-trash L2 domains", () => {
    const rows = domainRegistrySurfaceRows([
      page("l2-active", "Human Factors", "L2｜Domain", "Design / Human Factors", "ACTIVE"),
      page("l2-review", "CMF", "L2｜Domain", "Design / CMF", "REVIEW"),
      page("l1-active", "Design", "L1｜Branch", "Design", "ACTIVE"),
      page("l2-trash", "Old Domain", "L2｜Domain", "Design / Old", "ACTIVE", true),
    ]);

    expect(rows).toHaveLength(4);
    expect(rows[0]).toEqual({
      pageId: "l2-active",
      title: "Human Factors",
      level: "L2｜Domain",
      frameworkPath: "Design / Human Factors",
      governanceState: "ACTIVE",
      inTrash: false,
      lastEditedTime: "2026-09-14T00:00:00.000Z",
    });
    expect(activeL2DomainRows(rows).map((row) => row.pageId)).toEqual(["l2-active"]);
  });
});
