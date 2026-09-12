from __future__ import annotations

import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "00-governance/OLEANDER_ANTI_POLLUTION_CONTRACT_CURRENT.json"
POLICY_PATH = ROOT / "00-governance/OLEANDER_ANTI_POLLUTION_PROTOCOL_v1.0.md"


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def event_payload() -> dict:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        return {}
    path = Path(event_path)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def current_pr_delta() -> list[tuple[str, str]]:
    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        return []
    payload = event_payload()
    base_sha = payload.get("pull_request", {}).get("base", {}).get("sha")
    cmd = ["git", "diff", "--name-status"]
    if base_sha:
        cmd.append(f"{base_sha}...HEAD")
    else:
        cmd.extend(["HEAD^", "HEAD"])
    proc = subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True)
    out: list[tuple[str, str]] = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        out.append((parts[0], parts[-1]))
    return out


def is_ignored(path: str, ignored_roots: list[str]) -> bool:
    return any(path == root or path.startswith(root.rstrip("/") + "/") for root in ignored_roots)


def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def text_has_any(text: str, markers: list[str]) -> bool:
    upper = text.upper()
    return any(marker.upper() in upper for marker in markers)


def fetch_open_pull_requests(repository: str, token: str) -> list[dict]:
    pulls: list[dict] = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{repository}/pulls?state=open&per_page=100&page={page}"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "oleander-anti-pollution-gate",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                batch = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise AssertionError(f"cannot read open PR backlog: HTTP {exc.code}") from exc
        pulls.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return pulls


def enforce_consolidation_guard(contract: dict) -> None:
    guard = contract["consolidation_guard"]
    check(guard["enabled"] is True, "consolidation guard must remain enabled")
    check(guard["global_open_training_candidate_soft_limit"] >= 1, "invalid consolidation soft limit")
    check(guard["no_net_new_training_evidence_when_over_limit"] is True, "training debt throttle must remain enabled")

    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        return

    payload = event_payload()
    pr = payload.get("pull_request", {})
    if not pr:
        return

    created_at = pr.get("created_at")
    if not created_at:
        return
    if parse_utc(created_at) < parse_utc(guard["effective_from"]):
        print("consolidation_guard=GRANDFATHERED_PRE_EFFECTIVE_PR")
        return

    title_body = f"{pr.get('title') or ''}\n{pr.get('body') or ''}"
    project_exempt = guard["project_mode_exempt_from_training_throttle"] and text_has_any(
        title_body, guard["project_exemption_markers"]
    )
    training_or_candidate = text_has_any(
        title_body, guard["training_markers"] + guard["candidate_markers"]
    )

    if project_exempt or not training_or_candidate:
        print("consolidation_guard=NOT_TRAINING_DEBT")
        return

    token = os.environ.get("GITHUB_TOKEN")
    repository = os.environ.get("GITHUB_REPOSITORY")
    check(bool(token and repository), "GITHUB_TOKEN/GITHUB_REPOSITORY required for consolidation backlog enforcement")

    pulls = fetch_open_pull_requests(repository, token)
    debt = []
    for item in pulls:
        combined = f"{item.get('title') or ''}\n{item.get('body') or ''}"
        if text_has_any(combined, guard["project_exemption_markers"]):
            continue
        if text_has_any(combined, guard["training_markers"] + guard["candidate_markers"]):
            debt.append(item)

    debt_count = len(debt)
    limit = guard["global_open_training_candidate_soft_limit"]
    print(f"open_training_candidate_debt={debt_count}")
    print(f"training_candidate_soft_limit={limit}")
    if debt_count <= limit:
        return

    marker = re.escape(guard["required_closure_marker_when_over_limit"])
    actions = "|".join(re.escape(action) for action in guard["allowed_closure_actions"])
    closure_pattern = re.compile(rf"{marker}\s*:\s*({actions})\b", re.IGNORECASE)
    check(
        closure_pattern.search(title_body) is not None,
        "training/candidate backlog is above soft limit; new non-project debt is blocked. "
        f"Declare `{guard['required_closure_marker_when_over_limit']}: <"
        + "|".join(guard["allowed_closure_actions"])
        + ">` and make the PR reduce/absorb/promote existing debt instead of adding another evidence-only frontier.",
    )


def main() -> None:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    policy = POLICY_PATH.read_text(encoding="utf-8")

    check(contract["schema"] == "OLEANDER_ANTI_POLLUTION_CONTRACT_v1.0", "anti-pollution schema mismatch")
    check(contract["canonical_policy"] == rel(POLICY_PATH), "canonical policy pointer mismatch")
    check("ONE LOGICAL OBJECT" in policy, "one logical object rule missing")
    check("NO COMPRESSION / NO LOSS" in policy, "cleanup must preserve no-loss rule")

    for inherited in contract["inherits"]:
        check((ROOT / inherited).exists(), "inherited governance authority missing: " + inherited)
    for scope_root in contract["scope_roots"]:
        check((ROOT / scope_root).exists(), "scope root missing: " + scope_root)

    check(all(contract["single_current_rules"].values()), "all single-current rules must be enabled")
    check(not any(contract["validation_guard"].values()), "validation substitution flags must remain false")
    check(not any(contract["knowledge_guard"].values()), "knowledge pollution allowances must remain false")
    check(contract["automation_guard"]["material_delta_required"] is True, "automation must require material delta")
    check(contract["automation_guard"]["repeat_run_should_update_existing_object"] is True, "repeat automation must update existing objects")
    branch_guard = contract["git_branch_hygiene"]
    check(branch_guard["branch_ref_is_current_authority"] is False, "branch refs must not become Current authority")
    check(branch_guard["one_logical_object_one_active_work_branch_pr_frontier"] is True, "branch WIP frontier rule must remain enabled")
    check(branch_guard["recurring_run_may_create_branch_without_material_delta"] is False, "recurring runs may not create no-delta branches")
    check(branch_guard["bulk_delete_requires_audit_manifest"] is True, "bulk branch cleanup must preserve an audit manifest")
    check(branch_guard["unmerged_branch_delete_by_age_only"] is False, "unmerged branches may not be deleted by age alone")
    check(set(branch_guard["protect_merged_ref_when"]) >= {"OPEN_PR_HEAD", "OPEN_PR_BASE", "ACTIVE_WORKTREE", "EXPLICIT_KEEP"}, "merged-ref protection set incomplete")
    noop_conditions = set(branch_guard["unmerged_noop_delete_allowed_when"])
    check(
        {"NOT_OPEN_PR_HEAD", "NOT_OPEN_PR_BASE", "NOT_ACTIVE_WORKTREE", "NO_EXPLICIT_KEEP", "HYPOTHETICAL_MERGE_CLEAN", "HYPOTHETICAL_MERGE_TREE_EQUALS_CURRENT_MAIN_TREE"}.issubset(noop_conditions),
        "unmerged no-op cleanup conditions incomplete",
    )
    patch_conditions = set(branch_guard["unmerged_patch_equivalent_delete_allowed_when"])
    check(
        {"NOT_OPEN_PR_HEAD", "NOT_OPEN_PR_BASE", "NOT_ACTIVE_WORKTREE", "NO_EXPLICIT_KEEP", "NO_UNIQUE_MERGE_COMMITS", "GIT_CHERRY_HAS_AT_LEAST_ONE_UNIQUE_COMMIT", "ALL_GIT_CHERRY_RESULTS_ARE_ABSORBED_MINUS", "GIT_CHERRY_RESULT_COUNT_EQUALS_UNIQUE_COMMIT_COUNT"}.issubset(patch_conditions),
        "unmerged patch-equivalent cleanup conditions incomplete",
    )
    merged_base = branch_guard["merged_open_pr_base_resolution"]
    check(
        {"BASE_ALREADY_MERGED_INTO_MAIN", "HEAD_STILL_HAS_UNABSORBED_COMMITS", "MAIN_PLUS_HEAD_MERGE_TREE_CLEAN", "HEAD_REF_UNCHANGED"}.issubset(set(merged_base["retarget_to_main_when"])),
        "merged open-PR base retarget conditions incomplete",
    )
    check(merged_base["after_retarget"] == "DELETE_MERGED_BASE_REF_WHEN_NO_OTHER_DEPENDENCY_REMAINS", "merged base cleanup action drifted")
    check(merged_base["unsafe_or_ambiguous_retarget"] == "HOLD_AND_RETAIN_BASE", "unsafe merged-base retarget must HOLD")
    disposition = branch_guard["content_disposition"]
    check(
        set(disposition["states"]) == {"SUPERSEDED", "ACTIVE", "REVIEW", "REJECT", "ABSORB"},
        "branch content-disposition state set drifted",
    )
    check(disposition["state_is_delete_authority"] is False, "content disposition alone must not authorize branch deletion")
    check(
        {"BRANCH", "TIP_SHA", "CLASSIFICATION_BASE_SHA", "STATE", "ONE_LINE_EVIDENCE"}.issubset(set(disposition["audit_requires"])),
        "content-disposition audit evidence is incomplete",
    )
    check(disposition["main_must_be_pinned_during_classification"] is True, "content classification must pin main")
    check(disposition["revalidate_if_main_advances_before_mutation"] is True, "content mutation must revalidate after main drift")
    check(disposition["absorb_whole_branch_merge_default"] is False, "ABSORB must not default to whole-branch merge")
    check(disposition["absorb_may_upgrade_truth_or_promotion_state"] is False, "ABSORB must preserve truth/promotion boundaries")
    check(set(disposition["delete_allowed_states_after_gates"]) == {"SUPERSEDED", "REJECT"}, "only SUPERSEDED/REJECT may become delete candidates after gates")
    check(disposition["actions"]["ACTIVE"].startswith("RETAIN"), "ACTIVE branch disposition must retain")
    check(disposition["actions"]["REVIEW"].startswith("RETAIN"), "REVIEW branch disposition must retain")
    check("RECLASSIFY_SUPERSEDED" in disposition["actions"]["ABSORB"], "ABSORB must read back then reclassify SUPERSEDED")
    archive = branch_guard["provenance_archive"]
    check(set(archive["allowed_states"]) == {"SUPERSEDED", "REJECT"}, "provenance archive may only preserve SUPERSEDED/REJECT tips")
    check(archive["use_only_when_tip_not_reachable_from_main_pr_or_retained_successor"] is True, "provenance archive must be a fallback for otherwise unreachable tips")
    check(archive["ref_namespace"] == "refs/tags/oleander-provenance/", "provenance archive namespace drifted")
    check(archive["archive_object"] == "SYNTHETIC_COMMIT", "provenance archive object must remain a synthetic commit")
    check(archive["source_content_in_archive_tree_allowed"] is False, "provenance archive tree must not materialize source content")
    check(archive["parents_must_exactly_equal_unique_source_tip_set"] is True, "provenance archive parents must equal the unique archived tip SHA set")
    check(archive["archive_may_enter_main_ancestry"] is False, "provenance archive must remain outside main ancestry")
    check(archive["authority"] == "PROVENANCE_ONLY_NOT_CURRENT_NO_PROMOTION", "provenance archive authority boundary drifted")
    check(
        {"BRANCH", "TIP_SHA", "STATE", "ARCHIVE_REF", "ARCHIVE_COMMIT", "NO_PROMOTION"}.issubset(set(archive["manifest_requires"])),
        "provenance archive manifest requirements incomplete",
    )
    check(
        {"REMOTE_ARCHIVE_REF_READBACK", "EVERY_EXACT_TIP_IS_ANCESTOR_OF_ARCHIVE_COMMIT", "ARCHIVE_COMMIT_IS_NOT_ANCESTOR_OF_MAIN", "OPEN_PR_AND_WORKTREE_DEPENDENCIES_CLEAR"}.issubset(set(archive["delete_after"])),
        "provenance archive deletion gates incomplete",
    )
    check(archive["tag_mutation"] == "IMMUTABLE_UNLESS_REPLACEMENT_PROVENANCE_VERIFIED", "provenance archive tag immutability rule drifted")
    main_protection = branch_guard["main_branch_protection"]
    check(main_protection["direct_push_allowed"] is False, "main direct push must remain disabled")
    check(main_protection["require_pull_request"] is True, "main must require pull requests")
    check(main_protection["required_approving_review_count"] == 0, "main PR boundary must not require unavailable self-approval")
    check(main_protection["enforce_admins"] is True, "main protection must include administrators")
    check(main_protection["allow_force_pushes"] is False, "main force pushes must remain disabled")
    check(main_protection["allow_deletions"] is False, "main deletion must remain disabled")
    check(main_protection["required_status_checks_mode"] == "APPLICABLE_PATH_SCOPED_WORKFLOWS_NOT_GLOBAL_BRANCH_REQUIREMENT", "main status-check mode drifted")
    check("A branch ref is not a Current authority" in policy, "branch authority boundary missing from policy")
    check("OPEN PR BASE" in policy and "ACTIVE WORKTREE" in policy, "branch cleanup dependency protections missing from policy")
    check("SAFE_DELETE_NOOP_UNMERGED_ORPHAN" in policy, "content-equivalent unmerged cleanup rule missing from policy")
    check("SAFE_DELETE_PATCH_EQUIVALENT_UNMERGED_ORPHAN" in policy, "patch-equivalent unmerged cleanup rule missing from policy")
    check("open PR must not permanently retain an already-merged historical base" in policy, "merged PR-base retarget rule missing from policy")
    check("`main` is a PR-only integration surface" in policy, "main PR-only integration boundary missing from policy")
    check("Content-level disposition for an unmerged orphan branch uses exactly five states" in policy, "five-state branch content disposition rule missing")
    check("`ABSORB` is retain-until-readback" in policy, "ABSORB closure/readback rule missing")
    check("refs/tags/oleander-provenance/" in policy, "provenance-only archive namespace rule missing")
    check("synthetic provenance commit" in policy, "provenance-only archive object rule missing")
    check("PROVENANCE ONLY / NOT CURRENT / NO_PROMOTION" in policy, "provenance-only archive authority boundary missing")
    enforce_consolidation_guard(contract)

    queue = ROOT / "00-governance/OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT.json"
    check(queue.exists(), "project priority CURRENT queue missing")
    check(len(list((ROOT / "00-governance").glob("OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT*.json"))) == 1, "parallel project-priority CURRENT queue detected")

    guard = contract["new_file_guard"]
    patterns = [re.compile(p, re.IGNORECASE) for p in guard["forbidden_transient_filename_patterns"]]
    allow_current = set(guard["current_named_file_allowlist"])
    ignored = guard["ignored_roots"]
    prefixes = tuple(root.rstrip("/") + "/" for root in contract["scope_roots"])

    violations: list[str] = []
    delta = current_pr_delta()
    for status, path in delta:
        if not status.startswith("A") or is_ignored(path, ignored):
            continue
        if not (path in contract["scope_roots"] or path.startswith(prefixes)):
            continue
        name = Path(path).name
        if any(pattern.search(name) for pattern in patterns):
            violations.append("transient/duplicate-like filename added to authoritative scope: " + path)
        if "CURRENT" in name.upper() and path not in allow_current:
            violations.append("new CURRENT-named file is not registered in allowlist: " + path)

    check(not violations, "anti-pollution delta violations:\n- " + "\n- ".join(violations))
    print("OLEANDER_PROJECT_ANTI_POLLUTION=PASS")
    print("delta_files_checked=" + str(len(delta)))


if __name__ == "__main__":
    main()
