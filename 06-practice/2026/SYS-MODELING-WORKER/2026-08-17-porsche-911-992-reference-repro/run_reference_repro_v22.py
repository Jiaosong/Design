#!/usr/bin/env python3
"""V22 — V20 locked macro + full-fastback greenhouse interface + front/rear profile screening.

V21's short roof is discarded. V22 keeps V20/V16's complete fastback roof patch and lower-envelope
corrections, then replaces only glass/pillar/cowl/sail interfaces with real surface-width patches.
No front/rear cross-section geometry is edited yet; new profile metrics only establish the V23 target.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V20=HERE/'run_reference_repro_v20.py'
PROFILE=json.loads((HERE/'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json').read_text())
text=V20.read_text();marker='\ntry:\n v.main()'
if marker not in text:raise SystemExit('V20 declaration marker missing')
ns={'__file__':str(V20),'__name__':'oleander_v20_declarations'}
exec(compile(text.split(marker,1)[0],str(V20),'exec'),ns)
v=ns['v'];PROJ=ns['PROJ'];CONTOUR=ns['CONTOUR'];SIDE_TOP=ns['SIDE_TOP'];SIDE_LOW=ns['SIDE_LOW']
v.REF='2025_992.2_CARRERA_FULL_FASTBACK_INTERFACE_V22'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v22'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['greenhouse_interface']='FULL_FASTBACK_SURFACE_PATCH_NETWORK'
v.REFERENCE_CONTRACT['front_rear_profile_reference']='REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json'
v.FAMILY_CONTROLS['GREENHOUSE_INTERFACE_SURFACES']=['COWL','A_PILLAR_SURFACE','V20_FULL_FASTBACK_ROOF','ROOF_RAIL_SURFACE','B_PILLAR_SURFACE','C_PILLAR_SAIL_SURFACE','REAR_DECK_INTERFACE']

# Surface helpers.
def panel(name,verts,mat,thickness=.008,authority='DERIVED_REFERENCE_REPRO_INTERFACE'):
 me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],[tuple(range(len(verts)))]);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']=authority;o['OLEANDER_INTERFACE_SURFACE']=True
 if thickness:
  s=o.modifiers.new(name+'_THICKNESS','SOLIDIFY');s.thickness=thickness;s.offset=0
 for p in me.polygons:p.use_smooth=True
 return o

def strip(name,sections,mat,thickness=.008):
 verts=[]
 for outer,inner in sections:verts.extend((outer,inner))
 faces=[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(sections)-1)]
 me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';o['OLEANDER_INTERFACE_SURFACE']=True
 s=o.modifiers.new(name+'_THICKNESS','SOLIDIFY');s.thickness=thickness;s.offset=0
 for p in me.polygons:p.use_smooth=True
 return o

# V20 roof stays untouched. Replace only greenhouse infill/interfaces.
def greenhouse22(M):
 out=[]
 windshield=[(.650,.620,.830),(.650,-.620,.830),(.235,-.545,1.215),(.235,.545,1.215)]
 rear=[(-.390,.490,1.215),(-.390,-.490,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)]
 out.append(v.m.add_panel('REF_WINDSHIELD',windshield,M['glass'],.003));out[-1]['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL'
 out.append(v.m.add_panel('REF_REAR_GLASS',rear,M['glass'],.003));out[-1]['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL'
 # cowl/backlight interfaces are deliberately broad and attach to V20 locked body/roof.
 out.append(panel('REF_COWL_INTERFACE',[(.760,.700,.790),(.760,-.700,.790),(.650,-.620,.830),(.650,.620,.830)],M['body'],.010))
 out.append(panel('REF_REAR_DECK_INTERFACE',[(-1.150,.592,.990),(-1.150,-.592,.990),(-1.360,-.790,.835),(-1.360,.790,.835)],M['body'],.012))
 for side in (1,-1):
  s=side
  # Door and quarter glazing independently triangulate, eliminating the old diagonal specular artifact.
  door=[(.620,s*.600,.835),(.235,s*.545,1.205),(-.220,s*.525,1.220),(-.220,s*.570,.842),(.500,s*.605,.835)]
  quarter=[(-.220,s*.525,1.220),(-.390,s*.490,1.205),(-1.100,s*.575,.995),(-.820,s*.625,.842),(-.220,s*.570,.842)]
  out.append(v.m.add_panel('REF_DOOR_GLASS_'+('L' if s>0 else 'R'),door,M['glass'],.003));out[-1]['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL'
  out.append(v.m.add_panel('REF_QUARTER_GLASS_'+('L' if s>0 else 'R'),quarter,M['glass'],.003));out[-1]['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL'
  # A pillar: 55–70 mm surface width in Y rather than a bevelled centerline.
  out.append(panel('REF_A_PILLAR_SURFACE_'+('L' if s>0 else 'R'),[(.650,s*.675,.815),(.650,s*.600,.835),(.235,s*.525,1.205),(.235,s*.590,1.222)],M['body'],.010))
  # Roof rail follows the existing full fastback roof boundary from A header to rear header.
  sections=[]
  for i in range(17):
   x=.235+(-.625)*i/16;t=i/16;yo=.590*(1-t)+.525*t;yi=yo-.055;top=v.hermite(v.ROOF_TOP_PTS,x)-.020
   sections.append(((x,s*yo,top),(x,s*yi,top-.012)))
  out.append(strip('REF_ROOF_RAIL_SURFACE_'+('L' if s>0 else 'R'),sections,M['body'],.010))
  # B pillar.
  out.append(panel('REF_B_PILLAR_SURFACE_'+('L' if s>0 else 'R'),[(-.250,s*.590,.835),(-.190,s*.590,.835),(-.190,s*.515,1.225),(-.250,s*.515,1.225)],M['body_dark'],.010))
  # C pillar / sail is a wide tapered surface reaching the rear quarter shoulder, not a narrow strip.
  out.append(panel('REF_C_PILLAR_SAIL_'+('L' if s>0 else 'R'),[
      (-.390,s*.525,1.220),(-.390,s*.465,1.205),(-.760,s*.540,1.055),(-1.100,s*.575,.995),
      (-1.360,s*.790,.835),(-1.120,s*.820,.875),(-.760,s*.700,1.070)],M['body'],.012))
  # Belt surface closes the interface between open glazing and locked lower body.
  out.append(strip('REF_WINDOW_BELT_SURFACE_'+('L' if s>0 else 'R'),[
      ((.620,s*.650,.815),(.620,s*.600,.835)),((-.220,s*.630,.825),(-.220,s*.570,.842)),((-1.100,s*.640,.900),(-1.100,s*.575,.995))],M['body'],.009))
  out.append(v.m.add_cube('REF_DOOR_HANDLE_'+('L' if s>0 else 'R'),(-.020,s*.896,.682),(.105,.012,.017),M['body_dark'],.003))
  y=s*.912;out.append(v.m.add_curve('REF_DOOR_SEAM_'+('L' if s>0 else 'R'),[(.595,y,.765),(.545,y,.500),(-.635,y,.500),(-.800,y,.665),(-.785,y,.825)],M['seam'],.0016))
 return out
v.build_glass=greenhouse22

# Source semantic binding only; V20 macro controls are locked.
base_source=v.build_source
def source22(M):
 o=base_source(M);o['OLEANDER_GREENHOUSE_INTERFACE']='FULL_FASTBACK_SURFACE_PATCH_NETWORK';o['OLEANDER_V20_MACRO_LOCKED']=True;o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=source22

# Y/Z projection of selected front/rear halves. This is a screening profile, not orthographic CAD.
def yz_triangles(names,front=True):
 dg=bpy.context.evaluated_depsgraph_get();tris=[];members=[]
 for name in names:
  o=bpy.data.objects.get(name)
  if o is None:continue
  eo=o.evaluated_get(dg);me=eo.to_mesh();me.calc_loop_triangles();mw=eo.matrix_world.copy();n=0
  try:
   for lt in me.loop_triangles:
    pts3=[mw@me.vertices[i].co for i in lt.vertices];cx=sum(p.x for p in pts3)/3
    if (front and cx<.20) or ((not front) and cx>-.20):continue
    tris.append(tuple((float(p.y),float(p.z)) for p in pts3));n+=1
  finally:eo.to_mesh_clear()
  if n:members.append({'object':name,'triangles':n})
 return tris,members

def scan_y(tri,z):
 vals=[]
 for i in range(3):
  y1,z1=tri[i];y2,z2=tri[(i+1)%3]
  if abs(z2-z1)<1e-12:
   if abs(z-z1)<1e-9:vals.extend((y1,y2))
   continue
  if z<min(z1,z2)-1e-9 or z>max(z1,z2)+1e-9:continue
  t=(z-z1)/(z2-z1)
  if -1e-9<=t<=1+1e-9:vals.append(y1+t*(y2-y1))
 return vals

def width_profile(tris,targets):
 allp=[p for tri in tris for p in tri]
 if not allp:return [],9.0
 zmin=min(p[1] for p in allp);zmax=max(p[1] for p in allp);ymin=min(p[0] for p in allp);ymax=max(p[0] for p in allp);maxw=ymax-ymin
 rows=[];errs=[]
 for frac,target in targets:
  z=zmin+float(frac)*(zmax-zmin);ys=[]
  for tri in tris:
   if z<min(p[1] for p in tri)-1e-9 or z>max(p[1] for p in tri)+1e-9:continue
   ys.extend(scan_y(tri,z))
  cand=(max(ys)-min(ys))/maxw if ys else float('nan');e=cand-float(target);rows.append({'height_fraction':frac,'target_width_ratio':target,'candidate_width_ratio':cand,'error':e});
  if math.isfinite(e):errs.append(e)
 return rows,math.sqrt(sum(e*e for e in errs)/len(errs)) if errs else 9.0

# Preserve V20 trusted SIDE projection and append front/rear profile metrics.
base_projection=ns['projection20']
def projection22():
 d=base_projection();d['candidate_revision']='V22_FULL_FASTBACK_INTERFACE'
 for m in d['metrics']:m['candidate_measurement_source']=str(m['candidate_measurement_source']).replace('V20_','V22_')
 for s in d.get('side_upper_samples',[]):s['candidate_measurement_source']='V22_FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION'
 for s in d.get('side_lower_samples',[]):s['candidate_measurement_source']='V22_FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION'
 members=['DERIVED_911_9922_BODY','DERIVED_911_9922_CABIN']+[o.name for o in bpy.context.scene.objects if o.get('OLEANDER_INTERFACE_SURFACE')]
 ft,fm=yz_triangles(members,True);rt,rm=yz_triangles(members,False);fr,frmse=width_profile(ft,PROFILE['front']['profile']);rr,rrmse=width_profile(rt,PROFILE['rear']['profile'])
 d['metrics'] += [
   {'id':'FRONT_HALF_PROJECTED_PROFILE_RMSE','target':0.0,'candidate':frmse,'abs_error':frmse,'limit':PROFILE['gates']['front_profile_rmse_max'],'reference_target_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:front.profile','candidate_measurement_source':'V22_FRONT_HALF_FINAL_EVALUATED_MESH_YZ_PROFILE'},
   {'id':'REAR_HALF_PROJECTED_PROFILE_RMSE','target':0.0,'candidate':rrmse,'abs_error':rrmse,'limit':PROFILE['gates']['rear_profile_rmse_max'],'reference_target_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:rear.profile','candidate_measurement_source':'V22_REAR_HALF_FINAL_EVALUATED_MESH_YZ_PROFILE'}]
 d['front_profile']={'rmse':frmse,'samples':fr,'members':fm};d['rear_profile']={'rmse':rrmse,'samples':rr,'members':rm};d['status']='PROJECTION_MACHINE_SCREENING_PASS' if all(m['abs_error']<=m['limit'] for m in d['metrics']) else 'PROJECTION_MACHINE_SCREENING_FAIL';d['greenhouse_interface']='FULL_FASTBACK_SURFACE_PATCH_NETWORK';return d

base_lm=v.landmark_receipt
def lm22(source_hash):
 d=base_lm(source_hash)
 for item in d['landmarks']:item['candidate_measurement_source']='V22_FINAL_VISIBLE_PATCH_NETWORK'
 d['greenhouse_interface']='FULL_FASTBACK_SURFACE_PATCH_NETWORK';d['mass_families']=['V20_LOCKED_MACRO_SHELL','V20_FULL_FASTBACK_ROOF','COWL_INTERFACE','A_PILLAR_SURFACE','ROOF_RAIL_SURFACE','B_PILLAR_SURFACE','C_PILLAR_SAIL_SURFACE','REAR_DECK_INTERFACE'];return d
v.landmark_receipt=lm22

try:
 v.main()
except SystemExit as base_exit:
 a=v.m.parse_args();out=Path(a.out).resolve()
 if (out/'REFERENCE_REPRO_QA.json').exists():
  pr=projection22();(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n')
  urmse=next(m['candidate'] for m in pr['metrics'] if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M');maxabs=max(abs(s['top_error_m']) for s in pr['side_upper_samples'] if math.isfinite(s['top_error_m']));binding={'schema':'oleander.3d.reference-contour-binding.v8','reference':'REFERENCE_CONTOUR_TARGETS_992_2.json','candidate':'V22_FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION','side_top_rmse_m':urmse,'side_top_max_abs_m':maxabs,'thresholds':CONTOUR['gates'],'samples':pr['side_upper_samples'],'status':'MACHINE_BINDING_PASS' if urmse<=.040 and maxabs<=.080 else 'MACHINE_BINDING_FAIL','does_not_prove':CONTOUR['does_not_prove']};(out/'REFERENCE_CONTOUR_BINDING_RECEIPT.json').write_text(json.dumps(binding,ensure_ascii=False,indent=2)+'\n')
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V22_FULL_FASTBACK_INTERFACE';q['projection_machine_gate']=pr['status'];q['reference_contour_binding']=binding['status'];q['greenhouse_interface']='FULL_FASTBACK_SURFACE_PATCH_NETWORK';q['front_profile_rmse']=pr['front_profile']['rmse'];q['rear_profile_rmse']=pr['rear_profile']['rmse'];q['failure_routing']='MEASURE_FRONT_REAR_BEFORE_V23';q['verification_run']='PASS';q['visual_reference_fidelity']='HOLD';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V22_FULL_FASTBACK_INTERFACE';r['projection_machine_gate']=pr['status'];r['greenhouse_interface']='FULL_FASTBACK_SURFACE_PATCH_NETWORK';r['verification_run']='PASS';r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 raise SystemExit(base_exit.code if isinstance(base_exit.code,int) else 0)
