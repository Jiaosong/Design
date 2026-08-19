#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
HERE=Path(__file__).resolve();CONTRACT=HERE.parents[1]/'contracts'/'EVALUATED_SURFACE_SAMPLING_CONTRACT_v1.json'

def fail(code,detail): raise SystemExit(f'{code}: {detail}')
def validate(d,c):
    for k in c['required_receipt_fields']:
        if k not in d: fail('FAIL_EVALUATED_SAMPLING_RECEIPT_STRUCTURE',f'missing {k}')
    if d['schema']!='oleander.3d.evaluated-surface-sampling-receipt.v1': fail('FAIL_EVALUATED_SAMPLING_RECEIPT_STRUCTURE','unexpected schema')
    if d['source_control_count_role']!='INFORMATIONAL_CAUSAL_CONTROL_COMPLEXITY_NOT_EVALUATED_QUALITY_GATE': fail('FAIL_SOURCE_COUNT_ROLE','Source control count must be informational')
    if not isinstance(d['source_control_count'],int) or d['source_control_count']<=0: fail('FAIL_EVALUATED_SAMPLING_RECEIPT_STRUCTURE','bad source_control_count')
    gate=d['evaluated_sampling_gate']
    if not isinstance(gate,dict): fail('FAIL_EVALUATED_SAMPLING_RECEIPT_STRUCTURE','sampling gate missing')
    for k in ('basis','threshold_or_rule','observed','status','context'):
        if k not in gate: fail('FAIL_EVALUATED_SAMPLING_RECEIPT_STRUCTURE',f'missing evaluated_sampling_gate.{k}')
    if gate['basis'] in ('SOURCE_CONTROL_COUNT','SOURCE_RING_CONTROL_COUNT'): fail('FAIL_SOURCE_DENSITY_USED_AS_EVALUATED_GATE',gate['basis'])
    if gate['status'] not in c['allowed_sampling_status']: fail('FAIL_EVALUATED_SAMPLING_RECEIPT_STRUCTURE','bad sampling status')
    result=d['result']
    if result not in c['allowed_results']: fail('FAIL_EVALUATED_SAMPLING_RECEIPT_STRUCTURE','bad result')
    mutated=bool(d['source_mutated_for_sampling'])
    equivalence=bool(d.get('source_equivalence_proven_after_sampling_edit',False))
    if mutated and not equivalence and result=='PASS_EVALUATED_SAMPLING': fail('FAIL_SOURCE_MUTATED_FOR_SAMPLING_ONLY','sampling PASS cannot follow unproven Source mutation')
    if result=='PASS_EVALUATED_SAMPLING':
        if gate['status']!='PASS': fail('FAIL_EVALUATED_SAMPLING_FALSE_PASS','gate not PASS')
    elif result=='FAIL_EVALUATED_SAMPLING':
        if gate['status']!='FAIL': fail('FAIL_EVALUATED_SAMPLING_RECEIPT_STRUCTURE','FAIL result requires FAIL gate')
    elif result=='HOLD_EVALUATED_SAMPLING_BASIS_UNRESOLVED':
        if gate['status']!='HOLD': fail('FAIL_EVALUATED_SAMPLING_RECEIPT_STRUCTURE','HOLD result requires HOLD gate')
    elif result=='FAIL_SOURCE_MUTATED_FOR_SAMPLING_ONLY':
        if not mutated: fail('FAIL_EVALUATED_SAMPLING_RECEIPT_STRUCTURE','source-mutation failure without mutation')
    if not isinstance(d['does_not_prove'],list) or not d['does_not_prove']: fail('FAIL_EVALUATED_SAMPLING_RECEIPT_STRUCTURE','does_not_prove missing')
    return True

def main():
    ap=argparse.ArgumentParser();ap.add_argument('receipt');a=ap.parse_args();d=json.loads(Path(a.receipt).read_text());c=json.loads(CONTRACT.read_text());validate(d,c);print('EVALUATED SURFACE SAMPLING RECEIPT PASS')
if __name__=='__main__':main()
