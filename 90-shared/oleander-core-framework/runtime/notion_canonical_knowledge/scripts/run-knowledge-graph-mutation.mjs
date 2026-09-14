import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const vars = Object.fromEntries(
  fs.readFileSync(path.join(root, ".dev.vars"), "utf8")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("#") && line.includes("="))
    .map((line) => {
      const i = line.indexOf("=");
      let value = line.slice(i + 1).trim();
      if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) value = value.slice(1, -1);
      return [line.slice(0, i), value];
    }),
);
const token = vars.OLEANDER_API_TOKEN;
if (!token) throw new Error("OLEANDER_API_TOKEN missing");
const [pageId, canonicalId, ...args] = process.argv.slice(2);
if (!pageId || !canonicalId || args.length === 0) {
  throw new Error("usage: <page_id> <canonical_id> key=value ...");
}
const aliases = {
  level: "content_level",
  role: "knowledge_role",
  frameworkType: "framework_type",
  parent: "canonical_parent_ids",
  children: "canonical_children_ids",
  related: "semantic_related_ids",
  primaryProject: "primary_project_ids",
  relatedProjects: "related_project_ids",
};
const relationKeys = new Set(["canonical_parent_ids", "canonical_children_ids", "semantic_related_ids", "primary_project_ids", "related_project_ids"]);
const updates = {};
for (const arg of args) {
  const i = arg.indexOf("=");
  if (i <= 0) throw new Error(`invalid update arg: ${arg}`);
  const rawKey = arg.slice(0, i);
  const key = aliases[rawKey] ?? rawKey;
  const rawValue = arg.slice(i + 1);
  updates[key] = relationKeys.has(key)
    ? (rawValue ? rawValue.split(",").map((v) => v.trim()).filter(Boolean) : [])
    : rawValue === "null" ? null : rawValue;
}
const headers = { Authorization: `Bearer ${token}`, "Content-Type": "application/json" };
const inspectUrl = `https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/governance-page?page_id=${encodeURIComponent(pageId)}`;
const inspectResponse = await fetch(inspectUrl, { headers });
const inspect = await inspectResponse.json();
if (!inspectResponse.ok || !inspect.ok) throw new Error(`inspect failed: HTTP ${inspectResponse.status} ${JSON.stringify(inspect)}`);
const before = inspect.page;
if (before.canonicalId !== canonicalId) throw new Error(`canonical mismatch: expected ${canonicalId}, got ${before.canonicalId}`);
const fieldMap = {
  content_level: "contentLevel",
  knowledge_role: "knowledgeRole",
  framework_type: "frameworkType",
  primary_domain_ids: "primaryDomainIds",
  related_domain_ids: "relatedDomainIds",
  canonical_parent_ids: "canonicalParentIds",
  canonical_children_ids: "canonicalChildrenIds",
  semantic_related_ids: "semanticRelatedIds",
  primary_project_ids: "primaryProjectIds",
  related_project_ids: "relatedProjectIds",
  source_relation_ids: "sourceRelationIds",
  method_relation_ids: "methodRelationIds",
  replacement_ids: "replacementIds",
  replaced_document_ids: "replacedDocumentIds",
};
const expected = {
  canonical_id: canonicalId,
  notion_last_edited_time: before.lastEditedTime,
  relation_state: before.relationState,
};
for (const key of Object.keys(updates)) expected[key] = before[fieldMap[key]];
const reason = `Apply approved OLEANDER knowledge-graph reclassification for ${canonicalId} with exact live before-state and post-write readback.`;
const response = await fetch("https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/knowledge-graph-mutation", {
  method: "POST",
  headers,
  body: JSON.stringify({ page_id: pageId, reason, expected, updates }),
});
const text = await response.text();
console.log(`HTTP ${response.status}`);
try { console.log(JSON.stringify(JSON.parse(text), null, 2)); } catch { console.log(text); }
if (!response.ok) process.exit(1);
