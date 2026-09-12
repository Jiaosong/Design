#!/usr/bin/env python3
"""V67 — diagnostic-only canonical rear-glass / side-glass boundary crossing audit.

V66 proved six evaluated host faces satisfy both rear-glass and side-glass owner predicates. V67 does not
resolve that ambiguity with predicate order or a guessed normal threshold. It binds the declared V60 rear-glass
infill footprint itself and asks whether candidate host faces lie wholly inside, wholly outside, or straddle the
rear-glass lateral boundary while also intersecting the rear-glass XZ cut band.

If a face straddles the canonical boundary, whole-face ownership is invalid: topology must be split/partitioned
before destructive deletion. Geometry is not mutated in this diagnostic.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V59=HERE/'run_reference_repro_v59.py'
text=V59.read_text(encoding='utf-8'); marker='\nrun59()\n'
if marker not in text: raise SystemExit('V59 run marker missing')
ns={'__file__':str(V59),'__name__':'oleander_v67_boundary_crossing'}
exec(compile(text.split(marker,1)[0],str(V59),'exec'),ns)

v=ns['v']; runtime=ns['runtime']
REV='V67_REAR_SIDE_CANONICAL_BOUNDARY_CROSSING_AUDIT'
ns['REV']=REV
v.REF='2025_992.2_CARRERA_REAR_SIDE_BOUNDARY_AUDIT_V67'
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['source_edit_scope']='NONE_DIAGNOSTIC_ONLY'
v.REFERENCE_CONTRACT['diagnostic_question']='DO_EVALUATED_HOST_FACES_STRADDLE_DECLARED_REAR_GLASS_LATERAL_BOUNDARY'

# V60 candidate canonical geometry. These are Derived reference-reproduction boundaries, not manufacturer CAD.
REAR_GLASS_TOP=(-.405,.455,1.220)
REAR_GLASS_BOTTOM=(-1.145,.535,.970)
REAR_CUTTER_XZ=[(-.405,1.220),(-1.145,.970),(-1.255,.900),(-.330,1.255)]


def point_in_poly(p,poly):
    x,z=p;inside=False;j=len(poly)-1
    for i in range(len(poly)):
        xi,zi=poly[i];xj,zj=poly[j]
        if ((zi>z)!=(zj>z)) and (x < (xj-xi)*(z-zi)/((zj-zi) or 1e-12)+xi):inside=not inside
        j=i
    return inside


def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def seg_intersect(a,b,c,d):
    eps=1e-10;o1=orient(a,b,c);o2=orient(a,b,d);o3=orient(c,d,a);o4=orient(c,d,b)
    return ((o1>eps and o2<-eps) or (o1<-eps and o2>eps)) and ((o3>eps and o4<-eps) or (o3<-eps and o4>eps))


def polygons_overlap(a,b):
    if any(point_in_poly(p,b) for p in a):return True
    if any(point_in_poly(p,a) for p in b):return True
    for i in range(len(a)):
        for j in range(len(b)):
            if seg_intersect(a[i],a[(i+1)%len(a)],b[j],b[(j+1)%len(b)]):return True
    return False


def rear_half_width(x):
    x=float(x);x0=REAR_GLASS_TOP[0];x1=REAR_GLASS_BOTTOM[0]
    if x>=x0:return REAR_GLASS_TOP[1]
    if x<=x1:return REAR_GLASS_BOTTOM[1]
    t=(x-x0)/(x1-x0)
    return REAR_GLASS_TOP[1]*(1-t)+REAR_GLASS_BOTTOM[1]*t


def audit(out):
    obj=bpy.data.objects.get('DIAG_FEATURE_ALIGNED_SURFACED_V59') or bpy.data.objects.get('DERIVED_911_9922_BODY')
    if obj is None:raise SystemExit('FAIL_V67_HOST_MISSING')
    mw=obj.matrix_world
    counts={'REAR_INTERIOR_ONLY':0,'REAR_LATERAL_BOUNDARY_STRADDLE':0,'OUTSIDE_REAR_LATERAL_BOUNDARY':0}
    samples=[]
    for poly in obj.data.polygons:
        pts=[mw@obj.data.vertices[i].co for i in poly.vertices]
        xz=[(float(p.x),float(p.z)) for p in pts]
        if not polygons_overlap(xz,REAR_CUTTER_XZ):continue
        c=mw@poly.center; limit=rear_half_width(float(c.x))
        ay=[abs(float(p.y)) for p in pts]
        amin=min(ay);amax=max(ay)
        if amax < limit-1e-9:
            state='REAR_INTERIOR_ONLY'
        elif amin > limit+1e-9:
            state='OUTSIDE_REAR_LATERAL_BOUNDARY'
        else:
            state='REAR_LATERAL_BOUNDARY_STRADDLE'
        counts[state]+=1
        if len(samples)<120:
            samples.append({
                'polygon_index':int(poly.index),'state':state,
                'center':[float(c.x),float(c.y),float(c.z)],
                'rear_half_width_at_center_x':limit,
                'face_abs_y_min':amin,'face_abs_y_max':amax,
                'face_vertices_world':[[float(p.x),float(p.y),float(p.z)] for p in pts]
            })
    straddles=counts['REAR_LATERAL_BOUNDARY_STRADDLE']
    interior=counts['REAR_INTERIOR_ONLY']
    if straddles>0:
        result='HOLD_TOPOLOGY_SPLIT_REQUIRED_BEFORE_OWNER_ASSIGNMENT'
        route='SPLIT_EVALUATED_OR_GENERATED_TOPOLOGY_ON_CANONICAL_REAR_GLASS_LATERAL_BOUNDARY_THEN_RERUN_PREFLIGHT'
    elif interior>0:
        result='PASS_REAR_OWNER_CAN_BE_EXCLUSIVE_ON_EXISTING_FACES'
        route='RERUN_MULTI_OWNER_PREFLIGHT_WITH_CANONICAL_REAR_WIDTH_PARTITION'
    else:
        result='FAIL_REAR_CANONICAL_FOOTPRINT_NOT_OWNED_BY_CURRENT_HOST_FACES'
        route='RECLASSIFY_HOST_OR_GREENHOUSE_REPRESENTATION'
    d={
      'schema':'oleander.3d.canonical-boundary-crossing-audit.v1',
      'candidate_revision':REV,'source_revision_locked':'V59_SPARSE_FRONT_HOOD_FENDER_RELATION',
      'host':'DIAG_FEATURE_ALIGNED_SURFACED_V59','host_state_class':'DERIVED_DIAGNOSTIC_NOT_AUTHORITY',
      'canonical_boundary_source':'V60_REAR_GLASS_DERIVED_INFILL_FOOTPRINT_NOT_MANUFACTURER_CAD',
      'rear_glass_top_xyz':REAR_GLASS_TOP,'rear_glass_bottom_xyz':REAR_GLASS_BOTTOM,
      'rear_cutter_xz_band':REAR_CUTTER_XZ,
      'classification_counts':counts,'whole_face_first_match_assignment_allowed':False,
      'geometry_mutated':False,'audit_result':result,'next_route':route,
      'sample_faces':samples,
      'does_not_prove':['manufacturer rear-glass boundary','correct production topology','aperture closure','reference fidelity','Class-A continuity','Design KEEP']
    }
    Path(out,'V67_CANONICAL_BOUNDARY_CROSSING_AUDIT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(d,indent=2));return d


def run67():
    a=v.m.parse_args();out=Path(a.out).resolve();code=0
    try:runtime['run30']()
    except SystemExit as e:code=e.code if isinstance(e.code,int) else 0
    audit(out);raise SystemExit(code)

run67()
