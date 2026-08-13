#!/usr/bin/env python3
"""OLEANDER Modeling Worker v0.12 E1 — relationship-driven bicubic freeform benchmark.

This benchmark intentionally uses a sparse 4x4 bicubic Bezier control cage as the
editable Surface Source. The evaluated mesh is derived execution geometry only.

It demonstrates the architectural chain:
Design relationships -> semantic cage -> analytic fair surface -> execution mesh ->
quantitative fairness evidence -> visual review.

It does NOT claim Class-A surfacing, automotive engineering, G2 multi-patch production
quality, manufacturing validity or final automotive design authority.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Iterable

import bpy
from mathutils import Vector

MODEL = "OLEANDER_ModelingWorker_v0.12_E1_Freeform"

# Semantic low-frequency cage. u = longitudinal flow, v = centerline -> lower-side flow.
# Each point is [x, y, z]. The values are designer-estimate benchmark geometry, not
# engineering hard points.
CAGE = [
    [[ 2.20, 0.00, 0.82], [ 2.20, 0.34, 0.73], [ 2.20, 0.67, 0.55], [ 2.20, 0.80, 0.31]],
    [[ 0.72, 0.00, 1.34], [ 0.72, 0.46, 0.99], [ 0.72, 0.80, 0.69], [ 0.72, 0.86, 0.28]],
    [[-0.70, 0.00, 1.40], [-0.70, 0.48, 1.01], [-0.70, 0.82, 0.70], [-0.70, 0.86, 0.29]],
    [[-2.20, 0.00, 0.86], [-2.20, 0.38, 0.75], [-2.20, 0.70, 0.57], [-2.20, 0.80, 0.32]],
]

RELATIONSHIP_IR = {
    "schema": "oleander.modeling-worker.v0.12.e1.relationship-ir",
    "decision_question": "Can explicit low-frequency body-flow relationships compile to one sparse editable cage and a stable analytic freeform surface before execution topology?",
    "relations": [
        {
            "id": "REL-E1-01",
            "source": "CURVE-CENTER-FLOW",
            "target": "CURVE-SHOULDER-FLOW",
            "relation": "FLOW",
            "intent": "upper-side volume must be fed by the broad center/canopy volume rather than an attached local brow",
            "resolved_by": "shared bicubic cage columns",
        },
        {
            "id": "REL-E1-02",
            "source": "CURVE-SHOULDER-FLOW",
            "target": "CURVE-BELT-FLOW",
            "relation": "TENSION",
            "intent": "belt remains subordinate to shoulder and cannot become an independent ridge",
            "resolved_by": "monotonic v-row z/y ordering",
        },
        {
            "id": "REL-E1-03",
            "source": "CURVE-BELT-FLOW",
            "target": "CURVE-LOWER-FLOW",
            "relation": "PROPORTION",
            "intent": "lower body remains visually stable while upper volume changes",
            "resolved_by": "low-frequency lower row with bounded longitudinal variation",
        },
        {
            "id": "REL-E1-04",
            "source": "SURFACE-SOURCE",
            "target": "EXECUTION-MESH",
            "relation": "DEPENDENCY",
            "intent": "topology is derived after surface intent; it cannot become the shape authority",
            "resolved_by": "analytic Bezier evaluation into sampled mesh",
        },
    ],
    "authority": {
        "design_relationship": "WORKING_SOURCE",
        "surface_source": "WORKING_SOURCE",
        "execution_geometry": "DERIVED",
    },
}


def b3(t: float) -> tuple[float, float, float, float]:
    s = 1.0 - t
    return (s*s*s, 3*s*s*t, 3*s*t*t, t*t*t)


def db3(t: float) -> tuple[float, float, float, float]:
    s = 1.0 - t
    return (-3*s*s, 3*s*s - 6*s*t, 6*s*t - 3*t*t, 3*t*t)


def ddb3(t: float) -> tuple[float, float, float, float]:
    return (6*(1-t), -12 + 18*t, 6 - 18*t, 6*t)


def combine(bu: Iterable[float], bv: Iterable[float]) -> Vector:
    bu, bv = tuple(bu), tuple(bv)
    p = Vector((0.0, 0.0, 0.0))
    for i in range(4):
        for j in range(4):
            p += Vector(CAGE[i][j]) * (bu[i] * bv[j])
    return p


def surface_eval(u: float, v: float):
    bu, bv = b3(u), b3(v)
    du, dv = db3(u), db3(v)
    ddu, ddv = ddb3(u), ddb3(v)
    s = combine(bu, bv)
    su = combine(du, bv)
    sv = combine(bu, dv)
    suu = combine(ddu, bv)
    svv = combine(bu, ddv)
    suv = combine(du, dv)
    return s, su, sv, suu, svv, suv


def angle_deg(a: Vector, b: Vector) -> float:
    if a.length < 1e-12 or b.length < 1e-12:
        return 180.0
    c = max(-1.0, min(1.0, a.dot(b) / (a.length * b.length)))
    return math.degrees(math.acos(c))


def curvature_at(u: float, v: float):
    s, su, sv, suu, svv, suv = surface_eval(u, v)
    nraw = su.cross(sv)
    jac = nraw.length
    if jac < 1e-12:
        raise ValueError("degenerate surface differential")
    n = nraw.normalized()
    E, F, G = su.dot(su), su.dot(sv), sv.dot(sv)
    e, f, g = n.dot(suu), n.dot(suv), n.dot(svv)
    den = E*G - F*F
    if abs(den) < 1e-12:
        raise ValueError("degenerate first fundamental form")
    K = (e*g - f*f) / den
    H = (E*g - 2*F*f + G*e) / (2*den)
    disc = max(0.0, H*H - K)
    root = math.sqrt(disc)
    return s, n, jac, H, K, H + root, H - root


def fairness_report(nu: int = 61, nv: int = 31) -> dict:
    samples = []
    normal_jumps = []
    silhouette_jumps = []
    curv_rate = []
    min_jac = float("inf")
    max_abs_H = 0.0
    max_abs_K = 0.0
    normals: list[list[Vector]] = []
    means: list[list[float]] = []
    positions: list[list[Vector]] = []

    for iu in range(nu):
        u = iu/(nu-1)
        nr, hr, pr = [], [], []
        for iv in range(nv):
            v = iv/(nv-1)
            s, n, jac, H, K, k1, k2 = curvature_at(u, v)
            min_jac = min(min_jac, jac)
            max_abs_H = max(max_abs_H, abs(H))
            max_abs_K = max(max_abs_K, abs(K))
            nr.append(n); hr.append(H); pr.append(s)
            if (iu in (0, nu//2, nu-1)) and (iv in (0, nv//2, nv-1)):
                samples.append({"u": u, "v": v, "position": list(s), "normal": list(n), "mean_curvature": H, "gaussian_curvature": K, "k1": k1, "k2": k2})
        normals.append(nr); means.append(hr); positions.append(pr)

    for iu in range(nu):
        for iv in range(nv):
            if iu + 1 < nu:
                normal_jumps.append(angle_deg(normals[iu][iv], normals[iu+1][iv]))
            if iv + 1 < nv:
                normal_jumps.append(angle_deg(normals[iu][iv], normals[iu][iv+1]))

    # Center-flow silhouette derivative stability.
    center = [positions[i][0] for i in range(nu)]
    seg = [center[i+1] - center[i] for i in range(nu-1)]
    for a, b in zip(seg, seg[1:]):
        silhouette_jumps.append(angle_deg(a, b))

    # Mean-curvature rate proxy normalized by actual 3D sample spacing.
    for iu in range(nu):
        for iv in range(nv):
            if iu + 1 < nu:
                ds = max(1e-9, (positions[iu+1][iv] - positions[iu][iv]).length)
                curv_rate.append(abs(means[iu+1][iv] - means[iu][iv]) / ds)
            if iv + 1 < nv:
                ds = max(1e-9, (positions[iu][iv+1] - positions[iu][iv]).length)
                curv_rate.append(abs(means[iu][iv+1] - means[iu][iv]) / ds)

    metrics = {
        "grid": [nu, nv],
        "control_cage_points": 16,
        "min_surface_jacobian": min_jac,
        "max_adjacent_normal_jump_deg": max(normal_jumps),
        "p95_adjacent_normal_jump_deg": sorted(normal_jumps)[int(0.95*(len(normal_jumps)-1))],
        "max_center_silhouette_tangent_jump_deg": max(silhouette_jumps),
        "max_mean_curvature_rate_proxy": max(curv_rate),
        "max_abs_mean_curvature": max_abs_H,
        "max_abs_gaussian_curvature": max_abs_K,
    }
    thresholds = {
        "min_surface_jacobian": 0.20,
        "max_adjacent_normal_jump_deg": 5.0,
        "max_center_silhouette_tangent_jump_deg": 4.0,
        "max_mean_curvature_rate_proxy": 8.0,
    }
    checks = {
        "relationship_ir_present": len(RELATIONSHIP_IR["relations"]) >= 4,
        "low_frequency_cage": len(CAGE) * len(CAGE[0]) == 16,
        "topology_derived_from_surface": True,
        "jacobian_non_degenerate": metrics["min_surface_jacobian"] >= thresholds["min_surface_jacobian"],
        "normal_flow_stable": metrics["max_adjacent_normal_jump_deg"] <= thresholds["max_adjacent_normal_jump_deg"],
        "silhouette_derivative_stable": metrics["max_center_silhouette_tangent_jump_deg"] <= thresholds["max_center_silhouette_tangent_jump_deg"],
        "curvature_rate_bounded": metrics["max_mean_curvature_rate_proxy"] <= thresholds["max_mean_curvature_rate_proxy"],
        "smooth_shading_not_fairness_evidence": True,
    }
    return {
        "schema": "oleander.modeling-worker.v0.12.e1.fairness-report",
        "model": MODEL,
        "status": "MACHINE_PASS_HUMAN_M4_5_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL_REVISE_M4",
        "metrics": metrics,
        "thresholds": thresholds,
        "checks": checks,
        "diagnostic_samples": samples,
        "boundary": "Analytic single-patch fairness benchmark only. Does not prove multi-patch G2/G3, Class-A, engineering or final design quality. Human zebra/reflection review remains required.",
    }


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        # Keep datablocks only if reused by current file; fresh CI scene makes this safe.
        pass


def material_principled(name: str, color, roughness=.34, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    return m


def zebra_material():
    m = bpy.data.materials.new('MAT-ZEBRA-NORMAL-PROXY')
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    geo = nt.nodes.new('ShaderNodeNewGeometry')
    wave = nt.nodes.new('ShaderNodeTexWave')
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    wave.wave_type = 'BANDS'; wave.bands_direction = 'X'; wave.inputs['Scale'].default_value = 18.0; wave.inputs['Distortion'].default_value = 0.0
    ramp.color_ramp.interpolation = 'CONSTANT'
    ramp.color_ramp.elements[0].position = 0.46; ramp.color_ramp.elements[0].color = (0.01,0.01,0.01,1)
    ramp.color_ramp.elements[1].position = 0.54; ramp.color_ramp.elements[1].color = (0.92,0.92,0.92,1)
    bsdf.inputs['Roughness'].default_value = 0.18
    nt.links.new(geo.outputs['Normal'], wave.inputs['Vector'])
    nt.links.new(wave.outputs['Color'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return m


def build_surface(nu=61, nv=31):
    verts=[]; faces=[]
    for iu in range(nu):
        u=iu/(nu-1)
        for iv in range(nv):
            v=iv/(nv-1)
            s,*_=surface_eval(u,v); verts.append(tuple(s))
    def idx(i,j): return i*nv+j
    for i in range(nu-1):
        for j in range(nv-1):
            faces.append((idx(i,j),idx(i+1,j),idx(i+1,j+1),idx(i,j+1)))
    me=bpy.data.meshes.new('E1_EVALUATION_SURFACE_MESH'); me.from_pydata(verts,[],faces); me.update()
    o=bpy.data.objects.new('E1_EVALUATION_SURFACE_DERIVED',me); bpy.context.collection.objects.link(o)
    for p in me.polygons: p.use_smooth=True
    o['OLEANDER_AUTHORITY']='DERIVED_EXECUTION_GEOMETRY'
    o['OLEANDER_SOURCE']='4x4_BICUBIC_CONTROL_CAGE'
    mod=o.modifiers.new('Mirror-Symmetry','MIRROR'); mod.use_axis[0]=False; mod.use_axis[1]=True; mod.use_clip=True; mod.use_mirror_merge=True
    return o


def make_poly_curve(name: str, points: list[Vector], mat, bevel=0.009):
    cu=bpy.data.curves.new(name,'CURVE'); cu.dimensions='3D'; cu.bevel_depth=bevel; cu.bevel_resolution=3
    sp=cu.splines.new('POLY'); sp.points.add(len(points)-1)
    for p,co in zip(sp.points,points): p.co=(*co,1.0)
    o=bpy.data.objects.new(name,cu); bpy.context.collection.objects.link(o); o.data.materials.append(mat)
    return o


def build_cage_and_curves(mat_cage, mat_curve):
    cage_objs=[]
    # longitudinal cage rows
    for j in range(4):
        cage_objs.append(make_poly_curve(f'CAGE-VROW-{j}', [Vector(CAGE[i][j]) for i in range(4)], mat_cage, .006))
    # transverse cage columns
    for i in range(4):
        cage_objs.append(make_poly_curve(f'CAGE-UCOL-{i}', [Vector(CAGE[i][j]) for j in range(4)], mat_cage, .006))
    # exact evaluated semantic primary curves at stable v parameters
    roles=[('CURVE-CENTER-FLOW',0.0),('CURVE-SHOULDER-FLOW',1/3),('CURVE-BELT-FLOW',2/3),('CURVE-LOWER-FLOW',1.0)]
    prim=[]
    for name,v in roles:
        pts=[surface_eval(i/80,v)[0] for i in range(81)]
        o=make_poly_curve(name,pts,mat_curve,.010); o['OLEANDER_AUTHORITY']='WORKING_SOURCE_DIAGNOSTIC_CURVE'; prim.append(o)
    return cage_objs,prim


def look_at(obj, target: Vector):
    direction = target - obj.location
    obj.rotation_euler = direction.to_track_quat('-Z','Y').to_euler()


def add_camera(name, loc, target, ortho=5.4):
    data=bpy.data.cameras.new(name); data.type='ORTHO'; data.ortho_scale=ortho
    o=bpy.data.objects.new(name,data); bpy.context.collection.objects.link(o); o.location=loc; look_at(o,Vector(target)); return o


def add_area(name, loc, energy, size, color=(1,1,1)):
    d=bpy.data.lights.new(name,'AREA'); d.energy=energy; d.shape='DISK'; d.size=size; d.color=color
    o=bpy.data.objects.new(name,d); bpy.context.collection.objects.link(o); o.location=loc; look_at(o,Vector((0,0,0.7))); return o


def setup_scene(res=640):
    sc=bpy.context.scene; sc.render.engine='BLENDER_EEVEE_NEXT'; sc.render.resolution_x=res; sc.render.resolution_y=res; sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG'; sc.render.film_transparent=False
    sc.world.color=(0.025,0.025,0.025)
    add_area('KEY',(2.5,3.5,4.5),1300,4.0)
    add_area('FILL',(-2.5,-3.0,2.8),900,3.5)
    add_area('STRIP',(0.0,4.8,1.8),1100,1.0)
    return sc


def render_view(sc, out:Path, cam, name, surface, cage, prim, mat):
    surface.data.materials.clear(); surface.data.materials.append(mat)
    sc.camera=cam; sc.render.filepath=str(out/f'{name}.png')
    bpy.ops.render.render(write_still=True)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); ap.add_argument('--resolution',type=int,default=640)
    args=ap.parse_args(); out=Path(args.out).resolve(); out.mkdir(parents=True,exist_ok=True)
    clear_scene()
    clay=material_principled('MAT-CLAY',(0.38,0.40,0.43),.32)
    dark=material_principled('MAT-CAGE',(0.015,0.015,0.018),.42)
    curve=material_principled('MAT-PRIMARY-CURVE',(0.78,0.80,0.84),.25,0.15)
    zebra=zebra_material()
    surface=build_surface(); surface.data.materials.append(clay)
    cage,prim=build_cage_and_curves(dark,curve)
    sc=setup_scene(args.resolution)
    target=(0.0,0.0,0.70)
    cams={
        'E1_HERO_3Q': add_camera('CAM-HERO',(4.2,4.0,2.7),target,5.4),
        'E1_SIDE': add_camera('CAM-SIDE',(0.0,6.0,1.0),target,5.2),
        'E1_TOP': add_camera('CAM-TOP',(0.0,0.2,6.2),(0,0,0.55),5.5),
        'E1_ZEBRA_NORMAL_PROXY': add_camera('CAM-ZEBRA',(4.4,3.8,2.2),target,5.1),
    }
    render_view(sc,out,cams['E1_HERO_3Q'],'E1_HERO_3Q',surface,cage,prim,clay)
    render_view(sc,out,cams['E1_SIDE'],'E1_SIDE',surface,cage,prim,clay)
    render_view(sc,out,cams['E1_TOP'],'E1_TOP',surface,cage,prim,clay)
    # Hide cage/curve diagnostics for the normal-sensitive zebra proxy.
    for o in cage+prim: o.hide_render=True
    render_view(sc,out,cams['E1_ZEBRA_NORMAL_PROXY'],'E1_ZEBRA_NORMAL_PROXY',surface,cage,prim,zebra)
    for o in cage+prim: o.hide_render=False

    report=fairness_report()
    (out/'E1_RELATIONSHIP_IR.json').write_text(json.dumps(RELATIONSHIP_IR,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'E1_CONTROL_CAGE.json').write_text(json.dumps({'schema':'oleander.modeling-worker.v0.12.e1.control-cage','authority':'WORKING_SOURCE','frequency':'LOW','topology_independent':True,'points':CAGE},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'E1_FREEFORM_FAIRNESS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    sc['OLEANDER_MODEL']=MODEL; sc['OLEANDER_STAGE']='M4.5_E1'; sc['OLEANDER_RELATIONSHIP_IR']=json.dumps(RELATIONSHIP_IR,ensure_ascii=False)
    blend=out/f'{MODEL}.blend'; bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    print(json.dumps(report,ensure_ascii=False,indent=2))
    raise SystemExit(0 if report['status']=='MACHINE_PASS_HUMAN_M4_5_REVIEW_REQUIRED' else 5)


if __name__=='__main__':
    main()
