#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R22 — C1 Cosine-Squared Nested Wheel Arch.

R21 Final M5 = REVISE due genuine wheel-zone Source Geometry failure.

Locked:
- R09 cabin package / wheel hard points
- R11 transverse tension outside wheel zones
- R12 PCHIP interpolation
- R15 local terminal taper
- R16 shared-row topology ownership
- R18 structured front/rear termination topology
- R20 local termination winding

Open:
- wheel-zone z/y deformation law only.

New law:
w(u)=cos(pi*u/2)^2, |u|<=1
=> w=0 and dw/dx=0 at both endpoints.
Each nested row blends from its baseline to a center target without endpoint jumps.
"""
from __future__ import annotations
import importlib.util,bpy,json,math,hashlib
from pathlib import Path

BASE="/tmp/revise_v011_r20.py"
spec=importlib.util.spec_from_file_location("r20",BASE)
r20=importlib.util.module_from_spec(spec);spec.loader.exec_module(r20)
r18=r20.r18;r17=r20.r17;r16=r20.r16;r14=r20.r14;b=r20.b

MODEL="OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R22"
r20.MODEL=MODEL;r18.MODEL=MODEL;r17.MODEL=MODEL;r16.MODEL=MODEL
r16.r15.MODEL=MODEL;r14.MODEL=MODEL;r14.r12.MODEL=MODEL;r14.r11.MODEL=MODEL
r14.r10.MODEL=MODEL;r14.r09.MODEL=MODEL;r14.r08.MODEL=MODEL;r14.r08.r.MODEL=MODEL;b.MODEL=MODEL

SAMPLE_ZONE=.535  # locked R20/R17 x-station topology
DEFORM_ZONE=.475  # R22 actual C1 deformation corridor
TARGET_Z={3:.775,4:.835,5:.805,6:.780,7:.755}
Y_BIAS={3:.004,4:.018,5:.010,6:.005,7:.000}

def arch_weight(x,wx):
    u=(x-wx)/DEFORM_ZONE
    if abs(u)>=1:return 0.0
    return math.cos(math.pi*u/2.0)**2

def deform_at_x(rows,x):
    ps=[r14.interp_row(row,x) for row in rows]
    wx=min((b.FX,b.RX),key=lambda v:abs(x-v))
    w=arch_weight(x,wx)
    if w<=0:return ps
    out=list(ps)
    for row in (3,4,5,6,7):
        p=ps[row]
        tz=max(p[2],TARGET_Z[row])
        z=p[2]+w*(tz-p[2])
        y=p[1]+Y_BIAS[row]*w
        out[row]=(x,y,z)
    return out

def topology_membership_hash(o):
    h=hashlib.sha256()
    for p in o.data.polygons:
        h.update((",".join(map(str,sorted(p.vertices[:])))+";").encode())
    return h.hexdigest()

def coords(o):
    return [tuple(v.co) for v in o.data.vertices]

def build_r20_current(M,glass):
    rows=b.controls_resampled()
    base,xs,cols,mb=r16.build_source(rows,M,glass)
    r18src=r18.rebuild_termination(base,M,glass)
    src,flipped=r20.flip_termination_faces(r18src,M,glass)
    return src,xs,cols,flipped

def render_selective(out,samples,res,M,L,source,features,wire):
    rd=out/"renders";rd.mkdir(parents=True,exist_ok=True);R=[]
    V=[
      ("SIDE_SILHOUETTE",(0,-8.8,1.14),(0,0,.64),85,True,5.25,"BROAD","sil"),
      ("PACKAGE_SIDE",(0,-8.8,1.14),(0,0,.64),85,True,5.25,"BROAD","normal"),
      ("HERO_FRONT_3Q",(6.2,-7.0,2.75),(.05,0,.66),78,False,5,"BROAD","normal"),
      ("HERO_REAR_3Q",(-6.0,6.8,2.65),(-.10,0,.66),78,False,5,"BROAD","normal"),
      ("CLAY_STRIP",(6.2,-7.0,2.75),(.05,0,.66),78,False,5,"STRIP","normal"),
      ("CLAY_GRAZING",(6.2,-7.0,2.75),(.05,0,.66),78,False,5,"GRAZING","normal"),
      ("FRONT_ARCH_DETAIL",(2.65,-3.4,.95),(b.FX,-b.WY,.48),100,False,5,"STRIP","normal"),
      ("REAR_ARCH_DETAIL",(-2.55,-3.4,.95),(b.RX,-b.WY,.48),100,False,5,"STRIP","normal"),
      ("SOURCE_WIREFRAME",(5.8,-6.4,2.8),(0,0,.66),80,False,5,"BROAD","wire"),
    ]
    for lab,loc,t,lens,ortho,scale,rig,mode in V:
        b.setrig(L,rig);wire.hide_render=(mode!="wire");source.hide_render=(mode=="wire")
        for o in features:o.hide_render=True
        b.world((1,1,1),.75) if mode=="sil" else b.world((.012,.012,.012),.16)
        bpy.context.view_layer.material_override=M["BLACK"] if mode=="sil" else None
        c=b.camera("CAM_"+lab,loc,t,lens,ortho,scale);bpy.context.scene.camera=c
        p=rd/f"{MODEL}__{lab}.png";b.setup(p,samples,res);bpy.ops.render.render(write_still=True)
        R.append({"view":lab,"file":str(p),"mode":mode});bpy.data.objects.remove(c,do_unlink=True)
    bpy.context.view_layer.material_override=None;source.hide_render=False
    return R

def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials();glass=r14.diagnostic_glass()

    # Build R20 baseline before patching R16 deformation.
    baseline,x0,c0,f0=build_r20_current(M,glass)
    baseline_coords=coords(baseline);baseline_top=topology_membership_hash(baseline)
    bpy.data.objects.remove(baseline,do_unlink=True)

    # R22 wheel-zone law only.
    r16.deform_at_x=deform_at_x
    r16.ARCH_ZONE_R=SAMPLE_ZONE
    source,xs,cols,flipped=build_r20_current(M,glass)
    new_coords=coords(source);new_top=topology_membership_hash(source)

    assert len(baseline_coords)==len(new_coords)
    changed=[]
    outside_changed=[]
    for i,(a0,a1) in enumerate(zip(baseline_coords,new_coords)):
        if max(abs(a0[j]-a1[j]) for j in range(3))>1e-7:
            changed.append(i)
            x=a1[0]
            if not any(abs(x-wx)<=SAMPLE_ZONE+1e-6 for wx in (b.FX,b.RX)):
                outside_changed.append(i)

    features=r16.feature_guides(source,xs,cols,M)
    b.wheels(M);b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16)
    wire=r14.wire_overlay(source,M);stats=r14.topology_stats(source);islands=r16.island_count(source)

    scene=bpy.context.scene;scene["OLEANDER_MODEL"]=MODEL;scene["OLEANDER_STAGE"]="M5"
    scene["OLEANDER_REVISION"]="R22 C1 cosine-squared wheel-zone curvature only"

    r14.write_contract(out,source,stats,len(features))
    cp=out/"MODELING_CONTRACT.json";c=json.loads(cp.read_text())
    c["job_id"]="SYS-MODELING-WORKER-AUTO-M4M5-v0.11-R22"
    c["decision_question"]="Does replacing the R17 wheel-zone contact law with endpoint-C1 cosine-squared nested row deformation remove the R21 front/rear arch spikes while leaving all non-wheel source geometry and topology unchanged?"
    c["source_authority"]["editable_source"]=f"{MODEL}.blend"
    c["locks"].append({"target":"all non-wheel-zone R20 source coordinates + entire topology membership","state":"LOCKED","reason":"R22 isolates wheel-zone curvature","unlock_trigger":None})
    c["revision"]={"revision_id":"R22-C1-COSINE-ARCH","semantic_targets":["wheel-zone SHOULDER/MID/ROCKER/UNDER rows"],"parameters":{"sample_zone_radius_m":SAMPLE_ZONE,"deform_zone_radius_m":DEFORM_ZONE,"weight":"cos(pi*u/2)^2","center_target_z_m":TARGET_Z,"y_bias_m":Y_BIAS},"expected_affected_components":["front/rear wheel-zone Source vertices only"],"affected_view_policy":"MANUAL"}
    c["qa"]["construction"]=["face membership topology hash unchanged from R20","all changed vertices lie within wheel zones","C1 endpoint weight: w=0 and dw/dx=0","one connected source mesh","no Boolean/SubD/ngon"]
    c["qa"]["project"]=["front arch spike/tear must close","rear arch endpoint must close","termination geometry is R20 locked","M6/M7/M8 remains blocked"]
    c["resource_budget"]["max_render_views"]=9
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n")

    blend=out/f"{MODEL}.blend";bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    R=render_selective(out,a.samples,a.resolution,M,L,source,features,wire)
    checks={"topology_membership_unchanged":baseline_top==new_top,"changed_vertices_positive":len(changed)>0,
            "outside_wheel_zone_changed_zero":len(outside_changed)==0,"source_island_count_one":islands==1,
            "source_ngon_zero":stats["ngon"]==0,"termination_triangles_four":stats["tri"]==4,
            "termination_faces_winding_repaired":len(flipped)==28,
            "source_no_boolean":not any(m.type=="BOOLEAN" for m in source.modifiers),
            "source_no_subd":not any(m.type=="SUBSURF" for m in source.modifiers),"render_matrix":len(R)==9}
    q={"schema":"oleander.auto.v0.11.r22.qa","model":MODEL,"status":"MACHINE_PASS_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL",
       "baseline_topology_membership_hash":baseline_top,"new_topology_membership_hash":new_top,
       "changed_vertex_count":len(changed),"outside_wheel_zone_changed_count":len(outside_changed),
       "topology":stats,"checks":checks,"renders":R,
       "boundary":"R22 modifies only wheel-zone coordinate deformation. R20 termination and non-wheel geometry are locked. Visual QA required."}
    (out/"AUTOMOTIVE_V011_QA.json").write_text(json.dumps(q,ensure_ascii=False,indent=2)+"\n")
    rec={"schema":"oleander.auto.v0.11.r22.receipt","model":MODEL,"blender_version":bpy.app.version_string,
         "build_hash":bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),
         "renderer":"Cycles CPU","samples":a.samples,"resolution":[a.resolution,a.resolution],
         "status":"EXECUTED_"+q["status"],"blend":str(blend),"qa":str(out/"AUTOMOTIVE_V011_QA.json"),"renders":R}
    (out/"AUTOMOTIVE_V011_RECEIPT.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if all(checks.values()) else 5)

if __name__=="__main__":main()
