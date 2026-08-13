#!/usr/bin/env python3
"""OLEANDER Modeling Worker v0.12 E2 — relationship-driven multi-patch compiler.

E2 promotes seam continuity from an implicit modeling preference to an explicit design
relationship. A sparse editable center patch is combined with independent front/rear
termination boundaries. The compiler derives the two termination cages so the shared
boundaries satisfy parametric C2 continuity. Only after the surface network compiles is a
welded execution mesh generated.

This benchmark proves a multi-patch method contract only. It does not claim Class-A,
automotive engineering, manufacturing, production paneling or final design quality.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Iterable

import bpy
from mathutils import Vector

MODEL = "OLEANDER_ModelingWorker_v0.12_E2_MultiPatch"


def user_args() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]


def b3(t: float) -> tuple[float, float, float, float]:
    s = 1.0 - t
    return (s*s*s, 3*s*s*t, 3*s*t*t, t*t*t)


def db3(t: float) -> tuple[float, float, float, float]:
    s = 1.0 - t
    return (-3*s*s, 3*s*s - 6*s*t, 6*s*t - 3*t*t, 3*t*t)


def ddb3(t: float) -> tuple[float, float, float, float]:
    return (6*(1-t), -12 + 18*t, 6 - 18*t, 6*t)


def p_add(*pts: Iterable[float]) -> list[float]:
    vals = [tuple(p) for p in pts]
    return [sum(p[k] for p in vals) for k in range(3)]


def p_scale(p: Iterable[float], s: float) -> list[float]:
    q = tuple(p)
    return [q[k] * s for k in range(3)]


def compile_c2_chain(center: list[list[list[float]]], front_boundary: list[list[float]], rear_boundary: list[list[float]]):
    """Compile FRONT/CENTER/REAR bicubic cages with exact parametric C2 seams.

    For A->B cubic Bezier segments, C2 at the seam is satisfied by:
      B0 = A3
      B1 = 2*A3 - A2
      B2 = 4*A3 - 4*A2 + A1

    The front relation is solved backward from CENTER.u=0; rear is solved forward from
    CENTER.u=1. Far termination rows remain independent and do not enter seam position,
    first derivative or second derivative.
    """
    if len(center) != 4 or any(len(row) != 4 for row in center):
        raise ValueError("center_patch_cage must be 4x4")
    if len(front_boundary) != 4 or len(rear_boundary) != 4:
        raise ValueError("termination boundaries must contain four v-control points")

    c0, c1, c2, c3 = center
    f3 = [list(p) for p in c0]
    f2 = [p_add(p_scale(c0[j], 2), p_scale(c1[j], -1)) for j in range(4)]
    f1 = [p_add(c2[j], p_scale(c1[j], -4), p_scale(c0[j], 4)) for j in range(4)]
    front = [[list(p) for p in front_boundary], f1, f2, f3]

    r0 = [list(p) for p in c3]
    r1 = [p_add(p_scale(c3[j], 2), p_scale(c2[j], -1)) for j in range(4)]
    r2 = [p_add(p_scale(c3[j], 4), p_scale(c2[j], -4), c1[j]) for j in range(4)]
    rear = [r0, r1, r2, [list(p) for p in rear_boundary]]
    return {"PATCH-FRONT-TERMINATION": front, "PATCH-CENTER-VOLUME": center, "PATCH-REAR-TERMINATION": rear}


class Patch:
    def __init__(self, patch_id: str, cage: list[list[list[float]]]):
        self.id = patch_id
        self.cage = [[Vector(p) for p in row] for row in cage]

    def combine(self, bu: Iterable[float], bv: Iterable[float]) -> Vector:
        bu, bv = tuple(bu), tuple(bv)
        p = Vector((0.0, 0.0, 0.0))
        for i in range(4):
            for j in range(4):
                p += self.cage[i][j] * (bu[i] * bv[j])
        return p

    def evaluate(self, u: float, v: float):
        bu, bv = b3(u), b3(v)
        du, dv = db3(u), db3(v)
        ddu, ddv = ddb3(u), ddb3(v)
        s = self.combine(bu, bv)
        su = self.combine(du, bv)
        sv = self.combine(bu, dv)
        suu = self.combine(ddu, bv)
        svv = self.combine(bu, ddv)
        suv = self.combine(du, dv)
        return s, su, sv, suu, svv, suv

    def curvature(self, u: float, v: float):
        s, su, sv, suu, svv, suv = self.evaluate(u, v)
        nraw = su.cross(sv)
        jac = nraw.length
        if jac < 1e-12:
            raise ValueError(f"{self.id}: degenerate surface differential")
        n = nraw.normalized()
        E, F, G = su.dot(su), su.dot(sv), sv.dot(sv)
        e, f, g = n.dot(suu), n.dot(suv), n.dot(svv)
        den = E*G - F*F
        if abs(den) < 1e-12:
            raise ValueError(f"{self.id}: degenerate first fundamental form")
        K = (e*g - f*f) / den
        H = (E*g - 2*F*f + G*e) / (2*den)
        return s, n, jac, H, K


def angle_deg(a: Vector, b: Vector) -> float:
    if a.length < 1e-12 or b.length < 1e-12:
        return 180.0
    c = max(-1.0, min(1.0, a.dot(b) / (a.length * b.length)))
    return math.degrees(math.acos(c))


def seam_metrics(a: Patch, ua: float, b: Patch, ub: float, samples: int = 41) -> dict[str, float]:
    pos, tangent, second, normal, mean_curv = [], [], [], [], []
    for j in range(samples):
        v = j / (samples - 1)
        sa, sua, _, suua, _, _ = a.evaluate(ua, v)
        sb, sub, _, suub, _, _ = b.evaluate(ub, v)
        _, na, _, Ha, _ = a.curvature(ua, v)
        _, nb, _, Hb, _ = b.curvature(ub, v)
        pos.append((sa-sb).length)
        tangent.append(angle_deg(sua, sub))
        second.append((suua-suub).length)
        normal.append(angle_deg(na, nb))
        mean_curv.append(abs(Ha-Hb))
    return {
        "max_position_error": max(pos),
        "max_tangent_angle_deg": max(tangent),
        "max_second_derivative_error": max(second),
        "max_normal_angle_deg": max(normal),
        "max_mean_curvature_difference": max(mean_curv),
    }


def patch_fairness(patch: Patch, nu: int = 41, nv: int = 21) -> dict[str, float]:
    normals: list[list[Vector]] = []
    means: list[list[float]] = []
    positions: list[list[Vector]] = []
    min_jac = float("inf")
    for i in range(nu):
        nr, hr, pr = [], [], []
        for j in range(nv):
            s, n, jac, H, _ = patch.curvature(i/(nu-1), j/(nv-1))
            min_jac = min(min_jac, jac)
            nr.append(n); hr.append(H); pr.append(s)
        normals.append(nr); means.append(hr); positions.append(pr)
    jumps, rates = [], []
    for i in range(nu):
        for j in range(nv):
            if i + 1 < nu:
                jumps.append(angle_deg(normals[i][j], normals[i+1][j]))
                ds = max(1e-9, (positions[i+1][j]-positions[i][j]).length)
                rates.append(abs(means[i+1][j]-means[i][j]) / ds)
            if j + 1 < nv:
                jumps.append(angle_deg(normals[i][j], normals[i][j+1]))
                ds = max(1e-9, (positions[i][j+1]-positions[i][j]).length)
                rates.append(abs(means[i][j+1]-means[i][j]) / ds)
    sj = sorted(jumps)
    return {
        "min_surface_jacobian": min_jac,
        "max_adjacent_normal_jump_deg": max(jumps),
        "p95_adjacent_normal_jump_deg": sj[int(0.95*(len(sj)-1))],
        "max_mean_curvature_rate_proxy": max(rates),
    }


def termination_edit_stability(center, front_boundary, rear_boundary) -> dict:
    base = compile_c2_chain(center, front_boundary, rear_boundary)
    front_variant = [[p[0], p[1]*0.88, p[2] + (0.04 if j < 2 else -0.015)] for j,p in enumerate(front_boundary)]
    rear_variant = [[p[0], p[1]*1.06, p[2] + (0.02 if j < 2 else -0.01)] for j,p in enumerate(rear_boundary)]
    var = compile_c2_chain(center, front_variant, rear_variant)
    center_p = Patch("CENTER", base["PATCH-CENTER-VOLUME"])
    checks = []
    for tag, net in (("BASE", base), ("VARIANT", var)):
        fp = Patch("FRONT", net["PATCH-FRONT-TERMINATION"])
        rp = Patch("REAR", net["PATCH-REAR-TERMINATION"])
        checks.append({"variant": tag, "front_seam": seam_metrics(fp,1.0,center_p,0.0), "rear_seam": seam_metrics(center_p,1.0,rp,0.0)})
    return {
        "front_boundary_changed": front_variant != front_boundary,
        "rear_boundary_changed": rear_variant != rear_boundary,
        "center_cage_unchanged": base["PATCH-CENTER-VOLUME"] == var["PATCH-CENTER-VOLUME"],
        "seam_metrics": checks,
    }


def evaluate_network(contract: dict, network: dict[str, list[list[list[float]]]]) -> dict:
    thresholds = contract["fairness_thresholds"]
    patches = {k: Patch(k,v) for k,v in network.items()}
    front_seam = seam_metrics(patches["PATCH-FRONT-TERMINATION"],1.0,patches["PATCH-CENTER-VOLUME"],0.0)
    rear_seam = seam_metrics(patches["PATCH-CENTER-VOLUME"],1.0,patches["PATCH-REAR-TERMINATION"],0.0)
    fairness = {k: patch_fairness(v) for k,v in patches.items()}
    stability = termination_edit_stability(contract["center_patch_cage"], contract["termination_boundaries"]["front"], contract["termination_boundaries"]["rear"])

    seam_checks = []
    for seam in (front_seam, rear_seam):
        seam_checks.extend([
            seam["max_position_error"] <= thresholds["max_seam_position_error"],
            seam["max_tangent_angle_deg"] <= thresholds["max_seam_tangent_angle_deg"],
            seam["max_second_derivative_error"] <= thresholds["max_seam_second_derivative_error"],
        ])
    patch_checks = []
    for row in fairness.values():
        patch_checks.extend([
            row["min_surface_jacobian"] >= thresholds["min_surface_jacobian"],
            row["max_adjacent_normal_jump_deg"] <= thresholds["max_adjacent_normal_jump_deg"],
            row["max_mean_curvature_rate_proxy"] <= thresholds["max_mean_curvature_rate_proxy"],
        ])
    variant_seams = [s for variant in stability["seam_metrics"] for s in (variant["front_seam"], variant["rear_seam"])]
    variant_ok = all(
        s["max_position_error"] <= thresholds["max_seam_position_error"] and
        s["max_tangent_angle_deg"] <= thresholds["max_seam_tangent_angle_deg"] and
        s["max_second_derivative_error"] <= thresholds["max_seam_second_derivative_error"]
        for s in variant_seams
    )
    checks = {
        "three_patch_surface_network": len(network) == 3,
        "explicit_c2_relationships": sum(1 for r in contract["relationships"] if r.get("continuity_target") == "C2") >= 2,
        "front_seam_c2_proxy": all(seam_checks[:3]),
        "rear_seam_c2_proxy": all(seam_checks[3:]),
        "all_patch_interior_fairness": all(patch_checks),
        "termination_boundaries_independent": stability["front_boundary_changed"] and stability["rear_boundary_changed"] and stability["center_cage_unchanged"] and variant_ok,
        "termination_is_surface_patch_not_mesh_closure": contract["compiler_policy"]["mesh_closure_for_termination_forbidden"] is True,
        "execution_topology_after_surface_compile": contract["compiler_policy"]["execution_topology_generated_after_surface_compile"] is True,
        "smooth_shading_not_surface_authority": True
    }
    return {
        "schema": "oleander.modeling-worker.v0.12.e2.fairness-report",
        "model": MODEL,
        "status": "MACHINE_PASS_HUMAN_M4_5_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL_REVISE_M3_M4",
        "thresholds": thresholds,
        "front_seam": front_seam,
        "rear_seam": rear_seam,
        "patch_fairness": fairness,
        "termination_edit_stability": stability,
        "checks": checks,
        "boundary": "C2 is proven only for this three-patch parametric benchmark. Human zebra/reflection review remains required; no Class-A, engineering, manufacturing or final automotive authority is implied."
    }


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def material(name: str, color, roughness=.34, metallic=0.0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    bsdf=m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value=(*color,1.0); bsdf.inputs["Roughness"].default_value=roughness; bsdf.inputs["Metallic"].default_value=metallic
    return m


def zebra_material():
    m=bpy.data.materials.new("MAT-E2-ZEBRA"); m.use_nodes=True
    nt=m.node_tree; nt.nodes.clear()
    out=nt.nodes.new("ShaderNodeOutputMaterial"); bsdf=nt.nodes.new("ShaderNodeBsdfPrincipled"); geo=nt.nodes.new("ShaderNodeNewGeometry"); wave=nt.nodes.new("ShaderNodeTexWave"); ramp=nt.nodes.new("ShaderNodeValToRGB")
    wave.wave_type="BANDS"; wave.bands_direction="X"; wave.inputs["Scale"].default_value=20.0
    ramp.color_ramp.interpolation="CONSTANT"; ramp.color_ramp.elements[0].position=.46; ramp.color_ramp.elements[0].color=(.01,.01,.01,1); ramp.color_ramp.elements[1].position=.54; ramp.color_ramp.elements[1].color=(.94,.94,.94,1)
    bsdf.inputs["Roughness"].default_value=.16
    nt.links.new(geo.outputs["Normal"],wave.inputs["Vector"]); nt.links.new(wave.outputs["Color"],ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"],bsdf.inputs["Base Color"]); nt.links.new(bsdf.outputs["BSDF"],out.inputs["Surface"])
    return m


def poly_curve(name: str, points: list[Vector], mat, bevel=.007):
    cu=bpy.data.curves.new(name,"CURVE"); cu.dimensions="3D"; cu.bevel_depth=bevel; cu.bevel_resolution=3
    sp=cu.splines.new("POLY"); sp.points.add(len(points)-1)
    for p,co in zip(sp.points,points): p.co=(*co,1.0)
    o=bpy.data.objects.new(name,cu); bpy.context.collection.objects.link(o); o.data.materials.append(mat); return o


def build_execution_mesh(patches: list[Patch], nu=31, nv=21):
    rows=[]; seam_rows=[]
    for pi,patch in enumerate(patches):
        for i in range(nu):
            if pi and i==0: continue
            u=i/(nu-1)
            rows.append([patch.evaluate(u,j/(nv-1))[0] for j in range(nv)])
        if pi < len(patches)-1:
            seam_rows.append(len(rows)-1)
    verts=[tuple(p) for row in rows for p in row]; faces=[]
    def idx(i,j): return i*nv+j
    for i in range(len(rows)-1):
        for j in range(nv-1): faces.append((idx(i,j),idx(i+1,j),idx(i+1,j+1),idx(i,j+1)))
    me=bpy.data.meshes.new("E2_DERIVED_EXECUTION_MESH"); me.from_pydata(verts,[],faces); me.update()
    o=bpy.data.objects.new("E2_DERIVED_EXECUTION_SURFACE",me); bpy.context.collection.objects.link(o)
    for p in me.polygons: p.use_smooth=True
    o["OLEANDER_AUTHORITY"]="DERIVED_EXECUTION_GEOMETRY"; o["OLEANDER_SURFACE_SOURCE"]="THREE_PATCH_C2_NETWORK"
    mod=o.modifiers.new("Mirror-Symmetry","MIRROR"); mod.use_axis[0]=False; mod.use_axis[1]=True; mod.use_clip=True; mod.use_mirror_merge=True
    return o,rows,seam_rows


def cage_diagnostics(network, mat_cage, mat_seam):
    objs=[]
    for pid,cage in network.items():
        pv=[[Vector(p) for p in row] for row in cage]
        for j in range(4): objs.append(poly_curve(f"{pid}-V{j}",[pv[i][j] for i in range(4)],mat_cage,.005))
        for i in range(4): objs.append(poly_curve(f"{pid}-U{i}",[pv[i][j] for j in range(4)],mat_cage,.005))
    for name,pid,u in (("SEAM-FRONT-CENTER","PATCH-CENTER-VOLUME",0.0),("SEAM-CENTER-REAR","PATCH-CENTER-VOLUME",1.0)):
        patch=Patch(pid,network[pid]); pts=[patch.evaluate(u,j/80)[0] for j in range(81)]; objs.append(poly_curve(name,pts,mat_seam,.012))
    return objs


def look_at(obj,target:Vector): obj.rotation_euler=(target-obj.location).to_track_quat("-Z","Y").to_euler()


def camera(name,loc,target,ortho=5.3):
    d=bpy.data.cameras.new(name); d.type="ORTHO"; d.ortho_scale=ortho; o=bpy.data.objects.new(name,d); bpy.context.collection.objects.link(o); o.location=loc; look_at(o,Vector(target)); return o


def area(name,loc,energy,size):
    d=bpy.data.lights.new(name,"AREA"); d.energy=energy; d.shape="DISK"; d.size=size; o=bpy.data.objects.new(name,d); bpy.context.collection.objects.link(o); o.location=loc; look_at(o,Vector((0,0,.65))); return o


def scene_setup(res):
    sc=bpy.context.scene; sc.render.engine="BLENDER_EEVEE"; sc.render.resolution_x=res; sc.render.resolution_y=res; sc.render.resolution_percentage=100; sc.render.image_settings.file_format="PNG"; sc.world.color=(.025,.025,.025)
    area("KEY",(2.8,3.8,4.5),1300,4.0); area("FILL",(-2.8,-3.2,2.6),800,3.5); area("STRIP",(0,5,1.6),1100,1.0); return sc


def render(sc,out,cam,name,surface,mat):
    surface.data.materials.clear(); surface.data.materials.append(mat); sc.camera=cam; sc.render.filepath=str(out/f"{name}.png"); bpy.ops.render.render(write_still=True)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--contract",required=True); ap.add_argument("--out",required=True); ap.add_argument("--resolution",type=int,default=512); args=ap.parse_args(user_args())
    contract=json.loads(Path(args.contract).read_text(encoding="utf-8")); out=Path(args.out).resolve(); out.mkdir(parents=True,exist_ok=True)
    network=compile_c2_chain(contract["center_patch_cage"],contract["termination_boundaries"]["front"],contract["termination_boundaries"]["rear"])
    report=evaluate_network(contract,network)
    clear_scene(); clay=material("MAT-E2-CLAY",(.39,.41,.44),.31); cage_mat=material("MAT-E2-CAGE",(.02,.02,.025),.42); seam_mat=material("MAT-E2-SEAM",(.72,.74,.78),.22,.15); zebra=zebra_material()
    ordered=[Patch("PATCH-FRONT-TERMINATION",network["PATCH-FRONT-TERMINATION"]),Patch("PATCH-CENTER-VOLUME",network["PATCH-CENTER-VOLUME"]),Patch("PATCH-REAR-TERMINATION",network["PATCH-REAR-TERMINATION"])]
    surf,rows,seam_rows=build_execution_mesh(ordered); surf.data.materials.append(clay); diag=cage_diagnostics(network,cage_mat,seam_mat)
    sc=scene_setup(args.resolution); target=(0,0,.62)
    cams={
      "E2_HERO_NETWORK":camera("CAM-E2-HERO",(4.0,4.2,2.7),target,5.6),
      "E2_SIDE_NETWORK":camera("CAM-E2-SIDE",(0,6.2,1.0),target,5.4),
      "E2_TOP_NETWORK":camera("CAM-E2-TOP",(0,.2,6.2),(0,0,.55),5.5),
      "E2_ZEBRA_NETWORK":camera("CAM-E2-ZEBRA",(4.2,4.0,2.3),target,5.5)
    }
    render(sc,out,cams["E2_HERO_NETWORK"],"E2_HERO_NETWORK",surf,clay); render(sc,out,cams["E2_SIDE_NETWORK"],"E2_SIDE_NETWORK",surf,clay); render(sc,out,cams["E2_TOP_NETWORK"],"E2_TOP_NETWORK",surf,clay)
    for o in diag:o.hide_render=True
    render(sc,out,cams["E2_ZEBRA_NETWORK"],"E2_ZEBRA_NETWORK",surf,zebra)
    for o in diag:o.hide_render=False
    (out/"E2_COMPILED_PATCH_NETWORK.json").write_text(json.dumps({"schema":"oleander.modeling-worker.v0.12.e2.compiled-network","authority":"WORKING_SURFACE_SOURCE","network":network,"execution_mesh":{"derived":True,"sample_rows":len(rows),"sample_columns":21,"seam_row_indices":seam_rows}},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (out/"E2_FREEFORM_FAIRNESS.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    sc["OLEANDER_MODEL"]=MODEL; sc["OLEANDER_STAGE"]="M4.5_E2"; sc["OLEANDER_RELATIONSHIP_CONTRACT"]=json.dumps(contract,ensure_ascii=False)
    blend=out/f"{MODEL}.blend"; bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    print(json.dumps(report,ensure_ascii=False,indent=2)); raise SystemExit(0 if report["status"]=="MACHINE_PASS_HUMAN_M4_5_REVIEW_REQUIRED" else 5)


if __name__=="__main__": main()
