#!/usr/bin/env python3
"""Porsche 911 Carrera 992.2 V7 — end-form plan curvature + roof header refinement."""
from __future__ import annotations
import importlib.util,json,math,sys
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V5=HERE/'run_reference_repro_v5.py'
spec=importlib.util.spec_from_file_location('v5base',V5);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

# Reference-grounded form revision. Narrow terminal sections are intentional: rounded bumper
# volumes provide the lateral corners, preventing a constant-X planar end cap.
v.WIDTH_PTS=[(-2.271,.380),(-2.12,.735),(-1.90,.870),(-1.58,.915),(-1.195,.926),(-.90,.915),(-.55,.895),(0,.875),(.55,.880),(.90,.895),(1.255,.910),(1.60,.905),(1.90,.855),(2.12,.720),(2.271,.360)]
v.SPINE_PTS=[(-2.271,.500),(-2.12,.590),(-1.90,.685),(-1.58,.755),(-1.195,.800),(-.90,.815),(-.55,.805),(0,.795),(.55,.808),(.76,.822),(1.05,.810),(1.255,.790),(1.55,.755),(1.90,.675),(2.12,.565),(2.271,.455)]
v.ROOF_TOP_PTS=[(-1.06,.855),(-.92,.945),(-.75,1.060),(-.55,1.170),(-.34,1.245),(-.12,1.293),(-.02,1.298),(.16,1.282),(.36,1.225),(.55,1.130),(.69,1.000),(.77,.850)]
v.CABIN_W_PTS=[(-1.06,.650),(-.86,.628),(-.58,.607),(-.28,.592),(-.02,.588),(.28,.594),(.53,.615),(.77,.648)]
v.BELT_PTS=[(-1.06,.830),(-.78,.838),(-.35,.842),(0,.842),(.42,.840),(.77,.832)]
v.FAMILY_CONTROLS.update({'body_half_width':v.WIDTH_PTS,'hood_deck_spine_z':v.SPINE_PTS,'cabin_roof_top_z':v.ROOF_TOP_PTS,'cabin_half_width':v.CABIN_W_PTS,'cabin_belt_z':v.BELT_PTS,'terminal_plan_curvature':{'front_bumper_center_x':1.985,'front_bumper_half_x':.286,'rear_bumper_center_x':-1.985,'rear_bumper_half_x':.286}})

orig_materials=v.materials
M7={}
def materials7():
 M=orig_materials();M7.clear();M7.update(M)
 for key,col,rough,metal in [('body_dark',(.0015,.002,.003,1),.50,0.0),('glass',(.003,.008,.013,1),.13,.0)]:
  bs=M[key].node_tree.nodes.get('Principled BSDF')
  if bs:
   if 'Base Color' in bs.inputs:bs.inputs['Base Color'].default_value=col
   if 'Roughness' in bs.inputs:bs.inputs['Roughness'].default_value=rough
   if 'Metallic' in bs.inputs:bs.inputs['Metallic'].default_value=metal
   if key=='glass':
    if 'Transmission Weight' in bs.inputs:bs.inputs['Transmission Weight'].default_value=.08
 return M
v.materials=materials7

orig_loft=v.build_loft
def union_ellipsoid(host,name,loc,scale):
 # Derived-only terminal mass. It never changes sparse Source authority.
 sph=v.m.add_uv_sphere(name,loc,scale,M7['body']);sph['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY'
 bo=host.modifiers.new('UNION_'+name,'BOOLEAN');bo.operation='UNION';bo.solver='EXACT';bo.object=sph;bpy.context.view_layer.objects.active=host;host.select_set(True)
 try:bpy.ops.object.modifier_apply(modifier=bo.name)
 except Exception:pass
 bpy.data.objects.remove(sph,do_unlink=True)

def loft7(name,xs,ringfn,mat,authority,render=True):
 usemat=M7['glass'] if name=='DERIVED_911_9922_CABIN' and 'glass' in M7 else mat
 o=orig_loft(name,xs,ringfn,usemat,authority,render)
 if name=='DERIVED_911_9922_CABIN':o['OLEANDER_EXPOSURE_ROLE']='GREENHOUSE_BACKING_NOT_EXTERIOR_CAP'
 if name=='DERIVED_911_9922_BODY':
  union_ellipsoid(o,'DERIVED_FRONT_ROUNDED_NOSE',(1.985,0,.425),(.286,.785,.300))
  union_ellipsoid(o,'DERIVED_REAR_ROUNDED_TAIL',(-1.985,0,.430),(.286,.800,.305))
  o['OLEANDER_END_FORM']='NON_PLANAR_DERIVED_TERMINAL_MASSES'
 return o
v.build_loft=loft7

def roof_skin(M):
 # Only the actual roof panel between windshield and rear-glass headers; no long white arch over glazing.
 xs=[-.43+.75*k/48 for k in range(49)];fra=[-.86,-.58,-.30,0,.30,.58,.86];verts=[];rings=[]
 for x in xs:
  w=v.hermite(v.CABIN_W_PTS,x);top=v.hermite(v.ROOF_TOP_PTS,x);idx=[]
  for f in fra:
   idx.append(len(verts));verts.append((x,f*w,top-.045*(abs(f)**1.8)+.006))
  rings.append(idx)
 faces=[]
 for i in range(len(rings)-1):
  for j in range(len(fra)-1):faces.append((rings[i][j],rings[i+1][j],rings[i+1][j+1],rings[i][j+1]))
 me=bpy.data.meshes.new('DERIVED_ROOF_SKIN_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('DERIVED_ROOF_SKIN',me);bpy.context.collection.objects.link(o);o.data.materials.append(M['body']);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY';o['OLEANDER_FORM_FAMILY']='CABIN_ROOF_SKIN';sol=o.modifiers.new('ROOF_SKIN_THICKNESS','SOLIDIFY');sol.thickness=.010;sol.offset=0
 for p in me.polygons:p.use_smooth=True
 return o

def glass7(M):
 out=[roof_skin(M)]
 out.append(v.m.add_panel('REF_WINDSHIELD',[(.742,.642,.840),(.742,-.642,.840),(.340,-.565,1.205),(.340,.565,1.205)],M['glass'],.003))
 out.append(v.m.add_panel('REF_REAR_GLASS',[(-.355,.560,1.205),(-.355,-.560,1.205),(-1.015,-.650,.850),(-1.015,.650,.850)],M['glass'],.003))
 outline=[(.705,.846),(.410,1.160),(.105,1.222),(-.245,1.220),(-.545,1.143),(-.815,1.000),(-1.000,.860),(-.770,.830),(.555,.830)]
 for side in (1,-1):
  vv=[(x,side*(v.hermite(v.CABIN_W_PTS,x)+.008),z) for x,z in outline];out.append(v.m.add_panel('REF_SIDE_GLASS_'+('L' if side>0 else 'R'),vv,M['glass'],.003))
  out.append(v.m.add_curve('REF_A_PILLAR_'+('L' if side>0 else 'R'),[(.742,side*.642,.840),(.560,side*.610,1.020),(.340,side*.565,1.205)],M['body'],.010))
  out.append(v.m.add_curve('REF_C_PILLAR_EDGE_'+('L' if side>0 else 'R'),[(-.355,side*.560,1.205),(-.690,side*.615,1.075),(-1.015,side*.650,.850)],M['body'],.010))
  sy=side*(v.hermite(v.CABIN_W_PTS,-.33)+.012);out.append(v.m.add_cube('REF_B_PILLAR_'+('L' if side>0 else 'R'),(-.33,sy,1.005),(.030,.022,.305),M['body_dark'],.003));out.append(v.m.add_cube('REF_DOOR_HANDLE_'+('L' if side>0 else 'R'),(-.04,side*.886,.680),(.110,.014,.019),M['body_dark'],.003));y=side*.905;out.append(v.m.add_curve('REF_DOOR_SEAM_'+('L' if side>0 else 'R'),[(.690,y,.775),(.625,y,.510),(-.590,y,.505),(-.720,y,.655),(-.700,y,.825)],M['seam'],.0018))
 # Top headers define a thin body-color frame rather than a roof slab in front/rear view.
 out.append(v.m.add_curve('REF_WINDSHIELD_HEADER',[(.338,-.565,1.205),(.325,0,1.242),(.338,.565,1.205)],M['body'],.012))
 out.append(v.m.add_curve('REF_REAR_GLASS_HEADER',[(-.355,-.560,1.205),(-.405,0,1.235),(-.355,.560,1.205)],M['body'],.012))
 return out
v.build_glass=glass7

def identity7(M):
 out=[]
 for side in (1,-1):
  out.append(v.m.add_uv_sphere('REF_HEADLAMP_HOUSING_'+str(side),(1.735,side*.650,.755),(.040,.150,.148),M['body_dark']))
  out.append(v.m.add_uv_sphere('REF_HEADLAMP_LENS_'+str(side),(1.775,side*.650,.755),(.024,.134,.132),M['glass']))
  for iy,dy in enumerate((-.038,.038)):
   for iz,dz in enumerate((-.038,.038)):
    out.append(v.m.add_cube(f'REF_HEADLAMP_LED_{side}_{iy}_{iz}',(1.800,side*.650+dy,.755+dz),(.014,.027,.027),M['headlamp'],.005))
  out.append(v.m.add_uv_sphere('REF_MIRROR_'+str(side),(.555,side*.930,.875),(.105,.065,.043),M['body_dark']))
  y=side*.535;out.append(v.m.add_curve('REF_HOOD_SEAM_'+str(side),[(.76,y,.820),(1.12,y,.805),(1.52,y,.755),(1.92,side*.44,.650)],M['seam'],.0016))
 # Apertures placed on rounded terminal mass.
 out.append(v.m.add_cube('REF_FRONT_CENTER_INTAKE',(2.258,0,.295),(.014,.455,.105),M['body_dark'],.010))
 for side in (1,-1):out.append(v.m.add_cube('REF_FRONT_SIDE_INTAKE_'+str(side),(2.215,side*.520,.305),(.020,.330,.142),M['body_dark'],.014))
 out.append(v.m.add_cube('REF_FRONT_SPLITTER',(2.240,0,.158),(.018,1.350,.018),M['body_dark'],.005))
 out.append(v.m.add_cube('REF_REAR_LIGHTBAR',(-2.230,0,.655),(.018,1.500,.020),M['tail'],.004))
 for k in range(9):out.append(v.m.add_cube(f'REF_REAR_GRILLE_{k:02d}',(-1.79,-.44+k*.11,.800),(.010,.065,.012),M['body_dark'],.002))
 out.append(v.m.add_cube('REF_REAR_DIFFUSER',(-2.230,0,.235),(.018,1.160,.075),M['body_dark'],.010))
 return out
v.build_identity=identity7

orig_lm=v.landmark_receipt
def lm7(source_hash):
 d=orig_lm(source_hash)
 for x in d['landmarks']:x['candidate_measurement_source']='V7_ANALYTIC_SOURCE_PROJECTION'
 d['mass_families'] += ['APERTURE_EXPOSURE_CHAIN','END_FORM_PLAN_CURVATURE']
 return d
v.landmark_receipt=lm7

try:
 v.main()
except SystemExit:
 out=Path(v.bench[v.bench.index('--out')+1]) if '--out' in v.bench else None
 if out and (out/'REFERENCE_REPRO_QA.json').exists():
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V7_END_FORM_PLAN_CURVATURE';q['aperture_exposure_gate']='MACHINE_STRUCTURE_PASS_VISUAL_REVIEW_REQUIRED';q['end_form_plan_curvature_gate']='MACHINE_STRUCTURE_PASS_VISUAL_REVIEW_REQUIRED';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V7_END_FORM_PLAN_CURVATURE';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 raise
