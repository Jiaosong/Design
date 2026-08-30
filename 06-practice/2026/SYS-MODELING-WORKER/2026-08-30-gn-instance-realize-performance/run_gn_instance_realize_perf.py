#!/usr/bin/env python3
import argparse,json,math,statistics,sys,time,hashlib
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
 bpy.ops.object.select_all(action='DESELECT');proxy.select_set(True);bpy.context.view_layer.objects.active=proxy;p=out/name;bpy.ops.export_scene.gltf(filepath=str(p),export_format='GLB',use_selection=True,export_materials='NONE');bpy.data.objects.remove(proxy,do_unlink=True);return {'file':p.name,'bytes':p.stat().st_size,'sha256':sha(p),'static_vertices':len(copy.vertices),'static_polygons':len(copy.polygons)}
def main():
 a=cli();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);reset();rows=[]
 for res in [25,50,100]:
  count=res*res
  for realize in [False,True]:
   label=f'{"REALIZE" if realize else "INSTANCE"}_{res}x{res}';o,_=make_obj(label,realize,res);bpy.context.view_layer.update();ev=median_eval(o);blend=file_size_for(o,out,f'{label}.blend');glb=export_static(o,out,f'{label}.glb');rows.append({'mode':'REALIZE' if realize else 'INSTANCE','resolution':res,'instance_count':count,'eval':ev,'blend':blend,'static_glb':glb});bpy.data.objects.remove(o,do_unlink=True)
 byres={}
 for res in [25,50,100]:
  i=next(r for r in rows if r['resolution']==res and r['mode']=='INSTANCE');r=next(x for x in rows if x['resolution']==res and x['mode']=='REALIZE')
  byres[str(res)]={'instance_count':res*res,'realize_over_instance_eval_ratio':r['eval']['median_seconds']/i['eval']['median_seconds'] if i['eval']['median_seconds'] else None,'realize_over_instance_evaluated_vertex_ratio':r['eval']['evaluated_vertices']/max(1,i['eval']['evaluated_vertices']),'blend_byte_ratio_realize_over_instance':r['blend']['bytes']/max(1,i['blend']['bytes']),'static_glb_byte_ratio_realize_over_instance':r['static_glb']['bytes']/max(1,i['static_glb']['bytes'])}
 rec={'schema':'oleander.3d.gn-instance-realize-performance.v1','blender_version':bpy.app.version_string,'measurement_scope':'same GitHub runner process; medians support relative sensitivity only, not portable absolute performance budgets','source_geometry':'0.04 m cube instances on 8x8 m grid points','resolutions':[25,50,100],'rows':rows,'ratios':byres,'finding_boundary':'preserved instances may keep procedural representation compact during DCC evaluation, while explicit static export baking can collapse both modes to similar realized geometry. Realize is justified by downstream operations/export needs, not as a default cleanup step.','evidence_class':'NATIVE_GN_PERFORMANCE_SENSITIVITY','holds':['GPU viewport/render timing','browser draw-call/GPU memory profile','production asset complexity','collection instances','LOD/HLOD','Design KEEP']}
 (out/'PERF_RECEIPT.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
if __name__=='__main__':main()
