#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R08 — Locked R07 Source + Closed Derived Wheel-Arch Diagnostic.

R07 hard points and 22 section stations are LOCKED.
No design-coordinate change in this revision.
Purpose: remove package-guide visual contamination and judge the R07 source proportions
using a watertight derived diagnostic body with circular wheel openings.
"""
from __future__ import annotations
import importlib.util, bpy, bmesh, json, math, hashlib
from pathlib import Path
from mathutils import Vector

BASE="/tmp/revise_v011_r07.py"
spec=importlib.util.spec_from_file_location("r07",BASE)
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
b=r.b

MODEL="OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R08"
r.MODEL=MODEL;b.MODEL=MODEL

def source_hash(o):
    h=hashlib.sha256()
    for v in o.data.vertices:h.update(f"{v.co.x:.9f},{v.co.y:.9f},{v.co.z:.9f};".encode())
    for p in o.data.polygons:h.update((",".join(map(str,p.vertices[:]))+";").encode())
    return h.hexdigest()

def build_closed_derived(rows,M):
    nX=len(rows[0]);verts=[];ids=[]
    for xi in range(nX):
        right=[rows[i][xi] for i in range(7,0,-1)];center=[rows[0][xi]]
        left=[(p[0],-p[1],p[2]) for p in [rows[i][xi] for i in range(1,8)]]
        cross=right+center+left;row=[]
        for p in cross:row.append(len(verts));verts.append(p)
        ids.append(row)
    faces=[];nY=len(ids[0])
    for i in range(nX-1):
        for j in range(nY-1):faces.append((ids[i][j],ids[i+1][j],ids[i+1][j+1],ids[i][j+1]))
        faces.append((ids[i][-1],ids[i+1][-1],ids[i+1][0],ids[i][0]))
    for row,rev in ((ids[0],True),(ids[-1],False)):
        center=tuple(sum(verts[k][d] for k in row)/len(row) for d in range(3));ci=len(verts);verts.append(center)
        for j in range(len(row)):
            k=(j+1)%len(row);faces.append((ci,row[k],row[j]) if rev else (ci,row[j],row[k]))
    me=bpy.data.meshes.new("DERIVED_CLOSED_BODY_MESH");me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new("DERIVED_CLOSED_BODY",me);bpy.context.collection.objects.link(o);o.data.materials.append(M["CLAY"])
    for p in me.polygons:p.use_smooth=True
    for x,label in ((b.FX,"F"),(b.RX,"R")):
        bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=.405,depth=2.40,location=(x,0,b.WZ),rotation=(math.radians(90),0,0))
        cut=bpy.context.object;cut.name=f"DERIVED_WHEEL_CUT_{label}"
        bo=o.modifiers.new(f"DERIVED_WHEEL_ARCH_{label}","BOOLEAN");bo.operation="DIFFERENCE";bo.solver="EXACT";bo.object=cut
        bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=bo.name);bpy.data.objects.remove(cut,do_unlink=True)
    return o

def manifold(o):
    bm=bmesh.new();bm.from_mesh(o.data);n=sum(1 for e in bm.edges if not e.is_manifold);bm.free();return n

def render_r08(out,samples,res,M,L,G,source,derived):
    rd=out/"renders";rd.mkdir(parents=True,exist_ok=True);R=[]
    V=[
      ("SIDE_SILHOUETTE",(0,-8.8,1.14),(0,0,.64),85,True,5.25,"BROAD","sil"),
      ("PACKAGE_SIDE",(0,-8.8,1.14),(0,0,.64),85,True,5.25,"BROAD","normal"),
      ("TOP_ORTHO",(0,0,8),(0,0,.56),85,True,5.35,"BROAD","normal"),
      ("FRONT_ORTHO",(7.7,0,1.13),(0,0,.65),85,True,2.65,"BROAD","normal"),
      ("CLAY_BROAD",(6.2,-7.0,2.75),(.05,0,.66),78,False,5,"BROAD","normal"),
      ("CLAY_STRIP",(6.2,-7.0,2.75),(.05,0,.66),78,False,5,"STRIP","normal"),
      ("CLAY_GRAZING",(6.2,-7.0,2.75),(.05,0,.66),78,False,5,"GRAZING","normal"),
      ("SECTION_OVERLAY",(5.8,-6.4,3.0),(0,0,.70),80,False,5,"BROAD","guide"),
      ("CONTROL_CURVES",(5.8,-6.4,3.0),(0,0,.70),80,False,5,"BROAD","guide")]
    mesh=[o for o in bpy.context.scene.objects if o.type=="MESH" and o.name!="GROUND"]
    original={o.name:list(o.data.materials) for o in mesh};black=M["BLACK"]
    for lab,loc,t,lens,ortho,scale,rig,mode in V:
        b.setrig(L,rig)
        for o in G:o.hide_render=(mode!="guide")
        source.hide_render=True;derived.hide_render=False
        if mode=="sil":
            b.world((1,1,1),.75)
            for o in mesh:o.data.materials.clear();o.data.materials.append(black)
        else:
            b.world((.012,.012,.012),.16)
            for o in mesh:
                o.data.materials.clear()
                for mm in original[o.name]:o.data.materials.append(mm)
        c=b.camera("CAM_"+lab,loc,t,lens,ortho,scale);bpy.context.scene.camera=c
        p=rd/f"{MODEL}__{lab}.png";b.setup(p,samples,res);bpy.ops.render.render(write_still=True)
        R.append({"view":lab,"file":str(p),"mode":mode});bpy.data.objects.remove(c,do_unlink=True)
    return R

def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials()
    rows=b.controls_resampled();source,ids,verts=r.full_source_grid(rows,M);h0=source_hash(source);derived=build_closed_derived(rows,M);h1=source_hash(source)
    b.wheels(M);G=b.guides(rows,M);b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16)
    scene=bpy.context.scene;scene["OLEANDER_MODEL"]=MODEL;scene["OLEANDER_STAGE"]="M5";scene["OLEANDER_HARD_POINTS"]=json.dumps(b.HP)
    r.b.write_contract(out)
    cp=out/"MODELING_CONTRACT.json";c=json.loads(cp.read_text())
    c["job_id"]="SYS-MODELING-WORKER-AUTO-M1M5-v0.11-R08"
    c["decision_question"]="With R07 hard points and all 22 source sections locked, does the same source geometry read as a coherent automotive primary volume when wheel openings are tested only on a watertight derived diagnostic body?"
    c["source_authority"]["editable_source"]=f"{MODEL}.blend";c["source_authority"]["derived_models"]=["DERIVED_CLOSED_BODY"]
    c["sections"]["items"]=[{"id":f"SEC-{i:02d}","role":"transverse control station","station":s[0],"plane":"YZ","continuity_target":"R07 LOCKED","depends_on":["HP-WHEELBASE","HP-TRACK"],"status":"LOCKED"} for i,s in enumerate(b.SECTIONS)]
    c["locks"].append({"target":"R07 hard points + 22 sections","state":"LOCKED","reason":"R08 isolates diagnostic construction from design geometry","unlock_trigger":"post-R08 M5 Visual QA identifies proportion/section failure"})
    c["qa"]["construction"]=["R07 Source Grid hash unchanged before/after derived build","source remains continuous open quad authority","derived body is watertight after circular wheel openings","wheel-arch boolean never touches source"]
    c["qa"]["diagnostic_views"]=["SIDE_SILHOUETTE","PACKAGE_SIDE","TOP_ORTHO","FRONT_ORTHO","CLAY_BROAD","CLAY_STRIP","CLAY_GRAZING","SECTION_OVERLAY","CONTROL_CURVES"]
    c["resource_budget"]["max_render_views"]=9;cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n")
    blend=out/f"{MODEL}.blend";bpy.ops.wm.save_as_mainfile(filepath=str(blend));R=render_r08(out,a.samples,a.resolution,M,L,G,source,derived)
    mn,mx=b.bbox(source)
    qchecks={"source_hash_locked":h0==h1,"source_quad_only":all(len(p.vertices)==4 for p in source.data.polygons),"derived_manifold":manifold(derived)==0,"length":4.60<=mx.x-mn.x<=4.70,"width":1.80<=mx.y-mn.y<=1.92,"height":1.42<=mx.z<=1.47,"wheelbase":abs(b.FX-b.RX-2.82)<1e-8,"track":abs(2*b.WY-1.59)<1e-8,"section_count":len(b.SECTIONS)==22,"premature_detail_absent":not any(any(k in o.name for k in ["HANDLE","LAMP","MIRROR","SEAT","SCREEN","WIPER","CALIPER","SPOKE"]) for o in bpy.context.scene.objects),"render_matrix":len(R)==9}
    q={"schema":"oleander.auto.v0.11.r08.qa","model":MODEL,"status":"MACHINE_PASS_VISUAL_REVIEW_REQUIRED" if all(qchecks.values()) else "MACHINE_FAIL","source_hash_before":h0,"source_hash_after":h1,"source_locked":h0==h1,"derived_nonmanifold_edges":manifold(derived),"bounds":{"min":list(mn),"max":list(mx),"dimensions":[mx.x-mn.x,mx.y-mn.y,mx.z-mn.z]},"checks":qchecks,"renders":R,"boundary":"R08 tests presentation of the locked R07 primary source. Derived closed body and circular wheel arches are diagnostic only."}
    (out/"AUTOMOTIVE_V011_QA.json").write_text(json.dumps(q,ensure_ascii=False,indent=2)+"\n")
    rec={"schema":"oleander.auto.v0.11.r08.receipt","model":MODEL,"blender_version":bpy.app.version_string,"build_hash":bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),"renderer":"Cycles CPU","samples":a.samples,"resolution":[a.resolution,a.resolution],"status":"EXECUTED_"+q["status"],"blend":str(blend),"qa":str(out/"AUTOMOTIVE_V011_QA.json"),"renders":R}
    (out/"AUTOMOTIVE_V011_RECEIPT.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n");print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if all(qchecks.values()) else 5)

if __name__=="__main__":main()
