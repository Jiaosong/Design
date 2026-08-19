#!/usr/bin/env python3
"""V42 — boolean greenhouse apertures + robust pre-aperture silhouette scan on V40 zero-fold hull.

V41 confirmed that deleting coarse host faces is not acceptable aperture construction. V42 returns to V40's
zero-fold primary skin, cuts continuous windshield/rear/side openings with exact boolean cutter volumes, and fills
them with the calibrated independent glass. SIDE silhouette is measured from the pre-aperture diagnostic skin using
a triangle/plane intersection scanner that handles edge crossings, exact vertices and coplanar terminal faces.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
V40=HERE/'run_reference_repro_v40.py';text=V40.read_text();marker='\nrun40()\n'
if marker not in text:raise SystemExit('V40 run marker missing')
outer={'__file__':str(V40),'__name__':'oleander_v42_declarations'};exec(compile(text.split(marker,1)[0],str(V40),'exec'),outer)
core=outer['ns'];v=outer['v'];env=outer['env'];PROFILE=outer['PROFILE'];metric=outer['metric'];G=outer['G'];lerp=outer['lerp'];base_build=outer['build40'];base_projection=outer['projection40'];base_regression=outer['regression40'];base_surface=outer['surface40'];base_patch=outer['patch40'];base_identity=v.build_identity
VIS=json.loads((HERE/'REFERENCE_VISUAL_HULL_TARGETS_992_2.json').read_text());SIDE=[(float(x),float(z)) for x,z in VIS['side']['top_silhouette_m']]
REV='V42_BOOLEAN_APERTURE_ROBUST_TERMINAL_SCAN'
v.REF='2025_992.2_CARRERA_BOOLEAN_APERTURE_V42';v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v42';v.REFERENCE_CONTRACT['reference_revision']=v.REF;v.REFERENCE_CONTRACT['candidate_revision']=REV;v.REFERENCE_CONTRACT['primary_form_method']='V40_ZERO_FOLD_SKIN_PLUS_EXACT_BOOLEAN_GREENHOUSE_APERTURES';v.REFERENCE_CONTRACT['side_scan_method']='PRE_APERTURE_EVALUATED_TRIANGLE_X_PLANE_INTERSECTION_INCLUDING_COPLANAR_TERMINALS';v.FAMILY_CONTROLS['BOOLEAN_APERTURE_V42']={'greenhouse':'REFERENCE_GREENHOUSE_TARGETS_992_2.json','side_cutter':'CALIBRATED_XZ_POLYGON_EXTRUDED_THROUGH_SIDE_SKIN','windshield_cutter':'CALIBRATED_QUAD_PRISM','rear_glass_cutter':'CALIBRATED_QUAD_PRISM','protected':['V40_PRE_APERTURE_ZERO_FOLD_SKIN','FRONT_PROFILE','REAR_PROFILE','SIDE_LOWER','WHEELBASE','AXLE_CENTRES']};v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

def make_y_prism(name,poly_xz,y0,y1):
    verts=[(x,y0,z) for x,z in poly_xz]+[(x,y1,z) for x,z in poly_xz];n=len(poly_xz);faces=[]
    faces.append(tuple(reversed(range(n))));faces.append(tuple(range(n,2*n)))
    for i in range(n):j=(i+1)%n;faces.append((i,j,n+j,n+i))
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.hide_render=True;return o

def make_x_prism(name,quad,depth=.20):
    # Extrude along X; adequate for the sloped front/rear glass cutter volumes.
    verts=[(x-depth,y,z) for x,y,z in quad]+[(x+depth,y,z) for x,y,z in quad];faces=[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.hide_render=True;return o

def apply_bool(body,cutter,name):
    bpy.context.view_layer.objects.active=body;body.select_set(True);mod=body.modifiers.new(name,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
    bpy.ops.object.modifier_apply(modifier=mod.name);body.select_set(False);bpy.data.objects.remove(cutter,do_unlink=True)

def cut_apertures(body):
    # Side polygon follows calibrated glass top/bottom envelope with a 12 mm opening tolerance.
    poly=[(x,zt+.012) for x,zt,zb in G]+[(x,zb-.012) for x,zt,zb in reversed(G)]
    apply_bool(body,make_y_prism('CUT_SIDE_R',poly,.30,1.20),'BOOL_SIDE_R')
    apply_bool(body,make_y_prism('CUT_SIDE_L',poly,-1.20,-.30),'BOOL_SIDE_L')
    ws=[(.650,.635,.815),(.650,-.635,.815),(.225,-.558,1.225),(.225,.558,1.225)]
    rg=[(-.380,.505,1.225),(-.380,-.505,1.225),(-1.165,-.610,.975),(-1.165,.610,.975)]
    apply_bool(body,make_x_prism('CUT_WINDSHIELD',ws,.16),'BOOL_WINDSHIELD')
    apply_bool(body,make_x_prism('CUT_REAR_GLASS',rg,.16),'BOOL_REAR_GLASS')
    body['OLEANDER_APERTURE_STAGE']='EXACT_BOOLEAN_HOST_OPENINGS_PLUS_INDEPENDENT_GLASS';body['OLEANDER_OPAQUE_HOST_THROUGH_GLAZING']=False

def build42(name,bodymat):
    o=base_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':cut_apertures(o);o['OLEANDER_FORM_FAMILY']='V40_ZERO_FOLD_SKIN_BOOLEAN_APERTURE_V42'
    return o
core['build_visual_hull']=build42

# Replace old bright half-buried headlamp modules with dark round lenses + four-point signature.
def identity42(M):
    out=base_identity(M)
    for name in list(bpy.data.objects.keys()):
        if name.startswith('REF_HEADLAMP_HOUSING_') or name.startswith('REF_HEADLAMP_LENS_') or name.startswith('REF_FRONT_CENTER_INTAKE') or name.startswith('REF_FRONT_SIDE_INTAKE_') or name.startswith('REF_FRONT_SPLITTER'):
            o=bpy.data.objects.get(name)
            if o:o.hide_render=True
    for side in (1,-1):
        h=v.m.add_uv_sphere('V42_HEADLAMP_RECESS_'+str(side),(1.795,side*.675,.770),(.055,.165,.165),M['body_dark']);h['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(h)
        l=v.m.add_uv_sphere('V42_HEADLAMP_LENS_'+str(side),(1.850,side*.675,.770),(.032,.148,.148),M['glass']);l['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DETAIL';out.append(l)
        for dy in (-.042,.042):
            for dz in (-.042,.042):
                px=v.m.add_cube(f'V42_HEADLAMP_PIXEL_{side}_{dy}_{dz}',(1.884,side*.675+dy,.770+dz),(.010,.018,.018),M['headlamp'],.004);px['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DETAIL';out.append(px)
    c=v.m.add_cube('V42_FRONT_CENTER_INTAKE',(2.205,0,.292),(.020,.390,.090),M['body_dark'],.035);out.append(c)
    for side in (1,-1):out.append(v.m.add_cube('V42_FRONT_SIDE_INTAKE_'+str(side),(2.185,side*.560,.305),(.022,.235,.125),M['body_dark'],.045))
    out.append(v.m.add_cube('V42_FRONT_SPLITTER',(2.205,0,.177),(.018,1.300,.018),M['body_dark'],.008));return out
v.build_identity=identity42

# Robust pre-aperture X-plane scanner. This is intentionally independent of Source target values.
def tri_plane_top(obj,xq):
    dg=bpy.context.evaluated_depsgraph_get();eo=obj.evaluated_get(dg);me=eo.to_mesh();me.calc_loop_triangles();vals=[];eps=1e-8
    try:
        for tri in me.loop_triangles:
            ps=[eo.matrix_world @ me.vertices[i].co for i in tri.vertices];xs=[p.x for p in ps]
            if xq<min(xs)-eps or xq>max(xs)+eps:continue
            for p in ps:
                if abs(p.x-xq)<=eps:vals.append(float(p.z))
            for a,b in ((ps[0],ps[1]),(ps[1],ps[2]),(ps[2],ps[0])):
                da=a.x-xq;db=b.x-xq
                if da*db<0:
                    t=(xq-a.x)/(b.x-a.x);vals.append(float(a.z+t*(b.z-a.z)))
                elif abs(da)<=eps and abs(db)<=eps:vals.extend([float(a.z),float(b.z)])
        return max(vals) if vals else float('nan')
    finally:eo.to_mesh_clear()

def projection42():
    d=base_projection();d['candidate_revision']=REV;d['primary_form_stage']='BOOLEAN_APERTURE_ROBUST_TERMINAL_SCAN';diag=bpy.data.objects.get('DIAG_PRE_APERTURE_VISUAL_HULL_V34');errs=[];samples=[]
    for x,z in SIDE:
        cand=tri_plane_top(diag,x) if diag else float('nan');e=cand-z if math.isfinite(cand) else float('nan');samples.append({'x':x,'target_top':z,'candidate_top':cand,'top_error_m':e,'reference_target_source':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m','candidate_measurement_source':'V42_PRE_APERTURE_EVALUATED_TRIANGLE_X_PLANE_INTERSECTION'});errs.append(e) if math.isfinite(e) else None
    rmse=math.sqrt(sum(e*e for e in errs)/len(errs)) if errs else 9.0;d['side_upper_samples']=samples
    for m in d['metrics']:
        if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M':m['candidate']=rmse;m['abs_error']=rmse;m['candidate_measurement_source']='V42_PRE_APERTURE_EVALUATED_TRIANGLE_X_PLANE_INTERSECTION';m['finite_sample_coverage']=len(errs)/len(SIDE)
        else:m['candidate_measurement_source']=str(m.get('candidate_measurement_source','')).replace('V40_','V42_')
    d['side_upper_finite_sample_coverage']=len(errs)/len(SIDE);d['side_terminal_semantics']='ROBUST_COPLANAR_AND_VERTEX_INTERSECTION_ON_PRE_APERTURE_SKIN';d['greenhouse_representation']='BOOLEAN_HOST_OPENINGS_PLUS_INDEPENDENT_GLASS';d['status']='PROJECTION_MACHINE_SCREENING_PASS' if len(errs)/len(SIDE)>=.90 and all(math.isfinite(float(m['abs_error'])) and float(m['abs_error'])<=float(m['limit']) for m in d['metrics']) else 'PROJECTION_MACHINE_SCREENING_FAIL';return d
env['projection30']=projection42

def regression42(pr):
    d=base_regression(pr);d['candidate_revision']=REV;d['edit_scope']=['BOOLEAN_GREENHOUSE_APERTURES','ROBUST_PRE_APERTURE_TERMINAL_SCAN','ROUND_DARK_HEADLAMP_INTEGRATION'];d['visual_review_state']='NOT_RUN'
    if d.get('promotion_decision')=='PROMOTE_OVER_LKG':d['promotion_decision']='KEEP_LKG_HOLD_EXPERIMENT'
    return d
env['regression30']=regression42

def surface42():d=base_surface();d['revision']=REV;return d
env['surface_receipt']=surface42

def patch42(out):
    base_patch(out)
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():
            d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='BOOLEAN_APERTURE_ROBUST_TERMINAL_SCAN';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
outer['patch40']=patch42

def run42():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:env['run30']()
    except SystemExit as e:patch42(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch42(out)
run42()
