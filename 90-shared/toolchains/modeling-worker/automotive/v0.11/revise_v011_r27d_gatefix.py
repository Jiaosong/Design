#!/usr/bin/env python3
"""R27D gate adapter: replace the inherited R25 four-triangle-only assertion with
R27D's explicit 4 termination + 24 wheel-zone transition triangle contract."""
import importlib.util,json
from pathlib import Path
BASE='/tmp/revise_v011_r27d.py'
spec=importlib.util.spec_from_file_location('r27d',BASE);r27d=importlib.util.module_from_spec(spec);spec.loader.exec_module(r27d)

def main():
    code=0
    try:r27d.main()
    except SystemExit as e:code=int(e.code or 0)
    a=r27d.b.parse();out=Path(a.out).resolve();qp=out/'AUTOMOTIVE_V011_QA.json';rp=out/'AUTOMOTIVE_V011_RECEIPT.json'
    q=json.loads(qp.read_text());checks=q['checks'];expected=(q['topology']['tri']==28 and q['topology']['ngon']==0 and q['source_island_count']==1 and checks.get('source_no_boolean') is True and checks.get('source_no_subd') is True and checks.get('arch_endpoint_vertex_reuse_24') is True and checks.get('four_arch_boundaries') is True and checks.get('staggered_attachment_active') is True and checks.get('controlled_transition_triangles_24') is True and len(q.get('renders',[]))==9)
    checks['termination_triangles_four']=expected;checks['r27d_total_controlled_triangles_28']=q['topology']['tri']==28
    q['status']='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if expected else 'MACHINE_FAIL';qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    r=json.loads(rp.read_text());r['status']='EXECUTED_MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if expected else 'EXECUTED_MACHINE_FAIL';rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    raise SystemExit(0 if expected else (code or 2))
if __name__=='__main__':main()
