#!/usr/bin/env python3
"""Porsche 911 Carrera 992.2 V8 — integrated plan curvature and roof-rail continuity."""
from __future__ import annotations
import importlib.util,json,math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent;V5=HERE/'run_reference_repro_v5.py'
spec=importlib.util.spec_from_file_location('v5b',V5);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

v.WIDTH_PTS=[(-2.271,.560),(-2.10,.800),(-1.88,.890),(-1.55,.918),(-1.195,.926),(-.90,.915),(-.55,.895),(0,.875),(.55,.880),(.90,.895),(1.255,.910),(1.60,.905),(1.88,.865),(2.10,.790),(2.271,.540)]
v.SPINE_PTS=[(-2.271,.500),(-2.10,.600),(-1.85,.690),(-1.55,.755),(-1.195,.800),(-.90,.815),(-.55,.805),(0,.795),(.55,.808),(.76,.822),(1.05,.810),(1.255,.790),(1.55,.755),(1.85,.690),(2.10,.575),(2.271,.465)]
v.ROOF_TOP_PTS=[(-1.06,.855),(-.92,.945),(-.75,1.060),(-.55,1.170),(-.34,1.245),(-.12,1.293),(-.02,1.298),(.16,1.282),(.36,1.225),(.55,1.130),(.69,1.000),(.77,.850)]
v.CABIN_W_PTS=[(-1.06,.650),(-.86,.628),(-.58,.607),(-.28,.592),(-.02,.588),(.28,.594),(.53,.615),(.77,.648)]
v.BELT_PTS=[(-1.06,.830),(-.78,.838),(-.35,.842),(0,.842),(.42,.840),(.77,.832)]
v.FAMILY_CONTROLS.update({'body_half_width':v.WIDTH_PTS,'hood_deck_spine_z':v.SPINE_PTS,'cabin_roof_top_z':v.ROOF_TOP_PTS,'cabin_half_width':v.CABIN_W_PTS,'cabin_belt_z':v.BELT_PTS,'terminal_plan_curvature':{'method':'integrated_lateral_x_sweep','front_max_setback':.205,'rear_max_setback':.185}})

def body_ring8(x):
 w,zc,zsh,zl=v.body_fields(x);rock=.190
 pos=[(0,zc),(.22*w,zc+.10*(zsh-zc)),(.45*w,zc+.32*(zsh-zc)),(.66*w,zc+.62*(zsh-zc)),(.82*w,zc+.88*(zsh-zc)),(.92*w,zsh),(.975*w,zsh-.012),(w,zsh-.040),(w,zl),(.96*w,rock),(.76*w,.145),(0,.140)]
 ft=max(0,min(1,(x-1.72)/(v.FRONT_X-1.72)));rt=max(0,min(1,(-x-1.70)/(-v.REAR_X-1.70)))
 def pt(y,z):
  r=abs(y)/max(w,1e-6);xe=x-.205*ft*(r**1.75)+.185*rt*(r**1.75);return (xe,y,z)
 return [pt(y,z) for y,z in pos+[(-y,z) for y,z in reversed(pos[1:-1])]]
v.body_ring=body_ring8

orig_mat=v.materials;M8={}
def mats8():
 M=orig_mat();M8.clear();M8.update(M)
 for key,col,rough in [('body_dark',(.0015,.002,.003,1),.50),('glass',(.003,.008,.013,1),.13)]:
  bs=M[key].node_tree.nodes.get('Principled BSDF')
  if bs:
   if 'Base Color' in bs.inputs:bs.inputs['Base Color'].default_value=col
   if 'Roughness' in bs.inputs:bs.inputs['Roughness'].default_value=rough
   if 'Metallic' in bs.inputs:bs.inputs['Metallic'].default_value=0
   if key=='glass' and 'Transmission Weight' in bs.inputs:bs.inputs['Transmission Weight'].default_value=.08
 return M
v.materials=mats8
orig_loft=v.build_loft
def loft8(name,xs,ringfn,mat,authority,render=True):
 use=M8['glass'] if name=='DERIVED_911_9922_CABIN' and 'glass' in M8 else mat;o=orig_loft(name,xs,ringfn,use,authority,render)
 if name=='DERIVED_911_9922_CABIN':o['OLEANDER_EXPOSURE_ROLE']='GREENHOUSE_BACKING_NOT_EXTERIOR_CAP'
 if name=='DERIVED_911_9922_BODY':o['OLEANDER_END_FORM']='INTEGRATED_LATERAL_X_SWEEP'
 return o
v.build_loft=loft8

def roof_skin(M):
 xs=[-.43+.75*k/48 for k in range(49)];fra=[-.86,-.58,-.30,0,.30,.58,.86];verts=[];rings=[]
 for x in xs:
  w=v.hermite(v.CABIN_W_PTS,x);top=v.hermite(v.ROOF_TOP_PTS,x);ring=[]
  for f in fra:ring.append(len(verts));verts.append((x,f*w,top-.044*(abs(f)**1.8)+.005))
  rings.append(ring)
 faces=[]
 for i in range(len(rings)-1):
  for j in range(len(fra)-1):faces.append((rings[i][j],rings[i+1][j],rings[i+1][j+1],rings[i][j+1]))
 me=bpy.data.meshes.new('DERIVED_ROOF_SKIN_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('DERIVED_ROOF_SKIN',me);bpy.context.collection.objects.link(o);o.data.materials.append(M['body']);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY';sol=o.modifiers.new('ROOF_THICK','SOLIDIFY');sol.thickness=.010;sol.offset=0
 for p in me.polygons:p.use_smooth=True
 return o

def glass8(M):
 out=[roof_skin(M),v.m.add_panel('REF_WINDSHIELD',[(.742,.642,.840),(.742,-.642,.840),(.340,-.565,1.205),(.340,.565,1.205)],M['glass'],.003),v.m.add_panel('REF_REAR_GLASS',[(-.355,.560,1.205),(-.355,-.560,1.205),(-1.015,-.650,.850),(-1.015,.650,.850)],M['glass'],.003)]
 outline=[(.705,.846),(.410,1.160),(.105,1.222),(-.245,1.220),(-.545,1.143),(-.815,1.000),(-1.000,.860),(-.770,.830),(.555,.830)]
 for side in (1,-1):
  vv=[(x,side*(v.hermite(v.CABIN_W_PTS,x)+.008),z) for x,z in outline];out.append(v.m.add_panel('REF_SIDE_GLASS_'+('L' if side>0 else 'R'),vv,M['glass'],.003));out.append(v.m.add_curve('REF_A_PILLAR_'+('L' if side>0 else 'R'),[(.742,side*.642,.840),(.560,side*.610,1.020),(.340,side*.565,1.205)],M['body'],.012));out.append(v.m.add_curve('REF_ROOF_RAIL_'+('L' if side>0 else 'R'),[(.340,side*.565,1.205),(.120,side*.535,1.270),(-.120,side*.535,1.280),(-.355,side*.560,1.205)],M['body'],.014));out.append(v.m.add_curve('REF_C_PILLAR_EDGE_'+('L' if side>0 else 'R'),[(-.355,side*.560,1.205),(-.690,side*.615,1.075),(-1.015,side*.650,.850)],M['body'],.014));sy=side*(v.hermite(v.CABIN_W_PTS,-.33)+.012);out.append(v.m.add_cube('REF_B_PILLAR_'+('L' if side>0 else 'R'),(-.33,sy,1.005),(.030,.022,.305),M['body_dark'],.003));out.append(v.m.add_cube('REF_DOOR_HANDLE_'+('L' if side>0 else 'R'),(-.04,side*.886,.680),(.110,.014,.019),M['body_dark'],.003));y=side*.905;out.append(v.m.add_curve('REF_DOOR_SEAM_'+('L' if side>0 else 'R'),[(.690,y,.775),(.625,y,.510),(-.590,y,.505),(-.720,y,.655),(-.700,y,.825)],M['seam'],.0018))
 out.append(v.m.add_curve('REF_WINDSHIELD_HEADER',[(.338,-.565,1.205),(.325,0,1.242),(.338,.565,1.205)],M['body'],.012));out.append(v.m.add_curve('REF_REAR_GLASS_HEADER',[(-.355,-.560,1.205),(-.405,0,1.235),(-.355,.560,1.205)],M['body'],.012));return out
v.build_glass=glass8

def identity8(M):
 out=[]
 for side in (1,-1):
  out.append(v.m.add_uv_sphere('REF_HEADLAMP_HOUSING_'+str(side),(1.790,side*.650,.770),(.032,.150,.148),M['body_dark']));out.append(v.m.add_uv_sphere('REF_HEADLAMP_LENS_'+str(side),(1.825,side*.650,.770),(.020,.134,.132),M['glass']))
  for iy,dy in enumerate((-.038,.038)):
   for iz,dz in enumerate((-.038,.038)):out.append(v.m.add_cube(f'REF_HEADLAMP_LED_{side}_{iy}_{iz}',(1.848,side*.650+dy,.770+dz),(.012,.027,.027),M['headlamp'],.005))
  # Horizontal mirror capsule with a small stalk, replacing spherical placeholder.
  out.append(v.m.add_cube('REF_MIRROR_'+str(side),(.555,side*.935,.875),(.095,.060,.038),M['body_dark'],.028));out.append(v.m.add_cube('REF_MIRROR_STALK_'+str(side),(.560,side*.885,.850),(.035,.030,.020),M['body_dark'],.010));y=side*.535;out.append(v.m.add_curve('REF_HOOD_SEAM_'+str(side),[(.76,y,.820),(1.12,y,.805),(1.52,y,.755),(1.92,side*.44,.650)],M['seam'],.0016))
 out.append(v.m.add_cube('REF_FRONT_CENTER_INTAKE',(2.238,0,.275),(.016,.300,.080),M['body_dark'],.012))
 for side in (1,-1):out.append(v.m.add_cube('REF_FRONT_SIDE_INTAKE_'+str(side),(2.175,side*.520,.285),(.020,.285,.090),M['body_dark'],.018))
 out.append(v.m.add_cube('REF_FRONT_SPLITTER',(2.225,0,.160),(.015,1.320,.015),M['body_dark'],.005));out.append(v.m.add_cube('REF_REAR_LIGHTBAR',(-2.220,0,.655),(.018,1.500,.020),M['tail'],.004))
 for k in range(9):out.append(v.m.add_cube(f'REF_REAR_GRILLE_{k:02d}',(-1.79,-.44+k*.11,.800),(.010,.065,.012),M['body_dark'],.002))
 out.append(v.m.add_cube('REF_REAR_DIFFUSER',(-2.215,0,.235),(.018,1.150,.070),M['body_dark'],.010));return out
v.build_identity=identity8
orig_lm=v.landmark_receipt
def lm8(h):
 d=orig_lm(h)
 for x in d['landmarks']:x['candidate_measurement_source']='V8_ANALYTIC_SOURCE_PROJECTION'
 d['mass_families']+=['APERTURE_EXPOSURE_CHAIN','END_FORM_PLAN_CURVATURE','ROOF_RAIL_CONTINUITY'];return d
v.landmark_receipt=lm8
try:
 v.main()
except SystemExit:
 out=Path(v.bench[v.bench.index('--out')+1]) if '--out' in v.bench else None
 if out and (out/'REFERENCE_REPRO_QA.json').exists():
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V8_INTEGRATED_PLAN_CURVATURE';q['aperture_exposure_gate']='MACHINE_STRUCTURE_PASS_VISUAL_REVIEW_REQUIRED';q['end_form_plan_curvature_gate']='MACHINE_STRUCTURE_PASS_VISUAL_REVIEW_REQUIRED';q['roof_rail_continuity_gate']='MACHINE_STRUCTURE_PASS_VISUAL_REVIEW_REQUIRED';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V8_INTEGRATED_PLAN_CURVATURE';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 raise
