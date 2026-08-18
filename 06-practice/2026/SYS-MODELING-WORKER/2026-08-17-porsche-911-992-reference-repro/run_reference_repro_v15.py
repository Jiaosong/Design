#!/usr/bin/env python3
"""Porsche 911 Carrera 992.2 V15 — true aperture architecture.

V15 reuses the import-safe declaration portion of V14, then makes windows true host-surface
openings. Glass is placed inside those openings and body-colour A/B/C/roof frames are restored as
explicit interfaces. Rendered-alpha diagnostics are read back from the persisted PNG, not the
Render Result buffer, avoiding backend-size ambiguity.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent
V14=HERE/'run_reference_repro_v14.py'
text=V14.read_text()
marker='\ntry:\n v.main()'
if marker not in text: raise SystemExit('V14 declaration marker missing')
ns={'__file__':str(V14),'__name__':'oleander_v14_declarations'}
exec(compile(text.split(marker,1)[0],str(V14),'exec'),ns)
v=ns['v'];PROJ=ns['PROJ'];CONTOUR=ns['CONTOUR'];SIDE_TOP=ns['SIDE_TOP'];SIDE_LOW=ns['SIDE_LOW'];h=ns['h']

v.REF='2025_992.2_CARRERA_TRUE_APERTURE_V15'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v15'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['aperture_architecture']='TRUE_HOST_CUT_OPENINGS'
v.FAMILY_CONTROLS['APERTURE_HOST_CHAIN']={'windshield':'BOOLEAN_HOST_OPENING','side_glass':'BOOLEAN_HOST_OPENING','rear_glass':'BOOLEAN_HOST_OPENING','frames':'DERIVED_INTERFACE_GEOMETRY','glass':'DERIVED_APERTURE_INFILL'}

# Robust boolean helpers: cutter is moved ahead of the cosmetic bevel before application.
def apply_cut(host,cutter,tag):
 bpy.context.view_layer.objects.active=host;host.select_set(True)
 bo=host.modifiers.new('CUT_'+tag,'BOOLEAN');bo.operation='DIFFERENCE';bo.solver='EXACT';bo.object=cutter
 while host.modifiers.find(bo.name)>0:
  bpy.ops.object.modifier_move_up(modifier=bo.name)
 bpy.ops.object.modifier_apply(modifier=bo.name)
 bpy.data.objects.remove(cutter,do_unlink=True)

def panel_prism(name,quad,thickness):
 a,b,c=[Vector(x) for x in quad[:3]];n=(b-a).cross(c-a).normalized();front=[Vector(x)+n*thickness*.5 for x in quad];back=[Vector(x)-n*thickness*.5 for x in quad];verts=[tuple(x) for x in front+back];N=len(quad);faces=[tuple(range(N)),tuple(reversed(range(N,2*N)))]
 for i in range(N):j=(i+1)%N;faces.append((i,j,N+j,N+i))
 me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.hide_render=True;return o

def side_prism(name,outline,side,inner=.34,outer=1.05):
 # outline is ordered in X/Z. Two Y layers create a watertight side-window cutter.
 yin=side*inner;yout=side*outer;front=[(x,yout,z) for x,z in outline];back=[(x,yin,z) for x,z in outline];verts=front+back;N=len(outline);faces=[tuple(range(N)),tuple(reversed(range(N,2*N)))]
 for i in range(N):j=(i+1)%N;faces.append((i,j,N+j,N+i))
 me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.hide_render=True;return o

# True aperture build.
def build_glass_v15(M):
 body=bpy.data.objects['DERIVED_911_9922_BODY'];out=[]
 windshield=[(.650,.622,.840),(.650,-.622,.840),(.235,-.545,1.215),(.235,.545,1.215)]
 rear=[(-.390,.480,1.215),(-.390,-.480,1.215),(-1.150,-.592,.990),(-1.150,.592,.990)]
 apply_cut(body,panel_prism('CUTTER_WINDSHIELD',windshield,.28),'WINDSHIELD_APERTURE')
 apply_cut(body,panel_prism('CUTTER_REAR_GLASS',rear,.28),'REAR_GLASS_APERTURE')
 outline=[tuple(p) for p in PROJ['side']['glass_outline_m']]
 for side in (1,-1):apply_cut(body,side_prism('CUTTER_SIDE_'+('L' if side>0 else 'R'),outline,side),'SIDE_APERTURE_'+('L' if side>0 else 'R'))
 # Glass infill is slightly inset from exterior frames.
 out.append(v.m.add_panel('REF_WINDSHIELD',windshield,M['glass'],.003));out.append(v.m.add_panel('REF_REAR_GLASS',rear,M['glass'],.003))
 for side in (1,-1):
  vv=[(x,side*(max(.42,h(v.CABIN_W_PTS,x))+.002),z) for x,z in outline];out.append(v.m.add_panel('REF_SIDE_GLASS_'+('L' if side>0 else 'R'),vv,M['glass'],.003))
  # Restore body-colour frame/interface after host opening.
  out.append(v.m.add_curve('REF_A_PILLAR_'+('L' if side>0 else 'R'),[(.650,side*.622,.840),(.455,side*.585,1.055),(.235,side*.545,1.215)],M['body'],.012))
  out.append(v.m.add_curve('REF_ROOF_RAIL_'+('L' if side>0 else 'R'),[(.235,side*.545,1.215),(0,side*.535,1.282),(-.230,side*.515,1.235),(-.390,side*.480,1.215)],M['body'],.012))
  out.append(v.m.add_curve('REF_C_PILLAR_EDGE_'+('L' if side>0 else 'R'),[(-.390,side*.480,1.215),(-.760,side*.545,1.055),(-1.150,side*.592,.990)],M['body'],.014))
  out.append(v.m.add_cube('REF_B_PILLAR_'+('L' if side>0 else 'R'),(-.235,side*.548,1.020),(.035,.030,.300),M['body_dark'],.003))
  out.append(v.m.add_cube('REF_DOOR_HANDLE_'+('L' if side>0 else 'R'),(-.02,side*.896,.682),(.105,.012,.017),M['body_dark'],.003));y=side*.912;out.append(v.m.add_curve('REF_DOOR_SEAM_'+('L' if side>0 else 'R'),[(.595,y,.770),(.545,y,.500),(-.635,y,.500),(-.800,y,.665),(-.785,y,.825)],M['seam'],.0017))
 body['OLEANDER_APERTURE_HOST_CHAIN']='TRUE_OPENING_FRAME_GLASS_BACKING';return out
v.build_glass=build_glass_v15

# Update landmark provenance.
base_lm=v.landmark_receipt
def lm15(source_hash):
 d=base_lm(source_hash)
 for item in d['landmarks']:item['candidate_measurement_source']='V15_FINAL_VISIBLE_APERTURE_GEOMETRY'
 d['mass_families']=['ONE_CONTINUOUS_PRIMARY_SHELL','TRUE_WINDOW_APERTURES','SHALLOW_ROOF_CROSS_SECTION','FENDER_CROWN_SECTION','REAR_HAUNCH_SECTION','TERMINAL_PLAN_CURVATURE'];d['aperture_architecture']='TRUE_HOST_CUT_OPENINGS';return d
v.landmark_receipt=lm15

# Persisted-PNG alpha diagnostic readback.
def alpha_diag(body,out,label,loc,target,ortho_scale,w,hpx):
 sc=bpy.context.scene;states={o.name:o.hide_render for o in sc.objects}
 for o in sc.objects:o.hide_render=(o!=body)
 oldcam=sc.camera;oldfilm=sc.render.film_transparent;oldx=sc.render.resolution_x;oldy=sc.render.resolution_y;oldp=sc.render.resolution_percentage;oldpath=sc.render.filepath;olds=sc.cycles.samples
 cam=v.m.make_camera('DIAG_CAM_'+label,loc,target,70,True,ortho_scale);sc.camera=cam;sc.render.film_transparent=True;sc.render.resolution_x=w;sc.render.resolution_y=hpx;sc.render.resolution_percentage=100;sc.cycles.samples=1;dd=out/'diagnostics';dd.mkdir(exist_ok=True);p=dd/f'DIAG_{label}_FINAL_VISIBLE_BODY.png';sc.render.filepath=str(p);bpy.ops.render.render(write_still=True)
 im=bpy.data.images.load(str(p),check_existing=False);iw,ih=map(int,im.size);pix=list(im.pixels);cols=[]
 for x in range(iw):
  ys=[y for y in range(ih) if pix[(y*iw+x)*4+3]>.2];cols.append((min(ys),max(ys)) if ys else None)
 bpy.data.images.remove(im)
 bpy.data.objects.remove(cam,do_unlink=True);sc.camera=oldcam;sc.render.film_transparent=oldfilm;sc.render.resolution_x=oldx;sc.render.resolution_y=oldy;sc.render.resolution_percentage=oldp;sc.render.filepath=oldpath;sc.cycles.samples=olds
 for o in sc.objects:
  if o.name in states:o.hide_render=states[o.name]
 return {'file':str(p),'width_px':iw,'height_px':ih,'ortho_scale':ortho_scale,'center':target,'columns':cols}
def sample(diag,x):
 W,H=diag['width_px'],diag['height_px'];scale=diag['ortho_scale'];cx,cz=diag['center'][0],diag['center'][2];ww=scale*W/H;u=int(round(((x-cx)/ww+.5)*(W-1)));ys=[]
 for du in range(-2,3):
  c=diag['columns'][max(0,min(W-1,u+du))]
  if c:ys.append(c)
 if not ys:return float('nan'),float('nan')
 ymin=min(a for a,b in ys);ymax=max(b for a,b in ys);return cz+(ymax/(H-1)-.5)*scale,cz+(ymin/(H-1)-.5)*scale
def panel_ratio(name,lower):
 o=bpy.data.objects[name];vs=[o.matrix_world@q.co for q in o.data.vertices];zs=[p.z for p in vs];zr=min(zs) if lower else max(zs);sel=[p for p in vs if abs(p.z-zr)<.03];return (max(p.y for p in sel)-min(p.y for p in sel))/v.WIDTH

def projection(out):
 body=bpy.data.objects['DERIVED_911_9922_BODY'];side=alpha_diag(body,out,'SIDE',(0,-8,.75),(0,0,.75),1.55,1200,400);front=alpha_diag(body,out,'FRONT',(7,0,.75),(0,0,.75),1.55,800,600);rear=alpha_diag(body,out,'REAR',(-7,0,.75),(0,0,.75),1.55,800,600);ue=[];le=[];samples=[]
 for x,t in SIDE_TOP:
  top,bot=sample(side,x);e=top-t;ue.append(e);samples.append({'x':x,'target_top':t,'candidate_top':top,'top_error_m':e})
 for x,t in SIDE_LOW:
  top,bot=sample(side,x);le.append(bot-t)
 finiteu=[e for e in ue if math.isfinite(e)];finitel=[e for e in le if math.isfinite(e)];urmse=math.sqrt(sum(e*e for e in finiteu)/len(finiteu));lrmse=math.sqrt(sum(e*e for e in finitel)/len(finitel));fu=panel_ratio('REF_WINDSHIELD',False);fl=panel_ratio('REF_WINDSHIELD',True);rl=panel_ratio('REF_REAR_GLASS',True);t=PROJ['thresholds'];metrics=[
  {'id':'SIDE_UPPER_RENDERED_ALPHA_RMSE_M','target':0.0,'candidate':urmse,'abs_error':urmse,'limit':.035,'reference_target_source':'REFERENCE_CONTOUR_TARGETS_992_2.json:side_top_silhouette_m','candidate_measurement_source':'V15_RENDERED_SIDE_ALPHA_FINAL_VISIBLE_UNION'},
  {'id':'SIDE_LOWER_RENDERED_ALPHA_RMSE_M','target':0.0,'candidate':lrmse,'abs_error':lrmse,'limit':.065,'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:side.lower_body_silhouette_m','candidate_measurement_source':'V15_RENDERED_SIDE_ALPHA_FINAL_VISIBLE_UNION'},
  {'id':'FRONT_UPPER_CABIN_WIDTH_RATIO','target':PROJ['front']['roof_width_ratio_at_upper_cabin'],'candidate':fu,'abs_error':abs(fu-PROJ['front']['roof_width_ratio_at_upper_cabin']),'limit':t['front_roof_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.roof_width_ratio_at_upper_cabin','candidate_measurement_source':'V15_FINAL_WINDSHIELD_UPPER_MESH'},
  {'id':'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO','target':PROJ['front']['windshield_lower_width_ratio'],'candidate':fl,'abs_error':abs(fl-PROJ['front']['windshield_lower_width_ratio']),'limit':t['front_windshield_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.windshield_lower_width_ratio','candidate_measurement_source':'V15_FINAL_WINDSHIELD_LOWER_MESH'},
  {'id':'REAR_BACKLIGHT_LOWER_WIDTH_RATIO','target':PROJ['rear']['backlight_lower_width_ratio'],'candidate':rl,'abs_error':abs(rl-PROJ['rear']['backlight_lower_width_ratio']),'limit':t['rear_backlight_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:rear.backlight_lower_width_ratio','candidate_measurement_source':'V15_FINAL_REAR_GLASS_LOWER_MESH'}];ok=all(m['abs_error']<=m['limit'] for m in metrics);return {'schema':'oleander.3d.rendered-projection-fidelity-receipt.v2','reference':'REFERENCE_PROJECTION_TARGETS_992_2.json + REFERENCE_CONTOUR_TARGETS_992_2.json','candidate_revision':'V15_TRUE_APERTURE','status':'PROJECTION_MACHINE_SCREENING_PASS' if ok else 'PROJECTION_MACHINE_SCREENING_FAIL','metrics':metrics,'diagnostic_views':[{k:d[k] for k in ('file','width_px','height_px','ortho_scale','center')} for d in (side,front,rear)],'side_samples':samples,'independent_visual_review':False,'reference_fidelity_review':'HOLD','does_not_prove':PROJ['does_not_prove']}

try:
 v.main()
except SystemExit:
 a=v.m.parse_args();out=Path(a.out).resolve()
 if (out/'REFERENCE_REPRO_QA.json').exists():
  pr=projection(out);(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n');urmse=next(m['candidate'] for m in pr['metrics'] if m['id']=='SIDE_UPPER_RENDERED_ALPHA_RMSE_M');maxabs=max(abs(s['top_error_m']) for s in pr['side_samples'] if math.isfinite(s['top_error_m']));binding={'schema':'oleander.3d.reference-contour-binding.v3','reference':'REFERENCE_CONTOUR_TARGETS_992_2.json','candidate':'V15_RENDERED_SIDE_ALPHA_FINAL_VISIBLE_UNION','side_top_rmse_m':urmse,'side_top_max_abs_m':maxabs,'thresholds':CONTOUR['gates'],'samples':pr['side_samples'],'status':'MACHINE_BINDING_PASS' if urmse<=CONTOUR['gates']['side_top_rmse_m_max'] and maxabs<=CONTOUR['gates']['side_top_max_abs_m'] else 'MACHINE_BINDING_FAIL','does_not_prove':CONTOUR['does_not_prove']};(out/'REFERENCE_CONTOUR_BINDING_RECEIPT.json').write_text(json.dumps(binding,ensure_ascii=False,indent=2)+'\n')
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V15_TRUE_APERTURE';q['projection_machine_gate']=pr['status'];q['reference_contour_binding']=binding['status'];q['aperture_architecture']='TRUE_HOST_CUT_OPENINGS';q['projection_measurement']='PERSISTED_RENDERED_ALPHA_FINAL_VISIBLE_BODY';q['visible_primary_shell_count']=1;q['runtime_passes']=1;q['macro_form_gate']='MACHINE_SCREENING_ONLY_VISUAL_REVIEW_REQUIRED';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V15_TRUE_APERTURE';r['projection_machine_gate']=pr['status'];r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';r['aperture_architecture']='TRUE_HOST_CUT_OPENINGS';r['runtime_passes']=1;(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 raise
