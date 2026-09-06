#!/usr/bin/env python3
import argparse,json,math,sys,hashlib
from pathlib import Path
import bpy
from mathutils import Vector

HIGH='VD_HIGH'; LOW='VD_LOW_NORMAL'; DISP='VD_DISPLACED'; MAT_HIGH='VD_MAT_HIGH'; MAT_LOW='VD_MAT_LOW'; MAT_DISP='VD_MAT_DISP'; IMG='VD_NORMAL_TARGET'

def cli():
 a=sys.argv;a=a[a.index('--')+1:] if '--' in a else [];p=argparse.ArgumentParser();p.add_argument('--mode',choices=['build','reopen'],required=True);p.add_argument('--out',required=True);return p.parse_args(a)
def sha(p):
 h=hashlib.sha256();f=open(p,'rb')
 for c in iter(lambda:f.read(1<<20),b''):h.update(c)
 f.close();return h.hexdigest()
def macro(x,y):return 0.052*math.sin(1.2*x)*math.cos(1.05*y)+0.018*math.cos(0.7*x+0.5*y)
def meso(x,y):return 0.032*(0.72*math.sin(8.8*x)*math.cos(7.6*y)+0.28*math.sin(13.4*(x+y)))
def grid(name,n,size,with_meso=False,uv=False):
 vs=[];fs=[]
 for j in range(n):
  y=(j/(n-1)-.5)*size
  for i in range(n):
   x=(i/(n-1)-.5)*size;z=macro(x,y)+(meso(x,y) if with_meso else 0);vs.append((x,y,z))
 for j in range(n-1):
  for i in range(n-1):a=j*n+i;fs.append((a,a+1,a+n+1,a+n))
 me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(vs,[],fs);me.update()
 for p in me.polygons:p.use_smooth=True
 if uv:
  u=me.uv_layers.new(name='UVMap')
  for p in me.polygons:
   for li in p.loop_indices:
    vi=me.loops[li].vertex_index;i=vi%n;j=vi//n;u.data[li].uv=(i/(n-1),j/(n-1))
 o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);return o
def mat(name):
 m=bpy.data.materials.new(name);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(.46,.46,.46,1);b.inputs['Roughness'].default_value=.37;return m
def low_mat(img):
 m=mat(MAT_LOW);nt=m.node_tree;tx=nt.nodes.new('ShaderNodeTexImage');tx.name='NORMAL_TEX';tx.image=img;tx.select=True;nt.nodes.active=tx;nm=nt.nodes.new('ShaderNodeNormalMap');nm.name='NORMAL_MAP';nm.space='TANGENT';nt.links.new(nm.outputs['Normal'],nt.nodes.get('Principled BSDF').inputs['Normal']);return m
def bake(high,low,m,out):
 sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.render.bake.use_selected_to_active=True;sc.render.bake.cage_extrusion=.07;sc.render.bake.margin=12;sc.render.bake.normal_space='TANGENT'
 bpy.ops.object.select_all(action='DESELECT');high.select_set(True);low.select_set(True);bpy.context.view_layer.objects.active=low;bpy.ops.object.bake(type='NORMAL')
 im=bpy.data.images[IMG];p=out/'VIEW_DISTANCE_TANGENT_NORMAL.png';im.filepath_raw=str(p);im.file_format='PNG';im.save();ext=bpy.data.images.load(str(p),check_existing=False);ext.name='VD_EXTERNAL_NORMAL';ext.colorspace_settings.name='Non-Color';tx=m.node_tree.nodes['NORMAL_TEX'];tx.image=ext;nm=m.node_tree.nodes['NORMAL_MAP'];m.node_tree.links.new(tx.outputs['Color'],nm.inputs['Color']);return p
def look(o,t=(0,0,0)):o.rotation_euler=(Vector(t)-o.location).to_track_quat('-Z','Y').to_euler()
def setup():
 sc=bpy.context.scene;sc.render.engine='BLENDER_EEVEE';sc.render.resolution_x=720;sc.render.resolution_y=720;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=True
 if sc.world is None:sc.world=bpy.data.worlds.new('WORLD')
 sc.world.color=(.02,.02,.02)
 for name,loc,energy,size in [('KEY',(1.8,-2.0,3.5),950,2.0),('FILL',(-2.5,1.4,2.2),220,3.0)]:
  ld=bpy.data.lights.new(name,'AREA');ld.energy=energy;ld.size=size;o=bpy.data.objects.new(name,ld);bpy.context.collection.objects.link(o);o.location=loc;look(o)
 cd=bpy.data.cameras.new('CAM');cam=bpy.data.objects.new('CAM',cd);bpy.context.collection.objects.link(cam);sc.camera=cam;return cam
def render_variant(sc,cam,objs,active,view,out):
 for o in objs:o.hide_render=o is not active
 if view=='TOP_FAR':cam.location=(0.15,-0.10,5.2);cam.data.lens=68;look(cam,(0,0,0))
 else:cam.location=(2.75,-3.15,.42);cam.data.lens=58;look(cam,(0,0,0.02))
 p=out/f'{view}_{active.name}.png';sc.render.filepath=str(p);bpy.ops.render.render(write_still=True);return p
def load(path):
 im=bpy.data.images.load(str(path),check_existing=False);return im.size[:],list(im.pixels[:])
def cmp(a,b):
 (wa,ha),x=load(a);(wb,hb),y=load(b);assert(wa,ha)==(wb,hb);inter=union=0;err=0.;n=0
 for i in range(0,len(x),4):
  A=x[i+3]>.5;B=y[i+3]>.5
  if A or B:union+=1
  if A and B:
   inter+=1;err+=abs(x[i]-y[i])+abs(x[i+1]-y[i+1])+abs(x[i+2]-y[i+2]);n+=3
 return {'silhouette_iou':inter/union if union else 1.,'intersection_rgb_mae':err/n if n else 0.,'intersection_pixels':inter,'union_pixels':union}
def contract(m):
 tx=m.node_tree.nodes.get('NORMAL_TEX');nm=m.node_tree.nodes.get('NORMAL_MAP');im=tx.image if tx else None
 return {'image_source':getattr(im,'source',None),'colorspace':im.colorspace_settings.name if im else None,'normal_space':getattr(nm,'space',None),'image_path':bpy.path.abspath(im.filepath) if im else None}
def build(out):
 bpy.ops.wm.read_factory_settings(use_empty=True);out.mkdir(parents=True,exist_ok=True);size=2.4
 high=grid(HIGH,97,size,True,False);low=grid(LOW,25,size,False,True);disp=grid(DISP,49,size,True,False)
 mh=mat(MAT_HIGH);md=mat(MAT_DISP);high.data.materials.append(mh);disp.data.materials.append(md);im=bpy.data.images.new(IMG,width=1024,height=1024,alpha=False);im.generated_color=(.5,.5,1,1);im.colorspace_settings.name='Non-Color';ml=low_mat(im);low.data.materials.append(ml);normal_path=bake(high,low,ml,out)
 sc=bpy.context.scene;cam=setup();objs=[high,low,disp];renders={}
 for view in ['TOP_FAR','GRAZE_CLOSE']:
  for o in objs:renders[(view,o.name)]=render_variant(sc,cam,objs,o,view,out)
 metrics={}
 for view in ['TOP_FAR','GRAZE_CLOSE']:
  metrics[view]={'normal':cmp(renders[(view,HIGH)],renders[(view,LOW)]),'displacement':cmp(renders[(view,HIGH)],renders[(view,DISP)])}
 # This is a view-dependent representation witness. At grazing close range, real geometric displacement should preserve silhouette better than a normal-only carrier.
 if metrics['GRAZE_CLOSE']['displacement']['silhouette_iou'] <= metrics['GRAZE_CLOSE']['normal']['silhouette_iou'] + 0.002:
  raise RuntimeError(f'grazing view did not discriminate geometry vs normal: {metrics["GRAZE_CLOSE"]}')
 # In top/far view the normal carrier should retain high overlap and useful shading correspondence despite lower geometry density.
 if metrics['TOP_FAR']['normal']['silhouette_iou'] < .985 or metrics['TOP_FAR']['normal']['intersection_rgb_mae'] > .04:
  raise RuntimeError(f'far-view normal carrier outside bounded usefulness: {metrics["TOP_FAR"]["normal"]}')
 ml.node_tree.nodes['NORMAL_MAP'].inputs['Strength'].default_value=1.;blend=out/'NORMAL_VS_DISPLACEMENT.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend))
 rec={'schema':'oleander.3d.normal-vs-displacement-distance.v1','blender_version':bpy.app.version_string,'representation':{'high':'macro+meso geometry 97x97','normal':'macro geometry 25x25 + tangent normal','displacement':'macro+meso geometry 49x49'},'polygons':{HIGH:len(high.data.polygons),LOW:len(low.data.polygons),DISP:len(disp.data.polygons)},'normal_texture':normal_path.name,'normal_texture_sha256':sha(normal_path),'material_contract':contract(ml),'metrics':metrics,'grazing_silhouette_advantage':metrics['GRAZE_CLOSE']['displacement']['silhouette_iou']-metrics['GRAZE_CLOSE']['normal']['silhouette_iou'],'evidence_class':'NATIVE_VIEW_DEPENDENT_REPRESENTATION_PENDING_REOPEN','rule':'normal is acceptable only when required evidence is shading-direction rather than true silhouette/parallax/section; displacement/geometry is required when those geometric cues enter the view','holds':['true shader displacement subdivision','parallax occlusion mapping','cross-engine parity','performance budget','production texture filtering','Design KEEP']}
 (out/'BUILD_RECEIPT.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
def reopen(out):
 low=bpy.data.objects.get(LOW);m=bpy.data.materials.get(MAT_LOW);p=out/'VIEW_DISTANCE_TANGENT_NORMAL.png'
 if not low or not m or not p.exists():raise RuntimeError('reopen dependency missing')
 c=contract(m)
 if c['image_source']!='FILE' or c['colorspace']!='Non-Color' or c['normal_space']!='TANGENT':raise RuntimeError(c)
 rec={'schema':'oleander.3d.normal-vs-displacement-distance-reopen.v1','native_reopen_match':True,'material_contract':c,'normal_texture_sha256':sha(p),'evidence_class':'RECOVERED_NATIVE_VIEW_DEPENDENT_REPRESENTATION'};(out/'REOPEN_RECEIPT.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
def main():
 a=cli();out=Path(a.out).resolve();build(out) if a.mode=='build' else reopen(out)
if __name__=='__main__':main()
