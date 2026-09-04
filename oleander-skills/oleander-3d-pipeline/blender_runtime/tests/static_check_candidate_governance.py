from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PIPELINE = ROOT / "oleander-skills" / "oleander-3d-pipeline"
RUNTIME = PIPELINE / "blender_runtime"
GOV = RUNTIME / "CANDIDATE_GOVERNANCE.json"
STATUS = PIPELINE / "PROFESSIONAL_PARITY_STATUS.json"
WORKFLOWS = ROOT / ".github" / "workflows"


def fail(message: str) -> None:
    raise AssertionError(message)


def check(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


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

    policy = governance["workflow_policy"]
    grandfathered = set(policy["grandfathered_freecad_workflows"])
    actual = {
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in WORKFLOWS.glob("oleander-blender-professional-freecad-*.yml")
    }
    unexpected = sorted(actual - grandfathered)
    missing = sorted(grandfathered - actual)
    check(not unexpected, "new one-off FreeCAD workflow is prohibited; use shared frontier workflow: " + ", ".join(unexpected))
    check(not missing, "grandfathered workflow disappeared without governance migration: " + ", ".join(missing))
    check((ROOT / policy["shared_frontier_workflow"]).exists(), "shared frontier workflow must exist")
    check(policy["candidate_draft_frontier_owner"] == "SHARED_FRONTIER", "Draft Candidate professional development must use shared Frontier")
    check(policy["grandfathered_pr_trigger"] == "READY_FOR_REVIEW_ONLY", "grandfathered PR workflows must be review-boundary only")
    check(policy["grandfathered_push_main_regression_preserved"] is True, "grandfathered push-main regression must remain preserved")

    for relative in sorted(grandfathered):
        workflow_path = ROOT / relative
        text = workflow_path.read_text(encoding="utf-8")
        check("  pull_request:\n" in text and "\n  push:\n" in text, f"grandfathered workflow trigger blocks missing: {relative}")
        pull_block = text.split("  pull_request:\n", 1)[1].split("\n  push:\n", 1)[0]
        check("    types: [ready_for_review]\n" in pull_block, f"grandfathered workflow must not run on Draft synchronize: {relative}")
        check("synchronize" not in pull_block, f"grandfathered workflow cannot re-enable Draft synchronize: {relative}")
        push_block = text.split("\n  push:\n", 1)[1]
        check("    branches:\n      - main\n" in push_block, f"grandfathered workflow must preserve push-main regression: {relative}")

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

    gate = governance["promotion_gate"]
    check(gate["require_main_sync_behind_count"] == 0, "promotion gate must require zero commits behind main")
    check(gate["require_dynamic_main_compare_at_promotion"] is True, "promotion must use a fresh main comparison, not a stored behind count")
    check(gate["require_no_experimental_unverified_items"] is True, "promotion must block experimental items")
    check(gate["require_no_validation_pending_items"] is True, "promotion must block pending validation")
    check(gate["require_pr_authority_current"] is True, "promotion must require current PR authority")
    hygiene = governance["branch_hygiene"]
    check(hygiene["observation_is_advisory"] is True, "stored branch-distance observation must never be promotion authority")
    check(hygiene["state"] == "SYNC_REQUIRED_BEFORE_PROMOTION", "current branch must remain promotion-held until synchronized")

    print("OLEANDER_CANDIDATE_GOVERNANCE=PASS")
    print("grandfathered_freecad_workflows=" + str(len(grandfathered)))
    print("grandfathered_pr_trigger=" + policy["grandfathered_pr_trigger"])
    print("frontier_items=" + str(len(governance["frontier_items"])))


if __name__ == "__main__":
    main()
