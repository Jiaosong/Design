#!/usr/bin/env python3
"""OLEANDER Automotive Primary Surface v0.8 — R02 patch.

Applies only:
- QA height measurement correction (ground-referenced exterior height);
- cabin section refinement (flatter roof crown / stronger front-rear taper);
- explicit side/windshield/rear-glass rake.

Body primary sections, wheelbase, track, wheel guides and wheel openings remain locked.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import bpy

ap=argparse.ArgumentParser()
ap.add_argument("--base-source",required=True)
ap.add_argument("--out",required=True)
ap.add_argument("--samples",type=int,default=8)
ap.add_argument("--resolution",type=int,default=640)
av=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
a=ap.parse_args(av)

# Import definitions only; never execute base main().
src=Path(a.base_source).read_text(encoding="utf-8")
defs=src.split('if __name__=="__main__":')[0]
exec(compile(defs,a.base_source,"exec"),globals(),globals())

MODEL="OLEANDER_Automotive_Primary_Surface_v0.8"

CABIN_SECTIONS=[
    (-1.48,.66,.53,.35,.85,1.06,1.15),
    (-1.30,.70,.58,.43,.86,1.17,1.28),
    (-1.05,.73,.62,.50,.87,1.28,1.38),
    (-0.72,.745,.635,.55,.875,1.35,1.415),
    (-0.35,.750,.640,.57,.880,1.375,1.428),
    (-0.10,.750,.640,.575,.882,1.382,1.430),
    ( 0.20,.745,.635,.56,.885,1.355,1.415),
    ( 0.48,.730,.610,.50,.890,1.275,1.350),
    ( 0.72,.700,.570,.43,.895,1.165,1.255),
    ( 0.88,.650,.510,.35,.900,1.045,1.135),
]

def cabin_ring(sec):
    x,wb,wu,wr,zb,zu,zr=sec
    pts=[
        (0.0,zr),(wr*.55,zr),(wr,zr-.014),(wu,zu),(wb,zb),(0.0,zb-.022),
        (-wb,zb),(-wu,zu),(-wr,zr-.014),(-wr*.55,zr),
    ]
    return [(x,y,z) for y,z in pts]

def glazing_from_sections(mats):
    for side in (1,-1):
        sy=float(side)
        quad_panel(f"SIDE_GLASS_FRONT_{side:+}",[
            (.70,sy*.704,.908),(-.13,sy*.752,.895),(-.16,sy*.632,1.365),(.45,sy*.590,1.300)
        ],mats["GLASS"],.006)
        quad_panel(f"SIDE_GLASS_REAR_{side:+}",[
            (-.18,sy*.752,.895),(-1.18,sy*.690,.875),(-.92,sy*.565,1.245),(-.20,sy*.632,1.365)
        ],mats["GLASS"],.006)
        quad_panel(f"B_PILLAR_{side:+}",[
            (-.175,sy*.754,.895),(-.135,sy*.754,.895),(-.155,sy*.634,1.366),(-.195,sy*.634,1.366)
        ],mats["BODY"],.009)
    quad_panel("WINDSHIELD",[
        (.86,-.565,.908),(.86,.565,.908),(.44,.505,1.305),(.44,-.505,1.305)
    ],mats["GLASS"],.008)
    quad_panel("REAR_GLASS",[
        (-1.30,-.575,.865),(-.82,-.525,1.300),(-.82,.525,1.300),(-1.30,.575,.865)
    ],mats["GLASS"],.008)

# Remove only cabin-derived geometry and old diagnostic overlays.
for o in list(bpy.data.objects):
    n=o.name
    if (
        n.startswith("CABIN_PRIMARY") or n.startswith("SIDE_GLASS_") or
        n.startswith("B_PILLAR_") or n in {"WINDSHIELD","REAR_GLASS"} or
        n.startswith("SEC_BODY_") or n.startswith("SEC_CABIN_") or
        n.startswith("GUIDE_") or n in {"BODY_CONTROL_WIRE","CABIN_CONTROL_WIRE"}
    ):
        bpy.data.objects.remove(o,do_unlink=True)

mats={
    "BODY":bpy.data.materials["MAT_PRIMARY_CLAY"],
    "GLASS":bpy.data.materials["MAT_GUIDE_GLASS"],
    "TIRE":bpy.data.materials["MAT_TIRE_GUIDE"],
    "RIM":bpy.data.materials["MAT_RIM_GUIDE"],
    "GROUND":bpy.data.materials["MAT_GROUND"],
    "SECTION":bpy.data.materials["MAT_SECTION"],
    "GUIDE":bpy.data.materials["MAT_GUIDE"],
    "CAGE":bpy.data.materials["MAT_CONTROL_CAGE"],
    "BLACK":bpy.data.materials["MAT_SILHOUETTE"],
}

body=bpy.data.objects["BODY_PRIMARY"]
body_cage=bpy.data.objects["BODY_PRIMARY_CAGE"]
cabin,cabin_cage=loft_from_rings(
    "CABIN_PRIMARY",[cabin_ring(s) for s in CABIN_SECTIONS],mats["BODY"],2,True
)
glazing_from_sections(mats)
wire_objs=[
    make_wire_overlay(body_cage,"BODY_CONTROL_WIRE",mats["CAGE"]),
    make_wire_overlay(cabin_cage,"CABIN_CONTROL_WIRE",mats["CAGE"]),
]
section_objs=section_overlay(mats)
lights={
    "BROAD":[bpy.data.objects["BROAD_KEY"],bpy.data.objects["BROAD_FILL"]],
    "STRIP":[bpy.data.objects["STRIP_KEY"],bpy.data.objects["STRIP_FILL"]],
    "GRAZING":[bpy.data.objects["GRAZING_KEY"],bpy.data.objects["GRAZING_FILL"]],
}

out=Path(a.out).resolve()
out.mkdir(parents=True,exist_ok=True)
build_contract(out)

scene=bpy.context.scene
scene["OLEANDER_MODEL"]=MODEL
scene["OLEANDER_REVISION"]="R02"
scene["OLEANDER_REVISION_SCOPE"]="QA height + cabin sections + glazing rake; body/wheel hard points locked"

blend=out/f"{MODEL}.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
renders=render_matrix(out,a.samples,a.resolution,mats,lights,section_objs,wire_objs)

q=machine_qa(out,body,cabin,body_cage,cabin_cage,renders)
# Correct v0.8-R01 QA bug: exterior height is max-Z from ground datum, not bbox Z-span.
exterior_height=q["primary_bounds_m"]["max"][2]
q["checks"]["height_corridor"]=1.38 <= exterior_height <= 1.46
q["status"]="MACHINE_PASS_VISUAL_REVIEW_REQUIRED" if all(q["checks"].values()) else "MACHINE_FAIL"
q["revision"]="R02"
q["revision_scope"]="QA height + cabin section flattening/taper + explicit glazing rake"
q["exterior_height_from_ground_m"]=exterior_height
(out/"AUTOMOTIVE_PRIMARY_QA.json").write_text(json.dumps(q,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rec={
    "schema":"oleander.automotive-primary-surface.receipt.v0.8-r02",
    "model":MODEL,
    "revision":"R02",
    "blender_version":bpy.app.version_string,
    "build_hash":bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),
    "renderer":"Cycles CPU",
    "samples":a.samples,
    "resolution":[a.resolution,a.resolution],
    "status":"EXECUTED_MACHINE_PASS_VISUAL_REVIEW_REQUIRED" if q["status"].startswith("MACHINE_PASS") else "EXECUTED_MACHINE_FAIL",
    "blend":str(blend),
    "contract":str(out/"MODELING_CONTRACT.json"),
    "qa":str(out/"AUTOMOTIVE_PRIMARY_QA.json"),
    "renders":renders,
}
(out/"AUTOMOTIVE_PRIMARY_RECEIPT.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rec,ensure_ascii=False,indent=2))
raise SystemExit(0 if q["status"].startswith("MACHINE_PASS") else 5)
