import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const caseRoot = path.dirname(root);

const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const stable = (value) => JSON.stringify(value, Object.keys(value).sort());

function schemaErrors(value, schema, schemaRoot = schema, at = '$') {
  const errors = [];
  const visit = (item, rule, location) => {
    if (!rule) return;
    if (rule.$ref) {
      const prefix = '#/$defs/';
      if (!rule.$ref.startsWith(prefix)) {
        errors.push(`${location}: unsupported schema ref ${rule.$ref}`);
        return;
      }
      visit(item, schemaRoot.$defs?.[rule.$ref.slice(prefix.length)], location);
      return;
    }
    if (Object.hasOwn(rule, 'const') && item !== rule.const) {
      errors.push(`${location}: expected ${JSON.stringify(rule.const)}, got ${JSON.stringify(item)}`);
    }
    if (rule.enum && !rule.enum.includes(item)) errors.push(`${location}: invalid enum ${JSON.stringify(item)}`);
    if (rule.type === 'object') {
      if (typeof item !== 'object' || item === null || Array.isArray(item)) {
        errors.push(`${location}: expected object`);
        return;
      }
      for (const key of rule.required ?? []) if (!(key in item)) errors.push(`${location}.${key}: required`);
      for (const [key, child] of Object.entries(rule.properties ?? {})) if (key in item) visit(item[key], child, `${location}.${key}`);
    }
    if (rule.type === 'array') {
      if (!Array.isArray(item)) {
        errors.push(`${location}: expected array`);
        return;
      }
      if (rule.minItems !== undefined && item.length < rule.minItems) errors.push(`${location}: minItems ${rule.minItems}`);
      if (rule.maxItems !== undefined && item.length > rule.maxItems) errors.push(`${location}: maxItems ${rule.maxItems}`);
      item.forEach((child, index) => visit(child, rule.items, `${location}[${index}]`));
    }
    if (rule.type === 'string') {
      if (typeof item !== 'string') errors.push(`${location}: expected string`);
      else {
        if (rule.minLength !== undefined && item.length < rule.minLength) errors.push(`${location}: minLength ${rule.minLength}`);
        if (rule.pattern && !new RegExp(rule.pattern).test(item)) errors.push(`${location}: pattern ${rule.pattern}`);
      }
    }
    if (rule.type === 'boolean' && typeof item !== 'boolean') errors.push(`${location}: expected boolean`);
    if (rule.type === 'integer' && !Number.isInteger(item)) errors.push(`${location}: expected integer`);
    if (rule.type === 'number' && typeof item !== 'number') errors.push(`${location}: expected number`);
    if (typeof item === 'number' && rule.minimum !== undefined && item < rule.minimum) errors.push(`${location}: minimum ${rule.minimum}`);
  };
  visit(value, schema, at);
  return errors;
}

export function loadInputs() {
  return {
    runtime: readJson(path.join(root, 'runtime-state.json')),
    runtimeSchema: readJson(path.join(root, 'runtime-state.schema.json')),
    promotion: readJson(path.join(root, 'promotion-blockers.json')),
    promotionSchema: readJson(path.join(root, 'promotion-blockers.schema.json')),
    fieldRegister: readJson(path.join(root, 'field-package-register.json')),
    fieldSchema: readJson(path.join(root, 'field-package.schema.json')),
    fState: readJson(path.join(caseRoot, 'f-integration', 'runtime-state.json'))
  };
}

export function validateAll(inputs) {
  const { runtime, runtimeSchema, promotion, promotionSchema, fieldRegister, fieldSchema, fState } = inputs;
  const checks = [];
  const errors = [];
  const check = (id, pass, detail) => {
    checks.push({ id, pass, detail });
    if (!pass) errors.push(`${id}: ${detail}`);
  };

  const runtimeSchemaErrors = schemaErrors(runtime, runtimeSchema);
  const promotionSchemaErrors = schemaErrors(promotion, promotionSchema);
  check('RUNTIME_SCHEMA', runtimeSchemaErrors.length === 0, runtimeSchemaErrors.join('; ') || 'runtime schema enforced');
  check('PROMOTION_SCHEMA', promotionSchemaErrors.length === 0, promotionSchemaErrors.join('; ') || 'promotion schema enforced');
  check(
    'FIELD_PACKAGE_SCHEMA_CONTRACT',
    fieldSchema.$id === 'c04-field-package/1.0' && ['location', 'direction', 'photos', 'videos', 'dimensions', 'sightline', 'slope', 'safety', 'signage', 'operations', 'weather', 'equipment'].every((key) => fieldSchema.required.includes(key)),
    'field package requires the confirmed collection contract'
  );

  check(
    'AUTHORITY_CHAIN',
    runtime.authority_chain.master_protocol.id === 'OLEANDER_GOVERNANCE_V1_1_1' &&
      runtime.authority_chain.project_state.id === 'PRJ-C04-QINGJIANG-SHISHU_EXPLORE_G3_HOLD' &&
      runtime.authority_chain.source_authority.latest_revision === '672cd61bbac02dd6686c297567a16a5afd81a8fa' &&
      runtime.authority_chain.current_task.scope === 'MACHINE_READABLE_CONTROL_AND_EXECUTABLE_VALIDATION_ONLY' &&
      runtime.authority_chain.current_task.new_methodology === false,
    'MASTER PROTOCOL -> PROJECT STATE -> SOURCE AUTHORITY -> CURRENT TASK must remain explicit and pinned'
  );

  const lanesById = new Map();
  for (const lane of runtime.lanes) {
    if (!lanesById.has(lane.lane)) lanesById.set(lane.lane, []);
    lanesById.get(lane.lane).push(lane);
    check(`FRONTIER_${lane.lane}_CURRENT`, lane.authority_state === 'CURRENT', `${lane.lane} must expose exactly one CURRENT frontier`);
    if (lane.material_delta) {
      check(`DELTA_${lane.lane}_BOUND`, lane.delta_types.length > 0 && lane.output_action !== 'NO_MATERIAL_DELTA', `${lane.lane} material delta requires typed output`);
    } else {
      check(`NO_DELTA_${lane.lane}`, lane.delta_types.length === 0 && lane.output_action === 'NO_MATERIAL_DELTA', `${lane.lane} cannot create a version without material delta`);
    }
  }
  check(
    'SINGLE_FRONTIER_ALL_LANES',
    ['A', 'B', 'C', 'D', 'E', 'F'].every((lane) => lanesById.get(lane)?.length === 1) && lanesById.size === 6,
    'A-F must each have one and only one current frontier'
  );

  const agingThreshold = runtime.blocker_aging_policy.external_wait_after_no_delta_runs;
  for (const blocker of runtime.blockers) {
    check(`BLOCKER_FIELDS_${blocker.id}`, Boolean(blocker.owner && blocker.next_legal_action) && Number.isFinite(Date.parse(blocker.opened_at)) && Number.isFinite(Date.parse(blocker.last_evidence_delta)), `${blocker.id} aging fields must be complete`);
    if (blocker.status === 'OPEN' && blocker.no_delta_runs >= agingThreshold) {
      check(`BLOCKER_AGING_${blocker.id}`, blocker.aging_state === 'WAIT_EXTERNAL_EVIDENCE', `${blocker.id} must stop repeated research and wait for external evidence`);
    }
  }

  const requiredCapture = ['location', 'direction', 'photos', 'videos', 'dimensions', 'sightline', 'slope', 'safety', 'signage', 'operations', 'weather', 'equipment'];
  const registeredCapture = fieldRegister.capture_requirements.map((item) => item.field);
  check('FIELD_REGISTER_ZERO', fieldRegister.status === 'NOT_RUN' && fieldRegister.gate === 'HOLD' && fieldRegister.field_observed === 0 && fieldRegister.field_measured === 0 && fieldRegister.evidence_items.length === 0, 'unrun field package must remain zero/HOLD');
  check('FIELD_REGISTER_COMPLETE', stable([...registeredCapture].sort()) === stable([...requiredCapture].sort()) && fieldRegister.capture_requirements.every((item) => item.status === 'REQUIRED_NOT_COLLECTED'), 'register must contain every required field without fabricated evidence');
  check('FIELD_READBACK_GATE', fieldRegister.readback.status === 'NOT_READY' && stable(fieldRegister.readback.targets) === stable(['A', 'C', 'D', 'E', 'F']) && fieldRegister.readback.promotion_effect === 'NONE_UNTIL_VALIDATED', 'field package readback must be batch-bound and non-promotional');

  const contracts = Object.fromEntries(runtime.cross_line_contracts.map((contract) => [contract.id, contract]));
  check('CONTRACT_B_A', contracts.B_CLAIM_TYPE_TO_A_EVIDENCE_STATE?.producer_state === 'FIELD_NONE_G1F_HOLD' && contracts.B_CLAIM_TYPE_TO_A_EVIDENCE_STATE?.consumer_state === 'EVIDENCE_BOUND_OWNER_RECEIPT_FIELD_OPEN', 'B owner receipt must remain evidence-bound to A state');
  check('CONTRACT_C_D', contracts.C_ROUTE_STATE_TO_D_READING_MODE?.producer_state === 'C19_STATE_AXES_WITH_C17_M0_M7_ROUTE' && contracts.C_ROUTE_STATE_TO_D_READING_MODE?.consumer_state === 'OWNER_CONTRACT_CLOSED_ARCHITECTURE_FIELD_OPEN', 'D owner contract must follow C19/C17 without route sovereignty or field promotion');
  check('CONTRACT_C_E', contracts.C_REALITY_STATE_TO_E_DIGITAL_STATE?.producer_state === 'C19_REALITY_STATE_FIELD_NONE' && contracts.C_REALITY_STATE_TO_E_DIGITAL_STATE?.consumer_state === 'OWNER_CONTRACT_CLOSED_ARCHITECTURE_FIELD_OPEN', 'E owner contract must preserve route/safety/return without field promotion');
  check('CONTRACT_A_F', contracts.A_HOLD_TO_F_FINAL_WORDING?.producer_state === 'G1F_HOLD' && contracts.A_HOLD_TO_F_FINAL_WORDING?.consumer_state === 'NO_PROMOTION', 'A HOLD must force F no-promotion wording');

  const runtimeOpen = runtime.blockers.filter((item) => item.status === 'OPEN').map((item) => item.id).sort();
  const manifestOpen = promotion.blockers.filter((item) => item.status === 'OPEN').map((item) => item.id).sort();
  const fOpen = [...fState.final_wording_blockers].sort();
  const forbidden = ['FINAL', 'FIELD VALIDATED', 'IMPLEMENTABLE', 'SYSTEM PROMOTED'];
  check('PROMOTION_MANIFEST_SYNC', stable(runtimeOpen) === stable(manifestOpen) && stable(manifestOpen) === stable(fOpen), 'runtime, manifest and F wording blockers must match');
  check('PROMOTION_FREEZE', manifestOpen.length > 0 && promotion.freeze_active === true && promotion.decision === 'NO_PROMOTION' && runtime.promotion_freeze.decision === 'NO_PROMOTION', 'any open blocker must freeze promotion');
  check('PROMOTION_WORDING', forbidden.every((word) => promotion.blocked_transitions.includes(word) && runtime.promotion_freeze.forbidden_wording.includes(word)), 'all forbidden promotion wording must be blocked');
  check('OWNER_RECEIPTS_CLOSED_NOT_BLOCKING', ['B_R1_OWNER_LANE_RECEIPT', 'D_R1_R2_R3_OWNER_CONTRACTS', 'E_R1_R2_OWNER_CONTRACTS'].every((id) => promotion.closed_not_blocking.some((item) => item.id === id)) && !manifestOpen.some((id) => /^B_|^D_|^E_/.test(id)), 'current B/D/E owner receipts close architecture blockers only');
  check('F_MAIN_READBACK_CLOSED', promotion.closed_not_blocking.some((item) => item.id === 'F_MAIN_READBACK' && item.source_revision === '6c92097b0de16fd0cf02dd602000e68535672b11') && !manifestOpen.includes('F_MAIN_READBACK'), 'PR #97 verified main readback must be closed and removed from blockers');
  check('D_REMOTE_SEARCH_BOUNDARY', promotion.closed_not_blocking.some((item) => item.id === 'R06_R13_PUBLIC_INDEX_SEARCH_CURRENT_ITERATION' && item.source_revision === 'cdcf2e0d955ccb8b221fe4aba2c97e2035e10cab') && manifestOpen.includes('R06_EXACT_SCIENCE_HERO_AND_FIELD_GEOMETRY') && manifestOpen.includes('R13_IMAGE_ASSET_AND_FIELD_SAFETY'), 'remote search closure must not close exact media, field, expert or safety gates');

  check('VALIDATION_STOP_RULE', runtime.validation_stop_rule.active === true && ['NEW_DIGITAL_FEATURES', 'NEW_PAPER_EXPANSION', 'NARRATIVE_EXPANSION', 'SYSTEM_LEVEL_PROMOTION'].every((item) => runtime.validation_stop_rule.forbidden_progress.includes(item)), 'Validation Stop Rule remains active');
  check('FIELD_TRUTH_CEILING', runtime.evidence_state.field_observed === 0 && runtime.evidence_state.field_measured === 0 && runtime.evidence_state.field_pass === 'NONE' && runtime.evidence_state.G1F === 'HOLD' && runtime.evidence_state.remote_evidence_may_substitute_field === false, 'FIELD OBSERVED/MEASURED must remain 0 and G1F HOLD');
  check('F_FIELD_TRUTH_CEILING', fState.evidence_state.field_observed === 0 && fState.evidence_state.field_measured === 0 && fState.evidence_state.field_pass === 'NONE' && fState.evidence_state.G1F === 'IMPLEMENTATION_HOLD' && fState.decision.promote_P2 === false, 'F overlay must retain the same field truth ceiling');

  return { status: errors.length ? 'FAIL' : 'PASS', checks, errors };
}

function runCli() {
  const inputs = loadInputs();
  const result = validateAll(inputs);
  const receipt = {
    validator: 'C04-CROSS-LINE-ORCHESTRATION',
    schema_version: inputs.runtime.schema_version,
    run_at: new Date().toISOString(),
    input_sha256: crypto.createHash('sha256').update(JSON.stringify({ runtime: inputs.runtime, promotion: inputs.promotion, fieldRegister: inputs.fieldRegister, fState: inputs.fState })).digest('hex'),
    decision: inputs.promotion.decision,
    field_observed: inputs.runtime.evidence_state.field_observed,
    field_measured: inputs.runtime.evidence_state.field_measured,
    G1F: inputs.runtime.evidence_state.G1F,
    ...result
  };
  fs.writeFileSync(path.join(root, 'orchestration-result.json'), `${JSON.stringify(receipt, null, 2)}\n`);
  const summary = [
    '# C04 Six-lane Orchestration Controls',
    '',
    `- Status: **${receipt.status}**`,
    `- Decision: **${receipt.decision}**`,
    `- Field observed / measured: **${receipt.field_observed} / ${receipt.field_measured}**`,
    `- G1F: **${receipt.G1F}**`,
    '',
    '## Checks',
    ...receipt.checks.map((item) => `- ${item.pass ? 'PASS' : 'FAIL'} — ${item.id}: ${item.detail}`),
    ...(receipt.errors.length ? ['', '## Errors', ...receipt.errors.map((item) => `- ${item}`)] : [])
  ].join('\n');
  console.log(summary);
  if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, `${summary}\n`);
  if (receipt.errors.length) process.exitCode = 1;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) runCli();
