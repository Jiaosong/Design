#!/usr/bin/env python3
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector

MATERIALS = ('CONTROL_CONSTANT','ROUGHNESS_NONCOLOR','ROUGHNESS_SRGB_WRONG')
RIGS = ('BROAD','STRIP','GRAZING')


def cli():
    argv=sys.argv
    argv=argv[argv.index('--')+1:] if '--' in argv else []
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);return p.parse_args(argv)

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''):h.update(c)
    return h.hexdigest()

def aim(obj, target=(0,0,0)):
    d=Vector(target)-obj.location
    obj.rotation_euler=d.to_track_quat('-Z','Y').to_euler()

def clear_lights():
    for o in list(bpy.data.objects):
        if o.type=='LIGHT': bpy.data.objects.remove(o,do_unlink=True)

def add_area(name, location, energy, size, size_y=None, target=(0,0,0)):
    data=bpy.data.lights.new(name=name,type='AREA');data.energy=energy;data.shape='RECTANGLE'
    data.size=size;data.size_y=size if size_y is None else size_y
    obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj);obj.location=location;aim(obj,target);return obj

def set_rig(name):
    clear_lights()
    if name=='BROAD':
        add_area('RIG_BROAD',(-1.2,-2.2,3.8),620,4.8,4.8,(0,0,.15))
    elif name=='STRIP':
        add_area('RIG_STRIP',(2.7,-2.0,2.7),520,.28,3.4,(0,0,.15))
    elif name=='GRAZING':
        add_area('RIG_GRAZING',(3.8,-.25,.58),760,.18,3.0,(0,0,.12))
    else: raise ValueError(name)

def make_coupon():
    bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
    o=bpy.context.object;o.name='DIAGNOSTIC_ROUNDED_COUPON';o.scale=(1.35,.88,.24)
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    bevel=o.modifiers.new('BEVEL','BEVEL');bevel.width=.18;bevel.segments=6
    bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=bevel.name)
    for p in o.data.polygons:p.use_smooth=True
    bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.03)
    bpy.ops.object.mode_set(mode='OBJECT')
    if o.data.uv_layers: o.data.uv_layers.active.name='UVMap'
    return o

def write_roughness_png(out):
    w=h=128
    img=bpy.data.images.new('ROUGHNESS_SOURCE_WRITE',w,h,alpha=False,float_buffer=False)
    img.colorspace_settings.name='Non-Color'
    px=[]
    for y in range(h):
        v=y/(h-1)
        for x in range(w):
            u=x/(w-1)
            val=.23 + .42*(.5+.5*math.sin(2*math.pi*(4*u+.55*v)))
            val += .06*(.5+.5*math.sin(2*math.pi*(17*u-3*v)))
            val=max(.12,min(.78,val));px.extend((val,val,val,1.0))
    img.pixels=px
    p=out/'ROUGHNESS_DATA_SOURCE.png';img.filepath_raw=str(p);img.file_format='PNG';img.save()
    return p

def principled_base(name):
    m=bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;bs=nt.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(.34,.39,.43,1);bs.inputs['Metallic'].default_value=0.0;bs.inputs['Roughness'].default_value=.42
    if 'IOR' in bs.inputs: bs.inputs['IOR'].default_value=1.48
    return m,nt,bs

def mapped_material(name, png, colorspace):
    m,nt,bs=principled_base(name)
    im=bpy.data.images.load(str(png),check_existing=False);im.name=f'{name}_ROUGHNESS_IMAGE';im.colorspace_settings.name=colorspace
    tx=nt.nodes.new('ShaderNodeTexImage');tx.name='ROUGHNESS_IMAGE_TEXTURE';tx.image=im;tx.interpolation='Linear';tx.extension='REPEAT'
    uv=nt.nodes.new('ShaderNodeUVMap');uv.uv_map='UVMap';uv.name='UV_SOURCE'
    mapping=nt.nodes.new('ShaderNodeMapping');mapping.name='ROUGHNESS_MAPPING';mapping.inputs['Scale'].default_value=(2.6,2.1,1.0)
    nt.links.new(uv.outputs['UV'],mapping.inputs['Vector']);nt.links.new(mapping.outputs['Vector'],tx.inputs['Vector']);nt.links.new(tx.outputs['Color'],bs.inputs['Roughness'])
    return m

def make_materials(png):
    control,_,_=principled_base('CONTROL_CONSTANT')
    return {
        'CONTROL_CONSTANT':control,
        'ROUGHNESS_NONCOLOR':mapped_material('ROUGHNESS_NONCOLOR',png,'Non-Color'),
        'ROUGHNESS_SRGB_WRONG':mapped_material('ROUGHNESS_SRGB_WRONG',png,'sRGB'),
    }

def material_contract(m):
    nt=m.node_tree;bs=nt.nodes.get('Principled BSDF');rough_links=[l for l in nt.links if l.to_node==bs and l.to_socket==bs.inputs['Roughness']]
    tx=nt.nodes.get('ROUGHNESS_IMAGE_TEXTURE')
    return {
        'material':m.name,
        'principled_roughness_default':float(bs.inputs['Roughness'].default_value),
        'roughness_linked':bool(rough_links),
        'roughness_source_node':rough_links[0].from_node.name if rough_links else None,
        'image_name':tx.image.name if tx and tx.image else None,
        'image_colorspace':tx.image.colorspace_settings.name if tx and tx.image else None,
        'image_filepath':Path(bpy.path.abspath(tx.image.filepath)).name if tx and tx.image else None,
        'node_types':[n.bl_idname for n in nt.nodes],
    }

def render_metrics(scene, out_png):
    scene.render.filepath=str(out_png);bpy.ops.render.render(write_still=True)
    # In Blender 5.2 background mode the in-memory Render Result alpha can be
    # zero even when the written RGBA PNG has the correct object alpha. Use
    # the delivered PNG alpha as the visibility carrier, but retain linear/HDR
    # Render Result RGB for lighting/material metrics and >1 clipping checks.
    written=bpy.data.images.load(str(out_png),check_existing=False)
    ww,wh=written.size
    wa=np.array(written.pixels[:],dtype=np.float32).reshape(wh,ww,4)
    mask=wa[:,:,3]>.5
    object_pixels=int(mask.sum())
    bpy.data.images.remove(written)
    if object_pixels<1000: raise RuntimeError(f'visible object pixels too low in written PNG: {object_pixels}')
    rr=bpy.data.images.get('Render Result');w,h=rr.size
    if (w,h)!=(ww,wh): raise RuntimeError(f'render-result/write size mismatch: {(w,h)} vs {(ww,wh)}')
    a=np.array(rr.pixels[:],dtype=np.float32).reshape(h,w,4);rgb=a[:,:,:3]
    lum=.2126*rgb[:,:,0]+.7152*rgb[:,:,1]+.0722*rgb[:,:,2];vals=lum[mask]
    pairx=mask[:,1:]&mask[:,:-1];pairy=mask[1:,:]&mask[:-1,:]
    gx=np.abs(lum[:,1:]-lum[:,:-1])[pairx];gy=np.abs(lum[1:,:]-lum[:-1,:])[pairy]
    grad=float(np.mean(np.concatenate((gx,gy)))) if gx.size+gy.size else 0.0
    return {
        'object_pixels':object_pixels,
        'visibility_mask_source':'written PNG alpha',
        'lighting_metric_source':'Render Result linear/HDR RGB',
        'mean_luma':float(vals.mean()),
        'std_luma':float(vals.std()),
        'p95_luma':float(np.quantile(vals,.95)),
        'p99_luma':float(np.quantile(vals,.99)),
        'highlight_fraction_gt_0_65':float(np.mean(vals>.65)),
        'over_1_fraction':float(np.mean(np.max(rgb,axis=2)[mask]>1.0)),
        'mean_neighbor_gradient':grad,
    }

def metric_distance(a,b):
    keys=('mean_luma','std_luma','p95_luma','highlight_fraction_gt_0_65','mean_neighbor_gradient')
    return float(sum(abs(a[k]-b[k]) for k in keys))

def setup_scene(out):
    bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=False
    scene.render.resolution_x=256;scene.render.resolution_y=256;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.image_settings.color_depth='8';scene.render.film_transparent=True
    scene.render.filepath=str(out/'_tmp.png');scene.render.use_file_extension=True
    world=bpy.data.worlds.new('WORLD_DIAGNOSTIC');world.use_nodes=True;scene.world=world
    bg=world.node_tree.nodes.get('Background')
    if bg:
        bg.inputs['Color'].default_value=(.02,.02,.02,1.0);bg.inputs['Strength'].default_value=.08
    scene.view_settings.exposure=0.0
    obj=make_coupon()
    bpy.ops.object.camera_add(location=(0,-5.2,2.75));cam=bpy.context.object;cam.name='CAM_DIAGNOSTIC';cam.data.lens=72;aim(cam,(0,0,.08));scene.camera=cam
    return scene,obj

def main():
    args=cli();out=Path(args.out).resolve();renders=out/'renders';renders.mkdir(parents=True,exist_ok=True)
    scene,obj=setup_scene(out);png=write_roughness_png(out);tex_sha=sha256(png);materials=make_materials(png)
    for m in materials.values(): m.diffuse_color=(.34,.39,.43,1)
    results={}
    for mat_name in MATERIALS:
        obj.data.materials.clear();obj.data.materials.append(materials[mat_name])
        for rig in RIGS:
            set_rig(rig);bpy.context.view_layer.update();name=f'{mat_name}__{rig}';p=renders/f'{name}.png';results[name]=render_metrics(scene,p)
    controls={r:results[f'CONTROL_CONSTANT__{r}'] for r in RIGS}
    rig_dist={f'{a}__{b}':metric_distance(controls[a],controls[b]) for i,a in enumerate(RIGS) for b in RIGS[i+1:]}
    cs_effect={r:metric_distance(results[f'ROUGHNESS_NONCOLOR__{r}'],results[f'ROUGHNESS_SRGB_WRONG__{r}']) for r in RIGS}
    max_clip=max(v['over_1_fraction'] for v in results.values())
    contracts={k:material_contract(v) for k,v in materials.items()}
    evidence={
        'schema':'oleander.3d.material-nodes-lighting-diagnostic.v1',
        'blender_version':bpy.app.version_string,
        'engine':'CYCLES CPU',
        'render_settings':{'resolution':[256,256],'samples':16,'film_transparent':True,'exposure':float(scene.view_settings.exposure),'view_transform':scene.view_settings.view_transform,'look':scene.view_settings.look},
        'geometry':{'carrier':'procedural rounded coupon','object':obj.name,'uv_layer':obj.data.uv_layers.active.name if obj.data.uv_layers.active else None,'vertices':len(obj.data.vertices),'polygons':len(obj.data.polygons)},
        'metric_carrier':{'visibility':'written PNG alpha','lighting_material':'Render Result linear/HDR RGB','reason':'Blender 5.2 background-mode Render Result alpha diverged from delivered PNG alpha in failed run 33320024059; no rig/material/Gate threshold changed'},
        'roughness_texture':{'file':png.name,'sha256':tex_sha,'bytes':png.stat().st_size,'shared_same_bytes':True,'intent':'scalar roughness DATA map; same PNG is interpreted once as Non-Color and once intentionally wrong as sRGB'},
        'materials':contracts,
        'rigs':{'BROAD':'large frontal area; whole-surface response','STRIP':'narrow oblique strip; highlight width/continuity','GRAZING':'low-angle strip; roughness/noise sensitivity'},
        'renders':results,
        'control_rig_signature_distance':rig_dist,
        'roughness_colorspace_effect_distance':cs_effect,
        'max_control_rig_distance':max(rig_dist.values()),
        'max_colorspace_effect_distance':max(cs_effect.values()),
        'max_over_1_fraction':max_clip,
        'contract':{
            'same_texture_source_for_noncolor_and_srgb':contracts['ROUGHNESS_NONCOLOR']['image_filepath']==contracts['ROUGHNESS_SRGB_WRONG']['image_filepath']==png.name,
            'noncolor_label':contracts['ROUGHNESS_NONCOLOR']['image_colorspace'],
            'srgb_label':contracts['ROUGHNESS_SRGB_WRONG']['image_colorspace'],
            'all_nine_renders_present':all((renders/f'{m}__{r}.png').stat().st_size>0 for m in MATERIALS for r in RIGS),
            'rigs_discriminative':max(rig_dist.values())>.05,
            'colorspace_interpretation_discriminative':max(cs_effect.values())>.03,
            'clipping_bounded':max_clip<.08,
        },
        'promotion_scope':['same roughness texture bytes produce different shading when interpreted as scalar Non-Color data versus sRGB color data in this Blender/Cycles node carrier','Broad/Strip/Grazing rigs produce measurably distinct diagnostic signatures on one locked material/geometry carrier','material-node and image-color-space settings are evidence-bearing production state rather than UI decoration'],
        'holds':['XJ01 historical authority byte identity','physical PP/roughness measurement','texture-source photography/scan truth','normal/displacement map semantics','spectral/material metrology','hero-lighting quality','Design KEEP']
    }
    evidence['overall_pass']=all(evidence['contract'].values())
    blend=out/'MATERIAL_NODES_LIGHTING_DIAGNOSTIC.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));evidence['native_master']=blend.name;evidence['native_master_bytes']=blend.stat().st_size;evidence['native_master_sha256']=sha256(blend)
    (out/'RECEIPT.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8');print(json.dumps(evidence,indent=2))
    if not evidence['overall_pass']: raise SystemExit(6)

if __name__=='__main__':main()
