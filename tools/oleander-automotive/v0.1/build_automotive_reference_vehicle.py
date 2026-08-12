#!/usr/bin/env python3
"""OLEANDER Automotive Reference Vehicle v0.1
Generic unbranded fastback/crossover benchmark for comprehensive Blender modeling QA.

Designer benchmark only. Not engineering CAD / homologation / production geometry.
Target: Blender 5.2 LTS / Cycles CPU.
"""
from __future__ import annotations
import argparse, json, math, sys, traceback
from pathlib import Path
import bpy
from mathutils import Vector

MODEL = "OLEANDER_Automotive_Reference_Vehicle_v0.1"
DIMS = {
    "length_m": 4.42,
    "width_m": 1.86,
    "height_m": 1.48,
    "wheelbase_m": 2.72,
    "track_m": 1.58,
    "wheel_radius_m": 0.345,
    "tire_width_m": 0.235,
    "ground_clearance_target_m": 0.165,
}
FRONT_X = DIMS["wheelbase_m"]/2
REAR_X = -DIMS["wheelbase_m"]/2
WHEEL_Y = DIMS["track_m"]/2

def args():
    av=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    p=argparse.ArgumentParser();p.add_argument("--out",required=True);p.add_argument("--samples",type=int,default=8);p.add_argument("--resolution",type=int,default=720);return p.parse_args(av)

def set_input(node,names,value):
    if isinstance(names,str): names=[names]
    for n in names:
        s=node.inputs.get(n)
        if s is not None:s.default_value=value;return s
    return None

def clear():
    bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)

def material(name,base,rough=.4,metallic=0.0,coat=0.0,coat_rough=.1,transmission=0.0,ior=1.5,emission=None):
    m=bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;nt.nodes.clear();out=nt.nodes.new("ShaderNodeOutputMaterial");bs=nt.nodes.new("ShaderNodeBsdfPrincipled")
    set_input(bs,"Base Color",base);set_input(bs,"Roughness",rough);set_input(bs,"Metallic",metallic);set_input(bs,["Coat Weight","Clearcoat"],coat);set_input(bs,["Coat Roughness","Clearcoat Roughness"],coat_rough);set_input(bs,["Transmission Weight","Transmission"],transmission);set_input(bs,"IOR",ior)
    if emission:set_input(bs,["Emission Color","Emission"],emission[0]);set_input(bs,"Emission Strength",emission[1])
    nt.links.new(bs.outputs["BSDF"],out.inputs["Surface"]);return m

def make_materials():
    return {
      "BODY":material("MAT_BODY_PAINT",(0.16,0.22,0.19,1),.22,0.0,.85,.07),
      "LOWER_PP":material("MAT_PP_FINE_MATTE_D2",(0.025,0.03,0.03,1),.52,0.0),
      "PU":material("MAT_PU_SOFT_MATTE_D2",(0.018,0.022,0.023,1),.66,0.0),
      "COATED":material("MAT_COATED_METAL_D2",(0.05,0.055,0.055,1),.46,0.0),
      "AL":material("MAT_BRUSHED_ANODIZED_D2",(0.32,0.34,0.35,1),.28,1.0),
      "GLASS":material("MAT_AUTOMOTIVE_GLASS",(0.015,0.025,0.03,1),.08,0.0,0,0,0.25,1.45),
      "TIRE":material("MAT_TIRE",(0.012,0.014,0.014,1),.72,0.0),
      "DISC":material("MAT_BRAKE_DISC",(0.16,0.17,0.17,1),.33,1.0),
      "CALIPER":material("MAT_CALIPER",(0.35,0.055,0.02,1),.34,0.0,.25,.12),
      "LIGHT_WHITE":material("MAT_LIGHT_WHITE",(0.7,0.75,0.72,1),.20,0.0,0,0,.08,1.46,((1,0.96,0.84,1),5.0)),
      "LIGHT_RED":material("MAT_LIGHT_RED",(0.35,0.012,0.008,1),.22,0.0,0,0,.05,1.46,((1,0.015,0.008,1),4.0)),
      "INTERIOR":material("MAT_INTERIOR",(0.035,0.04,0.04,1),.58,0.0),
      "SCREEN":material("MAT_SCREEN",(0.015,0.02,0.025,1),.18,0.0,0,0,0,1.5,((0.10,0.36,0.55,1),1.5)),
      "CLAY":material("MAT_CLAY",(0.32,0.32,0.30,1),.52,0.0)
    }

def superellipse_loop(halfwidth,bottom,top,n=28,power=3.2):
    c=(top+bottom)/2;h=(top-bottom)/2;pts=[]
    for i in range(n):
        t=2*math.pi*i/n;cy=math.cos(t);sz=math.sin(t);y=halfwidth*math.copysign(abs(cy)**(2/power),cy);z=c+h*math.copysign(abs(sz)**(2/power),sz);pts.append((y,z))
    return pts

def loft_closed(name,stations,mat,loop_n=28,power=3.2,subsurf=1):
    verts=[];faces=[];loops=[]
    for x,hw,bottom,top in stations:
        loop=[]
        for y,z in superellipse_loop(hw,bottom,top,loop_n,power):loop.append(len(verts));verts.append((x,y,z))
        loops.append(loop)
    for a,b in zip(loops[:-1],loops[1:]):
        for j in range(loop_n):k=(j+1)%loop_n;faces.append((a[j],a[k],b[k],b[j]))
    faces.append(tuple(reversed(loops[0])));faces.append(tuple(loops[-1]));me=bpy.data.meshes.new(name+"_MESH");me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    if subsurf:
        mod=o.modifiers.new("SUBSURF","SUBSURF");mod.levels=subsurf;mod.render_levels=subsurf;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
    return o

def boolean_wheel_arch(body,x,z=.345,r=.405):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=2.3,location=(x,0,z),rotation=(math.radians(90),0,0));c=bpy.context.object
    mod=body.modifiers.new("ARCH_BOOL","BOOLEAN");mod.operation="DIFFERENCE";mod.solver="EXACT";mod.object=c;bpy.context.view_layer.objects.active=body;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(c,do_unlink=True)

def bevel_obj(o,width=.01,segments=4):m=o.modifiers.new("BEVEL","BEVEL");m.width=width;m.segments=segments;return m

def cube(name,loc,dims,mat,bevel=.02,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=loc,rotation=rot);o=bpy.context.object;o.name=name;o.dimensions=dims;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:bevel_obj(o,bevel,4)
    o.data.materials.append(mat);return o

def uv_sphere(name,loc,scale,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for p in o.data.polygons:p.use_smooth=True
    o.data.materials.append(mat);return o

def curve_line(name,pts,mat,bevel=.006):
    cu=bpy.data.curves.new(name+"_CURVE","CURVE");cu.dimensions="3D";cu.bevel_depth=bevel;cu.bevel_resolution=3;sp=cu.splines.new("BEZIER");sp.bezier_points.add(len(pts)-1)
    for bp,co in zip(sp.bezier_points,pts):bp.co=co;bp.handle_left_type="AUTO";bp.handle_right_type="AUTO"
    o=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(o);o.data.materials.append(mat);return o

def create_body(mats):
    stations=[(-2.21,.58,.24,.62),(-2.08,.78,.20,.70),(-1.90,.88,.18,.78),(-1.65,.92,.17,.84),(-1.40,.93,.17,.88),(-1.15,.935,.17,.90),(-.75,.94,.165,.90),(-.25,.945,.165,.89),(.25,.945,.165,.89),(.75,.94,.165,.90),(1.10,.935,.17,.91),(1.40,.93,.17,.86),(1.68,.91,.18,.80),(1.92,.86,.20,.74),(2.10,.74,.23,.66),(2.21,.55,.28,.58)]
    body=loft_closed("BODY_SHELL",stations,mats["BODY"],28,3.5,1);boolean_wheel_arch(body,REAR_X);boolean_wheel_arch(body,FRONT_X);bevel_obj(body,.012,3)
    cube("LOWER_SILL",(0,0,.29),(3.10,1.84,.20),mats["LOWER_PP"],.035);cube("FRONT_LOWER",(2.07,0,.38),(.18,1.38,.25),mats["LOWER_PP"],.045);cube("REAR_LOWER",(-2.07,0,.38),(.18,1.34,.25),mats["LOWER_PP"],.045)

def create_greenhouse(mats):
    stations=[(-1.38,.60,.86,.96),(-1.18,.73,.87,1.22),(-.88,.79,.88,1.40),(-.45,.81,.89,1.47),(0,.815,.90,1.49),(.42,.805,.90,1.47),(.78,.78,.89,1.38),(1.05,.70,.88,1.15),(1.18,.58,.88,.96)]
    loft_closed("GREENHOUSE_GLASS",stations,mats["GLASS"],24,3.0,1);cube("PANORAMIC_ROOF",(-.05,0,1.476),(1.30,1.08,.022),mats["GLASS"],.06)
    for y in (-.825,.825):
        curve_line(f"A_PILLAR_{y:+}",[(1.00,y,.92),(.72,y,1.36)],mats["BODY"],.020);curve_line(f"B_PILLAR_{y:+}",[(.22,y,.90),(.18,y,1.45)],mats["BODY"],.020);curve_line(f"C_PILLAR_{y:+}",[(-.78,y,.90),(-1.08,y,1.25)],mats["BODY"],.024)

def wheel(name,x,y,mats):
    bpy.ops.mesh.primitive_torus_add(major_radius=.270,minor_radius=.075,major_segments=64,minor_segments=20,location=(x,y,.345),rotation=(math.radians(90),0,0));t=bpy.context.object;t.name=name+"_TIRE";t.scale.y=1.55;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);t.data.materials.append(mats["TIRE"])
    bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.225,depth=.17,location=(x,y,.345),rotation=(math.radians(90),0,0));rim=bpy.context.object;rim.name=name+"_RIM";rim.data.materials.append(mats["AL"]);bevel_obj(rim,.012,3)
    bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.165,depth=.175,location=(x,y,.345),rotation=(math.radians(90),0,0));disc=bpy.context.object;disc.name=name+"_DISC";disc.data.materials.append(mats["DISC"])
    for i in range(10):
        ang=2*math.pi*i/10;rr=.112;sx=x+rr*math.cos(ang);sz=.345+rr*math.sin(ang);cube(name+f"_SPOKE_{i:02d}",(sx,y,sz),(.17,.19,.025),mats["AL"],.008,rot=(0,-ang,0))
    cy=y+(.095 if y>0 else -.095);cube(name+"_CALIPER",(x+.11,cy,.345),(.065,.035,.12),mats["CALIPER"],.01)

def create_wheels(mats):
    for x,p in [(FRONT_X,"F"),(REAR_X,"R")]:
        for y,s in [(WHEEL_Y,"L"),(-WHEEL_Y,"R")]:
            wheel(f"WHEEL_{p}{s}",x,y,mats);bpy.ops.mesh.primitive_torus_add(major_radius=.387,minor_radius=.018,major_segments=64,minor_segments=10,location=(x,.932 if y>0 else -.932,.345),rotation=(math.radians(90),0,0));bpy.context.object.data.materials.append(mats["LOWER_PP"])

def create_details(mats):
    for y in (-.56,.56):cube(f"HEADLAMP_{y:+}",(2.045,y,.68),(.11,.36,.10),mats["LIGHT_WHITE"],.035);cube(f"TAILLAMP_{y:+}",(-2.04,y,.71),(.10,.37,.09),mats["LIGHT_RED"],.030)
    cube("FRONT_LIGHT_GUIDE",(2.09,0,.68),(.055,.72,.035),mats["LIGHT_WHITE"],.017);cube("REAR_LIGHT_GUIDE",(-2.09,0,.72),(.055,.80,.035),mats["LIGHT_RED"],.017);cube("FRONT_INTAKE",(2.135,0,.43),(.045,.98,.19),mats["LOWER_PP"],.025)
    for y in (-.98,.98):uv_sphere(f"MIRROR_{y:+}",(.70,y,1.02),(.15,.075,.065),mats["BODY"]);cube(f"MIRROR_STEM_{y:+}",(.68,y*.95,.98),(.10,.04,.05),mats["LOWER_PP"],.018)
    for y in (-.944,.944):
        for x in (.45,-.65):cube(f"HANDLE_{x:+}_{y:+}",(x,y,.76),(.18,.018,.035),mats["AL"],.01)
        curve_line(f"SEAM_FRONT_{y:+}",[(.35,y,.40),(.35,y,.88)],mats["LOWER_PP"],.004);curve_line(f"SEAM_REAR_{y:+}",[(-.72,y,.40),(-.72,y,.88)],mats["LOWER_PP"],.004);curve_line(f"BELT_TRIM_{y:+}",[(1.05,y,.89),(.4,y,.91),(-.4,y,.91),(-1.20,y,.89)],mats["COATED"],.008)
    curve_line("HOOD_SEAM_L",[(1.78,-.55,.77),(1.35,-.55,.87),(1.08,-.55,.90)],mats["LOWER_PP"],.004);curve_line("HOOD_SEAM_R",[(1.78,.55,.77),(1.35,.55,.87),(1.08,.55,.90)],mats["LOWER_PP"],.004)

def create_interior(mats):
    cube("CABIN_FLOOR",(-.05,0,.54),(2.20,1.42,.08),mats["INTERIOR"],.03);cube("DASHBOARD",(.72,0,.79),(.30,1.30,.18),mats["INTERIOR"],.05);cube("CENTER_SCREEN",(.62,-.02,.93),(.035,.52,.22),mats["SCREEN"],.025,rot=(0,math.radians(-8),0))
    for x in (.25,-.65):
        for y in (-.34,.34):cube(f"SEAT_BASE_{x}_{y}",(x,y,.62),(.52,.48,.13),mats["PU"],.06);cube(f"SEAT_BACK_{x}_{y}",(x-.10,y,.85),(.16,.46,.50),mats["PU"],.07,rot=(0,math.radians(-10),0))
    bpy.ops.mesh.primitive_torus_add(major_radius=.14,minor_radius=.018,major_segments=48,minor_segments=12,location=(.50,-.37,.90),rotation=(math.radians(90),0,0));bpy.context.object.data.materials.append(mats["PU"]);cube("STEERING_COLUMN",(.58,-.37,.87),(.17,.045,.045),mats["COATED"],.015)

def create_ground():cube("GROUND",(0,0,-.045),(12,8,.08),material("MAT_GROUND",(.035,.035,.033,1),.72),0)

def camera(name,loc,target,lens=70,ortho=False,scale=6):
    d=bpy.data.cameras.new(name);d.lens=lens
    if ortho:d.type="ORTHO";d.ortho_scale=scale
    o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler();return o

def add_area(name,loc,energy,size,target=(0,0,.65)):
    d=bpy.data.lights.new(name,"AREA");d.energy=energy;d.shape="DISK";d.size=size;o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler()

def studio():
    add_area("KEY",(-3,-4,4.5),1500,3);add_area("RIM",(3.5,2.2,3),1100,2);add_area("FILL",(-1.5,3.5,2.3),600,2.5);w=bpy.context.scene.world;w.use_nodes=True;bg=w.node_tree.nodes.get("Background");bg.inputs["Color"].default_value=(.015,.015,.014,1);bg.inputs["Strength"].default_value=.18

def setup_render(path,samples,res):
    s=bpy.context.scene;s.render.engine="CYCLES";s.cycles.samples=samples
    try:s.cycles.use_adaptive_sampling=True
    except:pass
    try:s.render.use_persistent_data=True
    except:pass
    s.render.resolution_x=res;s.render.resolution_y=res;s.render.resolution_percentage=100;s.render.image_settings.file_format="PNG";s.render.image_settings.color_mode="RGB";s.render.filepath=str(path)
    try:s.view_settings.view_transform="Khronos PBR Neutral"
    except:pass
    try:bpy.context.view_layer.cycles.use_denoising=True
    except:pass

def render_views(outdir,samples,res,mats):
    rd=outdir/"renders";rd.mkdir(parents=True,exist_ok=True);views=[("HERO_FRONT_3Q",(6.4,-7.2,3.2),(.15,0,.65),72,False,0),("REAR_3Q",(-6,6.6,2.8),(-.15,0,.62),72,False,0),("SIDE_PROFILE",(0,-8.8,1.55),(0,0,.68),85,True,5.2),("TOP_3Q",(4.8,-5.5,6.3),(0,0,.55),76,False,0),("FRONT_ORTHO",(8,0,1.30),(0,0,.70),85,True,3.0),("WHEEL_DETAIL",(2.05,-3.4,1.05),(FRONT_X,-WHEEL_Y,.36),92,False,0),("CABIN_DETAIL",(2.3,-3.2,2.35),(.25,-.10,.86),85,False,0)];rec=[]
    for label,loc,tgt,lens,ortho,scale in views:
        cam=camera("CAM_"+label,loc,tgt,lens,ortho,scale);bpy.context.scene.camera=cam;p=rd/f"{MODEL}__{label}.png";setup_render(p,samples,res);bpy.ops.render.render(write_still=True);rec.append({"view":label,"file":str(p)});bpy.data.objects.remove(cam,do_unlink=True)
    cam=camera("CAM_CLAY",(6.4,-7.2,3.2),(.15,0,.65),72);bpy.context.scene.camera=cam;bpy.context.view_layer.material_override=mats["CLAY"];p=rd/f"{MODEL}__CLAY_SURFACING.png";setup_render(p,samples,res);bpy.ops.render.render(write_still=True);bpy.context.view_layer.material_override=None;rec.append({"view":"CLAY_SURFACING","file":str(p)});bpy.data.objects.remove(cam,do_unlink=True);return rec

def bounds_world():
    pts=[]
    for o in bpy.context.scene.objects:
        if o.type!="MESH" or o.name=="GROUND":continue
        for c in o.bound_box:pts.append(o.matrix_world@Vector(c))
    mn=Vector((min(p.x for p in pts),min(p.y for p in pts),min(p.z for p in pts)));mx=Vector((max(p.x for p in pts),max(p.y for p in pts),max(p.z for p in pts)));return mn,mx

def manifold(o):
    import bmesh;bm=bmesh.new();bm.from_mesh(o.data);n=sum(1 for e in bm.edges if not e.is_manifold);bm.free();return n

def qa(outdir,renders):
    mn,mx=bounds_world();dims=mx-mn;crit={n:manifold(bpy.data.objects[n]) for n in ["BODY_SHELL","GREENHOUSE_GLASS","CABIN_FLOOR","DASHBOARD"]}
    checks={"length_corridor":4.30<=dims.x<=4.55,"width_corridor":1.80<=dims.y<=2.05,"height_corridor":1.40<=dims.z<=1.58,"wheelbase":abs((FRONT_X-REAR_X)-2.72)<1e-6,"track":abs((2*WHEEL_Y)-1.58)<1e-6,"body_manifold":crit["BODY_SHELL"]==0,"greenhouse_manifold":crit["GREENHOUSE_GLASS"]==0,"render_count":len(renders)==8,"wheel_count":len([o for o in bpy.data.objects if o.name.endswith("_TIRE")])==4,"headlamp_count":len([o for o in bpy.data.objects if o.name.startswith("HEADLAMP_")])==2,"taillamp_count":len([o for o in bpy.data.objects if o.name.startswith("TAILLAMP_")])==2,"interior_seats":len([o for o in bpy.data.objects if o.name.startswith("SEAT_BASE")])==4}
    report={"schema":"oleander.automotive-reference-vehicle.qa.v1","model":MODEL,"status":"PASS" if all(checks.values()) else "FAIL","dimensions_m":{"x":dims.x,"y":dims.y,"z":dims.z,"min":list(mn),"max":list(mx)},"design_targets":DIMS,"checks":checks,"critical_manifold":crit,"object_count":len(bpy.context.scene.objects),"mesh_count":len([o for o in bpy.context.scene.objects if o.type=="MESH"]),"curve_count":len([o for o in bpy.context.scene.objects if o.type=="CURVE"]),"renders":renders,"reality_boundary":"Designer benchmark only; not engineering CAD, crash, aero, packaging, homologation or manufacturing validation."};(outdir/"AUTOMOTIVE_QA.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");return report

def main():
    a=args();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);clear();mats=make_materials();create_body(mats);create_greenhouse(mats);create_wheels(mats);create_details(mats);create_interior(mats);create_ground();studio();bpy.context.scene["OLEANDER_MODEL"]=MODEL;bpy.context.scene["OLEANDER_DESIGN_TARGETS"]=json.dumps(DIMS);blend=out/f"{MODEL}.blend";bpy.ops.wm.save_as_mainfile(filepath=str(blend));renders=render_views(out,a.samples,a.resolution,mats);q=qa(out,renders);receipt={"schema":"oleander.automotive-reference-vehicle.receipt.v1","model":MODEL,"blender_version":bpy.app.version_string,"build_hash":bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),"renderer":"Cycles","samples":a.samples,"resolution":[a.resolution,a.resolution],"status":"EXECUTED_QA_PASS" if q["status"]=="PASS" else "EXECUTED_QA_FAIL","blend":str(blend),"renders":renders,"qa":str(out/"AUTOMOTIVE_QA.json")};(out/"AUTOMOTIVE_RECEIPT.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(receipt,ensure_ascii=False,indent=2));raise SystemExit(0 if q["status"]=="PASS" else 5)
if __name__=="__main__":main()
