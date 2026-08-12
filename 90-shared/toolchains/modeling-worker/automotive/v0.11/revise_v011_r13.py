#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R13 — Clean Derived Wheel-Arch Diagnostic.

R12 hard points, 22 sections, transverse tension and PCHIP interpolation are LOCKED.
Source Grid is unchanged.
Derived-only change:
- close diagnostic body
- SIMPLE subdivision for density only (no shape smoothing)
- circular wheel-arch booleans on the denser derived mesh
Purpose: remove coarse-boolean spikes from M5 visual evidence.
"""
from __future__ import annotations
import importlib.util,bpy,bmesh,json,math,hashlib
from pathlib import Path

BASE="/tmp/revise_v011_r12.py"
spec=importlib.util.spec_from_file_location("r12",BASE)
r12=importlib.util.module_from_spec(spec);spec.loader.exec_module(r12)
r11=r12.r11;r10=r12.r10;r08=r12.r08;b=r12.b

MODEL="OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R13"
r12.MODEL=MODEL;r11.MODEL=MODEL;r10.MODEL=MODEL;r08.MODEL=MODEL;r08.r.MODEL=MODEL;b.MODEL=MODEL

def source_hash(o):return r08.source_hash(o)

def dense_closed_derived(rows,M):
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
    me=bpy.data.meshes.new("DERIVED_DENSE_BODY_MESH");me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new("DERIVED_DENSE_BODY",me);bpy.context.collection.objects.link(o);o.data.materials.append(M["CLAY"])
    for p in me.polygons:p.use_smooth=True
    sub=o.modifiers.new("DIAGNOSTIC_SIMPLE_DENSITY","SUBSURF");sub.subdivision_type='SIMPLE';sub.levels=1;sub.render_levels=1
    bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=sub.name)
    for x,label in ((b.FX,"F"),(b.RX,"R")):
        bpy.ops.mesh.primitive_cylinder_add(vertices=128,radius=.405,depth=2.40,location=(x,0,b.WZ),rotation=(math.radians(90),0,0))
        cut=bpy.context.object;cut.name=f"DENSE_WHEEL_CUT_{label}"
        bo=o.modifiers.new(f"DENSE_WHEEL_ARCH_{label}","BOOLEAN");bo.operation="DIFFERENCE";bo.solver="EXACT";bo.object=cut
        bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=bo.name);bpy.data.objects.remove(cut,do_unlink=True)
    return o

def manifold(o):
    bm=bmesh.new();bm.from_mesh(o.data);n=sum(1 for e in bm.edges if not e.is_manifold);bm.free();return n

def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials();rows=b.controls_resampled()
    source,ids,verts=r08.r.full_source_grid(rows,M);h0=source_hash(source);derived=dense_closed_derived(rows,M);h1=source_hash(source)
    glass=r10.semantic_glass_material();glass_faces=r10.assign_glazing_zone(derived,glass)
    b.wheels(M);G=b.guides(rows,M);b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16)
    scene=bpy.context.scene;scene["OLEANDER_MODEL"]=MODEL;scene["OLEANDER_STAGE"]="M5";scene["OLEANDER_HARD_POINTS"]=json.dumps(b.HP)
    r08.r.b.write_contract(out);cp=out/"MODELING_CONTRACT.json";c=json.loads(cp.read_text())
    c["job_id"]="SYS-MODELING-WORKER-AUTO-M1M5-v0.11-R13";c["decision_question"]="With R12 geometry and PCHIP interpolation locked, does a denser derived-only circular wheel-arch diagnostic remove Boolean artifacts sufficiently to judge the underlying primary proportion and section quality?"
    c["source_authority"]["editable_source"]=f"{MODEL}.blend";c["source_authority"]["derived_models"]=["DERIVED_DENSE_BODY","MAT_SEMANTIC_GLAZING_DIAG"]
    c["sections"]["items"]=[{"id":f"SEC-{i:02d}","role":"R12 locked section","station":s[0],"plane":"YZ","continuity_target":"LOCKED / diagnostic-only revision","depends_on":["HP-WHEELBASE","HP-TRACK"],"status":"LOCKED"} for i,s in enumerate(b.SECTIONS)]
    c["locks"].append({"target":"R12 hard points + 22 sections + transverse tension + PCHIP interpolation","state":"LOCKED","reason":"R13 isolates wheel-arch diagnostic quality","unlock_trigger":"post-R13 M5 Visual QA confirms genuine primary-geometry failure"})
    c["revision"]={"revision_id":"R13-DERIVED-ARCH-DIAGNOSTIC","semantic_targets":["DERIVED_DENSE_BODY"],"parameters":{"simple_subdivision":1,"wheel_cut_segments":128},"expected_affected_components":["DERIVED_DENSE_BODY"],"affected_view_policy":"HYBRID"}
    c["qa"]["construction"]=["Source Grid hash unchanged","SIMPLE subdivision modifies density only","wheel booleans occur on Derived only","Derived remains manifold","semantic glazing remains diagnostic only"]
    c["qa"]["project"]=["if arch artifacts disappear but vehicle still fails, reopen M3/M4","R13 cannot promote a source based solely on cleaner Boolean","no M6 authority created"]
    c["resource_budget"]["max_render_views"]=9;cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n")
    blend=out/f"{MODEL}.blend";bpy.ops.wm.save_as_mainfile(filepath=str(blend));R=r10.render_r10(out,a.samples,a.resolution,M,L,G,source,derived)
    mn,mx=b.bbox(source);checks={"source_hash_locked":h0==h1,"source_quad_only":all(len(p.vertices)==4 for p in source.data.polygons),"derived_manifold":manifold(derived)==0,"derived_vertex_density":len(derived.data.vertices)>len(source.data.vertices)*2,"glazing_zone_faces":glass_faces>100,"length":4.60<=mx.x-mn.x<=4.70,"width":1.80<=mx.y-mn.y<=1.94,"height":1.42<=mx.z<=1.47,"wheelbase":abs(b.FX-b.RX-2.82)<1e-8,"track":abs(2*b.WY-1.59)<1e-8,"section_count":len(b.SECTIONS)==22,"render_matrix":len(R)==9}
    q={"schema":"oleander.auto.v0.11.r13.qa","model":MODEL,"status":"MACHINE_PASS_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL","source_hash_before":h0,"source_hash_after":h1,"source_vertices":len(source.data.vertices),"derived_vertices":len(derived.data.vertices),"derived_nonmanifold_edges":manifold(derived),"glazing_zone_face_count":glass_faces,"checks":checks,"renders":R,"boundary":"R13 changes derived diagnostic density and wheel-arch cutting only. R12 source geometry remains locked."}
    (out/"AUTOMOTIVE_V011_QA.json").write_text(json.dumps(q,ensure_ascii=False,indent=2)+"\n");rec={"schema":"oleander.auto.v0.11.r13.receipt","model":MODEL,"blender_version":bpy.app.version_string,"build_hash":bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),"renderer":"Cycles CPU","samples":a.samples,"resolution":[a.resolution,a.resolution],"status":"EXECUTED_"+q["status"],"blend":str(blend),"qa":str(out/"AUTOMOTIVE_V011_QA.json"),"renders":R};(out/"AUTOMOTIVE_V011_RECEIPT.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n");print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if all(checks.values()) else 5)
if __name__=="__main__":main()
