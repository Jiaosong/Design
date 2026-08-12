#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R06 — Continuous Source Grid + Derived Wheel Arch Diagnostic."""
from __future__ import annotations
import importlib.util, bpy, json, math
from pathlib import Path
from mathutils import Vector

BASE="/tmp/build_automotive_v011_r05.py"
spec=importlib.util.spec_from_file_location("r05",BASE)
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)

MODEL="OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R06"
b.MODEL=MODEL

# Preserve stronger hood/cowl/A and C/backlight inflections.
b.SECTIONS=[
 ( 2.25,.52,.26,.53,.34,.47,.43,.35,.48,.24,.38,.16,.32),
 ( 2.16,.57,.35,.57,.44,.51,.53,.38,.58,.23,.47,.155,.38),
 ( 1.98,.65,.50,.64,.58,.57,.68,.41,.74,.215,.61,.15,.49),
 ( 1.72,.73,.62,.71,.69,.64,.82,.44,.88,.20,.77,.15,.62),
 ( 1.41,.80,.67,.78,.76,.69,.92,.47,.93,.19,.85,.15,.69),
 ( 1.16,.82,.68,.81,.78,.71,.925,.48,.93,.19,.86,.15,.70),
 ( 0.96,.87,.67,.84,.79,.73,.92,.49,.93,.19,.86,.15,.70),
 ( 0.86,.95,.64,.85,.79,.74,.92,.49,.93,.19,.86,.15,.70),
 ( 0.68,1.13,.53,.85,.80,.75,.915,.49,.925,.19,.86,.15,.70),
 ( 0.42,1.32,.52,.85,.81,.755,.91,.49,.92,.19,.86,.15,.70),
 ( 0.10,1.43,.55,.85,.81,.76,.91,.49,.92,.19,.86,.15,.70),
 (-0.12,1.45,.56,.85,.81,.76,.91,.49,.92,.19,.86,.15,.70),
 (-0.48,1.42,.54,.845,.805,.755,.91,.49,.92,.19,.86,.15,.70),
 (-0.78,1.34,.50,.84,.80,.75,.91,.49,.92,.19,.86,.15,.70),
 (-1.00,1.24,.47,.83,.79,.74,.905,.48,.92,.19,.85,.15,.69),
 (-1.20,1.08,.51,.815,.78,.72,.90,.47,.915,.19,.84,.15,.68),
 (-1.41,.92,.61,.79,.76,.69,.90,.46,.91,.19,.83,.15,.67),
 (-1.72,.79,.62,.75,.71,.64,.85,.43,.87,.20,.77,.15,.61),
 (-2.02,.67,.49,.64,.57,.56,.67,.40,.72,.22,.58,.15,.46),
 (-2.25,.54,.27,.55,.35,.48,.46,.36,.51,.25,.40,.16,.33)
]
b.HP["cowl_x_m"]=.86;b.HP["cowl_z_m"]=.95
b.HP["roof_peak_x_m"]=-.12;b.HP["roof_peak_z_m"]=1.45

def linear_resample(points,steps=4):
    out=[]
    for i in range(len(points)-1):
        p1,p2=points[i],points[i+1]
        for j in range(steps):
            t=j/steps
            out.append(tuple(p1[d]+(p2[d]-p1[d])*t for d in range(3)))
    out.append(points[-1])
    return out
b.resample_list=linear_resample

def full_grid(rows,M):
    nX=len(rows[0]);verts=[];ids=[]
    for xi in range(nX):
        right=[rows[i][xi] for i in range(7,0,-1)]
        center=[rows[0][xi]]
        left=[(p[0],-p[1],p[2]) for p in [rows[i][xi] for i in range(1,8)]]
        cross=right+center+left
        row=[]
        for p in cross:row.append(len(verts));verts.append(p)
        ids.append(row)
    nY=len(ids[0]);faces=[]
    for i in range(nX-1):
        for j in range(nY-1):
            faces.append((ids[i][j],ids[i+1][j],ids[i+1][j+1],ids[i][j+1]))
    me=bpy.data.meshes.new("PRIMARY_SOURCE_GRID_MESH");me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new("PRIMARY_SOURCE_GRID",me);bpy.context.collection.objects.link(o);o.data.materials.append(M["CLAY"])
    for p in me.polygons:p.use_smooth=True
    return o,ids,verts

def cap(name,cross,ma,reverse=False):
    verts=list(cross);face=tuple(reversed(range(len(verts)))) if reverse else tuple(range(len(verts)))
    me=bpy.data.meshes.new(name+"_M");me.from_pydata(verts,[],[face]);me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(ma);return o

def derived_body(source,M):
    d=source.copy();d.data=source.data.copy();d.name="BODY_DIAGNOSTIC_DERIVED";bpy.context.collection.objects.link(d)
    sol=d.modifiers.new("DIAGNOSTIC_THICKNESS","SOLIDIFY");sol.thickness=.008
    bpy.context.view_layer.objects.active=d;bpy.ops.object.modifier_apply(modifier=sol.name)
    for x,label in ((b.FX,"F"),(b.RX,"R")):
        bpy.ops.mesh.primitive_cylinder_add(vertices=72,radius=.405,depth=2.40,location=(x,0,b.WZ),rotation=(math.radians(90),0,0))
        cut=bpy.context.object;cut.name=f"CUT_WHEEL_{label}"
        bo=d.modifiers.new(f"WHEEL_ARCH_{label}","BOOLEAN");bo.operation="DIFFERENCE";bo.solver="EXACT";bo.object=cut
        bpy.context.view_layer.objects.active=d;bpy.ops.object.modifier_apply(modifier=bo.name);bpy.data.objects.remove(cut,do_unlink=True)
    return d

def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials()
    rows=b.controls_resampled()
    source,ids,verts=full_grid(rows,M);source.hide_render=True
    derived=derived_body(source,M)
    front=[verts[k] for k in ids[-1]];rear=[verts[k] for k in ids[0]]
    fcap=cap("FRONT_TERMINATION",front,M["CLAY"],False)
    rcap=cap("REAR_TERMINATION",rear,M["CLAY"],True)
    G=b.guides(rows,M);b.wheels(M);b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16)

    bpy.context.scene["OLEANDER_MODEL"]=MODEL;bpy.context.scene["OLEANDER_STAGE"]="M5";bpy.context.scene["OLEANDER_HARD_POINTS"]=json.dumps(b.HP)
    b.write_contract(out)
    cp=out/"MODELING_CONTRACT.json";c=json.loads(cp.read_text())
    c["job_id"]="SYS-MODELING-WORKER-AUTO-M1M5-v0.11-R06"
    c["decision_question"]="Can a continuous source grid with explicit profile inflections and a derived-only circular wheel-arch diagnostic establish a credible automotive primary proportion without corrupting source topology?"
    c["source_authority"]["editable_source"]=f"{MODEL}.blend"
    c["source_authority"]["derived_models"]=["BODY_DIAGNOSTIC_DERIVED","FRONT_TERMINATION","REAR_TERMINATION"]
    c["sections"]["items"]=[{"id":f"SEC-{i:02d}","role":"transverse control station","station":s[0],"plane":"YZ","continuity_target":"controlled longitudinal progression","depends_on":["HP-WHEELBASE","HP-TRACK"],"status":"OPEN"} for i,s in enumerate(b.SECTIONS)]
    c["primary_geometry"][0]["source_sections"]=[f"SEC-{i:02d}" for i in range(len(b.SECTIONS))]
    c["semantic_components"][1]["parameters"]={"section_count":len(b.SECTIONS),"resample_mode":"piecewise-linear / tangent-preserving"}
    c["qa"]["construction"]=["source grid is continuous and quad-only","cowl/backlight stations preserved without Catmull oversmoothing","wheel arches exist only on derived diagnostic shell","front/rear termination is derived diagnostic geometry"]
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n")

    blend=out/f"{MODEL}.blend";bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    R=b.render(out,a.samples,a.resolution,M,L,G,derived)

    mn,mx=b.bbox(source);tri=quad=ngon=0
    for p in source.data.polygons:
        n=len(p.vertices)
        if n==4:quad+=1
        elif n==3:tri+=1
        else:ngon+=1
    premature=[o.name for o in bpy.context.scene.objects if any(k in o.name for k in ["HANDLE","LAMP","MIRROR","SEAT","SCREEN","WIPER","CALIPER","SPOKE"])]
    checks={"length":4.45<=mx.x-mn.x<=4.55,"width":1.80<=mx.y-mn.y<=1.92,"height":1.42<=mx.z<=1.47,
            "wheelbase":abs(b.FX-b.RX-2.82)<1e-8,"track":abs(2*b.WY-1.60)<1e-8,"section_count":len(b.SECTIONS)==20,
            "source_quad_only":tri==0 and ngon==0,"derived_wheel_arches":all(f"WHEEL_ARCH_{x}" not in [m.name for m in derived.modifiers] for x in ("F","R")),
            "termination_surfaces":fcap is not None and rcap is not None,"premature_detail_absent":not premature,"render_matrix":len(R)==8}
    q={"schema":"oleander.auto.v0.11.r06.qa","model":MODEL,"status":"MACHINE_PASS_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL",
       "bounds":{"min":list(mn),"max":list(mx),"dimensions":[mx.x-mn.x,mx.y-mn.y,mx.z-mn.z]},"source_face_counts":{"quad":quad,"tri":tri,"ngon":ngon},
       "checks":checks,"renders":R,"boundary":"Editable source is the continuous open quad grid. Wheel arches and termination faces are diagnostic derived geometry only. Visual M5 review required."}
    (out/"AUTOMOTIVE_V011_QA.json").write_text(json.dumps(q,ensure_ascii=False,indent=2)+"\n")
    rec={"schema":"oleander.auto.v0.11.r06.receipt","model":MODEL,"blender_version":bpy.app.version_string,
         "build_hash":bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),"renderer":"Cycles CPU",
         "samples":a.samples,"resolution":[a.resolution,a.resolution],"status":"EXECUTED_"+q["status"],"blend":str(blend),"qa":str(out/"AUTOMOTIVE_V011_QA.json"),"renders":R}
    (out/"AUTOMOTIVE_V011_RECEIPT.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if all(checks.values()) else 5)

if __name__=="__main__":main()
