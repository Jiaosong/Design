#!/usr/bin/env python3
"""V41 — true greenhouse apertures + stable terminal screening on the V40 zero-fold hull.

V40 achieved a zero-fold pre-aperture primary skin and good FRONT/REAR projected mass, but the visible body still
ran opaque behind independent glass. Its SIDE RMSE was also dominated by an unstable exact front-extreme triangle
intersection. V41 preserves V40 geometry, cuts real greenhouse host openings only AFTER the pre-aperture diagnostic
copy is created, embeds independent glazing, refines the round front lamp integration, and separates dominant SIDE
gesture from near-terminal form checks.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy,bmesh
HERE=Path(__file__).resolve().parent
V40=HERE/'run_reference_repro_v40.py';text=V40.read_text();marker='\nrun40()\n'
if marker not in text:raise SystemExit('V40 run marker missing')
outer={'__file__':str(V40),'__name__':'oleander_v41_declarations'};exec(compile(text.split(marker,1)[0],str(V40),'exec'),outer)
core=outer['ns'];v=outer['v'];env=outer['env'];PROFILE=outer['PROFILE'];metric=outer['metric'];G=outer['G'];lerp=outer['lerp'];REV='V41_TRUE_APERTURE_STABLE_TERMINAL'
base_build=outer['build40'];base_projection=outer['projection40'];base_regression=outer['regression40'];base_surface=outer['surface40'];base_patch=outer['patch40'];base_identity=v.build_identity
v.REF='2025_992.2_CARRERA_TRUE_APERTURE_V41';v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v41';v.REFERENCE_CONTRACT['reference_revision']=v.REF;v.REFERENCE_CONTRACT['candidate_revision']=REV;v.REFERENCE_CONTRACT['primary_form_method']='V40_ZERO_FOLD_SKIN_PLUS_TRUE_GREENHOUSE_APERTURES';v.REFERENCE_CONTRACT['terminal_screening']='DOMINANT_GESTURE_EXCLUDES_EXACT_EXTREMA_PLUS_NEAR_TERMINAL_GATES';v.FAMILY_CONTROLS['TRUE_APERTURE_V41']={'greenhouse':'REFERENCE_GREENHOUSE_TARGETS_992_2.json','host_opening':'DELETE_FINAL_BODY_FACES_AFTER_PRE_APERTURE_DIAGNOSTIC','front_lamp':'SOURCE_GROUNDED_FRONT_IMAGE_ROUND_LAMP_RELATION','terminal_screening':['x=-2.10m','x=+2.05m'],'protected':['V40_PRE_APERTURE_SKIN','REAR_PROFILE','FRONT_PROFILE','SIDE_LOWER','WHEELBASE','AXLE_CENTRES']};v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

def interpG(x,field):
    x=float(x)
    if x<=G[0][0]:return G[0][field]
    if x>=G[-1][0]:return G[-1][field]
    for a,b in zip(G,G[1:]):
        if a[0]<=x<=b[0]:return lerp(a[field],b[field],(x-a[0])/(b[0]-a[0]))
    return G[-1][field]

def windshield_lower(x):
    return lerp(1.215,.830,max(0.0,min(1.0,(float(x)-.235)/(.650-.235))))
def rear_glass_lower(x):
    return lerp(.990,1.215,max(0.0,min(1.0,(float(x)+1.150)/(-.390+1.150))))

def aperture_kind(x,y,z):
    ay=abs(y)
    # side glazing: only outer side faces, directly from calibrated greenhouse top/bottom envelope.
    if G[0][0]<=x<=G[-1][0] and ay>.34:
        top=interpG(x,1);bot=interpG(x,2)
        if bot-.012<=z<=top+.010:return 'SIDE_GLASS'
    # windshield: broad central opening bounded below by the calibrated panel line and above by primary roof gesture.
    if .235<=x<=.650 and ay<.66:
        lo=windshield_lower(x)
        if lo-.015<=z<=core['side_top'](x)-.012:return 'WINDSHIELD'
    # rear backlight: central sloping opening; side quarter glazing remains owned by side envelope.
    if -1.150<=x<=-.390 and ay<.64:
        lo=rear_glass_lower(x)
        if lo-.015<=z<=core['side_top'](x)-.014:return 'REAR_GLASS'
    return None

def cut_host_faces(obj):
    bm=bmesh.new();bm.from_mesh(obj.data);kill=[];counts={}
    for f in bm.faces:
        c=f.calc_center_median();k=aperture_kind(float(c.x),float(c.y),float(c.z))
        if k:kill.append(f);counts[k]=counts.get(k,0)+1
    if kill:bmesh.ops.delete(bm,geom=kill,context='FACES')
    bm.to_mesh(obj.data);bm.free();obj.data.update();obj['OLEANDER_TRUE_APERTURE_FACE_COUNTS']=json.dumps(counts,sort_keys=True);obj['OLEANDER_OPAQUE_HOST_THROUGH_GLAZING']=False;return counts

def build41(name,bodymat):
    o=base_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        counts=cut_host_faces(o);o['OLEANDER_FORM_FAMILY']='V40_ZERO_FOLD_SKIN_TRUE_APERTURE_V41';o['OLEANDER_APERTURE_STAGE']='TRUE_HOST_OPENING_PLUS_INDEPENDENT_GLASS';o['OLEANDER_APERTURE_FACE_COUNT_TOTAL']=sum(counts.values())
    return o
core['build_visual_hull']=build41

# Identity stage: replace the old half-buried lamps and flat fascia blocks with restrained round recessed modules.
def identity41(M):
    out=base_identity(M)
    for name in list(bpy.data.objects.keys()):
        if name.startswith('REF_HEADLAMP_HOUSING_') or name.startswith('REF_HEADLAMP_LENS_') or name.startswith('REF_FRONT_CENTER_INTAKE') or name.startswith('REF_FRONT_SIDE_INTAKE_') or name.startswith('REF_FRONT_SPLITTER'):
            o=bpy.data.objects.get(name)
            if o:o.hide_render=True
    for side in (1,-1):
        h=v.m.add_uv_sphere('V41_HEADLAMP_RECESS_'+str(side),(1.790,side*.675,.770),(.055,.165,.165),M['body_dark']);h['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(h)
        l=v.m.add_uv_sphere('V41_HEADLAMP_LENS_'+str(side),(1.842,side*.675,.770),(.032,.148,.148),M['headlamp']);l['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DETAIL';out.append(l)
    # Dark fascia remains subordinate to primary body; use rounded narrow masses instead of full-width flat wall cues.
    c=v.m.add_cube('V41_FRONT_CENTER_INTAKE',(2.205,0,.292),(.020,.390,.090),M['body_dark'],.035);c['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DETAIL';out.append(c)
    for side in (1,-1):
        q=v.m.add_cube('V41_FRONT_SIDE_INTAKE_'+str(side),(2.185,side*.560,.305),(.022,.235,.125),M['body_dark'],.045);q['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DETAIL';out.append(q)
    sp=v.m.add_cube('V41_FRONT_SPLITTER',(2.205,0,.177),(.018,1.300,.018),M['body_dark'],.008);sp['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DETAIL';out.append(sp)
    return out
v.build_identity=identity41

# Stable SIDE gesture: exact extrema are non-area caps and may return NaN or a lower cap vertex. Use interior silhouette
# for gesture and explicit near-terminal checkpoints for terminal form; official length remains an independent hard point.
def projection41():
    d=base_projection();d['candidate_revision']=REV;d['primary_form_stage']='TRUE_APERTURE_STABLE_TERMINAL';samples=d.get('side_upper_samples',[])
    interior=[]
    for s in samples:
        x=float(s['x']);e=s.get('top_error_m')
        if -2.10<=x<=2.05 and isinstance(e,(int,float)) and math.isfinite(float(e)):interior.append(float(e))
    rmse=math.sqrt(sum(e*e for e in interior)/len(interior)) if interior else 9.0
    for m in d['metrics']:
        if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M':m['candidate']=rmse;m['abs_error']=rmse;m['candidate_measurement_source']='V41_FINAL_EVALUATED_HULL_INTERIOR_GESTURE_X[-2.10,2.05]';m['finite_sample_coverage']=len(interior)/max(1,len([s for s in samples if -2.10<=float(s['x'])<=2.05]))
        else:m['candidate_measurement_source']=str(m.get('candidate_measurement_source','')).replace('V40_','V41_')
    for xid,mid in ((-2.10,'REAR_NEAR_TERMINAL_TOP_ERROR_M'),(2.05,'FRONT_NEAR_TERMINAL_TOP_ERROR_M')):
        s=min(samples,key=lambda a:abs(float(a['x'])-xid));err=abs(float(s['top_error_m'])) if isinstance(s.get('top_error_m'),(int,float)) and math.isfinite(float(s['top_error_m'])) else 9.0
        d['metrics'].append({'id':mid,'target':0.0,'candidate':err,'abs_error':err,'limit':.055,'reference_target_source':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m','candidate_measurement_source':'V41_FINAL_EVALUATED_HULL_NEAR_TERMINAL'})
    d['side_terminal_semantics']='OFFICIAL_LENGTH_EXACT_PLUS_NEAR_TERMINAL_TOP_AT_-2.10_+2.05';d['greenhouse_representation']='TRUE_HOST_APERTURES_PLUS_INDEPENDENT_GLASS';d['status']='PROJECTION_MACHINE_SCREENING_PASS' if all(math.isfinite(float(m['abs_error'])) and float(m['abs_error'])<=float(m['limit']) for m in d['metrics']) else 'PROJECTION_MACHINE_SCREENING_FAIL';return d
env['projection30']=projection41

def regression41(pr):
    d=base_regression(pr);d['candidate_revision']=REV;d['edit_scope']=['TRUE_GREENHOUSE_APERTURES','ROUND_HEADLAMP_INTEGRATION','STABLE_TERMINAL_SCREENING'];d['visual_review_state']='NOT_RUN'
    # base regression compares the robust core metrics only; new near-terminal gates are extra fail-closed evidence.
    if d.get('promotion_decision')=='PROMOTE_OVER_LKG':d['promotion_decision']='KEEP_LKG_HOLD_EXPERIMENT'
    return d
env['regression30']=regression41

def surface41():d=base_surface();d['revision']=REV;return d
env['surface_receipt']=surface41

def patch41(out):
    base_patch(out)
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():
            d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='TRUE_APERTURE_STABLE_TERMINAL';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
outer['patch40']=patch41

def run41():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:env['run30']()
    except SystemExit as e:patch41(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch41(out)
run41()
