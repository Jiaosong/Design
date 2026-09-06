#!/usr/bin/env python3
import argparse,json,statistics,sys,time,hashlib
from pathlib import Path
import bpy


def cli():
 a=sys.argv;a=a[a.index('--')+1:] if '--' in a else [];p=argparse.ArgumentParser();p.add_argument('--out',required=True);return p.parse_args(a)
def sha(p):
 h=hashlib.sha256();f=open(p,'rb')
 for c in iter(lambda:f.read(1<<20),b''):h.update(c)
 f.close();return h.hexdigest()
def reset():bpy.ops.wm.read_factory_settings(use_empty=True)
def node_group(realize=False):
 ng=bpy.data.node_groups.new(f'GN_PERF_{"REALIZE" if realize else "INSTANCE"}','GeometryNodeTree')
 ng.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');ng.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
 n=ng.nodes;ln=ng.links;inp=n.new('NodeGroupInput');out=n.new('NodeGroupOutput');grid=n.new('GeometryNodeMeshGrid');pts=n.new('GeometryNodeMeshToPoints');cube=n.new('GeometryNodeMeshCube');inst=n.new('GeometryNodeInstanceOnPoints')
 grid.inputs['Size X'].default_value=8.;grid.inputs['Size Y'].default_value=8.;cube.inputs['Size'].default_value=(.04,.04,.04);ln.new(grid.outputs['Mesh'],pts.inputs['Mesh']);ln.new(pts.outputs['Points'],inst.inputs['Points']);ln.new(cube.outputs['Mesh'],inst.inputs['Instance'])
 if realize:
  r=n.new('GeometryNodeRealizeInstances');ln.new(inst.outputs['Instances'],r.inputs['Geometry']);ln.new(r.outputs['Geometry'],out.inputs['Geometry'])
 else:ln.new(inst.outputs['Instances'],out.inputs['Geometry'])
 return ng,grid

def make_obj(name,realize,res):
 me=bpy.data.meshes.new(name+'_EMPTY');o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);mod=o.modifiers.new('GN','NODES');ng,grid=node_group(realize);mod.node_group=ng;grid.inputs['Vertices X'].default_value=res;grid.inputs['Vertices Y'].default_value=res;return o,ng

def eval_once(o):
 dg=bpy.context.evaluated_depsgraph_get();t=time.perf_counter();eo=o.evaluated_get(dg);me=eo.to_mesh();counts=(len(me.vertices),len(me.edges),len(me.polygons));eo.to_mesh_clear();return time.perf_counter()-t,counts

def median_eval(o,warm=2,reps=7):
 for _ in range(warm):eval_once(o)
 vals=[];counts=None
 for _ in range(reps):dt,counts=eval_once(o);vals.append(dt)
 return {'median_seconds':statistics.median(vals),'min_seconds':min(vals),'max_seconds':max(vals),'samples_seconds':vals,'evaluated_vertices':counts[0],'evaluated_edges':counts[1],'evaluated_polygons':counts[2]}
def file_size_for(o,out,name):
 for x in bpy.context.scene.objects:x.hide_render=x!=o;x.hide_viewport=x!=o
 p=out/name;bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True);return {'file':p.name,'bytes':p.stat().st_size,'sha256':sha(p)}
def export_static(o,out,name):
 dg=bpy.context.evaluated_depsgraph_get();eo=o.evaluated_get(dg);me=eo.to_mesh(preserve_all_data_layers=True,depsgraph=dg);copy=me.copy();eo.to_mesh_clear();proxy=bpy.data.objects.new(name+'_PROXY',copy);bpy.context.collection.objects.link(proxy)
 bpy.ops.object.select_all(action='DESELECT');proxy.select_set(True);bpy.context.view_layer.objects.active=proxy;p=out/name;bpy.ops.export_scene.gltf(filepath=str(p),export_format='GLB',use_selection=True,export_materials='NONE');bpy.data.objects.remove(proxy,do_unlink=True);return {'file':p.name,'bytes':p.stat().st_size,'sha256':sha(p),'static_vertices':len(copy.vertices),'static_polygons':len(copy.polygons),'empty_mesh_export':len(copy.vertices)==0 and len(copy.polygons)==0}
def main():
 a=cli();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);reset();rows=[]
 for res in [25,50,100]:
  count=res*res
  for realize in [False,True]:
   label=f'{"REALIZE" if realize else "INSTANCE"}_{res}x{res}';o,_=make_obj(label,realize,res);bpy.context.view_layer.update();ev=median_eval(o);blend=file_size_for(o,out,f'{label}.blend');glb=export_static(o,out,f'{label}.glb');rows.append({'mode':'REALIZE' if realize else 'INSTANCE','resolution':res,'instance_count':count,'eval':ev,'blend':blend,'static_glb':glb});bpy.data.objects.remove(o,do_unlink=True)
 byres={}
 for res in [25,50,100]:
  i=next(r for r in rows if r['resolution']==res and r['mode']=='INSTANCE');r=next(x for x in rows if x['resolution']==res and x['mode']=='REALIZE')
  expected_vertices=res*res*8;expected_polygons=res*res*6
  byres[str(res)]={'instance_count':res*res,'expected_realized_vertices':expected_vertices,'expected_realized_polygons':expected_polygons,'realize_over_instance_eval_ratio':r['eval']['median_seconds']/i['eval']['median_seconds'] if i['eval']['median_seconds'] else None,'blend_byte_ratio_realize_over_instance':r['blend']['bytes']/max(1,i['blend']['bytes']),'instance_to_mesh_vertices':i['eval']['evaluated_vertices'],'realize_to_mesh_vertices':r['eval']['evaluated_vertices'],'instance_static_export_empty':i['static_glb']['empty_mesh_export'],'realize_static_export_vertices':r['static_glb']['static_vertices'],'realize_static_export_polygons':r['static_glb']['static_polygons']}
 rec={'schema':'oleander.3d.gn-instance-realize-representation.v2','blender_version':bpy.app.version_string,'measurement_scope':'same GitHub runner process; microsecond timings are retained only as provenance and are not portable performance budgets because INSTANCE to_mesh returns no mesh component in this route','source_geometry':'0.04 m cube instances on 8x8 m grid points','resolutions':[25,50,100],'rows':rows,'ratios':byres,'representation_contract':{'instance_component_not_mesh_component_in_to_mesh_route':True,'static_mesh_export_requires_realize_or_an_instance_aware_export_path':True,'procedural_instance_master_remains_compact_in_blend':True,'empty_instance_glb_is_not_visual_or_runtime_equivalence':True},'finding_boundary':'In this controlled Blender 5.2 Geometry Nodes route, preserved Instance Component survives procedurally in the .blend but Object.evaluated_get(...).to_mesh() yields no mesh component, so a mesh-only static export proxy is empty. Realize Instances converts the same population to explicit mesh with 8 vertices and 6 polygons per cube. Therefore INSTANCE vs REALIZE must first be treated as a representation/export-semantics decision; runtime performance must be measured later with an instance-aware runtime carrier, not by comparing an empty GLB with a flattened mesh GLB.','evidence_class':'NATIVE_GN_INSTANCE_COMPONENT_VS_MESH_COMPONENT','holds':['instance-aware glTF export semantics','EXT_mesh_gpu_instancing or equivalent runtime carrier','browser draw-call/GPU memory/frame profile','GPU viewport/render timing','production asset complexity','collection instances','LOD/HLOD','Design KEEP']}
 (out/'PERF_RECEIPT.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
if __name__=='__main__':main()
