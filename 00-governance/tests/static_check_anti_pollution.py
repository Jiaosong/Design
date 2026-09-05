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
