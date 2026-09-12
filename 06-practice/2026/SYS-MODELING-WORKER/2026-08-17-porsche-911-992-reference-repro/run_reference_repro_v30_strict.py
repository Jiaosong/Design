#!/usr/bin/env python3
"""Strict gate wrapper for V30. Representation experiments do not receive relaxed regression limits."""
from __future__ import annotations
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
SRC=HERE/'run_reference_repro_v30.py'
text=SRC.read_text();marker='\nrun30()\n'
if marker not in text:raise SystemExit('V30 run marker missing')
ns={'__file__':str(SRC),'__name__':'oleander_v30_strict_declarations'}
exec(compile(text.split(marker,1)[0],str(SRC),'exec'),ns)

metric=ns['metric'];BEST=ns['BEST'];PROFILE=ns['PROFILE']

def regression30_strict(pr):
    vals={
      'SIDE_UPPER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_UPPER_EVALUATED_MESH_RMSE_M')['candidate'],
      'SIDE_LOWER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_LOWER_EVALUATED_MESH_RMSE_M')['candidate'],
      'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':metric(pr,'FRONT_UPPER_CABIN_WIDTH_RATIO')['abs_error'],
      'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':metric(pr,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO')['abs_error'],
      'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':metric(pr,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO')['abs_error'],
      'FRONT_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'FRONT_HALF_PROJECTED_PROFILE_RMSE')['candidate'],
      'REAR_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'REAR_HALF_PROJECTED_PROFILE_RMSE')['candidate'],
    }
    limits={
      'SIDE_UPPER_EVALUATED_MESH_RMSE_M':.034,
      'SIDE_LOWER_EVALUATED_MESH_RMSE_M':.066,
      'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':.010,
      'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':.010,
      'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':.010,
      'FRONT_HALF_PROJECTED_PROFILE_RMSE':.090,
      'REAR_HALF_PROJECTED_PROFILE_RMSE':.130,
    }
    locks=[]
    for mid,b in BEST.items():
        c=vals[mid]
        locks.append({'id':mid,'baseline':b['value'],'baseline_revision':b['revision'],'candidate':c,
                      'limit':limits[mid],'status':'PASS' if math.isfinite(c) and c<=limits[mid] else 'REGRESSED',
                      'evidence_source':b['evidence_source']})
    all_locks=all(x['status']=='PASS' for x in locks)
    return {
      'schema':'oleander.3d.reference-regression-promotion-receipt.v2',
      'baseline_revision':'BEST_KNOWN_GATE_BASELINE_V25',
      'candidate_revision':'V30_DENSE_PRIMARY_BODY_GRID_STRICT',
      'edit_scope':['PRIMARY_BODY_REPRESENTATION','BODY_SECTION_GRID','TERMINAL_PLAN_CURVATURE','STABLE_CABIN_FOR_BODY_REVIEW'],
      'target_metric_delta':{'metric_id':'PRIMARY_BODY_RING_RAIL_COUNT','baseline':12,'candidate':16,'direction':'HIGHER_IS_BETTER','improved':True},
      'regression_locks':locks,'best_known_gate_baselines':BEST,
      'measurement_method_ids':['V30_FINAL_EVALUATED_MESH_XZ','V30_FINAL_EVALUATED_MESH_YZ','V30_DENSE_GRID_TOPOLOGY'],
      'measurement_comparability':'COMPARABLE',
      'promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT' if all_locks else 'KEEP_LKG_REJECT_EXPERIMENT',
      'visual_review_state':'NOT_RUN','does_not_prove':PROFILE['does_not_prove']}

# Functions defined by exec resolve globals in ns; replace the unsafe exploratory implementation before run.
ns['regression30']=regression30_strict
ns['run30']()
