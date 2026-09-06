#!/usr/bin/env python3
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector

OBJ='BLENDER_SUBD_SAME_SOURCE'

def cli():
    argv=sys.argv; argv=argv[argv.index('--')+1:] if '--' in argv else []
    p=argparse.ArgumentParser(); p.add_argument('--mode',choices=['build','reopen'],required=True); p.add_argument('--out',required=True); p.add_argument('--source'); p.add_argument('--freecad-obj'); return p.parse_args(argv)

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''): h.update(c)
    return h.hexdigest()

def load_source(path):
    d=json.loads(Path(path).read_text()); assert d['schema']=='oleander.3d.same-source-control-rings.v1'; return d

def build_cage(src):
    rings=src['rings']; seg=int(src['subd_radial_control_segments']); verts=[]; ring_ids=[]
    for r in rings:
        x=float(r['x']); rad=float(r['radius'])
        if rad==0:
            ring_ids.append(len(verts)); verts.append((x,0.0,0.0))
        else:
            ids=[]
            for j in range(seg):
                a=2*math.pi*j/seg; ids.append(len(verts)); verts.append((x,rad*math.cos(a),rad*math.sin(a)))
            ring_ids.append(ids)
    faces=[]
    first=ring_ids[0]; r1=ring_ids[1]
    for j in range(seg): faces.append((first,r1[j],r1[(j+1)%seg]))
    for i in range(1,len(rings)-2):
        a=ring_ids[i]; b=ring_ids[i+1]
        for j in range(seg): faces.append((a[j],b[j],b[(j+1)%seg],a[(j+1)%seg]))
    last=ring_ids[-1]; rn=ring_ids[-2]
    for j in range(seg): faces.append((rn[j],last,rn[(j+1)%seg]))
    mesh=bpy.data.meshes.new('SUBD_CONTROL_CAGE'); mesh.from_pydata(verts,[],faces); mesh.update()
    obj=bpy.data.objects.new(OBJ,mesh); bpy.context.collection.objects.link(obj)
    for p in mesh.polygons: p.use_smooth=True
    mod=obj.modifiers.new('CATMULL_CLARK_LIMIT','SUBSURF'); mod.subdivision_type='CATMULL_CLARK'; mod.levels=2; mod.render_levels=2
    return obj,mod,len(verts),len(faces)

def bbox_coords(coords):
    xs=[v[0] for v in coords]; ys=[v[1] for v in coords]; zs=[v[2] for v in coords]
    return {'min':[min(xs),min(ys),min(zs)],'max':[max(xs),max(ys),max(zs)],'size':[max(xs)-min(xs),max(ys)-min(ys),max(zs)-min(zs)]}

def evaluated_obj(obj,mod,level,path):
    mod.levels=level; mod.render_levels=level; bpy.context.view_layer.update(); dg=bpy.context.evaluated_depsgraph_get(); eo=obj.evaluated_get(dg); me=eo.to_mesh(); me.calc_loop_triangles()
    coords=[tuple(eo.matrix_world @ v.co) for v in me.vertices]
    with open(path,'w',encoding='utf-8') as f:
        f.write(f'# OLEANDER Blender Catmull-Clark evaluated level {level}\n')
        for v in coords: f.write(f'v {v[0]:.9f} {v[1]:.9f} {v[2]:.9f}\n')
        for tri in me.loop_triangles:
            a,b,c=[i+1 for i in tri.vertices]; f.write(f'f {a} {b} {c}\n')
    stats={'level':level,'vertices':len(me.vertices),'polygons':len(me.polygons),'triangles':len(me.loop_triangles),'bbox_mm':bbox_coords(coords),'file':Path(path).name,'bytes':Path(path).stat().st_size,'sha256':sha256(path)}
    eo.to_mesh_clear(); return stats

def aim(obj,target=(0,0,0)):
    d=Vector(target)-obj.location; obj.rotation_euler=d.to_track_quat('-Z','Y').to_euler()

def mat(name,rough=.25):
    m=bpy.data.materials.new(name); m.use_nodes=True; bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(0.46,0.50,0.54,1); bs.inputs['Metallic'].default_value=0.0; bs.inputs['Roughness'].default_value=rough; return m

def render_diagnostic(out,obj,freecad_obj_path):
    scene=bpy.context.scene; scene.render.engine='BLENDER_EEVEE'; scene.render.resolution_x=640; scene.render.resolution_y=400; scene.render.resolution_percentage=100; scene.render.image_settings.file_format='PNG'; scene.render.film_transparent=False
    world=bpy.data.worlds.new('WORLD_DIAGNOSTIC'); world.use_nodes=True; scene.world=world; bg=world.node_tree.nodes.get('Background'); bg.inputs['Color'].default_value=(0.018,0.018,0.022,1); bg.inputs['Strength'].default_value=0.16
    bpy.ops.object.camera_add(location=(300,-360,210)); cam=bpy.context.object; cam.data.lens=72; aim(cam,(0,0,0)); scene.camera=cam
    ld=bpy.data.lights.new('STRIP_KEY','AREA'); ld.energy=900; ld.shape='RECTANGLE'; ld.size=70; ld.size_y=300; lo=bpy.data.objects.new('STRIP_KEY',ld); bpy.context.collection.objects.link(lo); lo.location=(20,-170,230); aim(lo,(0,0,0))
    ld2=bpy.data.lights.new('BROAD_FILL','AREA'); ld2.energy=430; ld2.shape='DISK'; ld2.size=240; lo2=bpy.data.objects.new('BROAD_FILL',ld2); bpy.context.collection.objects.link(lo2); lo2.location=(-180,-80,160); aim(lo2,(0,0,0))
    mod=obj.modifiers['CATMULL_CLARK_LIMIT']; mod.levels=4; mod.render_levels=4; obj.data.materials.clear(); obj.data.materials.append(mat('SUBD_DIAGNOSTIC'))
    fc=None
    if freecad_obj_path and Path(freecad_obj_path).exists():
        bpy.ops.wm.obj_import(filepath=str(Path(freecad_obj_path).resolve())); fc=bpy.context.selected_objects[0]; fc.name='FREECAD_NURBS_REFERENCE'; fc.data.materials.clear(); fc.data.materials.append(mat('NURBS_DIAGNOSTIC'))
    if fc: fc.hide_render=True
    obj.hide_render=False; scene.render.filepath=str(out/'BLENDER_SUBD_DIAGNOSTIC.png'); bpy.ops.render.render(write_still=True)
    if fc:
        obj.hide_render=True; fc.hide_render=False; scene.render.filepath=str(out/'FREECAD_NURBS_DIAGNOSTIC.png'); bpy.ops.render.render(write_still=True); obj.hide_render=False

def build(args):
    out=Path(args.out).resolve(); out.mkdir(parents=True,exist_ok=True); src=load_source(args.source)
    bpy.ops.wm.read_factory_settings(use_empty=True); obj,mod,cv,cf=build_cage(src); obj['oleander_source_sha256']=sha256(args.source); obj['oleander_source_role']='shared control architecture, not interpolation constraints'; obj['oleander_radial_segments']=int(src['subd_radial_control_segments'])
    native=out/'BLENDER_SUBD_SAME_SOURCE.blend'; bpy.ops.wm.save_as_mainfile(filepath=str(native))
    l2=evaluated_obj(obj,mod,2,out/'BLENDER_SUBD_L2.obj'); l4=evaluated_obj(obj,mod,4,out/'BLENDER_SUBD_L4.obj'); mod.levels=2; mod.render_levels=2
    receipt={'schema':'oleander.3d.nurbs-subd.same-source.blender.v1','mode':'build','blender_version':bpy.app.version_string,'source_controls':Path(args.source).name,'source_controls_sha256':sha256(args.source),'representation':'polygon radial control cage -> Catmull-Clark Subdivision Surface','control_role':'rings/cage controls, not interpolation constraints','control_vertices':cv,'control_faces':cf,'radial_segments':int(src['subd_radial_control_segments']),'evaluated':[l2,l4],'native':{'file':native.name,'bytes':native.stat().st_size,'sha256':sha256(native)},'promotion_scope':['same control-ring source executed as Blender Catmull-Clark SubD','native .blend with unapplied Subdivision modifier','evaluated L2/L4 meshes for sampling-vs-representation comparison'],'holds':['Rhino native SubD/NURBS parity','Maya/Max SubD parity','manufacturing truth','aerodynamic performance','Design KEEP']}
    render_diagnostic(out,obj,args.freecad_obj); receipt['diagnostic_renders']=[p.name for p in [out/'BLENDER_SUBD_DIAGNOSTIC.png',out/'FREECAD_NURBS_DIAGNOSTIC.png'] if p.exists()]
    (out/'BLENDER_BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n'); print(json.dumps(receipt,indent=2))

def reopen(args):
    out=Path(args.out).resolve(); obj=bpy.data.objects.get(OBJ)
    if obj is None: raise RuntimeError('native reopen missing SubD object')
    mods=[m for m in obj.modifiers if m.type=='SUBSURF']; ok=len(mods)==1 and mods[0].subdivision_type=='CATMULL_CLARK' and obj.get('oleander_source_sha256') is not None
    r={'schema':'oleander.3d.nurbs-subd.same-source.blender-reopen.v1','blender_version':bpy.app.version_string,'native_reopen_valid':bool(ok),'object':OBJ,'modifier':mods[0].name if mods else None,'modifier_type':mods[0].subdivision_type if mods else None,'source_controls_sha256':obj.get('oleander_source_sha256'),'control_vertices':len(obj.data.vertices),'control_polygons':len(obj.data.polygons)}
    (out/'BLENDER_REOPEN_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps(r,indent=2))
    if not ok: raise SystemExit(8)

def main():
    args=cli(); build(args) if args.mode=='build' else reopen(args)
if __name__=='__main__': main()
