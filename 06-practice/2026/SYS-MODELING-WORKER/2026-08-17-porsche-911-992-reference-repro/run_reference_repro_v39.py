#!/usr/bin/env python3
"""V39 — local rear shoulder-to-haunch continuity repair.

V38 localized all four >99-degree adjacent-face reversals to the upper-side rail around the rear axle
(x≈-1.21/-1.19 m, z≈.88-.92 m) and brought REAR profile RMSE to .11715. V39 freezes SIDE/front/glass and
changes only that transition: a narrow high shoulder flows through six eased rails into the low wide haunch.
Rear high/mid cap is tightened slightly. No detail/CMF changes are allowed in this version.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy,bmesh
HERE=Path(__file__).resolve().parent
V34=HERE/'run_reference_repro_v34.py';text=V34.read_text();marker='\nrun34()\n'
if marker not in text:raise SystemExit('V34 run marker missing')
ns={'__file__':str(V34),'__name__':'oleander_v39_declarations'};exec(compile(text.split(marker,1)[0],str(V34),'exec'),ns)
v=ns['v'];env=ns['env'];PROFILE=ns['PROFILE'];metric=ns['metric'];REAR=ns['REAR'];s01=ns['s01'];lerp=ns['lerp'];Z0=ns['Z0'];ZR=ns['ZR'];base_hull=ns['hull_ring'];orig_build34=ns['orig_build'];base_projection=ns['projection34'];base_regression=ns['regression34'];base_surface=ns['surface34'];base_patch=ns['patch']
GREEN=json.loads((HERE/'REFERENCE_GREENHOUSE_TARGETS_992_2.json').read_text());G=[tuple(map(float,p)) for p in GREEN['side_glass_envelope_m']]
REV='V39_REAR_SHOULDER_HAUNCH_CONTINUITY'
v.REF='2025_992.2_CARRERA_REAR_SHOULDER_HAUNCH_CONTINUITY_V39';v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v39';v.REFERENCE_CONTRACT['reference_revision']=v.REF;v.REFERENCE_CONTRACT['candidate_revision']=REV;v.REFERENCE_CONTRACT['failure_routing']='REAR_SHOULDER_TO_HAUNCH_CONTINUITY_ONLY';v.FAMILY_CONTROLS['REAR_SHOULDER_HAUNCH_V39']={'rear_profile':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:rear.profile','fold_evidence':'V38 SURFACE_FOLD_DIAGNOSTIC.json rear axle rail10','transition_rails':6,'protected':['SIDE_GESTURE','SIDE_LOWER','FRONT_PROFILE','GREENHOUSE_ENVELOPE','WHEELBASE','AXLE_CENTRES']};v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

def rear_cap(z):
    frac=max(.10,min(.98,(float(z)-Z0)/ZR));return .5*v.WIDTH*ns['ratio_at'](REAR,frac)+.010

def rear_weight(x):
    x=float(x)
    if x<=-.10:return 1.0
    if x>=.20:return 0.0
    return 1.0-s01((x+.10)/.30)

def hull_ring39(x):
    raw=base_hull(x);half=(len(raw)+2)//2;pos=[list(p) for p in raw[:half]]
    rw=rear_weight(x)
    if rw>0:
        for i in range(min(11,len(pos))):
            xe,y,z=pos[i]
            if i==0 or z<.70:continue
            ay=abs(y);cap=rear_cap(z);desired=min(ay,cap);strength=rw*s01((z-.70)/.34)
            pos[i][1]=lerp(ay,desired,strength)
        pos[0][1]=0.0
        for i in range(1,min(11,len(pos))):pos[i][1]=max(pos[i][1],pos[i-1][1]+.002)
    # Preserve V34 lower authority but replace the single sharp shoulder->haunch jump with an eased fan.
    if len(pos)>=12:
        side=pos[10];low=pos[11];trans=[]
        for t in (.14,.28,.42,.56,.70,.84):
            # zero-ish lateral derivative at the upper shoulder; wider change is delayed downward.
            ey=math.sin(t*math.pi/2)**1.45
            trans.append([lerp(side[0],low[0],t),lerp(side[1],low[1],ey),lerp(side[2],low[2],t)])
        pos=pos[:11]+trans+pos[11:]
        # From the original first low rail inward, enforce the normal decreasing-y underbody order.
        start=11+len(trans)
        for i in range(start+1,len(pos)):pos[i][1]=max(0.0,min(pos[i][1],pos[i-1][1]-.002))
    pos[-1][1]=0.0
    return [tuple(p) for p in pos]+[(xe,-y,z) for xe,y,z in reversed([tuple(p) for p in pos[1:-1]])]
ns['hull_ring']=hull_ring39;v.body_ring=hull_ring39

# Opaque body + diagnostic copy.
def build39(name,bodymat):
    o=orig_build34(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        for p in o.data.polygons:p.material_index=0
        o['OLEANDER_FORM_FAMILY']='REAR_SHOULDER_HAUNCH_CONTINUITY_HULL_V39';o['OLEANDER_FAILURE_ROUTING']='REAR_SHOULDER_TO_HAUNCH_CONTINUITY_ONLY'
    d=o.copy();d.data=o.data.copy();d.name='DIAG_PRE_APERTURE_VISUAL_HULL_V34';bpy.context.collection.objects.link(d);d.hide_render=True;d.hide_set(True);d['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY';return o
ns['build_visual_hull']=build39

# Same calibrated real-glass representation as V38.
def interp(seq,x,field):
    x=float(x)
    if x<=seq[0][0]:return seq[0][field]
    if x>=seq[-1][0]:return seq[-1][field]
    for a,b in zip(seq,seq[1:]):
        if a[0]<=x<=b[0]:return lerp(a[field],b[field],(x-a[0])/(b[0]-a[0]))
    return seq[-1][field]
def glass_y(x,z):
    w=ns['plan_half_width'](x);raw=.5*v.WIDTH*ns['profile_ratio'](x,z);return min(w-.008,max(.42,raw+.012))
def strip(name,pts,side,mat):
    verts=[];faces=[]
    for x,zt,zb in pts:verts.extend([(x,side*glass_y(x,zt),zt),(x,side*glass_y(x,zb),zb)])
    for i in range(len(pts)-1):a=2*i;faces.append((a,a+1,a+3,a+2))
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL';o['OLEANDER_REFERENCE']='REFERENCE_GREENHOUSE_TARGETS_992_2.json';
    for p in me.polygons:p.use_smooth=True
    return o
def glass39(M):
    out=[v.m.add_panel('REF_WINDSHIELD',[(.650,.620,.830),(.650,-.620,.830),(.235,-.545,1.215),(.235,.545,1.215)],M['glass'],.0015),v.m.add_panel('REF_REAR_GLASS',[(-.390,.490,1.215),(-.390,-.490,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)],M['glass'],.0015)]
    bp=(-.20,interp(G,-.20,1),interp(G,-.20,2));q=[p for p in G if p[0]<-.20]+[bp];d=[bp]+[p for p in G if p[0]>-.20]
    for side,label in ((1,'L'),(-1,'R')):
        out+=[strip('REF_QUARTER_GLASS_'+label,q,side,M['glass']),strip('REF_DOOR_GLASS_'+label,d,side,M['glass'])]
        by=glass_y(-.20,(bp[1]+bp[2])*.5);bz=(bp[1]+bp[2])*.5;bh=max(.12,bp[1]-bp[2]);b=v.m.add_cube('REF_B_PILLAR_'+label,(-.20,side*by,bz),(.026,.016,bh),M['body_dark'],.002);b['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(b)
    for name,loc,scale in [('REF_CABIN_OCCLUSION_BACKING',(-.18,0,.785),(1.35,.80,.10)),('REF_DASH_BACKING',(.410,0,.760),(.30,.76,.09)),('REF_REAR_BULKHEAD_BACKING',(-.840,0,.745),(.16,.76,.12))]:o=v.m.add_cube(name,loc,scale,M['body_dark'],.006);o['OLEANDER_AUTHORITY']='DERIVED_EXECUTION_NOT_AUTHORITY';out.append(o)
    return out
v.build_glass=glass39

def projection39():
    d=base_projection();d['candidate_revision']=REV;d['primary_form_stage']='REAR_SHOULDER_HAUNCH_CONTINUITY';finite=[];total=0
    for s in d.get('side_upper_samples',[]):total+=1;e=s.get('top_error_m');finite.append(float(e)) if isinstance(e,(int,float)) and math.isfinite(float(e)) else None
    cov=len(finite)/max(1,total);rmse=math.sqrt(sum(e*e for e in finite)/len(finite)) if finite else 9.0
    for m in d['metrics']:
        if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M':m['candidate']=rmse;m['abs_error']=rmse;m['candidate_measurement_source']='V39_FINAL_EVALUATED_HULL_FINITE_INTERSECTIONS';m['finite_sample_coverage']=cov
        else:m['candidate_measurement_source']=str(m.get('candidate_measurement_source','')).replace('V34_','V39_')
    d['side_upper_finite_sample_coverage']=cov;d['greenhouse_representation']='INDEPENDENT_CALIBRATED_GLASS';d['status']='PROJECTION_MACHINE_SCREENING_PASS' if cov>=.90 and all(math.isfinite(float(m['abs_error'])) and float(m['abs_error'])<=float(m['limit']) for m in d['metrics']) else 'PROJECTION_MACHINE_SCREENING_FAIL';return d
env['projection30']=projection39

def regression39(pr):
    d=base_regression(pr);d['candidate_revision']=REV;d['edit_scope']=['REAR_SHOULDER_HAUNCH_CONTINUITY_ONLY'];d['visual_review_state']='NOT_RUN';
    if d.get('promotion_decision')=='PROMOTE_OVER_LKG':d['promotion_decision']='KEEP_LKG_HOLD_EXPERIMENT'
    return d
env['regression30']=regression39

def surface39():d=base_surface();d['revision']=REV;return d
env['surface_receipt']=surface39

def fold_diag(out):
    obj=bpy.data.objects.get('DIAG_PRE_APERTURE_VISUAL_HULL_V34');rows=[]
    if obj:
        me=obj.data;ef={}
        for p in me.polygons:
            for e in p.edge_keys:ef.setdefault(tuple(sorted(e)),[]).append(p.index)
        for e,fs in ef.items():
            if len(fs)==2:
                dot=float(me.polygons[fs[0]].normal.dot(me.polygons[fs[1]].normal))
                if dot<-.15:
                    c=(me.vertices[e[0]].co+me.vertices[e[1]].co)*.5;rows.append({'edge_vertices':list(e),'face_indices':fs,'normal_dot':dot,'center_m':[float(c.x),float(c.y),float(c.z)]})
    Path(out,'SURFACE_FOLD_DIAGNOSTIC.json').write_text(json.dumps({'schema':'oleander.3d.surface-fold-diagnostic.v1','candidate_revision':REV,'fold_count':len(rows),'folds':rows,'authority':'DIAGNOSTIC_NOT_REFERENCE_AUTHORITY'},indent=2)+'\n')
def patch39(out):
    base_patch(out);fold_diag(out)
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='REAR_SHOULDER_HAUNCH_CONTINUITY';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def run39():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:env['run30']()
    except SystemExit as e:patch39(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch39(out)
run39()
