#!/usr/bin/env python3
"""V74 — composition determinism probe for V72.

V73 produced a host signature inconsistent with standalone V72, so its residual tolerance A/B cannot yet be
promoted as operator evidence. V74 imports V72 declarations into an isolated context and runs the inherited
runtime WITHOUT changing v.REF, candidate revision, builder routing, or geometry controls before execution.
It then compares the resulting host signature to the exact same-head standalone V72 witness.

This is diagnostic-only. No new geometry intent is introduced.
"""
from __future__ import annotations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
V72=HERE/'run_reference_repro_v72.py'
text=V72.read_text(encoding='utf-8');marker='\nrun72()\n'
if marker not in text:raise SystemExit('V72 run marker missing')
v72_ctx={'__file__':str(V72),'__name__':'oleander_v74_v72_composition_probe'}
exec(compile(text.split(marker,1)[0],str(V72),'exec'),v72_ctx)

v=v72_ctx['v'];runtime=v72_ctx['runtime'];snapshot=v72_ctx['snapshot']
EXPECTED={
  'vertices':9093,'edges':18171,'faces':9080,'folds':0,'nonmanifold_edges':0,
  'xz_unique_straddling_faces':2,
  'dims':[4.4686994552612305,1.8454024195671082,1.1551822274923325]
}


def probe(out):
    identity_before={
      'v_ref':getattr(v,'REF',None),
      'candidate_revision':v.REFERENCE_CONTRACT.get('candidate_revision'),
      'source_edit_scope':v.REFERENCE_CONTRACT.get('source_edit_scope'),
      'build_visual_hull_name':getattr(v72_ctx['core'].get('build_visual_hull'),'__name__',None),
      'split_xz_edges_name':getattr(v72_ctx.get('ns',{}).get('split_xz_edges'),'__name__',None) if isinstance(v72_ctx.get('ns'),dict) else None
    }
    code=0
    try:runtime['run30']()
    except SystemExit as e:code=e.code if isinstance(e.code,int) else 0
    obj=v72_ctx['bpy'].data.objects.get('DERIVED_911_9922_BODY')
    if obj is None:raise SystemExit('FAIL_V74_HOST_MISSING')
    actual=snapshot(obj)
    checks={
      'vertices_match':actual['vertices']==EXPECTED['vertices'],
      'edges_match':actual['edges']==EXPECTED['edges'],
      'faces_match':actual['faces']==EXPECTED['faces'],
      'folds_match':actual['folds']==EXPECTED['folds'],
      'nonmanifold_match':actual['nonmanifold_edges']==EXPECTED['nonmanifold_edges'],
      'straddles_match':actual['xz_unique_straddling_faces']==EXPECTED['xz_unique_straddling_faces'],
      'dims_match':max(abs(actual['dims'][i]-EXPECTED['dims'][i]) for i in range(3))<=1e-9
    }
    result='PASS_COMPOSED_V72_MATCHES_STANDALONE' if all(checks.values()) else 'FAIL_COMPOSED_V72_DRIFT'
    d={
      'schema':'oleander.3d.composition-determinism-probe.v1','probe_revision':'V74_V72_COMPOSITION_DETERMINISM',
      'source_script':'run_reference_repro_v72.py','source_commit_expected_same_head':'7851b95523ef26c1fb78e3321203afcb0c60384f',
      'pre_run_identity_mutation':False,'identity_before':identity_before,'runtime_exit_code':code,
      'standalone_v72_expected':EXPECTED,'composed_v72_actual':actual,'checks':checks,
      'composition_result':result,
      'v73_provenance_note':'V73 changed diagnostic identity before inherited runtime and observed 8338 vertices / 8000 faces / 94 folds; its tolerance A/B remains non-promotable until composition cause is isolated.',
      'does_not_prove':['V73 operator conclusion','aperture closure','reference fidelity','Class-A continuity','Design KEEP']
    }
    Path(out,'V74_V72_COMPOSITION_DETERMINISM_PROBE.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(d,indent=2));return d,code


def main():
    a=v.m.parse_args();out=Path(a.out).resolve();d,code=probe(out)
    raise SystemExit(code if d['composition_result']=='PASS_COMPOSED_V72_MATCHES_STANDALONE' else 8)
main()
