#!/usr/bin/env python3
"""R28A HP diagnostic — normalize visible wheel meshes to locked 0.70 m OD.
R28A Source geometry remains bitwise/shape-hash locked. The correction applies only to
WHEEL_* display/package meshes before diagnostic rendering.

World-space envelope validation is computed directly from mesh vertices rather than
Object.bound_box so the post-edit readback cannot use Blender's stale bound-box cache.
"""
from __future__ import annotations
import importlib.util,bpy,json
from pathlib import Path
BASE='/tmp/revise_v011_r28a_diag.py'
spec=importlib.util.spec_from_file_location('diag',BASE);diag=importlib.util.module_from_spec(spec);spec.loader.exec_module(diag)
TARGET_OD=.700
_orig_wheels=diag.b.wheels
FIX_RECORD=[]

def wb(o):
    pts=[o.matrix_world@v.co for v in o.data.vertices]
    mn=[min(p[i] for p in pts) for i in range(3)];mx=[max(p[i] for p in pts) for i in range(3)]
    return {'min':mn,'max':mx,'dimensions':[mx[i]-mn[i] for i in range(3)],'center':[(mn[i]+mx[i])*.5 for i in range(3)]}

def fixed_wheels(M):
    res=_orig_wheels(M)
    for o in [x for x in bpy.context.scene.objects if x.type=='MESH' and x.name.startswith('WHEEL_')]:
        before=wb(o);cx=o.location.x;cz=o.location.z;fx=TARGET_OD/before['dimensions'][0];fz=TARGET_OD/before['dimensions'][2];inv=o.matrix_world.inverted()
        for v in o.data.vertices:
            p=o.matrix_world@v.co
            p.x=cx+(p.x-cx)*fx
            p.z=cz+(p.z-cz)*fz
            v.co=inv@p
        o.data.update();bpy.context.view_layer.update();after=wb(o)
        o['OLEANDER_HP_WHEEL_OD_M']=TARGET_OD;o['OLEANDER_HP_NORMALIZATION']='WORLD_XZ_ENVELOPE_ONLY'
        FIX_RECORD.append({'name':o.name,'before':before,'after':after,'factor_x':fx,'factor_z':fz})
    return res

diag.b.wheels=fixed_wheels

def main():
    code=0
    try:diag.main()
    except SystemExit as e:code=int(e.code or 0)
    a=diag.b.parse();out=Path(a.out).resolve();data={'schema':'oleander.auto.v0.11.wheel-hp-normalization','target_od_m':TARGET_OD,'source_change':False,'validation_method':'WORLD_SPACE_MESH_VERTICES','wheel_mesh_count':len(FIX_RECORD),'records':FIX_RECORD}
    (out/'WHEEL_HP_NORMALIZATION.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text());q['schema']='oleander.auto.v0.11.r28a.hpdiag.qa'
    q['checks']['wheel_hp_od_normalized']=len(FIX_RECORD)==4 and all(abs(r['after']['dimensions'][0]-TARGET_OD)<1e-5 and abs(r['after']['dimensions'][2]-TARGET_OD)<1e-5 for r in FIX_RECORD)
    q['checks']['wheel_centers_retained']=len(FIX_RECORD)==4 and all(abs(r['after']['center'][0]-r['before']['center'][0])<1e-6 and abs(r['after']['center'][2]-r['before']['center'][2])<1e-6 for r in FIX_RECORD)
    q['checks']['wheel_y_thickness_retained']=len(FIX_RECORD)==4 and all(abs(r['after']['dimensions'][1]-r['before']['dimensions'][1])<1e-6 for r in FIX_RECORD)
    q['boundary']='R28A Source locked. Four visible wheel meshes normalized in world X/Z to locked 0.70 m OD before diagnostic rendering; world-space mesh-vertex readback verifies OD, centers and Y thickness.'
    q['status']='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(q['checks'].values()) else 'MACHINE_FAIL';qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text());c['job_id']='SYS-MODELING-WORKER-AUTO-M1M5-v0.11-R28A-HPDIAG';c['revision']={'revision_id':'R28A-WHEEL-HP-DIAGNOSTIC','source_change':False,'wheel_display_change':'normalize WHEEL_* world x/z envelope to 0.70 m locked OD','validation_readback':'world-space mesh vertices','design_variable_change':False};c['qa']['construction'].append('R28A Source unchanged; wheel visualization corrected to locked M1 hard point before Human M5');cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    raise SystemExit(0 if q['status']=='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' else (code or 5))
if __name__=='__main__':main()
