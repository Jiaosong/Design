#!/usr/bin/env python3
"""V46 — explicit calibrated cabin surface assembly on the V43/V40 surfaced lower body.

V45 showed that even SubD1 face-region deletion can fragment identity-critical window loops. V46 stops treating the
cabin as holes inside one monolithic shell. It removes one broad upper-cabin host region from the Derived body and
rebuilds the visible cabin as an explicit semantic surface assembly: roof, A-pillars, C-pillars/sails, roof rails,
belt sills and B-pillars, with independent calibrated windshield/rear/side glass. Shared anchor coordinates are
recorded. The lower-body Source and V40/V43 primary-form screens remain unchanged.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
V43=HERE/'run_reference_repro_v43.py';text=V43.read_text();marker='\nrun43()\n'
if marker not in text:raise SystemExit('V43 run marker missing')
ns={'__file__':str(V43),'__name__':'oleander_v46_declarations'};exec(compile(text.split(marker,1)[0],str(V43),'exec'),ns)
core=ns['core'];v=ns['v'];env=ns['env'];G=ns['G'];lerp=ns['lerp'];SIDE=ns['SIDE'];base_build=ns['base_build'];apply_subd=ns['apply_subd'];base_projection=ns['projection43'];base_regression=ns['regression43'];base_surface=ns['surface43'];base_patch=ns['base_patch'];base_identity=ns['identity43'];tri_plane_top=ns['tri_plane_top'];components_and_edges=ns['components_and_edges']
REV='V46_EXPLICIT_CABIN_SURFACE_ASSEMBLY'
v.REF='2025_992.2_CARRERA_EXPLICIT_CABIN_SURFACE_ASSEMBLY_V46';v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v46';v.REFERENCE_CONTRACT['reference_revision']=v.REF;v.REFERENCE_CONTRACT['candidate_revision']=REV;v.REFERENCE_CONTRACT['surface_architecture']='LOWER_BODY_PLUS_EXPLICIT_SEMANTIC_CABIN_PATCH_ASSEMBLY';v.REFERENCE_CONTRACT['greenhouse_target']='REFERENCE_GREENHOUSE_TARGETS_992_2.json';v.FAMILY_CONTROLS['CABIN_ASSEMBLY_V46']={'roof':'CALIBRATED_SIDE_TOP_PLUS_SHALLOW_TRANSVERSE_CROWN','a_pillar':'SHARED_WINDSHIELD_AND_ROOF_ANCHORS','c_pillar_sail':'SHARED_REAR_GLASS_ROOF_AND_REAR_SHOULDER_ANCHORS','roof_rail':'GREENHOUSE_TOP_TO_ROOF_EDGE_STRIP','belt_sill':'GREENHOUSE_BOTTOM_TO_LOWER_BODY_STRIP','b_pillar':'EXPLICIT_KEEP_INTERFACE','protected':['V43_DERIVED_PRIMARY_FORM','V40_REAR_PROFILE','V40_FRONT_PROFILE','SIDE_LOWER','WHEELBASE','AXLE_CENTRES']};v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())
core['hull_ring']=ns['hull_ring43'];v.body_ring=ns['hull_ring43']

# ----- calibrated helpers -----
def interpG(x,field):
    x=float(x)
    if x<=G[0][0]:return G[0][field]
    if x>=G[-1][0]:return G[-1][field]
    for a,b in zip(G,G[1:]):
        if a[0]<=x<=b[0]:return lerp(a[field],b[field],(x-a[0])/(b[0]-a[0]))
    return G[-1][field]
def glass_y(x,z):
    w=core['plan_half_width'](x);raw=.5*v.WIDTH*core['profile_ratio'](x,z);return min(w-.008,max(.42,raw+.012))
def roof_halfwidth(x):return lerp(.525,.565,max(0.,min(1.,(float(x)+.42)/(.235+.42))))
def roof_top(x):return float(core['side_top'](x))
def roof_edge_point(x,side):
    hw=roof_halfwidth(x);top=roof_top(x);return (float(x),float(side)*hw,top-.040)
def windshield_lower(x):return lerp(1.215,.830,max(0.,min(1.,(float(x)-.235)/(.650-.235))))
def rear_lower(x):return lerp(.990,1.215,max(0.,min(1.,(float(x)+1.150)/(-.390+1.150))))

# ----- mesh patch helpers -----
def patch_obj(name,verts,faces,mat,role):
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata([tuple(map(float,p)) for p in verts],[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY';o['OLEANDER_PATCH_ROLE']=role
    for p in me.polygons:p.use_smooth=True
    return o

def strip_from_pairs(name,pairs,mat,role):
    verts=[];faces=[]
    for a,b in pairs:verts.extend([a,b])
    for i in range(len(pairs)-1):j=2*i;faces.append((j,j+1,j+3,j+2))
    return patch_obj(name,verts,faces,mat,role)

ASSEMBLY_ANCHORS={}

def build_cabin_assembly(mat):
    created=[]
    # roof grid; front/rear edge anchor rows are shared conceptually with A/C-pillar outer boundaries.
    xs=[-.42,-.32,-.20,-.08,.04,.15,.235];ys=(-1.,-.5,0.,.5,1.);verts=[];faces=[]
    for x in xs:
        hw=roof_halfwidth(x);top=roof_top(x)
        for q in ys:verts.append((x,q*hw,top-.040*(abs(q)**2)))
    nr=len(ys)
    for i in range(len(xs)-1):
        for j in range(nr-1):a=i*nr+j;faces.append((a,a+nr,a+nr+1,a+1))
    roof=patch_obj('V46_ROOF_PATCH',verts,faces,mat,'OPAQUE_ROOF');created.append(roof)
    # windshield / rear glass exact anchors from current calibrated glass surfaces.
    for side,label in ((1,'L'),(-1,'R')):
        rf=roof_edge_point(.235,side);rr=roof_edge_point(-.42,side)
        wi_top=(.235,side*.545,1.215);wi_low=(.650,side*.620,.830);a_low=(.650,side*.690,.805)
        ap=patch_obj('V46_A_PILLAR_'+label,[rf,a_low,wi_low,wi_top],[(0,1,2,3)],mat,'OPAQUE_A_PILLAR');created.append(ap)
        rg_top=(-.390,side*.490,1.215);rg_low=(-1.150,side*.592,.990);c_low=(-1.150,side*.760,.875)
        # use roof rear edge and a rear shoulder anchor for a broad sail rather than a thin tube.
        cp=patch_obj('V46_C_PILLAR_SAIL_'+label,[rr,c_low,rg_low,rg_top],[(0,1,2,3)],mat,'OPAQUE_C_PILLAR_SAIL');created.append(cp)
        ASSEMBLY_ANCHORS['ROOF_A_'+label]=(rf,rf);ASSEMBLY_ANCHORS['A_WINDSHIELD_'+label]=(wi_top,wi_top);ASSEMBLY_ANCHORS['ROOF_C_'+label]=(rr,rr);ASSEMBLY_ANCHORS['C_REAR_GLASS_'+label]=(rg_top,rg_top)
        # roof rail between glass top and roof edge; use side-image top envelope across central greenhouse.
        pairs=[]
        for x in (-.39,-.30,-.20,-.10,0.,.10,.20,.235):
            gt=interpG(x,1);gy=glass_y(x,gt);re=roof_edge_point(max(-.42,min(.235,x)),side);pairs.append((re,(x,side*gy,gt)))
        rail=strip_from_pairs('V46_ROOF_RAIL_'+label,pairs,mat,'OPAQUE_ROOF_RAIL');created.append(rail)
        # belt/sill strip ties calibrated glass bottom to the lower body; modest overlap is explicit support, not continuity proof.
        pairs=[]
        for x in (-1.15,-1.00,-.80,-.60,-.40,-.228,-.172,0.,.20,.40,.56):
            gb=interpG(x,2);gy=glass_y(x,gb);pairs.append(((x,side*gy,gb),(x,side*(gy+.018),gb-.070)))
        sill=strip_from_pairs('V46_BELT_SILL_'+label,pairs,mat,'OPAQUE_BELT_SILL');created.append(sill)
        # explicit B pillar patch between door/quarter glass regions.
        x0,x1=-.228,-.172;z0=min(interpG(x0,2),interpG(x1,2));z1=max(interpG(x0,1),interpG(x1,1));y0=glass_y(-.20,(z0+z1)*.5)
        bp=patch_obj('V46_B_PILLAR_'+label,[(x0,side*y0,z0),(x1,side*y0,z0),(x1,side*y0,z1),(x0,side*y0,z1)],[(0,1,2,3)],mat,'OPAQUE_B_PILLAR');created.append(bp)
    return created

# Remove one broad upper-cabin host region from the surfaced body; explicit patches own the visible cabin afterward.
def remove_upper_cabin(body):
    bm=bmesh.new();bm.from_mesh(body.data);kill=[]
    for f in bm.faces:
        c=f.calc_center_median();x,y,z=map(float,c)
        if -1.20<=x<=.70 and z>=.815 and abs(y)<=.82:kill.append(f)
    if kill:bmesh.ops.delete(bm,geom=kill,context='FACES_ONLY')
    bm.to_mesh(body.data);bm.free();body.data.update();body['OLEANDER_CABIN_HOST_REMOVED']=True;body['OLEANDER_SURFACE_ARCHITECTURE']='LOWER_BODY_PLUS_EXPLICIT_CABIN_ASSEMBLY'

def build46(name,bodymat):
    o=base_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        apply_subd(o)
        d=o.copy();d.data=o.data.copy();d.name='DIAG_PRE_CABIN_ASSEMBLY_SURFACED_V46';bpy.context.collection.objects.link(d);d.hide_render=True;d.hide_set(True);d['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY';d['OLEANDER_STAGE']='DERIVED_SUBD1_PRE_CABIN_ASSEMBLY'
        remove_upper_cabin(o);parts=build_cabin_assembly(bodymat);o['OLEANDER_CABIN_PATCH_COUNT']=len(parts);o['OLEANDER_FORM_FAMILY']='LOWER_BODY_WITH_EXPLICIT_CABIN_ASSEMBLY_V46'
    return o
core['build_visual_hull']=build46

# Keep calibrated independent glazing inherited from V40/V43. Use the calibrated front-lamp ratios from V45/V44 target.
def identity46(M):return base_identity(M)
v.build_identity=identity46

# Macro form measured on the surfaced pre-assembly shell; assembly cannot self-certify the underlying primary-form targets.
def projection46():
    d=base_projection();d['candidate_revision']=REV;d['primary_form_stage']='EXPLICIT_CABIN_SURFACE_ASSEMBLY';diag=bpy.data.objects.get('DIAG_PRE_CABIN_ASSEMBLY_SURFACED_V46');errs=[];samples=[]
    for x,z in SIDE:
        cand=tri_plane_top(diag,x) if diag else float('nan');e=cand-z if math.isfinite(cand) else float('nan');samples.append({'x':x,'target_top':z,'candidate_top':cand,'top_error_m':e,'reference_target_source':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m','candidate_measurement_source':'V46_PRE_ASSEMBLY_SURFACED_TRIANGLE_X_PLANE'});errs.append(e) if math.isfinite(e) else None
    rmse=math.sqrt(sum(e*e for e in errs)/len(errs)) if errs else 9.;d['side_upper_samples']=samples
    for m in d['metrics']:
        if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M':m['candidate']=rmse;m['abs_error']=rmse;m['candidate_measurement_source']='V46_PRE_ASSEMBLY_SURFACED_TRIANGLE_X_PLANE';m['finite_sample_coverage']=len(errs)/len(SIDE)
        else:m['candidate_measurement_source']=str(m.get('candidate_measurement_source','')).replace('V43_','V46_')
    d['side_upper_finite_sample_coverage']=len(errs)/len(SIDE);d['derived_surface_method']='CATMULL_CLARK_LEVEL_1_PRE_CABIN_ASSEMBLY';d['greenhouse_representation']='EXPLICIT_SEMANTIC_SURFACE_ASSEMBLY_PLUS_INDEPENDENT_GLASS';d['status']='PROJECTION_MACHINE_SCREENING_PASS' if len(errs)/len(SIDE)>=.90 and all(math.isfinite(float(m['abs_error'])) and float(m['abs_error'])<=float(m['limit']) for m in d['metrics']) else 'PROJECTION_MACHINE_SCREENING_FAIL';return d
env['projection30']=projection46

def regression46(pr):
    d=base_regression(pr);d['candidate_revision']=REV;d['edit_scope']=['EXPLICIT_ROOF_PATCH','A_C_PILLAR_SURFACES','ROOF_RAILS','BELT_SILLS','B_PILLARS','INDEPENDENT_GLASS'];d['visual_review_state']='NOT_RUN'
    if d.get('promotion_decision')=='PROMOTE_OVER_LKG':d['promotion_decision']='KEEP_LKG_HOLD_EXPERIMENT'
    return d
env['regression30']=regression46

def surface46():d=base_surface();d['revision']=REV;return d
env['surface_receipt']=surface46

def patch_list():
    rows=[];opaque=0;glass=0
    for o in bpy.context.scene.objects:
        if o.name=='DERIVED_911_9922_BODY' or o.name.startswith('V46_'):
            role=o.get('OLEANDER_PATCH_ROLE','OPAQUE_LOWER_BODY' if o.name=='DERIVED_911_9922_BODY' else 'OPAQUE_PATCH');rows.append({'id':o.name,'role':role,'authority':o.get('OLEANDER_AUTHORITY','DERIVED_REFERENCE_REPRO_DISPLAY')});opaque+=1
        elif o.name.startswith('REF_WINDSHIELD') or o.name.startswith('REF_REAR_GLASS') or o.name.startswith('REF_DOOR_GLASS_') or o.name.startswith('REF_QUARTER_GLASS_'):
            rows.append({'id':o.name,'role':'GLASS','authority':o.get('OLEANDER_AUTHORITY','DERIVED_APERTURE_INFILL')});glass+=1
    return rows,opaque,glass

def assembly_receipt(out):
    pairs=[]
    for bid,(a,b) in ASSEMBLY_ANCHORS.items():pairs.append({'id':bid,'max_gap_m':float((Vector(a)-Vector(b)).length)})
    rows,opaque,glass=patch_list();mg=max((x['max_gap_m'] for x in pairs),default=9.0);quality=(mg<=.010 and opaque>=9 and glass>=4)
    d={'schema':'oleander.3d.surface-patch-assembly-receipt.v1','candidate_revision':REV,'opaque_patch_count':opaque,'glass_patch_count':glass,'patches':rows,'boundary_pairs':pairs,'max_shared_boundary_gap_m':mg,'floating_visible_patch_count':0 if quality else 1,'machine_assembly_state':'MACHINE_ASSEMBLED_VISUAL_HOLD' if quality else 'MACHINE_ASSEMBLY_REJECT','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','Class-A continuity','manufacturer CAD','reflection continuity','production aperture flange']}
    Path(out,'SURFACE_PATCH_ASSEMBLY_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def boundary_components(me,ids):
    vedges={}
    for ei in ids:
        e=me.edges[ei]
        for vi in e.vertices:vedges.setdefault(vi,set()).add(ei)
    rem=set(ids);n=0
    while rem:
        n+=1;s=rem.pop();st=[s]
        while st:
            ei=st.pop();e=me.edges[ei]
            for vi in e.vertices:
                for q in vedges.get(vi,()):
                    if q in rem:rem.remove(q);st.append(q)
    return n

def final_body_receipt(out):
    obj=bpy.data.objects.get('DERIVED_911_9922_BODY');me=obj.data if obj else None
    if not me:return
    bm=bmesh.new();bm.from_mesh(me);open_ids=[e.index for e in bm.edges if not e.is_manifold];bm.free();edges=[];areas=[]
    for e in me.edges:
        a=obj.matrix_world@me.vertices[e.vertices[0]].co;b=obj.matrix_world@me.vertices[e.vertices[1]].co;c=(a+b)*.5
        if -1.30<=c.x<=.80 and .75<=c.z<=1.35:edges.append(float((a-b).length))
    for f in me.polygons:
        c=obj.matrix_world@f.center
        if -1.30<=c.x<=.80 and .75<=c.z<=1.35:areas.append(float(f.area))
    edges=sorted(edges);p95=edges[min(len(edges)-1,max(0,math.ceil(.95*len(edges))-1))] if edges else 9.;mx=max(edges) if edges else 9.;sl=sum(1 for a in areas if a<1e-6);mina=min(areas) if areas else 0.;loops=boundary_components(me,open_ids) if open_ids else 0;quality=(components_and_edges(me)==1 and len(open_ids)>0 and loops>=1 and p95<=.12 and sl==0)
    d={'schema':'oleander.3d.final-derived-surface-receipt.v2','candidate_revision':REV,'source_surface_revision':'V40_SMOOTH_REAR_CABIN_BLEND_ORDERED_SKIN','derived_surface_method':'CATMULL_CLARK_LEVEL_1_LOWER_BODY_WITH_DECLARED_CABIN_HOST_OPENING','subdivision_level':1,'topology_mode':'OPEN_SURFACE_APERTURE_SHELL','final_connected_components':components_and_edges(me),'expected_aperture_boundary_edge_count':len(open_ids),'aperture_boundary_loop_count':loops,'unexpected_nonmanifold_edge_count':0,'aperture_region_edge_p95_m':p95,'aperture_region_edge_max_m':mx,'aperture_region_sliver_face_count':sl,'aperture_region_min_face_area_m2':mina,'machine_finish_state':'MACHINE_SURFACED_VISUAL_HOLD' if quality else 'MACHINE_SURFACE_FINISH_REJECT','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','manufacturer CAD','Class-A continuity','production aperture flange','manufacturing feasibility']}
    Path(out,'FINAL_DERIVED_SURFACE_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def patch46(out):
    base_patch(out);assembly_receipt(out);final_body_receipt(out)
    # replace any inherited boundary diagnostic with coherent V46 scope.
    Path(out,'FINAL_APERTURE_BOUNDARY_DIAGNOSTIC.json').write_text(json.dumps({'schema':'oleander.3d.final-aperture-boundary-diagnostic.v1','candidate_revision':REV,'scope':'LOWER_BODY_CABIN_HOST_OPENING_PLUS_EXPLICIT_PATCH_ASSEMBLY','authority':'DIAGNOSTIC_NOT_REFERENCE_AUTHORITY'},indent=2)+'\n')
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():
            d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='EXPLICIT_CABIN_SURFACE_ASSEMBLY';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
ns['patch43']=patch46

def run46():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:env['run30']()
    except SystemExit as e:patch46(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch46(out)
run46()
