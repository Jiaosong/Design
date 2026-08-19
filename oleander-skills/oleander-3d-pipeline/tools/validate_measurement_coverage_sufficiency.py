#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path


def fail(code: str):
    raise SystemExit(code)


def _set(x):
    return set(x or [])


def validate(receipt: dict, contract: dict) -> bool:
    if receipt.get('schema') != contract.get('receipt_schema'):
        fail('FAIL_MEASUREMENT_COVERAGE_SCHEMA')
    for key in contract.get('required', []):
        if key not in receipt:
            fail('FAIL_MEASUREMENT_COVERAGE_MISSING_' + key.upper())

    relation = receipt.get('coverage_relation')
    result = receipt.get('result')
    if relation not in contract.get('allowed_coverage_relations', []):
        fail('FAIL_MEASUREMENT_COVERAGE_RELATION_INVALID')
    if result not in contract.get('allowed_results', []):
        fail('FAIL_MEASUREMENT_COVERAGE_RESULT_INVALID')

    req_dim = _set(receipt.get('required_dimensions'))
    got_dim = _set(receipt.get('measured_dimensions'))
    req_feat = _set(receipt.get('required_feature_families'))
    got_feat = _set(receipt.get('measured_feature_families'))
    req_hold = _set(receipt.get('held_out_views_required'))
    got_hold = _set(receipt.get('held_out_views_reviewed'))
    critical = receipt.get('unmeasured_critical_items') or []

    missing_dim = sorted(req_dim - got_dim)
    missing_feat = sorted(req_feat - got_feat)
    missing_hold = sorted(req_hold - got_hold)

    claim_pass = result == 'PASS_COVERAGE_FOR_DECLARED_CLAIM'
    screen_pass = result == 'PASS_COVERAGE_FOR_DECLARED_SCREEN'

    if claim_pass:
        if relation != 'SUFFICIENT_FOR_DECLARED_CLAIM':
            fail('FAIL_CLAIM_PASS_WITH_NONSUFFICIENT_RELATION')
        if missing_dim:
            fail('FAIL_CLAIM_PASS_MISSING_DIMENSIONS:' + ','.join(missing_dim))
        if missing_feat:
            fail('FAIL_CLAIM_PASS_MISSING_FEATURES:' + ','.join(missing_feat))
        if missing_hold:
            fail('FAIL_CLAIM_PASS_MISSING_HELD_OUT_VIEWS:' + ','.join(missing_hold))
        if critical:
            fail('FAIL_CLAIM_PASS_WITH_UNMEASURED_CRITICAL_ITEMS')

    if screen_pass and relation != 'SUFFICIENT_FOR_DECLARED_SCREEN':
        fail('FAIL_SCREEN_PASS_WITH_NONSCREEN_RELATION')

    if relation == 'PARTIAL_DIAGNOSTIC_ONLY' and (claim_pass or screen_pass):
        fail('FAIL_PARTIAL_DIAGNOSTIC_PROMOTED_TO_PASS')

    if relation.startswith('INSUFFICIENT_') and result != 'FAIL_COVERAGE_INSUFFICIENT':
        fail('FAIL_INSUFFICIENT_RELATION_NOT_FAILED')
    if relation == 'UNRESOLVED' and result not in ('HOLD_PARTIAL_COVERAGE','FAIL_COVERAGE_INSUFFICIENT'):
        fail('FAIL_UNRESOLVED_COVERAGE_PROMOTED')

    metrics = receipt.get('metric_results')
    if not isinstance(metrics, list) or not metrics:
        fail('FAIL_METRIC_RESULTS_MISSING')
    failed_critical = [m for m in metrics if m.get('critical') is True and m.get('status') in ('FAIL','REJECT','REGRESSED')]
    if failed_critical and claim_pass:
        fail('FAIL_CLAIM_PASS_WITH_FAILED_CRITICAL_METRIC')

    if not isinstance(receipt.get('does_not_prove'), list) or not receipt.get('does_not_prove'):
        fail('FAIL_DOES_NOT_PROVE_MISSING')
    return True


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) not in (1,2):
        raise SystemExit('usage: validate_measurement_coverage_sufficiency.py RECEIPT.json [CONTRACT.json]')
    receipt = json.loads(Path(argv[0]).read_text(encoding='utf-8'))
    contract_path = Path(argv[1]) if len(argv)==2 else Path(__file__).resolve().parents[1] / 'contracts' / 'MEASUREMENT_COVERAGE_SUFFICIENCY_CONTRACT_v1.json'
    contract = json.loads(contract_path.read_text(encoding='utf-8'))
    validate(receipt, contract)
    print('PASS_MEASUREMENT_COVERAGE_SUFFICIENCY')


if __name__ == '__main__':
    main()
