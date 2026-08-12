#!/usr/bin/env python3
"""OLEANDER Automotive Reference Vehicle v0.7 selective revision.
Loads the v0.6 working source and corrects only the roof-canopy envelope so the roof terminates
at the windshield/rear-glass upper edges and meets the side-glass/pillar line without a visor-like overhang.
Designer F1 benchmark only; not engineering CAD.
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import bpy

ap=argparse.ArgumentParser();ap.add_argument('--v04-source',required=True);ap.add_argument('--out',required=True);ap.add_argument('--samples',type=int,default=8);ap.add_argument('--resolution',type=int,default=720)
av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [];a=ap.parse_args(av)
code=Path(a.v04_source).read_text(encoding='utf-8').split('if __name__=="__main__":main()')[0]
exec(compile(code,a.v04_source,'exec'),globals(),globals())
MODEL='OLEANDER_Automotive_Reference_Vehicle_v0.7'

# Only the roof canopy changes. v0.5 lower body/wheels and v0.6 separate glazing/pillars remain locked.
for o in list(bpy.data.objects):
    if o.name.startswith('ROOF_CANOPY') or o.name.startswith('PANORAMIC_ROOF'):
        bpy.data.objects.remove(o,do_unlink=True)

# Roof envelope is deliberately bounded by the glazing:
# front edge ≈ windshield upper x=.67, rear edge ≈ rear-glass upper x=-.72,
# side edge ≈ side glazing y=±.755. No visor-like front/rear/side overhang.
st=[
    (-.76,.62,1.285,1.340),
    (-.55,.70,1.350,1.405),
    (-.28,.745,1.382,1.430),
    (.02,.755,1.390,1.435),
    (.32,.742,1.372,1.415),
    (.56,.690,1.315,1.365),
    (.66,.620,1.275,1.325),
]
loft('ROOF_CANOPY',st,M('MAT_BODY_PAINT'),24,3.2,1)

if bpy.data.materials.get('MAT_CLAY') is None:
    clay=bpy.data.materials.new('MAT_CLAY');clay.use_nodes=True;bs=clay.node_tree.nodes.get('Principled BSDF')
    if bs:
        if bs.inputs.get('Base Color'):bs.inputs['Base Color'].default_value=(.32,.315,.295,1)
        if bs.inputs.get('Roughness'):bs.inputs['Roughness'].default_value=.52

out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
bpy.context.scene['OLEANDER_MODEL']=MODEL
bpy.ops.wm.save_as_mainfile(filepath=str(out/f'{MODEL}.blend'))
R=render(out,a.samples,a.resolution)
q=qa(out,R);q['model']=MODEL;q['schema']='oleander.automotive.qa.v7';q['revision']='roof-canopy envelope only; v0.5 lower body/wheels and v0.6 glazing/pillars locked'
(out/'AUTOMOTIVE_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rec={'schema':'oleander.automotive.receipt.v7','model':MODEL,'blender_version':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),'status':'EXECUTED_QA_PASS' if q['status']=='PASS' else 'EXECUTED_QA_FAIL','renders':R,'qa':str(out/'AUTOMOTIVE_QA.json')}
(out/'AUTOMOTIVE_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if q['status']=='PASS' else 5)
