#!/usr/bin/env python3
"""V59 — sparse Source front-identity edit on the V49 no-fold LKG.

Geometry basis: V49 feature-aligned Source network.
Only Source edit family: FRONT_HOOD_FENDER_RELATION.
No profile inversion. No cage midpoint densification. No cabin-blend rewrite. No rear edit.

Goal: test whether a direct hood-center vs twin-fender-crown relation improves the front identity while
preserving the V49 fold-free evaluated surface. Machine execution/evidence remains separate from
held-out front/rear 3/4 reference fidelity and Design Quality.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V49=HERE/'run_reference_repro_v49.py'
text=V49.read_text(); marker='\nrun49()\n'
if marker not in text: raise SystemExit('V49 run marker missing')
ns={'__file__':str(V49),'__name__':'oleander_v59_sparse_front_identity'}
exec(compile(text.split(marker,1)[0],str(V49),'exec'),ns)

v=ns['v'];core=ns['core'];runtime=ns['runtime'];base_ring=ns['feature_ring49'];base_build=ns['base_build'];apply_subd=ns['apply_subd']
SIDE=ns['SIDE'];PROFILE=ns['PROFILE'];FRONT_ID=ns['FRONT_ID'];tri_plane_top=ns['tri_plane_top'];evaluated_mesh_data=ns['evaluated_mesh_data'];z_plane_points=ns['z_plane_points'];lerp=ns['lerp'];RAILS=ns['RAILS']
REV='V59_SPARSE_FRONT_HOOD_FENDER_RELATION'
ns['REV']=REV
v.REF='2025_992.2_CARRERA_SPARSE_FRONT_IDENTITY_V59'
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['representation_state']='V49_FEATURE_NETWORK_SPARSE_CAUSAL_EDIT'
v.REFERENCE_CONTRACT['source_edit_scope']='FRONT_HOOD_FENDER_RELATION_ONLY'
v.REFERENCE_CONTRACT['forbidden_deltas']=['PROFILE_INVERSION','CAGE_DENSIFICATION','CABIN_BLEND_REWRITE','REAR_EDIT']
v.FAMILY_CONTROLS['FRONT_HOOD_FENDER_RELATION_V59']={
  'owner':'TIER_A_FRONT_IDENTITY',
  'hood_center_drop_max_m':.020,
  'fender_crown_target_offset_from_side_top_m':[-.004,-.008],
  'x_center_m':1.48,
  'x_falloff_m':.62,
  'protected':['V49_Y_RELATIONS','V49_TERMINAL_PLAN','V49_LOWER_RETURN','REAR','HARD_POINTS','AXLES','WHEELS'],
  'rollback':'V49_FEATURE_ALIGNED_CURVE_NETWORK'
}
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

def ring59(x):
    full=base_ring(x);half=[list(p) for p in full[:11]]
    w=math.exp(-((float(x)-1.48)/.62)**4)
    if w>.0001:
        top=core['side_top'](x)
        half[0][2]-=.020*w
        half[3][2]=lerp(half[3][2],top-.004,.82*w)
        half[4][2]=lerp(half[4][2],top-.008,.86*w)
        half[5][2]=min(half[5][2],top-.010)
    return [tuple(p) for p in half]+[(px,-py,pz) for px,py,pz in reversed(half[1:-1])]
core['hull_ring']=ring59;v.body_ring=ring59

def build59(name,bodymat):
    o=base_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        apply_subd(o)
        d=o.copy();d.data=o.data.copy();d.name='DIAG_FEATURE_ALIGNED_SURFACED_V59';bpy.context.collection.objects.link(d);d.hide_render=True;d.hide_set(True)
        d['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY';d['OLEANDER_DIAGNOSTIC_ROLE']='FINAL_EVALUATED_V59_FRONT_IDENTITY'
        o['OLEANDER_FORM_FAMILY']='V49_FEATURE_NETWORK_PLUS_FRONT_HOOD_FENDER_RELATION';o['OLEANDER_SOURCE_RING_CONTROLS']=len(ring59(0.0));o['OLEANDER_SOURCE_EDIT_SCOPE']='FRONT_HOOD_FENDER_RELATION_ONLY'
    return o
core['build_visual_hull']=build59

Z0=.140;ZR=v.HEIGHT-Z0

def profile_rmse(tris,profile,which):
    errs=[];samples=[]
    for frac,target in profile:
        z=Z0+float(frac)*ZR;pts=[]
        for tri in tris:
            if z<min(p[2] for p in tri)-1e-9 or z>max(p[2] for p in tri)+1e-9:continue
            for xx,yy in z_plane_points(tri,z):
                if which=='front' and xx>=.55:pts.append((xx,yy))
                elif which=='rear' and xx<=-.55:pts.append((xx,yy))
        cand=max((abs(yy) for _,yy in pts),default=float('nan'))/(.5*v.WIDTH);err=cand-float(target) if math.isfinite(cand) else float('nan')
        samples.append({'height_fraction':frac,'target_half_width_ratio':target,'candidate_half_width_ratio':cand,'error':err})
        if math.isfinite(err):errs.append(err)
    return math.sqrt(sum(e*e for e in errs)/len(errs)),samples,len(errs)/len(profile)

def x_plane_points(tri,x):
    pts=[]
    for i in range(3):
        x1,y1,z1=tri[i];x2,y2,z2=tri[(i+1)%3]
        if abs(x2-x1)<1e-12:continue
        if x<min(x1,x2)-1e-9 or x>max(x1,x2)+1e-9:continue
        t=(x-x1)/(x2-x1)
        if -1e-9<=t<=1+1e-9:pts.append((y1+t*(y2-y1),z1+t*(z2-z1)))
    return pts

def semantic_front59(tris):
    lamps=[bpy.data.objects.get('REF_HEADLAMP_LENS_1'),bpy.data.objects.get('REF_HEADLAMP_LENS_-1')]
    if not all(lamps):return {'semantic_relation_state':'HOLD','reason':'HEADLAMP_SEMANTIC_OBJECTS_MISSING'}
    lx=sum(float(o.location.x) for o in lamps)/2.;lys=[float(o.location.y) for o in lamps];pts=[]
    for tri in tris:
        if min(p[0] for p in tri)-1e-9<=lx<=max(p[0] for p in tri)+1e-9:pts.extend(x_plane_points(tri,lx))
    def mz(c,h):
        z=[zz for yy,zz in pts if abs(yy-c)<=h];return max(z) if z else float('nan')
    hood=mz(0,.18);crowns=[mz(y,.15) for y in lys];mean=sum(crowns)/2 if all(math.isfinite(z) for z in crowns) else float('nan');delta=mean-hood if math.isfinite(mean) and math.isfinite(hood) else float('nan')
    lat=sum(abs(y) for y in lys)/2/(.5*v.WIDTH);target_lat=float(FRONT_ID['measurement']['lamp_center_lateral_ratio_of_half_body_width']);dia=sum(max(float(o.dimensions.y),float(o.dimensions.z)) for o in lamps)/2/v.WIDTH;target_dia=float(FRONT_ID['measurement']['visible_lamp_diameter_ratio_of_body_width'])
    state='SCREENED' if math.isfinite(delta) and delta>=.005 else ('FAIL' if math.isfinite(delta) else 'HOLD')
    return {'schema':'oleander.3d.front-semantic-identity-metric.v1','source':'REFERENCE_FRONT_IDENTITY_TARGETS_992_2.json','candidate_geometry_revision':REV,'evaluated_carrier':'DIAG_FEATURE_ALIGNED_SURFACED_V59','section_x_m':lx,'hood_center_top_z_m':hood,'left_fender_crown_z_m':crowns[0],'right_fender_crown_z_m':crowns[1],'mean_fender_crown_minus_hood_m':delta,'hood_fender_min_positive_delta_m':.005,'hood_fender_hierarchy_state':state,'lamp_center_lateral_ratio_target':target_lat,'lamp_center_lateral_ratio_candidate':lat,'lamp_center_lateral_ratio_abs_error':abs(lat-target_lat),'lamp_visible_diameter_ratio_target':target_dia,'lamp_visible_diameter_ratio_candidate':dia,'lamp_visible_diameter_ratio_abs_error':abs(dia-target_dia),'semantic_relation_state':state,'lamp_host_integration_state':'HOLD_APERTURE_ARCHITECTURE_NOT_CONSTRUCTED','lower_fascia_subordination_state':'HOLD_VISUAL_REVIEW_REQUIRED','does_not_prove':['full lamp-host integration','reference fidelity','Class-A continuity']}

def projection59():
    diag=bpy.data.objects.get('DIAG_FEATURE_ALIGNED_SURFACED_V59');tris=evaluated_mesh_data('DIAG_FEATURE_ALIGNED_SURFACED_V59')
    side=[];errs=[]
    for x,z in SIDE:
        cand=tri_plane_top(diag,x);e=cand-z if math.isfinite(cand) else float('nan');side.append({'x':x,'target_top':z,'candidate_top':cand,'top_error_m':e});
        if math.isfinite(e):errs.append(e)
    sr=math.sqrt(sum(e*e for e in errs)/len(errs));fr,fs,fc=profile_rmse(tris,PROFILE['front']['profile'],'front');rr,rs,rc=profile_rmse(tris,PROFILE['rear']['profile'],'rear')
    metrics=[{'id':'SIDE_UPPER_EVALUATED_MESH_RMSE_M','target':0.,'candidate':sr,'abs_error':sr,'limit':.040,'candidate_measurement_source':'V59_FINAL_EVALUATED_XZ'},{'id':'FRONT_BODY_ONLY_PROFILE_RMSE','target':0.,'candidate':fr,'abs_error':fr,'limit':.100,'candidate_measurement_source':'V59_BODY_ONLY_YZ','measurement_role':'BODY_ONLY_DIAGNOSTIC_NOT_WHOLE_VISIBLE_FIDELITY'},{'id':'REAR_BODY_ONLY_PROFILE_RMSE','target':0.,'candidate':rr,'abs_error':rr,'limit':.110,'candidate_measurement_source':'V59_BODY_ONLY_YZ','measurement_role':'BODY_ONLY_DIAGNOSTIC_NOT_WHOLE_VISIBLE_FIDELITY'}]
    return {'schema':'oleander.3d.v59-sparse-front-identity-projection.v1','candidate_revision':REV,'reference_revision':v.REF,'status':'MACHINE_SCREENING_RECORDED_NOT_REFERENCE_PASS','source_edit_scope':'FRONT_HOOD_FENDER_RELATION_ONLY','metrics':metrics,'front_identity_metrics':semantic_front59(tris),'side_upper_samples':side,'front_profile_samples':fs,'rear_profile_samples':rs,'fit_views':['SIDE','FRONT_BODY_ONLY','REAR_BODY_ONLY'],'held_out_views':['HERO_FRONT_3Q','HERO_REAR_3Q','TOP_FRONT_3Q'],'reference_fidelity_review':'HOLD','design_quality_gate':'HOLD','does_not_prove':['whole-visible reference fidelity','final aperture architecture','Class-A continuity','manufacturing feasibility']}
runtime['projection30']=projection59

def regression59(pr):
    m={x['id']:x for x in pr['metrics']};sem=pr['front_identity_metrics']
    return {'schema':'oleander.3d.reference-regression-promotion-receipt.v2','baseline_revision':'V49_FEATURE_ALIGNED_CURVE_NETWORK','candidate_revision':REV,'edit_scope':['FRONT_HOOD_FENDER_RELATION_ONLY'],'target_metric_delta':{'metric_id':'HOOD_FENDER_HIERARCHY','baseline':'UNSCREENED_IN_V49','candidate':sem.get('mean_fender_crown_minus_hood_m'),'direction':'POSITIVE_DELTA_REQUIRED','improved':sem.get('semantic_relation_state')=='SCREENED'},'regression_locks':[{'id':'SIDE_UPPER','baseline':0.013934324664521762,'candidate':m['SIDE_UPPER_EVALUATED_MESH_RMSE_M']['candidate'],'limit':.006,'status':'PASS' if m['SIDE_UPPER_EVALUATED_MESH_RMSE_M']['candidate']<=.019934324664521762 else 'REGRESSED'},{'id':'REAR_BODY_ONLY_DIAGNOSTIC','baseline':0.1724060805022639,'candidate':m['REAR_BODY_ONLY_PROFILE_RMSE']['candidate'],'limit':.010,'status':'PASS' if m['REAR_BODY_ONLY_PROFILE_RMSE']['candidate']<=.1824060805022639 else 'REGRESSED'}],'measurement_comparability':'PARTIAL_SEMANTIC_TARGET_NEW','promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','design quality','Class-A continuity']}
runtime['regression30']=regression59

def components(o):
    me=o.data;adj=[set() for _ in me.vertices];used=set()
    for p in me.polygons:
        vs=list(p.vertices);used.update(vs)
        for a,b in zip(vs,vs[1:]+vs[:1]):adj[a].add(b);adj[b].add(a)
    seen=set();n=0
    for s in used:
        if s in seen:continue
        n+=1;stack=[s];seen.add(s)
        while stack:
            q=stack.pop()
            for z in adj[q]:
                if z not in seen:seen.add(z);stack.append(z)
    return n

def folds(o):
    ef={};n=0
    for p in o.data.polygons:
        for e in p.edge_keys:ef.setdefault(tuple(sorted(e)),[]).append(p.index)
    for fs in ef.values():
        if len(fs)==2 and float(o.data.polygons[fs[0]].normal.dot(o.data.polygons[fs[1]].normal))<-.15:n+=1
    return n

def edge_p95(o):
    mw=o.matrix_world;ls=[]
    for e in o.data.edges:
        a=mw@o.data.vertices[e.vertices[0]].co;b=mw@o.data.vertices[e.vertices[1]].co;ls.append(float((a-b).length))
    ls.sort();return ls[min(len(ls)-1,max(0,int(math.ceil(.95*len(ls))-1)))] if ls else float('inf')

def emit_surface_v2(out):
    ev=bpy.data.objects.get('DIAG_FEATURE_ALIGNED_SURFACED_V59');me=ev.data;me.calc_loop_triangles();p95=edge_p95(ev);fc=folds(ev);cc=components(ev);sampling='PASS' if p95<=.30 else 'HOLD';machine='MACHINE_CONSTRUCTED_VISUAL_HOLD' if cc==1 and fc==0 and sampling=='PASS' else ('MACHINE_SURFACE_TOPOLOGY_FAIL' if cc!=1 or fc!=0 else 'MACHINE_SURFACE_SAMPLING_HOLD')
    d={'schema':'oleander.3d.primary-body-surface-receipt.v2','revision':REV,'surface_measurement_scope':'CLOSED_PRIMARY_VISUAL_HULL_BEFORE_FINAL_APERTURE_ARCHITECTURE','source_state_class':'SOURCE_CONTROL_CAGE','source_semantic_rail_count':len(RAILS),'source_ring_control_count':len(ring59(0.0)),'source_density_role':'INFORMATIONAL_CAUSAL_CONTROL_COMPLEXITY_NOT_EVALUATED_QUALITY_GATE','evaluated_carrier':'DIAG_FEATURE_ALIGNED_SURFACED_V59','evaluated_state_class':'DERIVED_DIAGNOSTIC_NOT_AUTHORITY','evaluated_vertices':len(me.vertices),'evaluated_edges':len(me.edges),'evaluated_faces':len(me.polygons),'evaluated_triangles':len(me.loop_triangles),'evaluated_connected_components':cc,'evaluated_adjacent_face_normal_flip_count':fc,'evaluated_edge_p95_m':p95,'evaluated_sampling_gate':{'basis':'EVALUATED_EDGE_P95_AT_CURRENT_REVIEW_SCALE','status':sampling,'threshold_or_rule':'evaluated_edge_p95_m <= 0.30','observed':p95,'review_scope':'992.2 primary-form review; not universal production tolerance'},'machine_surface_state':machine,'visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','Class-A continuity','final aperture architecture','Design KEEP']}
    Path(out,'PRIMARY_BODY_SURFACE_RECEIPT_V2.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');Path(out,'PRIMARY_BODY_SURFACE_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def run59():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:runtime['run30']()
    except SystemExit as e:
        emit_surface_v2(out)
        raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:emit_surface_v2(out)
run59()
