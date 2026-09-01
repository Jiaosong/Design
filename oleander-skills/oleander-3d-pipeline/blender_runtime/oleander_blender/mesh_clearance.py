"""OLEANDER evaluated-mesh surface clearance.

Computes Euclidean minimum distance between evaluated, triangulated Blender mesh
surfaces. Modifiers and object transforms are included via the dependency graph.
This is authoritative only for the evaluated polygonal mesh result; it does not
claim analytic CAD/B-Rep clearance, engineering fit approval or manufacturing
release.
"""

from __future__ import annotations

import json

import bpy
from mathutils import Vector

from .dependency import object_id
from .measurement_system import mm_to_scene_units, scene_units_to_mm

TRUE_MESH_CLEARANCE_KEY = "oleander_true_mesh_clearance"


def _closest_point_triangle(point, a, b, c):
    """Closest point on triangle using Ericson's region tests."""
    point = Vector(point)
    a = Vector(a)
    b = Vector(b)
    c = Vector(c)
    ab = b - a
    ac = c - a
    ap = point - a
    d1 = ab.dot(ap)
    d2 = ac.dot(ap)
    if d1 <= 0.0 and d2 <= 0.0:
        return a.copy()

    bp = point - b
    d3 = ab.dot(bp)
    d4 = ac.dot(bp)
    if d3 >= 0.0 and d4 <= d3:
        return b.copy()

    vc = d1 * d4 - d3 * d2
    if vc <= 0.0 and d1 >= 0.0 and d3 <= 0.0:
        v = d1 / (d1 - d3)
        return a + ab * v

    cp = point - c
    d5 = ab.dot(cp)
    d6 = ac.dot(cp)
    if d6 >= 0.0 and d5 <= d6:
        return c.copy()

    vb = d5 * d2 - d1 * d6
    if vb <= 0.0 and d2 >= 0.0 and d6 <= 0.0:
        w = d2 / (d2 - d6)
        return a + ac * w

    va = d3 * d6 - d5 * d4
    if va <= 0.0 and (d4 - d3) >= 0.0 and (d5 - d6) >= 0.0:
        w = (d4 - d3) / ((d4 - d3) + (d5 - d6))
        return b + (c - b) * w

    denom = va + vb + vc
    if abs(denom) <= 1e-20:
        # Degenerate triangle fallback: caller also checks edge-edge distances.
        candidates = (a, b, c)
        return min(candidates, key=lambda item: (point - item).length_squared).copy()
    inv = 1.0 / denom
    v = vb * inv
    w = vc * inv
    return a + ab * v + ac * w


def _closest_segment_segment(p1, q1, p2, q2):
    """Return closest points on two finite 3D segments."""
    p1 = Vector(p1)
    q1 = Vector(q1)
    p2 = Vector(p2)
    q2 = Vector(q2)
    d1 = q1 - p1
    d2 = q2 - p2
    r = p1 - p2
    a = d1.dot(d1)
    e = d2.dot(d2)
    eps = 1e-20

    if a <= eps and e <= eps:
        return p1.copy(), p2.copy()
    if a <= eps:
        s = 0.0
        t = max(0.0, min(1.0, d2.dot(r) / e))
    else:
        c = d1.dot(r)
        if e <= eps:
            t = 0.0
            s = max(0.0, min(1.0, -c / a))
        else:
            b = d1.dot(d2)
            f = d2.dot(r)
            denom = a * e - b * b
            s = 0.0 if abs(denom) <= eps else max(0.0, min(1.0, (b * f - c * e) / denom))
            t = (b * s + f) / e
            if t < 0.0:
                t = 0.0
                s = max(0.0, min(1.0, -c / a))
            elif t > 1.0:
                t = 1.0
                s = max(0.0, min(1.0, (b - c) / a))
    return p1 + d1 * s, p2 + d2 * t


def _triangle_triangle_closest(tri_a, tri_b):
    """Exact closest pair for two polygonal triangles, including edge-edge minima."""
    best_a = None
    best_b = None
    best_sq = None

    def consider(pa, pb):
        nonlocal best_a, best_b, best_sq
        dist_sq = (pa - pb).length_squared
        if best_sq is None or dist_sq < best_sq:
            best_sq = dist_sq
            best_a = pa.copy()
            best_b = pb.copy()

    a0, a1, a2 = tri_a
    b0, b1, b2 = tri_b
    for point in tri_a:
        closest = _closest_point_triangle(point, b0, b1, b2)
        consider(point, closest)
    for point in tri_b:
        closest = _closest_point_triangle(point, a0, a1, a2)
        consider(closest, point)

    edges_a = ((a0, a1), (a1, a2), (a2, a0))
    edges_b = ((b0, b1), (b1, b2), (b2, b0))
    for ea0, ea1 in edges_a:
        for eb0, eb1 in edges_b:
            pa, pb = _closest_segment_segment(ea0, ea1, eb0, eb1)
            consider(pa, pb)
    return best_sq, best_a, best_b


def evaluated_mesh_triangles(obj, depsgraph, max_triangles=20000):
    if obj.type != "MESH":
        raise ValueError("surface clearance requires mesh objects")
    max_triangles = int(max_triangles)
    if max_triangles < 1:
        raise ValueError("max_triangles must be positive")
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    if mesh is None:
        raise ValueError("evaluated object did not produce a mesh")
    try:
        mesh.calc_loop_triangles()
        count = len(mesh.loop_triangles)
        if count < 1:
            raise ValueError("evaluated mesh has no triangles")
        if count > max_triangles:
            raise ValueError(f"evaluated mesh triangle count exceeds {max_triangles}")
        matrix = evaluated.matrix_world.copy()
        triangles = []
        for item in mesh.loop_triangles:
            triangles.append(tuple(matrix @ mesh.vertices[index].co for index in item.vertices))
        return triangles
    finally:
        evaluated.to_mesh_clear()


def true_mesh_surface_clearance(scene, obj_a, obj_b, depsgraph=None, max_triangles=20000, max_pair_tests=2000000, zero_tolerance_mm=1e-6):
    """Minimum Euclidean distance between two evaluated triangulated mesh surfaces."""
    if obj_a is obj_b:
        raise ValueError("surface clearance requires two different objects")
    max_pair_tests = int(max_pair_tests)
    if max_pair_tests < 1:
        raise ValueError("max_pair_tests must be positive")
    zero_tolerance_mm = float(zero_tolerance_mm)
    if zero_tolerance_mm < 0.0:
        raise ValueError("zero tolerance must be non-negative")
    depsgraph = depsgraph or bpy.context.evaluated_depsgraph_get()
    tris_a = evaluated_mesh_triangles(obj_a, depsgraph, max_triangles=max_triangles)
    tris_b = evaluated_mesh_triangles(obj_b, depsgraph, max_triangles=max_triangles)
    pair_count = len(tris_a) * len(tris_b)
    if pair_count > max_pair_tests:
        raise ValueError(f"triangle pair count exceeds {max_pair_tests}")

    best_sq = None
    best_a = None
    best_b = None
    best_pair = None
    zero_scene = mm_to_scene_units(scene, zero_tolerance_mm)
    zero_sq = zero_scene * zero_scene

    for index_a, tri_a in enumerate(tris_a):
        for index_b, tri_b in enumerate(tris_b):
            dist_sq, point_a, point_b = _triangle_triangle_closest(tri_a, tri_b)
            if best_sq is None or dist_sq < best_sq:
                best_sq = dist_sq
                best_a = point_a
                best_b = point_b
                best_pair = (index_a, index_b)
            if best_sq is not None and best_sq <= zero_sq:
                break
        if best_sq is not None and best_sq <= zero_sq:
            break

    distance_scene = best_sq ** 0.5
    distance_mm = scene_units_to_mm(scene, distance_scene)
    intersects = distance_scene <= zero_scene
    result = {
        "schema": "OLEANDER_TRUE_MESH_CLEARANCE_v0.1",
        "a": object_id(obj_a) or obj_a.name,
        "b": object_id(obj_b) or obj_b.name,
        "surface_distance_mm": 0.0 if intersects else distance_mm,
        "intersecting_or_touching": intersects,
        "witness_a_world_scene": [float(v) for v in best_a],
        "witness_b_world_scene": [float(v) for v in best_b],
        "witness_a_world_mm": [scene_units_to_mm(scene, v) for v in best_a],
        "witness_b_world_mm": [scene_units_to_mm(scene, v) for v in best_b],
        "triangle_pair": list(best_pair),
        "triangle_count_a": len(tris_a),
        "triangle_count_b": len(tris_b),
        "triangle_pair_budget": max_pair_tests,
        "zero_tolerance_mm": zero_tolerance_mm,
        "geometry_source": "DEPSGRAPH_EVALUATED_TRIANGULATED_MESH",
        "authority": "EVALUATED_MESH_SURFACE_DISTANCE_NOT_ANALYTIC_CAD_BREP",
        "non_claims": ["analytic_cad_brep_clearance", "engineering_fit_approval", "manufacturing_release"],
    }
    scene[TRUE_MESH_CLEARANCE_KEY] = json.dumps(result, sort_keys=True)
    return result


class OLEANDER_OT_true_mesh_clearance(bpy.types.Operator):
    bl_idname = "oleander.true_mesh_clearance"
    bl_label = "Evaluated Mesh Clearance"
    bl_options = {"REGISTER"}

    max_pair_tests: bpy.props.IntProperty(name="Max triangle pairs", default=2000000, min=1)

    def execute(self, context):
        selected = [obj for obj in context.selected_objects if obj.type == "MESH"]
        if len(selected) != 2:
            self.report({"ERROR"}, "select exactly two mesh objects")
            return {"CANCELLED"}
        try:
            result = true_mesh_surface_clearance(
                context.scene,
                selected[0],
                selected[1],
                depsgraph=context.evaluated_depsgraph_get(),
                max_pair_tests=self.max_pair_tests,
            )
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Evaluated mesh clearance: {result['surface_distance_mm']:.6f} mm")
        return {"FINISHED"}


class OLEANDER_PT_mesh_clearance(bpy.types.Panel):
    bl_label = "Mesh Surface Clearance"
    bl_idname = "OLEANDER_PT_mesh_clearance"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OLEANDER"
    bl_parent_id = "OLEANDER_PT_runtime_panel"

    def draw(self, context):
        layout = self.layout
        layout.operator("oleander.true_mesh_clearance", text="Measure Evaluated Mesh Clearance")
        layout.label(text="Includes modifiers + world transforms", icon="INFO")
        layout.label(text="Polygonal mesh distance; not analytic CAD/B-Rep", icon="INFO")


OPERATOR_CLASSES = (OLEANDER_OT_true_mesh_clearance,)
PANEL_CLASSES = (OLEANDER_PT_mesh_clearance,)
