"""Blender readback for the CAD Sketcher -> FreeCAD/OCCT integration probe."""

from __future__ import annotations

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
from oleander_blender.cad_sidecar import (
    CADSidecarContractError,
    assert_response_matches_request,
    bind_display_derivative,
    load_response,
    payload_sha256,
    update_stale_state,
)

ROOT = pathlib.Path(os.environ.get("OLEANDER_CAD_INTEGRATION_DIR", "/tmp/oleander-cad-integration"))
REOPEN = ROOT / "cad_sidecar_integration.blend"
checks: list[str] = []


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def read_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    if not hasattr(bpy.types.Object, "oleander"):
        oleander_blender.register()
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001

    request1 = read_json(ROOT / "request_R001.json")
    request2 = read_json(ROOT / "request_R002.json")
    response1 = load_response(ROOT / "build_R001" / "cad_build_response.json")
    response2 = load_response(ROOT / "build_R002" / "cad_build_response.json")
    display1 = read_json(ROOT / "build_R001" / "cad_display_derivative.json")
    display2 = read_json(ROOT / "build_R002" / "cad_display_derivative.json")

    assert_response_matches_request(response1, request1)
    assert_response_matches_request(response2, request2)
    checks.extend(["revision1_response_matches_request", "revision2_response_matches_request"])
    check(response1["request_sha256"] != response2["request_sha256"], "rebuild_request_sha_changed")
    check(response1["authoritative"]["step"]["sha256"] != response2["authoritative"]["step"]["sha256"], "rebuild_step_sha_changed")

    obj = bind_display_derivative(response=response1, display_payload=display1)
    bpy.context.view_layer.update()
    check(abs(obj.dimensions.x - 80.0) < 1e-3, "revision1_display_width")
    check(abs(obj.dimensions.y - 50.0) < 1e-3, "revision1_display_depth")
    check(abs(obj.dimensions.z - 10.0) < 1e-3, "revision1_display_height")
    check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "revision1_display_non_authoritative")
    check(obj["cad_request_sha256"] == payload_sha256(request1), "revision1_bound_request_sha")

    check(update_stale_state(obj, request2), "revision2_intent_marks_revision1_display_stale")
    check(bool(obj["cad_stale"]), "stale_flag_set")
    check(bool(obj.oleander.stale), "governed_stale_flag_set")

    obj = bind_display_derivative(
        response=response2,
        display_payload=display2,
        existing_object=obj,
    )
    bpy.context.view_layer.update()
    check(not bool(obj["cad_stale"]), "revision2_rebind_clears_stale")
    check(not bool(obj.oleander.stale), "revision2_governed_stale_cleared")
    check(int(obj["cad_request_revision"]) == 2, "revision2_bound_revision")
    check(obj["cad_request_sha256"] == payload_sha256(request2), "revision2_bound_request_sha")
    check(abs(obj.dimensions.x - 100.0) < 1e-3, "revision2_display_width")
    check(abs(obj.dimensions.y - 50.0) < 1e-3, "revision2_display_depth")
    check(abs(obj.dimensions.z - 10.0) < 1e-3, "revision2_display_height")
    check(obj["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "revision2_display_non_authoritative")
    check(obj["authoritative_geometry_kernel"] == "FREECAD_OCCT_BREP", "revision2_kernel_authority")

    forged = copy.deepcopy(response2)
    forged["request_sha256"] = "f" * 64
    try:
        assert_response_matches_request(forged, request2)
    except CADSidecarContractError:
        checks.append("forged_response_sha_expected_failure")
    else:
        raise AssertionError("forged_response_sha_expected_failure")

    bpy.ops.wm.save_as_mainfile(filepath=str(REOPEN))
    check(REOPEN.exists(), "integration_blend_saved")
    name = obj.name
    step_sha = obj["source_step_sha256"]
    request_sha = obj["cad_request_sha256"]
    bpy.ops.wm.open_mainfile(filepath=str(REOPEN))
    reopened = bpy.data.objects.get(name)
    check(reopened is not None, "integration_blend_reopen")
    check(reopened["ole_id"] == "OLE_PRO_CAD_BRACKET_001", "ole_id_reopen")
    check(int(reopened["cad_request_revision"]) == 2, "revision_reopen")
    check(reopened["cad_request_sha256"] == request_sha, "request_sha_reopen")
    check(reopened["source_step_sha256"] == step_sha, "step_sha_reopen")
    check(reopened["geometry_authority"] == "DISPLAY_DERIVATIVE_ONLY", "authority_reopen")

    result = {
        "schema": "OLEANDER_CAD_SIDECAR_INTEGRATION_READBACK_v0.1",
        "status": "PASS",
        "blender": bpy.app.version_string,
        "checks": checks,
        "authority": {
            "source_intent": "CAD Sketcher + SolveSpace",
            "master": "FreeCAD/OCCT B-Rep",
            "blender": "DISPLAY_DERIVATIVE_ONLY",
        },
        "non_claims": [
            "P0_A_PARAMETRIC_CAD_PASS",
            "general_feature_tree",
            "general_direct_brep",
            "assembly_mates",
        ],
    }
    print("OLEANDER_CAD_SIDECAR_INTEGRATION=" + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
