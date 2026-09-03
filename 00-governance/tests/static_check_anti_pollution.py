from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "00-governance/OLEANDER_ANTI_POLLUTION_CONTRACT_CURRENT.json"
POLICY_PATH = ROOT / "00-governance/OLEANDER_ANTI_POLLUTION_PROTOCOL_v1.0.md"


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def current_head_delta() -> list[tuple[str, str]]:
    """Strictly inspect the newest PR commit so existing historical debt is not retroactively misclassified.

    Main uses whole-tree invariants only. Existing history is governed by separate audit/migration work.
    """
    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        return []
    proc = subprocess.run(
        ["git", "diff", "--name-status", "HEAD^", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    out: list[tuple[str, str]] = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        path = parts[-1]
        out.append((status, path))
    return out


def is_ignored(path: str, ignored_roots: list[str]) -> bool:
    return any(path == root or path.startswith(root.rstrip("/") + "/") for root in ignored_roots)


def main() -> None:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    policy = POLICY_PATH.read_text(encoding="utf-8")

    check(contract["schema"] == "OLEANDER_ANTI_POLLUTION_CONTRACT_v1.0", "anti-pollution schema mismatch")
    check(contract["canonical_policy"] == rel(POLICY_PATH), "canonical policy pointer mismatch")
    check("ONE LOGICAL OBJECT" in policy, "canonical one-logical-object rule missing")
    check("EXPERIMENTAL_UNVERIFIED" in policy and "VALIDATION_PENDING" in policy, "candidate isolation states missing")
    check("NO COMPRESSION / NO LOSS" in policy, "anti-pollution repair must preserve no-loss rule")

    for inherited in contract["inherits"]:
        check((ROOT / inherited).exists(), "inherited governance authority missing: " + inherited)
    for scope_root in contract["scope_roots"]:
        check((ROOT / scope_root).exists(), "scope root missing: " + scope_root)

    single = contract["single_current_rules"]
    check(all(single.values()), "all single-current rules must be enabled")
    validation = contract["validation_guard"]
    check(not any(validation.values()), "validation substitution flags must all remain false")
    knowledge = contract["knowledge_guard"]
    check(not any(knowledge.values()), "knowledge pollution allowances must all remain false")
    automation = contract["automation_guard"]
    check(automation["material_delta_required"] is True, "automation must require material delta")
    check(automation["repeat_run_should_update_existing_object"] is True, "automation must repair/update existing objects")
    check(automation["no_artifact_created_only_to_prove_run"] is True, "automation run-proof artifacts are prohibited")

    queue = ROOT / "00-governance/OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT.json"
    check(queue.exists(), "single project priority queue missing")
    current_queue_matches = list((ROOT / "00-governance").glob("OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT*.json"))
    check(len(current_queue_matches) == 1, "parallel project priority CURRENT queue detected")

    cross = contract["cross_surface_guard"]
    check(cross["authority_change_requires_downstream_readback"] is True, "authority change must require downstream readback")
    check(cross["notion_current_may_not_be_updated_from_candidate_only_evidence"] is True, "Notion Current must reject Candidate-only claims")

    guard = contract["new_file_guard"]
    patterns = [re.compile(pat, re.IGNORECASE) for pat in guard["forbidden_transient_filename_patterns"]]
    allow_current = set(guard["current_named_file_allowlist"])
    ignored_roots = guard["ignored_roots"]
    scope_roots = tuple(root.rstrip("/") + "/" for root in contract["scope_roots"])

    delta = current_head_delta()
    violations: list[str] = []
    for status, path in delta:
        if not status.startswith("A"):
            continue
        if is_ignored(path, ignored_roots):
            continue
        if not (path in contract["scope_roots"] or path.startswith(scope_roots)):
            continue
        name = Path(path).name
        if any(pattern.search(name) for pattern in patterns):
            violations.append("transient/duplicate-like filename added to authoritative scope: " + path)
        if "CURRENT" in name.upper() and path not in allow_current:
            violations.append("new CURRENT-named file is not registered in single-current allowlist: " + path)

    check(not violations, "anti-pollution delta violations:\n- " + "\n- ".join(violations))

    blender_contract = ROOT / contract["workflow_guard"]["blender_freecad_policy_source"]
    check(blender_contract.exists(), "Blender professional frontier governance source missing")

    print("OLEANDER_PROJECT_ANTI_POLLUTION=PASS")
    print("scope_roots=" + str(len(contract["scope_roots"])))
    print("delta_files_checked=" + str(len(delta)))


if __name__ == "__main__":
    main()
