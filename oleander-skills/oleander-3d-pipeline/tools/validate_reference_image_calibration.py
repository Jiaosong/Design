#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
HERE=Path(__file__).resolve()
CONTRACT=HERE.parents[1]/'contracts'/'REFERENCE_IMAGE_CALIBRATION_CONTRACT_v1.json'

def fail(code,detail): raise SystemExit(f'{code}: {detail}')

def validate(data,contract):
 for key in contract['required_fields']:
  if key not in data or data[key] in (None,'',[],{}): fail('FAIL_REFERENCE_CONTOUR_TARGETS',f'missing {key}')
 if not data.get('target_revision'): fail('FAIL_REFERENCE_REVISION_MIXED','target_revision missing')
 scope=data['source_scope']
 if not isinstance(scope,dict) or not scope: fail('HOLD_REFERENCE_TRANSFER_SCOPE_UNRESOLVED','source_scope missing')
 for role,entry in scope.items():
  if not entry.get('source') or not entry.get('allowed_transfer'): fail('HOLD_REFERENCE_TRANSFER_SCOPE_UNRESOLVED',f'{role} lacks source/allowed_transfer')
 hard=data['official_hard_points_m']
 for key in contract['required_metric_hard_points']:
  if key not in hard: fail('FAIL_REFERENCE_CALIBRATION_ANCHORS',f'missing hard point {key}')
  if not isinstance(hard[key],(int,float)) or not math.isfinite(float(hard[key])): fail('FAIL_REFERENCE_CALIBRATION_ANCHORS',f'invalid hard point {key}')
 cal=data['side_calibration']; anchors=cal.get('pixel_anchors') or {}
 for key in contract['required_side_pixel_anchors']:
  if key not in anchors: fail('FAIL_REFERENCE_CALIBRATION_ANCHORS',f'missing pixel anchor {key}')
 vals=[float(anchors[k]) for k in ('rear_extreme_x','rear_wheel_center_x','front_wheel_center_x','front_extreme_x')]
 if not vals[0] < vals[1] < vals[2] < vals[3]: fail('FAIL_REFERENCE_CALIBRATION_ANCHORS','longitudinal pixel anchors must be monotonic')
 pts=data['side_top_silhouette_m']
 if len(pts) < int(contract['minimum_side_contour_samples']): fail('FAIL_REFERENCE_CONTOUR_TARGETS','insufficient side contour samples')
 xs=[]
 for p in pts:
  if not isinstance(p,list) or len(p)!=2: fail('FAIL_REFERENCE_CONTOUR_TARGETS',f'invalid contour point {p!r}')
  x,z=map(float,p)
  if not (math.isfinite(x) and math.isfinite(z)): fail('FAIL_REFERENCE_CONTOUR_TARGETS','non-finite contour point')
  xs.append(x)
 if any(b<=a for a,b in zip(xs,xs[1:])): fail('FAIL_REFERENCE_CONTOUR_TARGETS','contour x must be strictly increasing')
 if abs(xs[0]+float(hard['length'])/2)>0.06 or abs(xs[-1]-float(hard['length'])/2)>0.06: fail('FAIL_REFERENCE_CONTOUR_TARGETS','contour does not span official length')
 gates=data['gates']
 if gates.get('visual_reference_gate')!='INDEPENDENT_REVIEW_REQUIRED': fail('FAIL_REFERENCE_CONTOUR_TARGETS','machine calibration may not self-promote visual fidelity')
 if not data.get('does_not_prove'): fail('FAIL_REFERENCE_CONTOUR_TARGETS','does_not_prove required')
 return True

def main():
 ap=argparse.ArgumentParser();ap.add_argument('target');args=ap.parse_args()
 data=json.loads(Path(args.target).read_text());contract=json.loads(CONTRACT.read_text())
 validate(data,contract);print('REFERENCE IMAGE CALIBRATION PASS')
if __name__=='__main__': main()
