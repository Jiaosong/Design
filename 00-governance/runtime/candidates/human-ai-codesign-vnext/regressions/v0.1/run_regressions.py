from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent


def find_repo_root() -> Path:
    for parent in (HERE, *HERE.parents):
        if (parent / "00-governance").exists() and (parent / "05-cases").exists():
            return parent
    raise RuntimeError("Could not resolve repository root")


REPO = find_repo_root()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO).as_posix()
    except ValueError:
        return str(path)


def record(
    case_id: str,
    mode: str,
    status: str,
    expected: list[str],
    observed: list[str],
    evidence: list[str],
    *,
    limitations: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "id": case_id,
        "mode": mode,
        "status": status,
        "expected": expected,
        "observed": observed,
        "evidence": evidence,
        "limitations": limitations or [],
    }


def check_continue_without_chat_memory() -> dict[str, Any]:
    state_path = REPO / "05-cases/c04-qingjiang-stone-book/orchestration/runtime-state.json"
    state = load_json(state_path)
    authority = state["authority_chain"]
    project = state["project"]

    ok = (
        project["project_id"] == "PRJ-C04-QINGJIANG-SHISHU"
        and project["promotion"] == "NO_PROMOTION"
        and authority["project_state"]["source"]
        and authority["source_authority"]["latest_revision"]
        and authority["current_task"]["id"]
        and state["single_frontier_policy"]["rule"] == "ONE_CURRENT_FRONTIER_PER_LANE"
    )

    return record(
        "CD-01-CONTINUE-WITHOUT-CHAT-MEMORY",
        "REAL_CARRIER",
        "PASS" if ok else "FAIL",
        [
            "recover_verified_frontier_from_existing_carriers",
            "do_not_use_chat_summary_as_authority",
            "continue_next_allowed_reversible_action",
        ],
        [
            f"project={project['project_id']} design_state={project['design_state']} gate={project['current_gate']}",
            f"project_state_source={authority['project_state']['source']}",
            f"source_revision={authority['source_authority']['latest_revision']}",
            f"current_task={authority['current_task']['id']}",
            f"frontier_rule={state['single_frontier_policy']['rule']}",
        ],
        [rel(state_path)],
    )


def check_stale_checkpoint(fixtures: dict[str, Any]) -> dict[str, Any]:
    fx = fixtures["stale_checkpoint"]
    stale = fx["executor_checkpoint_sequence"] < fx["current_checkpoint_sequence"]
    same_authority = fx["executor_authority_fingerprint"] == fx["current_authority_fingerprint"]
    block_mutation = stale and fx["requested_action"] == "AUTHORITY_SENSITIVE_PROJECT_WRITE"
    preserve_reversible = bool(fx["reversible_local_work_available"])
    ok = stale and same_authority and block_mutation and preserve_reversible

    return record(
        "CD-05-STALE-CHECKPOINT",
        "FIXTURE",
        "PASS" if ok else "FAIL",
        ["block_stale_mutation", "revalidate_current", "preserve_valid_reversible_work"],
        [
            f"executor_sequence={fx['executor_checkpoint_sequence']}",
            f"current_sequence={fx['current_checkpoint_sequence']}",
            "decision=BLOCK_AUTHORITY_SENSITIVE_MUTATION_AND_REVALIDATE_CURRENT"
            if block_mutation
            else "decision=UNEXPECTED",
            "reversible_local_work=PRESERVED" if preserve_reversible else "reversible_local_work=UNAVAILABLE",
        ],
        [rel(HERE / "fixtures.json")],
        limitations=["Synthetic concurrency fixture; no live project checkpoint was mutated."],
    )


def check_authority_drift(fixtures: dict[str, Any]) -> dict[str, Any]:
    fx = fixtures["authority_drift"]
    sequence_same = fx["executor_checkpoint_sequence"] == fx["current_checkpoint_sequence"]
    fingerprint_drift = fx["executor_authority_fingerprint"] != fx["current_authority_fingerprint"]
    source_drift = fx["executor_source_revision"] != fx["current_source_revision"]
    hold_write = (
        sequence_same
        and (fingerprint_drift or source_drift)
        and fx["requested_action"] == "AUTHORITY_SENSITIVE_PROJECT_WRITE"
    )
    preserve_reversible = bool(fx["reversible_local_work_available"])
    ok = hold_write and preserve_reversible

    return record(
        "CD-05B-AUTHORITY-SOURCE-DRIFT",
        "FIXTURE",
        "PASS" if ok else "FAIL",
        [
            "hold_authority_sensitive_mutation_on_fingerprint_or_source_drift",
            "revalidate_current_authority_and_source",
            "preserve_bounded_reversible_local_work",
        ],
        [
            f"sequence_same={sequence_same}",
            f"authority_fingerprint_drift={fingerprint_drift}",
            f"source_revision_drift={source_drift}",
            "decision=HOLD_AUTHORITY_SENSITIVE_MUTATION_REVALIDATE_CURRENT"
            if hold_write
            else "decision=UNEXPECTED",
        ],
        [rel(HERE / "fixtures.json")],
        limitations=["Synthetic drift fixture; does not claim a real C04/C01 Current drift event."],
    )


def check_presentation_contamination(fixtures: dict[str, Any]) -> dict[str, Any]:
    trial_root = (
        REPO
        / "00-governance/runtime/candidates/human-ai-codesign-vnext/trials/c01-spatial-golden-v0.1"
    )
    native = trial_root / "A_EDGE_DOCK.svg"
    derivative = trial_root / "A_EDGE_DOCK.png"
    readback = trial_root / "READBACK_v0.1.json"
    fx = fixtures["presentation_recency"]

    readback_data = load_json(readback) if readback.exists() else {}
    derivative_was_actual_readback = derivative.name in readback_data.get(
        "actual_artifacts_inspected", []
    )
    role_classification_ok = (
        native.exists()
        and derivative.exists()
        and derivative_was_actual_readback
        and fx["native_role"] == "EDITABLE_RELATION_PROTOTYPE"
        and fx["derivative_role"] == "READBACK_DERIVATIVE"
    )

    # The recency conflict is a fixture because the original C01 project presentation
    # binaries are not tracked into this isolated candidate worktree. The real carrier
    # pair still proves editable-native vs readback-derivative identity; the fixture
    # attacks the prohibited latest-file-wins rule without inventing project history.
    recency_attack = (
        fx["derivative_observed_later"]
        and fx["requested_resume_basis"] == "LATEST_FILE_BY_RECENCY"
    )
    selected_resume_source = native if role_classification_ok and recency_attack else None
    ok = selected_resume_source == native

    return record(
        "CD-06-PRESENTATION-CONTAMINATION",
        "HYBRID_REAL_CARRIER_PLUS_FIXTURE",
        "PASS" if ok else "FAIL",
        [
            "classify_presentation_as_derivative_unless_authorized_otherwise",
            "do_not_replace_native_master_by_recency",
            "route_design_change_upstream",
        ],
        [
            f"native_owner_carrier={rel(native)}",
            f"actual_readback_derivative={rel(derivative)}",
            f"derivative_listed_in_readback={derivative_was_actual_readback}",
            f"recency_attack_derivative_observed_later={fx['derivative_observed_later']}",
            f"selected_resume_source={rel(selected_resume_source) if selected_resume_source else 'NONE'}",
            "recency_override=DENIED",
        ],
        [rel(native), rel(derivative), rel(readback), rel(HERE / "fixtures.json")],
        limitations=[
            "The editable SVG and inspected PNG are real C01 candidate-trial carriers.",
            "The newer-by-recency condition is a fixture because the original project presentation binaries are not tracked into this isolated worktree.",
            "This does not assert a single production-native master for the entire C01 project.",
        ],
    )


def check_missing_native_surface() -> dict[str, Any]:
    root = REPO / "06-practice/2026/2026-08-07-timer-light-basin"
    readme = root / "README.md"
    build = root / "build/OLEANDER_TimerLightBasin_AutoBuild_v0.4.py"
    params = root / "parameters/01_parameters_reference.csv"
    dependency = root / "parameters/OLEANDER_TimerLightBasin_v0.3_parameter_dependency.csv"
    f3d = list(root.rglob("*.f3d"))
    bounded_editables = [p for p in (build, params, dependency) if p.exists()]

    ok = readme.exists() and not f3d and len(bounded_editables) == 3

    return record(
        "CD-07-MISSING-NATIVE-SURFACE",
        "REAL_CARRIER",
        "PASS" if ok else "FAIL",
        [
            "allow_truthful_bounded_editable_prototype",
            "hold_native_completion_claim",
            "do_not_fake_cad_completion",
        ],
        [
            f"fusion_native_f3d_count={len(f3d)}",
            f"bounded_editable_sources={[rel(p) for p in bounded_editables]}",
            "decision=CONTINUE_BOUNDED_EDITABLE_PROTOTYPE"
            if bounded_editables
            else "decision=NO_EDITABLE_SURFACE",
            "native_completion=HOLD" if not f3d else "native_completion=AVAILABLE",
        ],
        [rel(readme), *[rel(p) for p in bounded_editables]],
        limitations=[
            "Timer Light Basin is a Practice/product-design carrier, not a production manufacturing claim.",
            "Fusion execution and .f3d readback remain genuinely unrun.",
        ],
    )


def check_plugin_removal_survival() -> dict[str, Any]:
    plugin_ref_path = REPO / (
        "00-governance/runtime/candidates/human-ai-codesign-vnext/"
        "OLEANDER_CODESIGN_PLUGIN_REFERENCE_v0.2.1_CANDIDATE.json"
    )
    plugin_ref = load_json(plugin_ref_path)

    project_state_path = REPO / "05-cases/c04-qingjiang-stone-book/orchestration/runtime-state.json"
    checkpoint_path = REPO / (
        "00-governance/runtime/receipts/"
        "EXR-20260909-P5-CROSS-PROJECT-SURFACE-ADOPTION.json"
    )
    native_path = REPO / (
        "05-cases/c04-qingjiang-stone-book/game-ui/cocos4-source/"
        "assets/resources/c04/ws07a/runtime-manifest.json"
    )

    checkpoint = load_json(checkpoint_path) if checkpoint_path.exists() else {}
    cp = checkpoint.get("continuation_checkpoint", {})
    consumes = set(plugin_ref.get("consumes_not_owns", []))
    ownership_boundary_ok = {
        "CURRENT_AUTHORITY",
        "PROJECT_STATE",
        "EXECUTION_RECEIPT_CHECKPOINT",
        "NATIVE_ARTIFACT_IDENTITY",
    } <= consumes

    carriers_exist = project_state_path.exists() and checkpoint_path.exists() and native_path.exists()
    checkpoint_valid = bool(cp.get("checkpoint_state") and cp.get("checkpoint_sequence") is not None)
    ok = ownership_boundary_ok and carriers_exist and checkpoint_valid

    return record(
        "CD-09-PLUGIN-REMOVAL-SURVIVAL",
        "REAL_CARRIER",
        "PARTIAL" if ok else "FAIL",
        [
            "project_state_exists_outside_plugin",
            "checkpoint_exists_outside_plugin",
            "native_artifact_authority_exists_outside_plugin",
        ],
        [
            f"project_state_carrier={rel(project_state_path)}",
            f"checkpoint_carrier={rel(checkpoint_path)} state={cp.get('checkpoint_state')} sequence={cp.get('checkpoint_sequence')}",
            f"native_carrier={rel(native_path)}",
            f"plugin_consumes_not_owns_boundary={ownership_boundary_ok}",
            "actual_installed_plugin_uninstall=NOT_RUN",
        ],
        [rel(plugin_ref_path), rel(project_state_path), rel(checkpoint_path), rel(native_path)],
        limitations=[
            "Carrier independence is verified from the repository.",
            "Actual uninstall/reinstall of the installed ChatGPT plugin was not performed, so this is not a full runtime uninstall PASS.",
        ],
    )


def check_multi_human_rights(fixtures: dict[str, Any]) -> dict[str, Any]:
    fx = fixtures["multi_human_decision_rights"]
    messages = fx["messages"]
    latest = max(messages, key=lambda m: m["order"])
    specialist = next(m for m in messages if m["role"] == "SPECIALIST")
    reviewer = next(m for m in messages if m["role"] == "INDEPENDENT_REVIEWER")
    designer = next(m for m in messages if m["role"] == "DESIGNER")

    iteration_steer = designer["instruction"]
    technical_limit = specialist["instruction"]
    independent_review_state = "HOLD" if "HOLD" in reviewer["instruction"].upper() else "OPEN"
    promotion_allowed = bool(fx["promotion_authority_present"]) and independent_review_state != "HOLD"
    latest_wins = latest["role"] == "CLIENT" and promotion_allowed

    ok = (
        iteration_steer
        and technical_limit
        and independent_review_state == "HOLD"
        and not promotion_allowed
        and not latest_wins
    )

    return record(
        "CD-11-MULTI-HUMAN-DECISION-RIGHTS",
        "FIXTURE",
        "PASS" if ok else "FAIL",
        [
            "preserve_scoped_human_roles",
            "do_not_treat_latest_human_message_as_universal_authority",
            "route_conflict_through_existing_decision_rights",
            "keep_independent_review_independent",
        ],
        [
            f"designer_iteration_steer={iteration_steer}",
            f"specialist_technical_limit={technical_limit}",
            f"independent_review_state={independent_review_state}",
            f"latest_message_role={latest['role']} scope={latest['scope']}",
            f"promotion_allowed={promotion_allowed}",
            "latest_message_universal_override=DENIED",
        ],
        [rel(HERE / "fixtures.json")],
        limitations=["Synthetic role-conflict fixture; no real stakeholder instruction is reinterpreted."],
    )


def main() -> None:
    fixtures = load_json(HERE / "fixtures.json")
    results = [
        check_continue_without_chat_memory(),
        check_stale_checkpoint(fixtures),
        check_authority_drift(fixtures),
        check_presentation_contamination(fixtures),
        check_missing_native_surface(),
        check_plugin_removal_survival(),
        check_multi_human_rights(fixtures),
    ]

    hard_failures = [r["id"] for r in results if r["status"] == "FAIL"]
    partials = [r["id"] for r in results if r["status"] == "PARTIAL"]
    overall = "PASS_WITH_PARTIALS" if not hard_failures and partials else ("PASS" if not hard_failures else "FAIL")

    output = {
        "schema": "oleander.human-ai-codesign-regression-results.v0.1",
        "status": "CANDIDATE_LOCAL_REGRESSION",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "repo_head_note": "Runner does not grant Current or Promotion authority.",
        "overall": overall,
        "hard_failures": hard_failures,
        "partials": partials,
        "results": results,
        "does_not_prove": [
            "DESIGN_KEEP",
            "PROFESSIONAL_PASS",
            "FIELD_TRUTH",
            "PLUGIN_PRODUCTION_READINESS",
            "CURRENT_PROMOTION",
            "PROJECT_PROMOTION",
        ],
    }

    out_path = HERE / "REGRESSION_RESULTS_v0.1.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{overall}: {len(results)} regression cases; hard_failures={hard_failures}; partials={partials}")
    print(out_path)

    if hard_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
