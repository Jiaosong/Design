#!/usr/bin/env python3
"""V43 — Derived surface finish + boolean aperture boundary + front identity refinement.

V42 is the first candidate with SIDE/FRONT/REAR machine screening, zero pre-aperture folds and truthful CI success,
but six-view readback remains visually generic/faceted. V43 freezes V40/V42 hard points and rear mass. It adds a
small causal hood-valley / fender-crown relation in the Source-derived ring, applies one Catmull-Clark level to the
Derived display shell before aperture booleans, cuts continuous greenhouse openings on the surfaced shell, and
reduces/embeds the round headlamps toward same-revision front-image proportions. Source authority remains sparse;
SubD is Derived execution only.
"""
from __future__ import annotations
import json,math,statistics
from pathlib import Path
import bpy,bmesh
HERE=Path(__file__).resolve().parent
V40=HERE/'run_reference_repro_v40.py';text=V40.read_text();marker='\nrun40()\n'
if marker not in text:raise SystemExit('V40 run marker missing')
outer={'__file__':str(V40),'__name__':'oleander_v43_declarations'};exec(compile(text.split(marker,1)[0],str(V40),'exec'),outer)
core=outer['ns'];v=outer['v'];env=outer['env'];PROFILE=outer['PROFILE'];metric=outer['metric'];G=outer['G'];lerp=outer['lerp'];base_ring=outer['hull_ring40'];base_build=outer['build40'];base_projection=outer['projection40'];base_regression=outer['regression40'];base_surface=outer['surface40'];base_patch=outer['patch40'];base_identity=v.build_identity
VIS=json.loads((HERE/'REFERENCE_VISUAL_HULL_TARGETS_992_2.json').read_text());SIDE=[(float(x),float(z)) for x,z in VIS['side']['top_silhouette_m']]
REV='V43_DERIVED_SURFACE_FRONT_IDENTITY'
v.REF='2025_992.2_CARRERA_DERIVED_SURFACE_FRONT_IDENTITY_V43';v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v43';v.REFERENCE_CONTRACT['reference_revision']=v.REF;v.REFERENCE_CONTRACT['candidate_revision']=REV;v.REFERENCE_CONTRACT['primary_form_method']='V40_ZERO_FOLD_SOURCE_DERIVED_SUBD1_BOOLEAN_APERTURES';v.REFERENCE_CONTRACT['derived_surface_method']='CATMULL_CLARK_LEVEL_1_BEFORE_GREENHOUSE_BOOLEAN';v.REFERENCE_CONTRACT['source_authority_note']='SUBDIVISION_IS_DERIVED_EXECUTION_NOT_SOURCE_AUTHORITY';v.FAMILY_CONTROLS['FRONT_IDENTITY_V43']={'hood_valley':'CENTER_INNER_HOOD_LOWER_THAN_FENDER_CROWN','headlamp_center_y_m':.705,'headlamp_visible_radius_m':.118,'reference':'FRONT_9922.jpg same-revision front image, source-grounded visual estimate','protected':['V40_REAR_PROFILE','V40_ZERO_FOLD_SOURCE','SIDE_TOP_OUTER_RAIL','SIDE_LOWER','WHEELBASE','AXLE_CENTRES']};v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

# Small causal front section change only; outer SIDE rail is not moved.
def hull_ring43(x):
    ring=[list(p) for p in base_ring(x)];w=max(abs(p[1]) for p in ring) or 1.0
    fi=math.exp(-((float(x)-1.42)/.66)**4)
    if fi>.001:
        for p in ring:
            xe,y,z=p;q=abs(y)/w
            if z<.54:continue
            if q<.58:p[2]-=.040*fi*((1-q/.58)**1.45)
            elif .64<q<.94:
                bell=max(0.0,1-abs(q-.80)/.16);p[2]+=.014*fi*(bell**1.6)
    return [tuple(p) for p in ring]
core['hull_ring']=hull_ring43;v.body_ring=hull_ring43

# Continuous aperture cutters, sampled from the calibrated greenhouse envelope.
def make_y_prism(name,poly_xz,y0,y1):
    verts=[(x,y0,z) for x,z in poly_xz]+[(x,y1,z) for x,z in poly_xz];n=len(poly_xz);faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]
    for i in range(n):j=(i+1)%n;faces.append((i,j,n+j,n+i))
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.hide_render=True;return o
def make_x_prism(name,quad,depth=.20):
    verts=[(x-depth,y,z) for x,y,z in quad]+[(x+depth,y,z) for x,y,z in quad];faces=[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.hide_render=True;return o
def apply_bool(body,cutter,name):
    bpy.context.view_layer.objects.active=body;body.select_set(True);m=body.modifiers.new(name,'BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=cutter;bpy.ops.object.modifier_apply(modifier=m.name);body.select_set(False);bpy.data.objects.remove(cutter,do_unlink=True)
def cut_apertures(body):
    poly=[(x,zt+.010) for x,zt,zb in G]+[(x,zb-.010) for x,zt,zb in reversed(G)]
    apply_bool(body,make_y_prism('V43_CUT_SIDE_R',poly,.30,1.20),'V43_BOOL_SIDE_R');apply_bool(body,make_y_prism('V43_CUT_SIDE_L',poly,-1.20,-.30),'V43_BOOL_SIDE_L')
    ws=[(.650,.635,.815),(.650,-.635,.815),(.225,-.558,1.225),(.225,.558,1.225)];rg=[(-.380,.505,1.225),(-.380,-.505,1.225),(-1.165,-.610,.975),(-1.165,.610,.975)]
    apply_bool(body,make_x_prism('V43_CUT_WINDSHIELD',ws,.16),'V43_BOOL_WINDSHIELD');apply_bool(body,make_x_prism('V43_CUT_REAR_GLASS',rg,.16),'V43_BOOL_REAR_GLASS');body['OLEANDER_APERTURE_STAGE']='SURFACED_EXACT_BOOLEAN_PLUS_INDEPENDENT_GLASS';body['OLEANDER_OPAQUE_HOST_THROUGH_GLAZING']=False

def apply_subd(body):
    bpy.context.view_layer.objects.active=body;body.select_set(True);m=body.modifiers.new('V43_DERIVED_SUBD1','SUBSURF');m.subdivision_type='CATMULL_CLARK';m.levels=1;m.render_levels=1
    try:m.boundary_smooth='PRESERVE_CORNERS'
    except Exception:pass
    bpy.ops.object.modifier_apply(modifier=m.name);body.select_set(False);body['OLEANDER_DERIVED_SURFACE_METHOD']='CATMULL_CLARK_LEVEL_1';body['OLEANDER_SOURCE_AUTHORITY_CHANGED']=False

def build43(name,bodymat):
    o=base_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        apply_subd(o)
        d=o.copy();d.data=o.data.copy();d.name='DIAG_PRE_APERTURE_SURFACED_V43';bpy.context.collection.objects.link(d);d.hide_render=True;d.hide_set(True);d['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY';d['OLEANDER_STAGE']='DERIVED_SUBD_PRE_APERTURE'
        cut_apertures(o);o['OLEANDER_FORM_FAMILY']='DERIVED_SURFACED_BOOLEAN_APERTURE_HULL_V43'
    return o
core['build_visual_hull']=build43

# More proportionate round lamps; retain four-point signature but do not let detail rescue wrong primary form.
def identity43(M):
    out=base_identity(M)
    for name in list(bpy.data.objects.keys()):
        if name.startswith('REF_HEADLAMP_HOUSING_') or name.startswith('REF_HEADLAMP_LENS_') or name.startswith('REF_FRONT_CENTER_INTAKE') or name.startswith('REF_FRONT_SIDE_INTAKE_') or name.startswith('REF_FRONT_SPLITTER'):
            o=bpy.data.objects.get(name)
            if o:o.hide_render=True
    for side in (1,-1):
        h=v.m.add_uv_sphere('V43_HEADLAMP_RECESS_'+str(side),(1.800,side*.705,.755),(.050,.135,.135),M['body_dark']);h['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(h)
        l=v.m.add_uv_sphere('V43_HEADLAMP_LENS_'+str(side),(1.850,side*.705,.755),(.028,.118,.118),M['glass']);l['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DETAIL';out.append(l)
        for dy in (-.034,.034):
            for dz in (-.034,.034):out.append(v.m.add_cube(f'V43_HEADLAMP_PIXEL_{side}_{dy}_{dz}',(1.880,side*.705+dy,.755+dz),(.008,.014,.014),M['headlamp'],.003))
    out.append(v.m.add_cube('V43_FRONT_CENTER_INTAKE',(2.205,0,.292),(.020,.365,.082),M['body_dark'],.035))
    for side in (1,-1):out.append(v.m.add_cube('V43_FRONT_SIDE_INTAKE_'+str(side),(2.185,side*.555,.305),(.022,.220,.118),M['body_dark'],.045))
    out.append(v.m.add_cube('V43_FRONT_SPLITTER',(2.205,0,.177),(.018,1.260,.016),M['body_dark'],.008));return out
v.build_identity=identity43

# Robust X-plane triangle scan on the surfaced pre-aperture Derived shell.
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

def projection43():
    d=base_projection();d['candidate_revision']=REV;d['primary_form_stage']='DERIVED_SURFACE_FINAL_APERTURE';diag=bpy.data.objects.get('DIAG_PRE_APERTURE_SURFACED_V43');errs=[];samples=[]
    for x,z in SIDE:
        cand=tri_plane_top(diag,x) if diag else float('nan');e=cand-z if math.isfinite(cand) else float('nan');samples.append({'x':x,'target_top':z,'candidate_top':cand,'top_error_m':e,'reference_target_source':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m','candidate_measurement_source':'V43_SURFACED_PRE_APERTURE_TRIANGLE_X_PLANE'});errs.append(e) if math.isfinite(e) else None
    rmse=math.sqrt(sum(e*e for e in errs)/len(errs)) if errs else 9.0;d['side_upper_samples']=samples
    for m in d['metrics']:
        if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M':m['candidate']=rmse;m['abs_error']=rmse;m['candidate_measurement_source']='V43_SURFACED_PRE_APERTURE_TRIANGLE_X_PLANE';m['finite_sample_coverage']=len(errs)/len(SIDE)
        else:m['candidate_measurement_source']=str(m.get('candidate_measurement_source','')).replace('V40_','V43_')
    d['side_upper_finite_sample_coverage']=len(errs)/len(SIDE);d['derived_surface_method']='CATMULL_CLARK_LEVEL_1_BEFORE_BOOLEAN';d['greenhouse_representation']='SURFACED_BOOLEAN_HOST_OPENINGS_PLUS_INDEPENDENT_GLASS';d['status']='PROJECTION_MACHINE_SCREENING_PASS' if len(errs)/len(SIDE)>=.90 and all(math.isfinite(float(m['abs_error'])) and float(m['abs_error'])<=float(m['limit']) for m in d['metrics']) else 'PROJECTION_MACHINE_SCREENING_FAIL';return d
env['projection30']=projection43

def regression43(pr):
    d=base_regression(pr);d['candidate_revision']=REV;d['edit_scope']=['FRONT_HOOD_FENDER_CAUSAL_RELATION','DERIVED_SUBD1','SURFACED_BOOLEAN_APERTURES','HEADLAMP_PROPORTION'];d['visual_review_state']='NOT_RUN'
    if d.get('promotion_decision')=='PROMOTE_OVER_LKG':d['promotion_decision']='KEEP_LKG_HOLD_EXPERIMENT'
    return d
env['regression30']=regression43

def surface43():d=base_surface();d['revision']=REV;return d
env['surface_receipt']=surface43

# Final post-boolean / post-wheel-cut surface receipt; quality rejection is a valid evidence state.
def components_and_edges(me):
    adj={i:set() for i in range(len(me.vertices))}
    for e in me.edges:a,b=e.vertices;adj[a].add(b);adj[b].add(a)
    seen=set();comps=0
    for i in adj:
        if i in seen:continue
        comps+=1;stack=[i];seen.add(i)
        while stack:
            a=stack.pop()
            for b in adj[a]:
                if b not in seen:seen.add(b);stack.append(b)
    return comps

def final_surface_receipt(out):
    obj=bpy.data.objects.get('DERIVED_911_9922_BODY');me=obj.data if obj else None
    if not me:return
    bm=bmesh.new();bm.from_mesh(me);nonman=sum(1 for e in bm.edges if not e.is_manifold);bm.free()
    edges=[];areas=[]
    for e in me.edges:
        a=obj.matrix_world@me.vertices[e.vertices[0]].co;b=obj.matrix_world@me.vertices[e.vertices[1]].co;c=(a+b)*.5
        if -1.25<=c.x<=.75 and .78<=c.z<=1.32:edges.append(float((a-b).length))
    for f in me.polygons:
        c=obj.matrix_world@f.center
        if -1.25<=c.x<=.75 and .78<=c.z<=1.32:areas.append(float(f.area))
    edges=sorted(edges);p95=edges[min(len(edges)-1,max(0,math.ceil(.95*len(edges))-1))] if edges else 9.0;mx=max(edges) if edges else 9.0;mina=min(areas) if areas else 0.0;sliver=sum(1 for a in areas if a<1e-6)
    quality=(components_and_edges(me)==1 and nonman==0 and p95<=.12 and mx<=.25 and sliver==0)
    d={'schema':'oleander.3d.final-derived-surface-receipt.v1','candidate_revision':REV,'source_surface_revision':'V40_SMOOTH_REAR_CABIN_BLEND_ORDERED_SKIN','derived_surface_method':'CATMULL_CLARK_LEVEL_1_THEN_EXACT_BOOLEAN','subdivision_level':1,'final_connected_components':components_and_edges(me),'final_nonmanifold_edge_count':nonman,'aperture_region_edge_p95_m':p95,'aperture_region_edge_max_m':mx,'aperture_region_sliver_face_count':sliver,'aperture_region_min_face_area_m2':mina,'machine_finish_state':'MACHINE_SURFACED_VISUAL_HOLD' if quality else 'MACHINE_SURFACE_FINISH_REJECT','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','manufacturer CAD','Class-A continuity','production aperture flange','manufacturing feasibility']}
    Path(out,'FINAL_DERIVED_SURFACE_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def patch43(out):
    base_patch(out);final_surface_receipt(out)
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():
            d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='DERIVED_SURFACE_FINAL_APERTURE';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
outer['patch40']=patch43

def run43():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:env['run30']()
    except SystemExit as e:patch43(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch43(out)
run43()
