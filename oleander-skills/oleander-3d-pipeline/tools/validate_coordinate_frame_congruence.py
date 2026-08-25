#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path


def fail(code: str):
    raise SystemExit(code)


def validate(receipt: dict, contract: dict) -> bool:
    if receipt.get('schema') != contract.get('receipt_schema'):
        fail('FAIL_FRAME_SCHEMA')
    for key in contract.get('required', []):
        if key not in receipt:
            fail('FAIL_FRAME_MISSING_' + key.upper())
    if receipt.get('geometry_state_class') not in contract.get('allowed_geometry_state_classes', []):
        fail('FAIL_FRAME_GEOMETRY_STATE')
    result=receipt.get('frame_result')
    if result not in contract.get('allowed_results', []):
        fail('FAIL_FRAME_RESULT')
    downstream=receipt.get('downstream_evidence_state')
    if downstream not in contract.get('allowed_downstream_states', []):
        fail('FAIL_FRAME_DOWNSTREAM_STATE')

    predicate=receipt.get('predicate_frame');operator=receipt.get('operator_frame');canonical=receipt.get('canonical_target_frame')
    if not all(isinstance(x,str) and x for x in (predicate,operator,canonical)):
        fail('FAIL_FRAME_IDENTITY_EMPTY')
    transforms=receipt.get('transforms')
    if not isinstance(transforms,list):
        fail('FAIL_FRAME_TRANSFORMS_TYPE')

    frames_differ=predicate != operator
    verified=[t for t in transforms if isinstance(t,dict) and t.get('verified') is True]
    if frames_differ and not verified and result in ('PASS_FRAME_CONGRUENCE','PASS_DIAGNOSTIC_COPY_NORMALIZED_FRAME'):
        fail('FAIL_FRAME_PASS_WITHOUT_VERIFIED_TRANSFORM')

    checks=receipt.get('frame_checks')
    if not isinstance(checks,dict) or not checks:
        fail('FAIL_FRAME_CHECKS_MISSING')
    if 'quantity_semantics_bound' not in checks or 'canonical_target_bound' not in checks:
        fail('FAIL_FRAME_REQUIRED_CHECKS')

    equivalence=bool(receipt.get('selection_equivalence_required'))
    try:
        audit=int(receipt.get('audit_target_count'));selected=int(receipt.get('operator_selected_count'))
    except Exception:
        fail('FAIL_FRAME_SELECTION_COUNT_TYPE')
    counts_match=audit==selected

    if result in ('PASS_FRAME_CONGRUENCE','PASS_DIAGNOSTIC_COPY_NORMALIZED_FRAME'):
        if not checks.get('quantity_semantics_bound') or not checks.get('canonical_target_bound'):
            fail('FAIL_FRAME_PASS_REQUIRED_CHECK')
        if equivalence and not counts_match:
            fail('FAIL_FRAME_PASS_SELECTION_COUNT_MISMATCH')
        if downstream!='VALID_FOR_DECLARED_SCOPE':
            fail('FAIL_FRAME_PASS_DOWNSTREAM_STATE')
    elif result=='FAIL_FRAME_MISMATCH':
        if downstream!='NON_PROMOTABLE_DIAGNOSTIC_PROVENANCE':
            fail('FAIL_FRAME_MISMATCH_NOT_QUARANTINED')
        if equivalence and counts_match and checks.get('transform_verified') is True:
            fail('FAIL_FRAME_MISMATCH_WITH_CONGRUENT_WITNESS')
    elif result=='HOLD_TRANSFORM_UNVERIFIED':
        if downstream!='HOLD_NOT_COMPARABLE':
            fail('FAIL_FRAME_HOLD_DOWNSTREAM_STATE')

    if receipt.get('metric_or_tolerance_frame') in (None,''):
        fail('FAIL_TOLERANCE_FRAME_MISSING')
    if not isinstance(receipt.get('does_not_prove'),list) or not receipt['does_not_prove']:
        fail('FAIL_DOES_NOT_PROVE_MISSING')
    return True


def main(argv=None):
    argv=argv or sys.argv[1:]
    if len(argv) not in (1,2):raise SystemExit('usage: validate_coordinate_frame_congruence.py RECEIPT.json [CONTRACT.json]')
    receipt=json.loads(Path(argv[0]).read_text(encoding='utf-8'))
    cp=Path(argv[1]) if len(argv)==2 else Path(__file__).resolve().parents[1]/'contracts'/'COORDINATE_FRAME_CONGRUENCE_CONTRACT_v1.json'
    contract=json.loads(cp.read_text(encoding='utf-8'))
    validate(receipt,contract);print('PASS_COORDINATE_FRAME_CONGRUENCE')

if __name__=='__main__':main()
