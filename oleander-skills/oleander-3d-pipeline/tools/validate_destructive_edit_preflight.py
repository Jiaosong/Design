#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path


def fail(code: str):
    raise SystemExit(code)


def validate(receipt: dict, contract: dict) -> bool:
    if receipt.get('schema') != contract.get('receipt_schema'):
        fail('FAIL_DESTRUCTIVE_PREFLIGHT_SCHEMA')
    for key in contract.get('required', []):
        if key not in receipt:
            fail('FAIL_DESTRUCTIVE_PREFLIGHT_MISSING_' + key.upper())

    if receipt.get('host_state_class') not in contract.get('allowed_host_state_classes', []):
        fail('FAIL_DESTRUCTIVE_PREFLIGHT_HOST_STATE')
    result = receipt.get('preflight_result')
    if result not in contract.get('allowed_results', []):
        fail('FAIL_DESTRUCTIVE_PREFLIGHT_RESULT')

    required = list(receipt.get('required_owner_ids') or [])
    coverage = receipt.get('owner_coverage') or {}
    allowed_states = set(contract.get('allowed_owner_states', []))
    for owner in required:
        if owner not in coverage:
            fail('FAIL_REQUIRED_OWNER_COVERAGE_MISSING:' + owner)
        state = coverage[owner].get('state') if isinstance(coverage[owner], dict) else coverage[owner]
        if state not in allowed_states:
            fail('FAIL_OWNER_COVERAGE_STATE:' + owner)

    conflicts = receipt.get('multi_owner_conflicts')
    if not isinstance(conflicts, dict):
        fail('FAIL_MULTI_OWNER_CONFLICTS_TYPE')
    unresolved_conflicts = int(conflicts.get('unresolved_count', 0) or 0)
    resolution = conflicts.get('resolution_method')
    if resolution == 'FIRST_MATCH_CODE_ORDER':
        fail('FAIL_FIRST_MATCH_CODE_ORDER_AS_OWNERSHIP')

    try:
        straddles = int(receipt.get('boundary_straddle_count', 0) or 0)
    except Exception:
        fail('FAIL_BOUNDARY_STRADDLE_COUNT_TYPE')
    if straddles < 0:
        fail('FAIL_BOUNDARY_STRADDLE_COUNT_NEGATIVE')

    checks = receipt.get('predicted_preservation_checks')
    if not isinstance(checks, list) or not checks:
        fail('FAIL_PREDICTED_PRESERVATION_CHECKS_MISSING')
    hard_fail = [c for c in checks if c.get('hard') is True and c.get('status') != 'PASS']

    pass_result = result == 'PASS_DESTRUCTIVE_EDIT_ALLOWED'
    if pass_result:
        if receipt.get('destructive_edit_allowed') is not True:
            fail('FAIL_PASS_BUT_EDIT_NOT_ALLOWED')
        for owner in required:
            state = coverage[owner].get('state') if isinstance(coverage[owner], dict) else coverage[owner]
            if state not in ('COVERED_EXCLUSIVE','COVERED_SHARED_BOUNDARY_EXPLICIT'):
                fail('FAIL_PASS_WITH_UNCOVERED_OWNER:' + owner)
        if unresolved_conflicts:
            fail('FAIL_PASS_WITH_UNRESOLVED_MULTI_OWNER_CONFLICT')
        if straddles:
            fail('FAIL_PASS_WITH_UNSPLIT_BOUNDARY_STRADDLE')
        if hard_fail:
            fail('FAIL_PASS_WITH_PREDICTED_HOST_LOSS')
    else:
        if receipt.get('destructive_edit_allowed') is True:
            fail('FAIL_BLOCKED_PREFLIGHT_ALLOWS_EDIT')

    if result == 'FAIL_DESTRUCTIVE_EDIT_BLOCKED_BOUNDARY_STRADDLE' and straddles <= 0:
        fail('FAIL_BOUNDARY_STRADDLE_BLOCK_WITH_ZERO_STRADDLES')

    if receipt.get('source_mutation_allowed') is False and receipt.get('source_mutation_planned') is True:
        fail('FAIL_UNAUTHORIZED_SOURCE_MUTATION_PLANNED')

    deps = receipt.get('classifier_dependencies')
    if not isinstance(deps, list) or not deps:
        fail('FAIL_CLASSIFIER_DEPENDENCIES_MISSING')
    if any(str(x).startswith('HISTORICAL_NESTED_NAMESPACE:') for x in deps):
        fail('FAIL_HISTORICAL_NESTED_NAMESPACE_DEPENDENCY')

    if not isinstance(receipt.get('does_not_prove'), list) or not receipt.get('does_not_prove'):
        fail('FAIL_DOES_NOT_PROVE_MISSING')
    return True


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) not in (1,2):
        raise SystemExit('usage: validate_destructive_edit_preflight.py RECEIPT.json [CONTRACT.json]')
    receipt=json.loads(Path(argv[0]).read_text(encoding='utf-8'))
    contract_path=Path(argv[1]) if len(argv)==2 else Path(__file__).resolve().parents[1]/'contracts'/'DESTRUCTIVE_EDIT_PREFLIGHT_CONTRACT_v1.json'
    contract=json.loads(contract_path.read_text(encoding='utf-8'))
    validate(receipt,contract)
    print('PASS_DESTRUCTIVE_EDIT_PREFLIGHT')


if __name__=='__main__':
    main()
