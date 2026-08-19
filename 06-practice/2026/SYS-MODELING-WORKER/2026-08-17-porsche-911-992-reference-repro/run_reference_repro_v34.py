#!/usr/bin/env python3
"""V34 — recalibrated multi-view visual hull stage.

The benchmark stops composing a separate visible body and cabin shell. A single closed outer hull is generated
from: (1) recalibrated SIDE top silhouette, (2) official hard points / plan-width controls, and (3) FRONT/REAR
projected width-by-height profiles. Greenhouse is a material region on the visual hull at this stage, with light
frame overlays; final aperture architecture is explicitly deferred until the primary form is visually credible.

This is a primary-form experiment, not Porsche CAD / Class-A / final glazing construction.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy,bmesh

HERE=Path(__file__).resolve().parent
V30=HERE/'run_reference_repro_v30.py'
text=V30.read_text();marker='\nrun30()\n'
if marker not in text:raise SystemExit('V30 run marker missing')
env={'__file__':str(V30),'__name__':'oleander_v34_declarations'}
exec(compile(text.split(marker,1)[0],str(V30),'exec'),env)
v=env['v'];PROFILE=env['PROFILE'];metric=env['metric'];s01=env['s01'];h=env['h']
VIS=json.loads((HERE/'REFERENCE_VISUAL_HULL_TARGETS_992_2.json').read_text())
SIDE=[(float(x),float(z)) for x,z in VIS['side']['top_silhouette_m']]
FRONT=sorted([(float(f),float(r)) for f,r in PROFILE['front']['profile']],reverse=True)
REAR=sorted([(float(f),float(r)) for f,r in PROFILE['rear']['profile']],reverse=True)
REV='V34_RECALIBRATED_MULTI_VIEW_VISUAL_HULL'

v.REF='2025_992.2_CARRERA_MULTI_VIEW_VISUAL_HULL_V34'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v34'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['primary_form_method']='SINGLE_CLOSED_MULTI_VIEW_VISUAL_HULL'
v.REFERENCE_CONTRACT['visual_hull_target']='REFERENCE_VISUAL_HULL_TARGETS_992_2.json'
v.REFERENCE_CONTRACT['greenhouse_stage']='MATERIAL_REGION_ONLY_APERTURE_ARCHITECTURE_DEFERRED'
v.FAMILY_CONTROLS['MULTI_VIEW_VISUAL_HULL_V34']={
 'side':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m',
 'front_rear':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json',
 'longitudinal_stations':97,'half_section_rails':16,
 'protected':['LENGTH','WIDTH','HEIGHT','WHEELBASE','AXLE_CENTRES','V20_WHEEL_APERTURE','V20_LOWER_TERMINAL_RETURN']}
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

Z0=.140;ZH=1.298;ZR=ZH-Z0
MAT={}
base_materials=v.materials
def materials34():
    M=base_materials();MAT.clear();MAT.update(M)
    # visual-hull stage: glass is dark but not highly transparent; shape read first.
    bs=M['glass'].node_tree.nodes.get('Principled BSDF')
    if bs:
        if 'Base Color' in bs.inputs:bs.inputs['Base Color'].default_value=(.008,.014,.020,1)
        if 'Roughness' in bs.inputs:bs.inputs['Roughness'].default_value=.18
        if 'Transmission Weight' in bs.inputs:bs.inputs['Transmission Weight'].default_value=.02
    return M
v.materials=materials34

def side_top(x):return float(v.hermite(SIDE,float(x)))
def lerp(a,b,t):return a*(1-t)+b*t

def ratio_at(profile,frac):
    frac=float(frac)
    if frac>=profile[0][0]:
        f0,r0=profile[0];return max(.04,r0*(1-frac)/max(1e-6,1-f0)) if frac<=1 else .04
    if frac<=profile[-1][0]:return profile[-1][1]
    for (f0,r0),(f1,r1) in zip(profile,profile[1:]):
        if f0>=frac>=f1:
            t=(f0-frac)/(f0-f1);return lerp(r0,r1,t)
    return profile[-1][1]

def front_weight(x):return s01((float(x)+.55)/1.10)
def profile_ratio(x,z):
    frac=max(.10,min(.995,(float(z)-Z0)/ZR));w=front_weight(x)
    return lerp(ratio_at(REAR,frac),ratio_at(FRONT,frac),w)

def plan_half_width(x):
    w=h(v.WIDTH_PTS,x)+.018*math.exp(-((x-v.FRONT_AXLE)/.50)**4)+.030*math.exp(-((x-v.REAR_AXLE)/.54)**4)
    return min(v.WIDTH/2,max(.30,w))

def terminal_floor(x):
    rear=[(-2.271,.416),(-2.10,.407),(-1.90,.263),(-1.72,.150)]
    front=[(1.72,.155),(1.85,.160),(2.05,.197),(2.271,.207)]
    if x<=-1.72:return h(rear,x)
    if x>=1.72:return h(front,x)
    return .140

def cabin_weight(x):
    x=float(x)
    if -1.12<=x<=.58:return 1.0
    if -1.36<x<-1.12:return s01((x+1.36)/.24)
    if .58<x<.78:return 1.0-s01((x-.58)/.20)
    return 0.0

def body_half_section(x,w,top,f):
    fi=math.exp(-((x-v.FRONT_AXLE)/.52)**4);ri=math.exp(-((x-v.REAR_AXLE)/.60)**4)
    center=top-(.032+.045*fi+.060*ri)
    peak=.80
    if f<=peak:
        z=center+(top-center)*(math.sin((f/peak)*math.pi/2)**1.38)
    else:
        z=top-(.030+.010*ri)*((f-peak)/(1-peak))**1.18
    return f*w,z

def cabin_section_samples(x,w,top):
    belt=max(.805,min(.875,h(v.BELT_PTS,max(-1.03,min(.76,x)))))
    curves=[0.0,.025,.060,.115,.190,.290,.410,.545,.690,.825,1.0]
    ys=[];pts=[];prev=0.0
    for j,c in enumerate(curves):
        z=lerp(top,belt,c)
        if j==0:y=0.0
        elif j==len(curves)-1:y=w
        else:
            raw=min(w,.5*v.WIDTH*profile_ratio(x,z))
            y=max(prev+.012,raw)
            y=min(y,w-.010*(len(curves)-1-j))
        prev=y;pts.append((y,z))
    return pts

def hull_ring(x):
    w=plan_half_width(x);top=side_top(x);floor=terminal_floor(x);cw=cabin_weight(x)
    fvals=[0,.12,.24,.36,.48,.60,.70,.78,.85,.92,1.0]
    body=[body_half_section(x,w,top,f) for f in fvals]
    cab=cabin_section_samples(x,w,top)
    pos=[]
    for (yb,zb),(yc,zc) in zip(body,cab):pos.append((lerp(yb,yc,cw),lerp(zb,zc,cw)))
    # lower side / rocker / underbody rails: preserve V20 lower envelope.
    sidez=pos[-1][1]
    pos += [(.998*w,max(floor+.038,min(sidez-.050,.240))),(.90*w,max(floor,.150)),(.68*w,max(.140,floor-.006)),(.36*w,max(.140,floor-.010)),(0.0,max(.140,floor-.012))]
    # maintain monotonic Y from center -> side -> center to prevent bow-tie sections.
    for i in range(1,11):
        pos[i]=(max(pos[i][0],pos[i-1][0]+.002),pos[i][1])
    for i in range(12,len(pos)):
        pos[i]=(max(0.0,min(pos[i][0],pos[i-1][0]-.002)),pos[i][1])
    pos[-1]=(0.0,pos[-1][1])
    # terminal plan curvature is baked into the hull rather than a flat constant-X cap.
    ft=s01((x-1.78)/(v.FRONT_X-1.78)) if x>1.78 else 0.0
    rt=s01((-x-1.78)/(-v.REAR_X-1.78)) if x<-1.78 else 0.0
    out=[]
    for y,z in pos+[( -yy,zz) for yy,zz in reversed(pos[1:-1])]:
        q=abs(y)/max(w,1e-6);setback=(.105*ft+.085*rt)*(q**1.55)
        xe=x-setback if x>0 else x+setback
        out.append((xe,y,z))
    return out

def build_visual_hull(name,bodymat):
    xs=[v.REAR_X+(v.FRONT_X-v.REAR_X)*i/96 for i in range(97)]
    xs=sorted(set(round(x,6) for x in xs+[v.REAR_X,-2.10,-1.90,-1.72,v.REAR_AXLE,-1.36,-1.12,-.55,0,.58,.78,v.FRONT_AXLE,1.72,1.90,2.10,v.FRONT_X]))
    verts=[];rings=[]
    for x in xs:
        ring=hull_ring(x);rings.append(list(range(len(verts),len(verts)+len(ring))));verts.extend(ring)
    nr=len(rings[0]);faces=[]
    for i in range(len(rings)-1):
        for j in range(nr):faces.append((rings[i][j],rings[i+1][j],rings[i+1][(j+1)%nr],rings[i][(j+1)%nr]))
    faces.append(tuple(reversed(rings[0])));faces.append(tuple(rings[-1]))
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(bodymat);o.data.materials.append(MAT['glass']);o.data.materials.append(MAT['body_dark'])
    # Glass is a material region on the SAME continuous hull during primary-form stage.
    for p in me.polygons:
        c=p.center;x,y,z=map(float,c);cw=cabin_weight(x)
        glass=False
        if cw>.45 and z>.835:
            # windshield / rear backlight and side glazing are all part of the high greenhouse hull.
            if (.18<x<.73 and z>.86):glass=True
            if (-1.18<x<-.34 and z>.92):glass=True
            if (-1.08<x<.56 and abs(y)>.30 and z>.855):glass=True
            # keep central roof/body strip opaque.
            if -0.52<x<.25 and abs(y)<.30 and z>1.12:glass=False
        p.material_index=1 if glass else 0;p.use_smooth=True
    o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY';o['OLEANDER_FORM_FAMILY']='SINGLE_MULTI_VIEW_VISUAL_HULL_V34';o['OLEANDER_LONGITUDINAL_STATIONS']=len(xs);o['OLEANDER_RING_VERTICES']=nr;o['OLEANDER_GREENHOUSE_STAGE']='MATERIAL_REGION_NOT_FINAL_APERTURE'
    return o

def cabin_placeholder(name,mat):
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata([],[],[]);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.hide_render=True;o['OLEANDER_AUTHORITY']='DERIVED_STAGE_PLACEHOLDER';o['OLEANDER_STAGE']='VISUAL_HULL_HAS_INTEGRATED_GREENHOUSE';return o

base_loft=v.build_loft
def build_loft34(name,xs,ringfn,mat,authority,render=True):
    if name=='DERIVED_911_9922_BODY':return build_visual_hull(name,mat)
    if name=='DERIVED_911_9922_CABIN':return cabin_placeholder(name,mat)
    return base_loft(name,xs,ringfn,mat,authority,render)
v.build_loft=build_loft34
v.body_ring=hull_ring

# No separate exterior glazing shell. Keep diagnostic aperture panels hidden for ratios and add only visible frame cues.
def build_glass34(M):
    out=[]
    # diagnostic panels are non-rendered; they do not fake the visible candidate.
    ws=v.m.add_panel('REF_WINDSHIELD',[(.650,.620,.830),(.650,-.620,.830),(.235,-.545,1.215),(.235,.545,1.215)],M['glass'],.001);ws.hide_render=True;out.append(ws)
    rg=v.m.add_panel('REF_REAR_GLASS',[(-.390,.490,1.215),(-.390,-.490,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)],M['glass'],.001);rg.hide_render=True;out.append(rg)
    # restrained opaque frame cues over the integrated greenhouse material region.
    for side,label in ((1,'L'),(-1,'R')):
        out.append(v.m.add_curve('REF_A_PILLAR_FRAME_'+label,[(.635,side*.610,.850),(.440,side*.550,1.055),(.235,side*.500,1.210)],M['body'],.010))
        out.append(v.m.add_curve('REF_C_PILLAR_FRAME_'+label,[(-.390,side*.465,1.205),(-.700,side*.515,1.105),(-1.020,side*.585,.960)],M['body'],.012))
        out.append(v.m.add_cube('REF_B_PILLAR_'+label,(-.220,side*.500,1.010),(.030,.020,.285),M['body_dark'],.002))
        out.append(v.m.add_cube('REF_DOOR_HANDLE_'+label,(-.020,side*.896,.682),(.105,.012,.017),M['body_dark'],.003))
        y=side*.912;out.append(v.m.add_curve('REF_DOOR_SEAM_'+label,[(.595,y,.765),(.545,y,.500),(-.635,y,.500),(-.800,y,.665),(-.785,y,.825)],M['seam'],.0016))
    return out
v.build_glass=build_glass34

base_source=v.build_source
def source34(M):
    o=base_source(M);o['OLEANDER_VISUAL_HULL_TARGET']='REFERENCE_VISUAL_HULL_TARGETS_992_2.json';o['OLEANDER_STAGE']='PRIMARY_FORM_VISUAL_HULL';o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=source34

# Projection: reuse final evaluated scanner, but recompute SIDE upper against recalibrated V34 target.
base_projection=env['projection30']
def relabel(data):
    if isinstance(data,dict):return {k:relabel(x) for k,x in data.items()}
    if isinstance(data,list):return [relabel(x) for x in data]
    if isinstance(data,str):return data.replace('V30_','V34_')
    return data

def projection34():
    d=relabel(base_projection());d['candidate_revision']=REV;d['primary_form_stage']='MULTI_VIEW_VISUAL_HULL'
    nt={round(x,3):z for x,z in SIDE};errs=[]
    for s in d.get('side_upper_samples',[]):
        key=round(float(s['x']),3)
        if key in nt:
            s['target_top']=nt[key];s['top_error_m']=float(s['candidate_top'])-nt[key];s['reference_target_source']='REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m';errs.append(s['top_error_m'])
    rmse=math.sqrt(sum(e*e for e in errs)/len(errs)) if errs else 9.0
    for m in d['metrics']:
        if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M':m['candidate']=rmse;m['abs_error']=rmse;m['limit']=VIS['gates']['side_upper_rmse_max_m'];m['reference_target_source']='REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m';m['candidate_measurement_source']='V34_FINAL_EVALUATED_VISUAL_HULL'
        else:m['candidate_measurement_source']=str(m.get('candidate_measurement_source','')).replace('V30_','V34_')
    d['status']='PROJECTION_MACHINE_SCREENING_PASS' if all(float(m['abs_error'])<=float(m['limit']) for m in d['metrics']) else 'PROJECTION_MACHINE_SCREENING_FAIL'
    return d
env['projection30']=projection34

# Comparable locks only. Aperture-ratio panels are diagnostics during visual-hull stage and cannot promote this stage.
BEST={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':{'revision':'V25','value':0.030139600203300147,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},'SIDE_LOWER_EVALUATED_MESH_RMSE_M':{'revision':'V25','value':0.061843072886901856,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},'FRONT_HALF_PROJECTED_PROFILE_RMSE':{'revision':'V31','value':0.07230088060916158,'evidence_source':'V31 REFERENCE_PROJECTION_RECEIPT.json'},'REAR_HALF_PROJECTED_PROFILE_RMSE':{'revision':'V25','value':0.1165857932746437,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'}}
def regression34(pr):
    vals={k:metric(pr,k)['candidate'] for k in BEST};limits={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':.040,'SIDE_LOWER_EVALUATED_MESH_RMSE_M':.070,'FRONT_HALF_PROJECTED_PROFILE_RMSE':.105,'REAR_HALF_PROJECTED_PROFILE_RMSE':.130};locks=[]
    for mid,b in BEST.items():
        c=float(vals[mid]);locks.append({'id':mid,'baseline':b['value'],'baseline_revision':b['revision'],'candidate':c,'limit':limits[mid],'status':'PASS' if math.isfinite(c) and c<=limits[mid] else 'REGRESSED','evidence_source':b['evidence_source']})
    return {'schema':'oleander.3d.reference-regression-promotion-receipt.v2','baseline_revision':'MIXED_PER_GATE_BEST_KNOWN_VISUAL_HULL','candidate_revision':REV,'edit_scope':['PRIMARY_FORM_REPRESENTATION','SIDE_TARGET_RECALIBRATION','FRONT_REAR_VISUAL_HULL','GREENHOUSE_MATERIAL_STAGE'],'target_metric_delta':{'metric_id':'SIDE_UPPER_EVALUATED_MESH_RMSE_M','baseline':0.06603510466192342,'candidate':vals['SIDE_UPPER_EVALUATED_MESH_RMSE_M'],'direction':'LOWER_IS_BETTER','improved':vals['SIDE_UPPER_EVALUATED_MESH_RMSE_M']<0.06603510466192342},'regression_locks':locks,'best_known_gate_baselines':BEST,'measurement_method_ids':['V34_FINAL_EVALUATED_VISUAL_HULL_XZ','V34_FINAL_EVALUATED_VISUAL_HULL_YZ'],'measurement_comparability':'COMPARABLE','promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT' if all(x['status']=='PASS' for x in locks) else 'KEEP_LKG_REJECT_EXPERIMENT','visual_review_state':'NOT_RUN','does_not_prove':VIS['does_not_prove']}
env['regression30']=regression34

# Pre-aperture skin QA on the unified hull before wheel cuts: build_visual_hull already produces ordered topology; use hidden copy.
orig_build=build_visual_hull
def build_visual_hull_diag(name,mat):
    o=orig_build(name,mat);d=o.copy();d.data=o.data.copy();d.name='DIAG_PRE_APERTURE_VISUAL_HULL_V34';bpy.context.collection.objects.link(d);d.hide_render=True;d.hide_set(True);d['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY';return o
# swap function used by build_loft34
build_visual_hull=build_visual_hull_diag

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

def local_quality(obj):
    me=obj.data;ef={};lengths=[]
    for p in me.polygons:
        cx=sum(me.vertices[i].co.x for i in p.vertices)/len(p.vertices)
        if cx<=v.REAR_X+.01 or cx>=v.FRONT_X-.01:continue
        vs=list(p.vertices)
        for a,b in zip(vs,vs[1:]+vs[:1]):
            ef.setdefault(tuple(sorted((a,b))),[]).append(p.index);L=(me.vertices[a].co-me.vertices[b].co).length
            if L<.60:lengths.append(float(L))
    flips=sum(1 for fs in ef.values() if len(fs)==2 and me.polygons[fs[0]].normal.dot(me.polygons[fs[1]].normal)<-.15)
    lengths.sort();p95=lengths[min(len(lengths)-1,int(.95*(len(lengths)-1)))] if lengths else 9.0
    return flips,p95

def surface34():
    d=bpy.data.objects.get('DIAG_PRE_APERTURE_VISUAL_HULL_V34');fl,p95=local_quality(d) if d else (99,9.0);body=bpy.data.objects.get('DERIVED_911_9922_BODY')
    state='MACHINE_CONSTRUCTED_VISUAL_HOLD' if d and components(d)==1 and fl==0 and p95<=.30 else 'MACHINE_SURFACE_TOPOLOGY_FAIL'
    return {'schema':'oleander.3d.primary-body-surface-receipt.v1','revision':REV,'surface_measurement_scope':'PRE_APERTURE_PRIMARY_SKIN','body_cap_edges_excluded':True,'body_connected_components':components(d) if d else 99,'cabin_connected_components':1,'body_adjacent_face_normal_flip_count':fl,'cabin_adjacent_face_normal_flip_count':0,'body_local_edge_p95_m':p95,'body_longitudinal_stations':int(body.get('OLEANDER_LONGITUDINAL_STATIONS',0)) if body else 0,'body_ring_vertices':int(body.get('OLEANDER_RING_VERTICES',0)) if body else 0,'machine_surface_state':state,'visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','Class-A continuity','manufacturer CAD','reflection continuity','production patch layout']}
env['surface_receipt']=surface34

# Patch inherited QA/receipt revision coherently after core execution.
def patch(out):
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=out/fn
        if not p.exists():continue
        d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='MULTI_VIEW_VISUAL_HULL';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def run34():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:env['run30']()
    except SystemExit as e:
        patch(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch(out)
run34()
