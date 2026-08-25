#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path


def fail(code: str):
    raise SystemExit(code)


def validate(receipt: dict, contract: dict) -> bool:
    if receipt.get('schema') != contract.get('receipt_schema'):
        fail('FAIL_HOST_PRESERVATION_SCHEMA')
    for key in contract.get('required', []):
        if key not in receipt:
            fail('FAIL_HOST_PRESERVATION_MISSING_' + key.upper())

    if receipt.get('locality') not in contract.get('allowed_locality', []):
        fail('FAIL_EDIT_LOCALITY_INVALID')
    if receipt.get('operator_execution') not in contract.get('allowed_operator_execution', []):
        fail('FAIL_OPERATOR_EXECUTION_STATE_INVALID')
    if receipt.get('host_preservation_result') not in contract.get('allowed_host_preservation_result', []):
        fail('FAIL_HOST_PRESERVATION_RESULT_INVALID')
    if receipt.get('evidence_result') not in contract.get('allowed_evidence_result', []):
        fail('FAIL_EVIDENCE_RESULT_INVALID')
    if receipt.get('design_result') not in contract.get('allowed_design_result', []):
        fail('FAIL_DESIGN_RESULT_INVALID')

    before = receipt.get('before') or {}
    after = receipt.get('after') or {}
    for key in contract.get('required_metric_fields', []):
        if key not in before or key not in after:
            fail('FAIL_HOST_METRIC_MISSING_' + key.upper())

    checks = receipt.get('preservation_checks')
    if not isinstance(checks, list) or not checks:
        fail('HOLD_HOST_PRESERVATION_CHECKS_MISSING')
    for check in checks:
        for key in contract.get('required_check_fields', []):
            if key not in check:
                fail('FAIL_PRESERVATION_CHECK_FIELD_MISSING_' + key.upper())
        if check.get('status') not in ('PASS', 'FAIL', 'HOLD'):
            fail('FAIL_PRESERVATION_CHECK_STATUS_INVALID')

    if receipt.get('locality') == 'LOCAL':
        global_checks = [c for c in checks if c.get('scope') == 'GLOBAL_HOST']
        if not global_checks:
            fail('FAIL_LOCAL_EDIT_WITHOUT_GLOBAL_HOST_CHECK')

    if receipt.get('source_mutation_allowed') is False and receipt.get('source_unchanged_or_na') is not True:
        fail('FAIL_PROTECTED_SOURCE_NOT_PROVEN_UNCHANGED')

    result = receipt.get('host_preservation_result')
    if result == 'PASS_WITHIN_DECLARED_BUDGET':
        if receipt.get('operator_execution') != 'PASS_EXECUTED':
            fail('FAIL_HOST_PASS_WITH_OPERATOR_FAILURE')
        if any(c.get('status') != 'PASS' for c in checks):
            fail('FAIL_HOST_PASS_WITH_FAILED_OR_HELD_CHECK')

    # Geometry delta is evidence of modification only, never preservation.
    if result == 'PASS_WITHIN_DECLARED_BUDGET' and receipt.get('geometry_changed_only_basis') is True:
        fail('FAIL_GEOMETRY_CHANGED_ONLY_FALSE_POSITIVE')

    if receipt.get('design_result') == 'PASS_INDEPENDENT_DESIGN_REVIEW' and not receipt.get('independent_design_review_receipt'):
        fail('FAIL_MACHINE_HOST_GATE_SELF_PROMOTED_TO_DESIGN_PASS')

    if not isinstance(receipt.get('does_not_prove'), list) or not receipt.get('does_not_prove'):
        fail('FAIL_DOES_NOT_PROVE_MISSING')
    return True


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) not in (1, 2):
        raise SystemExit('usage: validate_derived_edit_host_preservation.py RECEIPT.json [CONTRACT.json]')
    receipt = json.loads(Path(argv[0]).read_text(encoding='utf-8'))
    contract_path = Path(argv[1]) if len(argv) == 2 else Path(__file__).resolve().parents[1] / 'contracts' / 'DERIVED_EDIT_HOST_PRESERVATION_CONTRACT_v1.json'
    contract = json.loads(contract_path.read_text(encoding='utf-8'))
    validate(receipt, contract)
    print('PASS_DERIVED_EDIT_HOST_PRESERVATION')


if __name__ == '__main__':
    main()
