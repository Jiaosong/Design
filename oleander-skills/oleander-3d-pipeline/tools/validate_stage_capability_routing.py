#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

HERE=Path(__file__).resolve()
CONTRACT=HERE.parents[1]/'contracts'/'STAGE_CAPABILITY_ROUTING_CONTRACT_v1.json'


def fail(code, detail):
    raise SystemExit(f'{code}: {detail}')


def str_list(v, name):
    if not isinstance(v, list) or any(not isinstance(x, str) or not x for x in v):
        fail('FAIL_STAGE_CAPABILITY_RECEIPT_STRUCTURE', f'{name} must be a string list')
    if len(v) != len(set(v)):
        fail('FAIL_STAGE_CAPABILITY_RECEIPT_STRUCTURE', f'{name} contains duplicates')
    return v


def validate(d, c):
    for key in c['required_receipt_fields']:
        if key not in d:
            fail('FAIL_STAGE_CAPABILITY_RECEIPT_STRUCTURE', f'missing {key}')
    if d['schema'] != 'oleander.3d.stage-capability-routing-receipt.v1':
        fail('FAIL_STAGE_CAPABILITY_RECEIPT_STRUCTURE', 'unexpected receipt schema')
    if not isinstance(d['candidate_revision'], str) or not d['candidate_revision']:
        fail('FAIL_STAGE_CAPABILITY_RECEIPT_STRUCTURE', 'candidate_revision missing')
    if not isinstance(d['stage'], str) or not d['stage']:
        fail('FAIL_STAGE_CAPABILITY_RECEIPT_STRUCTURE', 'stage missing')
    required=set(str_list(d['required_capabilities'],'required_capabilities'))
    available=set(str_list(d['available_capabilities'],'available_capabilities'))
    held=set(str_list(d['held_capabilities'],'held_capabilities'))
    failed=set(str_list(d['failed_required_capabilities'],'failed_required_capabilities'))
    str_list(d['legacy_name_dependencies_not_required'],'legacy_name_dependencies_not_required')
    if required & held:
        fail('FAIL_REQUIRED_CAPABILITY_MISCLASSIFIED_AS_HOLD', sorted(required & held))
    if available & held:
        fail('FAIL_CAPABILITY_STATE_OVERLAP', sorted(available & held))
    result=d['result']
    if result not in c['allowed_results']:
        fail('FAIL_STAGE_CAPABILITY_RECEIPT_STRUCTURE', f'invalid result {result}')
    if held and d['held_result'] != c['rules']['held_result_for_explicit_stage_deferral']:
        fail('FAIL_STAGE_CAPABILITY_RECEIPT_STRUCTURE', 'held_result must be NOT_APPLICABLE_STAGE_HOLD')
    if result == 'PASS_STAGE_AWARE_ROUTING':
        missing=required-available
        if missing:
            fail('FAIL_REQUIRED_CAPABILITY_MISSING', sorted(missing))
        if failed:
            fail('FAIL_STAGE_PASS_WITH_FAILED_REQUIRED_CAPABILITY', sorted(failed))
    elif result == 'FAIL_REQUIRED_CAPABILITY_MISSING':
        if not failed and not (required-available):
            fail('FAIL_STAGE_CAPABILITY_RECEIPT_STRUCTURE', 'failure result without missing required capability')
    elif result == 'HOLD_STAGE_CAPABILITY_UNRESOLVED':
        if not d.get('stage_applicability_unresolved', True):
            fail('FAIL_STAGE_CAPABILITY_RECEIPT_STRUCTURE', 'HOLD result contradicts resolved stage')
    if not isinstance(d['does_not_prove'], list) or not d['does_not_prove']:
        fail('FAIL_STAGE_CAPABILITY_RECEIPT_STRUCTURE', 'does_not_prove missing')
    return True


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('receipt')
    args=ap.parse_args()
    d=json.loads(Path(args.receipt).read_text(encoding='utf-8'))
    c=json.loads(CONTRACT.read_text(encoding='utf-8'))
    validate(d,c)
    print('STAGE CAPABILITY ROUTING RECEIPT PASS')


if __name__=='__main__':
    main()
