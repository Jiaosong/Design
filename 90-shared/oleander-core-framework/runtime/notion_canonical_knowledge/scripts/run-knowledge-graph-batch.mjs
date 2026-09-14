import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const commonGitDir = execFileSync("git", ["rev-parse", "--path-format=absolute", "--git-common-dir"], { cwd: root, encoding: "utf8" }).trim();
const mainCheckoutRoot = path.dirname(commonGitDir);
const varsPath = [
  process.env.OLEANDER_DEV_VARS,
  path.join(root, ".dev.vars"),
  path.join(mainCheckoutRoot, "90-shared", "oleander-core-framework", "runtime", "notion_canonical_knowledge", ".dev.vars"),
].filter(Boolean).find((candidate) => fs.existsSync(candidate));
if (!varsPath && !process.env.OLEANDER_API_TOKEN) throw new Error("OLEANDER_API_TOKEN missing and no .dev.vars found");
const vars = Object.fromEntries(
  (varsPath ? fs.readFileSync(varsPath, "utf8") : "")
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
const token = process.env.OLEANDER_API_TOKEN || vars.OLEANDER_API_TOKEN;
if (!token) throw new Error("OLEANDER_API_TOKEN missing");
const [mode, planInput, receiptInput] = process.argv.slice(2);
if (!mode || !["preflight", "apply", "reconcile"].includes(mode) || !planInput) {
  throw new Error("usage: preflight|apply|reconcile <plan.json> [receipt.json]");
}
const planPath = path.resolve(planInput);
const plan = JSON.parse(fs.readFileSync(planPath, "utf8"));
if (!Array.isArray(plan.nodes)) throw new Error("plan.nodes missing");
const receiptPath = receiptInput ? path.resolve(receiptInput) : null;
const headers = { Authorization: `Bearer ${token}`, "Content-Type": "application/json" };
const governanceBase = "https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/governance-page";
const mutationBase = "https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/knowledge-graph-mutation";
const reconcileBase = "https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/reconcile";
const reconcileStatusBase = "https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/reconcile-status";
const drainOnceBase = "https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/v1/drain-once";
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const results = [];

function sameIds(a = [], b = []) {
  const normalize = (value) => [...new Set(value)].sort();
  return JSON.stringify(normalize(a)) === JSON.stringify(normalize(b));
}

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
  for (const repair of node.edgeRepairs ?? []) {
    if (repair.action === "SET_PRIMARY_DOMAIN") {
      const target = repair.targetPageId;
      if (!target) throw new Error(`${node.canonicalId}: SET_PRIMARY_DOMAIN requires targetPageId`);
      if (!sameIds(live.primaryDomainIds ?? [], [target])) updates.primary_domain_ids = [target];
      continue;
    }
    if (repair.action === "REPLACE_RELATED_DOMAIN") {
      const oldTarget = repair.oldTargetPageId;
      const newTarget = repair.newTargetPageId;
      if (!oldTarget || !newTarget) throw new Error(`${node.canonicalId}: REPLACE_RELATED_DOMAIN requires oldTargetPageId and newTargetPageId`);
      const relatedDomains = [...new Set(updates.related_domain_ids ?? live.relatedDomainIds ?? [])];
      const next = [...new Set(relatedDomains.map((id) => id === oldTarget ? newTarget : id))];
      if (!sameIds(relatedDomains, next)) updates.related_domain_ids = next;
      continue;
    }
    if (repair.action === "REMOVE_RELATED_DOMAIN") {
      const target = repair.targetPageId;
      if (!target) throw new Error(`${node.canonicalId}: REMOVE_RELATED_DOMAIN requires targetPageId`);
      const relatedDomains = [...new Set(updates.related_domain_ids ?? live.relatedDomainIds ?? [])];
      if (relatedDomains.includes(target)) updates.related_domain_ids = relatedDomains.filter((id) => id !== target);
      continue;
    }
    if (repair.action === "RETYPE_SOURCE_TO_RELATED") {
      const target = repair.targetPageId;
      if (!target) throw new Error(`${node.canonicalId}: RETYPE_SOURCE_TO_RELATED requires targetPageId`);
      const sources = [...new Set(updates.source_relation_ids ?? live.sourceRelationIds ?? [])];
      const related = [...new Set(updates.semantic_related_ids ?? live.semanticRelatedIds ?? [])];
      if (sources.includes(target)) updates.source_relation_ids = sources.filter((id) => id !== target);
      if (!related.includes(target)) updates.semantic_related_ids = [...related, target];
      continue;
    }
    if (repair.action === "REMOVE_CANONICAL_PARENT") {
      const target = repair.targetPageId;
      if (!target) throw new Error(`${node.canonicalId}: REMOVE_CANONICAL_PARENT requires targetPageId`);
      const parents = [...new Set(updates.canonical_parent_ids ?? live.canonicalParentIds ?? [])];
      if (parents.includes(target)) updates.canonical_parent_ids = parents.filter((id) => id !== target);
      continue;
    }
    if (repair.action === "REMOVE_CANONICAL_CHILDREN") {
      const targets = [...new Set(repair.targetPageIds ?? [])];
      if (!targets.length) throw new Error(`${node.canonicalId}: REMOVE_CANONICAL_CHILDREN requires targetPageIds`);
      const children = [...new Set(updates.canonical_children_ids ?? live.canonicalChildrenIds ?? [])];
      const remainingChildren = children.filter((id) => !targets.includes(id));
      if (remainingChildren.length !== children.length) updates.canonical_children_ids = remainingChildren;
      continue;
    }
    if (repair.action === "RETYPE_CANONICAL_PARENT_TO_RELATED") {
      const target = repair.targetPageId;
      const parents = [...new Set(updates.canonical_parent_ids ?? live.canonicalParentIds ?? [])];
      const related = [...new Set(updates.semantic_related_ids ?? live.semanticRelatedIds ?? [])];
      if (parents.includes(target)) updates.canonical_parent_ids = parents.filter((id) => id !== target);
      if (!related.includes(target)) updates.semantic_related_ids = [...related, target];
      continue;
    }
    if (repair.action === "RETYPE_CANONICAL_PARENT_TO_METHOD") {
      const target = repair.targetPageId;
      if (!target) throw new Error(`${node.canonicalId}: RETYPE_CANONICAL_PARENT_TO_METHOD requires targetPageId`);
      const parents = [...new Set(updates.canonical_parent_ids ?? live.canonicalParentIds ?? [])];
      const methods = [...new Set(updates.method_relation_ids ?? live.methodRelationIds ?? [])];
      if (parents.includes(target)) updates.canonical_parent_ids = parents.filter((id) => id !== target);
      if (!methods.includes(target)) updates.method_relation_ids = [...methods, target];
      continue;
    }
    if (["RETYPE_CANONICAL_CHILDREN_TO_RELATED", "RETYPE_CANONICAL_CHILDREN_TO_SOURCE"].includes(repair.action)) {
      const targets = [...new Set(repair.targetPageIds ?? [])];
      if (!targets.length) throw new Error(`${node.canonicalId}: ${repair.action} requires targetPageIds`);
      const children = [...new Set(updates.canonical_children_ids ?? live.canonicalChildrenIds ?? [])];
      const remainingChildren = children.filter((id) => !targets.includes(id));
      if (remainingChildren.length !== children.length) updates.canonical_children_ids = remainingChildren;
      if (repair.action === "RETYPE_CANONICAL_CHILDREN_TO_RELATED") {
        const related = [...new Set(updates.semantic_related_ids ?? live.semanticRelatedIds ?? [])];
        const next = [...new Set([...related, ...targets])];
        if (next.length !== related.length) updates.semantic_related_ids = next;
      } else {
        const sources = [...new Set(updates.source_relation_ids ?? live.sourceRelationIds ?? [])];
        const next = [...new Set([...sources, ...targets])];
        if (next.length !== sources.length) updates.source_relation_ids = next;
      }
      continue;
    }
    throw new Error(`${node.canonicalId}: unsupported edge repair ${repair.action}`);
  }
  return updates;
}

function classificationAtTarget(node, live) {
  if (node.target.level && live.contentLevel !== node.target.level) return false;
  if (node.target.role && live.knowledgeRole !== node.target.role) return false;
  const targetLevel = String(node.target.level ?? live.contentLevel ?? "");
  if (targetLevel.startsWith("L4")) return live.frameworkType === node.target.frameworkType;
  return !live.frameworkType;
}

function edgeRepairsAtTarget(node, live) {
  return (node.edgeRepairs ?? []).every((repair) => {
    if (repair.action === "SET_PRIMARY_DOMAIN") {
      return sameIds(live.primaryDomainIds ?? [], [repair.targetPageId]);
    }
    if (repair.action === "REPLACE_RELATED_DOMAIN") {
      const oldTarget = repair.oldTargetPageId;
      const newTarget = repair.newTargetPageId;
      return !(live.relatedDomainIds ?? []).includes(oldTarget) && (live.relatedDomainIds ?? []).includes(newTarget);
    }
    if (repair.action === "REMOVE_RELATED_DOMAIN") {
      return !(live.relatedDomainIds ?? []).includes(repair.targetPageId);
    }
    if (repair.action === "RETYPE_SOURCE_TO_RELATED") {
      const target = repair.targetPageId;
      return !(live.sourceRelationIds ?? []).includes(target) && (live.semanticRelatedIds ?? []).includes(target);
    }
    if (repair.action === "REMOVE_CANONICAL_PARENT") {
      return !(live.canonicalParentIds ?? []).includes(repair.targetPageId);
    }
    if (repair.action === "REMOVE_CANONICAL_CHILDREN") {
      return (repair.targetPageIds ?? []).every((target) => !(live.canonicalChildrenIds ?? []).includes(target));
    }
    if (repair.action === "RETYPE_CANONICAL_PARENT_TO_RELATED") {
      const target = repair.targetPageId;
      return !(live.canonicalParentIds ?? []).includes(target) && (live.semanticRelatedIds ?? []).includes(target);
    }
    if (repair.action === "RETYPE_CANONICAL_PARENT_TO_METHOD") {
      const target = repair.targetPageId;
      return !(live.canonicalParentIds ?? []).includes(target) && (live.methodRelationIds ?? []).includes(target);
    }
    if (repair.action === "RETYPE_CANONICAL_CHILDREN_TO_RELATED") {
      const targets = repair.targetPageIds ?? [];
      return targets.every((target) => !(live.canonicalChildrenIds ?? []).includes(target) && (live.semanticRelatedIds ?? []).includes(target));
    }
    if (repair.action === "RETYPE_CANONICAL_CHILDREN_TO_SOURCE") {
      const targets = repair.targetPageIds ?? [];
      return targets.every((target) => !(live.canonicalChildrenIds ?? []).includes(target) && (live.sourceRelationIds ?? []).includes(target));
    }
    return false;
  });
}

function edgeRepairDrift(node, live) {
  const drift = [];
  for (const repair of node.edgeRepairs ?? []) {
    if (repair.action === "SET_PRIMARY_DOMAIN") {
      const target = repair.targetPageId;
      if (!target) drift.push("SET_PRIMARY_DOMAIN:targetPageIdMissing");
      continue;
    }
    if (repair.action === "REPLACE_RELATED_DOMAIN") {
      const oldTarget = repair.oldTargetPageId;
      const newTarget = repair.newTargetPageId;
      if (!oldTarget || !newTarget) {
        drift.push("REPLACE_RELATED_DOMAIN:targetPageIdMissing");
        continue;
      }
      const related = live.relatedDomainIds ?? [];
      const hasOld = related.includes(oldTarget);
      const hasNew = related.includes(newTarget);
      if (!hasOld && !hasNew) drift.push(`edgeRepairSourceMissing:${oldTarget}`);
      continue;
    }
    if (repair.action === "REMOVE_RELATED_DOMAIN") {
      const target = repair.targetPageId;
      if (!target) {
        drift.push("REMOVE_RELATED_DOMAIN:targetPageIdMissing");
        continue;
      }
      if (!(live.relatedDomainIds ?? []).includes(target)) drift.push(`edgeRepairSourceMissing:${target}`);
      continue;
    }
    if (repair.action === "RETYPE_SOURCE_TO_RELATED") {
      const target = repair.targetPageId;
      if (!target) {
        drift.push("RETYPE_SOURCE_TO_RELATED:targetPageIdMissing");
        continue;
      }
      const hasSource = (live.sourceRelationIds ?? []).includes(target);
      const hasRelated = (live.semanticRelatedIds ?? []).includes(target);
      if (!hasSource && !hasRelated) drift.push(`edgeRepairSourceMissing:${target}`);
      continue;
    }
    if (repair.action === "REMOVE_CANONICAL_PARENT") {
      const target = repair.targetPageId;
      if (!target) {
        drift.push("REMOVE_CANONICAL_PARENT:targetPageIdMissing");
        continue;
      }
      const hasParent = (live.canonicalParentIds ?? []).includes(target);
      if (!hasParent) drift.push(`edgeRepairSourceMissing:${target}`);
      continue;
    }
    if (repair.action === "REMOVE_CANONICAL_CHILDREN") {
      const targets = repair.targetPageIds ?? [];
      if (!targets.length) {
        drift.push("REMOVE_CANONICAL_CHILDREN:targetPageIdsMissing");
        continue;
      }
      for (const target of targets) {
        if (!(live.canonicalChildrenIds ?? []).includes(target)) drift.push(`edgeRepairSourceMissing:${target}`);
      }
      continue;
    }
    if (repair.action === "RETYPE_CANONICAL_PARENT_TO_RELATED") {
      const target = repair.targetPageId;
      const hasParent = (live.canonicalParentIds ?? []).includes(target);
      const hasRelated = (live.semanticRelatedIds ?? []).includes(target);
      if (!hasParent && !hasRelated) drift.push(`edgeRepairSourceMissing:${target}`);
      continue;
    }
    if (repair.action === "RETYPE_CANONICAL_PARENT_TO_METHOD") {
      const target = repair.targetPageId;
      if (!target) {
        drift.push("RETYPE_CANONICAL_PARENT_TO_METHOD:targetPageIdMissing");
        continue;
      }
      const hasParent = (live.canonicalParentIds ?? []).includes(target);
      const hasMethod = (live.methodRelationIds ?? []).includes(target);
      if (!hasParent && !hasMethod) drift.push(`edgeRepairSourceMissing:${target}`);
      continue;
    }
    if (["RETYPE_CANONICAL_CHILDREN_TO_RELATED", "RETYPE_CANONICAL_CHILDREN_TO_SOURCE"].includes(repair.action)) {
      for (const target of repair.targetPageIds ?? []) {
        const hasChild = (live.canonicalChildrenIds ?? []).includes(target);
        const hasRetyped = repair.action === "RETYPE_CANONICAL_CHILDREN_TO_RELATED"
          ? (live.semanticRelatedIds ?? []).includes(target)
          : (live.sourceRelationIds ?? []).includes(target);
        if (!hasChild && !hasRetyped) drift.push(`edgeRepairSourceMissing:${target}`);
      }
      continue;
    }
    drift.push(`unsupportedEdgeRepair:${repair.action}`);
  }
  return drift;
}

function effectiveRetrievalSpace(live) {
  if (live.searchEligibility === "HISTORY_ONLY") return "PROVENANCE";
  if (["LEGACY", "ARCHIVED"].includes(live.governanceState)) return "PROVENANCE";
  if (["CURRENT", "SUPPORT", "PROVENANCE"].includes(live.retrievalSpace)) return live.retrievalSpace;
  return live.governanceState === "ACTIVE" ? "SUPPORT" : "PROVENANCE";
}

for (const node of plan.nodes) {
  const startedAt = new Date().toISOString();
  let inspect;
  try {
    const response = await fetch(`${governanceBase}?page_id=${encodeURIComponent(node.pageId)}`, { headers });
    inspect = await response.json();
    if (!response.ok || !inspect.ok) throw new Error(`inspect HTTP ${response.status}: ${JSON.stringify(inspect)}`);
    const live = inspect.page;
    if (mode === "reconcile") {
      const drift = [];
      if (live.canonicalId !== node.canonicalId) drift.push(`canonicalId:${live.canonicalId}`);
      if (node.expectedRelationState && live.relationState !== node.expectedRelationState) {
        drift.push(`relationState:${live.relationState}`);
      }
      if (drift.length) {
        results.push({ sequence: node.sequence, pageId: node.pageId, canonicalId: node.canonicalId, status: "DRIFT", drift, live, startedAt, completedAt: new Date().toISOString() });
        break;
      }

      const scheduleResponse = await fetch(reconcileBase, { method: "POST", headers, body: JSON.stringify({ page_id: node.pageId }) });
      const schedulePayload = await scheduleResponse.json();
      if (!scheduleResponse.ok || !schedulePayload?.ok || !schedulePayload?.run_id) {
        results.push({ sequence: node.sequence, pageId: node.pageId, canonicalId: node.canonicalId, status: "FAILED", httpStatus: scheduleResponse.status, response: schedulePayload, live, startedAt, completedAt: new Date().toISOString() });
        break;
      }

      let run = null;
      let drainCalls = 0;
      for (; drainCalls < 24; drainCalls += 1) {
        const drainResponse = await fetch(drainOnceBase, { method: "POST", headers, body: "{}" });
        const drainPayload = await drainResponse.json();
        if (!drainResponse.ok || !drainPayload?.ok) {
          throw new Error(`drain-once HTTP ${drainResponse.status}: ${JSON.stringify(drainPayload)}`);
        }
        const statusResponse = await fetch(`${reconcileStatusBase}?run_id=${encodeURIComponent(schedulePayload.run_id)}`, { headers });
        const statusPayload = await statusResponse.json();
        if (!statusResponse.ok || !statusPayload?.ok) {
          throw new Error(`reconcile-status HTTP ${statusResponse.status}: ${JSON.stringify(statusPayload)}`);
        }
        run = statusPayload.run;
        if (run?.status === "COMPLETE" && Number(run?.task_counts?.PROCESSED ?? 0) === 1) break;
        if (["FAILED", "PARTIAL_BLOCKED"].includes(run?.status)) break;
        await sleep(150);
      }
      const reconciled = run?.status === "COMPLETE" && Number(run?.task_counts?.PROCESSED ?? 0) === 1;
      results.push({
        sequence: node.sequence,
        pageId: node.pageId,
        canonicalId: node.canonicalId,
        status: reconciled ? "RECONCILED" : "FAILED",
        runId: schedulePayload.run_id,
        run,
        drainCalls: drainCalls + (reconciled ? 1 : 0),
        live,
        startedAt,
        completedAt: new Date().toISOString(),
      });
      if (!reconciled) break;
      await sleep(150);
      continue;
    }
    const updates = plannedUpdates(node, live);
    if (classificationAtTarget(node, live) && edgeRepairsAtTarget(node, live) && !Object.keys(updates).length) {
      results.push({ sequence: node.sequence, pageId: node.pageId, canonicalId: node.canonicalId, status: "ALREADY_TARGET", live, updates, startedAt, completedAt: new Date().toISOString() });
      continue;
    }
    const drift = [];
    if (live.canonicalId !== node.canonicalId) drift.push(`canonicalId:${live.canonicalId}`);
    const liveEffectiveSpace = effectiveRetrievalSpace(live);
    if (liveEffectiveSpace !== node.retrievalSpace) drift.push(`retrievalSpace:${live.retrievalSpace}->${liveEffectiveSpace}`);
    if (live.contentLevel !== node.current.level) drift.push(`contentLevel:${live.contentLevel}`);
    if (live.knowledgeRole !== node.current.role) drift.push(`knowledgeRole:${live.knowledgeRole}`);
    if (live.relationState !== node.current.relationState) drift.push(`relationState:${live.relationState}`);
    if (Array.isArray(node.current.primaryDomainIds) && !sameIds(live.primaryDomainIds ?? [], node.current.primaryDomainIds)) {
      drift.push(`primaryDomainIds:${JSON.stringify(live.primaryDomainIds ?? [])}`);
    }
    if (Array.isArray(node.current.relatedDomainIds) && !sameIds(live.relatedDomainIds ?? [], node.current.relatedDomainIds)) {
      drift.push(`relatedDomainIds:${JSON.stringify(live.relatedDomainIds ?? [])}`);
    }
    if (Array.isArray(node.current.sourceRelationIds) && !sameIds(live.sourceRelationIds ?? [], node.current.sourceRelationIds)) {
      drift.push(`sourceRelationIds:${JSON.stringify(live.sourceRelationIds ?? [])}`);
    }
    if (Array.isArray(node.current.semanticRelatedIds) && !sameIds(live.semanticRelatedIds ?? [], node.current.semanticRelatedIds)) {
      drift.push(`semanticRelatedIds:${JSON.stringify(live.semanticRelatedIds ?? [])}`);
    }
    drift.push(...edgeRepairDrift(node, live));
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
      primary_domain_ids: "primaryDomainIds",
      related_domain_ids: "relatedDomainIds",
      canonical_parent_ids: "canonicalParentIds",
      canonical_children_ids: "canonicalChildrenIds",
      semantic_related_ids: "semanticRelatedIds",
      source_relation_ids: "sourceRelationIds",
      method_relation_ids: "methodRelationIds",
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

