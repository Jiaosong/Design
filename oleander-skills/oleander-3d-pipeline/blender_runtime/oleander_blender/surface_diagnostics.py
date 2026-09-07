"""OLEANDER evaluated-mesh surface diagnostic foundation.

The diagnostics in this module operate on Blender dependency-graph evaluated,
triangulated polygon meshes. They are intended to expose change quality and
surface/interface risks before hero rendering. They do not claim Class-A
continuity, analytic CAD/B-Rep curvature, moldability, engineering wall
thickness, manufacturing release or field truth.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

from .dependency import object_id
from .measurement_system import mm_to_scene_units, scene_units_to_mm

SURFACE_DIAGNOSTICS_KEY = "oleander_surface_diagnostics"


def _clamp(value, low=-1.0, high=1.0):
    return max(low, min(high, float(value)))


def _percentile(values, fraction):
    if not values:
        return None
    ordered = sorted(float(value) for value in values)
    if len(ordered) == 1:
        return ordered[0]
    position = _clamp(fraction, 0.0, 1.0) * (len(ordered) - 1)
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def _axis_vector(axis):
    if isinstance(axis, str):
        key = axis.strip().upper()
        mapping = {
            "X": Vector((1.0, 0.0, 0.0)),
            "Y": Vector((0.0, 1.0, 0.0)),
            "Z": Vector((0.0, 0.0, 1.0)),
            "-X": Vector((-1.0, 0.0, 0.0)),
            "-Y": Vector((0.0, -1.0, 0.0)),
            "-Z": Vector((0.0, 0.0, -1.0)),
        }
        if key not in mapping:
            raise ValueError("pull axis must be X, Y, Z, -X, -Y or -Z")
        return mapping[key]
    vector = Vector(axis)
    if vector.length <= 1e-12:
        raise ValueError("pull axis must be non-zero")
    return vector.normalized()


def evaluated_surface_data(obj, depsgraph=None, max_triangles=50000):
    """Return world-space evaluated triangulated mesh data and topology counts."""
    if obj.type != "MESH":
        raise ValueError("surface diagnostics require a mesh object")
    max_triangles = int(max_triangles)
    if max_triangles < 1:
        raise ValueError("max_triangles must be positive")

    depsgraph = depsgraph or bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    if mesh is None:
        raise ValueError("evaluated object did not produce a mesh")
    try:
        mesh.calc_loop_triangles()
        triangle_count = len(mesh.loop_triangles)
        if triangle_count < 1:
            raise ValueError("evaluated mesh has no triangles")
        if triangle_count > max_triangles:
            raise ValueError(f"evaluated mesh triangle count exceeds {max_triangles}")

        matrix = evaluated.matrix_world.copy()
        vertices = [matrix @ vertex.co for vertex in mesh.vertices]
        triangles = [tuple(int(index) for index in tri.vertices) for tri in mesh.loop_triangles]

        normals = []
        centers = []
        areas = []
        signed_volume = 0.0
        degenerate_triangles = 0
        for indices in triangles:
            a, b, c = (vertices[index] for index in indices)
            cross = (b - a).cross(c - a)
            double_area = cross.length
            if double_area <= 1e-18:
                degenerate_triangles += 1
                normals.append(Vector((0.0, 0.0, 0.0)))
            else:
                normals.append(cross / double_area)
            centers.append((a + b + c) / 3.0)
            areas.append(0.5 * double_area)
            signed_volume += a.dot(b.cross(c)) / 6.0

        edge_counts = Counter()
        edge_faces = defaultdict(list)
        for face_index, indices in enumerate(triangles):
            a, b, c = indices
            for left, right in ((a, b), (b, c), (c, a)):
                edge = (left, right) if left < right else (right, left)
                edge_counts[edge] += 1
                edge_faces[edge].append(face_index)

        boundary_edges = sum(1 for count in edge_counts.values() if count == 1)
        nonmanifold_edges = sum(1 for count in edge_counts.values() if count != 2)
        closed_two_manifold = bool(edge_counts) and nonmanifold_edges == 0

        orientation = "POSITIVE" if signed_volume > 1e-12 else "NEGATIVE" if signed_volume < -1e-12 else "UNRESOLVED"
        if orientation == "NEGATIVE":
            normals = [-normal for normal in normals]
            signed_volume = -signed_volume

        return {
            "object": object_id(obj) or obj.name,
            "geometry_source": "DEPSGRAPH_EVALUATED_TRIANGULATED_MESH",
            "vertices": vertices,
            "triangles": triangles,
            "triangle_normals": normals,
            "triangle_centers": centers,
            "triangle_areas": areas,
            "edge_counts": dict(edge_counts),
            "edge_faces": dict(edge_faces),
            "triangle_count": triangle_count,
            "vertex_count": len(vertices),
            "edge_count": len(edge_counts),
            "boundary_edge_count": boundary_edges,
            "nonmanifold_edge_count": nonmanifold_edges,
            "closed_two_manifold": closed_two_manifold,
            "degenerate_triangle_count": degenerate_triangles,
            "orientation": orientation,
            "signed_volume_scene3": float(signed_volume),
        }
    finally:
        evaluated.to_mesh_clear()


def dihedral_report(surface, hard_edge_threshold_deg=30.0):
    threshold = float(hard_edge_threshold_deg)
    if not (0.0 <= threshold <= 180.0):
        raise ValueError("hard edge threshold must be between 0 and 180 degrees")

    values = []
    hard = 0
    normals = surface["triangle_normals"]
    for edge, faces in surface["edge_faces"].items():
        if len(faces) != 2:
            continue
        n0 = normals[faces[0]]
        n1 = normals[faces[1]]
        if n0.length <= 1e-12 or n1.length <= 1e-12:
            continue
        angle = math.degrees(math.acos(_clamp(n0.dot(n1))))
        values.append(angle)
        if angle >= threshold:
            hard += 1

    return {
        "schema": "OLEANDER_MESH_DIHEDRAL_DIAGNOSTIC_v0.1",
        "sampled_shared_edges": len(values),
        "hard_edge_threshold_deg": threshold,
        "hard_edge_count": hard,
        "min_deg": min(values) if values else None,
        "max_deg": max(values) if values else None,
        "mean_deg": (sum(values) / len(values)) if values else None,
        "p95_deg": _percentile(values, 0.95),
        "authority": "TRIANGULATED_MESH_NORMAL_VARIATION_NOT_CLASS_A_CURVATURE",
        "non_claims": ["class_a_continuity", "analytic_curvature", "nurbs_fairness"],
    }


def pull_axis_orientation_report(surface, pull_axis="Z", minimum_draft_deg=2.0):
    """Report triangle normal orientation relative to a pull axis.

    `wall_draft_deg` is |90° - angle(normal, pull_axis)|. It is a polygonal
    orientation diagnostic only; it does not solve visibility/occlusion and
    therefore does not certify undercuts or moldability.
    """
    axis = _axis_vector(pull_axis)
    minimum = float(minimum_draft_deg)
    if not (0.0 <= minimum < 90.0):
        raise ValueError("minimum draft must be between 0 and 90 degrees")

    values = []
    positive = 0
    negative = 0
    near_parallel_wall = 0
    skipped = 0
    for normal in surface["triangle_normals"]:
        if normal.length <= 1e-12:
            skipped += 1
            continue
        dot = _clamp(normal.dot(axis))
        angle = math.degrees(math.acos(dot))
        wall_draft = abs(90.0 - angle)
        values.append(wall_draft)
        if dot > 1e-9:
            positive += 1
        elif dot < -1e-9:
            negative += 1
        if wall_draft < minimum:
            near_parallel_wall += 1

    return {
        "schema": "OLEANDER_PULL_AXIS_ORIENTATION_DIAGNOSTIC_v0.1",
        "pull_axis": [float(value) for value in axis],
        "minimum_draft_deg": minimum,
        "sampled_triangles": len(values),
        "skipped_degenerate_triangles": skipped,
        "positive_axis_facing_triangles": positive,
        "negative_axis_facing_triangles": negative,
        "below_minimum_wall_draft_triangles": near_parallel_wall,
        "min_wall_draft_deg": min(values) if values else None,
        "max_wall_draft_deg": max(values) if values else None,
        "mean_wall_draft_deg": (sum(values) / len(values)) if values else None,
        "authority": "POLYGON_NORMAL_PULL_AXIS_ORIENTATION_NOT_MOLDABILITY",
        "non_claims": ["undercut_certification", "moldability", "parting_line_solution", "manufacturing_release"],
    }


def normal_ray_thickness_report(scene, surface, max_samples=2048, epsilon_mm=1e-4):
    """Sample opposite-surface distances along inward triangle normals.

    The result is useful for interface/shell diagnostics on consistently oriented
    closed two-manifold polygon meshes. It is not a general engineering wall
    thickness solver and may hit unrelated opposite geometry in concave parts.
    """
    max_samples = int(max_samples)
    if max_samples < 1:
        raise ValueError("max_samples must be positive")
    epsilon_mm = float(epsilon_mm)
    if epsilon_mm <= 0.0:
        raise ValueError("epsilon_mm must be positive")
    if not surface["closed_two_manifold"]:
        raise ValueError("normal-ray thickness requires a closed two-manifold evaluated mesh")
    if surface["orientation"] == "UNRESOLVED":
        raise ValueError("normal-ray thickness requires resolvable closed-mesh orientation")

    triangles = surface["triangles"]
    if len(triangles) > max_samples:
        step = len(triangles) / float(max_samples)
        sample_indices = sorted({min(len(triangles) - 1, int(i * step)) for i in range(max_samples)})
    else:
        sample_indices = list(range(len(triangles)))

    vertices = surface["vertices"]
    bvh = BVHTree.FromPolygons(vertices, triangles, all_triangles=True)
    if bvh is None:
        raise ValueError("could not build BVH for thickness diagnostics")

    min_corner = Vector((
        min(vertex.x for vertex in vertices),
        min(vertex.y for vertex in vertices),
        min(vertex.z for vertex in vertices),
    ))
    max_corner = Vector((
        max(vertex.x for vertex in vertices),
        max(vertex.y for vertex in vertices),
        max(vertex.z for vertex in vertices),
    ))
    max_distance = max((max_corner - min_corner).length * 2.0, 1e-9)
    epsilon_scene = mm_to_scene_units(scene, epsilon_mm)

    distances_mm = []
    misses = 0
    for index in sample_indices:
        normal = surface["triangle_normals"][index]
        if normal.length <= 1e-12:
            misses += 1
            continue
        center = surface["triangle_centers"][index]
        direction = -normal.normalized()
        origin = center + direction * epsilon_scene
        hit = bvh.ray_cast(origin, direction, max_distance)
        location, _hit_normal, hit_index, distance = hit
        if location is None or hit_index is None or distance is None:
            misses += 1
            continue
        # Add back the offset so the reported sample approximates surface-to-surface distance.
        measured_scene = float(distance) + epsilon_scene
        distances_mm.append(scene_units_to_mm(scene, measured_scene))

    return {
        "schema": "OLEANDER_NORMAL_RAY_THICKNESS_DIAGNOSTIC_v0.1",
        "requested_max_samples": max_samples,
        "sampled_triangles": len(sample_indices),
        "successful_samples": len(distances_mm),
        "missed_samples": misses,
        "epsilon_mm": epsilon_mm,
        "min_mm": min(distances_mm) if distances_mm else None,
        "max_mm": max(distances_mm) if distances_mm else None,
        "mean_mm": (sum(distances_mm) / len(distances_mm)) if distances_mm else None,
        "p05_mm": _percentile(distances_mm, 0.05),
        "p50_mm": _percentile(distances_mm, 0.50),
        "p95_mm": _percentile(distances_mm, 0.95),
        "authority": "NORMAL_RAY_EVALUATED_MESH_THICKNESS_DIAGNOSTIC_ONLY",
        "non_claims": ["engineering_wall_thickness", "minimum_material_thickness_certification", "manufacturing_release"],
    }


def surface_diagnostic_snapshot(
    scene,
    obj,
    depsgraph=None,
    hard_edge_threshold_deg=30.0,
    pull_axis="Z",
    minimum_draft_deg=2.0,
    thickness_samples=2048,
    max_triangles=50000,
):
    surface = evaluated_surface_data(obj, depsgraph=depsgraph, max_triangles=max_triangles)
    dihedral = dihedral_report(surface, hard_edge_threshold_deg=hard_edge_threshold_deg)
    pull = pull_axis_orientation_report(surface, pull_axis=pull_axis, minimum_draft_deg=minimum_draft_deg)
    thickness = None
    thickness_state = "NOT_RUN_OPEN_OR_NONMANIFOLD"
    if surface["closed_two_manifold"] and surface["orientation"] != "UNRESOLVED":
        thickness = normal_ray_thickness_report(scene, surface, max_samples=thickness_samples)
        thickness_state = "DIAGNOSTIC_COMPLETE"

    result = {
        "schema": "OLEANDER_SURFACE_DIAGNOSTICS_v0.1",
        "object": surface["object"],
        "geometry_source": surface["geometry_source"],
        "triangle_count": surface["triangle_count"],
        "vertex_count": surface["vertex_count"],
        "edge_count": surface["edge_count"],
        "boundary_edge_count": surface["boundary_edge_count"],
        "nonmanifold_edge_count": surface["nonmanifold_edge_count"],
        "closed_two_manifold": surface["closed_two_manifold"],
        "degenerate_triangle_count": surface["degenerate_triangle_count"],
        "orientation": surface["orientation"],
        "dihedral": dihedral,
        "pull_axis_orientation": pull,
        "normal_ray_thickness_state": thickness_state,
        "normal_ray_thickness": thickness,
        "authority": "EVALUATED_POLYGON_MESH_SURFACE_DIAGNOSTICS",
        "non_claims": [
            "class_a_continuity", "analytic_curvature", "nurbs_fairness",
            "undercut_certification", "moldability", "engineering_wall_thickness",
            "manufacturing_release", "engineering_approval", "design_pass",
        ],
    }
    scene[SURFACE_DIAGNOSTICS_KEY] = json.dumps(result, sort_keys=True)
    return result


class OLEANDER_OT_surface_diagnostics(bpy.types.Operator):
    bl_idname = "oleander.surface_diagnostics"
    bl_label = "Surface Diagnostics"
    bl_options = {"REGISTER"}

    hard_edge_threshold_deg: bpy.props.FloatProperty(name="Hard edge °", default=30.0, min=0.0, max=180.0)
    pull_axis: bpy.props.EnumProperty(
        name="Pull axis",
        items=[(value, value, "") for value in ("X", "Y", "Z", "-X", "-Y", "-Z")],
        default="Z",
    )
    minimum_draft_deg: bpy.props.FloatProperty(name="Minimum wall draft °", default=2.0, min=0.0, max=89.999)
    thickness_samples: bpy.props.IntProperty(name="Thickness samples", default=2048, min=1, max=100000)

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != "MESH":
            self.report({"ERROR"}, "active mesh object required")
            return {"CANCELLED"}
        try:
            result = surface_diagnostic_snapshot(
                context.scene,
                obj,
                depsgraph=context.evaluated_depsgraph_get(),
                hard_edge_threshold_deg=self.hard_edge_threshold_deg,
                pull_axis=self.pull_axis,
                minimum_draft_deg=self.minimum_draft_deg,
                thickness_samples=self.thickness_samples,
            )
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        state = "closed" if result["closed_two_manifold"] else "open/nonmanifold"
        self.report({"INFO"}, f"Surface diagnostics: {result['triangle_count']} triangles; {state}")
        return {"FINISHED"}


class OLEANDER_PT_surface_diagnostics(bpy.types.Panel):
    bl_label = "Surface Diagnostics"
    bl_idname = "OLEANDER_PT_surface_diagnostics"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OLEANDER"
    bl_parent_id = "OLEANDER_PT_runtime_panel"

    def draw(self, context):
        layout = self.layout
        layout.operator("oleander.surface_diagnostics", text="Run Surface Diagnostics")
        layout.label(text="Evaluated mesh / manifold / dihedral / pull axis", icon="INFO")
        layout.label(text="Thickness = normal-ray diagnostic only", icon="INFO")
        layout.label(text="Not Class-A, CAD curvature or moldability proof", icon="INFO")


OPERATOR_CLASSES = (OLEANDER_OT_surface_diagnostics,)
PANEL_CLASSES = (OLEANDER_PT_surface_diagnostics,)
