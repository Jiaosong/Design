import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import process from 'node:process';

const root = path.dirname(new URL(import.meta.url).pathname);
const statePath = path.join(root, 'runtime-state.json');
const schemaPath = path.join(root, 'runtime-state.schema.json');
const outputPath = path.join(root, 'loop-result.json');

const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));

const errors = [];
const warnings = [];
const checks = [];

function addCheck(id, pass, detail) {
  checks.push({ id, pass, detail });
  if (!pass) errors.push(`${id}: ${detail}`);
}

function resolveRef(ref) {
  if (!ref.startsWith('#/$defs/')) throw new Error(`Unsupported $ref: ${ref}`);
  return schema.$defs[ref.slice('#/$defs/'.length)];
}

function validate(value, rule, pointer = '$') {
  if (!rule) return;
  if (rule.$ref) return validate(value, resolveRef(rule.$ref), pointer);
  if (rule.const !== undefined && value !== rule.const) errors.push(`${pointer}: expected const ${JSON.stringify(rule.const)}, got ${JSON.stringify(value)}`);
  if (rule.enum && !rule.enum.includes(value)) errors.push(`${pointer}: expected one of ${rule.enum.join(', ')}, got ${JSON.stringify(value)}`);
  if (rule.type === 'object') {
    if (typeof value !== 'object' || value === null || Array.isArray(value)) {
      errors.push(`${pointer}: expected object`);
      return;
    }
    for (const key of rule.required || []) {
      if (!(key in value)) errors.push(`${pointer}.${key}: required`);
    }
    for (const [key, child] of Object.entries(rule.properties || {})) {
      if (key in value) validate(value[key], child, `${pointer}.${key}`);
    }
  }
  if (rule.type === 'array') {
    if (!Array.isArray(value)) {
      errors.push(`${pointer}: expected array`);
      return;
    }
    if (rule.minItems !== undefined && value.length < rule.minItems) errors.push(`${pointer}: minItems ${rule.minItems}`);
    if (rule.maxItems !== undefined && value.length > rule.maxItems) errors.push(`${pointer}: maxItems ${rule.maxItems}`);
    if (rule.items) value.forEach((item, i) => validate(item, rule.items, `${pointer}[${i}]`));
  }
  if (rule.type === 'string') {
    if (typeof value !== 'string') errors.push(`${pointer}: expected string`);
    else if (rule.minLength !== undefined && value.length < rule.minLength) errors.push(`${pointer}: minLength ${rule.minLength}`);
  }
  if (rule.type === 'boolean' && typeof value !== 'boolean') errors.push(`${pointer}: expected boolean`);
  if (rule.type === 'integer') {
    if (!Number.isInteger(value)) errors.push(`${pointer}: expected integer`);
    if (rule.minimum !== undefined && value < rule.minimum) errors.push(`${pointer}: minimum ${rule.minimum}`);
  }
}

validate(state, schema);
addCheck('SCHEMA_ENFORCEMENT', errors.length === 0, errors.length ? 'runtime-state does not conform to runtime-state.schema.json' : 'schema file is loaded and enforced by runtime');

const receipts = Object.entries(state.lane_receipts || {});
const directDeltas = receipts.filter(([, r]) => r.direct_delta === true);

for (const [lane, r] of receipts) {
  const parsedObserved = Date.parse(r.observed_at);
  const parsedRevision = Date.parse(r.source_revision);
  addCheck(`RECEIPT_${lane}_TIME`, Number.isFinite(parsedObserved) && Number.isFinite(parsedRevision), 'observed_at/source_revision must be parseable timestamps');
  addCheck(`RECEIPT_${lane}_HASH`, /^[a-f0-9]{64}$/i.test(r.payload_hash), 'payload_hash must be SHA-256 hex');
  addCheck(`RECEIPT_${lane}_AUTHORITY_BOUND`, Boolean(r.object_id && r.source_id && r.authority_state), 'receipt must bind object_id + source_id + authority_state');
  if (r.receipt_type === 'REPLAY' && r.direct_delta) errors.push(`RECEIPT_${lane}: REPLAY cannot set direct_delta=true`);
  if (r.authority_state === 'LEGACY_READONLY' && r.direct_delta) errors.push(`RECEIPT_${lane}: LEGACY_READONLY cannot provide a live DIRECT delta`);
  if (r.receipt_type === 'NONE' && r.direct_delta) errors.push(`RECEIPT_${lane}: NONE cannot set direct_delta=true`);
  if (/NO_NEW|DO_NOT_REOPEN/.test(r.status) && r.direct_delta) errors.push(`RECEIPT_${lane}: semantic contradiction between status and direct_delta`);
}

const stateDelta = state.decision.direct_delta_present;
addCheck('DIRECT_DELTA_AGREEMENT', stateDelta === (directDeltas.length > 0), `decision.direct_delta_present=${stateDelta}; receipt deltas=${directDeltas.map(([lane]) => lane).join(',') || 'none'}`);

const g1fHold = state.evidence_state.G1F === 'IMPLEMENTATION_HOLD';
const noField = state.evidence_state.field_observed_count === 0 && state.evidence_state.field_measured_count === 0;
if (g1fHold && noField) {
  addCheck('CB04_EVIDENCE_SUBSTITUTION', state.decision.promote_P2 === false, 'G1F HOLD + no field evidence requires P2 promotion=false');
  addCheck('FIELD_REOPEN_GUARD', state.decision.reopen_C === false, 'G1F HOLD + no DIRECT delta cannot auto-reopen C');
}

const forbidden = new Set(state.forbidden_promotions || []);
addCheck('NO_AUTO_P2_PROMOTION', state.decision.promote_P2 === false && forbidden.has('P2_AUTHORITY_PROMOTION'), 'F loop never performs P2 authority promotion');
addCheck('NO_NEW_P3_NAMESPACE', state.overlay.creates_p3_namespace === false && state.overlay.authority_state === 'NOT_AUTHORITY', 'F remains a P2 temporary integration overlay');
addCheck('EXPLICIT_PROMOTION_TRANSITION', state.promotion_transition.machine_ceiling === 'READY_FOR_HUMAN_DECISION' && state.promotion_transition.human_decision_required === true, 'machine output ceiling must remain READY_FOR_HUMAN_DECISION');

if (directDeltas.length === 0) {
  addCheck('NO_DELTA_NO_REOPEN', state.decision.reopen_C === false, 'without DIRECT delta C stays closed');
  addCheck('NO_DELTA_RESULT', state.decision.result === 'CONTROLLED_INTEGRATION_CONTINUE_NO_PROMOTION', 'no-delta loop must remain controlled integration / no promotion');
} else {
  addCheck('DELTA_OWNER_REPLAY', state.decision.result === 'READY_FOR_OWNER_REPLAY', 'DIRECT delta routes to owner replay; F does not auto-promote');
  addCheck('DELTA_STILL_NO_AUTO_REOPEN', state.decision.reopen_C === false, 'owner replay/human decision is required before C can reopen');
}

const requiredCoreIds = new Set(['R01','R05','R02','R06','R07','R09','R12','R13']);
const presentCoreIds = new Set((state.core_pages || []).map(p => p.id));
addCheck('CORE_8_IDENTITY', requiredCoreIds.size === presentCoreIds.size && [...requiredCoreIds].every(id => presentCoreIds.has(id)), 'Core set must remain the retained 8 Core reading pages; this does not imply 8 physical stops');

const semanticHolds = (state.core_pages || []).filter(p => /OPEN|HOLD|PENDING/.test(`${p.reading_mode} ${p.media_state} ${p.f_state}`));
const result = {
  loop: 'C04-F-INTEGRATION',
  schema_version: state.schema_version,
  run_at: new Date().toISOString(),
  input_sha256: crypto.createHash('sha256').update(JSON.stringify(state)).digest('hex'),
  project_state: `${state.project.current_loop}/${state.project.design_state}/${state.project.current_gate}`,
  direct_delta_lanes: directDeltas.map(([lane]) => lane),
  semantic_holds: semanticHolds.map(p => ({ id: p.id, f_state: p.f_state, media_state: p.media_state })),
  decision: state.decision,
  machine_ceiling: state.promotion_transition.machine_ceiling,
  checks,
  warnings,
  errors,
  status: errors.length ? 'FAIL' : 'PASS'
};

fs.writeFileSync(outputPath, JSON.stringify(result, null, 2) + '\n');

const summary = [
  '# C04 F Integration Loop',
  '',
  `- Status: **${result.status}**`,
  `- Project: ${result.project_state}`,
  `- DIRECT delta lanes: ${result.direct_delta_lanes.join(', ') || 'none'}`,
  `- Decision: ${result.decision.result}`,
  `- Machine ceiling: ${result.machine_ceiling}`,
  `- Semantic OPEN/HOLD pages: ${result.semantic_holds.map(x => x.id).join(', ') || 'none'}`,
  '',
  '## Checks',
  ...checks.map(c => `- ${c.pass ? 'PASS' : 'FAIL'} — ${c.id}: ${c.detail}`),
  ...(errors.length ? ['', '## Errors', ...errors.map(e => `- ${e}`)] : [])
].join('\n');

console.log(summary);
if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, summary + '\n');
if (errors.length) process.exit(1);
