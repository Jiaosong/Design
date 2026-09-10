"""Real Blender 5.2 -> CAD sidecar -> FreeCAD -> Blender readback for bounded FACE_TANGENT_MOVE.

This is an additional operation case inside the existing CAD Sidecar Integration job,
not a Runtime stage, Frontier family, or general planar direct-modeling claim.
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
    DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE,
    assert_direct_edit_response_matches_request,
    bind_direct_edit_display_derivative,
    build_direct_edit_request_from_intent,
    file_sha256,
    load_direct_edit_response,
    payload_sha256,
    validate_direct_edit_request,
    write_direct_edit_request,
)

ROOT = pathlib.Path(os.environ.get("OLEANDER_CAD_DIRECT_INTEGRATION_DIR", "/tmp/oleander-cad-direct-integration"))
PHASE = os.environ.get("OLEANDER_CAD_TANGENT_PHASE", "PREPARE").strip().upper()
OLE_ID = "OLE_CAD_DIRECT_EXECUTION_001"
SUCCESS_REQUEST = ROOT / "tangent_request_success.json"
MISSING_REQUEST = ROOT / "tangent_request_missing.json"
AMBIGUOUS_REQUEST = ROOT / "tangent_request_ambiguous.json"
REOPEN = ROOT / "cad_direct_tangent_execution.blend"
checks: list[str] = []

def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)

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
    check(len(candidates) == 1, "prepare_tangent_unique_positive_z_face")
    candidates[0].select = True
    bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)

def vertex_snapshot(obj):
    return tuple(tuple(round(float(v), 9) for v in vertex.co) for vertex in obj.data.vertices)

def prepare_box_display(master_locator: str):
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    obj = bpy.context.active_object
    obj.name = "OLE_CAD_TANGENT_DISPLAY"
    obj.oleander.ole_id = OLE_ID
    result = bpy.ops.oleander.apply_metric_dimensions(x_mm=80.0, y_mm=50.0, z_mm=10.0)
    check("FINISHED" in result, "prepare_tangent_display_dimensions")
    for vertex in obj.data.vertices:
        vertex.co.z += 5.0
    obj.data.update()
    bpy.context.view_layer.update()
    obj.oleander.master_type = "CAD_NATIVE"
    obj.oleander.master_locator = master_locator
    obj.oleander.geometry_authority = "VISUAL_ONLY"
    return obj

def prepare() -> None:
    if hasattr(bpy.types.Object, "oleander"):
        try:
            oleander_blender.unregister()
        except Exception:
            pass
    oleander_blender.register()
    clear_scene()
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 0.001
    master_fcstd = ROOT / "base" / f"{OLE_ID}_R001.FCStd"
    obj = prepare_box_display(str(master_fcstd))
    before = vertex_snapshot(obj)
    select_top_face(obj)
    result = bpy.ops.oleander.direct_face_tangent_move(u_mm=3.0, v_mm=4.0)
    check("FINISHED" in result, "prepare_real_cad_native_tangent_operator")
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.update()
    check(vertex_snapshot(obj) == before, "prepare_tangent_display_geometry_unchanged")
    check(obj.get("oleander_cad_direct_edit_state") == "PENDING_SIDECAR", "prepare_tangent_pending_sidecar")
    intent = json.loads(obj["oleander_cad_direct_edit_intent"])
    check(intent["operation"] == DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE, "prepare_tangent_operation")
    check(intent["parameters"]["translation_local_mm"] == [3.0, 4.0, 0.0], "prepare_tangent_normalized_translation")
    check(intent["parameters"]["u_mm"] == 3.0 and intent["parameters"]["v_mm"] == 4.0, "prepare_tangent_uv_provenance")

    cases = {
        "success": str(master_fcstd),
        "missing": str(ROOT / "hold_missing" / "missing.FCStd"),
        "ambiguous": str(ROOT / "hold_ambiguous" / "ambiguous.FCStd"),
    }
    for name, locator in cases.items():
        candidate = copy.deepcopy(intent)
        candidate["authority"]["master_locator"] = locator
        request = build_direct_edit_request_from_intent(
            request_id=f"OLE_CAD_TANGENT_{name.upper()}_R003",
            revision=3,
            intent=candidate,
        )
        validate_direct_edit_request(request)
        check(request["operation"] == {"kind": DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE, "translation_local_mm": [3.0, 4.0, 0.0]}, f"prepare_{name}_normalized_request")
        check(request["authority"]["execution_state"] == "NOT_EXECUTED", f"prepare_{name}_not_executed")
        target = {"success": SUCCESS_REQUEST, "missing": MISSING_REQUEST, "ambiguous": AMBIGUOUS_REQUEST}[name]
        write_direct_edit_request(target, request)
        check(payload_sha256(request) == payload_sha256(read_json(target)), f"prepare_{name}_request_sha_readback")

    payload = {
        "schema": "OLEANDER_CAD_DIRECT_TANGENT_PREPARE_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "translation_local_mm": [3.0, 4.0, 0.0],
        "authority": {"master": "FREECAD_OCCT_BREP", "blender": "DISPLAY_DERIVATIVE_ONLY", "execution": "NOT_EXECUTED"},
        "non_claims": ["general_planar_face_translation", "oblique_face_execution", "general_brep_push_pull", "P0_B_DIRECT_BREP_PASS", "P0_G_MODELING_INTERACTION_PASS"],
    }
    print("OLEANDER_CAD_DIRECT_TANGENT_PREPARE=" + json.dumps(payload, sort_keys=True))

def validate_response(response: dict, request: dict, status: str, resolution_state: str) -> None:
    assert_direct_edit_response_matches_request(response, request)
    check(response["status"] == status, f"{status}_status")
    check(response["resolution"]["state"] == resolution_state, f"{status}_resolution")
    check(response["operation"]["kind"] == DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE, f"{status}_tangent_kind")
    check(response["operation"]["translation_local_mm"] == [3.0, 4.0, 0.0], f"{status}_translation")
    if status == "PASS":
        check(response["operation"]["execution_state"] == "EXECUTED", "pass_tangent_executed")
        for artifact in ("fcstd", "step", "brep"):
            record = response["authoritative"][artifact]
            path = pathlib.Path(record["path"])
            check(path.is_file() and file_sha256(path) == record["sha256"], f"pass_tangent_{artifact}_sha")
    else:
        check(response["operation"]["execution_state"] == "NOT_EXECUTED", f"{status}_tangent_not_executed")

def readback() -> None:
    if hasattr(bpy.types.Object, "oleander"):
        try:
            oleander_blender.unregister()
        except Exception:
            pass
    oleander_blender.register()
    clear_scene()
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 0.001
    requests = {name: read_json(path) for name, path in {"success": SUCCESS_REQUEST, "missing": MISSING_REQUEST, "ambiguous": AMBIGUOUS_REQUEST}.items()}
    for name, request in requests.items():
        validate_direct_edit_request(request)
        checks.append(f"readback_{name}_request_revalidated")
    responses = {
        "success": load_direct_edit_response(ROOT / "tangent_direct_success" / "cad_direct_edit_response.json"),
        "missing": load_direct_edit_response(ROOT / "tangent_direct_missing" / "cad_direct_edit_response.json", allow_hold=True),
        "ambiguous": load_direct_edit_response(ROOT / "tangent_direct_ambiguous" / "cad_direct_edit_response.json", allow_hold=True),
    }
    validate_response(responses["success"], requests["success"], "PASS", "RESOLVED_UNIQUE")
    validate_response(responses["missing"], requests["missing"], "HOLD", "MISSING_HOLD")
    validate_response(responses["ambiguous"], requests["ambiguous"], "HOLD", "AMBIGUOUS_HOLD")
    check(responses["ambiguous"]["resolution"]["candidate_count"] == 2, "tangent_ambiguous_two_candidates")

    measurements = responses["success"]["measurements"]
    check(all(abs(a-b) <= 1e-4 for a,b in zip(measurements["source_bbox_mm"], [80.0, 50.0, 10.0])), "tangent_source_bbox")
    check(all(abs(a-b) <= 1e-4 for a,b in zip(measurements["result_bbox_mm"], [83.0, 54.0, 10.0])), "tangent_result_bbox")
    check(abs(measurements["source_volume_mm3"] - 40000.0) <= 1e-3, "tangent_source_volume")
    check(abs(measurements["result_volume_mm3"] - 40000.0) <= 1e-3, "tangent_volume_preserved")

    display = read_json(ROOT / "tangent_direct_success" / "cad_direct_edit_display_derivative.json")
    obj = bind_direct_edit_display_derivative(response=responses["success"], display_payload=display, request=requests["success"])
    bpy.context.view_layer.update()
    check(abs(obj.dimensions.x - 83.0) <= 1e-3, "tangent_blender_width")
    check(abs(obj.dimensions.y - 54.0) <= 1e-3, "tangent_blender_depth")
    check(abs(obj.dimensions.z - 10.0) <= 1e-3, "tangent_blender_height")
    check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "tangent_blender_display_only")
    check(obj["cad_direct_edit_operation_kind"] == DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE, "tangent_operation_bound")
    check(list(obj["cad_direct_edit_translation_local_mm"]) == [3.0, 4.0, 0.0], "tangent_translation_bound")

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    name = obj.name
    request_sha = obj["cad_request_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    reopened = bpy.data.objects.get(name)
    check(reopened is not None, "tangent_reopen_object")
    check(reopened["cad_request_sha256"] == request_sha, "tangent_reopen_request_sha")
    check(reopened["cad_direct_edit_execution_state"] == "EXECUTED", "tangent_reopen_execution")
    check(reopened["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "tangent_reopen_display_only")

    payload = {
        "schema": "OLEANDER_CAD_DIRECT_TANGENT_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "translation_local_mm": [3.0, 4.0, 0.0],
        "result_bbox_mm": [83.0, 54.0, 10.0],
        "result_volume_mm3": 40000.0,
        "authority": {"master": "FREECAD_OCCT_BREP", "blender": "DISPLAY_DERIVATIVE_ONLY", "execution": "EXECUTED", "resolution": "RESOLVED_UNIQUE"},
        "failure_envelope": {"missing": "HOLD_NO_RELEASE", "ambiguous": "HOLD_NO_RELEASE"},
        "non_claims": ["general_planar_face_translation", "oblique_face_execution", "general_brep_push_pull", "persistent_topological_naming", "P0_B_DIRECT_BREP_PASS", "P0_G_MODELING_INTERACTION_PASS", "default_environment_promotion"],
    }
    print("OLEANDER_CAD_DIRECT_TANGENT_READBACK=" + json.dumps(payload, sort_keys=True))

if __name__ == "__main__":
    if PHASE == "PREPARE":
        prepare()
    elif PHASE == "READBACK":
        readback()
    else:
        raise SystemExit(f"unsupported OLEANDER_CAD_TANGENT_PHASE: {PHASE}")
