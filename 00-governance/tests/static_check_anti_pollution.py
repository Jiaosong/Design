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
    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        return []
    proc = subprocess.run(["git", "diff", "--name-status", "HEAD^", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True)
    out: list[tuple[str, str]] = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        out.append((parts[0], parts[-1]))
    return out


def is_ignored(path: str, ignored_roots: list[str]) -> bool:
    return any(path == root or path.startswith(root.rstrip("/") + "/") for root in ignored_roots)


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

    queue = ROOT / "00-governance/OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT.json"
    check(queue.exists(), "project priority CURRENT queue missing")
    check(len(list((ROOT / "00-governance").glob("OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT*.json"))) == 1, "parallel project-priority CURRENT queue detected")

    guard = contract["new_file_guard"]
    patterns = [re.compile(p, re.IGNORECASE) for p in guard["forbidden_transient_filename_patterns"]]
    allow_current = set(guard["current_named_file_allowlist"])
    ignored = guard["ignored_roots"]
    prefixes = tuple(root.rstrip("/") + "/" for root in contract["scope_roots"])

    violations: list[str] = []
    delta = current_head_delta()
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
