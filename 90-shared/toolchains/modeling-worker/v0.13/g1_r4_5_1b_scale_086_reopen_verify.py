#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import g1_geometry_core as base
import g1_r2_blender_roundtrip as rt
import g1_r2_core as r2
import g1_r2_topology_isolation as iso


REBUILD_TEXT = "OLEANDER_G1_R2_REBUILD.py"
LIVE_TEXT = "OLEANDER_G1_R2_LIVE_SOURCE.json"
RELATION_TEXT = "OLEANDER_G1_R4_5_1B_CONFIRMED_RELATION.json"
CANDIDATE_OBJECT = "OL_DERIVED_G1_R4_5_1B_CONFIRM_SCALE_086"


def args():
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--r2-correction", required=True)
    p.add_argument("--confirmation", required=True)
    p.add_argument("--out", required=True)
    return p.parse_args(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:])


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def verts(name):
    obj = bpy.data.objects.get(name)
    if obj is None or obj.type != "MESH":
        raise RuntimeError(f"missing mesh: {name}")
    return [tuple(float(v) for v in point.co) for point in obj.data.vertices]


def max_disp(a, b):
    if len(a) != len(b):
        return math.inf
    return max((math.dist(x, y) for x, y in zip(a, b)), default=0.0)


def run_embedded_rebuild():
    block = bpy.data.texts.get(REBUILD_TEXT)
    if block is None:
        raise RuntimeError(f"missing embedded text: {REBUILD_TEXT}")
    scope = {"__name__": "__main__", "__file__": f"<blender-text:{REBUILD_TEXT}>"}
    exec(compile(block.as_string(), scope["__file__"], "exec"), scope, scope)


def main():
    a = args()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    confirmation = load(a.confirmation)
    seed = load(a.source)
    correction = load(a.r2_correction)
    template = r2.apply(seed, correction)
    selected = confirmation["selected_relation"]

    lower = bpy.data.objects.get(rt.NAMES["LOWER_RETURN_PROFILE"])
    deck = bpy.data.objects.get(rt.NAMES["INTERFACE_DECK_BOUNDARY"])
    candidate = bpy.data.objects.get(CANDIDATE_OBJECT)
    embedded_live = bpy.data.texts.get(LIVE_TEXT)
    embedded_relation = bpy.data.texts.get(RELATION_TEXT)

    checks = {
        "opened_expected_saved_blend": Path(bpy.data.filepath).name == confirmation["outputs"]["blend"],
        "six_native_source_objects_present": all(bpy.data.objects.get(name) is not None for name in rt.NAMES.values()),
        "lower_return_source_present": lower is not None,
        "interface_source_present": deck is not None,
        "candidate_derived_present": candidate is not None,
        "embedded_live_source_present": embedded_live is not None,
        "embedded_relation_present": embedded_relation is not None,
        "embedded_rebuild_present": bpy.data.texts.get(REBUILD_TEXT) is not None,
    }
    if not all(checks.values()):
        report = {"status": "R4_5_1B_SCALE_086_REOPEN_PERSISTENCE_FAIL", "checks": checks}
        (out / confirmation["outputs"]["reopen_report"]).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return 18

    relation_payload = json.loads(embedded_relation.as_string())
    embedded_source = json.loads(embedded_live.as_string())
    actual_source = rt.extract_native_source(template)
    actual_digest = iso.source_digest(actual_source)
    embedded_digest = iso.source_digest(embedded_source)
    snapshot = load(out / confirmation["outputs"]["native_source_snapshot"])
    actual_readback, actual_diffs, authority = rt.authority_checks(actual_source)
    low = base.own(actual_source, "LOWER_RETURN_PROFILE")
    interface = base.own(actual_source, "INTERFACE_DECK_BOUNDARY")
    before_rebuild = verts(CANDIDATE_OBJECT)

    checks.update(
        {
            "exact_onset_0_88_persisted": abs(float(lower["termination_cap_onset_u"]) - 0.88) <= 1e-12,
            "exact_scale_0_86_persisted": abs(float(lower["termination_cap_pole_curvature_scale"]) - 0.86) <= 1e-12,
            "two_numeric_dofs_persisted": int(lower["termination_cap_numeric_dof_count"]) == 2,
            "cap_law_persisted": lower.get("termination_cap_law") == r2.CAP_LAW,
            "cap_semantics_persisted": lower.get("termination_cap_semantics") == r2.CAP_SEMANTICS,
            "cap_endpoint_persisted": lower.get("termination_cap_endpoint_section") == r2.CAP_ENDPOINT_SECTION,
            "termination_envelope_0_34_persisted": abs(float(lower["termination_envelope_exponent"]) - 0.34) <= 1e-12,
            "confirmed_interface_persisted": abs(float(interface["u_center"]) - 0.62) <= 1e-12
            and abs(float(interface["u_halfspan"]) - 0.26) <= 1e-12
            and abs(float(interface["theta_halfspan_rad"]) - 1.06) <= 1e-12
            and abs(float(interface["core_fraction"]) - 0.29) <= 1e-12
            and abs(float(interface["depth_m"]) - 0.012) <= 1e-12,
            "embedded_relation_matches_contract": relation_payload["selected_relation"] == selected,
            "embedded_source_matches_native_digest": embedded_digest == actual_digest,
            "snapshot_digest_matches_native": snapshot["live_source_digest"] == actual_digest,
            "scene_digest_matches_native": bpy.context.scene.get("OLEANDER_LIVE_SOURCE_DIGEST") == actual_digest,
            "native_authority_checks_pass": all(authority.values()),
            "native_readback_self_consistent": iso.source_digest(actual_readback) == actual_digest and max(actual_diffs.values()) <= 1e-8,
            "candidate_is_derived_not_authority": candidate.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_NOT_AUTHORITY",
            "scene_authority_is_working_source": bpy.context.scene.get("OLEANDER_AUTHORITY_STATE") == "WORKING_SOURCE",
            "scene_stage_is_exact_confirmation": bpy.context.scene.get("OLEANDER_STAGE") == "R4_5_1B_EXACT_SCALE_086_CONFIRMATION",
            "candidate_promotion_not_run": bpy.context.scene.get("OLEANDER_CANDIDATE_PROMOTION") == "NOT_RUN",
        }
    )

    run_embedded_rebuild()
    rebuilt = verts(CANDIDATE_OBJECT)
    rebuild_error = max_disp(before_rebuild, rebuilt)
    rebuilt_obj = bpy.data.objects[CANDIDATE_OBJECT]
    rebuilt_live = json.loads(bpy.data.texts[LIVE_TEXT].as_string())
    checks.update(
        {
            "reopen_rebuild_targets_exact_candidate": rebuilt_obj is not None,
            "reopen_rebuild_geometry_matches_saved_candidate": rebuild_error <= 1e-8,
            "reopen_rebuild_remains_non_authority": rebuilt_obj.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_NOT_AUTHORITY",
            "reopen_rebuild_cap_aware_marker": bpy.context.scene.get("OLEANDER_LAST_NATIVE_REBUILD_CAP_AWARE") is True,
            "reopen_rebuild_keeps_onset_0_88": abs(float(rebuilt_live["termination_cap"]["onset_u"]) - 0.88) <= 1e-12,
            "reopen_rebuild_keeps_scale_0_86": abs(float(rebuilt_live["termination_cap"]["pole_curvature_scale"]) - 0.86) <= 1e-12,
        }
    )

    status = "R4_5_1B_SCALE_086_REOPEN_PERSISTENCE_PASS" if all(checks.values()) else "R4_5_1B_SCALE_086_REOPEN_PERSISTENCE_FAIL"
    report = {
        "schema": "oleander.modeling-worker.v0.13.g1.r4.5.1b.scale-086-reopen-persistence.v1",
        "status": status,
        "blend": Path(bpy.data.filepath).name,
        "source_digest": actual_digest,
        "saved_candidate_vertex_count": len(before_rebuild),
        "rebuilt_candidate_vertex_count": len(rebuilt),
        "rebuild_max_displacement_m": rebuild_error,
        "checks": checks,
        "authority_state": "WORKING_SOURCE",
        "design_state": "REVISE / EXACT_VISUAL_DECISION_PENDING",
        "candidate_promotion": "NOT_RUN",
        "boundary": "This proves the saved Blender file reopens with the frozen .88/.86 native Source relation intact and can self-rebuild the exact cap-aware derived candidate without repository modules. It does not provide the required Human Visual decision or authorize promotion.",
    }
    (out / confirmation["outputs"]["reopen_report"]).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if status.endswith("PASS") else 18


if __name__ == "__main__":
    raise SystemExit(main())
