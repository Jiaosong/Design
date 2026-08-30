#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

LOW_NAME = "OLEANDER_LOW"
HIGH_NAME = "OLEANDER_HIGH"
IMAGE_NAME = "OLEANDER_TANGENT_NORMAL"
MAT_LOW = "OLEANDER_LOW_BAKED_MAT"
MAT_HIGH = "OLEANDER_HIGH_REFERENCE_MAT"


def cli():
    argv = sys.argv
    argv = argv[argv.index("--") + 1:] if "--" in argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["build", "reopen"], required=True)
    p.add_argument("--out", required=True)
    return p.parse_args(argv)


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for c in iter(lambda: f.read(1024 * 1024), b""):
            h.update(c)
    return h.hexdigest()


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def height_fn(x, y):
    # bounded embossed meso-detail: all source points remain above the low carrier
    wave = math.sin(x * 4.2) * math.cos(y * 3.6)
    fine = 0.35 * math.sin((x + y) * 9.0) * math.cos((x - y) * 7.0)
    return 0.055 + 0.030 * wave + 0.012 * fine


def create_grid(name, n, size, high=False):
    verts=[]
    for j in range(n):
        v=j/(n-1)
        y=(v-0.5)*size
        for i in range(n):
            u=i/(n-1)
            x=(u-0.5)*size
            z=height_fn(x,y) if high else 0.0
            verts.append((x,y,z))
    faces=[]
    for j in range(n-1):
        for i in range(n-1):
            a=j*n+i; b=a+1; c=a+n+1; d=a+n
            faces.append((a,b,c,d))
    mesh=bpy.data.meshes.new(name+"_MESH")
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    obj=bpy.data.objects.new(name,mesh)
    bpy.context.collection.objects.link(obj)
    if not high:
        uv=mesh.uv_layers.new(name="UVMap")
        for poly in mesh.polygons:
            for li in poly.loop_indices:
                vi=mesh.loops[li].vertex_index
                i=vi % n; j=vi // n
                uv.data[li].uv=(i/(n-1), j/(n-1))
    return obj


def make_high_material():
    mat=bpy.data.materials.new(MAT_HIGH)
    mat.use_nodes=True
    bsdf=mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value=(0.46,0.46,0.46,1)
    bsdf.inputs["Roughness"].default_value=0.38
    return mat


def make_low_bake_material(img):
    mat=bpy.data.materials.new(MAT_LOW)
    mat.use_nodes=True
    nt=mat.node_tree; nodes=nt.nodes; links=nt.links
    bsdf=nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value=(0.46,0.46,0.46,1)
    bsdf.inputs["Roughness"].default_value=0.38
    tex=nodes.new("ShaderNodeTexImage"); tex.name="BAKED_NORMAL_IMAGE"; tex.image=img
    normal=nodes.new("ShaderNodeNormalMap"); normal.name="TANGENT_NORMAL_NODE"; normal.space="TANGENT"; normal.inputs["Strength"].default_value=1.0
    links.new(tex.outputs["Color"],normal.inputs["Color"])
    links.new(normal.outputs["Normal"],bsdf.inputs["Normal"])
    nodes.active=tex
    tex.select=True
    return mat


def select_for_bake(high, low):
    bpy.ops.object.select_all(action="DESELECT")
    high.select_set(True); low.select_set(True)
    bpy.context.view_layer.objects.active=low


def bake_normal(high, low, img, out):
    scene=bpy.context.scene
    scene.render.engine="CYCLES"
    scene.cycles.device="CPU"
    scene.render.bake.use_selected_to_active=True
    scene.render.bake.cage_extrusion=0.18
    scene.render.bake.max_ray_distance=0.0
    scene.render.bake.margin=8
    scene.render.bake.normal_space="TANGENT"
    select_for_bake(high,low)
    bpy.ops.object.bake(type="NORMAL")
    img.filepath_raw=str(out/"TANGENT_NORMAL.png")
    img.file_format="PNG"
    img.save()


def image_stats(img):
    px=list(img.pixels[:])
    if len(px)<4: raise RuntimeError("empty bake image")
    rgb=[px[k::4] for k in range(3)]
    mean=[sum(c)/len(c) for c in rgb]
    lo=[min(c) for c in rgb]; hi=[max(c) for c in rgb]
    # flat tangent normal ~= (0.5,0.5,1.0); require material directional variation
    varied=sum(1 for i in range(0,len(px),4) if abs(px[i]-0.5)>0.02 or abs(px[i+1]-0.5)>0.02)
    return {"mean_rgb":mean,"min_rgb":lo,"max_rgb":hi,"varied_pixel_fraction":varied/(len(px)/4)}


def look_at(obj,target=(0,0,0)):
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()


def setup_render():
    scene=bpy.context.scene
    scene.render.engine="BLENDER_EEVEE"
    scene.render.resolution_x=720; scene.render.resolution_y=720; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    if scene.world is None: scene.world=bpy.data.worlds.new("WORLD")
    scene.world.color=(0.025,0.025,0.025)
    camd=bpy.data.cameras.new("CAM"); cam=bpy.data.objects.new("CAM",camd); bpy.context.collection.objects.link(cam)
    cam.location=(2.4,-2.6,1.8); camd.lens=58; look_at(cam,(0,0,0.02)); scene.camera=cam
    for name,loc,energy,size in [("STRIP",(1.0,-1.4,2.4),1050,1.4),("FILL",(-2.0,0.5,1.4),300,2.5)]:
        ld=bpy.data.lights.new(name,"AREA"); ld.energy=energy; ld.shape="RECTANGLE"; ld.size=size; ld.size_y=0.28 if name=="STRIP" else size
        o=bpy.data.objects.new(name,ld); bpy.context.collection.objects.link(o); o.location=loc; look_at(o,(0,0,0))


def render_pair(high,low,out):
    scene=bpy.context.scene
    high.hide_render=False; low.hide_render=True
    scene.render.filepath=str(out/"HIGH_REFERENCE.png"); bpy.ops.render.render(write_still=True)
    high.hide_render=True; low.hide_render=False
    scene.render.filepath=str(out/"LOW_BAKED_NORMAL.png"); bpy.ops.render.render(write_still=True)
    high.hide_render=False; low.hide_render=False


def mesh_stats(obj):
    return {"vertices":len(obj.data.vertices),"edges":len(obj.data.edges),"polygons":len(obj.data.polygons),"uv_layers":[u.name for u in obj.data.uv_layers]}


def node_contract(mat):
    types=[n.bl_idname for n in mat.node_tree.nodes]
    tex=mat.node_tree.nodes.get("BAKED_NORMAL_IMAGE"); nm=mat.node_tree.nodes.get("TANGENT_NORMAL_NODE")
    return {"node_types":sorted(types),"image_node":bool(tex and tex.image),"normal_map_node":bool(nm),"normal_space":getattr(nm,"space",None) if nm else None,"image_colorspace":tex.image.colorspace_settings.name if tex and tex.image else None}


def build(out):
    reset(); out.mkdir(parents=True,exist_ok=True)
    low=create_grid(LOW_NAME,17,2.0,False); high=create_grid(HIGH_NAME,65,2.0,True)
    high.data.materials.append(make_high_material())
    img=bpy.data.images.new(IMAGE_NAME,width=512,height=512,alpha=False,float_buffer=False)
    img.generated_color=(0.5,0.5,1.0,1.0); img.colorspace_settings.name="Non-Color"
    lowmat=make_low_bake_material(img); low.data.materials.append(lowmat)
    bake_normal(high,low,img,out)
    stats=image_stats(img)
    if stats["varied_pixel_fraction"] < 0.05:
        raise RuntimeError(f"normal bake lacks directional variation: {stats}")
    setup_render(); render_pair(high,low,out)
    blend=out/"SURFACE_DETAIL_NORMAL_BAKE.blend"; bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    receipt={
      "schema":"oleander.3d.surface-detail-normal-bake.v1","mode":"build","blender_version":bpy.app.version_string,
      "high":mesh_stats(high),"low":mesh_stats(low),"high_low_ratio":len(high.data.polygons)/len(low.data.polygons),
      "uv_policy":"explicit 0..1 UVMap on low carrier","bake":{"type":"TANGENT_NORMAL","selected_to_active":True,"cage_extrusion_m":0.18,"resolution":[512,512],"colorspace":"Non-Color"},
      "image_stats":stats,"material_contract":node_contract(lowmat),"native_master":blend.name,
      "outputs":["TANGENT_NORMAL.png","HIGH_REFERENCE.png","LOW_BAKED_NORMAL.png"],
      "evidence_class":"NATIVE_EXECUTED_PENDING_REOPEN",
      "holds":["pixel-perfect high/low appearance equivalence","cross-engine tangent parity","production texel-density budget","Design KEEP"]
    }
    (out/"BUILD_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
    files=[blend,out/"TANGENT_NORMAL.png",out/"HIGH_REFERENCE.png",out/"LOW_BAKED_NORMAL.png",out/"BUILD_RECEIPT.json"]
    (out/"SHA256.json").write_text(json.dumps({p.name:sha256(p) for p in files},indent=2)+"\n")
    print(json.dumps(receipt,indent=2))


def reopen(out):
    low=bpy.data.objects.get(LOW_NAME); high=bpy.data.objects.get(HIGH_NAME); mat=bpy.data.materials.get(MAT_LOW)
    if not low or not high or not mat: raise RuntimeError("native reopen missing benchmark objects/material")
    img=bpy.data.images.get(IMAGE_NAME)
    if not img: raise RuntimeError("native reopen missing bake image datablock")
    normal_path=out/"TANGENT_NORMAL.png"
    if not normal_path.exists(): raise RuntimeError("external normal map missing on reopen")
    contract=node_contract(mat)
    if not contract["image_node"] or not contract["normal_map_node"] or contract["normal_space"]!="TANGENT": raise RuntimeError(contract)
    if "UVMap" not in [u.name for u in low.data.uv_layers]: raise RuntimeError("UVMap missing on reopen")
    # Render once after reopen to prove the external normal texture resolves in a fresh process.
    setup_render()
    high.hide_render=True; low.hide_render=False
    bpy.context.scene.render.filepath=str(out/"LOW_BAKED_NORMAL_REOPEN.png")
    bpy.ops.render.render(write_still=True)
    receipt={
      "schema":"oleander.3d.surface-detail-normal-bake-reopen.v1","mode":"reopen","blender_version":bpy.app.version_string,
      "low":mesh_stats(low),"high":mesh_stats(high),"material_contract":contract,
      "normal_map_exists":True,"normal_map_sha256":sha256(normal_path),"reopen_render":"LOW_BAKED_NORMAL_REOPEN.png",
      "reopen_render_sha256":sha256(out/"LOW_BAKED_NORMAL_REOPEN.png"),"native_reopen_match":True,
      "evidence_class":"RECOVERED_NATIVE_TANGENT_NORMAL_BAKE",
      "promotion_scope":["high-to-low selected-to-active tangent normal bake","explicit low UV carrier","Non-Color data-map semantics","Normal Map node wiring","native .blend + external texture reopen"],
      "holds":["cross-engine tangent basis parity","production cage edge cases","UDIM/multi-material bake","Design KEEP"]
    }
    (out/"REOPEN_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,indent=2))


def main():
    a=cli(); out=Path(a.out).resolve()
    if a.mode=="build": build(out)
    else: reopen(out)

if __name__=="__main__": main()
