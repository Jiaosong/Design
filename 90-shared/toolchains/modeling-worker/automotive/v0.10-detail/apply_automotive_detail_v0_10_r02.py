#!/usr/bin/env python3
"""OLEANDER Automotive Detail v0.10 — M8-R02 visual refinement.

Starts from an M8-R01 derived blend, removes all M8 objects, then deterministically rebuilds
refined detail. v0.9 source objects remain immutable.
"""
from __future__ import annotations
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy

MODEL='OLEANDER_Automotive_Detail_v0.10';REV='M8-R02'
ap=argparse.ArgumentParser();ap.add_argument('--base-source',required=True);ap.add_argument('--out',required=True);ap.add_argument('--samples',type=int,default=8);ap.add_argument('--resolution',type=int,default=640)
av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [];a=ap.parse_args(av)
src=Path(a.base_source).read_text();defs=src.split('if __name__=="__main__":')[0];exec(compile(defs,a.base_source,'exec'),globals(),globals());MODEL='OLEANDER_Automotive_Detail_v0.10'
body=bpy.data.objects['BODY_PRIMARY']

def is_source(o):
    if o.name.startswith('M8_'):return False
    if o.name=='GROUND' or o.name.startswith(('SEC_SHELL_','GUIDE_')) or o.name=='BODY_CONTROL_WIRE':return False
    if o.type in {'LIGHT','CAMERA'}:return False
    return o.type in {'MESH','CURVE'}

def source_hash():
    h=hashlib.sha256()
    for o in sorted([x for x in bpy.data.objects if is_source(x)],key=lambda x:x.name):
        h.update((o.name+'|'+o.type+'|').encode())
        for row in o.matrix_world:h.update(','.join(f'{v:.9f}' for v in row).encode())
        for m in o.data.materials:h.update(((m.name if m else 'NONE')+';').encode())
        if o.type=='MESH':
            for v in o.data.vertices:h.update(f'v{v.co.x:.9f},{v.co.y:.9f},{v.co.z:.9f};'.encode())
            for p in o.data.polygons:h.update(('p'+','.join(map(str,p.vertices[:]))+f':{p.material_index};').encode())
        else:
            for sp in o.data.splines:
                for bp in sp.bezier_points:h.update(f'b{bp.co.x:.9f},{bp.co.y:.9f},{bp.co.z:.9f};'.encode())
                for pt in sp.points:h.update(f'q{pt.co.x:.9f},{pt.co.y:.9f},{pt.co.z:.9f},{pt.co.w:.9f};'.encode())
    return h.hexdigest()

before=source_hash();source_names=sorted(o.name for o in bpy.data.objects if is_source(o))
# Remove R01 detail wholesale; R02 is a clean rebuild, not an additive patch.
for o in list(bpy.data.objects):
    if o.name.startswith('M8_'):bpy.data.objects.remove(o,do_unlink=True)
assert before==source_hash()

def dmat(name,c,r=.35,metal=0):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;nt.nodes.clear();outn=nt.nodes.new('ShaderNodeOutputMaterial');bs=nt.nodes.new('ShaderNodeBsdfPrincipled');set_input(bs,'Base Color',c);set_input(bs,'Roughness',r);set_input(bs,'Metallic',metal);nt.links.new(bs.outputs['BSDF'],outn.inputs['Surface']);return m
rim=dmat('MAT_M8_RIM',(.23,.25,.26,1),.30,1);disc=dmat('MAT_M8_DISC',(.10,.11,.11,1),.40,1);cal=dmat('MAT_M8_CALIPER',(.14,.025,.015,1),.40,0);mirror=dmat('MAT_M8_MIRROR_BODY',(.025,.032,.031,1),.32,0);mglass=dmat('MAT_M8_MIRROR_GLASS',(.018,.026,.029,1),.14,0);handle=dmat('MAT_M8_HANDLE',(.16,.17,.17,1),.34,1);wiper=dmat('MAT_M8_WIPER',(.010,.012,.012,1),.65,0)

def cube(name,loc,dims,mat,rot=(0,0,0),bev=.004):
    bpy.ops.mesh.primitive_cube_add(location=loc,rotation=rot);o=bpy.context.object;o.name=name;o.dimensions=dims;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
    if bev:md=o.modifiers.new('EDGE','BEVEL');md.width=bev;md.segments=3
    return o

def sphere(name,loc,scale,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=20,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    return o

def curve(name,pts,mat,depth=.003):
    cu=bpy.data.curves.new(name+'_CURVE','CURVE');cu.dimensions='3D';cu.bevel_depth=depth;cu.bevel_resolution=3;sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
    for bp,co in zip(sp.bezier_points,pts):bp.co=co;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(o);o.data.materials.append(mat);return o

def flush_handle(name,x,side):
    y=side*.943;verts=[(x-.062,y,.742),(x+.062,y,.742),(x+.057,y,.758),(x-.057,y,.758)];me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],[(0,1,2,3)]);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(handle);sw=o.modifiers.new('CONFORM','SHRINKWRAP');sw.target=body;sw.wrap_method='NEAREST_SURFACEPOINT';sw.offset=.002;bpy.context.view_layer.objects.active=o
    try:bpy.ops.object.modifier_apply(modifier=sw.name)
    except:pass
    so=o.modifiers.new('THICKNESS','SOLIDIFY');so.thickness=.0025;bv=o.modifiers.new('EDGE','BEVEL');bv.width=.003;bv.segments=2;return o

FX,RX=1.36,-1.36;WY=.79;WZ=.345
for x,ax in ((FX,'F'),(RX,'R')):
    for side,sy in ((1,'L'),(-1,'R')):
        y=side*WY
        bpy.ops.mesh.primitive_cylinder_add(vertices=56,radius=.150,depth=.014,location=(x,y+side*.052,WZ),rotation=(math.radians(90),0,0));o=bpy.context.object;o.name=f'M8_DISC_{ax}{sy}';o.data.materials.append(disc)
        bpy.ops.mesh.primitive_torus_add(major_radius=.190,minor_radius=.016,major_segments=56,minor_segments=12,location=(x,y+side*.075,WZ),rotation=(math.radians(90),0,0));o=bpy.context.object;o.name=f'M8_RIM_RING_{ax}{sy}';o.data.materials.append(rim)
        bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=.032,depth=.030,location=(x,y+side*.084,WZ),rotation=(math.radians(90),0,0));o=bpy.context.object;o.name=f'M8_HUB_{ax}{sy}';o.data.materials.append(rim)
        # Five clean single spokes: lower visual density than R01 split-spoke pattern.
        for i in range(5):
            aa=2*math.pi*i/5;rr=.105;px=x+rr*math.cos(aa);pz=WZ+rr*math.sin(aa);cube(f'M8_SPOKE_{ax}{sy}_{i}',(px,y+side*.088,pz),(.165,.017,.013),rim,(0,-aa,0),.003)
        cube(f'M8_CALIPER_{ax}{sy}',(x-.105,y+side*.065,WZ),(.050,.018,.095),cal,(0,0,0),.007)
# Smaller/lower mirrors.
for side,sy in ((1,'L'),(-1,'R')):
    y=side*.978;sphere(f'M8_MIRROR_{sy}',(.65,y,.985),(.105,.043,.040),mirror);cube(f'M8_MIRROR_STEM_{sy}',(.625,side*.952,.955),(.070,.022,.030),mirror,(0,0,0),.008);cube(f'M8_MIRROR_GLASS_{sy}',(.646,y+side*.039,.986),(.076,.004,.035),mglass,(0,0,0),.006)
for side,sy in ((1,'L'),(-1,'R')):
    flush_handle(f'M8_HANDLE_FRONT_{sy}',.36,side);flush_handle(f'M8_HANDLE_REAR_{sy}',-.63,side)
curve('M8_WIPER_L',[(.72,-.14,.934),(.52,-.27,1.005)],wiper,.0033);curve('M8_WIPER_R',[(.72,.11,.934),(.54,.23,1.00)],wiper,.0033)

after=source_hash();m8=[o for o in bpy.data.objects if o.name.startswith('M8_')]
lights={'BROAD':[bpy.data.objects['BROAD_KEY'],bpy.data.objects['BROAD_FILL']],'STRIP':[bpy.data.objects['STRIP_KEY'],bpy.data.objects['STRIP_FILL']],'GRAZING':[bpy.data.objects['GRAZING_KEY'],bpy.data.objects['GRAZING_FILL']]}
for o in bpy.data.objects:
    if o.name.startswith(('SEC_SHELL_','GUIDE_')) or o.name=='BODY_CONTROL_WIRE':o.hide_render=True

def rv(out,label,loc,target,lens=75,ortho=False,scale=5,rig='BROAD',override=None):
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True);set_rig(lights,rig);layer=bpy.context.view_layer;old=layer.material_override;layer.material_override=override;set_world((.012,.012,.012),.16);cam=camera('CAM_'+label,loc,target,lens,ortho,scale);bpy.context.scene.camera=cam;p=rd/f'{MODEL}__{label}.png';setup_render(p,a.samples,a.resolution);bpy.ops.render.render(write_still=True);layer.material_override=old;bpy.data.objects.remove(cam,do_unlink=True);return {'view':label,'file':str(p),'rig':rig,'override':override.name if override else None}
out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);clay=bpy.data.materials['MAT_PRIMARY_CLAY'];renders=[rv(out,'HERO_FRONT_3Q',(5.8,-6.6,2.65),(.05,0,.63)),rv(out,'HERO_REAR_3Q',(-5.6,6.3,2.55),(-.08,0,.62)),rv(out,'SIDE_PROFILE',(0,-8.4,1.20),(0,0,.62),85,True,5.15),rv(out,'WHEEL_DETAIL',(2.05,-3.0,.92),(FX,-WY,.35),100,False,2.25),rv(out,'MIRROR_HANDLE_DETAIL',(2.1,-3.0,1.45),(.45,-.86,.88),95,False,2.3),rv(out,'TOP_3Q',(4.6,-5.2,5.0),(0,0,.58),78),rv(out,'CLAY_STRIP',(5.8,-6.6,2.65),(.05,0,.63),75,False,5,'STRIP',clay),rv(out,'CLAY_GRAZING',(5.8,-6.6,2.65),(.05,0,.63),75,False,5,'GRAZING',clay)]
checks={'source_model_hash_unchanged':before==after,'source_model_object_set_unchanged':source_names==sorted(o.name for o in bpy.data.objects if is_source(o)),'primary_manifold':nonmanifold(body)==0,'wheel_disc_count':len([o for o in m8 if o.name.startswith('M8_DISC_')])==4,'wheel_ring_count':len([o for o in m8 if o.name.startswith('M8_RIM_RING_')])==4,'wheel_spoke_count':len([o for o in m8 if o.name.startswith('M8_SPOKE_')])==20,'caliper_count':len([o for o in m8 if o.name.startswith('M8_CALIPER_')])==4,'mirror_housing_count':len([o for o in m8 if o.name.startswith('M8_MIRROR_') and 'STEM' not in o.name and 'GLASS' not in o.name])==2,'mirror_glass_count':len([o for o in m8 if o.name.startswith('M8_MIRROR_GLASS_')])==2,'handle_count':len([o for o in m8 if o.name.startswith('M8_HANDLE_')])==4,'wiper_count':len([o for o in m8 if o.name.startswith('M8_WIPER_')])==2,'render_matrix':len(renders)==8}
qa={'schema':'oleander.automotive-detail.qa.v0.10-r02','model':MODEL,'revision':REV,'source_authority':'OLEANDER_Automotive_Secondary_v0.9','status':'MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL','source_scene_hash_before':before,'source_scene_hash_after':after,'source_object_count':len(source_names),'m8_component_count':len(m8),'checks':checks,'renders':renders,'revision_scope':'M8 clean rebuild from v0.9 lineage; smaller mirror/handle, lower wheel-detail density.','boundary':'Exterior detail benchmark only; interior package/CMF remain later scope.'};(out/'AUTOMOTIVE_M8_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
bpy.context.scene['OLEANDER_MODEL']=MODEL;bpy.context.scene['OLEANDER_STAGE']='M8';bpy.context.scene['OLEANDER_REVISION']=REV;blend=out/f'{MODEL}.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));rec={'schema':'oleander.automotive-detail.receipt.v0.10-r02','model':MODEL,'revision':REV,'blender_version':bpy.app.version_string,'status':'EXECUTED_MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if qa['status'].startswith('MACHINE_PASS') else 'EXECUTED_MACHINE_FAIL','blend':str(blend),'qa':str(out/'AUTOMOTIVE_M8_QA.json'),'renders':renders};(out/'AUTOMOTIVE_M8_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if qa['status'].startswith('MACHINE_PASS') else 5)
