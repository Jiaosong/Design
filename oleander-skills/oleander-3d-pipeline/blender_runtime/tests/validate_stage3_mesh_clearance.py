"""Real-Blender validation for evaluated triangulated mesh surface clearance."""

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
from oleander_blender.mesh_clearance import (
    TRUE_MESH_CLEARANCE_KEY,
    evaluated_mesh_triangles,
    true_mesh_surface_clearance,
)

MM_TOL = 1e-3


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
    paths = [path for path in ADDON_ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".py", ".json", ".toml"}]
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


def add_plane(name, oid, z):
    bpy.ops.mesh.primitive_plane_add(size=100.0, location=(0.0, 0.0, z))
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

    # Evaluated mesh path must include modifiers. A plane at z=0 is solidified
    # upward to z=20; a second plane at z=100 therefore has true mesh clearance 80 mm.
    lower = add_plane("OLE_CLEAR_LOWER", "OLE_CLEAR_LOWER", 0.0)
    solidify = lower.modifiers.new(name="OLE_TEST_SOLIDIFY", type="SOLIDIFY")
    solidify.thickness = 20.0
    solidify.offset = 1.0
    upper = add_plane("OLE_CLEAR_UPPER", "OLE_CLEAR_UPPER", 100.0)
    depsgraph.update()

    raw_triangles = len(lower.data.polygons) * 2
    evaluated_lower = evaluated_mesh_triangles(lower, depsgraph)
    assert_true(len(evaluated_lower) > raw_triangles, "evaluated mesh must include Solidify modifier output")

    clearance = true_mesh_surface_clearance(scene, lower, upper, depsgraph=depsgraph)
    assert_close(clearance["surface_distance_mm"], 80.0, MM_TOL, "evaluated mesh clearance must include modifier thickness")
    assert_true(not clearance["intersecting_or_touching"], "80 mm separated surfaces must not intersect")
    assert_true(clearance["geometry_source"] == "DEPSGRAPH_EVALUATED_TRIANGULATED_MESH", "clearance must bind evaluated mesh source")
    assert_true(clearance["authority"] == "EVALUATED_MESH_SURFACE_DISTANCE_NOT_ANALYTIC_CAD_BREP", "mesh clearance must deny analytic CAD/B-Rep authority")
    assert_true(clearance["a"] == "OLE_CLEAR_LOWER" and clearance["b"] == "OLE_CLEAR_UPPER", "clearance must preserve OLE object provenance")
    witness_gap = clearance["witness_b_world_mm"][2] - clearance["witness_a_world_mm"][2]
    assert_close(abs(witness_gap), 80.0, MM_TOL, "witness points must correspond to measured surface gap")

    # Touch/overlap route returns zero without inventing negative clearance.
    touching = add_plane("OLE_CLEAR_TOUCH", "OLE_CLEAR_TOUCH", 20.0)
    touch = true_mesh_surface_clearance(scene, lower, touching, depsgraph=bpy.context.evaluated_depsgraph_get())
    assert_true(touch["intersecting_or_touching"], "touching evaluated surfaces must be classified as touching/intersecting")
    assert_close(touch["surface_distance_mm"], 0.0, MM_TOL, "touching surface clearance must be zero")

    # Pair/triangle budgets and invalid object states fail positively.
    expect_value_error(lambda: true_mesh_surface_clearance(scene, lower, lower, depsgraph=depsgraph), "different objects")
    expect_value_error(lambda: true_mesh_surface_clearance(scene, lower, upper, depsgraph=depsgraph, max_pair_tests=1), "triangle pair count")
    expect_value_error(lambda: evaluated_mesh_triangles(lower, depsgraph, max_triangles=1), "triangle count exceeds")
    expect_value_error(lambda: true_mesh_surface_clearance(scene, lower, upper, depsgraph=depsgraph, zero_tolerance_mm=-1), "non-negative")
    expect_value_error(lambda: true_mesh_surface_clearance(scene, lower, upper, depsgraph=depsgraph, max_pair_tests=0), "positive")

    bpy.ops.object.empty_add(type="PLAIN_AXES")
    empty = bpy.context.active_object
    expect_value_error(lambda: evaluated_mesh_triangles(empty, depsgraph), "mesh objects")

    # Operator: exactly two meshes selected, writes governed scene snapshot.
    bpy.ops.object.select_all(action="DESELECT")
    lower.select_set(True)
    upper.select_set(True)
    bpy.context.view_layer.objects.active = lower
    op = bpy.ops.oleander.true_mesh_clearance(max_pair_tests=2000000)
    assert_true("FINISHED" in op, "mesh clearance operator must execute on exactly two selected meshes")
    assert_true(TRUE_MESH_CLEARANCE_KEY in scene, "mesh clearance operator must persist governed result")
    stored = json.loads(scene[TRUE_MESH_CLEARANCE_KEY])
    assert_close(stored["surface_distance_mm"], 80.0, MM_TOL, "operator result must match direct clearance")
    assert_true("analytic_cad_brep_clearance" in stored["non_claims"], "stored result must preserve CAD/B-Rep non-claim")

    bpy.ops.object.select_all(action="DESELECT")
    lower.select_set(True)
    bpy.context.view_layer.objects.active = lower
    invalid_op = bpy.ops.oleander.true_mesh_clearance()
    assert_true("CANCELLED" in invalid_op, "mesh clearance operator must fail unless exactly two meshes are selected")

    # Persistence through .blend reopen.
    bpy.ops.object.select_all(action="DESELECT")
    lower.select_set(True)
    upper.select_set(True)
    bpy.context.view_layer.objects.active = lower
    bpy.ops.oleander.true_mesh_clearance()
    reopen_path = "/tmp/oleander-stage3-mesh-clearance-reopen.blend"
    bpy.ops.wm.save_as_mainfile(filepath=reopen_path)
    bpy.ops.wm.open_mainfile(filepath=reopen_path)
    reopened = bpy.context.scene
    assert_true(TRUE_MESH_CLEARANCE_KEY in reopened, "mesh clearance snapshot must survive reopen")
    reopened_result = json.loads(reopened[TRUE_MESH_CLEARANCE_KEY])
    assert_true(reopened_result["geometry_source"] == "DEPSGRAPH_EVALUATED_TRIANGULATED_MESH", "evaluated geometry source must survive reopen")
    assert_true(reopened_result["authority"] == "EVALUATED_MESH_SURFACE_DISTANCE_NOT_ANALYTIC_CAD_BREP", "mesh-only authority boundary must survive reopen")

    result = {
        "runtime":"OLEANDER Blender Runtime",
        "stage":"STAGE3_EVALUATED_MESH_CLEARANCE",
        "version":"0.2.0",
        "blender":bpy.app.version_string,
        "status":"PASS",
        "source_fingerprint_sha256":source_fingerprint(),
        "checks":[
            "depsgraph_evaluated_mesh_with_modifier","evaluated_mesh_triangulation","true_mesh_surface_distance_metric","modifier_aware_clearance",
            "clearance_witness_points","mesh_clearance_ole_provenance","mesh_clearance_geometry_source","mesh_clearance_cad_brep_boundary",
            "touching_surface_zero_clearance","same_object_expected_failure","triangle_pair_budget_expected_failure","triangle_count_budget_expected_failure",
            "negative_zero_tolerance_expected_failure","invalid_pair_budget_expected_failure","nonmesh_expected_failure",
            "mesh_clearance_operator_registration","exact_two_mesh_selection_failure_gate","mesh_clearance_snapshot_persistence","mesh_clearance_save_reopen_persistence"
        ],
        "expected_failure_cases":{
            "same_object":"PASS","triangle_pair_budget":"PASS","triangle_count_budget":"PASS","negative_zero_tolerance":"PASS",
            "invalid_pair_budget":"PASS","nonmesh":"PASS","exact_two_mesh_selection":"PASS"
        },
        "non_claims":[
            "analytic_cad_brep_clearance","engineering_fit_approval","manufacturing_release","field_truth","constructability","design_quality"
        ]
    }
    print("OLEANDER_STAGE3_MESH_CLEARANCE_VALIDATION=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
