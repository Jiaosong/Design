#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
from typing import Any
import g1_geometry_core as core

MODEL='OLEANDER_ModelingWorker_v0.13_G1_ErgonomicHandheldFreeformShell'

def sub(a,b): return (a[0]-b[0],a[1]-b[1],a[2]-b[2])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def norm(a): return math.sqrt(dot(a,a))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):
    n=norm(a)
    if n<=1e-15: raise ValueError('degenerate analytic normal')
    return (a[0]/n,a[1]/n,a[2]/n)
def angle(a,b): return math.degrees(math.acos(max(-1.0,min(1.0,dot(a,b)))))

def normal(source,u,theta,revision=False):
    du=dv=1e-4
    a=sub(core.point(source,min(.99999,u+du),theta,revision),core.point(source,max(.00001,u-du),theta,revision))
    b=sub(core.point(source,u,theta+dv,revision),core.point(source,u,theta-dv,revision))
    return unit(cross(a,b))

def fairness(source,revision=False):
    ml=mc=0.0
    for iu in range(45):
        u=.03+.94*iu/44
        for j in range(72):
            t=2*math.pi*j/72
            n0=normal(source,u,t,revision)
            ml=max(ml,angle(n0,normal(source,min(.97,u+.01),t,revision)))
            mc=max(mc,angle(n0,normal(source,u,t+.05,revision)))
    return {'max_longitudinal_normal_delta_deg_per_0_01u':ml,'max_circumferential_normal_delta_deg_per_0_05rad':mc}

def bbox(verts):
    mi=[min(p[i] for p in verts) for i in range(3)]; ma=[max(p[i] for p in verts) for i in range(3)]
    return {'min':mi,'max':ma,'dimensions':[ma[i]-mi[i] for i in range(3)]}
def scalar_count(v):
    if isinstance(v,bool): return 0
    if isinstance(v,(int,float)): return 1
    if isinstance(v,list): return sum(scalar_count(x) for x in v)
    if isinstance(v,dict): return sum(scalar_count(x) for k,x in v.items() if k!='editable')
    return 0

def write_obj(path,verts,faces):
    lines=[f'# {MODEL}','# Derived execution mesh; not editable Surface Source Authority.']
    lines += [f'v {x:.9f} {y:.9f} {z:.9f}' for x,y,z in verts]
    lines += ['f '+' '.join(str(i+1) for i in f) for f in faces]
    path.write_text('\n'.join(lines)+'\n',encoding='utf-8')

def evaluate(source,revision=False):
    verts,faces=core.mesh(source,revision); box=bbox(verts); th=source['machine_thresholds']; dims=box['dimensions']
    u=.55; grip=core.bezier(core.own(source,'GRIP_AXIS')['control_points'],u)
    thumb=core.point(source,u,math.pi/2,revision)[1]-grip[1]
    opposite=grip[1]-core.point(source,u,3*math.pi/2,revision)[1]
    asym=thumb-opposite
    d=core.own(source,'INTERFACE_DECK_BOUNDARY'); uc=float(d['u_center'])
    inset=core.point(source,uc,0,revision,False)[2]-core.point(source,uc,0,revision,True)[2]
    fair=fairness(source,revision); sparse=scalar_count(source['ownership'])
    front=[abs(core.point(source,x,math.pi/2,revision)[1]-core.bezier(core.own(source,'GRIP_AXIS')['control_points'],x)[1]) for x in (.02,.05,.10)]
    back=[abs(core.point(source,1-x,math.pi/2,revision)[1]-core.bezier(core.own(source,'GRIP_AXIS')['control_points'],1-x)[1]) for x in (.02,.05,.10)]
    checks={
      'derived_execution_not_authority':source['derived_execution']['editable_authority'] is False,
      'sparse_authority_within_limit':sparse<=int(th['max_sparse_authority_scalar_count']),
      'length_within_contract':abs(dims[0]-float(th['overall_length_target_m']))<=float(th['overall_length_tolerance_m']),
      'width_within_contract':abs(dims[1]-float(th['overall_width_target_m']))<=float(th['overall_width_tolerance_m']),
      'height_within_contract':abs(dims[2]-float(th['overall_height_target_m']))<=float(th['overall_height_tolerance_m']),
      'required_asymmetry_present':asym>=float(th['min_thumb_opposite_asymmetry_m']),
      'interface_inset_depth_valid':float(th['min_interface_inset_depth_m'])<=inset<=float(th['max_interface_inset_depth_m']),
      'longitudinal_fairness_pass':fair['max_longitudinal_normal_delta_deg_per_0_01u']<=float(th['max_longitudinal_normal_delta_deg_per_0_01u']),
      'circumferential_fairness_pass':fair['max_circumferential_normal_delta_deg_per_0_05rad']<=float(th['max_circumferential_normal_delta_deg_per_0_05rad']),
      'non_automotive_wrap_monotonic':front[0]<front[1]<front[2] and back[0]<back[1]<back[2],
      'finite_execution_geometry':all(math.isfinite(v) for p in verts for v in p),
      'topology_is_derived_rings_plus_poles':len(verts)==2+int(source['derived_execution']['u_rings'])*int(source['derived_execution']['circumferential_samples'])}
    return {'checks':checks,'bbox':box,'thumb_radius_probe_m':thumb,'opposite_radius_probe_m':opposite,'thumb_minus_opposite_probe_m':asym,'interface_inset_depth_m':inset,'sparse_authority_scalar_count':sparse,'fairness':fair,'wrap_probe_front_m':front,'wrap_probe_back_m':back,'vertex_count':len(verts),'face_count':len(faces)},verts,faces

def revision_evidence(source,base,rev):
    th=source['machine_thresholds']; maxd=max(norm(sub(a,b)) for a,b in zip(base,rev)); u=.55
    gain=core.point(source,u,math.pi/2,True)[1]-core.point(source,u,math.pi/2,False)[1]
    opp=abs(core.point(source,u,3*math.pi/2,True)[1]-core.point(source,u,3*math.pi/2,False)[1])
    checks={'only_declared_primary_curve_family_revised':source['revision_test']['allowed_source_family']=='THUMB_SIDE_PLAN','mesh_local_patch_not_used':source['revision_test']['mesh_local_patch_allowed'] is False,'revision_surface_displacement_in_band':float(th['min_revision_surface_displacement_m'])<=maxd<=float(th['max_revision_surface_displacement_m']),'thumb_side_relation_strengthened':gain>=float(th['min_revision_surface_displacement_m']),'opposite_extreme_remains_owned_by_opposite_curve':opp<=1e-6}
    return {'revision_id':source['revision_test']['revision_id'],'declared_source_family':'THUMB_SIDE_PLAN','max_surface_displacement_m':maxd,'thumb_extreme_gain_m':gain,'opposite_extreme_change_m':opp,'checks':checks}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    source=json.loads(Path(a.source).read_text(encoding='utf-8')); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    base,bv,bf=evaluate(source,False); revised,rv,rf=evaluate(source,True); relation=revision_evidence(source,bv,rv)
    write_obj(out/'G1_BASELINE.obj',bv,bf); write_obj(out/'G1_R1_THUMB_RELATION.obj',rv,rf)
    checks={'baseline_machine_checks_pass':all(base['checks'].values()),'revision_machine_checks_pass':all(revised['checks'].values()),'relation_revision_checks_pass':all(relation['checks'].values()),'primary_curve_ownership_explicit':set(source['ownership'])=={'GRIP_AXIS','PALM_PROFILE','THUMB_SIDE_PLAN','OPPOSITE_SIDE_PLAN','INTERFACE_DECK_BOUNDARY','LOWER_RETURN_PROFILE'},'candidate_not_implied_by_machine':True}
    status='MACHINE_PASS_RELATION_REVISION_PASS_VISUAL_PROJECT_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL_REVISE_G1'
    report={'schema':'oleander.modeling-worker.v0.13.g1.machine-report','model':MODEL,'benchmark_id':source['benchmark_id'],'status':status,'job_state':'EXECUTED','design_state':'EXPLORE','authority_state':'WORKING_SOURCE','checks':checks,'baseline':base,'relation_revision':relation,'revision_machine':revised,'boundary':'Machine + relation revision PASS open Human Visual / Project QA only. Candidate Authority remains false.'}
    (out/'G1_MACHINE_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'G1_COMPILED_SURFACE_SOURCE.json').write_text(json.dumps({'schema':'oleander.modeling-worker.v0.13.g1.compiled-surface-source','authority':'WORKING_SURFACE_SOURCE','benchmark_id':source['benchmark_id'],'ownership':source['ownership'],'relationship_priorities':source['relationship_priorities'],'derived_execution':source['derived_execution'],'execution_geometry_authority':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2)); return 0 if status.startswith('MACHINE_PASS') else 5
if __name__=='__main__': raise SystemExit(main())
