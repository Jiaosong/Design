#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path


def fail(code: str):
    raise SystemExit(code)


def _improved(before, after, direction, epsilon):
    if direction in ('LOWER_IS_BETTER','ZERO_REQUIRED'):
        return after <= before - epsilon
    if direction == 'HIGHER_IS_BETTER':
        return after >= before + epsilon
    return None


def validate(receipt: dict, contract: dict) -> bool:
    if receipt.get('schema') != contract.get('receipt_schema'):
        fail('FAIL_BOUNDED_ITERATION_SCHEMA')
    for key in contract.get('required', []):
        if key not in receipt:
            fail('FAIL_BOUNDED_ITERATION_MISSING_' + key.upper())

    direction=receipt.get('target_direction')
    if direction not in contract.get('allowed_target_directions',[]):
        fail('FAIL_BOUNDED_ITERATION_TARGET_DIRECTION')
    if receipt.get('result') not in contract.get('allowed_results',[]):
        fail('FAIL_BOUNDED_ITERATION_RESULT')

    stop_conditions=set(receipt.get('stop_conditions') or [])
    missing=set(contract.get('required_stop_conditions',[]))-stop_conditions
    if missing:
        fail('FAIL_BOUNDED_ITERATION_STOP_CONDITIONS:' + ','.join(sorted(missing)))

    try:max_iterations=int(receipt.get('max_iterations'))
    except Exception:fail('FAIL_BOUNDED_ITERATION_MAX_TYPE')
    if max_iterations<=0:fail('FAIL_BOUNDED_ITERATION_MAX_NONPOSITIVE')
    iterations=receipt.get('iterations')
    if not isinstance(iterations,list) or not iterations:
        fail('FAIL_BOUNDED_ITERATION_RECORDS_MISSING')
    if len(iterations)>max_iterations:
        fail('FAIL_BOUNDED_ITERATION_BUDGET_EXCEEDED')

    rule=receipt.get('material_improvement_rule') or {}
    try:epsilon=float(rule.get('epsilon',0.0))
    except Exception:fail('FAIL_BOUNDED_ITERATION_EPSILON_TYPE')
    if epsilon<0:fail('FAIL_BOUNDED_ITERATION_EPSILON_NEGATIVE')

    stop_reason=receipt.get('stop_reason')
    stopped=False
    for idx,it in enumerate(iterations):
        for key in ('before','after','protected_invariants'):
            if key not in it:fail(f'FAIL_BOUNDED_ITERATION_RECORD_{idx}_{key.upper()}')
        try:before=float(it['before']);after=float(it['after'])
        except Exception:fail(f'FAIL_BOUNDED_ITERATION_METRIC_TYPE_{idx}')
        protected=it.get('protected_invariants')
        if protected not in ('PASS','FAIL'):
            fail(f'FAIL_BOUNDED_ITERATION_INVARIANT_STATE_{idx}')
        if protected=='FAIL':
            if idx != len(iterations)-1:
                fail('FAIL_ITERATION_CONTINUED_AFTER_PROTECTED_REGRESSION')
            if stop_reason!='PROTECTED_INVARIANT_REGRESSION':
                fail('FAIL_PROTECTED_REGRESSION_STOP_REASON')
            stopped=True;continue

        if direction=='BOUNDED_RELATION':
            improved=bool(it.get('material_improvement'))
        else:
            improved=_improved(before,after,direction,epsilon)

        target_reached=bool(it.get('target_reached'))
        if target_reached:
            if idx != len(iterations)-1:
                fail('FAIL_ITERATION_CONTINUED_AFTER_TARGET_REACHED')
            if stop_reason!='TARGET_REACHED':
                fail('FAIL_TARGET_REACHED_STOP_REASON')
            stopped=True;continue

        if not improved:
            if idx != len(iterations)-1:
                fail('FAIL_ITERATION_CONTINUED_AFTER_STAGNATION')
            if stop_reason!='STAGNATION_NO_MATERIAL_IMPROVEMENT':
                fail('FAIL_STAGNATION_STOP_REASON')
            stopped=True;continue

    if stop_reason=='MAX_ITERATION_BUDGET_REACHED' and len(iterations)!=max_iterations:
        fail('FAIL_MAX_BUDGET_STOP_BEFORE_BUDGET')
    if stop_reason not in stop_conditions:
        fail('FAIL_STOP_REASON_NOT_DECLARED')

    expected={
      'TARGET_REACHED':'PASS_TARGET_REACHED',
      'STAGNATION_NO_MATERIAL_IMPROVEMENT':'HOLD_STAGNATION_RECLASSIFY',
      'PROTECTED_INVARIANT_REGRESSION':'FAIL_PROTECTED_INVARIANT_REGRESSION',
      'MAX_ITERATION_BUDGET_REACHED':'HOLD_MAX_ITERATION_BUDGET_REACHED'
    }.get(stop_reason)
    if expected and receipt.get('result')!=expected:
        fail('FAIL_RESULT_STOP_REASON_MISMATCH')

    if not isinstance(receipt.get('locked_variables'),list) or not receipt['locked_variables']:
        fail('FAIL_LOCKED_VARIABLES_MISSING')
    if not isinstance(receipt.get('protected_invariants'),list) or not receipt['protected_invariants']:
        fail('FAIL_PROTECTED_INVARIANTS_MISSING')
    if not isinstance(receipt.get('does_not_prove'),list) or not receipt['does_not_prove']:
        fail('FAIL_DOES_NOT_PROVE_MISSING')
    return True


def main(argv=None):
    argv=argv or sys.argv[1:]
    if len(argv) not in (1,2):raise SystemExit('usage: validate_bounded_causal_iteration.py RECEIPT.json [CONTRACT.json]')
    receipt=json.loads(Path(argv[0]).read_text(encoding='utf-8'))
    cp=Path(argv[1]) if len(argv)==2 else Path(__file__).resolve().parents[1]/'contracts'/'BOUNDED_CAUSAL_ITERATION_CONTRACT_v1.json'
    contract=json.loads(cp.read_text(encoding='utf-8'))
    validate(receipt,contract);print('PASS_BOUNDED_CAUSAL_ITERATION')

if __name__=='__main__':main()
