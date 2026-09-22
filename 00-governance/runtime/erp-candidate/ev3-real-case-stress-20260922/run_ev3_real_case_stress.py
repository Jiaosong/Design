from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ERP_ROOT = HERE.parent
REPO_ROOT = HERE.parents[3]
OUT = HERE / "output"
STAMP = "2026-09-22T16:20:00+08:00"

sys.path[:0] = [str(HERE), str(ERP_ROOT)]

from ev3_common import GENERATED_AT, MAIN_COMMIT, build_source_rows  # noqa: E402
import case_c01  # noqa: E402
import case_c04  # noqa: E402
import case_fallingwater  # noqa: E402
from build_enterprise_kernel import build_kernel  # noqa: E402
from reconcile_enterprise_kernel import reconcile  # noqa: E402
from validate_enterprise_phase1 import validate_kernel_in_memory, validate_reconciliation_in_memory  # noqa: E402
from validate_erp_candidate import validate_projection  # noqa: E402


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def sha_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest().upper()


def canonical_json_bytes(payload: dict) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def root_authority_keys(decision: dict) -> list[tuple[str, str, str, str]]:
    return [
        (row["subject_ref"], row["required_owner_kind"], row["authority_contract_ref"], row["scope"])
        for row in decision.get("unresolved_authority_requirements", [])
    ]


def run_case(name: str, module, template: Path) -> tuple[dict, dict, dict, list[dict]]:
    rows = build_source_rows(module.SOURCE_SPECS)
    for row in rows:
        assert ".worktrees" not in row["path"].replace("\\", "/"), f"{name}: source manifest leaked worktree path"
        if row["availability"] == "GIT_MAIN_EXACT":
            assert row["path"].startswith(f"git:{MAIN_COMMIT}:"), f"{name}: Git source path is not commit-stable"
    projection = module.build_projection(rows, template)
    validate_projection(projection)

    projection_path = OUT / f"{name.lower()}_enterprise_projection_v0.3.1.json"
    projection_bytes = canonical_json_bytes(projection)
    write_json(projection_path, projection)
    projection_sha = sha_bytes(projection_bytes)

    kernel = build_kernel(
        projection,
        projection_path.relative_to(REPO_ROOT).as_posix(),
        projection_sha,
        STAMP,
    )
    validate_kernel_in_memory(kernel)
    assert kernel["source_projection_ref"].startswith("00-governance/"), f"{name}: kernel source ref is not repo-relative"
    assert ".worktrees" not in kernel["source_projection_ref"], f"{name}: kernel source ref leaked worktree path"
    kernel_path = OUT / f"{name.lower()}_enterprise_kernel_v0.1.2.json"
    kernel_bytes = canonical_json_bytes(kernel)
    write_json(kernel_path, kernel)
    kernel_sha = sha_bytes(kernel_bytes)

    decision = reconcile(
        kernel,
        kernel_path.relative_to(REPO_ROOT).as_posix(),
        kernel_sha,
        STAMP,
    )
    validate_reconciliation_in_memory(decision, kernel)
    assert decision["kernel_ref"].startswith("00-governance/"), f"{name}: reconciliation kernel ref is not repo-relative"
    assert ".worktrees" not in decision["kernel_ref"], f"{name}: reconciliation kernel ref leaked worktree path"
    decision_path = OUT / f"{name.lower()}_enterprise_reconciliation_v0.1.2.json"
    write_json(decision_path, decision)

    keys = root_authority_keys(decision)
    assert len(keys) == len(set(keys)), f"{name}: authority requirement root dedup failed"
    assert decision["advance_decision"] == "HOLD", f"{name}: real-case stress unexpectedly advanced"
    assert not any(
        blocker["blocker_class"] == "CROSS_CARRIER_CONTRADICTION"
        for blocker in decision["blocking_conditions"]
    ), f"{name}: scoped quality carriers created false contradiction"

    return projection, kernel, decision, rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    template = ERP_ROOT / "example_enterprise_projection_v0.3.1.json"
    modules = {
        "C01": case_c01,
        "C04": case_c04,
        "FALLINGWATER": case_fallingwater,
    }
    source_manifest = {
        "manifest_id": "OLEANDER_ENTERPRISE_EV3_REAL_CASE_SOURCE_MANIFEST_20260922",
        "generated_at": GENERATED_AT,
        "baseline_main_commit": MAIN_COMMIT,
        "cases": {},
        "boundary": [
            "C01 local-current R1.7/downstream sources are exact local files and are not claimed as origin/main authority.",
            "C04 project-control sources are SHA-bound to exact main commit ab83fde14d0b341f373098e789be93cd527465ef.",
            "Fallingwater V06 sources are exact local diagnostics/native bytes; no P2 Project authority is inferred.",
            "Source binding does not prove Design KEEP, Professional PASS, field truth, engineering approval or Promotion.",
        ],
    }
    summary = {
        "stress_test_id": "OLEANDER_ENTERPRISE_EV3_REAL_CASE_STRESS_20260922",
        "generated_at": STAMP,
        "baseline_main_commit": MAIN_COMMIT,
        "kernel_reconciliation_revision": "v0.1.2-candidate",
        "cases": {},
        "overall_state": "HOLD",
        "promotion_eligible": False,
        "independent_review": "NOT_RUN",
        "worktree_path_independent_refs": True,
    }

    case_results = {}
    for name, module in modules.items():
        projection, kernel, decision, rows = run_case(name, module, template)
        case_results[name] = (projection, kernel, decision, rows)
        source_manifest["cases"][name] = rows
        summary["cases"][name] = {
            "projection_freshness_state": projection["reconciliation"]["projection_freshness_state"],
            "drift_state": projection["reconciliation"]["drift_state"],
            "enterprise_readiness_state": projection["reconciliation"]["enterprise_readiness_state"],
            "module_scope_counts": projection["control_metrics"]["module_scope_counts"],
            "unresolved_blocking_link_count": projection["control_metrics"]["unresolved_blocking_link_count"],
            "decision": decision["advance_decision"],
            "blocker_count": len(decision["blocking_conditions"]),
            "typed_action_count": len(decision["action_requests"]),
            "contradiction_count": len(decision["contradictions"]),
            "unresolved_authority_requirement_count": len(decision["unresolved_authority_requirements"]),
            "blocker_classes": sorted({row["blocker_class"] for row in decision["blocking_conditions"]}),
            "action_types": sorted({row["action_type"] for row in decision["action_requests"]}),
        }

    c01 = case_results["C01"][2]
    c04 = case_results["C04"][2]
    fw_projection, _, fw, fw_rows = case_results["FALLINGWATER"]
    assert c01["advance_decision"] == "HOLD" and c04["advance_decision"] == "HOLD"
    assert not c01["contradictions"] and not c04["contradictions"]
    assert fw_projection["reconciliation"]["projection_freshness_state"] == "SOURCE_READBACK_STALE"
    assert fw_projection["reconciliation"]["drift_state"] == "DIVERGED"
    assert "SOURCE_STALE" in {row["blocker_class"] for row in fw["blocking_conditions"]}
    assert not fw_projection["project_axis_refs"] and not fw_projection["work_packages"] and not fw_projection["jobs"]

    recorded = json.loads(case_fallingwater.SOURCE_SPECS[0][1].read_text(encoding="utf-8-sig"))
    current_native = next(row for row in fw_rows if row["ref"] == "EV3SRC:FW:NATIVE_BLEND")
    recorded_sha = recorded["final_saved_reopened_sha256"]
    current_sha = current_native["sha256"]
    assert recorded_sha != current_sha, "Fallingwater stale-readback stress precondition unexpectedly cleared"
    blender_exe = shutil.which("blender")
    bpy_available = importlib.util.find_spec("bpy") is not None
    invalidation = {
        "receipt_id": "FALLINGWATER_V06_NATIVE_READBACK_INVALIDATION_20260922",
        "status": "STALE_READBACK_INVALIDATED_FRESH_BLENDER_READBACK_REQUIRED",
        "source_native_path": str(case_fallingwater.SOURCE_SPECS[4][1]),
        "recorded_integrity_readback_ref": str(case_fallingwater.SOURCE_SPECS[0][1]),
        "recorded_final_sha256": recorded_sha,
        "recorded_final_bytes": recorded["final_bytes"],
        "current_native_sha256": current_sha,
        "current_native_bytes": current_native["bytes"],
        "sha_match": False,
        "fresh_blender_runtime": {
            "blender_executable": blender_exe,
            "bpy_available": bpy_available,
            "state": "NOT_AVAILABLE_IN_CURRENT_RUNTIME" if not blender_exe and not bpy_available else "AVAILABLE",
        },
        "invalidation": {
            "old_native_integrity_pass_current": False,
            "old_furniture_use_pass_current": False,
            "required_actions": [
                "RUN_FRESH_BLENDER_SAVE_REOPEN_AGAINST_CURRENT_NATIVE",
                "REGENERATE_FURNITURE_USE_AUDIT_AGAINST_FRESH_REOPENED_NATIVE",
                "REHASH_AND_REBIND_FALLINGWATER_EV3_SOURCE_MANIFEST",
            ],
        },
        "claim_ceiling": "CURRENT_NATIVE_BYTES_OBSERVED_AND_OLD_READBACK_INVALIDATED_ONLY_NO_FRESH_BLENDER_PASS",
        "does_not_prove": [
            "FRESH_SAVE_REOPEN_PASS",
            "FRESH_FURNITURE_USE_PASS",
            "DESIGN_KEEP",
            "PROFESSIONAL_PASS",
            "ENGINEERING_APPROVAL",
            "PROJECT_PROMOTION",
        ],
    }
    write_json(HERE / "FALLINGWATER_V06_NATIVE_READBACK_INVALIDATION_20260922.json", invalidation)
    write_json(HERE / "EV3_REAL_CASE_SOURCE_MANIFEST_20260922.json", source_manifest)
    write_json(HERE / "EV3_REAL_CASE_STRESS_SUMMARY_20260922.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
