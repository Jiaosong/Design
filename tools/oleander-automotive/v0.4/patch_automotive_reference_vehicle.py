#!/usr/bin/env python3
from __future__ import annotations
import bpy,bmesh,math,json,sys,argparse
from pathlib import Path
from mathutils import Vector
MODEL="OLEANDER_Automotive_Reference_Vehicle_v0.4"
FX=1.36; RX=-1.36; WY=.79; WZ=.345

def A():
    av=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    q=argparse.ArgumentParser();q.add_argument("--out",required=True);q.add_argument("--samples",type=int,default=8);q.add_argument("--resolution",type=int,default=720);return q.parse_args(av)
def M(n): return bpy.data.materials[n]
def delete(*prefix):
    for o in list(bpy.data.objects):
        if any(o.name.startswith(p) for p in prefix): bpy.data.objects.remove(o,do_unlink=True)
def cube(name,loc,dims,ma,bev=.02,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=loc,rotation=rot);o=bpy.context.object;o.name=name;o.dimensions=dims;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bev: b=o.modifiers.new("BEVEL","BEVEL");b.width=bev;b.segments=4
    o.data.materials.append(ma);return o
def curve(name,pts,ma,d=.005):
    cu=bpy.data.curves.new(name+"_C","CURVE");cu.dimensions="3D";cu.bevel_depth=d;cu.bevel_resolution=3
    sp=cu.splines.new("BEZIER");sp.bezier_points.add(len(pts)-1)
    for bp,co in zip(sp.bezier_points,pts):bp.co=co;bp.handle_left_type="AUTO";bp.handle_right_type="AUTO"
    o=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(o);o.data.materials.append(ma);return o
def sec(hw,b,t,n=30,p=4.5):
    c=(b+t)/2;h=(t-b)/2;r=[]
    for i in range(n):
        a=2*math.pi*i/n;co=math.cos(a);si=math.sin(a)
        r.append((hw*math.copysign(abs(co)**(2/p),co),c+h*math.copysign(abs(si)**(2/p),si)))
    return r
def loft(name,st,ma,n=30,p=4.5,sub=1):
    vv=[];ff=[];rings=[]
    for x,hw,b,t in st:
        rr=[]
        for y,z in sec(hw,b,t,n,p):rr.append(len(vv));vv.append((x,y,z))
        rings.append(rr)
    for a,b in zip(rings[:-1],rings[1:]):
        for j in range(n):k=(j+1)%n;ff.append((a[j],a[k],b[k],b[j]))
    ff += [tuple(reversed(rings[0])),tuple(rings[-1])]
    me=bpy.data.meshes.new(name+"_M");me.from_pydata(vv,[],ff);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(ma)
    for q in me.polygons:q.use_smooth=True
    if sub:
        md=o.modifiers.new("SUB","SUBSURF");md.levels=sub;md.render_levels=sub;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=md.name)
    return o
def arch(o,x):
    bpy.ops.mesh.primitive_cylinder_add(vertices=72,radius=.397,depth=2.35,location=(x,0,WZ),rotation=(math.radians(90),0,0));c=bpy.context.object
    md=o.modifiers.new("ARCH","BOOLEAN");md.operation="DIFFERENCE";md.solver="EXACT";md.object=c;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=md.name);bpy.data.objects.remove(c,do_unlink=True)
def panel(name,v,ma,th=.006,bev=.006):
    me=bpy.data.meshes.new(name+"_M");me.from_pydata(v,[],[tuple(range(len(v)))]);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(ma)
    s=o.modifiers.new("SOLID","SOLIDIFY");s.thickness=th
    b=o.modifiers.new("BEVEL","BEVEL");b.width=bev;b.segments=3;return o

def rebuild_body():
    delete("BODY_SHELL","CENTER_SILL","LOWER_SILL","FRONT_LOWER","REAR_LOWER","ARCH_","SHOULDER_","HOOD_","HATCH_")
    st=[
      (-2.23,.76,.26,.57),(-2.12,.86,.22,.64),(-1.92,.91,.19,.72),(-1.68,.925,.175,.79),
      (-1.42,.932,.17,.84),(-1.12,.935,.17,.88),(-.72,.938,.165,.90),(-.20,.94,.165,.91),
      (.35,.94,.165,.91),(.78,.938,.165,.90),(1.12,.934,.17,.88),(1.42,.928,.175,.84),
      (1.70,.92,.185,.79),(1.94,.90,.205,.72),(2.12,.86,.235,.65),(2.23,.76,.28,.58)]
    b=loft("BODY_SHELL",st,M("MAT_BODY_PAINT"),30,4.7,1);arch(b,FX);arch(b,RX)
    bev=b.modifiers.new("BODY_BEVEL","BEVEL");bev.width=.008;bev.segments=3
    cube("CENTER_SILL",(0,0,.265),(1.78,1.81,.16),M("MAT_PP_FINE_MATTE_D2"),.028)
    cube("FRONT_LOWER",(2.10,0,.405),(.18,1.16,.18),M("MAT_PP_FINE_MATTE_D2"),.028)
    cube("REAR_LOWER",(-2.10,0,.405),(.18,1.12,.18),M("MAT_PP_FINE_MATTE_D2"),.028)
    for y in (-.936,.936):
        curve("SHOULDER_L" if y>0 else "SHOULDER_R",[(1.72,y,.76),(1.10,y,.83),(.25,y,.85),(-.72,y,.83),(-1.62,y,.75)],M("MAT_BODY_PAINT"),.0035)
    for y in (-.47,.47):
        curve(f"HOOD_{y:+}",[(2.02,y,.69),(1.58,y,.80),(1.05,y,.88)],M("MAT_PP_FINE_MATTE_D2"),.0028)
        curve(f"HATCH_{y:+}",[(-1.08,y,.88),(-1.52,y,.80),(-1.97,y,.69)],M("MAT_PP_FINE_MATTE_D2"),.0028)

def rebuild_cabin():
    delete("GREENHOUSE_GLASS","CABIN_ROOF_SHELL","PANORAMIC_ROOF","WINDSHIELD","REAR_GLASS","FRONT_SIDE_GLASS_","REAR_SIDE_GLASS_","QUARTER_GLASS_","A_PILLAR_","B_PILLAR_","C_PILLAR_","BELT_TRIM_")
    st=[(-1.18,.52,1.16,1.22),(-.92,.66,1.28,1.35),(-.48,.72,1.35,1.42),(.02,.73,1.37,1.44),(.42,.71,1.34,1.41),(.76,.64,1.25,1.32),(.98,.50,1.13,1.19)]
    loft("ROOF_CANOPY",st,M("MAT_BODY_PAINT"),24,3.2,1)
    cube("PANORAMIC_ROOF",(-.05,0,1.414),(.86,.74,.008),M("MAT_AUTOMOTIVE_GLASS"),.018)
    for y in (-.755,.755):
        tag="L" if y>0 else "R"
        panel("FRONT_SIDE_GLASS_"+tag,[(.91,y,.91),(.67,y,1.28),(.12,y,1.35),(.10,y,.92)],M("MAT_AUTOMOTIVE_GLASS"))
        panel("REAR_SIDE_GLASS_"+tag,[(.07,y,.92),(.10,y,1.35),(-.63,y,1.31),(-.86,y,.92)],M("MAT_AUTOMOTIVE_GLASS"))
        panel("QUARTER_GLASS_"+tag,[(-.88,y,.92),(-.64,y,1.30),(-1.00,y,1.15),(-1.12,y,.91)],M("MAT_AUTOMOTIVE_GLASS"))
        curve("BELT_TRIM_"+tag,[(.98,y,.91),(.30,y,.925),(-.50,y,.925),(-1.16,y,.905)],M("MAT_COATED_METAL_D2"),.006)
        curve("A_PILLAR_"+tag,[(.99,y,.91),(.67,y,1.28)],M("MAT_BODY_PAINT"),.017)
        curve("B_PILLAR_"+tag,[(.10,y,.92),(.11,y,1.35)],M("MAT_COATED_METAL_D2"),.017)
        curve("C_PILLAR_"+tag,[(-.86,y,.92),(-1.02,y,1.15)],M("MAT_BODY_PAINT"),.021)
    panel("WINDSHIELD",[(1.00,-.58,.91),(1.00,.58,.91),(.67,.55,1.28),(.67,-.55,1.28)],M("MAT_AUTOMOTIVE_GLASS"),.008,.010)
    panel("REAR_GLASS",[(-1.05,-.56,.91),(-.72,-.53,1.27),(-.72,.53,1.27),(-1.05,.56,.91)],M("MAT_AUTOMOTIVE_GLASS"),.008,.010)

def rebuild_wheels():
    for o in list(bpy.data.objects):
        if "_SPOKE_" in o.name or o.name.endswith("_HUB") or o.name.endswith("_RIM") or "RIM_RING" in o.name:bpy.data.objects.remove(o,do_unlink=True)
    for x,fx in [(FX,"F"),(RX,"R")]:
        for y,sy in [(WY,"L"),(-WY,"R")]:
            name=f"WHEEL_{fx}{sy}"
            bpy.ops.mesh.primitive_torus_add(major_radius=.188,minor_radius=.018,major_segments=64,minor_segments=14,location=(x,y,WZ),rotation=(math.radians(90),0,0));r=bpy.context.object;r.name=name+"_RIM";r.data.materials.append(M("MAT_BRUSHED_ANODIZED_D2"))
            bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.035,depth=.060,location=(x,y,WZ),rotation=(math.radians(90),0,0));h=bpy.context.object;h.name=name+"_HUB";h.data.materials.append(M("MAT_BRUSHED_ANODIZED_D2"))
            for i in range(5):
                a=2*math.pi*i/5
                for j,da in enumerate((-.055,.055)):
                    aa=a+da;rr=.108;sx=x+rr*math.cos(aa);sz=WZ+rr*math.sin(aa)
                    cube(f"{name}_SPOKE_{i}_{j}",(sx,y,sz),(.135,.022,.012),M("MAT_BRUSHED_ANODIZED_D2"),.003,rot=(0,-aa,0))

def refine_details():
    delete("FRONT_LIGHT_GUIDE","REAR_LIGHT_GUIDE","FRONT_LIGHT_BAR","REAR_LIGHT_BAR","HEADLAMP_","TAILLAMP_","MIRROR_")
    for y in (-.47,.47):
        cube(f"HEADLAMP_{y:+}",(2.115,y,.665),(.035,.28,.035),M("MAT_LIGHT_WHITE"),.012)
        cube(f"TAILLAMP_{y:+}",(-2.115,y,.695),(.035,.27,.034),M("MAT_LIGHT_RED"),.012)
    cube("FRONT_LIGHT_BAR",(2.135,0,.665),(.022,.60,.012),M("MAT_LIGHT_WHITE"),.006)
    cube("REAR_LIGHT_BAR",(-2.135,0,.695),(.022,.66,.012),M("MAT_LIGHT_RED"),.006)
    for y in (-.985,.985):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,location=(.62,y,.98));o=bpy.context.object;o.name=f"MIRROR_{y:+}";o.scale=(.115,.045,.042);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(M("MAT_BODY_PAINT"))

def camera(name,loc,tgt,lens=70,ortho=False,scale=6):
    d=bpy.data.cameras.new(name);d.lens=lens
    if ortho:d.type="ORTHO";d.ortho_scale=scale
    o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(tgt)-o.location).to_track_quat("-Z","Y").to_euler();return o
def setup(p,samples,res):
    s=bpy.context.scene;s.render.engine="CYCLES";s.cycles.samples=samples
    try:s.cycles.use_adaptive_sampling=True;s.render.use_persistent_data=True;bpy.context.view_layer.cycles.use_denoising=True
    except:pass
    s.render.resolution_x=res;s.render.resolution_y=res;s.render.resolution_percentage=100;s.render.image_settings.file_format="PNG";s.render.image_settings.color_mode="RGB";s.render.filepath=str(p)
    try:s.view_settings.view_transform="Khronos PBR Neutral"
    except:pass
def render(out,samples,res):
    rd=out/"renders";rd.mkdir(parents=True,exist_ok=True)
    for p in rd.glob("*.png"):p.unlink()
    V=[("HERO_FRONT_3Q",(6.2,-7.2,2.65),(.05,0,.62),76,False,0),("REAR_3Q",(-5.8,6.4,2.55),(-.05,0,.60),76,False,0),("SIDE_PROFILE",(0,-8.4,1.38),(0,0,.61),85,True,5.25),("TOP_3Q",(4.5,-5.1,5.4),(0,0,.54),80,False,0),("FRONT_ORTHO",(7.3,0,1.16),(0,0,.62),85,True,2.55),("WHEEL_DETAIL",(2.0,-3,.90),(FX,-WY,.34),98,False,0),("CABIN_DETAIL",(1.8,-2.7,1.82),(.08,-.06,.82),90,False,0)]
    R=[]
    for lab,loc,tgt,lens,ortho,sc in V:
        c=camera("CAM_"+lab,loc,tgt,lens,ortho,sc);bpy.context.scene.camera=c;p=rd/f"{MODEL}__{lab}.png";setup(p,samples,res);bpy.ops.render.render(write_still=True);R.append({"view":lab,"file":str(p)});bpy.data.objects.remove(c,do_unlink=True)
    c=camera("CAM_CLAY",(6.2,-7.2,2.65),(.05,0,.62),76);bpy.context.scene.camera=c;bpy.context.view_layer.material_override=M("MAT_CLAY");p=rd/f"{MODEL}__CLAY_SURFACING.png";setup(p,samples,res);bpy.ops.render.render(write_still=True);bpy.context.view_layer.material_override=None;R.append({"view":"CLAY_SURFACING","file":str(p)});bpy.data.objects.remove(c,do_unlink=True);return R
def bbox(o):
    P=[o.matrix_world@Vector(c) for c in o.bound_box];return Vector((min(p.x for p in P),min(p.y for p in P),min(p.z for p in P))),Vector((max(p.x for p in P),max(p.y for p in P),max(p.z for p in P)))
def nonman(o):
    bm=bmesh.new();bm.from_mesh(o.data);n=sum(1 for e in bm.edges if not e.is_manifold);bm.free();return n
def qa(out,R):
    mn,mx=bbox(bpy.data.objects["BODY_SHELL"]);bd=mx-mn;rn,rx=bbox(bpy.data.objects["ROOF_CANOPY"]);ext=max(mx.z,rx.z)
    P=[]
    for o in bpy.context.scene.objects:
        if o.type=="MESH" and o.name!="GROUND":P += [o.matrix_world@Vector(c) for c in o.bound_box]
    ow=max(p.y for p in P)-min(p.y for p in P)
    C={"body_length":4.30<=bd.x<=4.50,"body_width":1.80<=bd.y<=1.90,"overall_width":1.98<=ow<=2.12,"exterior_height":1.38<=ext<=1.48,"body_manifold":nonman(bpy.data.objects["BODY_SHELL"])==0,"roof_manifold":nonman(bpy.data.objects["ROOF_CANOPY"])==0,"side_windows":len([o for o in bpy.data.objects if "SIDE_GLASS" in o.name])==4,"wheels":len([o for o in bpy.data.objects if o.name.endswith("_TIRE")])==4,"renders":len(R)==8}
    q={"schema":"oleander.automotive.qa.v4","model":MODEL,"status":"PASS" if all(C.values()) else "FAIL","body_dimensions_m":list(bd),"overall_width_m":ow,"exterior_height_m":ext,"checks":C,"renders":R,"reality_boundary":"Designer benchmark only; not engineering CAD/crash/aero/package/homologation/manufacturing validation."};(out/"AUTOMOTIVE_QA.json").write_text(json.dumps(q,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");return q
def main():
    a=A();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);rebuild_body();rebuild_cabin();rebuild_wheels();refine_details();bpy.context.scene["OLEANDER_MODEL"]=MODEL;bpy.ops.wm.save_as_mainfile(filepath=str(out/f"{MODEL}.blend"));R=render(out,a.samples,a.resolution);q=qa(out,R);rec={"schema":"oleander.automotive.receipt.v4","model":MODEL,"blender_version":bpy.app.version_string,"build_hash":bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),"status":"EXECUTED_QA_PASS" if q["status"]=="PASS" else "EXECUTED_QA_FAIL","renders":R};(out/"AUTOMOTIVE_RECEIPT.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if q["status"]=="PASS" else 5)
if __name__=="__main__":main()
