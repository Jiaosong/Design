from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PIPELINE = ROOT / "oleander-skills" / "oleander-3d-pipeline"
RUNTIME = PIPELINE / "blender_runtime"
GOV = RUNTIME / "CANDIDATE_GOVERNANCE.json"
STATUS = PIPELINE / "PROFESSIONAL_PARITY_STATUS.json"
SKILL = PIPELINE / "SKILL.md"
WORKBENCH_EXTENSION = PIPELINE / "BLENDER_RUNTIME_WORKBENCH_EXTENSION.md"
RUNTIME_README = RUNTIME / "README.md"
WORKFLOWS = ROOT / ".github" / "workflows"


def fail(message: str) -> None:
    raise AssertionError(message)


def check(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def assert_review_boundary_workflow(relative: str) -> None:
    workflow_path = ROOT / relative
    check(workflow_path.exists(), f"review-boundary workflow missing: {relative}")
    text = workflow_path.read_text(encoding="utf-8")
    check("  pull_request:\n" in text and "\n  push:\n" in text, f"review-boundary trigger blocks missing: {relative}")
    pull_block = text.split("  pull_request:\n", 1)[1].split("\n  push:\n", 1)[0]
    check("    types: [ready_for_review]\n" in pull_block, f"historical baseline must not run on Draft synchronize: {relative}")
    check("synchronize" not in pull_block, f"historical baseline cannot re-enable Draft synchronize: {relative}")
    push_block = text.split("\n  push:\n", 1)[1]
    check("    branches:\n      - main\n" in push_block, f"historical baseline must preserve push-main regression: {relative}")


def main() -> None:
    governance = json.loads(GOV.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))

    check(governance["authority"]["main_is_only_installed_current"] is True, "main must remain only installed CURRENT")
    check(governance["authority"]["candidate_may_not_self_promote"] is True, "candidate self-promotion must be disabled")
    check(governance["authority"]["promotion_state"] != "PROMOTED", "candidate governance cannot already be promoted")
    check(status["default_environment_eligible"] is False, "default environment must remain ineligible during candidate governance hold")
    check(status["p0"]["P0_B_DIRECT_BREP"]["state"] != "PASS", "P0-B cannot PASS while recorded blockers remain")

    project_wide = governance["project_wide_governance"]
    check(project_wide["authority"] == "main/00-governance/OLEANDER_ANTI_POLLUTION_PROTOCOL_v1.0.md", "Blender candidate must inherit canonical project-wide protocol from main")
    check(project_wide["machine_contract"] == "main/00-governance/OLEANDER_ANTI_POLLUTION_CONTRACT_CURRENT.json", "Blender candidate must inherit project-wide machine contract from main")
    check(project_wide["inherit_without_fork"] is True, "Blender candidate may not fork project-wide anti-pollution governance")
    check(project_wide["blender_candidate_rules_may_only_be_stricter"] is True, "Blender-specific rules may only tighten global governance")

    consolidation = governance["consolidation_guard"]
    check(consolidation["mode"] == "EXISTING_CANDIDATE_CLOSURE", "PR #470 must operate as existing Candidate closure debt")
    check(consolidation["net_new_frontier_items_allowed"] is False, "consolidation throttle must block net-new frontier items")
    check(consolidation["ci_receipt_or_probe_count_is_not_closure"] is True, "CI/receipt/probe count cannot be treated as closure")
    allowed_closure = set(consolidation["allowed_actions"])
    check({"REPAIR", "SYNC", "ABSORB", "MERGE", "SUPERSEDE", "CLOSE", "PROJECT_USAGE_EVIDENCE", "PROMOTION"}.issubset(allowed_closure), "closure action set is incomplete")

    alignment = governance["skill_runtime_alignment"]
    check(alignment["parent_skill"] == "oleander-skills/oleander-3d-pipeline/SKILL.md", "Blender runtime must stay under the existing 3D Skill owner")
    check(alignment["skill_capability_contract"] == "oleander-skills/oleander-3d-pipeline/CAPABILITY.json", "Candidate alignment must reference the existing installed Skill capability contract")
    check(alignment["runtime_capability_map_role"] == "CAPABILITY_AND_HISTORICAL_STAGE_PROVENANCE_MAP_NOT_CURRENT_RUNTIME_COMPATIBILITY_AUTHORITY", "runtime capability map role must preserve historical stage provenance")
    check(alignment["existing_module_first"] is True, "Blender runtime alignment must be existing-module-first")
    check(alignment["no_new_skill_or_parallel_runtime_framework"] is True, "Blender candidate must prohibit parallel Skill/runtime frameworks")
    check(alignment["material_runtime_change_requires_alignment_readback"] is True, "material runtime changes must require alignment readback")
    check(alignment["production_runtime_authority"] == "Blender 5.2.0 LTS", "production Blender authority must be 5.2.0 LTS")
    check(alignment["historical_per_stage_blender_5_1_receipts_role"] == "PROVENANCE", "Blender 5.1 stage receipts must be provenance only")

    skill_text = SKILL.read_text(encoding="utf-8")
    workbench_text = WORKBENCH_EXTENSION.read_text(encoding="utf-8")
    runtime_readme = RUNTIME_README.read_text(encoding="utf-8")
    check("## Blender Workbench existing-first route" in skill_text, "parent 3D Skill must expose Blender existing-first routing")
    check("Do not create `oleander-blender-skill`" in skill_text, "parent 3D Skill must block parallel Blender Skill creation")
    check("Status: CANDIDATE IMPLEMENTATION LAYER / NOT INSTALLED CURRENT" in workbench_text, "Workbench extension status must match actual Candidate authority")
    check("Status: PROPOSED IMPLEMENTATION LAYER" not in workbench_text, "Workbench extension cannot remain falsely PROPOSED")
    check("Blender `5.2.0 LTS`" in runtime_readme, "Runtime README must bind current compatibility to Blender 5.2 LTS")
    check("seventeen bound validation stages" in runtime_readme, "Runtime README must reflect the seventeen-layer current regression")

    current_receipt_path = ROOT / alignment["current_runtime_compatibility_receipt"]
    check(current_receipt_path.exists(), "current Blender 5.2 consolidated regression receipt missing")
    current_receipt = json.loads(current_receipt_path.read_text(encoding="utf-8"))
    check(current_receipt["validation_state"] == "PASS", "current Blender runtime receipt must be PASS")
    check(current_receipt["host"]["blender_version"] == "5.2.0 LTS", "current runtime receipt must bind Blender 5.2.0 LTS")
    check(current_receipt["runtime_result"] == "PASS", "current Blender runtime regression result must be PASS")

    policy = governance["workflow_policy"]
    grandfathered = set(policy["grandfathered_freecad_workflows"])
    cad_baselines = set(policy["grandfathered_cad_baseline_workflows"])
    review_boundary = grandfathered | cad_baselines
    actual = {
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in WORKFLOWS.glob("oleander-blender-professional-freecad-*.yml")
    }
    unexpected = sorted(actual - grandfathered)
    missing = sorted(grandfathered - actual)
    check(not unexpected, "new one-off FreeCAD workflow is prohibited; use shared frontier workflow: " + ", ".join(unexpected))
    check(not missing, "grandfathered workflow disappeared without governance migration: " + ", ".join(missing))
    check(len(cad_baselines) == 3, "exactly three stable CAD baselines are review-boundary governed")

    frontier_workflow = policy["shared_frontier_workflow"]
    runtime_workflow = policy["runtime_5_2_regression_workflow"]
    check(frontier_workflow == ".github/workflows/oleander-blender-professional-frontier-5-2-lts.yml", "5.2 frontier workflow path must be version-bound, not CURRENT-named")
    check(runtime_workflow == ".github/workflows/oleander-blender-runtime-5-2-lts.yml", "5.2 runtime workflow path must be version-bound, not CURRENT-named")
    check((ROOT / frontier_workflow).exists(), "5.2 shared frontier workflow must exist")
    check((ROOT / runtime_workflow).exists(), "Blender 5.2 runtime regression workflow must exist")
    check((ROOT / "90-shared/toolchains/blender-runtime/ensure-blender-5.2.sh").exists(), "canonical Blender 5.2 runtime resolver must exist")
    for obsolete in policy["superseded_workflows"]:
        check(not (ROOT / obsolete).exists(), f"superseded workflow must not remain in current tree: {obsolete}")
    check(policy["candidate_regression_frontier_owner"] == "SHARED_FRONTIER_5_2_LTS", "Candidate regression owner must be shared 5.2 Frontier")
    check(policy["net_new_frontier_development"] == "BLOCKED_BY_CONSOLIDATION_THROTTLE", "net-new frontier development must remain blocked during consolidation")
    check(policy["grandfathered_pr_trigger"] == "READY_FOR_REVIEW_ONLY", "grandfathered PR workflows must be review-boundary only")
    check(policy["grandfathered_push_main_regression_preserved"] is True, "grandfathered push-main regression must remain preserved")

    for relative in sorted(review_boundary):
        assert_review_boundary_workflow(relative)

    parity_candidates = status.get("reuse_candidates", {})
    allowed_states = set(governance["allowed_frontier_states"])
    for item in governance["frontier_items"]:
        state = item["state"]
        check(state in allowed_states, f"invalid frontier state: {item['id']}={state}")
        check((ROOT / item["probe"]).exists(), f"frontier probe missing: {item['probe']}")
        if item.get("readback"):
            check((ROOT / item["readback"]).exists(), f"frontier readback missing: {item['readback']}")

        parity_key = item["parity_key"]
        receipt = item.get("receipt")
        if state in {"EXPERIMENTAL_UNVERIFIED", "VALIDATION_PENDING"}:
            check(item["promotion_allowed"] is False, f"unverified item cannot allow promotion: {item['id']}")
            check(parity_key not in parity_candidates, f"unverified frontier item leaked into PROFESSIONAL_PARITY_STATUS: {parity_key}")
            check(receipt is None, f"unverified frontier item cannot claim receipt: {item['id']}")
        elif state == "VALIDATED_FOR_BOUNDED_SCOPE":
            check(item["promotion_allowed"] is True, f"validated item must explicitly allow bounded promotion: {item['id']}")
            check(receipt, f"validated item must bind receipt: {item['id']}")
            check((ROOT / receipt).exists(), f"validated receipt missing: {receipt}")
            check(parity_key in parity_candidates, f"validated item missing from PROFESSIONAL_PARITY_STATUS: {parity_key}")
            check(parity_candidates[parity_key]["state"] == "VALIDATED_FOR_BOUNDED_SCOPE", f"parity state mismatch: {parity_key}")

    check(len(governance["frontier_items"]) == 5, "consolidation mode must not add new frontier items")

    gate = governance["promotion_gate"]
    check(gate["require_main_sync_behind_count"] == 0, "promotion gate must require zero commits behind main")
    check(gate["require_dynamic_main_compare_at_promotion"] is True, "promotion must use a fresh main comparison, not a stored behind count")
    check(gate["require_no_experimental_unverified_items"] is True, "promotion must block experimental items")
    check(gate["require_no_validation_pending_items"] is True, "promotion must block pending validation")
    check(gate["require_pr_authority_current"] is True, "promotion must require current PR authority")
    check(gate["require_current_runtime_5_2_regression"] is True, "promotion must require Blender 5.2 regression")
    check(gate["require_contradiction_scan"] is True, "promotion must require contradiction scan")
    check(gate["require_project_usage_or_explicit_bounded_absorption_decision"] is True, "promotion must require project usage or explicit bounded absorption decision")

    hygiene = governance["branch_hygiene"]
    check(hygiene["observation_is_advisory"] is True, "stored branch-distance observation must never be promotion authority")
    observed_behind = int(hygiene["last_observed_behind_main"])
    if observed_behind == 0:
        check(
            hygiene["state"] == "SYNCHRONIZED_AWAITING_FINAL_REGRESSION_AND_EXPLICIT_PROMOTION_DECISION",
            "zero-behind snapshot must use synchronized Candidate state without implying promotion",
        )
    else:
        check(hygiene["state"] == "SYNC_REQUIRED_BEFORE_PROMOTION", "nonzero-behind snapshot must remain synchronization-held")

    print("OLEANDER_CANDIDATE_GOVERNANCE=PASS")
    print("consolidation_mode=" + consolidation["mode"])
    print("skill_runtime_alignment=PASS")
    print("net_new_frontier_items_allowed=" + str(consolidation["net_new_frontier_items_allowed"]))
    print("review_boundary_workflows=" + str(len(review_boundary)))
    print("runtime_5_2_regression=" + runtime_workflow)
    print("frontier_5_2_regression=" + frontier_workflow)
    print("observed_behind_main=" + str(observed_behind))
    print("frontier_items=" + str(len(governance["frontier_items"])))


if __name__ == "__main__":
    main()
