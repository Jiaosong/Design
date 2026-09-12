#!/usr/bin/env python3
"""V66 — diagnostic-only aperture classifier ownership conflict audit.

V63 reported REAR_GLASS=0 because its first-match classifier evaluates SIDE before REAR.
V65 proved the rear target actually overlaps the evaluated V59 host (6 centroid hits, 112 projected+Y overlap faces).
V66 tests all owner predicates independently. A face matching multiple semantic owners is AMBIGUOUS; code order
is not allowed to assign physical ownership.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V59=HERE/'run_reference_repro_v59.py'
text=V59.read_text(encoding='utf-8'); marker='\nrun59()\n'
if marker not in text: raise SystemExit('V59 run marker missing')
ns={'__file__':str(V59),'__name__':'oleander_v66_aperture_owner_conflict'}
exec(compile(text.split(marker,1)[0],str(V59),'exec'),ns)

v=ns['v']; runtime=ns['runtime']; G=ns['ns']['G']
REV='V66_APERTURE_CLASSIFIER_OWNERSHIP_CONFLICT_AUDIT'
ns['REV']=REV
v.REF='2025_992.2_CARRERA_APERTURE_OWNER_AUDIT_V66'
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['source_edit_scope']='NONE_DIAGNOSTIC_ONLY'

WS=[(.625,.845),(.245,1.220),(.185,1.255),(.710,.775)]
RG=[(-.405,1.220),(-1.145,.970),(-1.255,.900),(-.330,1.255)]


def interpG(x,field):
    x=float(x)
    if x<=float(G[0][0]): return float(G[0][field])
    if x>=float(G[-1][0]): return float(G[-1][field])
    for a,b in zip(G,G[1:]):
        if float(a[0])<=x<=float(b[0]):
            den=float(b[0])-float(a[0]);t=0.0 if abs(den)<1e-12 else (x-float(a[0]))/den
            return float(a[field])*(1-t)+float(b[field])*t
    return float(G[-1][field])


def point_in_poly(p,poly):
    x,z=p;inside=False;j=len(poly)-1
    for i in range(len(poly)):
        xi,zi=poly[i];xj,zj=poly[j]
        if ((zi>z)!=(zj>z)) and (x < (xj-xi)*(z-zi)/((zj-zi) or 1e-12)+xi):inside=not inside
        j=i
    return inside


def owner_matches(x,y,z):
    out=[]
    if float(G[0][0])<=x<=float(G[-1][0]):
        zt=interpG(x,1);zb=interpG(x,2)
        if zb-.012<=z<=zt+.012 and y>=.34: out.append('BOUNDARY_SIDE_GLASS_L')
        if zb-.012<=z<=zt+.012 and y<=-.34: out.append('BOUNDARY_SIDE_GLASS_R')
    if abs(y)<=.67 and point_in_poly((x,z),WS): out.append('BOUNDARY_WINDSHIELD')
    if abs(y)<=.66 and point_in_poly((x,z),RG): out.append('BOUNDARY_REAR_GLASS')
    return out


def diagnostic(out):
    obj=bpy.data.objects.get('DIAG_FEATURE_ALIGNED_SURFACED_V59') or bpy.data.objects.get('DERIVED_911_9922_BODY')
    if obj is None: raise SystemExit('FAIL_V66_HOST_MISSING')
    mw=obj.matrix_world; normal_m= mw.to_3x3()
    single={}; conflict_sets={}; conflicts=[]; unmatched=0
    for poly in obj.data.polygons:
        c=mw @ poly.center
        matches=owner_matches(float(c.x),float(c.y),float(c.z))
        if not matches:
            unmatched+=1;continue
        if len(matches)==1:
            single[matches[0]]=single.get(matches[0],0)+1;continue
        key='|'.join(sorted(matches));conflict_sets[key]=conflict_sets.get(key,0)+1
        if len(conflicts)<80:
            n=(normal_m @ poly.normal).normalized()
            conflicts.append({
                'polygon_index':int(poly.index),'owners':matches,
                'center':[float(c.x),float(c.y),float(c.z)],
                'normal_world':[float(n.x),float(n.y),float(n.z)],
                'abs_normal_y':abs(float(n.y)),
                'abs_normal_xz':math.hypot(float(n.x),float(n.z))
            })
    total_conflicts=sum(conflict_sets.values())
    rear_side=[x for x in conflicts if 'BOUNDARY_REAR_GLASS' in x['owners'] and any('SIDE_GLASS' in o for o in x['owners'])]
    if rear_side:
        ny=[x['abs_normal_y'] for x in rear_side]
        normal_summary={'sample_count':len(rear_side),'abs_normal_y_min':min(ny),'abs_normal_y_max':max(ny),'abs_normal_y_mean':sum(ny)/len(ny)}
    else: normal_summary={'sample_count':0}
    d={
        'schema':'oleander.3d.aperture-classifier-ownership-audit.v1',
        'candidate_revision':REV,'source_revision_locked':'V59_SPARSE_FRONT_HOOD_FENDER_RELATION',
        'host':'DIAG_FEATURE_ALIGNED_SURFACED_V59','geometry_mutated':False,
        'single_owner_face_counts':single,'multi_owner_conflict_counts':conflict_sets,
        'multi_owner_face_count':total_conflicts,'unmatched_face_count':unmatched,
        'rear_side_conflict_normal_summary':normal_summary,'sample_conflicts':conflicts,
        'first_match_classifier_allowed':False,
        'audit_result':'FAIL_AMBIGUOUS_OWNER_MASKS' if total_conflicts else 'PASS_EXCLUSIVE_OWNER_MASKS',
        'next_route':'DEFINE_EXPLICIT_OWNER_DISAMBIGUATION_OR_SHARED_BOUNDARY_PARTITION_BEFORE_DESTRUCTIVE_EDIT' if total_conflicts else 'OWNER_MASKS_EXCLUSIVE__MAY_RETURN_TO_PREFLIGHT',
        'does_not_prove':['correct aperture partition','aperture closure','reference fidelity','Class-A continuity','Design KEEP']
    }
    Path(out,'V66_APERTURE_CLASSIFIER_OWNERSHIP_AUDIT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(d,indent=2))
    return d


def run66():
    a=v.m.parse_args();out=Path(a.out).resolve();code=0
    try:runtime['run30']()
    except SystemExit as e:code=e.code if isinstance(e.code,int) else 0
    diagnostic(out)
    raise SystemExit(code)

run66()
