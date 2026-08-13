#!/usr/bin/env python3
"""R27D technical orientation fix.
Recalculate Source face normals after staggered transition topology construction.
No vertex coordinates, topology membership, attachment radii or design parameters change.
"""
import importlib.util,bmesh,json
from pathlib import Path
BASE='/tmp/revise_v011_r27d.py'
spec=importlib.util.spec_from_file_location('r27d',BASE);r27d=importlib.util.module_from_spec(spec);spec.loader.exec_module(r27d)
_orig=r27d.build_source_r27d

def build_fixed(rows,M,glass):
    o,xs,cols,meta,reuse=_orig(rows,M,glass)
    bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
    o['R27D_ORIENTATION_FIX']='RECALC_FACE_NORMALS_ONLY'
    return o,xs,cols,meta,reuse
r27d.r25.build_source_raw=build_fixed

def main():
    code=0
    try:r27d.r25.main()
    except SystemExit as e:code=int(e.code or 0)
    a=r27d.b.parse();out=Path(a.out).resolve();r27d.patch_outputs(out)
    qp=out/'AUTOMOTIVE_V011_QA.json';rp=out/'AUTOMOTIVE_V011_RECEIPT.json';cp=out/'MODELING_CONTRACT.json'
    q=json.loads(qp.read_text());checks=q['checks'];expected=(q['topology']['tri']==28 and q['topology']['ngon']==0 and q['source_island_count']==1 and checks.get('source_no_boolean') is True and checks.get('source_no_subd') is True and checks.get('arch_endpoint_vertex_reuse_24') is True and checks.get('four_arch_boundaries') is True and checks.get('staggered_attachment_active') is True and checks.get('controlled_transition_triangles_24') is True and len(q.get('renders',[]))==9)
    checks['termination_triangles_four']=expected;checks['r27d_total_controlled_triangles_28']=q['topology']['tri']==28;checks['face_normals_recalculated']=True
    q['status']='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if expected else 'MACHINE_FAIL';q['boundary']='R27D geometry unchanged; face normals recalculated after controlled transition construction. Human M5 Visual QA required; M6/M7/M8 blocked.';qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    r=json.loads(rp.read_text());r['status']='EXECUTED_MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if expected else 'EXECUTED_MACHINE_FAIL';rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    c=json.loads(cp.read_text());c['revision']['orientation_fix']='RECALC_FACE_NORMALS_ONLY_NO_GEOMETRY_CHANGE';c['qa']['construction'].append('R27D full Source face normals recalculated after topology assembly');cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    raise SystemExit(0 if expected else (code or 2))
if __name__=='__main__':main()
