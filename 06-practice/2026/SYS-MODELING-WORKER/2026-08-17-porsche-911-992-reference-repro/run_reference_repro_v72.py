#!/usr/bin/env python3
"""V72 — bounded iterative Derived boundary refinement on V71.

V71 reduced true XZ-boundary straddling faces from 118 to 34 while preserving Source, bounds, folds and
manifoldness. The remaining crossings are confined to the two long rear-aperture edges. V72 does not widen
or move the canonical boundary and does not delete aperture faces. It repeats the same local, true-straddle
Derived split with an explicit convergence breaker:

- maximum 4 additional cycles after the V71 pass;
- stop immediately at zero straddles;
- stop if a cycle does not reduce the count;
- stop/fail on bounds, fold or manifold regression;
- Source remains V59 and no Source controls are added.

`REPEATABLE_LOCAL_REFINEMENT` is allowed only while each cycle materially reduces the declared boundary
error without degrading protected invariants.
"""
from __future__ import annotations
import json
from pathlib import Path
import bpy,bmesh
from mathutils import Vector

HERE=Path(__file__).resolve().parent
V71=HERE/'run_reference_repro_v71.py'
text=V71.read_text(encoding='utf-8');marker='\nrun71()\n'
if marker not in text:raise SystemExit('V71 run marker missing')
ns={'__file__':str(V71),'__name__':'oleander_v72_iterative_xz_refinement'}
exec(compile(text.split(marker,1)[0],str(V71),'exec'),ns)

v=ns['v'];core=ns['core'];runtime=ns['runtime']
base_split=ns['split_xz_edges'];BAND=ns['BAND'];select_edge_geom=ns['select_edge_geom'];edge_straddle_counts=ns['edge_straddle_counts']
world_dims=ns['world_dims'];folds=ns['folds'];nonmanifold_count=ns['nonmanifold_count'];boundary_counts=ns['boundary_counts']
REV='V72_DERIVED_REAR_APERTURE_ITERATIVE_XZ_BOUNDARY_SPLIT'
ns['REV']=REV
v.REF='2025_992.2_CARRERA_ITERATIVE_XZ_BOUNDARY_SPLIT_V72'
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['source_edit_scope']='NONE__BOUNDED_ITERATIVE_DERIVED_XZ_BOUNDARY_REFINEMENT_ONLY'
v.REFERENCE_CONTRACT['primary_body_source_revision_locked']='V59_SPARSE_FRONT_HOOD_FENDER_RELATION'
v.REFERENCE_CONTRACT['iteration_policy']='MAX_4_ADDITIONAL_CYCLES__STOP_ZERO_OR_STAGNATION_OR_PROTECTED_INVARIANT_REGRESSION'

V72_STATS={'cycles':[]}


def snapshot(obj):
    edge_counts,unique,_=edge_straddle_counts(obj)
    return {
      'vertices':len(obj.data.vertices),'edges':len(obj.data.edges),'faces':len(obj.data.polygons),
      'dims':world_dims(obj),'folds':folds(obj),'nonmanifold_edges':nonmanifold_count(obj),
      'lateral_boundary_counts':boundary_counts(obj),'xz_edge_straddles':edge_counts,
      'xz_unique_straddling_faces':unique
    }


def one_cycle(obj,cycle_id):
    before=snapshot(obj)
    bm=bmesh.new();bm.from_mesh(obj.data);ops=[]
    for idx in range(4):
        a=BAND[idx];b=BAND[(idx+1)%4];faces,geom=select_edge_geom(bm,a,b)
        dx=b[0]-a[0];dz=b[1]-a[1];pre=(len(bm.verts),len(bm.edges),len(bm.faces))
        if faces:
            bmesh.ops.bisect_plane(
                bm,geom=geom,dist=1e-7,
                plane_co=Vector((a[0],0.0,a[1])),plane_no=Vector((dz,0.0,-dx)).normalized(),
                clear_inner=False,clear_outer=False)
        post=(len(bm.verts),len(bm.edges),len(bm.faces))
        ops.append({'edge':idx,'selected_true_straddling_faces':len(faces),'before':pre,'after':post})
    bm.normal_update();bm.to_mesh(obj.data);bm.free();obj.data.update()
    after=snapshot(obj)
    dimerr=[abs(after['dims'][i]-before['dims'][i]) for i in range(3)]
    protected_ok=(max(dimerr)<=1e-6 and after['folds']==before['folds'] and after['nonmanifold_edges']==before['nonmanifold_edges'])
    reduced=after['xz_unique_straddling_faces'] < before['xz_unique_straddling_faces']
    rec={
      'cycle':cycle_id,'before_unique_straddles':before['xz_unique_straddling_faces'],
      'after_unique_straddles':after['xz_unique_straddling_faces'],'edge_counts_before':before['xz_edge_straddles'],
      'edge_counts_after':after['xz_edge_straddles'],'dimension_abs_error_m':dimerr,
      'protected_invariants':'PASS' if protected_ok else 'FAIL','material_reduction':reduced,'operations':ops
    }
    V72_STATS['cycles'].append(rec)
    return rec


def iterative_split(obj):
    V72_STATS['global_before']=snapshot(obj)
    base_split(obj)
    # V71's first pass is retained as cycle 1 provenance.
    first_after=snapshot(obj)
    V72_STATS['cycles'].append({
      'cycle':1,'source':'V71_BASE_PASS','before_unique_straddles':V72_STATS['global_before']['xz_unique_straddling_faces'],
      'after_unique_straddles':first_after['xz_unique_straddling_faces'],
      'edge_counts_before':V72_STATS['global_before']['xz_edge_straddles'],'edge_counts_after':first_after['xz_edge_straddles'],
      'dimension_abs_error_m':[abs(first_after['dims'][i]-V72_STATS['global_before']['dims'][i]) for i in range(3)],
      'protected_invariants':'PASS' if (first_after['folds']==V72_STATS['global_before']['folds'] and first_after['nonmanifold_edges']==V72_STATS['global_before']['nonmanifold_edges']) else 'FAIL',
      'material_reduction':first_after['xz_unique_straddling_faces']<V72_STATS['global_before']['xz_unique_straddling_faces']
    })
    stop='MAX_CYCLES_REACHED'
    for cycle in range(2,6):
        current=snapshot(obj)
        if current['xz_unique_straddling_faces']==0:
            stop='ZERO_STRADDLES';break
        rec=one_cycle(obj,cycle)
        if rec['protected_invariants']!='PASS':
            stop='PROTECTED_INVARIANT_REGRESSION';break
        if not rec['material_reduction']:
            stop='STAGNATION_NO_MATERIAL_REDUCTION';break
    V72_STATS['global_after']=snapshot(obj);V72_STATS['stop_reason']=stop
    # Keep V71 shared stats coherent with the final object for downstream evidence readback.
    ns['STATS']['after']=V72_STATS['global_after']
    obj['OLEANDER_DERIVED_ITERATIVE_BOUNDARY_REFINEMENT']=REV;obj['OLEANDER_SOURCE_MUTATED']=False
    return obj

ns['split_xz_edges']=iterative_split


def emit72(out):
    b=V72_STATS['global_before'];a=V72_STATS['global_after'];dimerr=[abs(a['dims'][i]-b['dims'][i]) for i in range(3)]
    protected_ok=(max(dimerr)<=1e-6 and a['folds']==b['folds'] and a['nonmanifold_edges']==b['nonmanifold_edges'])
    lateral_ok=a['lateral_boundary_counts']['REAR_LATERAL_BOUNDARY_STRADDLE']==0
    xz_ok=a['xz_unique_straddling_faces']==0
    result='PASS_COMPLETE_REAR_BOUNDARY_REFINEMENT' if protected_ok and lateral_ok and xz_ok else 'FAIL_COMPLETE_REAR_BOUNDARY_REFINEMENT'
    d={
      'schema':'oleander.3d.iterative-semantic-boundary-refinement-receipt.v1','candidate_revision':REV,
      'source_revision_locked':'V59_SPARSE_FRONT_HOOD_FENDER_RELATION','source_mutated':False,
      'host':'DERIVED_911_9922_BODY','edit_scope':'REAR_APERTURE_XZ_BOUNDARY_BOUNDED_ITERATIVE_DERIVED_TOPOLOGY_ONLY',
      'global_before':b,'global_after':a,'cycles':V72_STATS['cycles'],'stop_reason':V72_STATS['stop_reason'],
      'dimension_abs_error_m':dimerr,'protected_invariants':'PASS' if protected_ok else 'FAIL',
      'lateral_boundary_ready':lateral_ok,'xz_boundary_ready':xz_ok,'boundary_refinement_result':result,
      'next_route':'V73_COMPLETE_REAR_OPENING_DESTRUCTIVE_PREFLIGHT_ONLY' if result=='PASS_COMPLETE_REAR_BOUNDARY_REFINEMENT' else 'DO_NOT_DELETE__RECLASSIFY_REMAINING_BOUNDARY_OPERATOR_FAILURE',
      'does_not_prove':['aperture deletion success','aperture closure','reference fidelity','Class-A continuity','manufacturer topology','Design KEEP']
    }
    Path(out,'V72_ITERATIVE_REAR_BOUNDARY_REFINEMENT_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(d,indent=2));return d


def run72():
    a=v.m.parse_args();out=Path(a.out).resolve();code=0
    try:runtime['run30']()
    except SystemExit as e:code=e.code if isinstance(e.code,int) else 0
    emit72(out);raise SystemExit(code)
run72()
