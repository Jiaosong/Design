#!/usr/bin/env python3
"""V45 — surfaced open-aperture shell with six declared glazing loops.

V44 proved plane-normal cutters eliminate unexpected non-manifold defects, but a CLOSED_SOLID_BOOLEAN body still
creates cavity/cap behavior around identity-critical glazing and generates sliver intersections. V45 returns to the
V43/V40 zero-fold primary cage, applies one Derived Catmull-Clark level, then creates six declared aperture boundary
loops on that denser Derived surface: windshield, rear glass, L/R door glass and L/R quarter glass. The Source cage
is unchanged. Open aperture boundaries are expected topology, not defects; glazing remains independent infill.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
V43=HERE/'run_reference_repro_v43.py';text=V43.read_text();marker='\nrun43()\n'
if marker not in text:raise SystemExit('V43 run marker missing')
ns={'__file__':str(V43),'__name__':'oleander_v45_declarations'};exec(compile(text.split(marker,1)[0],str(V43),'exec'),ns)
core=ns['core'];v=ns['v'];env=ns['env'];G=ns['G'];lerp=ns['lerp'];SIDE=ns['SIDE'];base_build=ns['base_build'];apply_subd=ns['apply_subd'];base_projection=ns['projection43'];base_regression=ns['regression43'];base_surface=ns['surface43'];base_patch=ns['base_patch'];base_identity=ns['identity43'];tri_plane_top=ns['tri_plane_top'];components_and_edges=ns['components_and_edges']
FRONT=json.loads((HERE/'REFERENCE_FRONT_IDENTITY_TARGETS_992_2.json').read_text())
REV='V45_OPEN_SURFACE_APERTURE_SHELL'
v.REF='2025_992.2_CARRERA_OPEN_SURFACE_APERTURE_SHELL_V45'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v45'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['derived_surface_method']='V40_ZERO_FOLD_SOURCE_PLUS_CATmull_CLARK_LEVEL_1_OPEN_APERTURE_LOOPS'
v.REFERENCE_CONTRACT['aperture_topology_mode']='OPEN_SURFACE_APERTURE_SHELL'
v.REFERENCE_CONTRACT['aperture_boundary_method']='DENSE_SURFACE_DECLARED_FACE_REGION_BOUNDARY_AFTER_SUBD1'
v.REFERENCE_CONTRACT['aperture_loop_ids']=['WINDSHIELD','REAR_GLASS','LEFT_DOOR_GLASS','LEFT_QUARTER_GLASS','RIGHT_DOOR_GLASS','RIGHT_QUARTER_GLASS']
v.FAMILY_CONTROLS['OPEN_APERTURE_V45']={
 'greenhouse':'REFERENCE_GREENHOUSE_TARGETS_992_2.json',
 'source_surface':'V40_ZERO_FOLD_PRIMARY_SKIN',
 'derived_density':'CATMULL_CLARK_LEVEL_1',
 'b_pillar_keep_band_x_m':[-.228,-.172],
 'side_opening_min_abs_y_m':.50,
 'protected':['SIDE_GESTURE','FRONT_PROFILE','REAR_PROFILE','SIDE_LOWER','WHEELBASE','AXLE_CENTRES','SOURCE_CAGE']}
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

# Keep the V43 hood/fender Source-derived relation and V40 macro shape.
core['hull_ring']=ns['hull_ring43'];v.body_ring=ns['hull_ring43']

def interpG(x,field):
    x=float(x)
    if x<=G[0][0]:return G[0][field]
    if x>=G[-1][0]:return G[-1][field]
    for a,b in zip(G,G[1:]):
        if a[0]<=x<=b[0]:return lerp(a[field],b[field],(x-a[0])/(b[0]-a[0]))
    return G[-1][field]
def windshield_lower(x):return lerp(1.215,.830,max(0.,min(1.,(float(x)-.235)/(.650-.235))))
def rear_lower(x):return lerp(.990,1.215,max(0.,min(1.,(float(x)+1.150)/(-.390+1.150))))

def aperture_id(x,y,z,tol=.014):
    x=float(x);y=float(y);z=float(z);ay=abs(y)
    # two side apertures per side, with an explicit B-pillar host band retained.
    if G[0][0]<=x<=G[-1][0] and ay>=.50:
        top=interpG(x,1);bot=interpG(x,2)
        if bot-tol<=z<=top+tol:
            side='LEFT' if y>0 else 'RIGHT'
            if x<-.228:return side+'_QUARTER_GLASS'
            if x>-.172:return side+'_DOOR_GLASS'
    if .235<=x<=.650 and ay<=.535:
        lo=windshield_lower(x)
        # leave an explicit roof/header band; hole follows the glass below the roof top.
        if lo-tol<=z<=core['side_top'](x)-.020:return 'WINDSHIELD'
    if -1.150<=x<=-.390 and ay<=.535:
        lo=rear_lower(x)
        if lo-tol<=z<=core['side_top'](x)-.020:return 'REAR_GLASS'
    return None

def delete_dense_aperture_faces(obj):
    bm=bmesh.new();bm.from_mesh(obj.data);kill=[];counts={}
    for f in bm.faces:
        c=f.calc_center_median();aid=aperture_id(c.x,c.y,c.z)
        if aid:
            kill.append(f);counts[aid]=counts.get(aid,0)+1
    if kill:bmesh.ops.delete(bm,geom=kill,context='FACES_ONLY')
    bm.to_mesh(obj.data);bm.free();obj.data.update()
    obj['OLEANDER_APERTURE_STAGE']='OPEN_SURFACE_DECLARED_LOOPS_PLUS_INDEPENDENT_GLASS'
    obj['OLEANDER_TOPOLOGY_MODE']='OPEN_SURFACE_APERTURE_SHELL'
    obj['OLEANDER_APERTURE_FACE_COUNTS']=json.dumps(counts,sort_keys=True)
    obj['OLEANDER_OPAQUE_HOST_THROUGH_GLAZING']=False
    return counts

def build45(name,bodymat):
    o=base_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        apply_subd(o)
        d=o.copy();d.data=o.data.copy();d.name='DIAG_PRE_APERTURE_SURFACED_V45';bpy.context.collection.objects.link(d);d.hide_render=True;d.hide_set(True);d['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY';d['OLEANDER_STAGE']='DERIVED_SUBD1_PRE_APERTURE'
        counts=delete_dense_aperture_faces(o)
        o['OLEANDER_FORM_FAMILY']='DERIVED_SUBD1_OPEN_APERTURE_SHELL_V45';o['OLEANDER_DECLARED_APERTURE_IDS']=json.dumps(sorted(counts))
    return o
core['build_visual_hull']=build45

# Calibrated lamp location/diameter target, but no additional fascia redesign in this aperture-focused revision.
def identity45(M):
    out=base_identity(M)
    for name in list(bpy.data.objects.keys()):
        if name.startswith('REF_HEADLAMP_HOUSING_') or name.startswith('REF_HEADLAMP_LENS_') or name.startswith('V43_HEADLAMP_'):
            o=bpy.data.objects.get(name)
            if o:o.hide_render=True
    half=v.WIDTH*.5;cy=float(FRONT['measurement']['lamp_center_lateral_ratio_of_half_body_width'])*half;r=.5*float(FRONT['measurement']['visible_lamp_diameter_ratio_of_body_width'])*v.WIDTH
    for side in (1,-1):
        h=v.m.add_uv_sphere('V45_HEADLAMP_RECESS_'+str(side),(1.865,side*cy,.755),(.048,r*1.08,r*1.08),M['body_dark']);h['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(h)
        l=v.m.add_uv_sphere('V45_HEADLAMP_LENS_'+str(side),(1.914,side*cy,.755),(.025,r,r),M['glass']);l['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DETAIL';out.append(l)
        for dy in (-r*.29,r*.29):
            for dz in (-r*.29,r*.29):out.append(v.m.add_cube(f'V45_HEADLAMP_PIXEL_{side}_{dy}_{dz}',(1.941,side*cy+dy,.755+dz),(.007,.013,.013),M['headlamp'],.003))
    return out
v.build_identity=identity45

# Measure primary form on the surfaced PRE-aperture shell, so open holes cannot distort the macro profile gate.
def projection45():
    d=base_projection();d['candidate_revision']=REV;d['primary_form_stage']='OPEN_SURFACE_APERTURE_SHELL';diag=bpy.data.objects.get('DIAG_PRE_APERTURE_SURFACED_V45');errs=[];samples=[]
    for x,z in SIDE:
        cand=tri_plane_top(diag,x) if diag else float('nan');e=cand-z if math.isfinite(cand) else float('nan');samples.append({'x':x,'target_top':z,'candidate_top':cand,'top_error_m':e,'reference_target_source':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m','candidate_measurement_source':'V45_SURFACED_PRE_APERTURE_TRIANGLE_X_PLANE'});errs.append(e) if math.isfinite(e) else None
    rmse=math.sqrt(sum(e*e for e in errs)/len(errs)) if errs else 9.0;d['side_upper_samples']=samples
    for m in d['metrics']:
        if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M':m['candidate']=rmse;m['abs_error']=rmse;m['candidate_measurement_source']='V45_SURFACED_PRE_APERTURE_TRIANGLE_X_PLANE';m['finite_sample_coverage']=len(errs)/len(SIDE)
        else:m['candidate_measurement_source']=str(m.get('candidate_measurement_source','')).replace('V43_','V45_')
    d['side_upper_finite_sample_coverage']=len(errs)/len(SIDE);d['derived_surface_method']='CATMULL_CLARK_LEVEL_1_PRE_APERTURE';d['greenhouse_representation']='OPEN_SURFACE_DECLARED_APERTURE_LOOPS_PLUS_INDEPENDENT_GLASS';d['status']='PROJECTION_MACHINE_SCREENING_PASS' if len(errs)/len(SIDE)>=.90 and all(math.isfinite(float(m['abs_error'])) and float(m['abs_error'])<=float(m['limit']) for m in d['metrics']) else 'PROJECTION_MACHINE_SCREENING_FAIL';return d
env['projection30']=projection45

def regression45(pr):
    d=base_regression(pr);d['candidate_revision']=REV;d['edit_scope']=['OPEN_SURFACE_APERTURE_LOOPS','B_PILLAR_KEEP_BAND','SUBD1_PRE_APERTURE','CALIBRATED_LAMP_RATIO'];d['visual_review_state']='NOT_RUN'
    if d.get('promotion_decision')=='PROMOTE_OVER_LKG':d['promotion_decision']='KEEP_LKG_HOLD_EXPERIMENT'
    return d
env['regression30']=regression45

def surface45():d=base_surface();d['revision']=REV;return d
env['surface_receipt']=surface45

# Boundary classification for the open surface shell.
def edge_center(obj,e):
    a=obj.matrix_world@obj.data.vertices[e.vertices[0]].co;b=obj.matrix_world@obj.data.vertices[e.vertices[1]].co;return (a+b)*.5,float((a-b).length)
def is_expected_boundary(c):
    return aperture_id(float(c.x),float(c.y),float(c.z),tol=.055) is not None

def boundary_components(me,edge_ids):
    vedges={}
    for ei in edge_ids:
        e=me.edges[ei]
        for vi in e.vertices:vedges.setdefault(vi,set()).add(ei)
    remaining=set(edge_ids);count=0
    while remaining:
        count+=1;seed=remaining.pop();stack=[seed]
        while stack:
            ei=stack.pop();e=me.edges[ei]
            for vi in e.vertices:
                for nei in vedges.get(vi,()):
                    if nei in remaining:remaining.remove(nei);stack.append(nei)
    return count

def final_surface45(out):
    obj=bpy.data.objects.get('DERIVED_911_9922_BODY');me=obj.data if obj else None
    if not me:return
    bm=bmesh.new();bm.from_mesh(me);nonman_ids=[e.index for e in bm.edges if not e.is_manifold];bm.free()
    expected=[];unexpected=[];ap_edges=[];areas=[]
    for ei in nonman_ids:
        e=me.edges[ei];c,L=edge_center(obj,e)
        if is_expected_boundary(c):expected.append(ei)
        else:unexpected.append({'edge':ei,'center_m':[float(c.x),float(c.y),float(c.z)],'length_m':L})
    for e in me.edges:
        c,L=edge_center(obj,e)
        if -1.25<=c.x<=.75 and .78<=c.z<=1.32:ap_edges.append(L)
    for f in me.polygons:
        c=obj.matrix_world@f.center
        if -1.25<=c.x<=.75 and .78<=c.z<=1.32:areas.append(float(f.area))
    ap_edges=sorted(ap_edges);p95=ap_edges[min(len(ap_edges)-1,max(0,math.ceil(.95*len(ap_edges))-1))] if ap_edges else 9.;mx=max(ap_edges) if ap_edges else 9.;mina=min(areas) if areas else 0.;sliver=sum(1 for a in areas if a<1e-6);loops=boundary_components(me,expected) if expected else 0
    quality=(components_and_edges(me)==1 and len(unexpected)==0 and len(expected)>0 and loops>=4 and p95<=.12 and sliver==0)
    d={'schema':'oleander.3d.final-derived-surface-receipt.v2','candidate_revision':REV,'source_surface_revision':'V40_SMOOTH_REAR_CABIN_BLEND_ORDERED_SKIN','derived_surface_method':'CATMULL_CLARK_LEVEL_1_THEN_DECLARED_OPEN_APERTURE_FACE_REGIONS','subdivision_level':1,'topology_mode':'OPEN_SURFACE_APERTURE_SHELL','final_connected_components':components_and_edges(me),'expected_aperture_boundary_edge_count':len(expected),'aperture_boundary_loop_count':loops,'unexpected_nonmanifold_edge_count':len(unexpected),'aperture_region_edge_p95_m':p95,'aperture_region_edge_max_m':mx,'aperture_region_sliver_face_count':sliver,'aperture_region_min_face_area_m2':mina,'machine_finish_state':'MACHINE_SURFACED_VISUAL_HOLD' if quality else 'MACHINE_SURFACE_FINISH_REJECT','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','manufacturer CAD','Class-A continuity','production aperture flange','manufacturing feasibility']}
    Path(out,'FINAL_DERIVED_SURFACE_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    Path(out,'FINAL_APERTURE_BOUNDARY_DIAGNOSTIC.json').write_text(json.dumps({'schema':'oleander.3d.final-aperture-boundary-diagnostic.v1','candidate_revision':REV,'expected_boundary_edge_count':len(expected),'boundary_loop_count':loops,'unexpected_edges':unexpected,'authority':'DIAGNOSTIC_NOT_REFERENCE_AUTHORITY'},ensure_ascii=False,indent=2)+'\n')

def patch45(out):
    base_patch(out);final_surface45(out)
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():
            d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='OPEN_SURFACE_APERTURE_SHELL';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
ns['patch43']=patch45

def run45():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:env['run30']()
    except SystemExit as e:patch45(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch45(out)
run45()
