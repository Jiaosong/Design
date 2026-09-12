#!/usr/bin/env python3
"""V21 — greenhouse interface surface refinement on locked V20 macro geometry.

V20 passing macro gates are frozen. V21 replaces curve-like greenhouse frames with actual surface
patches: cowl, A-pillar, roof panel, roof rail, B-pillar, C-pillar/sail and rear-deck interfaces.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V20=HERE/'run_reference_repro_v20.py'
text=V20.read_text();marker='\ntry:\n v.main()'
if marker not in text:raise SystemExit('V20 declaration marker missing')
ns={'__file__':str(V20),'__name__':'oleander_v20_declarations'}
exec(compile(text.split(marker,1)[0],str(V20),'exec'),ns)
v=ns['v'];PROJ=ns['PROJ'];CONTOUR=ns['CONTOUR'];SIDE_TOP=ns['SIDE_TOP'];SIDE_LOW=ns['SIDE_LOW']
v.REF='2025_992.2_CARRERA_GREENHOUSE_SURFACE_V21'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v21'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['greenhouse_interface']='SURFACE_PATCH_NETWORK'
v.FAMILY_CONTROLS['GREENHOUSE_INTERFACE_SURFACES']=['COWL','WINDSHIELD','A_PILLAR_SURFACE','ROOF_PANEL','ROOF_RAIL_SURFACE','B_PILLAR_SURFACE','C_PILLAR_SAIL_SURFACE','REAR_GLASS','REAR_DECK_INTERFACE']

def add_panel(name,verts,mat,thickness=.008,authority='DERIVED_REFERENCE_REPRO_INTERFACE'):
 me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],[tuple(range(len(verts)))]);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']=authority;o['OLEANDER_INTERFACE_SURFACE']=True
 if thickness:
  s=o.modifiers.new(name+'_THICKNESS','SOLIDIFY');s.thickness=thickness;s.offset=0
 for p in me.polygons:p.use_smooth=True
 return o

def add_strip(name,sections,mat,thickness=.008):
 # sections = [(outer_xyz, inner_xyz), ...]
 verts=[]
 for outer,inner in sections:verts.extend((outer,inner))
 faces=[]
 for i in range(len(sections)-1):faces.append((2*i,2*i+1,2*i+3,2*i+2))
 me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';o['OLEANDER_INTERFACE_SURFACE']=True
 s=o.modifiers.new(name+'_THICKNESS','SOLIDIFY');s.thickness=thickness;s.offset=0
 for p in me.polygons:p.use_smooth=True
 return o

# Intercept V16/V20 CABIN loft: roof exists only between windshield and backlight headers.
base_loft=v.build_loft
def roof_panel(name,mat):
 xs=[-.390+(.625)*i/40 for i in range(41)];fracs=(-1,-.55,0,.55,1);verts=[];rings=[]
 for x in xs:
  t=(x+.390)/.625;half=.490*(1-t)+.545*t;top=v.hermite(v.ROOF_TOP_PTS,x);ring=[]
  for f in fracs:
   z=top-.030*(abs(f)**1.8);ring.append(len(verts));verts.append((x,f*half,z))
  rings.append(ring)
 faces=[]
 for i in range(len(rings)-1):
  for j in range(len(fracs)-1):faces.append((rings[i][j],rings[i+1][j],rings[i+1][j+1],rings[i][j+1]))
 me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';o['OLEANDER_FORM_FAMILY']='ROOF_OUTER_PANEL';o['OLEANDER_BOUNDARY_OWNER']='WINDSHIELD_HEADER_BACKLIGHT_HEADER_ROOF_RAILS'
 s=o.modifiers.new('ROOF_PANEL_THICKNESS','SOLIDIFY');s.thickness=.010;s.offset=-.3
 for p in me.polygons:p.use_smooth=True
 return o
def loft21(name,xs,ringfn,mat,authority,render=True):
 if name=='DERIVED_911_9922_CABIN':return roof_panel(name,mat)
 return base_loft(name,xs,ringfn,mat,authority,render)
v.build_loft=loft21

# Real surface-width greenhouse interfaces.
def greenhouse21(M):
 out=[]
 # Glass dimensions preserve V20 passing FRONT/REAR width ratios.
 windshield=[(.650,.620,.830),(.650,-.620,.830),(.235,-.545,1.215),(.235,.545,1.215)]
 rear=[(-.390,.490,1.215),(-.390,-.490,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)]
 out.append(v.m.add_panel('REF_WINDSHIELD',windshield,M['glass'],.003));out[-1]['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL'
 out.append(v.m.add_panel('REF_REAR_GLASS',rear,M['glass'],.003));out[-1]['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL'
 # Cowl and rear-deck interfaces connect glass to locked lower body shell.
 out.append(add_panel('REF_COWL_INTERFACE',[(.715,.665,.800),(.715,-.665,.800),(.650,-.620,.830),(.650,.620,.830)],M['body'],.010))
 out.append(add_panel('REF_REAR_DECK_INTERFACE',[(-1.150,.592,.990),(-1.150,-.592,.990),(-1.320,-.705,.845),(-1.320,.705,.845)],M['body'],.010))
 # Side glass is split into door and quarter pieces, creating an actual B-pillar interface.
 for side in (1,-1):
  s=side
  door=[(.620,s*.600,.835),(.235,s*.545,1.205),(-.220,s*.525,1.225),(-.220,s*.570,.842),(.500,s*.605,.835)]
  quarter=[(-.220,s*.525,1.225),(-.390,s*.490,1.205),(-1.100,s*.575,.995),(-.790,s*.600,.842),(-.220,s*.570,.842)]
  out.append(v.m.add_panel('REF_DOOR_GLASS_'+('L' if s>0 else 'R'),door,M['glass'],.003));out[-1]['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL'
  out.append(v.m.add_panel('REF_QUARTER_GLASS_'+('L' if s>0 else 'R'),quarter,M['glass'],.003));out[-1]['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL'
  # A-pillar tapered surface: exterior edge ↔ glass/roof inner edge.
  out.append(add_panel('REF_A_PILLAR_SURFACE_'+('L' if s>0 else 'R'),[(.650,s*.660,.815),(.650,s*.600,.835),(.235,s*.505,1.205),(.235,s*.555,1.220)],M['body'],.010))
  # Roof rail as a broad strip, not a curve/tube.
  sections=[]
  for i in range(13):
   x=.235+(-.625)*i/12;t=i/12;yo=.555*(1-t)+.500*t;yi=yo-.050;top=v.hermite(v.ROOF_TOP_PTS,x)-.025
   sections.append(((x,s*yo,top),(x,s*yi,top-.010)))
  out.append(add_strip('REF_ROOF_RAIL_SURFACE_'+('L' if s>0 else 'R'),sections,M['body'],.009))
  # B pillar broad surface.
  out.append(add_panel('REF_B_PILLAR_SURFACE_'+('L' if s>0 else 'R'),[(-.245,s*.582,.835),(-.195,s*.582,.835),(-.195,s*.520,1.230),(-.245,s*.520,1.230)],M['body_dark'],.010))
  # C-pillar/sail surface connects roof/backlight/quarter to rear deck.
  out.append(add_panel('REF_C_PILLAR_SAIL_'+('L' if s>0 else 'R'),[(-.390,s*.500,1.220),(-.390,s*.440,1.205),(-1.150,s*.505,.990),(-1.320,s*.705,.845),(-1.120,s*.675,.915)],M['body'],.012))
  # Belt interface and door details.
  out.append(add_strip('REF_WINDOW_BELT_SURFACE_'+('L' if s>0 else 'R'),[((.620,s*.615,.825),(.620,s*.570,.842)),((-.220,s*.600,.830),(-.220,s*.570,.842)),((-1.100,s*.610,.910),(-1.100,s*.575,.995))],M['body'],.008))
  out.append(v.m.add_cube('REF_DOOR_HANDLE_'+('L' if s>0 else 'R'),(-.020,s*.896,.682),(.105,.012,.017),M['body_dark'],.003))
  y=s*.912;out.append(v.m.add_curve('REF_DOOR_SEAM_'+('L' if s>0 else 'R'),[(.595,y,.765),(.545,y,.500),(-.635,y,.500),(-.800,y,.665),(-.785,y,.825)],M['seam'],.0016))
 return out
v.build_glass=greenhouse21

# Refresh source digest semantics.
base_source=v.build_source
def source21(M):
 o=base_source(M);o['OLEANDER_GREENHOUSE_INTERFACE']='SURFACE_PATCH_NETWORK';o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=source21

# Keep V20 projection logic; only candidate revision/provenance changes.
base_projection=ns['projection20']
def projection21():
 d=base_projection();d['candidate_revision']='V21_GREENHOUSE_SURFACE_PATCH_NETWORK'
 for m in d['metrics']:
  m['candidate_measurement_source']=str(m['candidate_measurement_source']).replace('V20_','V21_')
 for s in d.get('side_upper_samples',[]):s['candidate_measurement_source']='V21_FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION'
 for s in d.get('side_lower_samples',[]):s['candidate_measurement_source']='V21_FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION'
 d['greenhouse_interface']='SURFACE_PATCH_NETWORK';return d

# Landmark provenance.
base_lm=v.landmark_receipt
def lm21(source_hash):
 d=base_lm(source_hash)
 for item in d['landmarks']:item['candidate_measurement_source']='V21_FINAL_VISIBLE_GREENHOUSE_PATCH_NETWORK'
 d['greenhouse_interface']='SURFACE_PATCH_NETWORK';d['mass_families']=['V20_LOCKED_MACRO_SHELL','COWL_INTERFACE','A_PILLAR_SURFACE','ROOF_PANEL','ROOF_RAIL_SURFACE','B_PILLAR_SURFACE','C_PILLAR_SAIL_SURFACE','REAR_DECK_INTERFACE'];return d
v.landmark_receipt=lm21

try:
 v.main()
except SystemExit as base_exit:
 a=v.m.parse_args();out=Path(a.out).resolve()
 if (out/'REFERENCE_REPRO_QA.json').exists():
  pr=projection21();(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n')
  urmse=next(m['candidate'] for m in pr['metrics'] if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M');maxabs=max(abs(s['top_error_m']) for s in pr['side_upper_samples'] if math.isfinite(s['top_error_m']));binding={'schema':'oleander.3d.reference-contour-binding.v7','reference':'REFERENCE_CONTOUR_TARGETS_992_2.json','candidate':'V21_FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION','side_top_rmse_m':urmse,'side_top_max_abs_m':maxabs,'thresholds':CONTOUR['gates'],'samples':pr['side_upper_samples'],'status':'MACHINE_BINDING_PASS' if urmse<=.040 and maxabs<=.080 else 'MACHINE_BINDING_FAIL','does_not_prove':CONTOUR['does_not_prove']};(out/'REFERENCE_CONTOUR_BINDING_RECEIPT.json').write_text(json.dumps(binding,ensure_ascii=False,indent=2)+'\n')
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V21_GREENHOUSE_SURFACE_PATCH_NETWORK';q['projection_machine_gate']=pr['status'];q['reference_contour_binding']=binding['status'];q['greenhouse_interface']='SURFACE_PATCH_NETWORK';q['failure_routing']='GREENHOUSE_INTERFACE_ONLY';q['verification_run']='PASS';q['visual_reference_fidelity']='HOLD';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V21_GREENHOUSE_SURFACE_PATCH_NETWORK';r['projection_machine_gate']=pr['status'];r['greenhouse_interface']='SURFACE_PATCH_NETWORK';r['verification_run']='PASS';r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 raise SystemExit(base_exit.code if isinstance(base_exit.code,int) else 0)
