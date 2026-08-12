#!/usr/bin/env python3
"""v0.5 revision wrapper: reuse v0.4 cabin/window logic, rebuild body without end-cap subdivision pinching, and place wheel faces outboard."""
import argparse,sys,math,json
from pathlib import Path
import bpy

ap=argparse.ArgumentParser();ap.add_argument('--v04-source',required=True);ap.add_argument('--out',required=True);ap.add_argument('--samples',type=int,default=8);ap.add_argument('--resolution',type=int,default=720)
av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
a=ap.parse_args(av)

# Load v0.4 helper/function definitions without executing its main().
code=Path(a.v04_source).read_text(encoding='utf-8')
code=code.split('if __name__=="__main__":main()')[0]
exec(compile(code,a.v04_source,'exec'),globals(),globals())
MODEL='OLEANDER_Automotive_Reference_Vehicle_v0.5'

def rebuild_body_v05():
    delete('BODY_SHELL','CENTER_SILL','LOWER_SILL','FRONT_LOWER','REAR_LOWER','ARCH_','SHOULDER_','HOOD_','HATCH_')
    st=[
      (-2.23,.82,.27,.58),(-2.14,.88,.23,.64),(-1.96,.91,.20,.71),(-1.70,.925,.18,.78),
      (-1.42,.932,.17,.84),(-1.12,.935,.17,.88),(-.72,.938,.165,.90),(-.20,.94,.165,.91),
      (.35,.94,.165,.91),(.78,.938,.165,.90),(1.12,.934,.17,.88),(1.42,.928,.18,.84),
      (1.70,.92,.19,.79),(1.96,.91,.21,.72),(2.14,.88,.24,.65),(2.23,.82,.29,.59)]
    # no global Subdivision here: the n-gon front/rear caps must remain planar and free of star pinching
    b=loft('BODY_SHELL',st,M('MAT_BODY_PAINT'),30,4.8,0);arch(b,FX);arch(b,RX)
    for p in b.data.polygons:p.use_smooth=True
    bev=b.modifiers.new('BODY_BEVEL','BEVEL');bev.width=.010;bev.segments=3
    cube('CENTER_SILL',(0,0,.265),(1.78,1.81,.16),M('MAT_PP_FINE_MATTE_D2'),.028)
    cube('FRONT_LOWER',(2.12,0,.405),(.14,1.16,.18),M('MAT_PP_FINE_MATTE_D2'),.024)
    cube('REAR_LOWER',(-2.12,0,.405),(.14,1.12,.18),M('MAT_PP_FINE_MATTE_D2'),.024)
    for y in (-.936,.936):curve('SHOULDER_L' if y>0 else 'SHOULDER_R',[(1.72,y,.76),(1.10,y,.83),(.25,y,.85),(-.72,y,.83),(-1.62,y,.75)],M('MAT_BODY_PAINT'),.0035)
    for y in (-.47,.47):
        curve(f'HOOD_{y:+}',[(2.05,y,.69),(1.58,y,.80),(1.05,y,.88)],M('MAT_PP_FINE_MATTE_D2'),.0028)
        curve(f'HATCH_{y:+}',[(-1.08,y,.88),(-1.52,y,.80),(-2.00,y,.69)],M('MAT_PP_FINE_MATTE_D2'),.0028)

def rebuild_wheels_v05():
    for o in list(bpy.data.objects):
        if '_SPOKE_' in o.name or o.name.endswith('_HUB') or o.name.endswith('_RIM') or 'RIM_RING' in o.name or o.name.endswith('_DISC'):
            bpy.data.objects.remove(o,do_unlink=True)
    for x,fx in [(FX,'F'),(RX,'R')]:
        for y,sy in [(WY,'L'),(-WY,'R')]:
            name=f'WHEEL_{fx}{sy}';sgn=1 if y>0 else -1;face_y=y+sgn*.105;disc_y=y+sgn*.070
            bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.142,depth=.025,location=(x,disc_y,WZ),rotation=(math.radians(90),0,0));d=bpy.context.object;d.name=name+'_DISC';d.data.materials.append(M('MAT_BRAKE_DISC'))
            bpy.ops.mesh.primitive_torus_add(major_radius=.188,minor_radius=.018,major_segments=64,minor_segments=14,location=(x,face_y,WZ),rotation=(math.radians(90),0,0));r=bpy.context.object;r.name=name+'_RIM';r.data.materials.append(M('MAT_BRUSHED_ANODIZED_D2'))
            bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.034,depth=.028,location=(x,face_y,WZ),rotation=(math.radians(90),0,0));h=bpy.context.object;h.name=name+'_HUB';h.data.materials.append(M('MAT_BRUSHED_ANODIZED_D2'))
            for i in range(5):
                ang=2*math.pi*i/5
                for j,da in enumerate((-.055,.055)):
                    aa=ang+da;rr=.108;sx=x+rr*math.cos(aa);sz=WZ+rr*math.sin(aa)
                    cube(f'{name}_SPOKE_{i}_{j}',(sx,face_y,sz),(.135,.020,.012),M('MAT_BRUSHED_ANODIZED_D2'),.003,rot=(0,-aa,0))

def ensure_clay():
    if bpy.data.materials.get('MAT_CLAY') is not None:return
    m=bpy.data.materials.new('MAT_CLAY');m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF')
    if bs is not None:
        if bs.inputs.get('Base Color'):bs.inputs['Base Color'].default_value=(.32,.315,.295,1)
        if bs.inputs.get('Roughness'):bs.inputs['Roughness'].default_value=.52

out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
rebuild_body_v05();rebuild_cabin();rebuild_wheels_v05();refine_details();ensure_clay()
bpy.context.scene['OLEANDER_MODEL']=MODEL
bpy.ops.wm.save_as_mainfile(filepath=str(out/f'{MODEL}.blend'))
R=render(out,a.samples,a.resolution)
q=qa(out,R)
# Rewrite v0.4 QA identity to the v0.5 model.
q['model']=MODEL;q['schema']='oleander.automotive.qa.v5'
(out/'AUTOMOTIVE_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rec={'schema':'oleander.automotive.receipt.v5','model':MODEL,'blender_version':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),'status':'EXECUTED_QA_PASS' if q['status']=='PASS' else 'EXECUTED_QA_FAIL','renders':R,'qa':str(out/'AUTOMOTIVE_QA.json')}
(out/'AUTOMOTIVE_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(rec,ensure_ascii=False,indent=2))
raise SystemExit(0 if q['status']=='PASS' else 5)
