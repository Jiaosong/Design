#!/usr/bin/env python3
"""V52 — semantic front-identity evidence adapter for V51 geometry.

Geometry delta: NONE. Candidate geometry remains V51_FRONT_TRANSVERSE_IDENTITY_REPAIR.

This adapter fixes an evidence bug: FRONT gross-profile RMSE cannot prove the semantic relation
"hood center lower than twin fender crowns". V52 adds a direct final-evaluated-surface section
measurement near the actual lamp X and records lamp placement/diameter screening separately.
The lamp-host/aperture architecture itself remains HOLD and is not promoted from proxy geometry.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V51=HERE/'run_reference_repro_v51.py'
text=V51.read_text();marker='\nrun51()\n'
if marker not in text: raise SystemExit('V51 run marker missing')
ctx={'__file__':str(V51),'__name__':'oleander_v52_evidence_adapter'}
exec(compile(text.split(marker,1)[0],str(V51),'exec'),ctx)

v=ctx['v'];runtime=ctx['runtime'];patch51=ctx['patch51'];evaluated_mesh_data=ctx['evaluated_mesh_data'];FRONT_ID=ctx['FRONT_ID']
base_projection=runtime['projection30']
EVIDENCE_REV='V52_SEMANTIC_FRONT_IDENTITY_EVIDENCE'


def x_plane_points(tri,x):
    pts=[]
    for i in range(3):
        x1,y1,z1=tri[i];x2,y2,z2=tri[(i+1)%3]
        if abs(x2-x1)<1e-12:
            if abs(x-x1)<1e-8:pts.extend(((y1,z1),(y2,z2)))
            continue
        if x<min(x1,x2)-1e-9 or x>max(x1,x2)+1e-9:continue
        t=(x-x1)/(x2-x1)
        if -1e-9<=t<=1+1e-9:pts.append((y1+t*(y2-y1),z1+t*(z2-z1)))
    return pts

def max_z_band(points,center,halfspan):
    vals=[z for y,z in points if abs(y-center)<=halfspan]
    return max(vals) if vals else float('nan')

def projection52():
    d=base_projection()
    d['evidence_revision']=EVIDENCE_REV
    d['geometry_revision_unchanged']='V51_FRONT_TRANSVERSE_IDENTITY_REPAIR'
    body='DIAG_FRONT_IDENTITY_FEATURE_GRID_V51';tris=evaluated_mesh_data(body)
    lamps=[bpy.data.objects.get('REF_HEADLAMP_LENS_1'),bpy.data.objects.get('REF_HEADLAMP_LENS_-1')]
    if not all(lamps):
        d['front_identity_metrics']={'semantic_relation_state':'HOLD','reason':'HEADLAMP_SEMANTIC_OBJECTS_MISSING','does_not_prove':['hood-fender hierarchy','lamp host integration']}
        return d
    lamp_x=sum(float(o.location.x) for o in lamps)/2.0
    lamp_y=[float(o.location.y) for o in lamps]
    section=[]
    for tri in tris:
        if lamp_x<min(p[0] for p in tri)-1e-9 or lamp_x>max(p[0] for p in tri)+1e-9:continue
        section.extend(x_plane_points(tri,lamp_x))
    hood=max_z_band(section,0.0,.18)
    crowns=[max_z_band(section,y,.15) for y in lamp_y]
    crown_mean=sum(crowns)/2 if all(math.isfinite(z) for z in crowns) else float('nan')
    delta=crown_mean-hood if math.isfinite(crown_mean) and math.isfinite(hood) else float('nan')
    target_lat=float(FRONT_ID['measurement']['lamp_center_lateral_ratio_of_half_body_width'])
    target_dia=float(FRONT_ID['measurement']['visible_lamp_diameter_ratio_of_body_width'])
    actual_lat=sum(abs(y) for y in lamp_y)/2.0/(.5*v.WIDTH)
    actual_dia=sum(max(float(o.dimensions.y),float(o.dimensions.z)) for o in lamps)/2.0/v.WIDTH
    lat_err=abs(actual_lat-target_lat);dia_err=abs(actual_dia-target_dia)
    hierarchy_ok=math.isfinite(delta) and delta>=.005
    lat_ok=lat_err<=.04;dia_ok=dia_err<=.02
    sem='SCREENED' if hierarchy_ok else ('FAIL' if math.isfinite(delta) else 'HOLD')
    d['front_identity_metrics']={
        'schema':'oleander.3d.front-semantic-identity-metric.v1',
        'source':'REFERENCE_FRONT_IDENTITY_TARGETS_992_2.json',
        'candidate_geometry_revision':'V51_FRONT_TRANSVERSE_IDENTITY_REPAIR',
        'evidence_revision':EVIDENCE_REV,
        'evaluated_carrier':body,
        'section_x_m':lamp_x,
        'hood_center_top_z_m':hood,
        'left_fender_crown_z_m':crowns[0],
        'right_fender_crown_z_m':crowns[1],
        'mean_fender_crown_minus_hood_m':delta,
        'hood_fender_min_positive_delta_m':.005,
        'hood_fender_hierarchy_state':'SCREENED' if hierarchy_ok else ('FAIL' if math.isfinite(delta) else 'HOLD'),
        'lamp_center_lateral_ratio_target':target_lat,
        'lamp_center_lateral_ratio_candidate':actual_lat,
        'lamp_center_lateral_ratio_abs_error':lat_err,
        'lamp_center_lateral_ratio_screen':'SCREENED' if lat_ok else 'FAIL',
        'lamp_visible_diameter_ratio_target':target_dia,
        'lamp_visible_diameter_ratio_candidate':actual_dia,
        'lamp_visible_diameter_ratio_abs_error':dia_err,
        'lamp_visible_diameter_ratio_screen':'SCREENED' if dia_ok else 'FAIL',
        'semantic_relation_state':sem,
        'lamp_host_integration_state':'HOLD_APERTURE_ARCHITECTURE_NOT_CONSTRUCTED',
        'lower_fascia_subordination_state':'HOLD_VISUAL_REVIEW_REQUIRED',
        'does_not_prove':['full lamp-host integration','exact lamp package','Class-A continuity','reference fidelity','homologation']
    }
    return d

runtime['projection30']=projection52

def run52():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:runtime['run30']()
    except SystemExit as e:
        patch51(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch51(out)
run52()
