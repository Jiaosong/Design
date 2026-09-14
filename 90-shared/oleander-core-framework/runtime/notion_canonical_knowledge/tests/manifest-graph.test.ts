import { describe, expect, it } from "vitest";
import { saveDocumentAndChunks } from "../src/manifest";
import type { AuthorityDecision, NormalizedPage } from "../src/types";

class FakeStatement {
  readonly sql: string;
  readonly bindings: unknown[];
  constructor(sql: string, bindings: unknown[] = []) {
    this.sql = sql;
    this.bindings = bindings;
  }
  bind(...values: unknown[]): FakeStatement {
    return new FakeStatement(this.sql, values);
  }
}

class FakeDb {
  batchStatements: FakeStatement[] = [];
  prepare(sql: string): FakeStatement {
    return new FakeStatement(sql);
  }
  async batch(statements: FakeStatement[]): Promise<unknown[]> {
    for (const statement of statements) {
      const placeholders = (statement.sql.match(/\?/g) ?? []).length;
      expect(statement.bindings.length, `bind count for ${statement.sql.slice(0, 60)}`).toBe(placeholders);
    }
    this.batchStatements = statements;
    return [];
  }
}

function page(): NormalizedPage {
  return {
    pageId: "note-1",
    canonicalId: "KN-TEST-001",
    title: "Graph test",
    url: "https://example.invalid/note-1",
    lastEditedTime: "2026-09-14T00:00:00.000Z",
    inTrash: false,
    parentDataSourceId: "notes",
    retrievalSpace: "SUPPORT",
    searchEligibility: "DEFAULT",
    trustState: "VERIFIED",
    governanceState: "ACTIVE",
    relationState: "VALID",
    contentLevel: "L4｜Integrating Framework / Cluster",
    knowledgeRole: "INDEX",
    frameworkType: "NAVIGATION_MAP",
    canonicalParentIds: [],
    canonicalChildrenIds: ["child-1"],
    semanticRelatedIds: ["related-1"],
    methodFamilies: [],
    primaryDomainIds: ["domain-1"],
    relatedDomainIds: ["domain-2"],
    primaryProjectIds: ["project-1"],
    relatedProjectIds: ["project-2"],
    sourceRelationIds: ["source-1"],
    methodRelationIds: ["method-1"],
    replacementIds: ["replacement-1"],
    replacedDocumentIds: ["replaced-1"],
  };
}

describe("full graph derivative manifest", () => {
  it("persists the revised taxonomy and every typed outgoing relation with matched SQL bindings", async () => {
    const db = new FakeDb();
    const authority: AuthorityDecision = { index: true, effectiveSpace: "SUPPORT", reason: "TEST", conflict: false };
    await saveDocumentAndChunks(db as unknown as D1Database, {
      page: page(),
      authority,
      contentHash: "content",
      structureHash: "structure",
      indexRevision: "knowledge-index-v1",
      truncated: false,
      unknownBlockIds: [],
      chunks: [],
    });
    const insert = db.batchStatements.find((statement) => statement.sql.includes("INSERT INTO documents"));
    expect(insert?.bindings).toContain("NAVIGATION_MAP");
    const edgeStatements = db.batchStatements.filter((statement) => statement.sql.includes("INSERT OR REPLACE INTO lineage_edges"));
    const relationTypes = edgeStatements.map((statement) => String(statement.bindings[1])).sort();
    expect(relationTypes).toEqual([
      "CANONICAL_CHILD",
      "METHOD",
      "PRIMARY_DOMAIN",
      "PRIMARY_PROJECT",
      "RELATED",
      "RELATED_DOMAIN",
      "RELATED_PROJECT",
      "REPLACED_DOCUMENT",
      "REPLACEMENT",
      "SOURCE",
    ].sort());
  });
});
