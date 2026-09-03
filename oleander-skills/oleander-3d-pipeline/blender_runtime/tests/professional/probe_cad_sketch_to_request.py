"""Export OLEANDER CAD build requests from a real CAD Sketcher solved profile.

The profile is fully constrained at bounded scope: four connected rectangle
edges, horizontal/vertical relations, one fixed corner, and driving width/depth.
Revision 2 edits the driving width and re-solves before request export.
Revision 3 remains contract-valid but uses a closed collinear three-point
profile that cannot produce a positive-area OCCT face, providing a deterministic
FreeCAD failure-envelope fixture.
"""

from __future__ import annotations

import importlib
import json
import os
import pathlib
import sys

import bpy

SCRIPT = pathlib.Path(__file__).resolve()
RUNTIME_ROOT = SCRIPT.parents[2]
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

from professional_adapter.cad_sidecar import build_request, payload_sha256, write_request

CAD_PACKAGE = os.environ.get(
    "OLEANDER_CAD_SKETCHER_PACKAGE",
    "bl_ext.oleander_professional.CAD_Sketcher",
)
OUT = pathlib.Path(os.environ.get("OLEANDER_CAD_INTEGRATION_DIR", "/tmp/oleander-cad-integration"))
OUT.mkdir(parents=True, exist_ok=True)
checks: list[str] = []


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def load_cad_sketcher():
    addon = importlib.import_module(CAD_PACKAGE)
    if not hasattr(bpy.context.scene, "sketcher"):
        addon.register()
    curve_data = importlib.import_module(f"{CAD_PACKAGE}.utilities.curve_data")
    sketch_ref = importlib.import_module(f"{CAD_PACKAGE}.model.sketch_ref")
    curve_ref = importlib.import_module(f"{CAD_PACKAGE}.model.curve_ref")
    return addon, curve_data, sketch_ref, curve_ref


def new_sketch(curve_data, sketch_ref):
    entities = bpy.context.scene.sketcher.entities
    entities.ensure_origin_elements(bpy.context)
    entity_sketch = entities.add_sketch(entities.origin_plane_XY)
    curve_data.ensure_sketch_curve_object(entity_sketch)
    sketch_ref.stamp_sketch_props(entity_sketch.target_object)
    sketch = sketch_ref.Sketch(entity_sketch.target_object)
    sketch.name = "OLEANDER_CAD_PROFILE"
    sketch_ref.set_active_sketch(bpy.context, sketch.target_object)
    return sketch


def solve_and_refresh(sketch, curve_data, label: str):
    ok = sketch.solve(bpy.context)
    check(ok, label)
    curve_data.refresh_curve_geometry(sketch)
    bpy.context.view_layer.update()


def set_driving_value(constraint, value: float):
    endpoint = bpy.context.scene.sketcher.get_constraint_value_endpoint(constraint)
    check(bool(endpoint), "driving_endpoint_exists")
    bpy.context.scene[endpoint] = float(constraint.from_displayed_value(value))
    check(abs(float(constraint.value) - value) < 1e-8, "driving_endpoint_readback")


def coords(points):
    return [[float(point.co.x), float(point.co.y)] for point in points]


def main() -> None:
    addon, curve_data, sketch_ref, curve_ref = load_cad_sketcher()
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001

    sketch = new_sketch(curve_data, sketch_ref)
    p0 = curve_ref.PointRef.create(sketch, (0.0, 0.0), fixed=True)
    p1 = curve_ref.PointRef.create(sketch, (80.0, 0.0))
    p2 = curve_ref.PointRef.create(sketch, (80.0, 50.0))
    p3 = curve_ref.PointRef.create(sketch, (0.0, 50.0))
    points = [p0, p1, p2, p3]

    l0 = curve_ref.LineRef.create(sketch, p0, p1)
    l1 = curve_ref.LineRef.create(sketch, p1, p2)
    l2 = curve_ref.LineRef.create(sketch, p2, p3)
    l3 = curve_ref.LineRef.create(sketch, p3, p0)
    constraints = sketch.constraints
    constraints.add_horizontal(curve_id_1=l0.curve_id)
    constraints.add_vertical(curve_id_1=l1.curve_id)
    constraints.add_horizontal(curve_id_1=l2.curve_id)
    constraints.add_vertical(curve_id_1=l3.curve_id)
    width = constraints.add_distance(init=True, curve_id_1=p0.curve_id, curve_id_2=p1.curve_id)
    depth = constraints.add_distance(init=True, curve_id_1=p0.curve_id, curve_id_2=p3.curve_id)
    set_driving_value(width, 80.0)
    set_driving_value(depth, 50.0)
    solve_and_refresh(sketch, curve_data, "revision1_solver_pass")
    check(abs(p1.co.x - 80.0) < 1e-6, "revision1_width")
    check(abs(p3.co.y - 50.0) < 1e-6, "revision1_depth")
    check(abs(p2.co.x - 80.0) < 1e-6 and abs(p2.co.y - 50.0) < 1e-6, "revision1_corner")

    source_v1 = OUT / "cad_source_R001.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(source_v1))
    request1 = build_request(
        request_id="OLE_CAD_REQ_BRACKET_001", ole_id="OLE_PRO_CAD_BRACKET_001", revision=1,
        editable_source=str(source_v1), solver="CAD Sketcher + SolveSpace", solver_state="FULLY_CONSTRAINED",
        profile_points_mm=coords(points), extrusion_depth_mm=10.0,
        holes=[{"center_mm": [40.0, 25.0], "radius_mm": 5.0}],
    )
    request1_path = OUT / "request_R001.json"
    hash1 = write_request(request1_path, request1)
    check(hash1 == payload_sha256(request1), "revision1_request_hash")

    set_driving_value(width, 100.0)
    solve_and_refresh(sketch, curve_data, "revision2_solver_pass")
    check(abs(p1.co.x - 100.0) < 1e-6, "revision2_width")
    check(abs(p2.co.x - 100.0) < 1e-6, "revision2_dependent_corner")
    check(abs(p3.co.y - 50.0) < 1e-6, "revision2_depth_preserved")

    source_v2 = OUT / "cad_source_R002.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(source_v2))
    request2 = build_request(
        request_id="OLE_CAD_REQ_BRACKET_001", ole_id="OLE_PRO_CAD_BRACKET_001", revision=2,
        editable_source=str(source_v2), solver="CAD Sketcher + SolveSpace", solver_state="FULLY_CONSTRAINED",
        profile_points_mm=coords(points), extrusion_depth_mm=10.0,
        holes=[{"center_mm": [50.0, 25.0], "radius_mm": 5.0}],
    )
    request2_path = OUT / "request_R002.json"
    hash2 = write_request(request2_path, request2)
    check(hash2 == payload_sha256(request2), "revision2_request_hash")
    check(hash1 != hash2, "parameter_edit_changes_request_hash")

    # Contract-valid but geometrically invalid: three unique collinear points form
    # a closed zero-area profile. The request serializer accepts it, while the
    # authoritative FreeCAD/OCCT service must reject it before releasing a solid.
    bad_request = build_request(
        request_id="OLE_CAD_REQ_BRACKET_001", ole_id="OLE_PRO_CAD_BRACKET_001", revision=3,
        editable_source=str(source_v2), solver="CAD Sketcher + SolveSpace", solver_state="FULLY_CONSTRAINED",
        profile_points_mm=[[0.0, 0.0], [50.0, 0.0], [100.0, 0.0]], extrusion_depth_mm=10.0,
        holes=[],
    )
    bad_path = OUT / "request_R003_EXPECT_FAIL.json"
    hash3 = write_request(bad_path, bad_request)
    check(hash3 == payload_sha256(bad_request), "failure_request_hash")
    check(bad_request["profile"]["closed"] is True, "failure_fixture_contract_closed")
    check(len(bad_request["profile"]["points_mm"]) == 3, "failure_fixture_contract_min_points")

    result = {
        "schema": "OLEANDER_CAD_SKETCH_TO_REQUEST_PROBE_v0.1", "status": "PASS", "blender": bpy.app.version_string,
        "cad_sketcher_package": CAD_PACKAGE, "checks": checks,
        "requests": {
            "revision1": {"path": str(request1_path), "sha256": hash1},
            "revision2": {"path": str(request2_path), "sha256": hash2},
            "expected_fail_revision3": {"path": str(bad_path), "sha256": hash3, "fixture": "COLLINEAR_ZERO_AREA_PROFILE"}
        },
        "non_claims": ["P0_A_PARAMETRIC_CAD_PASS", "general_sketch_export", "general_feature_tree", "assembly_mates"]
    }
    print("OLEANDER_CAD_SKETCH_TO_REQUEST=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
