#!/usr/bin/env python3
"""OLEANDER Automotive Reference Vehicle v0.3 selective revision.
Loads the verified v0.2 working source, replaces upper-body/window logic and wheel faces,
then rerenders F1 views. Designer benchmark only; not engineering CAD.
"""
from __future__ import annotations
import bpy,bmesh,math,json,sys,argparse
from pathlib import Path
from mathutils import Vector

MODEL='OLEANDER_Automotive_Reference_Vehicle_v0.3'
FX=1.36; RX=-1.36; WY=.79; WZ=.345

def args():
    av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--samples',type=int,default=8);p.add_argument('--resolution',type=int,default=720);return p.parse_args(av)

def M(n): return bpy.data.materials[n]

def delete_prefix(*prefixes):
    for o in list(bpy.data.objects):
        if any(o.name.startswith(p) for p in prefixes): bpy.data.objects.remove(o,do_unlink=True)

def cube(name,loc,dims,mat,bev=.02,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=loc,rotation=rot);o=bpy.context.object;o.name=name;o.dimensions=dims;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bev: md=o.modifiers.new('BEVEL','BEVEL');md.width=bev;md.segments=4
    o.data.materials.append(mat);return o

def curve(name,pts,mat,depth=.005):
    cu=bpy.data.curves.new(name+'_C','CURVE');cu.dimensions='3D';cu.bevel_depth=depth;cu.bevel_resolution=3;sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
    for bp,co in zip(sp.bezier_points,pts):bp.co=co;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(o);o.data.materials.append(mat);return o

def section(hw,b,t,n=26,power=3.0):
    c=(b+t)/2;h=(t-b)/2;out=[]
    for i in range(n):
        a=2*math.pi*i/n;co=math.cos(a);si=math.sin(a);out.append((hw*math.copysign(abs(co)**(2/power),co),c+h*math.copysign(abs(si)**(2/power),si)))
    return out

def loft(name,stations,mat,n=26):
    vv=[];ff=[];rings=[]
    for x,hw,b,t in stations:
        r=[]
        for y,z in section(hw,b,t,n):r.append(len(vv));vv.append((x,y,z))
        rings.append(r)
    for a,b in zip(rings[:-1],rings[1:]):
        for j in range(n):k=(j+1)%n;ff.append((a[j],a[k],b[k],b[j]))
    ff += [tuple(reversed(rings[0])),tuple(rings[-1])]
    me=bpy.data.meshes.new(name+'_M');me.from_pydata(vv,[],ff);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat)
    for p in me.polygons:p.use_smooth=True
    md=o.modifiers.new('SUBSURF','SUBSURF');md.levels=1;md.render_levels=1;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=md.name);return o

def panel(name,verts,mat,thick=.006,bev=.008):
    me=bpy.data.meshes.new(name+'_M');me.from_pydata(verts,[],[tuple(range(len(verts)))]);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat)
    s=o.modifiers.new('SOLIDIFY','SOLIDIFY');s.thickness=thick
    b=o.modifiers.new('BEVEL','BEVEL');b.width=bev;b.segments=3;return o

def rebuild_cabin():
    delete_prefix('GREENHOUSE_GLASS','PANORAMIC_ROOF','A_PILLAR_','B_PILLAR_','C_PILLAR_','BELT_TRIM_')
    st=[(-1.28,.50,.88,.96),(-1.05,.65,.89,1.16),(-.76,.71,.90,1.32),(-.38,.735,.90,1.405),(0,.74,.90,1.43),(.38,.735,.90,1.405),(.70,.70,.90,1.31),(.96,.63,.89,1.14),(1.10,.48,.88,.96)]
    loft('CABIN_ROOF_SHELL',st,M('MAT_BODY_PAINT'))
    cube('PANORAMIC_ROOF',(-.04,0,1.414),(1.00,.84,.010),M('MAT_AUTOMOTIVE_GLASS'),.045)
    for y in (-.752,.752):
        tag='L' if y>0 else 'R'
        panel('FRONT_SIDE_GLASS_'+tag,[(.93,y,.91),(.69,y,1.30),(.16,y,1.39),(.14,y,.92)],M('MAT_AUTOMOTIVE_GLASS'))
        panel('REAR_SIDE_GLASS_'+tag,[(.12,y,.92),(.14,y,1.39),(-.58,y,1.36),(-.82,y,.92)],M('MAT_AUTOMOTIVE_GLASS'))
        panel('QUARTER_GLASS_'+tag,[(-.86,y,.92),(-.60,y,1.35),(-1.03,y,1.18),(-1.14,y,.91)],M('MAT_AUTOMOTIVE_GLASS'))
        curve('BELT_TRIM_'+tag,[(1.00,y,.91),(.35,y,.925),(-.45,y,.925),(-1.15,y,.91)],M('MAT_COATED_METAL_D2'),.007)
        curve('B_PILLAR_'+tag,[(.14,y,.92),(.15,y,1.39)],M('MAT_COATED_METAL_D2'),.018)
        curve('A_PILLAR_'+tag,[(1.04,y,.91),(.69,y,1.31)],M('MAT_BODY_PAINT'),.018)
        curve('C_PILLAR_'+tag,[(-.82,y,.92),(-1.08,y,1.16)],M('MAT_BODY_PAINT'),.022)
    panel('WINDSHIELD',[(1.06,-.58,.91),(1.06,.58,.91),(.69,.56,1.31),(.69,-.56,1.31)],M('MAT_AUTOMOTIVE_GLASS'),.008,.012)
    panel('REAR_GLASS',[(-1.05,-.58,.91),(-.78,-.55,1.29),(-.78,.55,1.29),(-1.05,.58,.91)],M('MAT_AUTOMOTIVE_GLASS'),.008,.012)

def rebuild_wheel_faces():
    for o in list(bpy.data.objects):
        if '_SPOKE_' in o.name or o.name.endswith('_HUB') or o.name.endswith('_RIM'): bpy.data.objects.remove(o,do_unlink=True)
    for x,fx in [(FX,'F'),(RX,'R')]:
        for y,sy in [(WY,'L'),(-WY,'R')]:
            name='WHEEL_'+fx+sy
            bpy.ops.mesh.primitive_torus_add(major_radius=.185,minor_radius=.020,major_segments=64,minor_segments=14,location=(x,y,WZ),rotation=(math.radians(90),0,0));r=bpy.context.object;r.name=name+'_RIM';r.data.materials.append(M('MAT_BRUSHED_ANODIZED_D2'))
            bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.038,depth=.065,location=(x,y,WZ),rotation=(math.radians(90),0,0));h=bpy.context.object;h.name=name+'_HUB';h.data.materials.append(M('MAT_BRUSHED_ANODIZED_D2'))
            for i in range(5):
                a=2*math.pi*i/5
                for j,da in enumerate((-.07,.07)):
                    aa=a+da;rr=.112;sx=x+rr*math.cos(aa);sz=WZ+rr*math.sin(aa)
                    cube(f'{name}_SPOKE_{i}_{j}',(sx,y,sz),(.145,.026,.014),M('MAT_BRUSHED_ANODIZED_D2'),.004,rot=(0,-aa,0))

def add_shoulder():
    delete_prefix('SHOULDER_')
    for y in (-.936,.936):curve('SHOULDER_L' if y>0 else 'SHOULDER_R',[(1.72,y,.77),(1.05,y,.84),(.20,y,.84),(-.70,y,.83),(-1.58,y,.77)],M('MAT_BODY_PAINT'),.004)

def camera(name,loc,tgt,lens=70,ortho=False,scale=6):
    d=bpy.data.cameras.new(name);d.lens=lens
    if ortho:d.type='ORTHO';d.ortho_scale=scale
    o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(tgt)-o.location).to_track_quat('-Z','Y').to_euler();return o

def setup(path,samples,res):
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=samples
    try:s.cycles.use_adaptive_sampling=True;s.render.use_persistent_data=True;bpy.context.view_layer.cycles.use_denoising=True
    except:pass
    s.render.resolution_x=res;s.render.resolution_y=res;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(path)
    try:s.view_settings.view_transform='Khronos PBR Neutral'
    except:pass

def rerender(out,samples,res):
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True)
    for p in rd.glob('*.png'):p.unlink()
    views=[('HERO_FRONT_3Q',(6,-6.8,2.7),(.08,0,.63),75,False,0),('REAR_3Q',(-5.6,6.2,2.55),(-.08,0,.61),75,False,0),('SIDE_PROFILE',(0,-8.3,1.42),(0,0,.63),85,True,5.20),('TOP_3Q',(4.4,-5,5.5),(0,0,.55),80,False,0),('FRONT_ORTHO',(7.2,0,1.20),(0,0,.64),85,True,2.55),('WHEEL_DETAIL',(2,-3,.92),(FX,-WY,.34),98,False,0),('CABIN_DETAIL',(1.9,-2.7,1.90),(.12,-.06,.83),90,False,0)]
    R=[]
    for lab,loc,tgt,lens,orth,sc in views:
        c=camera('CAM_'+lab,loc,tgt,lens,orth,sc);bpy.context.scene.camera=c;p=rd/f'{MODEL}__{lab}.png';setup(p,samples,res);bpy.ops.render.render(write_still=True);R.append({'view':lab,'file':str(p)});bpy.data.objects.remove(c,do_unlink=True)
    c=camera('CAM_CLAY',(6,-6.8,2.7),(.08,0,.63),75);bpy.context.scene.camera=c;bpy.context.view_layer.material_override=M('MAT_CLAY');p=rd/f'{MODEL}__CLAY_SURFACING.png';setup(p,samples,res);bpy.ops.render.render(write_still=True);bpy.context.view_layer.material_override=None;R.append({'view':'CLAY_SURFACING','file':str(p)});bpy.data.objects.remove(c,do_unlink=True);return R

def bbox(o):
    P=[o.matrix_world@Vector(c) for c in o.bound_box];return Vector((min(p.x for p in P),min(p.y for p in P),min(p.z for p in P))),Vector((max(p.x for p in P),max(p.y for p in P),max(p.z for p in P)))

def nonman(o):
    bm=bmesh.new();bm.from_mesh(o.data);n=sum(1 for e in bm.edges if not e.is_manifold);bm.free();return n

def qa(out,R):
    mn,mx=bbox(bpy.data.objects['BODY_SHELL']);bd=mx-mn;cmn,cmx=bbox(bpy.data.objects['CABIN_ROOF_SHELL']);ext=max(mx.z,cmx.z)
    P=[]
    for o in bpy.context.scene.objects:
        if o.type=='MESH' and o.name!='GROUND':P += [o.matrix_world@Vector(c) for c in o.bound_box]
    omy=max(p.y for p in P)-min(p.y for p in P)
    C={'body_length':4.30<=bd.x<=4.50,'body_width':1.80<=bd.y<=1.90,'overall_width':2.00<=omy<=2.14,'exterior_height':1.38<=ext<=1.48,'body_manifold':nonman(bpy.data.objects['BODY_SHELL'])==0,'cabin_manifold':nonman(bpy.data.objects['CABIN_ROOF_SHELL'])==0,'side_windows':len([o for o in bpy.data.objects if 'SIDE_GLASS' in o.name])==4,'wheels':len([o for o in bpy.data.objects if o.name.endswith('_TIRE')])==4,'renders':len(R)==8}
    q={'schema':'oleander.automotive.qa.v3','model':MODEL,'status':'PASS' if all(C.values()) else 'FAIL','body_dimensions_m':list(bd),'exterior_height_m':ext,'overall_width_m':omy,'checks':C,'renders':R,'reality_boundary':'Designer benchmark only; not engineering CAD/crash/aero/package/homologation/manufacturing validation.'};(out/'AUTOMOTIVE_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return q

def main():
    a=args();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);rebuild_cabin();rebuild_wheel_faces();add_shoulder();bpy.context.scene['OLEANDER_MODEL']=MODEL;bpy.ops.wm.save_as_mainfile(filepath=str(out/f'{MODEL}.blend'));R=rerender(out,a.samples,a.resolution);q=qa(out,R);rec={'schema':'oleander.automotive.receipt.v3','model':MODEL,'blender_version':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),'status':'EXECUTED_QA_PASS' if q['status']=='PASS' else 'EXECUTED_QA_FAIL','renders':R};(out/'AUTOMOTIVE_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if q['status']=='PASS' else 5)
if __name__=='__main__':main()
