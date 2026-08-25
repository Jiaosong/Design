#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
HERE=Path(__file__).resolve();CONTRACT=HERE.parents[1]/'contracts'/'EVIDENCE_CARRIER_CONGRUENCE_CONTRACT_v1.json'

def fail(code,detail): raise SystemExit(f'{code}: {detail}')
def validate(d,c):
    for k in c['required_receipt_fields']:
        if k not in d: fail('FAIL_CARRIER_RECEIPT_STRUCTURE',f'missing {k}')
    if d['schema']!='oleander.3d.evidence-carrier-receipt.v1': fail('FAIL_CARRIER_RECEIPT_STRUCTURE','unexpected schema')
    if d['coverage_relation'] not in c['allowed_coverage_relations']: fail('FAIL_CARRIER_RECEIPT_STRUCTURE','bad coverage relation')
    if d['result'] not in c['allowed_results']: fail('FAIL_CARRIER_RECEIPT_STRUCTURE','bad result')
    rel,res=d['coverage_relation'],d['result']
    if res=='PASS_CARRIER_CONGRUENCE' and rel!='CONGRUENT': fail('FAIL_CARRIER_FALSE_PASS',f'{rel} cannot PASS_CARRIER_CONGRUENCE')
    if res=='PASS_SUFFICIENT_PROXY_FOR_DECLARED_SCOPE' and rel!='SUFFICIENT_PROXY_FOR_DECLARED_SCOPE': fail('FAIL_CARRIER_FALSE_PASS','proxy pass requires proxy relation')
    if rel=='MISMATCH' and not res.startswith('HOLD_'): fail('FAIL_CARRIER_FALSE_PASS','mismatch cannot pass')
    if rel=='UNRESOLVED' and not res.startswith('HOLD_'): fail('FAIL_CARRIER_FALSE_PASS','unresolved cannot pass')
    if d['candidate_state_class']=='VISUAL_PROXY' and res.startswith('PASS_'):
        if not d.get('proxy_claim_boundary') or not isinstance(d.get('does_not_prove'),list) or not d['does_not_prove']:
            fail('FAIL_PROXY_SCOPE_UNBOUNDED','visual proxy pass requires proxy_claim_boundary and does_not_prove')
    if d['regression_comparability'] not in ('COMPARABLE','NOT_COMPARABLE_CARRIER_CHANGED','NOT_APPLICABLE'):
        fail('FAIL_CARRIER_RECEIPT_STRUCTURE','bad regression_comparability')
    return True

def main():
    ap=argparse.ArgumentParser();ap.add_argument('receipt');a=ap.parse_args();d=json.loads(Path(a.receipt).read_text());c=json.loads(CONTRACT.read_text());validate(d,c);print('EVIDENCE CARRIER CONGRUENCE RECEIPT PASS')
if __name__=='__main__': main()
