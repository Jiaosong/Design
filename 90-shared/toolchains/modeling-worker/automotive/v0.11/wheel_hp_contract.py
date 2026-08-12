#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 wheel hard-point implementation contract.

The current wheel asset generation preserves the intended wheel centers but produces an
anisotropic X/Z envelope (~0.71 x 1.0792 m) instead of the locked 0.70 m OD. This helper
wraps b.wheels() and deterministically normalizes the rendered wheel mesh to the current
runtime hard points while preserving Y thickness. It changes no body Source geometry.
"""
from __future__ import annotations
import bpy,json
TARGET_OD=.700

def _bounds(points):
    mn=[min(p[i] for p in points) for i in range(3)];mx=[max(p[i] for p in points) for i in range(3)]
    return {'min':mn,'max':mx,'dimensions':[mx[i]-mn[i] for i in range(3)],'center':[(mn[i]+mx[i])*.5 for i in range(3)]}
def raw_bounds(o):return _bounds([o.matrix_world@v.co for v in o.data.vertices])
def evaluated_bounds(o):
    dg=bpy.context.evaluated_depsgraph_get();oe=o.evaluated_get(dg);me=oe.to_mesh()
    try:return _bounds([oe.matrix_world@v.co for v in me.vertices])
    finally:oe.to_mesh_clear()
def near(a,b,t=1e-5):return abs(a-b)<t

def target_center(b,name):
    code=name.split('_')[1]
    x=b.FX if code.startswith('F') else b.RX
    y=b.WY if code.endswith('L') else -b.WY
    return [float(x),float(y),float(b.WZ)],code

def correct_existing_wheels(b,target_od=TARGET_OD):
    records=[]
    wheels=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('WHEEL_')]
    for o in wheels:
        before=raw_bounds(o);target,code=target_center(b,o.name);cx,cy,cz=before['center'];dx,dy,dz=before['dimensions'];fx=target_od/dx;fz=target_od/dz;inv=o.matrix_world.inverted()
        for v in o.data.vertices:
            p=o.matrix_world@v.co;p.x=target[0]+(p.x-cx)*fx;p.y=target[1]+(p.y-cy);p.z=target[2]+(p.z-cz)*fz;v.co=inv@p
        o.data.update();bpy.context.view_layer.update();after=evaluated_bounds(o)
        o['OLEANDER_HP_CONTRACT']='v0.11-OD700';o['OLEANDER_HP_TARGET_CENTER']=json.dumps(target);o['OLEANDER_HP_OD_M']=target_od
        records.append({'name':o.name,'wheel_code':code,'target_center':target,'before':before,'after_evaluated':after,'y_thickness_target':dy,'factor_x':fx,'factor_z':fz})
    return records

def package_exact(records,target_od=TARGET_OD):
    return len(records)==4 and all(near(r['after_evaluated']['dimensions'][0],target_od) and near(r['after_evaluated']['dimensions'][2],target_od) and near(r['after_evaluated']['dimensions'][1],r['y_thickness_target']) and all(near(r['after_evaluated']['center'][i],r['target_center'][i]) for i in range(3)) and ((r['after_evaluated']['center'][1]>0)==r['wheel_code'].endswith('L')) for r in records)

def install(b,target_od=TARGET_OD):
    if getattr(b,'_OLEANDER_WHEEL_HP_INSTALLED',False):return
    original=b.wheels
    def wrapped(M):
        result=original(M);records=correct_existing_wheels(b,target_od);b._OLEANDER_WHEEL_HP_RECORDS=records;b._OLEANDER_WHEEL_HP_EXACT=package_exact(records,target_od);return result
    b._OLEANDER_WHEELS_ORIGINAL=original;b.wheels=wrapped;b._OLEANDER_WHEEL_HP_INSTALLED=True
