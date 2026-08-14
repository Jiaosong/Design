import assert from 'node:assert/strict';
import test from 'node:test';
import { loadInputs, validateAll } from './validate-cross-line-contracts.mjs';

const baseline = loadInputs();
const clone = () => structuredClone(baseline);
const fails = (inputs, id) => validateAll(inputs).errors.some((error) => error.startsWith(`${id}:`));

test('current C04 orchestration state passes every control', () => {
  const result = validateAll(clone());
  assert.equal(result.status, 'PASS', result.errors.join('\n'));
});

test('No-Delta Rule rejects version-producing output without material delta', () => {
  const inputs = clone();
  inputs.runtime.lanes.find((lane) => lane.lane === 'A').output_action = 'CREATE_VERSION';
  assert.equal(fails(inputs, 'NO_DELTA_A'), true);
});

test('Single Frontier Rule rejects duplicate current lane', () => {
  const inputs = clone();
  inputs.runtime.lanes[5].lane = 'A';
  assert.equal(fails(inputs, 'SINGLE_FRONTIER_ALL_LANES'), true);
});

test('Blocker Aging rejects repeated research after external wait threshold', () => {
  const inputs = clone();
  inputs.runtime.blockers.find((item) => item.id === 'A_G1F').aging_state = 'CONTINUE_RESEARCH';
  assert.equal(fails(inputs, 'BLOCKER_AGING_A_G1F'), true);
});

test('Field Package Gate rejects fabricated observed or measured counts', () => {
  const inputs = clone();
  inputs.fieldRegister.field_observed = 1;
  assert.equal(fails(inputs, 'FIELD_REGISTER_ZERO'), true);
});

test('Cross-line contract rejects C reality to E digital mismatch', () => {
  const inputs = clone();
  inputs.runtime.cross_line_contracts.find((item) => item.id === 'C_REALITY_STATE_TO_E_DIGITAL_STATE').consumer_state = 'ONLINE_ONLY';
  assert.equal(fails(inputs, 'CONTRACT_C_E'), true);
});

test('Promotion Freeze rejects blocker drift between runtime, manifest and F', () => {
  const inputs = clone();
  inputs.promotion.blockers = inputs.promotion.blockers.filter((item) => item.id !== 'A_G1F');
  assert.equal(fails(inputs, 'PROMOTION_MANIFEST_SYNC'), true);
});

test('Validation ceiling rejects false field promotion', () => {
  const inputs = clone();
  inputs.runtime.evidence_state.G1F = 'PASS';
  assert.equal(fails(inputs, 'FIELD_TRUTH_CEILING'), true);
});
