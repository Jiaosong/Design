"""Real-Blender validation for OLEANDER evaluated mesh surface diagnostics."""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys

import bpy

SCRIPT = pathlib.Path(__file__).resolve()
RUNTIME_ROOT = SCRIPT.parents[1]
PIPELINE_ROOT = SCRIPT.parents[2]
ADDON_ROOT = RUNTIME_ROOT / "oleander_blender"
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

import oleander_blender
from oleander_blender.surface_diagnostics import (
    SURFACE_DIAGNOSTICS_KEY,
    dihedral_report,
    evaluated_surface_data,
    normal_ray_thickness_report,
    pull_axis_orientation_report,
    surface_diagnostic_snapshot,
)

MM_TOL = 2e-3


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def assert_close(actual, expected, tolerance, message):
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"{message}: actual={actual!r} expected={expected!r}")


def expect_value_error(fn, text):
    try:
        fn()
    except ValueError as exc:
        assert_true(text in str(exc), f"expected {text!r}; got {exc!r}")
        return
    raise AssertionError(f"expected ValueError containing {text!r}")


def source_fingerprint():
    paths = [
        path
        for path in ADDON_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".py", ".json", ".toml"}
    ]
    paths.append(SCRIPT)
    digest = hashlib.sha256()
    for path in sorted(set(paths), key=lambda item: item.as_posix()):
        digest.update(path.relative_to(PIPELINE_ROOT).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def set_metadata(obj, oid):
    obj.oleander.ole_id = oid
    obj.oleander.geometry_authority = "VERIFIED_SOURCE"
    obj.oleander.field_state = "NOT_APPLICABLE"
    obj.oleander.engineering_state = "NOT_APPLICABLE"
    obj.oleander.manufacturing_state = "NOT_APPLICABLE"
    obj.oleander.design_review_state = "NA"


def add_cube(name, oid, size=100.0, location=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = name
    set_metadata(obj, oid)
    return obj


def add_plane(name, oid, size=100.0):
    bpy.ops.mesh.primitive_plane_add(size=size)
    obj = bpy.context.active_object
    obj.name = name
    set_metadata(obj, oid)
    return obj


def main():
    if hasattr(bpy.types.Object, "oleander"):
        try:
            oleander_blender.unregister()
        except Exception:
            pass
    oleander_blender.register()
    clear_scene()

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    depsgraph = bpy.context.evaluated_depsgraph_get()

    cube = add_cube("OLE_SURFACE_CUBE", "OLE_SURFACE_CUBE", size=100.0)
    depsgraph.update()
    surface = evaluated_surface_data(cube, depsgraph)
    assert_true(surface["geometry_source"] == "DEPSGRAPH_EVALUATED_TRIANGULATED_MESH", "surface diagnostics must use evaluated mesh")
    assert_true(surface["triangle_count"] == 12, "plain cube must triangulate to 12 triangles")
    assert_true(surface["closed_two_manifold"], "cube must be closed two-manifold")
    assert_true(surface["boundary_edge_count"] == 0, "closed cube must have no boundary edges")
    assert_true(surface["nonmanifold_edge_count"] == 0, "closed cube must have no nonmanifold edges")
    assert_true(surface["orientation"] in {"POSITIVE", "NEGATIVE"}, "closed cube orientation must be resolvable")

    # Dihedral diagnostic: cube triangle diagonals are coplanar; physical cube edges are 90 degrees.
    dihedral = dihedral_report(surface, hard_edge_threshold_deg=45.0)
    assert_true(dihedral["hard_edge_count"] == 12, "cube must expose 12 physical hard edges above 45 degrees")
    assert_close(dihedral["max_deg"], 90.0, 1e-5, "cube max dihedral must be 90 degrees")
    assert_true(dihedral["authority"] == "TRIANGULATED_MESH_NORMAL_VARIATION_NOT_CLASS_A_CURVATURE", "dihedral authority boundary required")

    pull = pull_axis_orientation_report(surface, pull_axis="Z", minimum_draft_deg=2.0)
    assert_true(pull["below_minimum_wall_draft_triangles"] == 8, "cube must expose eight vertical wall triangles below 2 degree draft")
    assert_true(pull["positive_axis_facing_triangles"] == 2, "cube top must contribute two +Z triangles")
    assert_true(pull["negative_axis_facing_triangles"] == 2, "cube bottom must contribute two -Z triangles")
    assert_true(pull["authority"] == "POLYGON_NORMAL_PULL_AXIS_ORIENTATION_NOT_MOLDABILITY", "pull-axis diagnostic must deny moldability authority")

    thickness = normal_ray_thickness_report(scene, surface, max_samples=32)
    assert_true(thickness["successful_samples"] == 12 and thickness["missed_samples"] == 0, "cube thickness rays must all resolve")
    assert_close(thickness["min_mm"], 100.0, MM_TOL, "cube minimum normal-ray thickness must be 100 mm")
    assert_close(thickness["max_mm"], 100.0, MM_TOL, "cube maximum normal-ray thickness must be 100 mm")
    assert_close(thickness["mean_mm"], 100.0, MM_TOL, "cube mean normal-ray thickness must be 100 mm")
    assert_true(thickness["authority"] == "NORMAL_RAY_EVALUATED_MESH_THICKNESS_DIAGNOSTIC_ONLY", "thickness must remain diagnostic-only")

    snapshot = surface_diagnostic_snapshot(
        scene,
        cube,
        depsgraph=depsgraph,
        hard_edge_threshold_deg=45.0,
        pull_axis="Z",
        minimum_draft_deg=2.0,
        thickness_samples=32,
    )
    assert_true(SURFACE_DIAGNOSTICS_KEY in scene, "surface diagnostic snapshot must persist on scene")
    assert_true(snapshot["normal_ray_thickness_state"] == "DIAGNOSTIC_COMPLETE", "closed cube must run thickness diagnostic")
    assert_true("class_a_continuity" in snapshot["non_claims"], "snapshot must deny Class-A certification")
    assert_true("engineering_wall_thickness" in snapshot["non_claims"], "snapshot must deny engineering wall-thickness authority")

    # Dependency-graph evaluated path must include modifiers.
    evaluated_cube = add_cube("OLE_SURFACE_EVALUATED", "OLE_SURFACE_EVALUATED", size=100.0, location=(200.0, 0.0, 0.0))
    bevel = evaluated_cube.modifiers.new(name="OLE_SURFACE_TEST_BEVEL", type="BEVEL")
    bevel.width = 5.0
    bevel.segments = 2
    bpy.context.evaluated_depsgraph_get().update()
    evaluated = evaluated_surface_data(evaluated_cube, bpy.context.evaluated_depsgraph_get())
    assert_true(evaluated["triangle_count"] > 12, "evaluated surface data must include Bevel modifier output")

    # Open mesh keeps topology diagnostics but does not fabricate thickness.
    plane = add_plane("OLE_SURFACE_PLANE", "OLE_SURFACE_PLANE", size=100.0)
    open_surface = evaluated_surface_data(plane, bpy.context.evaluated_depsgraph_get())
    assert_true(not open_surface["closed_two_manifold"], "plane must be open")
    assert_true(open_surface["boundary_edge_count"] > 0, "plane must expose boundary edges")
    expect_value_error(lambda: normal_ray_thickness_report(scene, open_surface), "closed two-manifold")
    open_snapshot = surface_diagnostic_snapshot(scene, plane, depsgraph=bpy.context.evaluated_depsgraph_get())
    assert_true(open_snapshot["normal_ray_thickness_state"] == "NOT_RUN_OPEN_OR_NONMANIFOLD", "open mesh must not fabricate thickness")
    assert_true(open_snapshot["normal_ray_thickness"] is None, "open mesh thickness result must remain null")

    # Positive failure gates.
    expect_value_error(lambda: evaluated_surface_data(plane, depsgraph, max_triangles=0), "positive")
    expect_value_error(lambda: dihedral_report(surface, hard_edge_threshold_deg=181.0), "between 0 and 180")
    expect_value_error(lambda: pull_axis_orientation_report(surface, pull_axis="BAD"), "pull axis")
    expect_value_error(lambda: pull_axis_orientation_report(surface, pull_axis=(0.0, 0.0, 0.0)), "non-zero")
    expect_value_error(lambda: pull_axis_orientation_report(surface, minimum_draft_deg=90.0), "between 0 and 90")
    expect_value_error(lambda: normal_ray_thickness_report(scene, surface, max_samples=0), "positive")
    expect_value_error(lambda: normal_ray_thickness_report(scene, surface, epsilon_mm=0.0), "positive")

    bpy.ops.object.empty_add(type="PLAIN_AXES")
    empty = bpy.context.active_object
    expect_value_error(lambda: evaluated_surface_data(empty, depsgraph), "mesh object")

    # Operator registration and governed persistence.
    bpy.context.view_layer.objects.active = cube
    cube.select_set(True)
    op = bpy.ops.oleander.surface_diagnostics(hard_edge_threshold_deg=45.0, pull_axis="Z", minimum_draft_deg=2.0, thickness_samples=32)
    assert_true("FINISHED" in op, "surface diagnostic operator must execute on active mesh")
    stored = json.loads(scene[SURFACE_DIAGNOSTICS_KEY])
    assert_true(stored["object"] == "OLE_SURFACE_CUBE", "operator snapshot must preserve OLE provenance")
    assert_true(stored["authority"] == "EVALUATED_POLYGON_MESH_SURFACE_DIAGNOSTICS", "operator snapshot authority boundary required")

    reopen_path = "/tmp/oleander-stage3-surface-diagnostics-reopen.blend"
    bpy.ops.wm.save_as_mainfile(filepath=reopen_path)
    bpy.ops.wm.open_mainfile(filepath=reopen_path)
    reopened = bpy.context.scene
    assert_true(SURFACE_DIAGNOSTICS_KEY in reopened, "surface diagnostic snapshot must survive reopen")
    reopened_result = json.loads(reopened[SURFACE_DIAGNOSTICS_KEY])
    assert_true(reopened_result["object"] == "OLE_SURFACE_CUBE", "surface diagnostic OLE provenance must survive reopen")
    assert_true("moldability" in reopened_result["non_claims"], "moldability non-claim must survive reopen")

    result = {
        "runtime": "OLEANDER Blender Runtime",
        "stage": "STAGE3_SURFACE_DIAGNOSTIC_FOUNDATION",
        "version": "0.2.0",
        "blender": bpy.app.version_string,
        "status": "PASS",
        "source_fingerprint_sha256": source_fingerprint(),
        "checks": [
            "depsgraph_evaluated_surface_data", "evaluated_mesh_modifier_inclusion",
            "closed_two_manifold_detection", "boundary_edge_detection", "nonmanifold_edge_count",
            "closed_mesh_orientation_resolution", "triangulated_dihedral_diagnostic",
            "cube_hard_edge_count", "dihedral_class_a_boundary", "pull_axis_orientation_diagnostic",
            "minimum_wall_draft_flagging", "pull_axis_moldability_boundary",
            "normal_ray_thickness_sampling", "normal_ray_metric_thickness",
            "thickness_engineering_boundary", "surface_diagnostic_snapshot",
            "open_mesh_thickness_not_fabricated", "surface_diagnostic_operator_registration",
            "surface_diagnostic_ole_provenance", "surface_diagnostic_save_reopen_persistence",
            "invalid_triangle_budget_expected_failure", "invalid_dihedral_threshold_expected_failure",
            "invalid_pull_axis_expected_failure", "zero_pull_axis_expected_failure",
            "invalid_minimum_draft_expected_failure", "invalid_thickness_samples_expected_failure",
            "invalid_thickness_epsilon_expected_failure", "nonmesh_expected_failure"
        ],
        "expected_failure_cases": {
            "invalid_triangle_budget": "PASS", "invalid_dihedral_threshold": "PASS",
            "invalid_pull_axis": "PASS", "zero_pull_axis": "PASS",
            "invalid_minimum_draft": "PASS", "invalid_thickness_samples": "PASS",
            "invalid_thickness_epsilon": "PASS", "nonmesh": "PASS",
            "open_mesh_thickness": "PASS"
        },
        "non_claims": [
            "class_a_continuity", "analytic_curvature", "nurbs_fairness",
            "undercut_certification", "moldability", "engineering_wall_thickness",
            "manufacturing_release", "engineering_approval", "field_truth", "design_quality"
        ]
    }
    print("OLEANDER_STAGE3_SURFACE_DIAGNOSTICS_VALIDATION=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
