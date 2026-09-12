#!/usr/bin/env python3
"""V47 — 911 visual-mass identity LKG experiment, aperture architecture explicitly HOLD.

V41/V45/V46 showed that iterating final aperture topology before the whole car reads as a 911 destroys first-read
quality. V47 freezes the V40 zero-fold Source and V43 SubD1 display strategy, restores identity-critical section
relief (hood valley / twin fender crowns, rear deck / wide haunch), adds a z-dependent upper-nose setback so the
front no longer reads as a vertical wall, and uses calibrated greenhouse glass + dark proxy backing ONLY for visual
mass evaluation. Proxy greenhouse does not prove/open final apertures; the contract keeps aperture architecture HOLD.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
V43=HERE/'run_reference_repro_v43.py';text=V43.read_text();marker='\nrun43()\n'
if marker not in text:raise SystemExit('V43 run marker missing')
ns={'__file__':str(V43),'__name__':'oleander_v47_declarations'};exec(compile(text.split(marker,1)[0],str(V43),'exec'),ns)
core=ns['core'];v=ns['v'];env=ns['env'];G=ns['G'];lerp=ns['lerp'];SIDE=ns['SIDE'];base_ring=ns['base_ring'];base_build=ns['base_build'];apply_subd=ns['apply_subd'];base_projection=ns['projection43'];base_regression=ns['regression43'];base_surface=ns['surface43'];base_patch=ns['base_patch'];tri_plane_top=ns['tri_plane_top'];components_and_edges=ns['components_and_edges']
FRONT=json.loads((HERE/'REFERENCE_FRONT_IDENTITY_TARGETS_992_2.json').read_text())
REV='V47_911_VISUAL_MASS_LKG_EXPERIMENT'
v.REF='2025_992.2_CARRERA_VISUAL_MASS_V47';v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v47';v.REFERENCE_CONTRACT['reference_revision']=v.REF;v.REFERENCE_CONTRACT['candidate_revision']=REV;v.REFERENCE_CONTRACT['primary_form_method']='V40_ZERO_FOLD_PLUS_CAUSAL_FRONT_REAR_RELIEF_AND_SUBD1';v.REFERENCE_CONTRACT['aperture_architecture_state']='HOLD_PROXY_GREENHOUSE_FOR_VISUAL_MASS_ONLY';v.REFERENCE_CONTRACT['proxy_does_not_prove']='host opening / flange / production aperture / final reference fidelity';v.FAMILY_CONTROLS['VISUAL_MASS_V47']={'front':['HOOD_VALLEY','TWIN_FENDER_CROWN','UPPER_NOSE_SETBACK','CALIBRATED_ROUND_LAMP'],'rear':['CENTER_DECK_RELIEF','WIDE_REAR_HAUNCH'],'greenhouse':'CALIBRATED_GLASS_PLUS_DARK_PROXY_BACKING_VISUAL_ONLY','protected':['V40_ZERO_FOLD_SOURCE','SIDE_OUTER_GESTURE','FRONT_REAR_GROSS_WIDTH_PROFILES','SIDE_LOWER','WHEELBASE','AXLE_CENTRES']};v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

# Identity relief is applied to interior transverse rails only. Outer side rail remains the SIDE silhouette authority.
def hull_ring47(x):
    ring=[list(p) for p in base_ring(x)];w=max(abs(p[1]) for p in ring) or 1.0
    fi=math.exp(-((float(x)-1.38)/.70)**4);ri=math.exp(-((float(x)+1.12)/.78)**4)
    for p in ring:
        xe,y,z=p;q=abs(y)/w
        if z>=.54:
            # Front: lower hood center, lift the crown band around lamp/fender; preserve q>=.95 side silhouette.
            if fi>.001:
                if q<.56:p[2]-=.058*fi*((1-q/.56)**1.45)
                elif .64<q<.93:
                    bell=max(0.,1-abs(q-.79)/.15);p[2]+=.036*fi*(bell**1.6)
            # Rear: lower center deck relative to the wide outer haunch, without moving the outer SIDE rail.
            if ri>.001:
                if q<.50:p[2]-=.034*ri*((1-q/.50)**1.35)
                elif .60<q<.93:
                    bell=max(0.,1-abs(q-.79)/.19);p[2]+=.032*ri*(bell**1.5)
        # Upper nose retreats from bumper plane. Lower bumper remains the terminal-most mass.
        if x>1.72 and z>.50:
            t=core['s01']((x-1.72)/(v.FRONT_X-1.72));shape=.65+.35*max(0.,min(1.,(z-.50)/.45));p[0]-=.205*t*shape*(.82+.18*q)
    return [tuple(p) for p in ring]
core['hull_ring']=hull_ring47;v.body_ring=hull_ring47

def build47(name,bodymat):
    o=base_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        apply_subd(o);d=o.copy();d.data=o.data.copy();d.name='DIAG_PRE_PROXY_GREENHOUSE_SURFACED_V47';bpy.context.collection.objects.link(d);d.hide_render=True;d.hide_set(True);d['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY';o['OLEANDER_FORM_FAMILY']='911_VISUAL_MASS_SURFACED_HULL_V47';o['OLEANDER_APERTURE_ARCHITECTURE']='HOLD_PROXY_GREENHOUSE'
    return o
core['build_visual_hull']=build47

# ----- calibrated greenhouse proxy backing + glass; explicitly NOT final host opening architecture -----
def interpG(x,field):
    x=float(x)
    if x<=G[0][0]:return G[0][field]
    if x>=G[-1][0]:return G[-1][field]
    for a,b in zip(G,G[1:]):
        if a[0]<=x<=b[0]:return lerp(a[field],b[field],(x-a[0])/(b[0]-a[0]))
    return G[-1][field]
def gy(x,z):
    w=core['plan_half_width'](x);raw=.5*v.WIDTH*core['profile_ratio'](x,z);return min(w-.004,max(.42,raw+.014))
def strip(name,pts,side,mat,offset=.0,authority='DERIVED_REFERENCE_REPRO_DETAIL'):
    verts=[];faces=[]
    for x,zt,zb in pts:
        yy=gy(x,(zt+zb)*.5)+offset;verts.extend([(x,side*yy,zt),(x,side*yy,zb)])
    for i in range(len(pts)-1):a=2*i;faces.append((a,a+1,a+3,a+2))
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']=authority
    for p in me.polygons:p.use_smooth=True
    return o

def proxy_glass47(M):
    out=[];bp=(-.20,interpG(-.20,1),interpG(-.20,2));q=[p for p in G if p[0]<-.20]+[bp];d=[bp]+[p for p in G if p[0]>-.20]
    for side,label in ((1,'L'),(-1,'R')):
        out.append(strip('V47_PROXY_QUARTER_BACKING_'+label,q,side,M['body_dark'],.006,'DERIVED_EXECUTION_NOT_AUTHORITY'));out.append(strip('V47_QUARTER_GLASS_'+label,q,side,M['glass'],.012,'DERIVED_APERTURE_INFILL'))
        out.append(strip('V47_PROXY_DOOR_BACKING_'+label,d,side,M['body_dark'],.006,'DERIVED_EXECUTION_NOT_AUTHORITY'));out.append(strip('V47_DOOR_GLASS_'+label,d,side,M['glass'],.012,'DERIVED_APERTURE_INFILL'))
        top=max(interpG(-.20,1),interpG(-.20,1));bot=min(interpG(-.20,2),interpG(-.20,2));yy=gy(-.20,(top+bot)*.5)+.014
        out.append(v.m.add_cube('V47_B_PILLAR_'+label,(-.20,side*yy,(top+bot)*.5),(.030,.016,max(.10,top-bot)),M['body_dark'],.002))
    # windshield + rear: dark backing slightly in front of the white host, glass slightly farther out. This is visual proxy only.
    ws=[(.650,.620,.830),(.650,-.620,.830),(.235,-.545,1.215),(.235,.545,1.215)];rg=[(-.390,.490,1.215),(-.390,-.490,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)]
    def panel(name,pts,mat,dx,auth):
        pp=[(x+dx,y,z) for x,y,z in pts];o=v.m.add_panel(name,pp,mat,.0015);o['OLEANDER_AUTHORITY']=auth;return o
    out += [panel('V47_PROXY_WINDSHIELD_BACKING',ws,M['body_dark'],.006,'DERIVED_EXECUTION_NOT_AUTHORITY'),panel('V47_WINDSHIELD',ws,M['glass'],.010,'DERIVED_APERTURE_INFILL')]
    out += [panel('V47_PROXY_REAR_BACKING',rg,M['body_dark'],-.006,'DERIVED_EXECUTION_NOT_AUTHORITY'),panel('V47_REAR_GLASS',rg,M['glass'],-.010,'DERIVED_APERTURE_INFILL')]
    return out
v.build_glass=proxy_glass47

# Front identity: calibrated lamp ratio, farther embedded into the sculpted fender crown; lower fascia kept subordinate.
def identity47(M):
    out=[];half=v.WIDTH*.5;cy=float(FRONT['measurement']['lamp_center_lateral_ratio_of_half_body_width'])*half;r=.5*float(FRONT['measurement']['visible_lamp_diameter_ratio_of_body_width'])*v.WIDTH
    for side in (1,-1):
        h=v.m.add_uv_sphere('V47_HEADLAMP_RECESS_'+str(side),(1.875,side*cy,.755),(.040,r*1.07,r*1.07),M['body_dark']);h['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(h)
        l=v.m.add_uv_sphere('V47_HEADLAMP_LENS_'+str(side),(1.908,side*cy,.755),(.020,r,r),M['glass']);l['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DETAIL';out.append(l)
        for dy in (-r*.29,r*.29):
            for dz in (-r*.29,r*.29):out.append(v.m.add_cube(f'V47_HEADLAMP_PIXEL_{side}_{dy}_{dz}',(1.928,side*cy+dy,.755+dz),(.006,.012,.012),M['headlamp'],.003))
    out.append(v.m.add_cube('V47_FRONT_CENTER_INTAKE',(2.205,0,.285),(.018,.330,.072),M['body_dark'],.030))
    for side in (1,-1):out.append(v.m.add_cube('V47_FRONT_SIDE_INTAKE_'+str(side),(2.170,side*.545,.305),(.018,.205,.105),M['body_dark'],.040))
    out.append(v.m.add_cube('V47_FRONT_SPLITTER',(2.205,0,.177),(.016,1.220,.014),M['body_dark'],.007))
    # restrained rear identity cues from the stable prior system.
    out.append(v.m.add_cube('V47_REAR_LIGHTBAR',(-2.150,0,.660),(.018,1.360,.035),M['rear_light'],.012))
    return out
v.build_identity=identity47

# Measure primary form on the surfaced shell before proxy greenhouse.
def projection47():
    d=base_projection();d['candidate_revision']=REV;d['primary_form_stage']='VISUAL_MASS_PROXY_APERTURE_HOLD';diag=bpy.data.objects.get('DIAG_PRE_PROXY_GREENHOUSE_SURFACED_V47');errs=[];samples=[]
    for x,z in SIDE:
        cand=tri_plane_top(diag,x) if diag else float('nan');e=cand-z if math.isfinite(cand) else float('nan');samples.append({'x':x,'target_top':z,'candidate_top':cand,'top_error_m':e,'reference_target_source':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m','candidate_measurement_source':'V47_SURFACED_VISUAL_MASS_TRIANGLE_X_PLANE'});errs.append(e) if math.isfinite(e) else None
    rmse=math.sqrt(sum(e*e for e in errs)/len(errs)) if errs else 9.;d['side_upper_samples']=samples
    for m in d['metrics']:
        if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M':m['candidate']=rmse;m['abs_error']=rmse;m['candidate_measurement_source']='V47_SURFACED_VISUAL_MASS_TRIANGLE_X_PLANE';m['finite_sample_coverage']=len(errs)/len(SIDE)
        else:m['candidate_measurement_source']=str(m.get('candidate_measurement_source','')).replace('V43_','V47_')
    d['side_upper_finite_sample_coverage']=len(errs)/len(SIDE);d['aperture_architecture_state']='HOLD_PROXY_GREENHOUSE_FOR_VISUAL_MASS_ONLY';d['status']='PROJECTION_MACHINE_SCREENING_PASS' if len(errs)/len(SIDE)>=.90 and all(math.isfinite(float(m['abs_error'])) and float(m['abs_error'])<=float(m['limit']) for m in d['metrics']) else 'PROJECTION_MACHINE_SCREENING_FAIL';return d
env['projection30']=projection47

def regression47(pr):
    d=base_regression(pr);d['candidate_revision']=REV;d['edit_scope']=['FRONT_HOOD_FENDER_RELIEF','UPPER_NOSE_SETBACK','REAR_DECK_HAUNCH_RELIEF','CALIBRATED_PROXY_GREENHOUSE'];d['visual_review_state']='NOT_RUN'
    if d.get('promotion_decision')=='PROMOTE_OVER_LKG':d['promotion_decision']='KEEP_LKG_HOLD_EXPERIMENT'
    return d
env['regression30']=regression47

def surface47():d=base_surface();d['revision']=REV;return d
env['surface_receipt']=surface47

# Final surface topology is intentionally not claimed because aperture architecture is proxy/HOLD.
def proxy_receipt(out):
    d={'schema':'oleander.3d.visual-mass-proxy-receipt.v1','candidate_revision':REV,'primary_surface':'V40_ZERO_FOLD_SOURCE_PLUS_SUBD1','greenhouse_representation':'CALIBRATED_DARK_BACKING_PLUS_GLASS_PROXY','aperture_architecture_state':'HOLD_NOT_CONSTRUCTED','visual_review_state':'NOT_RUN','machine_state':'MACHINE_VISUAL_MASS_READY_FOR_REVIEW','does_not_prove':['reference fidelity','true host opening','aperture flange','Class-A continuity','manufacturer CAD','production feasibility']}
    Path(out,'VISUAL_MASS_PROXY_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def patch47(out):
    base_patch(out);proxy_receipt(out)
    # Remove inherited final-surface receipt: this revision intentionally does not claim final aperture construction.
    p=Path(out,'FINAL_DERIVED_SURFACE_RECEIPT.json')
    if p.exists():p.unlink()
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():
            d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='VISUAL_MASS_PROXY_APERTURE_HOLD';d['aperture_architecture_state']='HOLD_PROXY_ONLY';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
ns['patch43']=patch47

def run47():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:env['run30']()
    except SystemExit as e:patch47(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch47(out)
run47()
