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
PROJECTS = {
    "c01-yimai-guangdu": {
        "project_id": "PRJ-C01-YIMAI-GUANGDU",
        "state_evidence": "README.md",
        "state_evidence_class": "CURRENT_PUBLIC_STATE_SUMMARY_NOT_PROJECT_STATE",
        "project_state_ref": None,
        "authority_ref": None,
        "required_markers": [],
    },
    "c02-daylily": {
        "project_id": "PRJ-C02-DAYLILY",
        "state_evidence": "README.md",
        "state_evidence_class": "CURRENT_PUBLIC_STATE_SUMMARY_NOT_PROJECT_STATE",
        "project_state_ref": None,
        "authority_ref": None,
        "required_markers": [],
    },
    "c03-the-light-collection": {
        "project_id": "PRJ-C03-LIGHT-COLLECTION",
        "state_evidence": "README.md",
        "state_evidence_class": "CURRENT_PUBLIC_STATE_SUMMARY_NOT_PROJECT_STATE",
        "project_state_ref": None,
        "authority_ref": None,
        "required_markers": [],
    },
    "c04-qingjiang-stone-book": {
        "project_id": "PRJ-C04-QINGJIANG-SHISHU",
        "state_evidence": "C04_CURRENT.md",
        "state_evidence_class": "OWNER_NATIVE_CURRENT_AUTHORITY",
        "project_state_ref": "file:C04_CURRENT.md",
        "authority_ref": "file:C04_CURRENT.md",
        "required_markers": [
            "Current Execution Authority",
            "this file",
            "NO_PROMOTION",
        ],
    },
}

BOOTSTRAP_FORBIDDEN_FIELDS = {
    "project_current_payload",
    "design_keep",
    "professional_pass",
    "promotion",
    "release_authority",
}


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


def _is_ancestor(repository: Path, ancestor: str | None, descendant: str | None) -> bool:
    if not ancestor or not descendant:
        return False
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=repository,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=10,
    )
    return result.returncode == 0


def _verify_project_state_evidence(repository: Path, spec: dict[str, Any]) -> dict[str, Any]:
    evidence_ref = str(spec["state_evidence"])
    evidence_path = repository / evidence_ref
    if not evidence_path.is_file():
        return {
            "status": "MISSING",
            "evidence_ref": evidence_ref,
            "evidence_class": spec["state_evidence_class"],
            "owner_native_project_state_verified": False,
            "reason": "STATE_EVIDENCE_FILE_MISSING",
        }
    try:
        content = evidence_path.read_text(encoding="utf-8")
    except OSError:
        return {
            "status": "UNREADABLE",
            "evidence_ref": evidence_ref,
            "evidence_class": spec["state_evidence_class"],
            "owner_native_project_state_verified": False,
            "reason": "STATE_EVIDENCE_FILE_UNREADABLE",
        }
    project_id_present = str(spec["project_id"]) in content
    required_markers = [str(value) for value in spec.get("required_markers") or []]
    markers_present = all(marker in content for marker in required_markers)
    declared_ref = spec.get("project_state_ref")
    verified = bool(
        declared_ref
        and spec.get("state_evidence_class") == "OWNER_NATIVE_CURRENT_AUTHORITY"
        and project_id_present
        and markers_present
    )
    return {
        "status": "VERIFIED_OWNER_NATIVE_PROJECT_STATE" if verified else "EVIDENCE_ONLY_NOT_PROJECT_STATE",
        "evidence_ref": evidence_ref,
        "evidence_class": spec["state_evidence_class"],
        "project_id_present": project_id_present,
        "required_markers_present": markers_present,
        "owner_native_project_state_verified": verified,
        "project_state_ref": declared_ref if verified else None,
        "authority_ref": spec.get("authority_ref") if verified else None,
        "reason": None if verified else "EVIDENCE_DOES_NOT_DECLARE_OWNER_NATIVE_PROJECT_STATE_AUTHORITY",
    }


def _read_bootstrap_manifest(repository: Path, spec: dict[str, Any], state_evidence: dict[str, Any]) -> dict[str, Any]:
    manifest_path = repository / ".oleander" / "project.json"
    if not manifest_path.is_file():
        return {
            "status": "MISSING",
            "ref": ".oleander/project.json",
            "tracked": False,
            "locator_only_verified": False,
        }
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "status": "HOLD_INVALID",
            "ref": ".oleander/project.json",
            "tracked": False,
            "locator_only_verified": False,
            "reason": "BOOTSTRAP_MANIFEST_INVALID_JSON",
        }
    if not isinstance(payload, dict):
        return {
            "status": "HOLD_INVALID",
            "ref": ".oleander/project.json",
            "tracked": False,
            "locator_only_verified": False,
            "reason": "BOOTSTRAP_MANIFEST_NOT_OBJECT",
        }
    leaked = sorted(BOOTSTRAP_FORBIDDEN_FIELDS & {str(key).lower() for key in payload})
    expected_state_ref = state_evidence.get("project_state_ref")
    expected_authority_ref = state_evidence.get("authority_ref")
    errors: list[str] = []
    if payload.get("authority_ceiling") != "LOCATOR_ONLY":
        errors.append("BOOTSTRAP_AUTHORITY_CEILING_INVALID")
    if payload.get("project_id") != spec.get("project_id"):
        errors.append("BOOTSTRAP_PROJECT_ID_MISMATCH")
    if payload.get("project_state_ref") != expected_state_ref:
        errors.append("BOOTSTRAP_PROJECT_STATE_REF_MISMATCH")
    if payload.get("authority_ref") != expected_authority_ref:
        errors.append("BOOTSTRAP_AUTHORITY_REF_MISMATCH")
    if leaked:
        errors.append("BOOTSTRAP_FORBIDDEN_AUTHORITY_FIELDS")
    tracked = bool(_git("-C", str(repository), "ls-files", "--error-unmatch", ".oleander/project.json", check=False))
    return {
        "status": "VERIFIED_LOCATOR_ONLY" if not errors else "HOLD_INVALID",
        "ref": ".oleander/project.json",
        "tracked": tracked,
        "locator_only_verified": not errors,
        "errors": errors,
        "project_id": payload.get("project_id"),
        "project_state_ref": payload.get("project_state_ref"),
        "authority_ref": payload.get("authority_ref"),
        "authority_ceiling": payload.get("authority_ceiling"),
    }


def build_inventory() -> dict[str, Any]:
    container_head = _git("rev-parse", "HEAD")
    container_branch = _git("branch", "--show-current")
    remote = _git("config", "--get", "remote.origin.url", check=False) or None
    projects: list[dict[str, Any]] = []
    for slug, spec in PROJECTS.items():
        branch = f"migration/{slug}"
        sha = _branch_sha(branch)
        source_path = ROOT / "05-cases" / slug
        local_repository = LOCAL_PROJECTS_ROOT / slug
        local_ready = (local_repository / ".git").is_dir()
        local_head = None if not local_ready else _git("-C", str(local_repository), "rev-parse", "HEAD", check=False) or None
        local_branch = None if not local_ready else _git("-C", str(local_repository), "branch", "--show-current", check=False) or None
        local_remotes_raw = None if not local_ready else _git("-C", str(local_repository), "remote", check=False) or None
        local_dirty_raw = None if not local_ready else _git("-C", str(local_repository), "status", "--porcelain", check=False) or None
        tree_entries = [] if sha is None else [line for line in _git("ls-tree", "--name-only", sha).splitlines() if line]
        history_count = None if sha is None else int(_git("rev-list", "--count", sha))
        state_evidence = (
            _verify_project_state_evidence(local_repository, spec)
            if local_ready
            else {
                "status": "LOCAL_REPOSITORY_NOT_READY",
                "evidence_ref": spec["state_evidence"],
                "evidence_class": spec["state_evidence_class"],
                "owner_native_project_state_verified": False,
            }
        )
        bootstrap = (
            _read_bootstrap_manifest(local_repository, spec, state_evidence)
            if local_ready and state_evidence.get("owner_native_project_state_verified")
            else {
                "status": "NOT_ELIGIBLE_PROJECT_STATE_UNRESOLVED",
                "ref": ".oleander/project.json",
                "tracked": False,
                "locator_only_verified": False,
            }
        )
        contains_split = _is_ancestor(local_repository, sha, local_head) if local_ready else False
        next_actions: list[str] = []
        if not state_evidence.get("owner_native_project_state_verified"):
            next_actions.append("VERIFY_OWNER_NATIVE_PROJECT_STATE")
        next_actions.extend([
            "VERIFY_ARTIFACT_AND_KNOWLEDGE_BINDINGS",
            "VERIFY_TARGET_REMOTE_EXISTENCE_AND_HISTORY",
            "CREATE_TARGET_REMOTE_REPOSITORY_IF_VERIFIED_ABSENT_AND_EXPLICITLY_AUTHORIZED",
            "PUSH_SPLIT_HISTORY_IF_REMOTE_ROUTE_VERIFIED_AND_EXPLICITLY_AUTHORIZED",
            "READBACK_REMOTE_HISTORY_AFTER_ANY_REMOTE_MUTATION",
        ])
        if state_evidence.get("owner_native_project_state_verified") and not bootstrap.get("locator_only_verified"):
            next_actions.append("BIND_PROJECT_MANIFEST")
        elif not state_evidence.get("owner_native_project_state_verified"):
            next_actions.append("BIND_PROJECT_MANIFEST_ONLY_AFTER_OWNER_NATIVE_PROJECT_STATE_VERIFIED")
        next_actions.append("REMOVE_OLD_MONOREPO_DUPLICATE_ONLY_AFTER_VERIFIED_BINDING")
        projects.append({
            "project_candidate_id": slug.split("-", 1)[0].upper(),
            "project_id": spec["project_id"],
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
            "local_repository_contains_split_history": contains_split,
            "local_repository_dirty": bool(local_dirty_raw),
            "local_repository_remotes": [] if not local_remotes_raw else local_remotes_raw.splitlines(),
            # Local `git remote` state cannot prove whether a target repository
            # already exists elsewhere or whether this split history was pushed
            # from another clone. Keep external state explicitly unverified
            # until an owner-authorized remote readback establishes it.
            "remote_repo_created": None,
            "remote_repo_pushed": None,
            "remote_repository_verification": "UNVERIFIED",
            "remote_history_verification": "UNVERIFIED",
            "old_duplicate_retained": source_path.is_dir(),
            "project_state_evidence": state_evidence,
            "project_state_ref": state_evidence.get("project_state_ref"),
            "authority_ref": state_evidence.get("authority_ref"),
            "bootstrap_manifest": bootstrap,
            "artifact_store_binding": "UNRESOLVED",
            "knowledge_mount_binding": "UNRESOLVED",
            "authority_ceiling": "MIGRATION_READBACK_ONLY",
            "next_actions": next_actions,
        })
    complete = all(
        row["migration_state"] == "SPLIT_BRANCH_READY"
        and row["local_repository_ready"]
        and row["local_repository_contains_split_history"]
        for row in projects
    )
    owner_native_state_verified_count = sum(
        1 for row in projects if (row.get("project_state_evidence") or {}).get("owner_native_project_state_verified")
    )
    locator_verified_count = sum(
        1 for row in projects if (row.get("bootstrap_manifest") or {}).get("locator_only_verified")
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
        "binding_progress": {
            "owner_native_project_state_verified": owner_native_state_verified_count,
            "bootstrap_locator_verified": locator_verified_count,
            "project_state_unresolved": len(projects) - owner_native_state_verified_count,
            "artifact_store_unresolved": sum(1 for row in projects if row["artifact_store_binding"] == "UNRESOLVED"),
            "knowledge_mount_unresolved": sum(1 for row in projects if row["knowledge_mount_binding"] == "UNRESOLVED"),
        },
        "projects": projects,
        "hard_invariants": [
            "GIT_SPLIT_BRANCH_NE_PROJECT_CURRENT",
            "LOCAL_REMOTE_CONFIG_NE_REMOTE_REPOSITORY_EXISTENCE_OR_HISTORY",
            "REMOTE_REPOSITORY_CREATION_NE_PROJECT_PROMOTION",
            "OLD_DUPLICATE_REMOVAL_REQUIRES_VERIFIED_PROJECT_ARTIFACT_KNOWLEDGE_BINDING",
            "PUBLIC_STATUS_SUMMARY_NE_OWNER_NATIVE_PROJECT_STATE",
            "BOOTSTRAP_MANIFEST_IS_LOCATOR_ONLY_NOT_PROJECT_STATE",
        ],
        "does_not_prove": ["PROJECT_CURRENT", "REMOTE_REPOSITORY_CREATED", "REMOTE_PUSHED", "DESIGN_KEEP", "PROMOTION"],
    }


def main() -> None:
    payload = build_inventory()
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "output": str(OUTPUT), "projects": payload["projects"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
