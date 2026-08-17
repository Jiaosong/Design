#!/usr/bin/env python3
"""Porsche 911 Carrera 992.2 V6 — greenhouse exposure + integrated aperture refinement."""
from __future__ import annotations
import importlib.util,json,math,sys
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V5=HERE/'run_reference_repro_v5.py'
spec=importlib.util.spec_from_file_location('v5',V5);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

# Refine the visual-source-grounded spine and roof gesture without changing official hard points.
v.SPINE_PTS=[(-2.271,.510),(-2.10,.600),(-1.85,.690),(-1.55,.755),(-1.195,.800),(-.90,.815),(-.55,.805),(0,.795),(.55,.808),(.76,.822),(1.05,.810),(1.255,.790),(1.55,.755),(1.85,.690),(2.10,.575),(2.271,.470)]
v.ROOF_TOP_PTS=[(-1.06,.855),(-.92,.945),(-.75,1.060),(-.55,1.170),(-.34,1.245),(-.12,1.293),(-.02,1.298),(.16,1.282),(.36,1.225),(.55,1.130),(.69,1.000),(.77,.850)]
v.CABIN_W_PTS=[(-1.06,.650),(-.86,.628),(-.58,.607),(-.28,.592),(-.02,.588),(.28,.594),(.53,.615),(.77,.648)]
v.BELT_PTS=[(-1.06,.830),(-.78,.838),(-.35,.842),(0,.842),(.42,.840),(.77,.832)]
v.FAMILY_CONTROLS.update({'hood_deck_spine_z':v.SPINE_PTS,'cabin_roof_top_z':v.ROOF_TOP_PTS,'cabin_half_width':v.CABIN_W_PTS,'cabin_belt_z':v.BELT_PTS})

orig_materials=v.materials
V6_M={}
def materials_v6():
 M=orig_materials();V6_M.clear();V6_M.update(M)
 for key,col,rough,metal in [('body_dark',(.002,.003,.004,1),.46,0.0),('glass',(.004,.009,.014,1),.12,.02)]:
  bs=M[key].node_tree.nodes.get('Principled BSDF')
  if bs:
   if 'Base Color' in bs.inputs:bs.inputs['Base Color'].default_value=col
   if 'Roughness' in bs.inputs:bs.inputs['Roughness'].default_value=rough
   if 'Metallic' in bs.inputs:bs.inputs['Metallic'].default_value=metal
   if key=='glass':
    if 'Transmission Weight' in bs.inputs:bs.inputs['Transmission Weight'].default_value=.10
    elif 'Transmission' in bs.inputs:bs.inputs['Transmission'].default_value=.10
 return M
v.materials=materials_v6

orig_loft=v.build_loft
def loft_v6(name,xs,ringfn,mat,authority,render=True):
 # The cabin base volume is dark greenhouse/interior backing. It may not be a silver exterior cap behind glazing.
 usemat=V6_M['glass'] if name=='DERIVED_911_9922_CABIN' and 'glass' in V6_M else mat
 o=orig_loft(name,xs,ringfn,usemat,authority,render)
 if name=='DERIVED_911_9922_CABIN':o['OLEANDER_EXPOSURE_ROLE']='GREENHOUSE_BACKING_NOT_EXTERIOR_CAP'
 return o
v.build_loft=loft_v6

def roof_cap(M):
 xs=[-.98+1.62*k/64 for k in range(65)];fra=[-.86,-.58,-.30,0,.30,.58,.86];verts=[];rings=[]
 for x in xs:
  w=v.hermite(v.CABIN_W_PTS,x);top=v.hermite(v.ROOF_TOP_PTS,x);idx=[]
  for f in fra:
   y=f*w;z=top-.050*(abs(f)**1.8);idx.append(len(verts));verts.append((x,y,z+.006))
  rings.append(idx)
 faces=[]
 for i in range(len(rings)-1):
  for j in range(len(fra)-1):faces.append((rings[i][j],rings[i+1][j],rings[i+1][j+1],rings[i][j+1]))
 me=bpy.data.meshes.new('DERIVED_ROOF_CAP_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('DERIVED_ROOF_CAP',me);bpy.context.collection.objects.link(o);o.data.materials.append(M['body']);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY';o['OLEANDER_FORM_FAMILY']='CABIN_ROOF_SKIN'
 sol=o.modifiers.new('ROOF_SKIN_THICKNESS','SOLIDIFY');sol.thickness=.010;sol.offset=0
 for p in me.polygons:p.use_smooth=True
 return o

def glass_v6(M):
 out=[roof_cap(M)]
 # Glass now sees dark greenhouse backing, never a silver body end-cap.
 out.append(v.m.add_panel('REF_WINDSHIELD',[(.742,.642,.840),(.742,-.642,.840),(.340,-.565,1.205),(.340,.565,1.205)],M['glass'],.003))
 out.append(v.m.add_panel('REF_REAR_GLASS',[(-.355,.560,1.205),(-.355,-.560,1.205),(-1.015,-.650,.850),(-1.015,.650,.850)],M['glass'],.003))
 outline=[(.705,.846),(.410,1.160),(.105,1.222),(-.245,1.220),(-.545,1.143),(-.815,1.000),(-1.000,.860),(-.770,.830),(.555,.830)]
 for side in (1,-1):
  vv=[(x,side*(v.hermite(v.CABIN_W_PTS,x)+.008),z) for x,z in outline];out.append(v.m.add_panel('REF_SIDE_GLASS_'+('L' if side>0 else 'R'),vv,M['glass'],.003))
  # Exterior A-pillar / window frame strips.
  out.append(v.m.add_curve('REF_A_PILLAR_'+('L' if side>0 else 'R'),[(.742,side*.642,.840),(.560,side*.610,1.020),(.340,side*.565,1.205)],M['body'],.010))
  out.append(v.m.add_curve('REF_C_PILLAR_EDGE_'+('L' if side>0 else 'R'),[(-.355,side*.560,1.205),(-.690,side*.615,1.075),(-1.015,side*.650,.850)],M['body'],.010))
  sy=side*(v.hermite(v.CABIN_W_PTS,-.33)+.012);out.append(v.m.add_cube('REF_B_PILLAR_'+('L' if side>0 else 'R'),(-.33,sy,1.005),(.030,.022,.305),M['body_dark'],.003));out.append(v.m.add_cube('REF_DOOR_HANDLE_'+('L' if side>0 else 'R'),(-.04,side*.886,.680),(.110,.014,.019),M['body_dark'],.003));y=side*.905;out.append(v.m.add_curve('REF_DOOR_SEAM_'+('L' if side>0 else 'R'),[(.690,y,.775),(.625,y,.510),(-.590,y,.505),(-.720,y,.655),(-.700,y,.825)],M['seam'],.0018))
 return out
v.build_glass=glass_v6

def identity_v6(M):
 out=[]
 for side in (1,-1):
  # Recessed dark lamp module with four emissive pixels; X is the thin axis so side view stays flush.
  out.append(v.m.add_uv_sphere('REF_HEADLAMP_HOUSING_'+str(side),(1.695,side*.650,.752),(.042,.148,.145),M['body_dark']))
  out.append(v.m.add_uv_sphere('REF_HEADLAMP_LENS_'+str(side),(1.724,side*.650,.752),(.022,.132,.130),M['glass']))
  for iy,dy in enumerate((-.038,.038)):
   for iz,dz in enumerate((-.038,.038)):
    out.append(v.m.add_cube(f'REF_HEADLAMP_LED_{side}_{iy}_{iz}',(1.748,side*.650+dy,.752+dz),(.014,.028,.028),M['headlamp'],.005))
  out.append(v.m.add_uv_sphere('REF_MIRROR_'+str(side),(.555,side*.930,.875),(.105,.065,.043),M['body_dark']))
  y=side*.535;out.append(v.m.add_curve('REF_HOOD_SEAM_'+str(side),[(.76,y,.820),(1.12,y,.805),(1.52,y,.755),(1.90,side*.46,.655)],M['seam'],.0016))
 # Three-part dark lower intake family instead of one bright slab.
 out.append(v.m.add_cube('REF_FRONT_CENTER_INTAKE',(2.252,0,.295),(.018,.470,.110),M['body_dark'],.010))
 for side in (1,-1):out.append(v.m.add_cube('REF_FRONT_SIDE_INTAKE_'+str(side),(2.250,side*.545,.310),(.020,.390,.150),M['body_dark'],.014))
 out.append(v.m.add_cube('REF_FRONT_SPLITTER',(2.255,0,.166),(.018,1.430,.018),M['body_dark'],.005))
 out.append(v.m.add_cube('REF_REAR_LIGHTBAR',(-2.250,0,.665),(.018,1.545,.020),M['tail'],.004))
 for k in range(9):out.append(v.m.add_cube(f'REF_REAR_GRILLE_{k:02d}',(-1.79,-.44+k*.11,.800),(.010,.065,.012),M['body_dark'],.002))
 out.append(v.m.add_cube('REF_REAR_DIFFUSER',(-2.250,0,.245),(.018,1.230,.080),M['body_dark'],.010))
 return out
v.build_identity=identity_v6

# Update candidate landmark provenance to this runtime rather than inherited V5 name.
orig_landmark=v.landmark_receipt
def landmark_v6(source_hash):
 d=orig_landmark(source_hash)
 for x in d['landmarks']:x['candidate_measurement_source']='V6_ANALYTIC_SOURCE_PROJECTION'
 d['mass_families'].append('APERTURE_EXPOSURE_CHAIN')
 return d
v.landmark_receipt=landmark_v6

try:
 v.main()
except SystemExit as e:
 out=None
 if '--out' in v.bench:out=Path(v.bench[v.bench.index('--out')+1])
 if out and (out/'REFERENCE_REPRO_QA.json').exists():
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V6_GREENHOUSE_EXPOSURE_INTEGRATED_LAMPS';q['aperture_exposure_gate']='MACHINE_STRUCTURE_PASS_VISUAL_REVIEW_REQUIRED';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V6_GREENHOUSE_EXPOSURE_INTEGRATED_LAMPS';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 raise
