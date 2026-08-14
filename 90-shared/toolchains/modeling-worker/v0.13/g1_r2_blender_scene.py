from __future__ import annotations
from typing import Any
import bpy
from mathutils import Vector
import g1_geometry_core as base
import g1_r2_core as r2

SRC='OLEANDER_SOURCE_AUTHORITY'; DER='OLEANDER_DERIVED_EXECUTION'; QA='OLEANDER_QA_RIG'

def clean():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    root=bpy.context.scene.collection; d=bpy.data.collections.get('Collection')
    if d and d.name in root.children: root.children.unlink(d); bpy.data.collections.remove(d)

def col(name):
    c=bpy.data.collections.get(name)
    if not c: c=bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c)
    return c

def nurbs(name,pts,c,role):
    data=bpy.data.curves.new(name+'_DATA','CURVE'); data.dimensions='3D'; data.resolution_u=24
    sp=data.splines.new('NURBS'); sp.points.add(len(pts)-1)
    for p,co in zip(sp.points,pts): p.co=(*co,1.0); p.weight=1.0
    sp.order_u=min(6,len(pts)); sp.use_endpoint_u=True
    o=bpy.data.objects.new(name,data); c.objects.link(o); o.hide_render=True; o.display_type='WIRE'
    o['OLEANDER_AUTHORITY']='WORKING_SURFACE_SOURCE'; o['OLEANDER_ROLE']=role; o['OLEANDER_EDITABLE']=True
    return o

def profile(name,vals,c,role,axis):
    pts=[]
    for i,v in enumerate(vals):
        x=.190*i/(len(vals)-1)
        pts.append((x,float(v),0) if axis=='Y+' else (x,-float(v),0) if axis=='Y-' else (x,0,-float(v)) if axis=='Z-' else (x,0,float(v)))
    o=nurbs(name,pts,c,role); o['OLEANDER_PROFILE_AXIS']=axis; o['OLEANDER_CONTROL_VALUES']=[float(v) for v in vals]; return o

def sources(s,c):
    own=base.own
    out=[nurbs('OL_SRC_GRIP_AXIS',[tuple(map(float,p)) for p in own(s,'GRIP_AXIS')['control_points']],c,own(s,'GRIP_AXIS')['role'])]
    out += [profile('OL_SRC_PALM_PROFILE',own(s,'PALM_PROFILE')['control_values'],c,own(s,'PALM_PROFILE')['role'],'Z+'),
            profile('OL_SRC_THUMB_SIDE_PLAN',own(s,'THUMB_SIDE_PLAN')['control_values'],c,own(s,'THUMB_SIDE_PLAN')['role'],'Y+'),
            profile('OL_SRC_OPPOSITE_SIDE_PLAN',own(s,'OPPOSITE_SIDE_PLAN')['control_values'],c,own(s,'OPPOSITE_SIDE_PLAN')['role'],'Y-'),
            profile('OL_SRC_LOWER_RETURN_PROFILE',own(s,'LOWER_RETURN_PROFILE')['control_values'],c,own(s,'LOWER_RETURN_PROFILE')['role'],'Z-')]
    d=own(s,'INTERFACE_DECK_BOUNDARY'); o=bpy.data.objects.new('OL_SRC_INTERFACE_DECK_BOUNDARY',None); c.objects.link(o)
    o.empty_display_type='CIRCLE'; o.empty_display_size=.012; o['OLEANDER_AUTHORITY']='WORKING_SURFACE_SOURCE'; o['OLEANDER_ROLE']=d['role']; o['OLEANDER_EDITABLE']=True
    for k in ('u_center','u_halfspan','theta_center_rad','theta_halfspan_rad','depth_m','core_fraction'):
        if k in d: o[k]=float(d[k])
    o['blend']=str(d.get('blend','QUINTIC_SMOOTHERSTEP')); o.location=r2.point(s,float(d['u_center']),float(d.get('theta_center_rad',0)),False,False); out.append(o)
    return out

def mesh_obj(name,verts,faces,c,role):
    m=bpy.data.meshes.new(name+'_MESH'); m.from_pydata(verts,[],faces); m.update(); o=bpy.data.objects.new(name,m); c.objects.link(o)
    o['OLEANDER_AUTHORITY']='DERIVED_EXECUTION_NOT_AUTHORITY'; o['OLEANDER_ROLE']=role; o['OLEANDER_EDITABLE']=False
    for p in m.polygons: p.use_smooth=True
    return o

def material(name,color,rough,metal=0):
    m=bpy.data.materials.new(name); m.use_nodes=True; b=m.node_tree.nodes.get('Principled BSDF')
    if b is None: raise RuntimeError('Principled BSDF missing')
    b.inputs['Base Color'].default_value=(*color,1); b.inputs['Roughness'].default_value=rough
    if 'Metallic' in b.inputs: b.inputs['Metallic'].default_value=metal
    return m

def zebra():
    m=bpy.data.materials.new('OLEANDER_MAT_QA_ZEBRA_NORMAL_v1'); m.use_nodes=True; nt=m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out=nt.nodes.new('ShaderNodeOutputMaterial'); b=nt.nodes.new('ShaderNodeBsdfPrincipled'); geo=nt.nodes.new('ShaderNodeNewGeometry'); sep=nt.nodes.new('ShaderNodeSeparateXYZ'); mul=nt.nodes.new('ShaderNodeMath'); sine=nt.nodes.new('ShaderNodeMath'); ramp=nt.nodes.new('ShaderNodeValToRGB')
    mul.operation='MULTIPLY'; mul.inputs[1].default_value=18; sine.operation='SINE'; ramp.color_ramp.interpolation='CONSTANT'; ramp.color_ramp.elements[0].position=.49; ramp.color_ramp.elements[0].color=(.01,.01,.01,1); ramp.color_ramp.elements[1].position=.51; ramp.color_ramp.elements[1].color=(.96,.96,.96,1)
    nt.links.new(geo.outputs['Normal'],sep.inputs[0]); nt.links.new(sep.outputs['X'],mul.inputs[0]); nt.links.new(mul.outputs[0],sine.inputs[0]); nt.links.new(sine.outputs[0],ramp.inputs[0]); nt.links.new(ramp.outputs['Color'],b.inputs['Base Color']); b.inputs['Roughness'].default_value=.22; nt.links.new(b.outputs[0],out.inputs[0]); return m

def assign(o,m): o.data.materials.clear(); o.data.materials.append(m)
def aim(o,target): o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def camera(name,lens,loc,target,c):
    d=bpy.data.cameras.new(name+'_DATA'); d.lens=lens; o=bpy.data.objects.new(name,d); c.objects.link(o); o.location=loc; aim(o,target); return o

def area(name,loc,energy,size,target,c,size_y=None):
    d=bpy.data.lights.new(name+'_DATA','AREA'); d.energy=energy; d.shape='RECTANGLE' if size_y is not None else 'DISK'; d.size=size
    if size_y is not None: d.size_y=size_y
    o=bpy.data.objects.new(name,d); c.objects.link(o); o.location=loc; aim(o,target); return o

def neg_card(c,target):
    bpy.ops.mesh.primitive_plane_add(size=1,location=(.10,.34,.06)); o=bpy.context.object; o.name='R2_NEG_FILL'
    for u in list(o.users_collection): u.objects.unlink(o)
    c.objects.link(o); o.scale=(.22,.10,.26); aim(o,target); assign(o,material('R2_NEG_FILL_MAT',(.002,.002,.002),1)); return o

def rigs(c,target):
    broad=[area('BROAD_R2_KEY_BROAD',(.10,-.38,.32),560,.34,target,c,.20),area('BROAD_R2_TOP_CARD',(.12,.02,.48),420,.26,target,c,.20),area('BROAD_R2_CONTACT_FILL',(-.08,.18,.10),180,.18,target,c,.10)]
    strip=[area('STRIP_R2_SIDE_STRIP_A',(.11,-.32,.12),720,.035,target,c,.34),area('STRIP_R2_SIDE_STRIP_B',(.17,.30,.17),580,.025,target,c,.28)]
    grazing=[area('GRAZING_R2_GRAZING_STRIP',(-.10,-.24,.07),900,.025,target,c,.42)]; neg=neg_card(c,target)
    for x in broad+strip+grazing: x.hide_render=True
    return {'BROAD':[o.name for o in broad]+[neg.name],'STRIP':[o.name for o in strip]+[neg.name],'GRAZING':[o.name for o in grazing]+[neg.name],'ZEBRA':['OLEANDER_MAT_QA_ZEBRA_NORMAL_v1']}

def render_setup(scene,contract,res):
    scene.render.engine='CYCLES'; scene.cycles.samples=int(contract['runtime']['cycles_samples']); scene.cycles.use_denoising=bool(contract['runtime']['denoise'])
    if hasattr(scene.cycles,'use_adaptive_sampling'): scene.cycles.use_adaptive_sampling=bool(contract['runtime']['adaptive_sampling'])
    scene.render.resolution_x=res; scene.render.resolution_y=res; scene.render.resolution_percentage=100; scene.render.image_settings.file_format='PNG'; scene.render.film_transparent=False; scene.world.color=(.018,.018,.022)
    view=scene.view_layers[0]
    for a in ('use_pass_z','use_pass_normal','use_pass_diffuse_color','use_pass_glossy_direct','use_pass_glossy_indirect','use_pass_glossy_color','use_pass_shadow'):
        if hasattr(view,a): setattr(view,a,True)

def render(scene,out,stem,cam,obj,mat,rig,qac):
    scene.camera=cam; assign(obj,mat)
    for x in qac.objects:
        if x.type=='LIGHT': x.hide_render=not x.name.startswith(rig)
    n=bpy.data.objects.get('R2_NEG_FILL')
    if n: n.hide_render=(rig=='ZEBRA')
    scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_depth='8'; scene.render.filepath=str(out/f'{stem}.png'); bpy.ops.render.render(write_still=True); return f'{stem}.png'

def master_exr(scene,out,cam,obj,mat,qac):
    scene.camera=cam; assign(obj,mat)
    for x in qac.objects:
        if x.type=='LIGHT': x.hide_render=not x.name.startswith('BROAD')
    scene.render.image_settings.file_format='OPEN_EXR_MULTILAYER'; scene.render.image_settings.color_depth='32'; p=out/'G1_R2_BASELINE_MASTER.exr'; scene.render.filepath=str(p); bpy.ops.render.render(write_still=True); scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_depth='8'; return p.name
