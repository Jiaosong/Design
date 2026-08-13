#!/usr/bin/env python3
"""Inspect the exact world-space wheel package envelope used by Automotive v0.11.
No Source geometry is built or modified."""
from __future__ import annotations
import importlib.util,bpy,json
from pathlib import Path
from mathutils import Vector
BASE='/tmp/build_automotive_v011_r05.py'
spec=importlib.util.spec_from_file_location('b',BASE);b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)

def bounds(o):
    pts=[o.matrix_world@Vector(c) for c in o.bound_box]
    return {'min':[min(p.x for p in pts),min(p.y for p in pts),min(p.z for p in pts)],'max':[max(p.x for p in pts),max(p.y for p in pts),max(p.z for p in pts)]}
def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials();b.wheels(M)
    objs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('WHEEL_')]
    records=[]
    for o in objs:
        bb=bounds(o);records.append({'name':o.name,'location':list(o.location),'bounds':bb})
    clusters={}
    for axle,wx in (('FRONT',b.FX),('REAR',b.RX)):
        for side,sy in (('NEAR',-1),('FAR',1)):
            sel=[]
            for r in records:
                cx=(r['bounds']['min'][0]+r['bounds']['max'][0])/2;cy=(r['bounds']['min'][1]+r['bounds']['max'][1])/2
                if abs(cx-wx)<.35 and (cy*sy)>0:sel.append(r)
            if sel:
                mn=[min(r['bounds']['min'][i] for r in sel) for i in range(3)];mx=[max(r['bounds']['max'][i] for r in sel) for i in range(3)]
                clusters[f'{axle}_{side}']={'object_count':len(sel),'min':mn,'max':mx,'dimensions':[mx[i]-mn[i] for i in range(3)],'center':[(mn[i]+mx[i])/2 for i in range(3)]}
    data={'schema':'oleander.auto.v0.11.wheel-envelope','hard_points':{'FX':b.FX,'RX':b.RX,'WY':b.WY,'WZ':b.WZ,'track_center_m':2*b.WY},'wheel_mesh_count':len(objs),'clusters':clusters,'objects':records}
    (out/'WHEEL_ENVELOPE.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');print(json.dumps(data,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
