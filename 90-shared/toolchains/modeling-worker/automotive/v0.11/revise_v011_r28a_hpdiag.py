#!/usr/bin/env python3
"""R28A HP diagnostic — enforce the locked wheel package before visual review.

R28A Source geometry remains shape-hash locked. Only visible WHEEL_* package meshes are
corrected. Validation uses both raw mesh vertices and evaluated depsgraph geometry.
Required wheel authority:
- X/Z outside diameter = 0.700 m;
- wheel center = FX/RX, +/-WY, WZ;
- Y thickness unchanged from the current wheel asset.
"""
from __future__ import annotations
import importlib.util,bpy,json
from pathlib import Path
BASE='/tmp/revise_v011_r28a_diag.py'
spec=importlib.util.spec_from_file_location('diag',BASE);diag=importlib.util.module_from_spec(spec);spec.loader.exec_module(diag)
TARGET_OD=.700
_orig_wheels=diag.b.wheels
FIX_RECORD=[]

def bounds_from_points(pts):
    mn=[min(p[i] for p in pts) for i in range(3)];mx=[max(p[i] for p in pts) for i in range(3)]
    return {'min':mn,'max':mx,'dimensions':[mx[i]-mn[i] for i in range(3)],'center':[(mn[i]+mx[i])*.5 for i in range(3)]}

def raw_wb(o):return bounds_from_points([o.matrix_world@v.co for v in o.data.vertices])
def eval_wb(o):
    dg=bpy.context.evaluated_depsgraph_get();oe=o.evaluated_get(dg);me=oe.to_mesh()
    try:return bounds_from_points([oe.matrix_world@v.co for v in me.vertices])
    finally:oe.to_mesh_clear()

def target_center(name):
    code=name.split('_')[1]
    x=diag.b.FX if code.startswith('F') else diag.b.RX
    y=diag.b.WY if code.endswith('L') else -diag.b.WY
    return [float(x),float(y),float(diag.b.WZ)]

def fixed_wheels(M):
    res=_orig_wheels(M)
    wheels=[x for x in bpy.context.scene.objects if x.type=='MESH' and x.name.startswith('WHEEL_')]
    for o in wheels:
        before_raw=raw_wb(o);before_eval=eval_wb(o);target=target_center(o.name)
        cx,cy,cz=before_raw['center'];dx,dy,dz=before_raw['dimensions'];fx=TARGET_OD/dx;fz=TARGET_OD/dz;inv=o.matrix_world.inverted()
        for v in o.data.vertices:
            p=o.matrix_world@v.co
            p.x=target[0]+(p.x-cx)*fx
            p.y=target[1]+(p.y-cy)
            p.z=target[2]+(p.z-cz)*fz
            v.co=inv@p
        o.data.update();bpy.context.view_layer.update()
        after_raw=raw_wb(o);after_eval=eval_wb(o)
        o['OLEANDER_HP_WHEEL_OD_M']=TARGET_OD;o['OLEANDER_HP_TARGET_CENTER']=json.dumps(target);o['OLEANDER_HP_NORMALIZATION']='WORLD_RAW_AND_EVALUATED_GEOMETRY'
        FIX_RECORD.append({'name':o.name,'target_center':target,'before_raw':before_raw,'before_evaluated':before_eval,'after_raw':after_raw,'after_evaluated':after_eval,'factor_x':fx,'factor_z':fz,'y_thickness_target':dy})
    return res

diag.b.wheels=fixed_wheels

def near(a,b,tol=1e-5):return abs(a-b)<tol

def package_ok(r):
    ar=r['after_raw'];ae=r['after_evaluated'];tc=r['target_center']
    return (near(ar['dimensions'][0],TARGET_OD) and near(ar['dimensions'][2],TARGET_OD) and near(ae['dimensions'][0],TARGET_OD) and near(ae['dimensions'][2],TARGET_OD) and all(near(ar['center'][i],tc[i]) for i in range(3)) and all(near(ae['center'][i],tc[i]) for i in range(3)) and near(ar['dimensions'][1],r['y_thickness_target']) and near(ae['dimensions'][1],r['y_thickness_target']))

def main():
    code=0
    try:diag.main()
    except SystemExit as e:code=int(e.code or 0)
    a=diag.b.parse();out=Path(a.out).resolve();data={'schema':'oleander.auto.v0.11.wheel-hp-normalization.v3','target_od_m':TARGET_OD,'target_centers':{'front_left':[diag.b.FX,diag.b.WY,diag.b.WZ],'front_right':[diag.b.FX,-diag.b.WY,diag.b.WZ],'rear_left':[diag.b.RX,diag.b.WY,diag.b.WZ],'rear_right':[diag.b.RX,-diag.b.WY,diag.b.WZ]},'source_change':False,'validation_method':'RAW_MESH_PLUS_EVALUATED_DEPSGRAPH_WORLD_GEOMETRY','wheel_mesh_count':len(FIX_RECORD),'records':FIX_RECORD}
    (out/'WHEEL_HP_NORMALIZATION.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text());q['schema']='oleander.auto.v0.11.r28a.hpdiag.v3.qa';q['checks']['wheel_hp_package_exact']=len(FIX_RECORD)==4 and all(package_ok(r) for r in FIX_RECORD);q['checks']['wheel_hp_od_normalized']=q['checks']['wheel_hp_package_exact'];q['checks']['wheel_centers_match_hard_points']=len(FIX_RECORD)==4 and all(all(near(r['after_evaluated']['center'][i],r['target_center'][i]) for i in range(3)) for r in FIX_RECORD);q['checks']['wheel_y_thickness_retained']=len(FIX_RECORD)==4 and all(near(r['after_evaluated']['dimensions'][1],r['y_thickness_target']) for r in FIX_RECORD);q['checks'].pop('wheel_centers_retained',None);q['boundary']='R28A Source locked. Four visible wheel meshes must match M1 hard points in actual evaluated world geometry: OD X/Z=0.70 m, centers=FX/RX +/-WY WZ, Y thickness retained; FL/RL map to +WY and FR/RR to -WY.';q['status']='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(q['checks'].values()) else 'MACHINE_FAIL';qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text());c['job_id']='SYS-MODELING-WORKER-AUTO-M1M5-v0.11-R28A-HPDIAG-v3';c['revision']={'revision_id':'R28A-WHEEL-HP-DIAGNOSTIC-v3','source_change':False,'wheel_display_change':'enforce 0.70 m OD and exact M1 center on WHEEL_* world geometry','left_right_mapping':'FL/RL +WY; FR/RR -WY','validation_readback':'raw mesh + evaluated depsgraph','design_variable_change':False};c['qa']['construction'].append('R28A Source unchanged; wheel package must match locked M1 OD and centers before Human M5');cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    raise SystemExit(0 if q['status']=='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' else (code or 5))
if __name__=='__main__':main()
