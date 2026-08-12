#!/usr/bin/env python3
"""v0.6 selective revision: widen roof canopy to close window interface gaps and remove invalid buried pano-roof slit."""
import argparse,sys,json
from pathlib import Path
import bpy

ap=argparse.ArgumentParser();ap.add_argument('--v04-source',required=True);ap.add_argument('--out',required=True);ap.add_argument('--samples',type=int,default=8);ap.add_argument('--resolution',type=int,default=720)
av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [];a=ap.parse_args(av)
code=Path(a.v04_source).read_text(encoding='utf-8').split('if __name__=="__main__":main()')[0]
exec(compile(code,a.v04_source,'exec'),globals(),globals())
MODEL='OLEANDER_Automotive_Reference_Vehicle_v0.6'

# Lock all v0.5 geometry except the roof/window interface.
for o in list(bpy.data.objects):
    if o.name.startswith('ROOF_CANOPY') or o.name.startswith('PANORAMIC_ROOF'):
        bpy.data.objects.remove(o,do_unlink=True)

# Wider, thin body-color roof canopy. The side windows are at y +/-0.755 m;
# canopy width now lands on their upper edge instead of floating inward.
st=[
 (-1.18,.64,1.16,1.215),(-.92,.72,1.275,1.335),(-.48,.76,1.34,1.405),
 (.02,.77,1.365,1.43),(.42,.76,1.335,1.40),(.76,.72,1.245,1.31),(.98,.63,1.125,1.185)
]
loft('ROOF_CANOPY',st,M('MAT_BODY_PAINT'),24,3.2,1)

# No panoramic insert at F1. A glass roof feature can be added later only if it helps a project-specific benchmark.
# This keeps the roof/window junction readable and avoids the previous two-slit artifact.

if bpy.data.materials.get('MAT_CLAY') is None:
    clay=bpy.data.materials.new('MAT_CLAY');clay.use_nodes=True;bs=clay.node_tree.nodes.get('Principled BSDF')
    if bs:
        if bs.inputs.get('Base Color'):bs.inputs['Base Color'].default_value=(.32,.315,.295,1)
        if bs.inputs.get('Roughness'):bs.inputs['Roughness'].default_value=.52

out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
bpy.context.scene['OLEANDER_MODEL']=MODEL
bpy.ops.wm.save_as_mainfile(filepath=str(out/f'{MODEL}.blend'))
R=render(out,a.samples,a.resolution)
q=qa(out,R);q['model']=MODEL;q['schema']='oleander.automotive.qa.v6';q['revision']='roof-window interface only; v0.5 lower body/wheels locked'
(out/'AUTOMOTIVE_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rec={'schema':'oleander.automotive.receipt.v6','model':MODEL,'blender_version':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),'status':'EXECUTED_QA_PASS' if q['status']=='PASS' else 'EXECUTED_QA_FAIL','renders':R,'qa':str(out/'AUTOMOTIVE_QA.json')}
(out/'AUTOMOTIVE_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if q['status']=='PASS' else 5)
