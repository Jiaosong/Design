#!/usr/bin/env python3
"""V31 — side-contour-driven fastback + pre-aperture primary-skin QA.

V30 materially improved the visible body but missed the calibrated SIDE upper envelope and its surface QA
was polluted by intentional wheel-arch Boolean/cap edges. V31 keeps the dense primary-body representation,
binds body/cabin upper geometry directly to REFERENCE_CONTOUR_TARGETS_992_2.json, and evaluates local skin
quality on a pre-aperture diagnostic copy. Strict V25 best-known regression locks remain unchanged.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy, bmesh

HERE=Path(__file__).resolve().parent
V30=HERE/'run_reference_repro_v30.py'
text=V30.read_text();marker='\nrun30()\n'
if marker not in text:raise SystemExit('V30 run marker missing')
ns={'__file__':str(V30),'__name__':'oleander_v31_declarations'}
exec(compile(text.split(marker,1)[0],str(V30),'exec'),ns)
v=ns['v'];PROFILE=ns['PROFILE'];metric=ns['metric'];BEST=ns['BEST'];old_macro=ns['macro_fields'];old_build_grid=ns['build_grid_body'];base_projection=ns['projection30'];h=ns['h'];s01=ns['s01'];lerp=lambda a,b,t:a*(1-t)+b*t
CONTOUR=json.loads((HERE/'REFERENCE_CONTOUR_TARGETS_992_2.json').read_text())
SIDE=[(float(x),float(z)) for x,z in CONTOUR['side_top_silhouette_m']]

v.REF='2025_992.2_CARRERA_SIDE_CONTOUR_FASTBACK_V31'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v31'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['side_upper_geometry_source']='REFERENCE_CONTOUR_TARGETS_992_2.json:side_top_silhouette_m'
v.REFERENCE_CONTRACT['surface_quality_measurement']='PRE_APERTURE_PRIMARY_SKIN'
v.FAMILY_CONTROLS['SIDE_CONTOUR_FASTBACK_V31']={'side_target':'REFERENCE_CONTOUR_TARGETS_992_2.json','body_target_regions':['x<=-1.05','x>=0.55'],'cabin_target_region':[-1.15,.65],'pre_aperture_skin_QA':True,'protected':['V20_WHEEL_APERTURE','V20_LOWER_TERMINAL_RETURN','WHEELBASE','AXLE_CENTRES']}
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

def side_ref(x):return float(v.hermite(SIDE,float(x)))
def blend(a,b,t):return a*(1-t)+b*t

def macro_fields31(x):
    w,center,crown,lower,fi,ri=old_macro(x)
    ref=side_ref(x)
    # Body owns the side silhouette outside the greenhouse. Blend only in narrow transition zones.
    if x>=.72 or x<=-1.20:
        target=ref
    elif .55<x<.72:
        target=blend(crown,ref,s01((x-.55)/.17))
    elif -1.20<x<-1.05:
        target=blend(ref,crown,s01((x+1.20)/.15))
    else:
        # Beneath the greenhouse the body must remain below the glazing/belt, not become the roof.
        target=min(crown,.865)
    # Keep hood/deck center lower than fender/quarter crown; rear gap slightly stronger.
    gap=.024+.045*fi+.065*ri
    center=min(center,target-gap)
    return w,center,target,lower,fi,ri
ns['macro_fields']=macro_fields31
# body_ring30 resolves macro_fields through this execution namespace.

# Pre-aperture diagnostic copy before V20 wheel-arch Boolean modifiers are later applied to the returned body.
def build_grid31(name,material):
    body=old_build_grid(name,material)
    diag=body.copy();diag.data=body.data.copy();diag.name='DIAG_PRE_APERTURE_PRIMARY_SKIN_V31';bpy.context.collection.objects.link(diag);diag.hide_render=True;diag.hide_set(True)
    diag['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY';diag['OLEANDER_DIAGNOSTIC_SCOPE']='PRE_APERTURE_PRIMARY_SKIN'
    return body
ns['build_grid_body']=build_grid31

# Fastback cabin: upper edges follow the same calibrated side contour; lower glass anchors remain independent.
def cabin31(name,material):
    verts=[];faces=[];idx={}
    def add(k,p):
        if k in idx:return idx[k]
        idx[k]=len(verts);verts.append(tuple(map(float,p)));return idx[k]
    def face(*a):faces.append(tuple(a))
    # Central roof is short in plan but follows the calibrated fastback apex in X/Z.
    xs=[-.450,-.390,-.330,-.270,-.210,-.150,-.090,-.030,.030,.090,.150,.205,.235];rows=[]
    for x in xs:
        t=(x+.450)/(.685);rw=.445+.095*s01(t);top=side_ref(x)
        row=[add(('r',x,-2),(x,-rw,top-.045)),add(('r',x,-1),(x,-rw*.58,top-.014)),add(('r',x,0),(x,0,top)),add(('r',x,1),(x,rw*.58,top-.014)),add(('r',x,2),(x,rw,top-.045))];rows.append(row)
    for a,b in zip(rows,rows[1:]):
        for j in range(4):face(a[j],b[j],b[j+1],a[j+1])
    rear,front=rows[0],rows[-1]
    # A-pillar: outer ridge traces side target; inner edge is windshield boundary below it.
    ax=[.235,.315,.395,.475,.555,.650]
    for side,lab,outer0,inner0 in ((1,'R',front[4],front[3]),(-1,'L',front[0],front[1])):
        outs=[outer0];ins=[inner0]
        for k,x in enumerate(ax[1:],1):
            t=k/(len(ax)-1);ridge=side_ref(x);oy=blend(abs(verts[outer0][1]),.680,t);iy=blend(abs(verts[inner0][1]),.620,t);iz=blend(verts[inner0][2],.830,t)
            outs.append(add(('A',lab,k,'o'),(x,side*oy,ridge)));ins.append(add(('A',lab,k,'i'),(x,side*iy,min(ridge-.025,iz))))
        for i in range(len(outs)-1):face(outs[i],outs[i+1],ins[i+1],ins[i])
    # C-pillar / fastback sail: outer ridge follows SIDE exactly, inner rear-glass edge drops smoothly.
    cx=[-.450,-.560,-.680,-.800,-.920,-1.040,-1.150]
    for side,lab,outer0,inner0 in ((1,'R',rear[4],rear[3]),(-1,'L',rear[0],rear[1])):
        outs=[outer0];ins=[inner0]
        for k,x in enumerate(cx[1:],1):
            t=k/(len(cx)-1);ridge=side_ref(x);oy=blend(abs(verts[outer0][1]),.790,t);iy=blend(abs(verts[inner0][1]),.592,t);iz=blend(verts[inner0][2],.990,t)
            outs.append(add(('C',lab,k,'o'),(x,side*oy,ridge)));ins.append(add(('C',lab,k,'i'),(x,side*iy,min(ridge-.028,iz))))
        for i in range(len(outs)-1):face(outs[i],outs[i+1],ins[i+1],ins[i])
        deck=add(('deck',lab),(-1.380,side*.760,min(.830,side_ref(-1.38)-.080)));face(outs[-1],deck,ins[-1])
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(material);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY';o['OLEANDER_FORM_FAMILY']='SIDE_CONTOUR_FASTBACK_CABIN_V31';o['OLEANDER_NO_OPAQUE_SURFACE_BEHIND_GLAZING']=True;o['OLEANDER_OPEN_PATCH_RIM_WALLS']=False
    for p in me.polygons:p.use_smooth=True
    return o
ns['simple_cabin30']=cabin31

# Restore build dispatcher / body function to globals just changed above.
v.body_ring=ns['body_ring30']

# Glazing follows the revised roof headers but keeps lower anchor widths.
def add_panel(name,pts,mat,th=.0025):
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(pts,[],[tuple(range(len(pts)))]);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL'
    if th:
        s=o.modifiers.new(name+'_THICKNESS','SOLIDIFY');s.thickness=th;s.offset=0;s.use_rim=False
    for p in me.polygons:p.use_smooth=True
    return o

def glass31(M):
    out=[];fu=side_ref(.235)-.014;ru=side_ref(-.450)-.018
    out.append(add_panel('REF_WINDSHIELD',[(.650,.620,.830),(.650,-.620,.830),(.235,-.535,fu),(.235,.535,fu)],M['glass']))
    out.append(add_panel('REF_REAR_GLASS',[(-.450,.465,ru),(-.450,-.465,ru),(-1.150,-.592,.990),(-1.150,.592,.990)],M['glass']))
    for side,label in ((1,'L'),(-1,'R')):
        door=[(.600,side*.600,.840),(.235,side*.525,fu-.008),(-.200,side*.490,side_ref(-.20)-.030),(-.200,side*.565,.842),(.500,side*.600,.840)]
        quarter=[door[2],(-.450,side*.455,ru-.010),(-.760,side*.535,min(side_ref(-.76)-.040,1.105)),(-1.100,side*.585,1.005),(-.680,side*.565,.860),(-.200,side*.565,.842)]
        out.append(add_panel('REF_DOOR_GLASS_'+label,door,M['glass']));out.append(add_panel('REF_QUARTER_GLASS_'+label,quarter,M['glass']))
        b=v.m.add_cube('REF_B_PILLAR_'+label,(-.200,side*.535,1.015),(.030,.024,.300),M['body_dark'],.003);b['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(b)
        out.append(v.m.add_cube('REF_DOOR_HANDLE_'+label,(-.020,side*.896,.682),(.105,.012,.017),M['body_dark'],.003));y=side*.912;out.append(v.m.add_curve('REF_DOOR_SEAM_'+label,[(.595,y,.765),(.545,y,.500),(-.635,y,.500),(-.800,y,.665),(-.785,y,.825)],M['seam'],.0016))
    for nm,loc,scale in [('REF_CABIN_OCCLUSION_BACKING',(-.18,0,.790),(1.34,.84,.10)),('REF_DASH_BACKING',(.410,0,.760),(.30,.86,.09)),('REF_REAR_BULKHEAD_BACKING',(-.850,0,.760),(.16,.80,.12))]:
        o=v.m.add_cube(nm,loc,scale,M['body_dark'],.006);o['OLEANDER_AUTHORITY']='DERIVED_EXECUTION_NOT_AUTHORITY';out.append(o)
    return out
v.build_glass=glass31

base_source=v.build_source
def source31(M):
    o=base_source(M);o['OLEANDER_SIDE_CONTOUR_GEOMETRY']='V31_DIRECT_CAUSAL_BINDING';o['OLEANDER_SURFACE_QA_SCOPE']='PRE_APERTURE_PRIMARY_SKIN';o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=source31

# V30 build_loft function resolves build_grid_body/simple_cabin30 in ns after replacements.
v.build_loft=ns['build_loft30']

def relabel(data):
    if isinstance(data,dict):return {k:relabel(x) for k,x in data.items()}
    if isinstance(data,list):return [relabel(x) for x in data]
    if isinstance(data,str):return data.replace('V30_','V31_')
    return data

def projection31():
    d=relabel(base_projection());d['candidate_revision']='V31_SIDE_CONTOUR_FASTBACK';d['side_upper_geometry_source']='REFERENCE_CONTOUR_TARGETS_992_2.json';return d
ns['projection30']=projection31

# Strict per-gate locks: unchanged from V25 policy.
def regression31(pr):
    vals={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_UPPER_EVALUATED_MESH_RMSE_M')['candidate'],'SIDE_LOWER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_LOWER_EVALUATED_MESH_RMSE_M')['candidate'],'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':metric(pr,'FRONT_UPPER_CABIN_WIDTH_RATIO')['abs_error'],'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':metric(pr,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO')['abs_error'],'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':metric(pr,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO')['abs_error'],'FRONT_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'FRONT_HALF_PROJECTED_PROFILE_RMSE')['candidate'],'REAR_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'REAR_HALF_PROJECTED_PROFILE_RMSE')['candidate']}
    limits={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':.034,'SIDE_LOWER_EVALUATED_MESH_RMSE_M':.066,'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':.010,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':.010,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':.010,'FRONT_HALF_PROJECTED_PROFILE_RMSE':.090,'REAR_HALF_PROJECTED_PROFILE_RMSE':.130};locks=[]
    for mid,b in BEST.items():
        c=vals[mid];locks.append({'id':mid,'baseline':b['value'],'baseline_revision':b['revision'],'candidate':c,'limit':limits[mid],'status':'PASS' if math.isfinite(c) and c<=limits[mid] else 'REGRESSED','evidence_source':b['evidence_source']})
    all_locks=all(x['status']=='PASS' for x in locks)
    return {'schema':'oleander.3d.reference-regression-promotion-receipt.v2','baseline_revision':'BEST_KNOWN_GATE_BASELINE_V25','candidate_revision':'V31_SIDE_CONTOUR_FASTBACK','edit_scope':['SIDE_UPPER_CAUSAL_BINDING','FASTBACK_CABIN','PRE_APERTURE_SURFACE_QA'],'target_metric_delta':{'metric_id':'SIDE_UPPER_EVALUATED_MESH_RMSE_M','baseline':.10654795205383265,'candidate':vals['SIDE_UPPER_EVALUATED_MESH_RMSE_M'],'direction':'LOWER_IS_BETTER','improved':vals['SIDE_UPPER_EVALUATED_MESH_RMSE_M']<.10654795205383265},'regression_locks':locks,'best_known_gate_baselines':BEST,'measurement_method_ids':['V31_FINAL_EVALUATED_MESH_XZ','V31_FINAL_EVALUATED_MESH_YZ','V31_PRE_APERTURE_SKIN'],'measurement_comparability':'COMPARABLE','promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT' if all_locks else 'KEEP_LKG_REJECT_EXPERIMENT','visual_review_state':'NOT_RUN','does_not_prove':PROFILE['does_not_prove']}
ns['regression30']=regression31

# Region-aware pre-aperture skin diagnostics.
def components(obj):
    me=obj.data;adj=[set() for _ in me.vertices];used=set()
    for p in me.polygons:
        vs=list(p.vertices);used.update(vs)
        for a,b in zip(vs,vs[1:]+vs[:1]):adj[a].add(b);adj[b].add(a)
    seen=set();n=0
    for s in used:
        if s in seen:continue
        n+=1;st=[s];seen.add(s)
        while st:
            q=st.pop()
            for z in adj[q]:
                if z not in seen:seen.add(z);st.append(z)
    return n

def skin_quality(obj,exclude_caps=True):
    me=obj.data;valid_faces=set()
    for p in me.polygons:
        cx=sum(me.vertices[i].co.x for i in p.vertices)/len(p.vertices)
        if exclude_caps and (cx<=v.REAR_X+.008 or cx>=v.FRONT_X-.008):continue
        valid_faces.add(p.index)
    ef={};edges=[]
    for p in me.polygons:
        if p.index not in valid_faces:continue
        vs=list(p.vertices)
        for a,b in zip(vs,vs[1:]+vs[:1]):
            ef.setdefault(tuple(sorted((a,b))),[]).append(p.index)
            L=(me.vertices[a].co-me.vertices[b].co).length
            if L<.60:edges.append(float(L))
    flips=sum(1 for fs in ef.values() if len(fs)==2 and me.polygons[fs[0]].normal.dot(me.polygons[fs[1]].normal)<-.15)
    edges.sort();p95=edges[min(len(edges)-1,int(.95*(len(edges)-1)))] if edges else 9.0
    return flips,p95

def surface31():
    diag=bpy.data.objects.get('DIAG_PRE_APERTURE_PRIMARY_SKIN_V31');body=bpy.data.objects.get('DERIVED_911_9922_BODY');cabin=bpy.data.objects.get('DERIVED_911_9922_CABIN')
    bf,p95=skin_quality(diag,True) if diag else (99,9.0);cf,_=skin_quality(cabin,False) if cabin else (99,9.0)
    state='MACHINE_CONSTRUCTED_VISUAL_HOLD' if diag and cabin and components(diag)==1 and components(cabin)==1 and bf==0 and cf==0 and p95<=.30 else 'MACHINE_SURFACE_TOPOLOGY_FAIL'
    return {'schema':'oleander.3d.primary-body-surface-receipt.v1','revision':'V31_SIDE_CONTOUR_FASTBACK','surface_measurement_scope':'PRE_APERTURE_PRIMARY_SKIN','body_cap_edges_excluded':True,'body_connected_components':components(diag) if diag else 99,'cabin_connected_components':components(cabin) if cabin else 99,'body_adjacent_face_normal_flip_count':bf,'cabin_adjacent_face_normal_flip_count':cf,'body_local_edge_p95_m':p95,'body_longitudinal_stations':int(body.get('OLEANDER_LONGITUDINAL_STATIONS',0)) if body else 0,'body_ring_vertices':int(body.get('OLEANDER_RING_VERTICES',0)) if body else 0,'machine_surface_state':state,'visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','Class-A continuity','manufacturer CAD','reflection continuity','production patch layout']}
ns['surface_receipt']=surface31

# Post/run functions from V30 resolve projection30/regression30/surface_receipt in ns.
ns['run30']()
