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
const [mode, planInput, receiptInput] = process.argv.slice(2);
if (!mode || !["preflight", "apply"].includes(mode) || !planInput) {
  throw new Error("usage: preflight|apply <plan.json> [receipt.json]");
}
const planPath = path.resolve(planInput);
const plan = JSON.parse(fs.readFileSync(planPath, "utf8"));
if (!Array.isArray(plan.nodes)) throw new Error("plan.nodes missing");
const receiptPath = receiptInput ? path.resolve(receiptInput) : null;
const headers = { Authorization: `Bearer ${token}`, "Content-Type": "application/json" };
const governanceBase = "https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/governance-page";
const mutationBase = "https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/knowledge-graph-mutation";
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const results = [];

function plannedUpdates(node, live) {
  const updates = {};
  if (node.target.level && live.contentLevel !== node.target.level) updates.content_level = node.target.level;
  if (node.target.role && live.knowledgeRole !== node.target.role) updates.knowledge_role = node.target.role;
  if (String(node.target.level ?? live.contentLevel ?? "").startsWith("L4")) {
    if (!node.target.frameworkType) throw new Error(`${node.canonicalId}: L4 target missing frameworkType`);
    if (live.frameworkType !== node.target.frameworkType) updates.framework_type = node.target.frameworkType;
  } else if (live.frameworkType) {
    updates.framework_type = null;
  }
  return updates;
}

for (const node of plan.nodes) {
  const startedAt = new Date().toISOString();
  let inspect;
  try {
    const response = await fetch(`${governanceBase}?page_id=${encodeURIComponent(node.pageId)}`, { headers });
    inspect = await response.json();
    if (!response.ok || !inspect.ok) throw new Error(`inspect HTTP ${response.status}: ${JSON.stringify(inspect)}`);
    const live = inspect.page;
    const drift = [];
    if (live.canonicalId !== node.canonicalId) drift.push(`canonicalId:${live.canonicalId}`);
    if (live.retrievalSpace !== node.retrievalSpace) drift.push(`retrievalSpace:${live.retrievalSpace}`);
    if (live.contentLevel !== node.current.level) drift.push(`contentLevel:${live.contentLevel}`);
    if (live.knowledgeRole !== node.current.role) drift.push(`knowledgeRole:${live.knowledgeRole}`);
    if (live.relationState !== node.current.relationState) drift.push(`relationState:${live.relationState}`);
    const updates = plannedUpdates(node, live);
    if (drift.length) {
      results.push({ sequence: node.sequence, pageId: node.pageId, canonicalId: node.canonicalId, status: "DRIFT", drift, live, updates, startedAt, completedAt: new Date().toISOString() });
      continue;
    }
    if (!Object.keys(updates).length) {
      results.push({ sequence: node.sequence, pageId: node.pageId, canonicalId: node.canonicalId, status: "ALREADY_TARGET", live, updates, startedAt, completedAt: new Date().toISOString() });
      continue;
    }
    if (mode === "preflight") {
      results.push({ sequence: node.sequence, pageId: node.pageId, canonicalId: node.canonicalId, status: "READY", live, updates, startedAt, completedAt: new Date().toISOString() });
      continue;
    }
    const expected = {
      canonical_id: node.canonicalId,
      notion_last_edited_time: live.lastEditedTime,
      relation_state: live.relationState,
    };
    const fieldMap = {
      content_level: "contentLevel",
      knowledge_role: "knowledgeRole",
      framework_type: "frameworkType",
    };
    for (const key of Object.keys(updates)) expected[key] = live[fieldMap[key]];
    const body = {
      page_id: node.pageId,
      reason: `Apply HIGH-confidence OLEANDER graph decision ${node.migrationAction} for ${node.canonicalId}. ${node.reason}`.slice(0, 1900),
      expected,
      updates,
    };
    const mutationResponse = await fetch(mutationBase, { method: "POST", headers, body: JSON.stringify(body) });
    const text = await mutationResponse.text();
    let payload;
    try { payload = JSON.parse(text); } catch { payload = { raw: text }; }
    const status = mutationResponse.ok && payload?.ok ? "APPLIED" : "FAILED";
    results.push({ sequence: node.sequence, pageId: node.pageId, canonicalId: node.canonicalId, status, httpStatus: mutationResponse.status, updates, response: payload, startedAt, completedAt: new Date().toISOString() });
    if (status === "FAILED") break;
    await sleep(750);
  } catch (error) {
    results.push({ sequence: node.sequence, pageId: node.pageId, canonicalId: node.canonicalId, status: "ERROR", error: error instanceof Error ? error.message : String(error), startedAt, completedAt: new Date().toISOString() });
    break;
  }
}
const summary = Object.fromEntries([...new Set(results.map((r) => r.status))].map((status) => [status, results.filter((r) => r.status === status).length]));
const receipt = {
  version: "oleander-knowledge-graph-migration-receipt/v1",
  mode,
  generatedAt: new Date().toISOString(),
  plan: planPath,
  plannedCount: plan.nodes.length,
  processedCount: results.length,
  summary,
  results,
};
if (receiptPath) fs.writeFileSync(receiptPath, JSON.stringify(receipt, null, 2) + "\n");
console.log(JSON.stringify({ plannedCount: receipt.plannedCount, processedCount: receipt.processedCount, summary, receiptPath }, null, 2));
if (results.some((r) => ["DRIFT", "FAILED", "ERROR"].includes(r.status))) process.exit(2);

