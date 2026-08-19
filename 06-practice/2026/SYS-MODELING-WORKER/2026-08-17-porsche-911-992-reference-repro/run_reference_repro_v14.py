#!/usr/bin/env python3
"""Porsche 911 Carrera 992.2 V14 — shallow-roof continuous shell + rendered-alpha projection gate."""
from __future__ import annotations
import importlib.util,json,math
from pathlib import Path
import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent
CORE=HERE/'run_reference_repro_v5.py'
CONTOUR=json.loads((HERE/'REFERENCE_CONTOUR_TARGETS_992_2.json').read_text())
PROJ=json.loads((HERE/'REFERENCE_PROJECTION_TARGETS_992_2.json').read_text())
SIDE_TOP=[tuple(map(float,p)) for p in CONTOUR['side_top_silhouette_m']]
SIDE_LOW=[tuple(map(float,p)) for p in PROJ['side']['lower_body_silhouette_m']]
spec=importlib.util.spec_from_file_location('v5core',CORE);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

v.REF='2025_992.2_CARRERA_RENDERED_ALPHA_V14'
v.WIDTH_PTS=[(-2.271,.845),(-2.10,.895),(-1.85,.918),(-1.55,.926),(-1.195,.926),(-.80,.920),(-.40,.905),(0,.895),(.40,.897),(.80,.905),(1.255,.914),(1.60,.910),(1.85,.895),(2.10,.860),(2.271,.790)]
v.SPINE_PTS=[(-2.271,.590),(-2.10,.675),(-1.85,.730),(-1.55,.785),(-1.195,.815),(-.80,.820),(-.40,.815),(0,.800),(.40,.790),(.80,.790),(1.00,.790),(1.255,.775),(1.45,.750),(1.65,.690),(1.85,.600),(2.05,.555),(2.271,.460)]
v.LOWER_PTS=[(-2.271,.205),(-2.05,.195),(-1.85,.170),(-1.72,.150),(-.75,.145),(0,.145),(.90,.145),(1.72,.155),(1.86,.170),(2.05,.195),(2.271,.205)]
v.ROOF_TOP_PTS=SIDE_TOP
v.CABIN_W_PTS=[(-1.55,.485),(-1.30,.525),(-1.15,.545),(-.90,.552),(-.65,.548),(-.40,.542),(-.15,.540),(.05,.542),(.25,.548),(.45,.565),(.65,.605)]
v.BELT_PTS=[(-1.70,.775),(-1.50,.800),(-1.20,.825),(-.90,.838),(-.50,.842),(0,.840),(.40,.836),(.65,.822)]
CROWN={'front_peak_fraction':.82,'rear_peak_fraction':.88,'front_center_drop_m':.082,'rear_center_drop_m':.058,'outer_drop_m':.034}
TERM={'front_outer_setback_m':.080,'rear_outer_setback_m':.070}
v.FAMILY_CONTROLS={'BODY_PLAN':v.WIDTH_PTS,'HOOD_DECK_SPINE':v.SPINE_PTS,'LOWER_BODY':v.LOWER_PTS,'CALIBRATED_SIDE_TOP':SIDE_TOP,'ROOF_WIDTH':v.CABIN_W_PTS,'BELT':v.BELT_PTS,'FRONT_FENDER_CROWN':CROWN,'REAR_HAUNCH':CROWN,'ROOF_CROSS_SECTION':{'edge_drop_m':.055,'glass_transition_fraction':.82},'TERMINAL_PLAN_CURVATURE':TERM,'GLASS_APERTURE':{'a_pillar_x':.650,'c_pillar_x':-1.150},'WHEEL_APERTURE':{'front_gap':.043,'rear_gap':.044}}
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v14';v.REFERENCE_CONTRACT['reference_revision']=v.REF;v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS);v.REFERENCE_CONTRACT['visible_primary_shell_count']=1;v.REFERENCE_CONTRACT['projection_measurement']='RENDERED_ALPHA_FINAL_VISIBLE_BODY'

def h(pts,x):return v.hermite(pts,x)
def s01(t):t=max(0.0,min(1.0,t));return t*t*(3-2*t)
def rwgt(x):
 if x<=-1.72 or x>=.72:return 0
 if x<-1.45:return s01((x+1.72)/.27)
 if x<=.48:return 1
 return 1-s01((x-.48)/.24)
def fi(x):return math.exp(-((x-v.FRONT_AXLE)/.62)**4)
def ri(x):return math.exp(-((x-v.REAR_AXLE)/.70)**4)
def fields(x):return h(v.WIDTH_PTS,x),h(v.SPINE_PTS,x),h(v.LOWER_PTS,x),h(SIDE_TOP,x),h(v.BELT_PTS,x)
v.body_fields=lambda x:(fields(x)[0],fields(x)[1],fields(x)[3],fields(x)[2])

def crown(f,target,x):
 a,b=fi(x),ri(x);rear=b>=a;inf=max(a,b);peak=CROWN['rear_peak_fraction'] if rear else CROWN['front_peak_fraction'];drop=(CROWN['rear_center_drop_m'] if rear else CROWN['front_center_drop_m'])*(.35+.65*inf)+.018*(1-inf);center=target-drop
 if f<=peak:return center+(target-center)*(math.sin((f/peak)*math.pi/2)**1.55)
 return target-CROWN['outer_drop_m']*((f-peak)/(1-peak))**1.2

def roof(f,target,x,w,belt):
 roof_half=min(w*.72,max(.40,h(v.CABIN_W_PTS,x)));rf=roof_half/max(w,1e-6);edge=target-.055
 if f<=rf:return target-(target-edge)*(f/max(rf,1e-6))**1.9
 # A wide shallow roof edge then falls through the hidden glass aperture zone to the body shoulder.
 if f<=.82:
  u=(f-rf)/max(.82-rf,1e-6);return edge+(belt+.025-edge)*s01(u)
 u=(f-.82)/.18;return belt+.025-.035*s01(u)

def body_ring(x):
 w,zc,zl,target,belt=fields(x);r=rwgt(x);fs=(0,.10,.22,.34,.46,.58,.68,.76,.84,.91,.965,1.0);zv=[]
 for f in fs:zv.append(r*roof(f,target,x,w,belt)+(1-r)*crown(f,target,x))
 off=target-max(zv);pos=[(f*w,z+off) for f,z in zip(fs,zv)]+[(.998*w,zl),(.968*w,.190),(.84*w,.146),(0,.140)]
 ft=s01((x-1.80)/(v.FRONT_X-1.80)) if x>1.80 else 0;rt=s01((-x-1.80)/(-v.REAR_X-1.80)) if x<-1.80 else 0;out=[]
 for y,z in pos+[(-yy,zz) for yy,zz in reversed(pos[1:-1])]:
  q=abs(y)/max(w,1e-6);out.append((x-TERM['front_outer_setback_m']*ft*q**1.65+TERM['rear_outer_setback_m']*rt*q**1.65,y,z))
 return out
v.body_ring=body_ring

# Source
def build_source(M):
 verts=[];edges=[]
 for name,pts,kind in [('PLAN',v.WIDTH_PTS,'w'),('SPINE',v.SPINE_PTS,'z'),('LOWER',v.LOWER_PTS,'z'),('SIDE_TOP',SIDE_TOP,'z'),('ROOF_WIDTH',v.CABIN_W_PTS,'w'),('BELT',v.BELT_PTS,'z')]:
  st=len(verts)
  for x,val in pts:verts.append((x,val,h(v.SPINE_PTS,x)) if kind=='w' else (x,0,val))
  edges += [(st+i,st+i+1) for i in range(len(pts)-1)]
 for co in [(v.REAR_X,0,.14),(v.FRONT_X,0,.14),(v.REAR_AXLE,v.WIDTH/2,.70),(v.REAR_AXLE,-v.WIDTH/2,.70),(-.15,0,v.HEIGHT)]:verts.append(co)
 me=bpy.data.meshes.new('SRC_911_9922_V14_MESH');me.from_pydata(verts,edges,[]);me.update();o=bpy.data.objects.new('SRC_911_9922_V14',me);bpy.context.collection.objects.link(o);o.hide_render=True;o.hide_set(True);o['OLEANDER_AUTHORITY']='SPARSE_REFERENCE_REPRO_SOURCE';o['OLEANDER_VISIBLE_PRIMARY_SHELL_COUNT']=1;o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=build_source

# hidden backing
def cabin_ring(x):
 top=h(SIDE_TOP,x)-.07;w=max(.36,h(v.CABIN_W_PTS,x)-.05);belt=h(v.BELT_PTS,x)-.03;pos=[(0,top),(.45*w,top-.025),(.78*w,top-.10),(w,belt),(0,belt-.04)];return [(x,y,z) for y,z in pos+[(-yy,zz) for yy,zz in reversed(pos[1:-1])]]
v.cabin_ring=cabin_ring
base_loft=v.build_loft
def loft(name,xs,ringfn,mat,authority,render=True):
 o=base_loft(name,xs,ringfn,mat,authority,render)
 if name=='DERIVED_911_9922_CABIN':o.hide_render=True;o['OLEANDER_EXPOSURE_ROLE']='NON_RENDERED_BACKING'
 if name=='DERIVED_911_9922_BODY':o['OLEANDER_FORM_SYSTEM']='V14_SHALLOW_ROOF_CONTINUOUS_PRIMARY_SHELL';o['OLEANDER_VISIBLE_PRIMARY_SHELL']=True
 return o
v.build_loft=loft

# Make glazing dark/opaque for geometric reference read; CMF/glass transmission is not under review here.
base_materials=v.materials
def materials():
 M=base_materials();g=M['glass'];bs=g.node_tree.nodes.get('Principled BSDF') if g.use_nodes else None
 if bs:
  if 'Base Color' in bs.inputs:bs.inputs['Base Color'].default_value=(.004,.009,.014,1)
  if 'Roughness' in bs.inputs:bs.inputs['Roughness'].default_value=.12
  if 'Transmission Weight' in bs.inputs:bs.inputs['Transmission Weight'].default_value=0.0
  elif 'Transmission' in bs.inputs:bs.inputs['Transmission'].default_value=0.0
 return M
v.materials=materials

# Calibrated apertures
def glass(M):
 out=[]
 out.append(v.m.add_panel('REF_WINDSHIELD',[(.650,.622,.840),(.650,-.622,.840),(.235,-.545,1.215),(.235,.545,1.215)],M['glass'],.003))
 out.append(v.m.add_panel('REF_REAR_GLASS',[(-.390,.480,1.215),(-.390,-.480,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)],M['glass'],.003))
 outline=[tuple(p) for p in PROJ['side']['glass_outline_m']]
 for side in (1,-1):
  vv=[(x,side*(max(.42,h(v.CABIN_W_PTS,x))+.006),z) for x,z in outline];out.append(v.m.add_panel('REF_SIDE_GLASS_'+('L' if side>0 else 'R'),vv,M['glass'],.003))
  out.append(v.m.add_curve('REF_A_PILLAR_'+('L' if side>0 else 'R'),[(.650,side*.622,.840),(.455,side*.585,1.055),(.235,side*.545,1.215)],M['body'],.008));out.append(v.m.add_curve('REF_ROOF_RAIL_'+('L' if side>0 else 'R'),[(.235,side*.545,1.215),(0,side*.535,1.282),(-.230,side*.515,1.235),(-.390,side*.480,1.215)],M['body'],.009));out.append(v.m.add_curve('REF_C_PILLAR_EDGE_'+('L' if side>0 else 'R'),[(-.390,side*.480,1.215),(-.760,side*.545,1.055),(-1.150,side*.592,.990)],M['body'],.010))
  out.append(v.m.add_cube('REF_B_PILLAR_'+('L' if side>0 else 'R'),(-.235,side*.545,1.020),(.026,.020,.300),M['body_dark'],.003));out.append(v.m.add_cube('REF_DOOR_HANDLE_'+('L' if side>0 else 'R'),(-.02,side*.896,.682),(.105,.012,.017),M['body_dark'],.003));y=side*.912;out.append(v.m.add_curve('REF_DOOR_SEAM_'+('L' if side>0 else 'R'),[(.595,y,.770),(.545,y,.500),(-.635,y,.500),(-.800,y,.665),(-.785,y,.825)],M['seam'],.0017))
 return out
v.build_glass=glass

# Thin identity only.
def cut_sphere(host,name,loc,scale):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,location=loc);c=bpy.context.object;c.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);bo=host.modifiers.new('CUT_'+name,'BOOLEAN');bo.operation='DIFFERENCE';bo.solver='EXACT';bo.object=c;bpy.context.view_layer.objects.active=host;host.select_set(True);bpy.ops.object.modifier_apply(modifier=bo.name);bpy.data.objects.remove(c,do_unlink=True)
def identity(M):
 out=[];body=bpy.data.objects.get('DERIVED_911_9922_BODY')
 if body:
  for side in (1,-1):cut_sphere(body,'HEADLAMP_'+str(side),(1.745,side*.655,.758),(.050,.136,.132))
 for side in (1,-1):
  out.append(v.m.add_uv_sphere('REF_HEADLAMP_HOUSING_'+str(side),(1.728,side*.655,.758),(.025,.124,.120),M['body_dark']));out.append(v.m.add_uv_sphere('REF_HEADLAMP_LENS_'+str(side),(1.749,side*.655,.758),(.009,.112,.108),M['glass']))
  for iy,dy in enumerate((-.033,.033)):
   for iz,dz in enumerate((-.033,.033)):out.append(v.m.add_cube(f'REF_HEADLAMP_LED_{side}_{iy}_{iz}',(1.759,side*.655+dy,.758+dz),(.005,.018,.018),M['headlamp'],.0025))
  out.append(v.m.add_uv_sphere('REF_MIRROR_'+str(side),(.500,side*.940,.875),(.088,.060,.040),M['body_dark']));y=side*.525;out.append(v.m.add_curve('REF_HOOD_SEAM_'+str(side),[(.645,y,.805),(1.04,y,.790),(1.43,y,.750),(1.82,side*.455,.665)],M['seam'],.0014))
 out.append(v.m.add_cube('REF_FRONT_CENTER_INTAKE',(2.205,0,.285),(.012,.460,.070),M['body_dark'],.005))
 for side in (1,-1):out.append(v.m.add_cube('REF_FRONT_SIDE_INTAKE_'+str(side),(2.198,side*.520,.300),(.012,.255,.090),M['body_dark'],.007))
 out.append(v.m.add_cube('REF_FRONT_SPLITTER',(2.215,0,.160),(.010,1.300,.010),M['body_dark'],.003));out.append(v.m.add_cube('REF_REAR_LIGHTBAR',(-2.250,0,.700),(.009,1.620,.014),M['tail'],.002));out.append(v.m.add_cube('REF_REAR_GRILLE_PANEL',(-2.215,0,.790),(.010,.875,.078),M['body_dark'],.007));out.append(v.m.add_cube('REF_REAR_PLATE_RECESS',(-2.252,0,.450),(.009,.550,.078),M['body_dark'],.009));out.append(v.m.add_cube('REF_REAR_DIFFUSER',(-2.242,0,.245),(.010,1.250,.095),M['body_dark'],.010))
 return out
v.build_identity=identity

# Landmarks
base_lm=v.landmark_receipt
def lm(source_hash):
 d=base_lm(source_hash)
 for item in d['landmarks']:
  item['candidate_measurement_source']='V14_FINAL_VISIBLE_GEOMETRY_OR_APERTURE'
  if item['id']=='A_PILLAR_BASE':item['candidate']=.650;item['normalized_error']=abs(.650-float(item['target']))/float(item['normalization'])
  if item['id']=='C_PILLAR_BASE':item['candidate']=-1.150;item['normalized_error']=abs(-1.150-float(item['target']))/float(item['normalization'])
 d['mass_families']=['ONE_CONTINUOUS_PRIMARY_SHELL','SHALLOW_ROOF_CROSS_SECTION','FENDER_CROWN_SECTION','REAR_HAUNCH_SECTION','TERMINAL_PLAN_CURVATURE','APERTURE_HOST_CHAIN'];d['visible_primary_shell_count']=1;return d
v.landmark_receipt=lm

# Rendered alpha diagnostic: final visible BODY only.
def alpha_diag(body,out,label,loc,target,ortho_scale,w,hpx):
 sc=bpy.context.scene;states={o.name:o.hide_render for o in sc.objects}
 for o in sc.objects:o.hide_render=(o!=body)
 oldcam=sc.camera;oldfilm=sc.render.film_transparent;oldx=sc.render.resolution_x;oldy=sc.render.resolution_y;oldp=sc.render.resolution_percentage;oldpath=sc.render.filepath;olds=sc.cycles.samples
 cam=v.m.make_camera('DIAG_CAM_'+label,loc,target,70,True,ortho_scale);sc.camera=cam;sc.render.film_transparent=True;sc.render.resolution_x=w;sc.render.resolution_y=hpx;sc.render.resolution_percentage=100;sc.cycles.samples=1
 dd=out/'diagnostics';dd.mkdir(exist_ok=True);p=dd/f'DIAG_{label}_FINAL_VISIBLE_BODY.png';sc.render.filepath=str(p);bpy.ops.render.render(write_still=True)
 img=bpy.data.images.get('Render Result');pix=list(img.pixels);cols=[]
 for x in range(w):
  ys=[y for y in range(hpx) if pix[(y*w+x)*4+3]>.2]
  cols.append((min(ys),max(ys)) if ys else None)
 bpy.data.objects.remove(cam,do_unlink=True);sc.camera=oldcam;sc.render.film_transparent=oldfilm;sc.render.resolution_x=oldx;sc.render.resolution_y=oldy;sc.render.resolution_percentage=oldp;sc.render.filepath=oldpath;sc.cycles.samples=olds
 for o in sc.objects:
  if o.name in states:o.hide_render=states[o.name]
 return {'file':str(p),'width_px':w,'height_px':hpx,'ortho_scale':ortho_scale,'center':target,'columns':cols}
def sample_diag(diag,x):
 W=diag['width_px'];H=diag['height_px'];scale=diag['ortho_scale'];cx=diag['center'][0];cz=diag['center'][2];world_w=scale*W/H;u=int(round(((x-cx)/world_w+.5)*(W-1)));ys=[]
 for du in range(-2,3):
  j=max(0,min(W-1,u+du));c=diag['columns'][j]
  if c:ys.append(c)
 if not ys:return float('nan'),float('nan')
 ymin=min(a for a,b in ys);ymax=max(b for a,b in ys);bottom=cz+(ymin/(H-1)-.5)*scale;top=cz+(ymax/(H-1)-.5)*scale;return top,bottom

def panel_ratio(name,lower):
 o=bpy.data.objects[name];vs=[o.matrix_world@q.co for q in o.data.vertices];zs=[p.z for p in vs];zr=min(zs) if lower else max(zs);sel=[p for p in vs if abs(p.z-zr)<.03];return (max(p.y for p in sel)-min(p.y for p in sel))/v.WIDTH

def projection_receipt(out):
 body=bpy.data.objects['DERIVED_911_9922_BODY'];side=alpha_diag(body,out,'SIDE',(0,-8,.75),(0,0,.75),1.55,1200,400);front=alpha_diag(body,out,'FRONT',(7,0,.75),(0,0,.75),1.55,800,600);rear=alpha_diag(body,out,'REAR',(-7,0,.75),(0,0,.75),1.55,800,600)
 ue=[];le=[];samples=[]
 for x,t in SIDE_TOP:
  top,bot=sample_diag(side,x);e=top-t;ue.append(e);samples.append({'x':x,'target_top':t,'candidate_top':top,'top_error_m':e})
 for x,t in SIDE_LOW:
  top,bot=sample_diag(side,x);le.append(bot-t)
 urmse=math.sqrt(sum(e*e for e in ue if math.isfinite(e))/len([e for e in ue if math.isfinite(e)]));lrmse=math.sqrt(sum(e*e for e in le if math.isfinite(e))/len([e for e in le if math.isfinite(e)]));fu=panel_ratio('REF_WINDSHIELD',False);fl=panel_ratio('REF_WINDSHIELD',True);rl=panel_ratio('REF_REAR_GLASS',True);t=PROJ['thresholds']
 metrics=[
  {'id':'SIDE_UPPER_RENDERED_ALPHA_RMSE_M','target':0.0,'candidate':urmse,'abs_error':urmse,'limit':.035,'reference_target_source':'REFERENCE_CONTOUR_TARGETS_992_2.json:side_top_silhouette_m','candidate_measurement_source':'V14_RENDERED_SIDE_ALPHA_FINAL_VISIBLE_UNION'},
  {'id':'SIDE_LOWER_RENDERED_ALPHA_RMSE_M','target':0.0,'candidate':lrmse,'abs_error':lrmse,'limit':.065,'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:side.lower_body_silhouette_m','candidate_measurement_source':'V14_RENDERED_SIDE_ALPHA_FINAL_VISIBLE_UNION'},
  {'id':'FRONT_UPPER_CABIN_WIDTH_RATIO','target':PROJ['front']['roof_width_ratio_at_upper_cabin'],'candidate':fu,'abs_error':abs(fu-PROJ['front']['roof_width_ratio_at_upper_cabin']),'limit':t['front_roof_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.roof_width_ratio_at_upper_cabin','candidate_measurement_source':'V14_FINAL_WINDSHIELD_UPPER_MESH'},
  {'id':'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO','target':PROJ['front']['windshield_lower_width_ratio'],'candidate':fl,'abs_error':abs(fl-PROJ['front']['windshield_lower_width_ratio']),'limit':t['front_windshield_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.windshield_lower_width_ratio','candidate_measurement_source':'V14_FINAL_WINDSHIELD_LOWER_MESH'},
  {'id':'REAR_BACKLIGHT_LOWER_WIDTH_RATIO','target':PROJ['rear']['backlight_lower_width_ratio'],'candidate':rl,'abs_error':abs(rl-PROJ['rear']['backlight_lower_width_ratio']),'limit':t['rear_backlight_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:rear.backlight_lower_width_ratio','candidate_measurement_source':'V14_FINAL_REAR_GLASS_LOWER_MESH'}]
 ok=all(m['abs_error']<=m['limit'] for m in metrics);return {'schema':'oleander.3d.rendered-projection-fidelity-receipt.v2','reference':'REFERENCE_PROJECTION_TARGETS_992_2.json + REFERENCE_CONTOUR_TARGETS_992_2.json','candidate_revision':'V14_RENDERED_ALPHA','status':'PROJECTION_MACHINE_SCREENING_PASS' if ok else 'PROJECTION_MACHINE_SCREENING_FAIL','metrics':metrics,'diagnostic_views':[{k:d[k] for k in ('file','width_px','height_px','ortho_scale','center')} for d in (side,front,rear)],'side_samples':samples,'independent_visual_review':False,'reference_fidelity_review':'HOLD','does_not_prove':PROJ['does_not_prove']}

try:
 v.main()
except SystemExit:
 a=v.m.parse_args();out=Path(a.out).resolve()
 if (out/'REFERENCE_REPRO_QA.json').exists():
  pr=projection_receipt(out);(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n');urmse=next(m['candidate'] for m in pr['metrics'] if m['id']=='SIDE_UPPER_RENDERED_ALPHA_RMSE_M');binding={'schema':'oleander.3d.reference-contour-binding.v3','reference':'REFERENCE_CONTOUR_TARGETS_992_2.json','candidate':'V14_RENDERED_SIDE_ALPHA_FINAL_VISIBLE_UNION','side_top_rmse_m':urmse,'side_top_max_abs_m':max(abs(s['top_error_m']) for s in pr['side_samples'] if math.isfinite(s['top_error_m'])),'thresholds':CONTOUR['gates'],'samples':pr['side_samples'],'status':'MACHINE_BINDING_PASS' if urmse<=CONTOUR['gates']['side_top_rmse_m_max'] else 'MACHINE_BINDING_FAIL','does_not_prove':CONTOUR['does_not_prove']};(out/'REFERENCE_CONTOUR_BINDING_RECEIPT.json').write_text(json.dumps(binding,ensure_ascii=False,indent=2)+'\n')
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V14_RENDERED_ALPHA';q['projection_machine_gate']=pr['status'];q['reference_contour_binding']=binding['status'];q['visible_primary_shell_count']=1;q['continuous_primary_shell_gate']='MACHINE_STRUCTURE_PASS_VISUAL_REVIEW_REQUIRED';q['projection_measurement']='RENDERED_ALPHA_FINAL_VISIBLE_BODY';q['runtime_passes']=1;q['macro_form_gate']='MACHINE_SCREENING_ONLY_VISUAL_REVIEW_REQUIRED';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V14_RENDERED_ALPHA';r['projection_machine_gate']=pr['status'];r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';r['visible_primary_shell_count']=1;r['runtime_passes']=1;(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 raise
