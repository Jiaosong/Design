#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
HERE=Path(__file__).resolve(); CONTRACT=HERE.parents[1]/'contracts'/'RENDERED_PROJECTION_FIDELITY_CONTRACT_v1.json'

def fail(code,detail): raise SystemExit(f'{code}: {detail}')
def num(v):
 if isinstance(v,(int,float)) and math.isfinite(float(v)): return float(v)
 fail('FAIL_PROJECTION_RECEIPT_STRUCTURE',f'invalid number {v!r}')
def validate(d,c):
 for k in c['required_fields']:
  if k not in d or d[k] in (None,'',[],{}): fail('FAIL_PROJECTION_RECEIPT_STRUCTURE',f'missing {k}')
 if d['status'] not in c['allowed_status']: fail('FAIL_PROJECTION_RECEIPT_STRUCTURE',f"invalid status {d['status']}")
 metrics=d['metrics']
 if not isinstance(metrics,list) or not metrics: fail('FAIL_PROJECTION_RECEIPT_STRUCTURE','metrics missing')
 expected_pass=True
 for m in metrics:
  for k in ('id','target','candidate','limit','reference_target_source','candidate_measurement_source'):
   if k not in m: fail('FAIL_PROJECTION_RECEIPT_STRUCTURE',f"{m.get('id')} missing {k}")
  if m['reference_target_source']==m['candidate_measurement_source']: fail('FAIL_PROJECTION_SELF_REFERENCE',m['id'])
  src=str(m['candidate_measurement_source']).upper()
  if any(x in src for x in ('BASE_SHELL_RING','SOURCE_TARGET','CONTROL_TARGET')) and 'FINAL_VISIBLE_UNION' not in src:
   fail('FAIL_INTERMEDIATE_GEOMETRY_AS_FINAL_CANDIDATE',f"{m['id']} uses {m['candidate_measurement_source']}")
  err=abs(num(m['candidate'])-num(m['target']));lim=num(m['limit'])
  if 'abs_error' in m and abs(num(m['abs_error'])-err)>1e-6: fail('FAIL_PROJECTION_ERROR_MISMATCH',m['id'])
  if err>lim: expected_pass=False
 if (d['status']=='PROJECTION_MACHINE_SCREENING_PASS') != expected_pass:
  fail('FAIL_PROJECTION_METRIC_LIMIT',f"declared {d['status']} expected {'PASS' if expected_pass else 'FAIL'}")
 if d.get('reference_fidelity_review') in ('PASS','KEEP') and not d.get('independent_visual_review',False):
  fail('FAIL_PROJECTION_SELF_PROMOTION','reference fidelity KEEP/PASS requires independent visual review')
 if d.get('design_quality_gate') in ('PASS','KEEP') and not d.get('independent_design_review',False):
  fail('FAIL_PROJECTION_SELF_PROMOTION','design KEEP/PASS requires independent review')
 return True

def main():
 ap=argparse.ArgumentParser();ap.add_argument('receipt');a=ap.parse_args();d=json.loads(Path(a.receipt).read_text());c=json.loads(CONTRACT.read_text());validate(d,c);print('RENDERED PROJECTION FIDELITY RECEIPT PASS')
if __name__=='__main__':main()
