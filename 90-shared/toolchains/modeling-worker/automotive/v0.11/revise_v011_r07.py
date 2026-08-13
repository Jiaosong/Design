#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R07 — Real-Proportion Section Baseline

M1-M5 only.
Reference corridor is calibrated from current production sedan/fastback dimensions,
but geometry remains generic and unbranded.

Editable authority = continuous open quad Primary Source Grid.
Wheel package = guide geometry only at M5.
Front/rear caps = derived diagnostic termination only.
No boolean wheel openings; no M7/M8 details.
"""
from __future__ import annotations
import importlib.util, bpy, json, math
from pathlib import Path
from mathutils import Vector

BASE="/tmp/build_automotive_v011_r05.py"
spec=importlib.util.spec_from_file_location("r05",BASE)
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)

MODEL="OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R07"
b.MODEL=MODEL

b.HP.update({
    "length_m":4.65,"wheelbase_m":2.82,"body_width_m":1.86,"track_m":1.59,
    "wheel_outer_diameter_m":.70,"height_target_m":1.45,"front_axle_x_m":1.465,
    "rear_axle_x_m":-1.355,"wheel_center_z_m":.35,"cowl_x_m":.93,"cowl_z_m":.89,
    "roof_peak_x_m":-.12,"roof_peak_z_m":1.45,"belt_z_nominal_m":.86,
})
b.FX=1.465; b.RX=-1.355; b.WY=.795; b.WZ=.35

b.SECTIONS=[
 ( 2.325,.51,.24,.52,.31,.46,.40,.34,.45,.23,.36,.15,.30),
 ( 2.22 ,.56,.34,.56,.42,.50,.51,.37,.57,.22,.46,.15,.37),
 ( 2.02 ,.64,.50,.63,.57,.56,.67,.40,.73,.205,.60,.145,.48),
 ( 1.72 ,.72,.62,.70,.68,.63,.81,.43,.87,.19,.76,.14,.61),
 ( 1.465,.77,.66,.75,.74,.67,.90,.45,.92,.18,.83,.14,.67),
 ( 1.20 ,.80,.67,.78,.77,.69,.92,.46,.93,.18,.85,.14,.69),
 ( 1.00 ,.84,.67,.82,.78,.71,.92,.47,.93,.18,.86,.14,.70),
 ( .93  ,.89,.65,.85,.79,.73,.92,.48,.93,.18,.86,.14,.70),
 ( .73  ,1.08,.55,.86,.80,.74,.915,.48,.925,.18,.86,.14,.70),
 ( .48  ,1.29,.52,.86,.81,.75,.91,.48,.92,.18,.86,.14,.70),
 ( .18  ,1.42,.55,.86,.81,.755,.91,.48,.92,.18,.86,.14,.70),
 (-.12  ,1.45,.56,.86,.81,.755,.91,.48,.92,.18,.86,.14,.70),
 (-.45  ,1.43,.55,.855,.81,.75,.91,.48,.92,.18,.86,.14,.70),
 (-.75  ,1.37,.52,.85,.80,.745,.91,.48,.92,.18,.86,.14,.70),
 (-1.00  ,1.27,.48,.84,.79,.73,.905,.47,.915,.18,.85,.14,.69),
 (-1.20  ,1.12,.50,.825,.78,.71,.90,.46,.91,.18,.84,.14,.68),
 (-1.355 ,.99,.58,.81,.77,.69,.90,.45,.91,.18,.83,.14,.67),
 (-1.62  ,.87,.63,.79,.75,.67,.88,.44,.90,.19,.80,.145,.64),
 (-1.88  ,.79,.60,.75,.70,.63,.83,.42,.86,.20,.73,.15,.58),
 (-2.10  ,.69,.49,.66,.59,.57,.70,.39,.75,.215,.60,.155,.47),
 (-2.25  ,.61,.37,.59,.46,.52,.55,.36,.61,.23,.49,.16,.39),
 (-2.325 ,.55,.27,.55,.35,.48,.45,.34,.50,.24,.40,.16,.32)
]

def linear_resample(points,steps=4):
    out=[]
    for i in range(len(points)-1):
        p1,p2=points[i],points[i+1]
        for j in range(steps):
            t=j/steps
            out.append(tuple(p1[d]+(p2[d]-p1[d])*t for d in range(3)))
    out.append(points[-1]);return out
b.resample_list=linear_resample

def full_source_grid(rows,M):
    nX=len(rows[0]);verts=[];ids=[]
    for xi in range(nX):
        right=[rows[i][xi] for i in range(7,0,-1)];center=[rows[0][xi]]
        left=[(p[0],-p[1],p[2]) for p in [rows[i][xi] for i in range(1,8)]]
        cross=right+center+left;row=[]
        for p in cross:row.append(len(verts));verts.append(p)
        ids.append(row)
    faces=[]
    for i in range(nX-1):
        for j in range(len(ids[0])-1):faces.append((ids[i][j],ids[i+1][j],ids[i+1][j+1],ids[i][j+1]))
    me=bpy.data.meshes.new("PRIMARY_SOURCE_GRID_MESH");me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new("PRIMARY_SOURCE_GRID",me);bpy.context.collection.objects.link(o);o.data.materials.append(M["CLAY"])
    for p in me.polygons:p.use_smooth=True
    return o,ids,verts

def cap(name,cross,ma,reverse=False):
    verts=list(cross);face=tuple(reversed(range(len(verts)))) if reverse else tuple(range(len(verts)))
    me=bpy.data.meshes.new(name+"_MESH");me.from_pydata(verts,[],[face]);me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(ma);return o

def guide_mat(M):return b.mat("MAT_PACKAGE_GUIDE",(0.04,.16,.65,1),.30,0,((.03,.18,1,1),1.0))

def wheel_package(M):
    gm=guide_mat(M)
    for x,px in ((b.FX,"F"),(b.RX,"R")):
        for y,py in ((b.WY,"L"),(-b.WY,"R")):
            bpy.ops.mesh.primitive_torus_add(major_radius=.273,minor_radius=.077,major_segments=64,minor_segments=18,location=(x,y,b.WZ),rotation=(math.radians(90),0,0))
            t=bpy.context.object;t.name=f"PACKAGE_WHEEL_{px}{py}";t.scale.y=1.52
            bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);t.data.materials.append(gm)

def render_r07(out,samples,res,M,L,G,source,caps):
    rd=out/"renders";rd.mkdir(parents=True,exist_ok=True);R=[]
    V=[
      ("PACKAGE_SIDE",(0,-8.8,1.14),(0,0,.64),85,True,5.25,"BROAD","normal"),
      ("TOP_ORTHO",(0,0,8),(0,0,.56),85,True,5.35,"BROAD","normal"),
      ("FRONT_ORTHO",(7.7,0,1.13),(0,0,.65),85,True,2.65,"BROAD","normal"),
      ("CLAY_BROAD",(6.2,-7.0,2.75),(.05,0,.66),78,False,5,"BROAD","normal"),
      ("CLAY_STRIP",(6.2,-7.0,2.75),(.05,0,.66),78,False,5,"STRIP","normal"),
      ("CLAY_GRAZING",(6.2,-7.0,2.75),(.05,0,.66),78,False,5,"GRAZING","normal"),
      ("SECTION_OVERLAY",(5.8,-6.4,3.0),(0,0,.70),80,False,5,"BROAD","guide"),
      ("CONTROL_CURVES",(5.8,-6.4,3.0),(0,0,.70),80,False,5,"BROAD","guide")]
    for lab,loc,t,lens,ortho,scale,rig,mode in V:
        b.setrig(L,rig)
        for o in G:o.hide_render=(mode!="guide")
        source.hide_render=False
        for c in caps:c.hide_render=False
        b.world((.012,.012,.012),.16)
        c=b.camera("CAM_"+lab,loc,t,lens,ortho,scale);bpy.context.scene.camera=c
        p=rd/f"{MODEL}__{lab}.png";b.setup(p,samples,res);bpy.ops.render.render(write_still=True)
        R.append({"view":lab,"file":str(p),"mode":mode});bpy.data.objects.remove(c,do_unlink=True)
    return R

def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials()
    rows=b.controls_resampled();source,ids,verts=full_source_grid(rows,M)
    front=[verts[k] for k in ids[-1]];rear=[verts[k] for k in ids[0]]
    caps=[cap("FRONT_TERMINATION_DIAG",front,M["CLAY"],False),cap("REAR_TERMINATION_DIAG",rear,M["CLAY"],True)]
    G=b.guides(rows,M);wheel_package(M);b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16)
    scene=bpy.context.scene;scene["OLEANDER_MODEL"]=MODEL;scene["OLEANDER_STAGE"]="M5";scene["OLEANDER_HARD_POINTS"]=json.dumps(b.HP);scene["OLEANDER_REFERENCE_CORRIDOR"]="generic production sedan/fastback; no brand geometry copied"
    b.write_contract(out)
    cp=out/"MODELING_CONTRACT.json";c=json.loads(cp.read_text())
    c["job_id"]="SYS-MODELING-WORKER-AUTO-M1M5-v0.11-R07"
    c["decision_question"]="Can a production-calibrated 4.65 m / 2.82 m package and 22-section continuous source grid establish a credible generic sedan/fastback primary proportion before wheel arches, glazing, lamps, or other secondary geometry?"
    c["source_authority"]["editable_source"]=f"{MODEL}.blend";c["source_authority"]["derived_models"]=["FRONT_TERMINATION_DIAG","REAR_TERMINATION_DIAG","PACKAGE_WHEEL_*"]
    c["sections"]["items"]=[{"id":f"SEC-{i:02d}","role":"transverse control station","station":s[0],"plane":"YZ","continuity_target":"controlled longitudinal progression","depends_on":["HP-WHEELBASE","HP-TRACK"],"status":"OPEN"} for i,s in enumerate(b.SECTIONS)]
    c["primary_geometry"][0]["source_sections"]=[f"SEC-{i:02d}" for i in range(len(b.SECTIONS))]
    c["semantic_components"][1]["parameters"]={"section_count":len(b.SECTIONS),"resample_mode":"piecewise-linear / tangent-preserving","wheel_arch_state":"M7_BLOCKED"}
    c["qa"]["construction"]=["single continuous open quad source grid","22 explicit transverse stations","no global SubD inflation","no destructive wheel-arch boolean at M5","front/rear caps are diagnostic only"]
    c["qa"]["design_geometry"]=["package side proportion","top body/cabin taper","front tumblehome","hood-cowl-A-roof-backlight trajectory","belt/shoulder/rocker hierarchy","Broad/Strip/Grazing surface flow"]
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n")
    blend=out/f"{MODEL}.blend";bpy.ops.wm.save_as_mainfile(filepath=str(blend));R=render_r07(out,a.samples,a.resolution,M,L,G,source,caps)
    mn,mx=b.bbox(source);tri=quad=ngon=0
    for p in source.data.polygons:
        n=len(p.vertices)
        if n==4:quad+=1
        elif n==3:tri+=1
        else:ngon+=1
    premature=[o.name for o in bpy.context.scene.objects if any(k in o.name for k in ["HANDLE","LAMP","MIRROR","SEAT","SCREEN","WIPER","CALIPER","SPOKE"])]
    checks={"length":4.60<=mx.x-mn.x<=4.70,"width":1.80<=mx.y-mn.y<=1.92,"height":1.42<=mx.z<=1.47,"wheelbase":abs(b.FX-b.RX-2.82)<1e-8,"track":abs(2*b.WY-1.59)<1e-8,"section_count":len(b.SECTIONS)==22,"source_quad_only":tri==0 and ngon==0,"no_destructive_wheel_boolean":not any(o.name=="BODY_DIAGNOSTIC_DERIVED" for o in bpy.context.scene.objects),"diagnostic_caps":len(caps)==2,"premature_detail_absent":not premature,"render_matrix":len(R)==8}
    q={"schema":"oleander.auto.v0.11.r07.qa","model":MODEL,"status":"MACHINE_PASS_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL","bounds":{"min":list(mn),"max":list(mx),"dimensions":[mx.x-mn.x,mx.y-mn.y,mx.z-mn.z]},"source_face_counts":{"quad":quad,"tri":tri,"ngon":ngon},"checks":checks,"renders":R,"boundary":"M5 source is the continuous open quad grid. Wheel package and end caps are diagnostic only. No wheel arch, glazing, lamp, panel or detail authority exists yet."}
    (out/"AUTOMOTIVE_V011_QA.json").write_text(json.dumps(q,ensure_ascii=False,indent=2)+"\n")
    rec={"schema":"oleander.auto.v0.11.r07.receipt","model":MODEL,"blender_version":bpy.app.version_string,"build_hash":bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),"renderer":"Cycles CPU","samples":a.samples,"resolution":[a.resolution,a.resolution],"status":"EXECUTED_"+q["status"],"blend":str(blend),"qa":str(out/"AUTOMOTIVE_V011_QA.json"),"renders":R}
    (out/"AUTOMOTIVE_V011_RECEIPT.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n");print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if all(checks.values()) else 5)

if __name__=="__main__":main()
