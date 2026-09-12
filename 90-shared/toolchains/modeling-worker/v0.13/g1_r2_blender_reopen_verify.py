#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import math
import sys
from pathlib import Path

import bpy

SOURCE_OBJECT = 'OL_SRC_THUMB_SIDE_PLAN'
DERIVED_OBJECT = 'OL_DERIVED_G1_R2_BASELINE'
REBUILD_TEXT = 'OLEANDER_G1_R2_REBUILD.py'
LIVE_TEXT = 'OLEANDER_G1_R2_LIVE_SOURCE.json'


def args():
    p=argparse.ArgumentParser(); p.add_argument('--out',required=True); p.add_argument('--delta',type=float,default=0.003)
    return p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])


def verts(name):
    return [tuple(float(v) for v in x.co) for x in bpy.data.objects[name].data.vertices]


def max_disp(a,b):
    return max(math.dist(x,y) for x,y in zip(a,b))


def run_embedded_rebuild():
    t=bpy.data.texts.get(REBUILD_TEXT)
    if t is None: raise RuntimeError(f'missing embedded text: {REBUILD_TEXT}')
    scope={'__name__':'__main__','__file__':f'<blender-text:{REBUILD_TEXT}>'}
    exec(compile(t.as_string(), scope['__file__'], 'exec'), scope, scope)


def main():
    a=args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    checks={}
    checks['blend_has_native_source_object']=bpy.data.objects.get(SOURCE_OBJECT) is not None
    checks['blend_has_derived_surface']=bpy.data.objects.get(DERIVED_OBJECT) is not None
    checks['blend_has_embedded_rebuild']=bpy.data.texts.get(REBUILD_TEXT) is not None
    if not all(checks.values()):
        report={'status':'REOPEN_REBUILD_FAIL','checks':checks}; (out/'G1_R2_BLENDER_REOPEN_REBUILD_REPORT.json').write_text(json.dumps(report,indent=2)+'\n'); return 6

    baseline=verts(DERIVED_OBJECT); src=bpy.data.objects[SOURCE_OBJECT]; point=src.data.splines[0].points[3]; original=tuple(point.co)
    point.co[1]+=a.delta
    run_embedded_rebuild()
    edited=verts(DERIVED_OBJECT); edited_disp=max_disp(baseline,edited)
    live=json.loads(bpy.data.texts[LIVE_TEXT].as_string())
    live_thumb=float(live['thumb_side_plan'][3])
    point.co=original
    run_embedded_rebuild()
    restored=verts(DERIVED_OBJECT); restore_disp=max_disp(baseline,restored)

    checks.update({
        'embedded_rebuild_sets_pass_marker':bpy.context.scene.get('OLEANDER_LAST_NATIVE_REBUILD')=='PASS',
        'native_edit_changes_rebuilt_surface':edited_disp>=0.001,
        'live_source_text_reflects_native_edit':abs(live_thumb-float(original[1])-a.delta)<=1e-8,
        'restored_native_source_restores_surface':restore_disp<=1e-12,
        'derived_surface_remains_non_authority':bpy.data.objects[DERIVED_OBJECT].get('OLEANDER_AUTHORITY')=='DERIVED_EXECUTION_NOT_AUTHORITY',
        'authority_state_remains_working_source':bpy.context.scene.get('OLEANDER_AUTHORITY_STATE')=='WORKING_SOURCE',
        'candidate_promotion_remains_not_run':bpy.context.scene.get('OLEANDER_CANDIDATE_PROMOTION')=='NOT_RUN',
    })
    status='REOPEN_NATIVE_SOURCE_REBUILD_PASS' if all(checks.values()) else 'REOPEN_REBUILD_FAIL'
    report={
        'schema':'oleander.modeling-worker.v0.13.g1.r2.blender-reopen-rebuild',
        'status':status,'blend':Path(bpy.data.filepath).name,'source_object':SOURCE_OBJECT,'source_control_index':3,'edit_delta_m':a.delta,
        'edited_derived_surface_max_displacement_m':edited_disp,'restored_surface_max_error_m':restore_disp,'checks':checks,
        'authority_state':'WORKING_SOURCE','design_state':'REVISE','candidate_review':'REOPENED','candidate_promotion':'NOT_RUN',
        'boundary':'This proves the saved native .blend can continue editing the Blender-native Working Source and deterministically rebuild derived execution geometry. Reflection Visual QA remains separate and REVISE.'
    }
    (out/'G1_R2_BLENDER_REOPEN_REBUILD_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    bpy.context.scene['OLEANDER_REOPEN_NATIVE_REBUILD_VERIFIED']=status
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    print(json.dumps(report,ensure_ascii=False,indent=2)); return 0 if status.endswith('PASS') else 6


if __name__=='__main__': raise SystemExit(main())
