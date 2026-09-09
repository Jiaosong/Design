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

    authority = governance["authority"]
    check(authority["installed_current_branch"] == "main", "main must be the installed Blender Runtime Current")
    check(authority["main_is_only_installed_current"] is True, "main must remain the only installed Current")
    check(authority["candidate_may_not_self_promote"] is True, "historical Candidate self-promotion must stay disabled")
    check(
        authority["promotion_state"] == "BOUNDED_ABSORPTION_COMPLETED_CURRENT_WITH_BLOCKED_PARITY_GATES",
        "post-absorption authority must remain bounded Current with professional parity gates blocked",
    )
    check(status["default_environment_eligible"] is False, "default environment must remain ineligible until its independent gate passes")
    check(status["p0"]["P0_B_DIRECT_BREP"]["state"] != "PASS", "P0-B cannot PASS while recorded blockers remain")

    absorption = governance["bounded_absorption_plan"]
    check(absorption["state"] == "ABSORBED_INTO_MAIN", "bounded absorption must remain recorded as completed")
    check(absorption["absorb_into_existing_owner_only"] == "oleander-skills/oleander-3d-pipeline", "absorption must stay inside the existing 3D owner")
    check(absorption["decision_does_not_enable_default_environment"] is True, "bounded absorption must not enable the default environment")
    check(absorption["decision_does_not_promote_p0_b"] is True, "bounded absorption must not promote P0-B")

    project_wide = governance["project_wide_governance"]
    check(project_wide["authority"] == "main/00-governance/OLEANDER_ANTI_POLLUTION_PROTOCOL_v1.0.md", "Blender governance must inherit canonical project-wide protocol from main")
    check(project_wide["machine_contract"] == "main/00-governance/OLEANDER_ANTI_POLLUTION_CONTRACT_CURRENT.json", "Blender governance must inherit project-wide machine contract from main")
    check(project_wide["inherit_without_fork"] is True, "Blender Runtime may not fork project-wide anti-pollution governance")
    check(project_wide["blender_candidate_rules_may_only_be_stricter"] is True, "Blender-specific rules may only tighten global governance")

    consolidation = governance["consolidation_guard"]
    check(consolidation["net_new_frontier_items_allowed"] is False, "consolidation throttle must still block a sixth Frontier")
    check(consolidation["ci_receipt_or_probe_count_is_not_closure"] is True, "CI/receipt/probe count cannot be treated as closure")
    allowed_actions = set(consolidation["allowed_actions"])
    check({"REPAIR", "SYNC", "ABSORB", "MERGE", "SUPERSEDE", "CLOSE", "PROJECT_USAGE_EVIDENCE", "PROMOTION"}.issubset(allowed_actions), "governed closure action set is incomplete")

    alignment = governance["skill_runtime_alignment"]
    check(alignment["parent_skill"] == "oleander-skills/oleander-3d-pipeline/SKILL.md", "Blender Runtime must stay under the existing 3D Skill owner")
    check(alignment["skill_capability_contract"] == "oleander-skills/oleander-3d-pipeline/CAPABILITY.json", "Runtime alignment must reference the installed Skill capability contract")
    check(alignment["runtime_capability_map_role"] == "CAPABILITY_AND_HISTORICAL_STAGE_PROVENANCE_MAP_NOT_CURRENT_RUNTIME_COMPATIBILITY_AUTHORITY", "runtime capability map role must preserve historical stage provenance")
    check(alignment["existing_module_first"] is True, "Blender Runtime alignment must be existing-module-first")
    check(alignment["no_new_skill_or_parallel_runtime_framework"] is True, "parallel Skill/runtime frameworks must remain prohibited")
    check(alignment["material_runtime_change_requires_alignment_readback"] is True, "material runtime changes must require alignment readback")
    check(alignment["production_runtime_authority"] == "Blender 5.2.0 LTS", "production Blender authority must remain 5.2.0 LTS")
    check(alignment["historical_per_stage_blender_5_1_receipts_role"] == "PROVENANCE", "Blender 5.1 stage receipts must remain provenance only")

    skill_text = SKILL.read_text(encoding="utf-8")
    workbench_text = WORKBENCH_EXTENSION.read_text(encoding="utf-8")
    runtime_readme = RUNTIME_README.read_text(encoding="utf-8")
    check("## Blender Workbench existing-first route" in skill_text, "parent 3D Skill must expose Blender existing-first routing")
    check("Do not create `oleander-blender-skill`" in skill_text, "parent 3D Skill must block parallel Blender Skill creation")
    check("Status: CURRENT IMPLEMENTATION LAYER / BOUNDED ABSORPTION IN MAIN" in workbench_text, "Workbench extension status must match installed bounded Current authority")
    check("Status: CANDIDATE IMPLEMENTATION LAYER / NOT INSTALLED CURRENT" not in workbench_text, "Workbench extension cannot regress to pre-absorption Candidate authority")
    check("Status: `ABSORBED INTO MAIN / BOUNDED CURRENT`" in runtime_readme, "Runtime README must identify the absorbed bounded Current")
    check("Blender `5.2.0 LTS`" in runtime_readme, "Runtime README must bind current compatibility to Blender 5.2 LTS")
    check("seventeen bound validation stages" in runtime_readme, "Runtime README must reflect the seventeen-layer current regression")

    current_receipt_path = ROOT / alignment["current_runtime_compatibility_receipt"]
    check(current_receipt_path.exists(), "current Blender 5.2 consolidated regression receipt missing")
    current_receipt = json.loads(current_receipt_path.read_text(encoding="utf-8"))
    check(current_receipt["validation_state"] == "PASS", "current Blender Runtime receipt must be PASS")
    check(current_receipt["host"]["blender_version"] == "5.2.0 LTS", "current runtime receipt must bind Blender 5.2.0 LTS")
    check(current_receipt["runtime_result"] == "PASS", "current Blender Runtime regression result must be PASS")

    policy = governance["workflow_policy"]
    grandfathered = set(policy["grandfathered_freecad_workflows"])
    cad_baselines = set(policy["grandfathered_cad_baseline_workflows"])
    review_boundary = grandfathered | cad_baselines
    actual = {
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in WORKFLOWS.glob("oleander-blender-professional-freecad-*.yml")
    }
    check(not (actual - grandfathered), "new one-off FreeCAD workflow is prohibited; use shared Frontier workflow")
    check(not (grandfathered - actual), "grandfathered FreeCAD workflow disappeared without governance migration")
    check(len(cad_baselines) == 3, "exactly three stable CAD baselines are review-boundary governed")

    frontier_workflow = policy["shared_frontier_workflow"]
    runtime_workflow = policy["runtime_5_2_regression_workflow"]
    check(frontier_workflow == ".github/workflows/oleander-blender-professional-frontier-5-2-lts.yml", "shared Frontier workflow must remain version-bound")
    check(runtime_workflow == ".github/workflows/oleander-blender-runtime-5-2-lts.yml", "runtime regression workflow must remain version-bound")
    check((ROOT / frontier_workflow).exists(), "Blender 5.2 shared Frontier workflow must exist")
    check((ROOT / runtime_workflow).exists(), "Blender 5.2 Runtime regression workflow must exist")
    check((ROOT / "90-shared/toolchains/blender-runtime/ensure-blender-5.2.sh").exists(), "canonical Blender 5.2 runtime resolver must exist")
    for obsolete in policy["superseded_workflows"]:
        check(not (ROOT / obsolete).exists(), f"superseded workflow must not remain in Current tree: {obsolete}")
    check(policy["net_new_frontier_development"] == "BLOCKED_BY_CONSOLIDATION_THROTTLE", "net-new Frontier development must remain blocked")
    check(policy["grandfathered_pr_trigger"] == "READY_FOR_REVIEW_ONLY", "grandfathered PR workflows must remain review-boundary only")
    check(policy["grandfathered_push_main_regression_preserved"] is True, "grandfathered push-main regression must remain preserved")

    for relative in sorted(review_boundary):
        assert_review_boundary_workflow(relative)

    parity_candidates = status.get("reuse_candidates", {})
    allowed_states = set(governance["allowed_frontier_states"])
    frontier_items = governance["frontier_items"]
    check(len(frontier_items) == 5, "bounded Current must not add a sixth Frontier item")
    for item in frontier_items:
        state = item["state"]
        check(state in allowed_states, f"invalid Frontier state: {item['id']}={state}")
        check((ROOT / item["probe"]).exists(), f"Frontier probe missing: {item['probe']}")
        if item.get("readback"):
            check((ROOT / item["readback"]).exists(), f"Frontier readback missing: {item['readback']}")
        if state == "VALIDATED_FOR_BOUNDED_SCOPE":
            check(item["promotion_allowed"] is True, f"validated bounded item must explicitly permit bounded reuse: {item['id']}")
            receipt = item.get("receipt")
            check(bool(receipt) and (ROOT / receipt).exists(), f"validated Frontier receipt missing: {item['id']}")
            parity_key = item["parity_key"]
            check(parity_key in parity_candidates, f"validated Frontier item missing from PROFESSIONAL_PARITY_STATUS: {parity_key}")
            check(parity_candidates[parity_key]["state"] == "VALIDATED_FOR_BOUNDED_SCOPE", f"parity state mismatch: {parity_key}")

    hygiene = governance["branch_hygiene"]
    check(hygiene["observation_is_advisory"] is True, "stored branch-distance observation must remain advisory, not Current authority")

    print("OLEANDER_BLENDER_CURRENT_GOVERNANCE=PASS")
    print("installed_current=main")
    print("promotion_state=" + authority["promotion_state"])
    print("net_new_frontier_items_allowed=" + str(consolidation["net_new_frontier_items_allowed"]))
    print("review_boundary_workflows=" + str(len(review_boundary)))
    print("runtime_5_2_regression=" + runtime_workflow)
    print("frontier_5_2_regression=" + frontier_workflow)
    print("frontier_items=" + str(len(frontier_items)))


if __name__ == "__main__":
    main()
