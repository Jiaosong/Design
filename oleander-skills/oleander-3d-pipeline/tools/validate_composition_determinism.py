#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path


def fail(code: str):
    raise SystemExit(code)


def validate(receipt: dict, contract: dict) -> bool:
    if receipt.get('schema') != contract.get('receipt_schema'):
        fail('FAIL_COMPOSITION_SCHEMA')
    for key in contract.get('required', []):
        if key not in receipt:
            fail('FAIL_COMPOSITION_MISSING_' + key.upper())
    if receipt.get('composition_result') not in contract.get('allowed_results', []):
        fail('FAIL_COMPOSITION_RESULT')
    if receipt.get('downstream_evidence_state') not in contract.get('allowed_downstream_states', []):
        fail('FAIL_COMPOSITION_DOWNSTREAM_STATE')

    standalone=receipt.get('standalone_signature') or {}
    composed=receipt.get('composed_signature') or {}
    for field in contract.get('required_signature_fields', []):
        if field not in standalone or field not in composed:
            fail('FAIL_COMPOSITION_SIGNATURE_FIELD:' + field)

    checks=receipt.get('comparison_checks')
    if not isinstance(checks,dict) or not checks:
        fail('FAIL_COMPOSITION_CHECKS_MISSING')

    comparable=bool(checks.get('source_identity_match')) and bool(checks.get('runtime_identity_match'))
    required_signature_keys=['vertices_match','edges_match','faces_match','bounds_or_dimensions_match','folds_match','nonmanifold_match','target_diagnostic_state_match']
    missing=[k for k in required_signature_keys if k not in checks]
    if missing:
        fail('FAIL_COMPOSITION_REQUIRED_CHECKS:' + ','.join(missing))
    all_signature=all(bool(checks[k]) for k in required_signature_keys)

    result=receipt.get('composition_result')
    downstream=receipt.get('downstream_evidence_state')
    if result=='PASS_COMPOSITION_DETERMINISTIC':
        if not comparable:
            fail('FAIL_COMPOSITION_PASS_NOT_COMPARABLE')
        if not all_signature:
            fail('FAIL_COMPOSITION_PASS_SIGNATURE_DRIFT')
        if downstream!='VALID_FOR_DECLARED_SCOPE':
            fail('FAIL_COMPOSITION_PASS_DOWNSTREAM_STATE')
    elif result=='FAIL_COMPOSITION_DETERMINISM':
        if not comparable:
            fail('FAIL_COMPOSITION_DETERMINISM_REQUIRES_COMPARABLE_INPUTS')
        if all_signature:
            fail('FAIL_COMPOSITION_FAIL_WITHOUT_DRIFT')
        if downstream!='NON_PROMOTABLE_DIAGNOSTIC_PROVENANCE':
            fail('FAIL_COMPOSITION_DRIFT_NOT_QUARANTINED')
    elif result=='HOLD_SOURCE_OR_RUNTIME_NOT_COMPARABLE':
        if comparable:
            fail('FAIL_COMPOSITION_HOLD_DESPITE_COMPARABLE_INPUTS')
        if downstream!='HOLD_NOT_COMPARABLE':
            fail('FAIL_COMPOSITION_HOLD_DOWNSTREAM_STATE')
    elif result=='PASS_REOPENED_PARENT_WITNESS':
        if receipt.get('composition_mechanism')!='REOPENED_NATIVE_PARENT_ARTIFACT':
            fail('FAIL_REOPEN_WITNESS_MECHANISM')
        if not comparable or not all_signature:
            fail('FAIL_REOPEN_WITNESS_SIGNATURE')
        if not checks.get('native_artifact_hash_match'):
            fail('FAIL_REOPEN_WITNESS_HASH')
        if downstream!='VALID_FOR_DECLARED_SCOPE':
            fail('FAIL_REOPEN_WITNESS_DOWNSTREAM_STATE')

    # Explicit guard against treating matching bounds as sufficient.
    if checks.get('bounds_or_dimensions_match') and not all_signature and result in ('PASS_COMPOSITION_DETERMINISTIC','PASS_REOPENED_PARENT_WITNESS'):
        fail('FAIL_BOUNDS_ONLY_FALSE_PASS')

    if not isinstance(receipt.get('does_not_prove'),list) or not receipt['does_not_prove']:
        fail('FAIL_DOES_NOT_PROVE_MISSING')
    return True


def main(argv=None):
    argv=argv or sys.argv[1:]
    if len(argv) not in (1,2):
        raise SystemExit('usage: validate_composition_determinism.py RECEIPT.json [CONTRACT.json]')
    receipt=json.loads(Path(argv[0]).read_text(encoding='utf-8'))
    cp=Path(argv[1]) if len(argv)==2 else Path(__file__).resolve().parents[1]/'contracts'/'COMPOSITION_DETERMINISM_CONTRACT_v1.json'
    contract=json.loads(cp.read_text(encoding='utf-8'))
    validate(receipt,contract);print('PASS_COMPOSITION_DETERMINISM')

if __name__=='__main__':main()
