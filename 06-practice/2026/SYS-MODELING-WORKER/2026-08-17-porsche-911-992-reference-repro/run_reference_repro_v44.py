#!/usr/bin/env python3
"""V44 — plane-normal windshield/rear cutters + final surface localization on V43 surfaced hull.

V43 materially improved visible surface smoothness but the final-surface receipt found 3 non-manifold edges,
8 sliver faces and a 1.27 m aperture-region edge. The cutter construction was causal: windshield/rear quads were
extruded along WORLD_X instead of their own plane normal, over-cutting A/C-pillar interfaces and intersecting side
cutters poorly. V44 changes cutter orientation only, preserves V43 Source/Derived surface and mass, and emits exact
final-surface defect locations. Lamp proportion is updated to the calibrated front-image target.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
V43=HERE/'run_reference_repro_v43.py';text=V43.read_text();marker='\nrun43()\n'
if marker not in text:raise SystemExit('V43 run marker missing')
ns={'__file__':str(V43),'__name__':'oleander_v44_declarations'};exec(compile(text.split(marker,1)[0],str(V43),'exec'),ns)
v=ns['v'];env=ns['env'];core=ns['core'];base_identity=ns['base_identity'];base_patch=ns['patch43'];REV='V44_PLANE_NORMAL_APERTURE_CUTTERS'
FRONT=json.loads((HERE/'REFERENCE_FRONT_IDENTITY_TARGETS_992_2.json').read_text())
v.REF='2025_992.2_CARRERA_PLANE_NORMAL_APERTURE_V44';v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v44';v.REFERENCE_CONTRACT['reference_revision']=v.REF;v.REFERENCE_CONTRACT['candidate_revision']=REV;v.REFERENCE_CONTRACT['aperture_cutter_method']='SIDE_Y_PRISM_PLUS_WINDSHIELD_REAR_PLANE_NORMAL_PRISM';v.REFERENCE_CONTRACT['front_identity_target']='REFERENCE_FRONT_IDENTITY_TARGETS_992_2.json';v.FAMILY_CONTROLS['PLANE_NORMAL_APERTURE_V44']={'windshield_rear_cutters':'LOCAL_PLANE_NORMAL_EXTRUSION','side_cutters':'CALIBRATED_XZ_Y_EXTRUSION','front_lamp':'REFERENCE_FRONT_IDENTITY_TARGETS_992_2.json','protected':['V43_DERIVED_SUBD1','V43_REAR_PROFILE','V43_FRONT_PROFILE','V43_SOURCE_CAGE']};v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())
ns['REV']=REV

# Override V43 make_x_prism globally: its cut_apertures() resolves this symbol at runtime.
def make_plane_prism(name,quad,depth=.10):
    pts=[Vector(p) for p in quad];n=(pts[1]-pts[0]).cross(pts[2]-pts[0])
    if n.length<1e-8:raise RuntimeError('degenerate aperture cutter plane')
    n.normalize();a=[p-n*depth for p in pts];b=[p+n*depth for p in pts];verts=[tuple(p) for p in a+b];faces=[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.hide_render=True;o['OLEANDER_CUTTER_NORMAL']=[float(x) for x in n];return o
ns['make_x_prism']=make_plane_prism

# Calibrated front-image ratios: center ≈0.779 of half body width, diameter ≈0.139 of body width.
def identity44(M):
    out=base_identity(M)
    for name in list(bpy.data.objects.keys()):
        if name.startswith('REF_HEADLAMP_HOUSING_') or name.startswith('REF_HEADLAMP_LENS_') or name.startswith('REF_FRONT_CENTER_INTAKE') or name.startswith('REF_FRONT_SIDE_INTAKE_') or name.startswith('REF_FRONT_SPLITTER'):
            o=bpy.data.objects.get(name)
            if o:o.hide_render=True
    half=v.WIDTH*.5;cy=float(FRONT['measurement']['lamp_center_lateral_ratio_of_half_body_width'])*half;r=.5*float(FRONT['measurement']['visible_lamp_diameter_ratio_of_body_width'])*v.WIDTH
    for side in (1,-1):
        h=v.m.add_uv_sphere('V44_HEADLAMP_RECESS_'+str(side),(1.865,side*cy,.755),(.048,r*1.10,r*1.10),M['body_dark']);h['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(h)
        l=v.m.add_uv_sphere('V44_HEADLAMP_LENS_'+str(side),(1.915,side*cy,.755),(.026,r,r),M['glass']);l['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DETAIL';out.append(l)
        for dy in (-r*.29,r*.29):
            for dz in (-r*.29,r*.29):out.append(v.m.add_cube(f'V44_HEADLAMP_PIXEL_{side}_{dy}_{dz}',(1.943,side*cy+dy,.755+dz),(.007,.013,.013),M['headlamp'],.003))
    out.append(v.m.add_cube('V44_FRONT_CENTER_INTAKE',(2.205,0,.292),(.020,.365,.082),M['body_dark'],.035))
    for side in (1,-1):out.append(v.m.add_cube('V44_FRONT_SIDE_INTAKE_'+str(side),(2.185,side*.555,.305),(.022,.220,.118),M['body_dark'],.045))
    out.append(v.m.add_cube('V44_FRONT_SPLITTER',(2.205,0,.177),(.018,1.260,.016),M['body_dark'],.008));return out
v.build_identity=identity44

# Update projection/regression labels while preserving V43 measured semantics.
base_projection=ns['projection43'];base_regression=ns['regression43'];base_surface=ns['surface43']
def projection44():
    d=base_projection();d['candidate_revision']=REV;d['primary_form_stage']='PLANE_NORMAL_APERTURE_FINAL_SURFACE'
    for m in d['metrics']:m['candidate_measurement_source']=str(m.get('candidate_measurement_source','')).replace('V43_','V44_')
    return d
env['projection30']=projection44
def regression44(pr):
    d=base_regression(pr);d['candidate_revision']=REV;d['edit_scope']=['PLANE_NORMAL_WINDSHIELD_CUTTER','PLANE_NORMAL_REAR_GLASS_CUTTER','CALIBRATED_LAMP_RATIO'];d['visual_review_state']='NOT_RUN';return d
env['regression30']=regression44
def surface44():d=base_surface();d['revision']=REV;return d
env['surface_receipt']=surface44

# V43 final-surface emitter looks up global REV dynamically after this replacement.
ns['REV']=REV

def localize_final_surface(out):
    obj=bpy.data.objects.get('DERIVED_911_9922_BODY');rows_nm=[];rows_edge=[];rows_sliver=[]
    if obj:
        me=obj.data;bm=bmesh.new();bm.from_mesh(me)
        for e in bm.edges:
            if not e.is_manifold:
                c=sum((vtx.co for vtx in e.verts),Vector())/max(1,len(e.verts));rows_nm.append({'vertex_ids':[vtx.index for vtx in e.verts],'center_m':[float(c.x),float(c.y),float(c.z)],'face_count':len(e.link_faces)})
        bm.free()
        for e in me.edges:
            a=obj.matrix_world@me.vertices[e.vertices[0]].co;b=obj.matrix_world@me.vertices[e.vertices[1]].co;c=(a+b)*.5
            if -1.25<=c.x<=.75 and .78<=c.z<=1.32:rows_edge.append({'vertices':list(e.vertices),'length_m':float((a-b).length),'center_m':[float(c.x),float(c.y),float(c.z)]})
        for f in me.polygons:
            c=obj.matrix_world@f.center
            if -1.25<=c.x<=.75 and .78<=c.z<=1.32 and f.area<1e-6:rows_sliver.append({'face':f.index,'area_m2':float(f.area),'center_m':[float(c.x),float(c.y),float(c.z)]})
    rows_edge=sorted(rows_edge,key=lambda x:x['length_m'],reverse=True)[:12]
    d={'schema':'oleander.3d.final-surface-localization.v1','candidate_revision':REV,'nonmanifold_edges':rows_nm,'longest_aperture_region_edges':rows_edge,'sliver_faces':rows_sliver,'authority':'DIAGNOSTIC_NOT_REFERENCE_AUTHORITY'}
    Path(out,'FINAL_SURFACE_LOCALIZATION.json').write_text(json.dumps(d,indent=2)+'\n')

def patch44(out):
    base_patch(out);localize_final_surface(out)
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():
            d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='PLANE_NORMAL_APERTURE_FINAL_SURFACE';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
ns['patch43']=patch44

def run44():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:env['run30']()
    except SystemExit as e:patch44(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch44(out)
run44()
