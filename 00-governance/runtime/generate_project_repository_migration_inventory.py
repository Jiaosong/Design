#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "00-governance" / "runtime" / "OLEANDER_PROJECT_REPOSITORY_MIGRATION_INVENTORY_20260927.json"
LOCAL_PROJECTS_ROOT = Path(r"D:\OLEANDER\projects")
PROJECTS = (
    "c01-yimai-guangdu",
    "c02-daylily",
    "c03-the-light-collection",
    "c04-qingjiang-stone-book",
)


def _git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def _branch_sha(branch: str) -> str | None:
    value = _git("rev-parse", "--verify", f"refs/heads/{branch}", check=False)
    return value or None


def build_inventory() -> dict[str, Any]:
    container_head = _git("rev-parse", "HEAD")
    container_branch = _git("branch", "--show-current")
    remote = _git("config", "--get", "remote.origin.url", check=False) or None
    projects: list[dict[str, Any]] = []
    for slug in PROJECTS:
        branch = f"migration/{slug}"
        sha = _branch_sha(branch)
        source_path = ROOT / "05-cases" / slug
        local_repository = LOCAL_PROJECTS_ROOT / slug
        local_ready = (local_repository / ".git").is_dir()
        local_head = None if not local_ready else _git("-C", str(local_repository), "rev-parse", "HEAD", check=False) or None
        local_branch = None if not local_ready else _git("-C", str(local_repository), "branch", "--show-current", check=False) or None
        local_remotes_raw = None if not local_ready else _git("-C", str(local_repository), "remote", check=False) or None
        tree_entries = [] if sha is None else [line for line in _git("ls-tree", "--name-only", sha).splitlines() if line]
        history_count = None if sha is None else int(_git("rev-list", "--count", sha))
        projects.append({
            "project_candidate_id": slug.split("-", 1)[0].upper(),
            "source_path": f"05-cases/{slug}",
            "source_path_exists": source_path.is_dir(),
            "target_repository_candidate": slug,
            "migration_branch": branch,
            "split_commit": sha,
            "split_history_commit_count": history_count,
            "split_top_level_entries": tree_entries,
            "split_is_subdirectory_rooted": bool(sha) and not any(entry == "05-cases" for entry in tree_entries),
            "migration_state": "SPLIT_BRANCH_READY" if sha else "SPLIT_PENDING",
            "local_repository_path": str(local_repository),
            "local_repository_ready": local_ready,
            "local_repository_branch": local_branch,
            "local_repository_revision": local_head,
            "local_repository_matches_split": bool(sha and local_head == sha),
            "local_repository_remotes": [] if not local_remotes_raw else local_remotes_raw.splitlines(),
            "remote_repo_created": False,
            "remote_repo_pushed": False,
            "old_duplicate_retained": source_path.is_dir(),
            "project_state_ref": None,
            "artifact_store_binding": "UNRESOLVED",
            "knowledge_mount_binding": "UNRESOLVED",
            "authority_ceiling": "MIGRATION_READBACK_ONLY",
            "next_actions": [
                "VERIFY_OWNER_NATIVE_PROJECT_STATE",
                "VERIFY_ARTIFACT_AND_KNOWLEDGE_BINDINGS",
                "CREATE_TARGET_REMOTE_REPOSITORY_WITH_EXPLICIT_EXTERNAL_ACTION_AUTHORIZATION",
                "PUSH_AND_READBACK_SPLIT_HISTORY",
                "BIND_PROJECT_MANIFEST",
                "REMOVE_OLD_MONOREPO_DUPLICATE_ONLY_AFTER_VERIFIED_BINDING",
            ],
        })
    complete = all(
        row["migration_state"] == "SPLIT_BRANCH_READY"
        and row["local_repository_ready"]
        and row["local_repository_matches_split"]
        for row in projects
    )
    return {
        "schema": "oleander.project-repository-migration-inventory.v0.1",
        "status": "LOCAL_REPOSITORIES_READY" if complete else "SPLIT_IN_PROGRESS",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_ceiling": "MIGRATION_READBACK_ONLY",
        "container_repository": remote,
        "container_branch": container_branch,
        "container_revision": container_head,
        "migration_strategy": "HISTORY_PRESERVING_SUBTREE_SPLIT_WITH_OLD_DUPLICATE_RETAINED_UNTIL_REMOTE_AND_PROJECT_BINDING_READBACK",
        "projects": projects,
        "hard_invariants": [
            "GIT_SPLIT_BRANCH_NE_PROJECT_CURRENT",
            "REMOTE_REPOSITORY_CREATION_NE_PROJECT_PROMOTION",
            "OLD_DUPLICATE_REMOVAL_REQUIRES_VERIFIED_PROJECT_ARTIFACT_KNOWLEDGE_BINDING",
        ],
        "does_not_prove": ["PROJECT_CURRENT", "REMOTE_REPOSITORY_CREATED", "REMOTE_PUSHED", "DESIGN_KEEP", "PROMOTION"],
    }


def main() -> None:
    payload = build_inventory()
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "output": str(OUTPUT), "projects": payload["projects"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
