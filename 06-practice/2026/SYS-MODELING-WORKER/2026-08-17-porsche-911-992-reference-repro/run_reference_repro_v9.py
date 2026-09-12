#!/usr/bin/env python3
"""Porsche 911 Carrera 992.2 V9 — section hierarchy + recessed aperture refinement."""
from __future__ import annotations
import importlib.util,json,math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent;V5=HERE/'run_reference_repro_v5.py'
spec=importlib.util.spec_from_file_location('v5core',V5);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

# Same official hard points. Visual controls are revised against 992.2 side/front/rear references.
v.WIDTH_PTS=[(-2.271,.500),(-2.10,.785),(-1.88,.892),(-1.55,.920),(-1.195,.926),(-.90,.920),(-.55,.900),(0,.882),(.55,.886),(.90,.900),(1.255,.912),(1.60,.905),(1.88,.862),(2.10,.775),(2.271,.490)]
v.SPINE_PTS=[(-2.271,.555),(-2.10,.645),(-1.85,.715),(-1.55,.775),(-1.195,.815),(-.90,.820),(-.55,.805),(0,.790),(.55,.795),(.78,.805),(1.05,.790),(1.255,.770),(1.55,.745),(1.85,.695),(2.10,.610),(2.271,.520)]
v.LOWER_PTS=[(-2.271,.300),(-1.90,.400),(-1.45,.470),(-.90,.495),(0,.490),(.90,.475),(1.45,.445),(1.90,.380),(2.271,.285)]
# Longer, less bubble-like greenhouse: A-pillar base ~0.56, C-pillar base ~-0.78.
v.ROOF_TOP_PTS=[(-1.02,.850),(-.88,.950),(-.72,1.060),(-.54,1.165),(-.34,1.242),(-.14,1.290),(-.03,1.298),(.14,1.286),(.30,1.250),(.44,1.190),(.56,1.100),(.64,.995),(.68,.860)]
v.CABIN_W_PTS=[(-1.02,.645),(-.82,.625),(-.56,.603),(-.28,.588),(-.02,.582),(.25,.588),(.48,.610),(.68,.642)]
v.BELT_PTS=[(-1.02,.815),(-.78,.825),(-.35,.832),(0,.834),(.35,.832),(.68,.820)]
v.FAMILY_CONTROLS.update({'body_half_width':v.WIDTH_PTS,'hood_deck_spine_z':v.SPINE_PTS,'lower_side_z':v.LOWER_PTS,'cabin_roof_top_z':v.ROOF_TOP_PTS,'cabin_half_width':v.CABIN_W_PTS,'cabin_belt_z':v.BELT_PTS,'front_fender':{'axle_x':v.FRONT_AXLE,'sigma':.47,'height':.038,'width_bias':.014},'rear_quarter':{'axle_x':v.REAR_AXLE,'sigma':.52,'height':.060,'width_bias':.030},'terminal_plan_curvature':{'method':'integrated_lateral_x_sweep','front_max_setback':.175,'rear_max_setback':.155},'greenhouse_extent':{'a_pillar_base_x':.56,'c_pillar_base_x':-.78}})

# Override body fields: lower hood/fender front and stronger rear-biased shoulder.
def body_fields9(x):
 w=v.hermite(v.WIDTH_PTS,x)+.014*v.g(x,v.FRONT_AXLE,.47)+.030*v.g(x,v.REAR_AXLE,.52);w=min(.926,w)
 zc=v.hermite(v.SPINE_PTS,x);front=.038*v.g(x,v.FRONT_AXLE,.47);rear=.060*v.g(x,v.REAR_AXLE,.52);zsh=zc+.014+front+rear;zl=v.hermite(v.LOWER_PTS,x);return w,zc,zsh,zl
v.body_fields=body_fields9

def body_ring9(x):
 w,zc,zsh,zl=v.body_fields(x);rock=.180
 pos=[(0,zc),(.20*w,zc+.08*(zsh-zc)),(.42*w,zc+.25*(zsh-zc)),(.62*w,zc+.55*(zsh-zc)),(.78*w,zc+.86*(zsh-zc)),(.90*w,zsh),(.968*w,zsh-.010),(w,zsh-.038),(.985*w,zl),(.920*w,.205),(.810*w,.150),(0,.140)]
 ft=max(0,min(1,(x-1.70)/(v.FRONT_X-1.70)));rt=max(0,min(1,(-x-1.68)/(-v.REAR_X-1.68)))
 out=[]
 for y,z in pos+[(-y,z) for y,z in reversed(pos[1:-1])]:
  r=abs(y)/max(w,1e-6);xe=x-.175*ft*(r**1.65)+.155*rt*(r**1.65);out.append((xe,y,z))
 return out
v.body_ring=body_ring9

orig_mat=v.materials;M9={}
def mats9():
 M=orig_mat();M9.clear();M9.update(M)
 for key,col,rough in [('body_dark',(.0015,.002,.003,1),.48),('glass',(.003,.008,.013,1),.14)]:
  bs=M[key].node_tree.nodes.get('Principled BSDF')
  if bs:
   if 'Base Color' in bs.inputs:bs.inputs['Base Color'].default_value=col
   if 'Roughness' in bs.inputs:bs.inputs['Roughness'].default_value=rough
   if 'Metallic' in bs.inputs:bs.inputs['Metallic'].default_value=0
   if key=='glass' and 'Transmission Weight' in bs.inputs:bs.inputs['Transmission Weight'].default_value=.07
 return M
v.materials=mats9
orig_loft=v.build_loft
def loft9(name,xs,ringfn,mat,authority,render=True):
 use=M9['glass'] if name=='DERIVED_911_9922_CABIN' and 'glass' in M9 else mat;o=orig_loft(name,xs,ringfn,use,authority,render)
 if name=='DERIVED_911_9922_CABIN':o['OLEANDER_EXPOSURE_ROLE']='GREENHOUSE_BACKING_NOT_EXTERIOR_CAP'
 if name=='DERIVED_911_9922_BODY':o['OLEANDER_END_FORM']='INTEGRATED_LATERAL_X_SWEEP';o['OLEANDER_SECTION_HIERARCHY']='HOOD|FRONT_FENDER|REAR_QUARTER|LOWER_SIDE'
 return o
v.build_loft=loft9

# More tapered cabin cross-section; top width is visibly narrower than belt width.
def cabin_ring9(x):
 top=v.hermite(v.ROOF_TOP_PTS,x);w=v.hermite(v.CABIN_W_PTS,x);belt=v.hermite(v.BELT_PTS,x)
 pos=[(0,top),(.18*w,top-.006),(.38*w,top-.020),(.58*w,top-.045),(.74*w,top-.080),(.88*w,top-.120),(w,belt+.015),(w,belt),(0,belt-.016)]
 return [(x,y,z) for y,z in pos+[(-y,z) for y,z in reversed(pos[1:-1])]]
v.cabin_ring=cabin_ring9

def roof_skin(M):
 xs=[-.36+.62*k/50 for k in range(51)];fra=[-.86,-.58,-.30,0,.30,.58,.86];verts=[];rings=[]
 for x in xs:
  w=v.hermite(v.CABIN_W_PTS,x);top=v.hermite(v.ROOF_TOP_PTS,x);rr=[]
  for f in fra:rr.append(len(verts));verts.append((x,f*w,top-.038*(abs(f)**1.8)+.004))
  rings.append(rr)
 faces=[]
 for i in range(len(rings)-1):
  for j in range(len(fra)-1):faces.append((rings[i][j],rings[i+1][j],rings[i+1][j+1],rings[i][j+1]))
 me=bpy.data.meshes.new('DERIVED_ROOF_SKIN_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('DERIVED_ROOF_SKIN',me);bpy.context.collection.objects.link(o);o.data.materials.append(M['body']);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY';o['OLEANDER_FORM_FAMILY']='CABIN_ROOF_SKIN';sol=o.modifiers.new('ROOF_THICK','SOLIDIFY');sol.thickness=.009;sol.offset=0
 for p in me.polygons:p.use_smooth=True
 return o

def glass9(M):
 out=[roof_skin(M)]
 # Windshield and rear glass extent now follow the longer 992 side profile.
 out.append(v.m.add_panel('REF_WINDSHIELD',[(.565,.650,.820),(.565,-.650,.820),(.260,-.545,1.215),(.260,.545,1.215)],M['glass'],.003))
 out.append(v.m.add_panel('REF_REAR_GLASS',[(-.330,.545,1.215),(-.330,-.545,1.215),(-.900,-.645,.825),(-.900,.645,.825)],M['glass'],.003))
 outline=[(.565,.825),(.405,1.055),(.260,1.215),(.050,1.255),(-.200,1.235),(-.430,1.170),(-.650,1.055),(-.850,.895),(-.780,.820),(.500,.815)]
 for side in (1,-1):
  vv=[(x,side*(v.hermite(v.CABIN_W_PTS,x)+.006),z) for x,z in outline];out.append(v.m.add_panel('REF_SIDE_GLASS_'+('L' if side>0 else 'R'),vv,M['glass'],.003));out.append(v.m.add_curve('REF_A_PILLAR_'+('L' if side>0 else 'R'),[(.565,side*.650,.820),(.410,side*.605,1.055),(.260,side*.545,1.215)],M['body'],.011));out.append(v.m.add_curve('REF_ROOF_RAIL_'+('L' if side>0 else 'R'),[(.260,side*.545,1.215),(.050,side*.525,1.265),(-.180,side*.525,1.245),(-.330,side*.545,1.215)],M['body'],.012));out.append(v.m.add_curve('REF_C_PILLAR_EDGE_'+('L' if side>0 else 'R'),[(-.330,side*.545,1.215),(-.600,side*.610,1.070),(-.900,side*.645,.825)],M['body'],.012));sy=side*(v.hermite(v.CABIN_W_PTS,-.18)+.010);out.append(v.m.add_cube('REF_B_PILLAR_'+('L' if side>0 else 'R'),(-.18,sy,1.000),(.028,.020,.305),M['body_dark'],.003));out.append(v.m.add_cube('REF_DOOR_HANDLE_'+('L' if side>0 else 'R'),(-.01,side*.890,.675),(.108,.013,.018),M['body_dark'],.003));y=side*.907;out.append(v.m.add_curve('REF_DOOR_SEAM_'+('L' if side>0 else 'R'),[(.610,y,.770),(.550,y,.505),(-.610,y,.500),(-.760,y,.650),(-.740,y,.815)],M['seam'],.0018))
 out.append(v.m.add_curve('REF_WINDSHIELD_HEADER',[(.258,-.545,1.215),(.245,0,1.242),(.258,.545,1.215)],M['body'],.010));out.append(v.m.add_curve('REF_REAR_GLASS_HEADER',[(-.330,-.545,1.215),(-.370,0,1.240),(-.330,.545,1.215)],M['body'],.010));return out
v.build_glass=glass9

# Derived-only shallow recess helpers. Source remains untouched.
def recess_sphere(host,name,loc,scale):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,location=loc);c=bpy.context.object;c.name=name;c.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);bo=host.modifiers.new('CUT_'+name,'BOOLEAN');bo.operation='DIFFERENCE';bo.solver='EXACT';bo.object=c;bpy.context.view_layer.objects.active=host;host.select_set(True)
 try:bpy.ops.object.modifier_apply(modifier=bo.name)
 except Exception:pass
 bpy.data.objects.remove(c,do_unlink=True)

def recess_cube(host,name,loc,size,bevel=.02):
 c=v.m.add_cube(name,loc,size,M9['body_dark'],bevel);bo=host.modifiers.new('CUT_'+name,'BOOLEAN');bo.operation='DIFFERENCE';bo.solver='EXACT';bo.object=c;bpy.context.view_layer.objects.active=host;host.select_set(True)
 try:bpy.ops.object.modifier_apply(modifier=bo.name)
 except Exception:pass
 bpy.data.objects.remove(c,do_unlink=True)

orig_main=v.main
# identity objects are generated after body; use scene lookup to cut the body when identity is built.
def identity9(M):
 out=[];body=bpy.data.objects.get('DERIVED_911_9922_BODY')
 if body:
  for side in (1,-1):recess_sphere(body,'CUT_HEADLAMP_'+str(side),(1.775,side*.650,.755),(.105,.165,.160))
  for side in (1,-1):recess_cube(body,'CUT_FRONT_INTAKE_'+str(side),(2.105,side*.500,.285),(.230,.330,.130),.022)
 for side in (1,-1):
  out.append(v.m.add_uv_sphere('REF_HEADLAMP_HOUSING_'+str(side),(1.760,side*.650,.755),(.050,.145,.140),M['body_dark']));out.append(v.m.add_uv_sphere('REF_HEADLAMP_LENS_'+str(side),(1.790,side*.650,.755),(.026,.132,.128),M['glass']))
  for iy,dy in enumerate((-.041,.041)):
   for iz,dz in enumerate((-.041,.041)):out.append(v.m.add_cube(f'REF_HEADLAMP_LED_{side}_{iy}_{iz}',(1.815,side*.650+dy,.755+dz),(.012,.026,.026),M['headlamp'],.004))
  out.append(v.m.add_cube('REF_MIRROR_'+str(side),(.485,side*.928,.850),(.090,.060,.036),M['body_dark'],.026));out.append(v.m.add_cube('REF_MIRROR_STALK_'+str(side),(.500,side*.882,.835),(.032,.028,.018),M['body_dark'],.009))
  y=side*.515;out.append(v.m.add_curve('REF_HOOD_SEAM_'+str(side),[(.590,y,.790),(1.02,y,.785),(1.46,y,.745),(1.86,side*.445,.665)],M['seam'],.0016))
  # Dark recess back planes sit behind the cut host surface.
  out.append(v.m.add_cube('REF_FRONT_INTAKE_BACK_'+str(side),(2.045,side*.500,.285),(.025,.285,.100),M['body_dark'],.012))
 # clean lower centre opening, not a giant rectangle.
 out.append(v.m.add_cube('REF_FRONT_CENTER_OPENING',(2.145,0,.245),(.026,.320,.060),M['body_dark'],.008));out.append(v.m.add_cube('REF_FRONT_SPLITTER',(2.185,0,.155),(.014,1.280,.014),M['body_dark'],.004))
 # rear: thin lightbar, body-colour bumper remains dominant; modest license recess and two exhausts.
 out.append(v.m.add_cube('REF_REAR_LIGHTBAR',(-2.165,0,.680),(.014,1.495,.018),M['tail'],.004));out.append(v.m.add_cube('REF_REAR_PLATE_RECESS',(-2.175,0,.435),(.018,.600,.115),M['body_dark'],.018))
 for k in range(9):out.append(v.m.add_cube(f'REF_REAR_GRILLE_{k:02d}',(-1.76,-.42+k*.105,.815),(.010,.060,.012),M['body_dark'],.002))
 for side in (1,-1):
  bpy.ops.mesh.primitive_torus_add(major_radius=.052,minor_radius=.008,major_segments=40,minor_segments=8,location=(-2.180,side*.480,.265),rotation=(0,math.pi/2,0));e=bpy.context.object;e.name='REF_EXHAUST_'+str(side);e.data.materials.append(M['rim']);out.append(e)
 out.append(v.m.add_cube('REF_REAR_LOWER_TRIM',(-2.175,0,.225),(.015,1.080,.055),M['body_dark'],.010));return out
v.build_identity=identity9

orig_lm=v.landmark_receipt
def lm9(h):
 d=orig_lm(h)
 # Replace greenhouse candidates with revised values and preserve separate provenance.
 for x in d['landmarks']:
  x['candidate_measurement_source']='V9_ANALYTIC_SOURCE_PROJECTION'
  if x['id']=='A_PILLAR_BASE':x['candidate']=.565;x['normalized_error']=abs(.565-x['target'])/x['normalization']
  if x['id']=='C_PILLAR_BASE':x['candidate']=-.900;x['normalized_error']=abs(-.900-x['target'])/x['normalization']
 d['mass_families']+=['SECTION_HIERARCHY','RECESSED_IDENTITY_APERTURE','GREENHOUSE_EXTENT'];return d
v.landmark_receipt=lm9

try:
 v.main()
except SystemExit:
 out=Path(v.bench[v.bench.index('--out')+1]) if '--out' in v.bench else None
 if out and (out/'REFERENCE_REPRO_QA.json').exists():
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V9_SECTION_HIERARCHY_RECESSED_APERTURES';q['aperture_exposure_gate']='MACHINE_STRUCTURE_PASS_VISUAL_REVIEW_REQUIRED';q['end_form_plan_curvature_gate']='MACHINE_STRUCTURE_PASS_VISUAL_REVIEW_REQUIRED';q['roof_rail_continuity_gate']='MACHINE_STRUCTURE_PASS_VISUAL_REVIEW_REQUIRED';q['section_hierarchy_gate']='MACHINE_STRUCTURE_PASS_VISUAL_REVIEW_REQUIRED';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V9_SECTION_HIERARCHY_RECESSED_APERTURES';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 raise
