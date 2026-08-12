#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R10 — Semantic Glazing Diagnostic on Locked R09 Geometry.

Geometry/hard points/sections are unchanged from R09.
Only a diagnostic material-zone classification is added on DERIVED body faces.
This is not M6 component authority and does not mutate the Source Grid.
"""
from __future__ import annotations
import importlib.util,bpy,json
from pathlib import Path
from mathutils import Vector

BASE="/tmp/revise_v011_r09.py"
spec=importlib.util.spec_from_file_location("r09",BASE)
r09=importlib.util.module_from_spec(spec);spec.loader.exec_module(r09)
r08=r09.r08;b=r09.b

MODEL="OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R10"
r09.MODEL=MODEL;r08.MODEL=MODEL;r08.r.MODEL=MODEL;b.MODEL=MODEL

def semantic_glass_material():
    return b.mat("MAT_SEMANTIC_GLAZING_DIAG",(0.012,.025,.030,1),.16,0)

def assign_glazing_zone(o,glass):
    o.data.materials.append(glass);glass_index=len(o.data.materials)-1;count=0
    for p in o.data.polygons:
        pts=[o.data.vertices[i].co for i in p.vertices]
        cx=sum(v.x for v in pts)/len(pts);cz=sum(v.z for v in pts)/len(pts);nz=abs(p.normal.z)
        if -1.22 <= cx <= .72 and cz >= .84 and nz < .82:
            p.material_index=glass_index;count+=1
    return count

def render_r10(out,samples,res,M,L,G,source,derived):
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
    for lab,loc,t,lens,ortho,scale,rig,mode in V:
        b.setrig(L,rig)
        for o in G:o.hide_render=(mode!="guide")
        source.hide_render=True;derived.hide_render=False
        b.world((1,1,1),.75) if mode=="sil" else b.world((.012,.012,.012),.16)
        bpy.context.view_layer.material_override=M["BLACK"] if mode=="sil" else None
        c=b.camera("CAM_"+lab,loc,t,lens,ortho,scale);bpy.context.scene.camera=c
        p=rd/f"{MODEL}__{lab}.png";b.setup(p,samples,res);bpy.ops.render.render(write_still=True)
        R.append({"view":lab,"file":str(p),"mode":mode});bpy.data.objects.remove(c,do_unlink=True)
    bpy.context.view_layer.material_override=None;return R

def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials();rows=b.controls_resampled()
    source,ids,verts=r08.r.full_source_grid(rows,M);h0=r08.source_hash(source);derived=r08.build_closed_derived(rows,M);h1=r08.source_hash(source)
    glass=semantic_glass_material();glass_faces=assign_glazing_zone(derived,glass)
    b.wheels(M);G=b.guides(rows,M);b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16)
    scene=bpy.context.scene;scene["OLEANDER_MODEL"]=MODEL;scene["OLEANDER_STAGE"]="M5";scene["OLEANDER_HARD_POINTS"]=json.dumps(b.HP)
    r08.r.b.write_contract(out);cp=out/"MODELING_CONTRACT.json";c=json.loads(cp.read_text())
    c["job_id"]="SYS-MODELING-WORKER-AUTO-M1M5-v0.11-R10";c["decision_question"]="With R09 geometry completely locked, does a derived semantic glazing-zone diagnostic reveal a coherent greenhouse/body proportion, or does the section network still require M3 revision?"
    c["source_authority"]["editable_source"]=f"{MODEL}.blend";c["source_authority"]["derived_models"]=["DERIVED_CLOSED_BODY","MAT_SEMANTIC_GLAZING_DIAG"]
    c["sections"]["items"]=[{"id":f"SEC-{i:02d}","role":"R09 locked transverse station","station":s[0],"plane":"YZ","continuity_target":"LOCKED for semantic diagnostic","depends_on":["HP-WHEELBASE","HP-TRACK"],"status":"LOCKED"} for i,s in enumerate(b.SECTIONS)]
    c["locks"].append({"target":"R09 geometry / hard points / sections","state":"LOCKED","reason":"R10 tests semantic reading only","unlock_trigger":"R10 Visual QA = REVISE"})
    c["qa"]["construction"]=["source hash unchanged","derived wheel-arch body manifold","semantic glazing is polygon material classification only","silhouette uses material override and preserves polygon material indices"]
    c["qa"]["project"]=["glazing zone must clarify rather than hide greenhouse proportion","if semantic reading remains monolithic or cabin is oversized, reopen M3","no M6 authority is created by R10"]
    c["resource_budget"]["max_render_views"]=9;cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n")
    blend=out/f"{MODEL}.blend";bpy.ops.wm.save_as_mainfile(filepath=str(blend));R=render_r10(out,a.samples,a.resolution,M,L,G,source,derived)
    mn,mx=b.bbox(source);checks={"source_hash_locked":h0==h1,"source_quad_only":all(len(p.vertices)==4 for p in source.data.polygons),"derived_manifold":r08.manifold(derived)==0,"glazing_zone_faces":glass_faces>100,"length":4.60<=mx.x-mn.x<=4.70,"width":1.80<=mx.y-mn.y<=1.92,"height":1.42<=mx.z<=1.47,"wheelbase":abs(b.FX-b.RX-2.82)<1e-8,"track":abs(2*b.WY-1.59)<1e-8,"section_count":len(b.SECTIONS)==22,"render_matrix":len(R)==9}
    q={"schema":"oleander.auto.v0.11.r10.qa","model":MODEL,"status":"MACHINE_PASS_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL","source_hash_before":h0,"source_hash_after":h1,"derived_nonmanifold_edges":r08.manifold(derived),"glazing_zone_face_count":glass_faces,"checks":checks,"renders":R,"boundary":"R10 adds only a semantic glazing diagnostic to locked R09 derived geometry. It creates no M6 component or material authority."}
    (out/"AUTOMOTIVE_V011_QA.json").write_text(json.dumps(q,ensure_ascii=False,indent=2)+"\n");rec={"schema":"oleander.auto.v0.11.r10.receipt","model":MODEL,"blender_version":bpy.app.version_string,"build_hash":bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),"renderer":"Cycles CPU","samples":a.samples,"resolution":[a.resolution,a.resolution],"status":"EXECUTED_"+q["status"],"blend":str(blend),"qa":str(out/"AUTOMOTIVE_V011_QA.json"),"renders":R};(out/"AUTOMOTIVE_V011_RECEIPT.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n");print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if all(checks.values()) else 5)
if __name__=="__main__":main()
