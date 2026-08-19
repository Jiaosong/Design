#!/usr/bin/env python3
"""V65 — diagnostic-only rear-glass host overlap audit on V59 LKG.

V63 preflight correctly blocked topology deletion because the rear-glass owner mask classified zero face
centroids. V65 does not widen the mask and does not edit geometry. It tests whether zero centroid hits mean:

A) the reference-derived rear-glass target truly does not intersect the current host representation; or
B) the centroid-only classifier is under-covering a real projected face/target overlap.

It compares centroid hits, vertex hits and projected polygon overlap on the evaluated V59 host.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V59=HERE/'run_reference_repro_v59.py'
text=V59.read_text(encoding='utf-8'); marker='\nrun59()\n'
if marker not in text: raise SystemExit('V59 run marker missing')
ns={'__file__':str(V59),'__name__':'oleander_v65_rear_glass_host_overlap'}
exec(compile(text.split(marker,1)[0],str(V59),'exec'),ns)

v=ns['v']; runtime=ns['runtime']
REV='V65_REAR_GLASS_HOST_OVERLAP_DIAGNOSTIC'
ns['REV']=REV
v.REF='2025_992.2_CARRERA_REAR_GLASS_HOST_OVERLAP_V65'
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['source_edit_scope']='NONE_DIAGNOSTIC_ONLY'
v.REFERENCE_CONTRACT['diagnostic_question']='REAR_GLASS_ZERO_CENTROID_HIT__HOST_MISMATCH_OR_CLASSIFIER_UNDERCOVERAGE'

TARGET=[(-.405,1.220),(-1.145,.970),(-1.255,.900),(-.330,1.255)]
YMIN=-.66; YMAX=.66


def point_in_poly(p, poly):
    x,z=p; inside=False; j=len(poly)-1
    for i in range(len(poly)):
        xi,zi=poly[i]; xj,zj=poly[j]
        cross=((zi>z)!=(zj>z)) and (x < (xj-xi)*(z-zi)/((zj-zi) or 1e-12)+xi)
        if cross: inside=not inside
        j=i
    return inside


def orient(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def seg_intersect(a,b,c,d):
    o1=orient(a,b,c);o2=orient(a,b,d);o3=orient(c,d,a);o4=orient(c,d,b)
    eps=1e-10
    return ((o1>eps and o2<-eps) or (o1<-eps and o2>eps)) and ((o3>eps and o4<-eps) or (o3<-eps and o4>eps))


def polygons_overlap(a,b):
    if any(point_in_poly(p,b) for p in a): return True
    if any(point_in_poly(p,a) for p in b): return True
    for i in range(len(a)):
        a1=a[i];a2=a[(i+1)%len(a)]
        for j in range(len(b)):
            b1=b[j];b2=b[(j+1)%len(b)]
            if seg_intersect(a1,a2,b1,b2): return True
    return False


def pseg_dist(p,a,b):
    px,pz=p; ax,az=a; bx,bz=b
    dx=bx-ax; dz=bz-az; den=dx*dx+dz*dz
    if den<1e-14: return math.hypot(px-ax,pz-az)
    t=max(0.0,min(1.0,((px-ax)*dx+(pz-az)*dz)/den))
    q=(ax+t*dx,az+t*dz)
    return math.hypot(px-q[0],pz-q[1])


def diagnostic(out):
    obj=bpy.data.objects.get('DIAG_FEATURE_ALIGNED_SURFACED_V59') or bpy.data.objects.get('DERIVED_911_9922_BODY')
    if obj is None: raise SystemExit('FAIL_V65_HOST_MISSING')
    mw=obj.matrix_world
    centroid_hits=0; vertex_hits=0; overlap_hits=0; overlap_y_hits=0
    overlap_faces=[]; all_vertices=[]
    for poly in obj.data.polygons:
        pts3=[mw @ obj.data.vertices[i].co for i in poly.vertices]
        xz=[(float(p.x),float(p.z)) for p in pts3]
        ys=[float(p.y) for p in pts3]
        c=mw @ poly.center
        y_overlap=max(ys)>=YMIN and min(ys)<=YMAX
        c_hit=point_in_poly((float(c.x),float(c.z)),TARGET) and YMIN<=float(c.y)<=YMAX
        v_hit=any(point_in_poly(q,TARGET) for q in xz) and y_overlap
        ov=polygons_overlap(xz,TARGET)
        if c_hit: centroid_hits+=1
        if v_hit: vertex_hits+=1
        if ov: overlap_hits+=1
        if ov and y_overlap:
            overlap_y_hits+=1
            overlap_faces.append({'polygon_index':int(poly.index),'center':[float(c.x),float(c.y),float(c.z)],'y_range':[min(ys),max(ys)]})
        all_vertices.extend(xz)
    nearest=[]
    for t in TARGET:
        nearest.append(min((pseg_dist(t,all_vertices[i],all_vertices[i]) for i in range(len(all_vertices))),default=float('inf')))
    # vertex-nearest distances are enough here to distinguish a broad carrier miss from a centroid-only miss.
    nearest_vertex=[]
    for t in TARGET:
        nearest_vertex.append(min((math.hypot(t[0]-p[0],t[1]-p[1]) for p in all_vertices),default=float('inf')))
    if overlap_y_hits>0 and centroid_hits==0:
        conclusion='CLASSIFIER_UNDERCOVERAGE_CENTROID_ONLY'
    elif overlap_y_hits==0:
        conclusion='TARGET_HOST_PROJECTED_OVERLAP_MISSING_OR_REPRESENTATION_MISMATCH'
    else:
        conclusion='CENTROID_CLASSIFIER_HAS_VALID_HITS'
    d={
        'schema':'oleander.3d.rear-glass-host-overlap-diagnostic.v1',
        'candidate_revision':REV,'source_revision_locked':'V59_SPARSE_FRONT_HOOD_FENDER_RELATION',
        'target_source':'REFERENCE_GREENHOUSE_TARGETS_992_2.json + declared rear-glass XZ boundary',
        'target_xz':TARGET,'target_y_interval':[YMIN,YMAX],
        'host':'DIAG_FEATURE_ALIGNED_SURFACED_V59','host_state_class':'DERIVED_DIAGNOSTIC_NOT_AUTHORITY',
        'centroid_hits':centroid_hits,'vertex_hits':vertex_hits,'projected_polygon_overlap_hits':overlap_hits,
        'projected_polygon_and_y_overlap_hits':overlap_y_hits,
        'nearest_target_vertex_to_host_vertex_xz_m':nearest_vertex,
        'sample_overlap_faces':overlap_faces[:24],
        'conclusion':conclusion,
        'geometry_mutated':False,
        'next_route':'REPLACE_CENTROID_MASK_WITH_VALIDATED_FACE_OVERLAP_CLASSIFIER' if conclusion=='CLASSIFIER_UNDERCOVERAGE_CENTROID_ONLY' else 'RESOLVE_REAR_GLASS_HOST_BOUNDARY_OR_PRIMARY_GREENHOUSE_RELATION_BEFORE_DELETION',
        'does_not_prove':['aperture closure','reference fidelity','Class-A continuity','Design KEEP','MAIN KEEP']
    }
    Path(out,'V65_REAR_GLASS_HOST_OVERLAP_DIAGNOSTIC.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(d,indent=2))
    return d


def run65():
    a=v.m.parse_args(); out=Path(a.out).resolve(); code=0
    try: runtime['run30']()
    except SystemExit as e: code=e.code if isinstance(e.code,int) else 0
    diagnostic(out)
    raise SystemExit(code)

run65()
