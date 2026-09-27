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
        "state_evidence_class": "OWNER_NATIVE_PROJECT_STATE",
        "project_state_kind": "PUBLIC_PROJECT_STATE",
        "project_state_ref": "file:README.md",
        "authority_ref": "platform-file:00-governance/OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT.json#PRJ-C01-YIMAI-GUANGDU",
        "required_markers": ["Current public state:", "Canonical status map"],
        "authority_evidence": "00-governance/OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT.json",
        "authority_markers": ["PRJ-C01-YIMAI-GUANGDU", "whole_project_authority", "05-cases/c01-yimai-guangdu/README.md"],
    },
    "c02-daylily": {
        "project_id": "PRJ-C02-DAYLILY",
        "state_evidence": "README.md",
        "state_evidence_class": "OWNER_NATIVE_PROJECT_STATE",
        "project_state_kind": "PUBLIC_PROJECT_STATE",
        "project_state_ref": "file:README.md",
        "authority_ref": "platform-file:00-governance/case-map.md#PRJ-C02-DAYLILY",
        "required_markers": ["Current public state:", "Canonical status map"],
        "authority_evidence": "00-governance/case-map.md",
        "authority_markers": ["PRJ-C02-DAYLILY", "PROTOTYPED / TEST PLANNED / NOT RUN"],
    },
    "c03-the-light-collection": {
        "project_id": "PRJ-C03-LIGHT-COLLECTION",
        "state_evidence": "README.md",
        "state_evidence_class": "OWNER_NATIVE_PROJECT_STATE",
        "project_state_kind": "PUBLIC_PROJECT_STATE",
        "project_state_ref": "file:README.md",
        "authority_ref": "platform-file:00-governance/case-map.md#PRJ-C03-LIGHT-COLLECTION",
        "required_markers": ["Current public state:", "Canonical status map"],
        "authority_evidence": "00-governance/case-map.md",
        "authority_markers": ["PRJ-C03-LIGHT-COLLECTION", "VISUALIZED / SAMPLE TEST PENDING"],
    },
    "c04-qingjiang-stone-book": {
        "project_id": "PRJ-C04-QINGJIANG-SHISHU",
        "state_evidence": "C04_CURRENT.md",
        "state_evidence_class": "OWNER_NATIVE_PROJECT_STATE",
        "project_state_kind": "CURRENT_EXECUTION_AUTHORITY",
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
    authority_evidence_ref = spec.get("authority_evidence")
    authority_markers_present = True
    if authority_evidence_ref:
        authority_path = ROOT / str(authority_evidence_ref)
        if not authority_path.is_file():
            authority_markers_present = False
        else:
            try:
                authority_content = authority_path.read_text(encoding="utf-8")
            except OSError:
                authority_markers_present = False
            else:
                authority_markers_present = all(
                    str(marker) in authority_content
                    for marker in spec.get("authority_markers") or []
                )
    declared_ref = spec.get("project_state_ref")
    verified = bool(
        declared_ref
        and spec.get("state_evidence_class") == "OWNER_NATIVE_PROJECT_STATE"
        and project_id_present
        and markers_present
        and authority_markers_present
    )
    return {
        "status": "VERIFIED_OWNER_NATIVE_PROJECT_STATE" if verified else "EVIDENCE_ONLY_NOT_PROJECT_STATE",
        "evidence_ref": evidence_ref,
        "evidence_class": spec["state_evidence_class"],
        "project_id_present": project_id_present,
        "required_markers_present": markers_present,
        "authority_evidence_ref": authority_evidence_ref,
        "authority_markers_present": authority_markers_present,
        "owner_native_project_state_verified": verified,
        "project_state_kind": spec.get("project_state_kind"),
        "project_state_ref": declared_ref if verified else None,
        "authority_ref": spec.get("authority_ref") if verified else None,
        "reason": None if verified else "EVIDENCE_DOES_NOT_DECLARE_OWNER_NATIVE_PROJECT_STATE_AUTHORITY",
    }


def _resolve_repo_ref(repository: Path, ref: str) -> Path | None:
    if not ref.startswith("repo:"):
        return None
    relative = Path(ref[5:])
    if relative.is_absolute() or ".." in relative.parts:
        return None
    candidate = (repository / relative).resolve()
    try:
        candidate.relative_to(repository.resolve())
    except ValueError:
        return None
    return candidate if candidate.exists() else None


def _read_materialization_bindings(repository: Path, spec: dict[str, Any]) -> dict[str, Any]:
    path = repository / ".oleander" / "bindings.json"
    if not path.is_file():
        return {
            "status": "UNRESOLVED",
            "ref": ".oleander/bindings.json",
            "tracked": False,
            "artifact_store_binding": "UNRESOLVED",
            "knowledge_mount_binding": "UNRESOLVED",
        }
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "status": "HOLD_INVALID",
            "ref": ".oleander/bindings.json",
            "tracked": False,
            "artifact_store_binding": "UNRESOLVED",
            "knowledge_mount_binding": "UNRESOLVED",
            "errors": ["BINDINGS_INVALID_JSON"],
        }
    errors: list[str] = []
    if not isinstance(payload, dict):
        errors.append("BINDINGS_NOT_OBJECT")
        payload = {}
    if payload.get("project_id") != spec.get("project_id"):
        errors.append("BINDINGS_PROJECT_ID_MISMATCH")
    if payload.get("authority_ceiling") != "PROJECT_MATERIALIZATION_BINDING_ONLY":
        errors.append("BINDINGS_AUTHORITY_CEILING_INVALID")
    repository_binding = payload.get("repository") if isinstance(payload.get("repository"), dict) else {}
    if repository_binding.get("repository_ref") != "repo:." or repository_binding.get("role") != "PRIMARY":
        errors.append("PRIMARY_REPOSITORY_BINDING_INVALID")
    expected_remote = f"https://github.com/Jiaosong/{repository.name}.git"
    if repository_binding.get("remote_identity") != expected_remote:
        errors.append("REMOTE_IDENTITY_MISMATCH")

    artifact_refs = [
        str(row.get("ref") or "")
        for row in payload.get("artifact_stores") or []
        if isinstance(row, dict)
    ]
    unresolved_artifacts = [ref for ref in artifact_refs if _resolve_repo_ref(repository, ref) is None]
    if unresolved_artifacts:
        errors.append("ARTIFACT_STORE_REF_MISSING")
    artifact_state = str(payload.get("artifact_store_state") or "")
    artifact_binding = (
        "VERIFIED_LOCAL_PATHS"
        if artifact_state == "VERIFIED_LOCAL_PATHS" and artifact_refs and not unresolved_artifacts
        else ("NONE_DECLARED" if artifact_state == "NONE_DECLARED" and not artifact_refs else "UNRESOLVED")
    )
    if artifact_binding == "UNRESOLVED":
        errors.append("ARTIFACT_STORE_BINDING_UNRESOLVED")

    knowledge_refs = [
        str(row.get("ref") or "")
        for row in payload.get("knowledge_mounts") or []
        if isinstance(row, dict)
    ]
    unresolved_knowledge = [ref for ref in knowledge_refs if _resolve_repo_ref(repository, ref) is None]
    if unresolved_knowledge:
        errors.append("KNOWLEDGE_MOUNT_REF_MISSING")
    knowledge_state = str(payload.get("knowledge_mount_state") or "")
    if knowledge_state == "VERIFIED_SOURCE_REFS" and knowledge_refs and not unresolved_knowledge:
        knowledge_binding = "VERIFIED_SOURCE_REFS"
    elif knowledge_state == "NONE_DECLARED_FOR_CURRENT_PUBLIC_STATE" and not knowledge_refs:
        knowledge_binding = "NONE_DECLARED_FOR_CURRENT_PUBLIC_STATE"
    else:
        knowledge_binding = "UNRESOLVED"
        errors.append("KNOWLEDGE_MOUNT_BINDING_UNRESOLVED")

    tracked = bool(_git("-C", str(repository), "ls-files", "--error-unmatch", ".oleander/bindings.json", check=False))
    return {
        "status": "VERIFIED_MATERIALIZATION_BINDINGS" if not errors else "HOLD_INVALID",
        "ref": ".oleander/bindings.json",
        "tracked": tracked,
        "errors": sorted(set(errors)),
        "artifact_store_binding": artifact_binding,
        "artifact_store_refs": artifact_refs,
        "knowledge_mount_binding": knowledge_binding,
        "knowledge_mount_refs": knowledge_refs,
        "remote_identity": repository_binding.get("remote_identity"),
        "authority_ceiling": payload.get("authority_ceiling"),
    }


def _remote_readback(repository: Path, local_head: str | None) -> dict[str, Any]:
    remote_url = _git("-C", str(repository), "remote", "get-url", "origin", check=False) or None
    if not remote_url:
        return {
            "remote_repo_created": None,
            "remote_repo_pushed": None,
            "remote_repository_verification": "UNVERIFIED",
            "remote_history_verification": "UNVERIFIED",
            "remote_url": None,
            "remote_main_revision": None,
        }
    remote_line = _git("-C", str(repository), "ls-remote", "origin", "refs/heads/main", check=False)
    remote_head = remote_line.split()[0] if remote_line else None
    verified = bool(remote_head and local_head and remote_head == local_head)
    return {
        "remote_repo_created": bool(remote_head),
        "remote_repo_pushed": verified,
        "remote_repository_verification": "VERIFIED" if remote_head else "UNVERIFIED",
        "remote_history_verification": "VERIFIED_HEAD_MATCH" if verified else ("HEAD_MISMATCH" if remote_head else "UNVERIFIED"),
        "remote_url": remote_url,
        "remote_main_revision": remote_head,
    }


def _compatibility_reference_files(slug: str) -> list[str]:
    needle = f"05-cases/{slug}"
    raw = _git("grep", "-l", "-F", needle, "--", ":!05-cases/**", check=False)
    return sorted({line.strip() for line in raw.splitlines() if line.strip()}) if raw else []


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
        materialization = (
            _read_materialization_bindings(local_repository, spec)
            if local_ready
            else {
                "status": "LOCAL_REPOSITORY_NOT_READY",
                "artifact_store_binding": "UNRESOLVED",
                "knowledge_mount_binding": "UNRESOLVED",
            }
        )
        remote_readback = (
            _remote_readback(local_repository, local_head)
            if local_ready
            else {
                "remote_repo_created": None,
                "remote_repo_pushed": None,
                "remote_repository_verification": "UNVERIFIED",
                "remote_history_verification": "UNVERIFIED",
                "remote_url": None,
                "remote_main_revision": None,
            }
        )
        contains_split = _is_ancestor(local_repository, sha, local_head) if local_ready else False
        compatibility_refs = _compatibility_reference_files(slug)
        binding_closed = bool(
            state_evidence.get("owner_native_project_state_verified")
            and bootstrap.get("locator_only_verified")
            and materialization.get("status") == "VERIFIED_MATERIALIZATION_BINDINGS"
            and remote_readback.get("remote_history_verification") == "VERIFIED_HEAD_MATCH"
        )
        next_actions: list[str] = []
        if not state_evidence.get("owner_native_project_state_verified"):
            next_actions.append("VERIFY_OWNER_NATIVE_PROJECT_STATE")
        if materialization.get("status") != "VERIFIED_MATERIALIZATION_BINDINGS":
            next_actions.append("VERIFY_ARTIFACT_AND_KNOWLEDGE_BINDINGS")
        if remote_readback.get("remote_history_verification") != "VERIFIED_HEAD_MATCH":
            next_actions.extend([
                "VERIFY_TARGET_REMOTE_EXISTENCE_AND_HISTORY",
                "CREATE_TARGET_REMOTE_REPOSITORY_IF_VERIFIED_ABSENT_AND_EXPLICITLY_AUTHORIZED",
                "PUSH_SPLIT_HISTORY_IF_REMOTE_ROUTE_VERIFIED_AND_EXPLICITLY_AUTHORIZED",
                "READBACK_REMOTE_HISTORY_AFTER_ANY_REMOTE_MUTATION",
            ])
        if state_evidence.get("owner_native_project_state_verified") and not bootstrap.get("locator_only_verified"):
            next_actions.append("BIND_PROJECT_MANIFEST")
        elif not state_evidence.get("owner_native_project_state_verified"):
            next_actions.append("BIND_PROJECT_MANIFEST_ONLY_AFTER_OWNER_NATIVE_PROJECT_STATE_VERIFIED")
        if source_path.is_dir() and compatibility_refs:
            next_actions.append("RETAIN_COMPATIBILITY_MOUNT_UNTIL_PLATFORM_REFERENCE_REWRITE")
        elif source_path.is_dir() and binding_closed:
            next_actions.append("REMOVE_OLD_MONOREPO_DUPLICATE")
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
            **remote_readback,
            "old_duplicate_retained": source_path.is_dir(),
            "old_source_role": "COMPATIBILITY_MOUNT" if source_path.is_dir() and compatibility_refs else ("DUPLICATE_REMOVAL_ELIGIBLE" if source_path.is_dir() and binding_closed else "LEGACY_SOURCE"),
            "compatibility_reference_count": len(compatibility_refs),
            "compatibility_reference_files": compatibility_refs,
            "migration_binding_closed": binding_closed,
            "project_state_evidence": state_evidence,
            "project_state_ref": state_evidence.get("project_state_ref"),
            "authority_ref": state_evidence.get("authority_ref"),
            "bootstrap_manifest": bootstrap,
            "materialization_bindings": materialization,
            "artifact_store_binding": materialization.get("artifact_store_binding", "UNRESOLVED"),
            "knowledge_mount_binding": materialization.get("knowledge_mount_binding", "UNRESOLVED"),
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
    remote_verified_count = sum(
        1 for row in projects if row.get("remote_history_verification") == "VERIFIED_HEAD_MATCH"
    )
    materialization_verified_count = sum(
        1 for row in projects if (row.get("materialization_bindings") or {}).get("status") == "VERIFIED_MATERIALIZATION_BINDINGS"
    )
    full_binding_closed = all(row.get("migration_binding_closed") is True for row in projects)
    return {
        "schema": "oleander.project-repository-migration-inventory.v0.1",
        "status": "MIGRATION_COMPLETE_COMPATIBILITY_MOUNT" if complete and full_binding_closed else ("LOCAL_REPOSITORIES_READY" if complete else "SPLIT_IN_PROGRESS"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_ceiling": "MIGRATION_READBACK_ONLY",
        "container_repository": remote,
        "container_branch": container_branch,
        "container_revision": container_head,
        "migration_strategy": "HISTORY_PRESERVING_SPLIT_TO_PRIMARY_INDEPENDENT_REPOSITORIES_WITH_REFERENCE_GATED_COMPATIBILITY_MOUNTS",
        "binding_progress": {
            "owner_native_project_state_verified": owner_native_state_verified_count,
            "bootstrap_locator_verified": locator_verified_count,
            "project_state_unresolved": len(projects) - owner_native_state_verified_count,
            "artifact_store_unresolved": sum(1 for row in projects if row["artifact_store_binding"] == "UNRESOLVED"),
            "knowledge_mount_unresolved": sum(1 for row in projects if row["knowledge_mount_binding"] == "UNRESOLVED"),
            "materialization_bindings_verified": materialization_verified_count,
            "remote_history_verified": remote_verified_count,
            "compatibility_mounts_retained": sum(1 for row in projects if row.get("old_source_role") == "COMPATIBILITY_MOUNT"),
        },
        "projects": projects,
        "hard_invariants": [
            "GIT_SPLIT_BRANCH_NE_PROJECT_CURRENT",
            "LOCAL_REMOTE_CONFIG_NE_REMOTE_REPOSITORY_EXISTENCE_OR_HISTORY",
            "REMOTE_REPOSITORY_CREATION_NE_PROJECT_PROMOTION",
            "OLD_DUPLICATE_REMOVAL_REQUIRES_VERIFIED_PROJECT_ARTIFACT_KNOWLEDGE_BINDING",
            "PROJECT_STATE_REF_NE_PROJECT_CURRENT",
            "PUBLIC_PROJECT_STATE_NE_PROJECT_CURRENT",
            "BOOTSTRAP_MANIFEST_IS_LOCATOR_ONLY_NOT_PROJECT_STATE",
            "MATERIALIZATION_BINDINGS_NE_PROJECT_CURRENT",
            "KNOWLEDGE_SOURCE_BINDING_NE_KNOWLEDGE_CURRENT",
            "COMPATIBILITY_MOUNT_NE_PROJECT_AUTHORITY",
        ],
        "does_not_prove": ["PROJECT_CURRENT", "DESIGN_KEEP", "PROFESSIONAL_PASS", "PROMOTION"],
    }


def main() -> None:
    payload = build_inventory()
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "output": str(OUTPUT), "projects": payload["projects"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
