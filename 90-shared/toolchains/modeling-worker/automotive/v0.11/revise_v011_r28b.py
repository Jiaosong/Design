#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R28B — Package-Constrained Inset Fender Patch.

R28A established the correct architectural direction: rebuild the complete local
shoulder-to-rocker fender window as one U-boundary-to-wheel-opening Source patch.
After correcting the wheel display/package implementation to the locked 0.70 m OD,
Human M5 still shows a folded/outboard fender lip. R28A's inner crown used
`shoulder + 0.026 m`, forcing the wheel-opening boundary outside the locked shoulder.

R28B isolates that relation only:
- retain R28A topology, U boundary, inner x/z opening target and radial layers;
- change the crown relation to `shoulder - 0.018 m` (inset, not outboard flange);
- normalize all four wheel display/package meshes to the locked 0.70 m x/z OD before
  the canonical 9-view render matrix;
- verify wheel centers/Y thickness and package-to-crown lateral clearance;
- keep R09/R11/R12/R18/R20 and all Source geometry outside the bounded wheel windows locked.
"""
from __future__ import annotations
import importlib.util,bpy,json
from pathlib import Path

BASE='/tmp/revise_v011_r28a.py'
spec=importlib.util.spec_from_file_location('r28a',BASE)
r28a=importlib.util.module_from_spec(spec);spec.loader.exec_module(r28a)
r25=r28a.r25;r24=r28a.r24;r20=r28a.r20;r18=r28a.r18;r16=r28a.r16;r14=r28a.r14;b=r28a.b

MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R28B'
for m in (r28a,r25,r24,r20,r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):
    m.MODEL=MODEL

# R28B isolates the R28A outboard-lip relation. Topology and x/z opening target stay locked.
CROWN_INSET_M=.018
r28a.LIP_Y=-CROWN_INSET_M
TARGET_OD=.700
PACKAGE_CLEARANCE_MIN=.015
TIRE_HALF_WIDTH=.077000052
PACKAGE_OUTER_Y=b.WY+TIRE_HALF_WIDTH

_orig_wheels=b.wheels
WHEEL_FIX=[]

def mesh_world_bounds(o):
    pts=[o.matrix_world@v.co for v in o.data.vertices]
    mn=[min(p[i] for p in pts) for i in range(3)]
    mx=[max(p[i] for p in pts) for i in range(3)]
    return {'min':mn,'max':mx,'dimensions':[mx[i]-mn[i] for i in range(3)],'center':[(mn[i]+mx[i])*.5 for i in range(3)]}

def hp_wheels(M):
    res=_orig_wheels(M)
    for o in [x for x in bpy.context.scene.objects if x.type=='MESH' and x.name.startswith('WHEEL_')]:
        before=mesh_world_bounds(o);cx=before['center'][0];cz=before['center'][2]
        fx=TARGET_OD/before['dimensions'][0];fz=TARGET_OD/before['dimensions'][2];inv=o.matrix_world.inverted()
        for v in o.data.vertices:
            p=o.matrix_world@v.co;p.x=cx+(p.x-cx)*fx;p.z=cz+(p.z-cz)*fz;v.co=inv@p
        o.data.update();bpy.context.view_layer.update();after=mesh_world_bounds(o)
        WHEEL_FIX.append({'name':o.name,'before':before,'after':after,'factor_x':fx,'factor_z':fz})
    return res
b.wheels=hp_wheels


def context_snapshot():
    rows=b.controls_resampled();items=[]
    for label,wx in (('FRONT',b.FX),('REAR',b.RX)):
        shoulder=r14.interp_row(rows[4],wx);under=r14.interp_row(rows[7],wx)
        crown_y=shoulder[1]-CROWN_INSET_M
        items.append({
            'axle':label,'wheel_x_m':wx,
            'shoulder_y_m':shoulder[1],'shoulder_z_m':shoulder[2],
            'under_y_m':under[1],'under_z_m':under[2],
            'package_outer_y_m':PACKAGE_OUTER_Y,
            'crown_inner_y_m':crown_y,
            'package_to_crown_clearance_m':crown_y-PACKAGE_OUTER_Y,
        })
    return items


def patch_outputs(out:Path,ctx):
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text())
    c['job_id']='SYS-MODELING-WORKER-AUTO-M4M5-v0.11-R28B'
    c['decision_question']='With the wheel package corrected to the locked 0.70 m OD, does insetting the R28A inner fender crown relative to the locked shoulder remove the folded/outboard lip while preserving package cover and the local U-boundary patch architecture?'
    c['source_authority']['editable_source']=f'{MODEL}.blend'
    c['revision']={
        'revision_id':'R28B-PACKAGE-CONSTRAINED-INSET-FENDER',
        'semantic_targets':['front/rear inner fender crown lateral relation','wheel display/package hard-point implementation'],
        'parameters':{
            'r28a_topology_locked':True,'window_half_m':r28a.WINDOW,'inner_rx_m':r28a.INNER_RX,'inner_rz_m':r28a.INNER_RZ,
            'radial_layers':r28a.RADIAL_LAYERS,'crown_relation':'shoulder_y - 0.018 m','target_wheel_od_m':TARGET_OD,
            'wheel_y_thickness_change':False,'source_boolean':False,'source_subd':False,
        },
        'expected_affected_components':['local fender patch y-coordinates inside bounded wheel windows','wheel display/package meshes only'],
        'affected_view_policy':'HYBRID',
    }
    c['locks'].append({'target':'R28A topology + U outer boundary + inner x/z opening + R09/R11/R12/R18/R20','state':'LOCKED','reason':'R28B isolates crown lateral ordering after HP wheel correction','unlock_trigger':None})
    c['qa']['project']=['R28A folded/outboard white lip must disappear','inner fender crown must remain outside corrected near-side tire package by >=15 mm at wheel center','fender crown must remain shoulder-fed','Strip/Grazing highlights must not show a fold or self-overlap','M6/M7/M8 remains blocked']
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')

    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text())
    q['schema']='oleander.auto.v0.11.r28b.qa';q['model']=MODEL
    q['checks']['r28a_topology_retained']=True
    q['checks']['inset_crown_relation_active']=r28a.LIP_Y<0
    q['checks']['wheel_hp_od_normalized']=len(WHEEL_FIX)==4 and all(abs(x['after']['dimensions'][0]-TARGET_OD)<1e-5 and abs(x['after']['dimensions'][2]-TARGET_OD)<1e-5 for x in WHEEL_FIX)
    q['checks']['wheel_centers_retained']=len(WHEEL_FIX)==4 and all(abs(x['after']['center'][0]-x['before']['center'][0])<1e-6 and abs(x['after']['center'][2]-x['before']['center'][2])<1e-6 for x in WHEEL_FIX)
    q['checks']['wheel_y_thickness_retained']=len(WHEEL_FIX)==4 and all(abs(x['after']['dimensions'][1]-x['before']['dimensions'][1])<1e-6 for x in WHEEL_FIX)
    q['checks']['package_crown_clearance_min']=all(x['package_to_crown_clearance_m']>=PACKAGE_CLEARANCE_MIN for x in ctx)
    q['boundary']='R28B retains R28A local patch topology and x/z opening. Only inner-crown y ordering is inset relative to shoulder; all rendered wheels are corrected to locked 0.70 m OD. Human M5 required; M6/M7/M8 blocked.'
    q['status']='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(q['checks'].values()) else 'MACHINE_FAIL'
    qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')

    rp=out/'AUTOMOTIVE_V011_RECEIPT.json';r=json.loads(rp.read_text());r['schema']='oleander.auto.v0.11.r28b.receipt';r['model']=MODEL;r['status']='EXECUTED_'+q['status'];rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    (out/'R28B_CONTEXT.json').write_text(json.dumps({'schema':'oleander.auto.v0.11.r28b.context','model':MODEL,'wheel_target_od_m':TARGET_OD,'wheel_package_outer_y_m':PACKAGE_OUTER_Y,'crown_inset_m':CROWN_INSET_M,'minimum_required_clearance_m':PACKAGE_CLEARANCE_MIN,'axles':ctx,'wheel_normalization':WHEEL_FIX},ensure_ascii=False,indent=2)+'\n')
    (out/'R28_PATCH_CONTRACT.json').write_text(json.dumps({'model':MODEL,'stage':'M5','revision':'R28B','status':q['status'],'topology':'R28A_LOCAL_POLAR_TO_BODY_PATCH_RETAINED','crown_relation':'SHOULDER_MINUS_18MM','wheel_display_package':'HP_NORMALIZED_700MM_OD','blocked':['M6','M7','M8']},ensure_ascii=False,indent=2)+'\n')
    return q


def main():
    ctx=context_snapshot();code=0
    try:r28a.main()
    except SystemExit as e:code=int(e.code or 0)
    a=b.parse();out=Path(a.out).resolve();q=patch_outputs(out,ctx)
    raise SystemExit(0 if q['status']=='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' else (code or 5))

if __name__=='__main__':main()
