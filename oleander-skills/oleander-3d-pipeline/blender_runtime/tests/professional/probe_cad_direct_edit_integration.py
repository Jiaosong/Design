"""Blender 5.2 integration probe for bounded CAD direct-edit execution.

PREPARE drives the real OLEANDER CAD_NATIVE Face Normal Move operator, confirms
that Blender display geometry is not mutated, then writes a base CAD build
request plus strict direct-edit requests. READBACK validates FreeCAD/OCCT PASS
and HOLD responses, binds only the PASS display derivative into Blender, and
save/reopens the governed display state.
"""

from __future__ import annotations

import bmesh
import copy
import json
import os
import pathlib
import sys

import bpy

SCRIPT = pathlib.Path(__file__).resolve()
RUNTIME_ROOT = SCRIPT.parents[2]
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

import oleander_blender
from professional_adapter.cad_sidecar import (
    CADSidecarContractError,
    DISPLAY_SCHEMA,
    RESPONSE_SCHEMA,
    bind_display_derivative,
    build_direct_edit_request_from_intent,
    build_request,
    file_sha256,
    payload_sha256,
    validate_direct_edit_request,
    write_direct_edit_request,
    write_request,
)

ROOT = pathlib.Path(os.environ.get("OLEANDER_CAD_DIRECT_INTEGRATION_DIR", "/tmp/oleander-cad-direct-integration"))
ROOT.mkdir(parents=True, exist_ok=True)
PHASE = os.environ.get("OLEANDER_CAD_DIRECT_PHASE", "PREPARE").strip().upper()
DIRECT_RESPONSE_SCHEMA = "OLEANDER_CAD_DIRECT_EDIT_RESPONSE_v0.1"
DIRECT_DISPLAY_SCHEMA = "OLEANDER_CAD_DIRECT_EDIT_DISPLAY_DERIVATIVE_v0.1"
OLE_ID = "OLE_CAD_DIRECT_EXECUTION_001"
BASE_REQUEST = ROOT / "base_build_request.json"
SUCCESS_REQUEST = ROOT / "direct_request_success.json"
MISSING_REQUEST = ROOT / "direct_request_missing.json"
AMBIGUOUS_REQUEST = ROOT / "direct_request_ambiguous.json"
REOPEN = ROOT / "cad_direct_edit_execution.blend"
checks: list[str] = []


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def canonical_text(payload: dict) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def read_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def clear_scene() -> None:
    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def select_only(obj) -> None:
    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def select_top_face(obj) -> None:
    select_only(obj)
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(obj.data)
    bm.normal_update()
    for face in bm.faces:
        face.select = False
    candidates = [face for face in bm.faces if face.normal.z > 0.999999]
    check(len(candidates) == 1, "prepare_unique_positive_z_display_face")
    candidates[0].select = True
    bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)


def vertex_snapshot(obj):
    return tuple(tuple(round(float(v), 9) for v in vertex.co) for vertex in obj.data.vertices)


def prepare_box_display(master_locator: str):
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    obj = bpy.context.active_object
    obj.name = "OLE_CAD_DIRECT_EXECUTION_DISPLAY"
    obj.oleander.ole_id = OLE_ID
    result = bpy.ops.oleander.apply_metric_dimensions(x_mm=80.0, y_mm=50.0, z_mm=10.0)
    check("FINISHED" in result, "prepare_display_dimensions")
    # Scene scale is 0.001, so one Blender unit is one millimetre. Move local
    # geometry upward so the display derivative spans Z=0..10 like FreeCAD.
    for vertex in obj.data.vertices:
        vertex.co.z += 5.0
    obj.data.update()
    bpy.context.view_layer.update()
    obj.oleander.master_type = "CAD_NATIVE"
    obj.oleander.master_locator = master_locator
    obj.oleander.geometry_authority = "VISUAL_ONLY"
    return obj


def make_direct_request_from_intent(intent: dict, request_id: str, master_locator: str) -> dict:
    candidate = copy.deepcopy(intent)
    candidate["authority"]["master_locator"] = master_locator
    request = build_direct_edit_request_from_intent(request_id=request_id, revision=2, intent=candidate)
    validate_direct_edit_request(request)
    return candidate, request


def prepare() -> None:
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

    base_dir = ROOT / "base"
    master_fcstd = base_dir / f"{OLE_ID}_R001.FCStd"
    master_locator = str(master_fcstd)
    obj = prepare_box_display(master_locator)
    before = vertex_snapshot(obj)
    select_top_face(obj)
    result = bpy.ops.oleander.direct_face_normal_move(distance_mm=5.0)
    check("FINISHED" in result, "prepare_real_cad_native_face_operator")
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.update()
    check(vertex_snapshot(obj) == before, "prepare_cad_display_geometry_unchanged")
    check(obj.get("oleander_cad_direct_edit_state") == "PENDING_SIDECAR", "prepare_pending_sidecar_state")
    intent = json.loads(obj["oleander_cad_direct_edit_intent"])
    check(intent["operation"] == "FACE_NORMAL_MOVE", "prepare_bounded_operation")
    check(abs(intent["parameters"]["distance_mm"] - 5.0) <= 1e-9, "prepare_metric_distance")
    check(all(abs(a - b) <= 1e-4 for a, b in zip(intent["target"]["center_local_mm"], [0.0, 0.0, 10.0])), "prepare_descriptor_top_center")
    check(abs(intent["target"]["area_mm2"] - 4000.0) <= 1e-3, "prepare_descriptor_area")
    check(all(abs(a - b) <= 1e-4 for a, b in zip(intent["target"]["edge_lengths_mm"], [50.0, 50.0, 80.0, 80.0])), "prepare_descriptor_edge_lengths")

    base_request = build_request(
        request_id="OLE_CAD_DIRECT_BASE_R001",
        ole_id=OLE_ID,
        revision=1,
        editable_source="OLEANDER_DIRECT_EXECUTION_FIXTURE",
        solver="BOUNDED_TEST_FIXTURE",
        solver_state="FULLY_CONSTRAINED",
        profile_points_mm=[[-40.0, -25.0], [40.0, -25.0], [40.0, 25.0], [-40.0, 25.0]],
        extrusion_depth_mm=10.0,
    )
    write_request(BASE_REQUEST, base_request)

    success_intent, success_request = make_direct_request_from_intent(
        intent,
        "OLE_CAD_DIRECT_REQ_SUCCESS_R002",
        master_locator,
    )
    missing_locator = str(ROOT / "hold_missing" / "missing.FCStd")
    ambiguous_locator = str(ROOT / "hold_ambiguous" / "ambiguous.FCStd")
    missing_intent, missing_request = make_direct_request_from_intent(
        intent,
        "OLE_CAD_DIRECT_REQ_MISSING_R002",
        missing_locator,
    )
    ambiguous_intent, ambiguous_request = make_direct_request_from_intent(
        intent,
        "OLE_CAD_DIRECT_REQ_AMBIGUOUS_R002",
        ambiguous_locator,
    )
    write_direct_edit_request(SUCCESS_REQUEST, success_request)
    write_direct_edit_request(MISSING_REQUEST, missing_request)
    write_direct_edit_request(AMBIGUOUS_REQUEST, ambiguous_request)
    for name, payload in (
        ("direct_intent_success.json", success_intent),
        ("direct_intent_missing.json", missing_intent),
        ("direct_intent_ambiguous.json", ambiguous_intent),
    ):
        (ROOT / name).write_text(canonical_text(payload), encoding="utf-8")

    check(payload_sha256(success_request) == payload_sha256(read_json(SUCCESS_REQUEST)), "prepare_success_request_readback_sha")
    check(success_request["authority"]["execution_state"] == "NOT_EXECUTED", "prepare_request_not_executed")
    check(success_request["target_selector"]["resolution_policy"] == "SEMANTIC_REBIND_FAIL_CLOSED", "prepare_fail_closed_selector")
    check("polygon_index" not in success_request["target_selector"]["descriptor"], "prepare_no_polygon_index_descriptor_key")
    check(
        set(success_request["target_selector"]["prohibited_persistence"])
        == {"FaceN", "EdgeN", "VertexN", "subshape_ordinal", "polygon_index"},
        "prepare_topology_persistence_prohibition_declared",
    )
    check("Face17" not in canonical_text(success_request), "prepare_no_concrete_face_ordinal")

    result_payload = {
        "schema": "OLEANDER_CAD_DIRECT_EDIT_INTEGRATION_PREPARE_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "base_request_sha256": payload_sha256(base_request),
        "direct_request_sha256": payload_sha256(success_request),
        "authority": {"master": "FREECAD_OCCT_BREP", "blender": "DISPLAY_DERIVATIVE_ONLY", "execution": "NOT_EXECUTED"},
        "non_claims": ["cad_direct_edit_execution_before_sidecar", "general_brep_push_pull", "persistent_topological_naming", "P0_B_DIRECT_BREP_PASS"],
    }
    print("OLEANDER_CAD_DIRECT_EDIT_PREPARE=" + json.dumps(result_payload, sort_keys=True))


def validate_response(response: dict, request: dict, expected_status: str, expected_resolution: str) -> None:
    check(response.get("schema") == DIRECT_RESPONSE_SCHEMA, f"{expected_status}_response_schema")
    check(response.get("status") == expected_status, f"{expected_status}_response_status")
    check(response.get("request_id") == request["request_id"], f"{expected_status}_request_id_match")
    check(response.get("ole_id") == request["ole_id"], f"{expected_status}_ole_id_match")
    check(int(response.get("revision", -1)) == int(request["revision"]), f"{expected_status}_revision_match")
    check(response.get("request_sha256") == payload_sha256(request), f"{expected_status}_request_sha_match")
    check(response.get("resolution", {}).get("state") == expected_resolution, f"{expected_status}_resolution_state")
    check(response.get("authoritative", {}).get("master_type") == "CAD_NATIVE", f"{expected_status}_cad_native_authority")
    check(response.get("authoritative", {}).get("geometry_authority") == "FREECAD_OCCT_BREP", f"{expected_status}_freecad_occt_authority")
    if expected_status == "PASS":
        check(response.get("operation", {}).get("execution_state") == "EXECUTED", "pass_operation_executed")
        check(response.get("resolution", {}).get("candidate_count") == 1, "pass_unique_candidate")
        for artifact in ("fcstd", "step", "brep"):
            record = response["authoritative"][artifact]
            path = pathlib.Path(record["path"])
            check(path.is_file() and path.stat().st_size > 0, f"pass_{artifact}_artifact_exists")
            check(file_sha256(path) == record["sha256"], f"pass_{artifact}_artifact_sha")
        display_record = response["display_derivative"]
        display_path = pathlib.Path(display_record["path"])
        check(display_path.is_file(), "pass_display_derivative_exists")
        check(file_sha256(display_path) == display_record["sha256"], "pass_display_derivative_sha")
    else:
        check(response.get("operation", {}).get("execution_state") == "NOT_EXECUTED", f"{expected_status}_operation_not_executed")
        check(response.get("measurements", {}).get("result_solid_count") == 0, f"{expected_status}_zero_released_solids")
        for artifact in ("fcstd", "step", "brep"):
            check(not response["authoritative"][artifact]["path"], f"{expected_status}_{artifact}_not_released")
        check(not response["display_derivative"]["path"], f"{expected_status}_display_not_released")


def readback() -> None:
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

    success_request = read_json(SUCCESS_REQUEST)
    missing_request = read_json(MISSING_REQUEST)
    ambiguous_request = read_json(AMBIGUOUS_REQUEST)
    for request in (success_request, missing_request, ambiguous_request):
        validate_direct_edit_request(request)
    checks.append("readback_all_requests_strictly_revalidated")

    success_response = read_json(ROOT / "direct_success" / "cad_direct_edit_response.json")
    missing_response = read_json(ROOT / "direct_missing" / "cad_direct_edit_response.json")
    ambiguous_response = read_json(ROOT / "direct_ambiguous" / "cad_direct_edit_response.json")
    validate_response(success_response, success_request, "PASS", "RESOLVED_UNIQUE")
    validate_response(missing_response, missing_request, "HOLD", "MISSING_HOLD")
    validate_response(ambiguous_response, ambiguous_request, "HOLD", "AMBIGUOUS_HOLD")
    check(ambiguous_response["resolution"]["candidate_count"] == 2, "ambiguous_exactly_two_candidates")

    measurements = success_response["measurements"]
    check(all(abs(a - b) <= 1e-4 for a, b in zip(measurements["source_bbox_mm"], [80.0, 50.0, 10.0])), "pass_source_bbox")
    check(all(abs(a - b) <= 1e-4 for a, b in zip(measurements["result_bbox_mm"], [80.0, 50.0, 15.0])), "pass_result_bbox")
    check(abs(measurements["source_volume_mm3"] - 40000.0) <= 1e-3, "pass_source_volume")
    check(abs(measurements["result_volume_mm3"] - 60000.0) <= 1e-3, "pass_result_volume")
    check(success_response["source_master"]["brep"]["sha256"] != success_response["authoritative"]["brep"]["sha256"], "pass_authoritative_brep_changed")

    display = read_json(ROOT / "direct_success" / "cad_direct_edit_display_derivative.json")
    check(display.get("schema") == DIRECT_DISPLAY_SCHEMA, "readback_direct_display_schema")
    check(display.get("request_sha256") == payload_sha256(success_request), "readback_display_request_sha")
    check(display.get("display_authority") == "DISPLAY_DERIVATIVE_ONLY", "readback_display_non_authoritative")

    # Reuse the existing CAD sidecar Blender binder. Only schema adaptation is
    # performed here; the direct-edit response remains separately typed on disk.
    adapted_response = {
        "schema": RESPONSE_SCHEMA,
        "request_id": success_response["request_id"],
        "ole_id": success_response["ole_id"],
        "revision": success_response["revision"],
        "status": "PASS",
        "request_sha256": success_response["request_sha256"],
        "authoritative": success_response["authoritative"],
    }
    adapted_display = dict(display)
    adapted_display["schema"] = DISPLAY_SCHEMA
    obj = bind_display_derivative(response=adapted_response, display_payload=adapted_display)
    obj["cad_direct_edit_response_schema"] = DIRECT_RESPONSE_SCHEMA
    obj["cad_direct_edit_display_schema"] = DIRECT_DISPLAY_SCHEMA
    obj["cad_direct_edit_execution_state"] = "EXECUTED"
    obj["cad_direct_edit_resolution_state"] = success_response["resolution"]["state"]
    bpy.context.view_layer.update()
    check(abs(obj.dimensions.x - 80.0) <= 1e-3, "readback_blender_width")
    check(abs(obj.dimensions.y - 50.0) <= 1e-3, "readback_blender_depth")
    check(abs(obj.dimensions.z - 15.0) <= 1e-3, "readback_blender_height")
    check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "readback_blender_display_only")
    check(obj["authoritative_geometry_kernel"] == "FREECAD_OCCT_BREP", "readback_kernel_authority")
    check(obj["cad_request_sha256"] == payload_sha256(success_request), "readback_bound_request_sha")

    forged = copy.deepcopy(success_response)
    forged["request_sha256"] = "f" * 64
    try:
        validate_response(forged, success_request, "PASS", "RESOLVED_UNIQUE")
    except AssertionError:
        checks.append("forged_direct_response_sha_expected_failure")
    else:
        raise AssertionError("forged_direct_response_sha_expected_failure")

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.is_file(), "readback_blend_saved")
    name = obj.name
    request_sha = obj["cad_request_sha256"]
    step_sha = obj["source_step_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    reopened = bpy.data.objects.get(name)
    check(reopened is not None, "readback_blend_reopen")
    check(reopened["ole_id"] == OLE_ID, "readback_ole_id_reopen")
    check(reopened["cad_request_sha256"] == request_sha, "readback_request_sha_reopen")
    check(reopened["source_step_sha256"] == step_sha, "readback_step_sha_reopen")
    check(reopened["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "readback_authority_reopen")
    check(reopened["cad_direct_edit_execution_state"] == "EXECUTED", "readback_execution_state_reopen")

    result_payload = {
        "schema": "OLEANDER_CAD_DIRECT_EDIT_INTEGRATION_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "request_sha256": payload_sha256(success_request),
        "authority": {"master": "FREECAD_OCCT_BREP", "blender": "DISPLAY_DERIVATIVE_ONLY", "execution": "EXECUTED", "resolution": "RESOLVED_UNIQUE"},
        "failure_envelope": {"missing": "HOLD_NO_RELEASE", "ambiguous": "HOLD_NO_RELEASE"},
        "non_claims": ["general_brep_push_pull", "persistent_topological_naming", "P0_B_DIRECT_BREP_PASS", "default_environment_promotion", "engineering_approval", "manufacturing_release", "field_truth"],
    }
    print("OLEANDER_CAD_DIRECT_EDIT_READBACK=" + json.dumps(result_payload, sort_keys=True))


if __name__ == "__main__":
    if PHASE == "PREPARE":
        prepare()
    elif PHASE == "READBACK":
        readback()
    else:
        raise SystemExit(f"unsupported OLEANDER_CAD_DIRECT_PHASE: {PHASE}")
