from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class RefRecord:
    branch: str
    sha: str
    committed_at: str
    subject: str
    classification: str
    protected_reason: str = ""


def run(*args: str, check: bool = True) -> str:
    proc = subprocess.run(
        args,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.stdout.strip()


def repo_root() -> Path:
    return Path(run("git", "rev-parse", "--show-toplevel"))


def github_repo() -> str:
    remote = run("git", "remote", "get-url", "origin")
    if remote.startswith("https://github.com/"):
        value = remote.removeprefix("https://github.com/").removesuffix(".git")
    elif remote.startswith("git@github.com:"):
        value = remote.removeprefix("git@github.com:").removesuffix(".git")
    else:
        raise RuntimeError(f"unsupported GitHub origin: {remote}")
    if value.count("/") != 1:
        raise RuntimeError(f"cannot resolve owner/repo from origin: {remote}")
    return value


def open_prs(repo: str) -> list[dict]:
    raw = run(
        "gh",
        "pr",
        "list",
        "--repo",
        repo,
        "--state",
        "open",
        "--limit",
        "1000",
        "--json",
        "number,headRefName,baseRefName,isDraft,updatedAt,title",
    )
    return json.loads(raw or "[]")


def active_worktree_branches() -> set[str]:
    out = run("git", "worktree", "list", "--porcelain")
    result: set[str] = set()
    prefix = "branch refs/heads/"
    for line in out.splitlines():
        if line.startswith(prefix):
            result.add(line[len(prefix) :])
    return result


def remote_merged_records() -> list[RefRecord]:
    fmt = "%(refname:short)|%(objectname)|%(committerdate:iso8601)|%(subject)"
    out = run(
        "git",
        "for-each-ref",
        "--merged=refs/remotes/origin/main",
        f"--format={fmt}",
        "refs/remotes/origin",
    )
    records: list[RefRecord] = []
    for line in out.splitlines():
        parts = line.split("|", 3)
        if len(parts) != 4:
            continue
        ref, sha, committed_at, subject = parts
        if not ref.startswith("origin/"):
            continue
        branch = ref.removeprefix("origin/")
        if branch in {"HEAD", "main"}:
            continue
        records.append(RefRecord(branch, sha, committed_at, subject, "MERGED_REMOTE"))
    return records


def remote_unmerged_records() -> list[RefRecord]:
    fmt = "%(refname:short)|%(objectname)|%(committerdate:iso8601)|%(subject)"
    out = run(
        "git",
        "for-each-ref",
        "--no-merged=refs/remotes/origin/main",
        f"--format={fmt}",
        "refs/remotes/origin",
    )
    records: list[RefRecord] = []
    for line in out.splitlines():
        parts = line.split("|", 3)
        if len(parts) != 4:
            continue
        ref, sha, committed_at, subject = parts
        if not ref.startswith("origin/"):
            continue
        branch = ref.removeprefix("origin/")
        if branch in {"HEAD", "main"}:
            continue
        records.append(RefRecord(branch, sha, committed_at, subject, "UNMERGED_REMOTE"))
    return records


def local_merged_records() -> list[RefRecord]:
    fmt = "%(refname:short)|%(objectname)|%(committerdate:iso8601)|%(subject)"
    out = run(
        "git",
        "for-each-ref",
        "--merged=refs/remotes/origin/main",
        f"--format={fmt}",
        "refs/heads",
    )
    records: list[RefRecord] = []
    for line in out.splitlines():
        parts = line.split("|", 3)
        if len(parts) != 4:
            continue
        branch, sha, committed_at, subject = parts
        if branch == "main":
            continue
        records.append(RefRecord(branch, sha, committed_at, subject, "MERGED_LOCAL"))
    return records


def classify(
    records: list[RefRecord],
    *,
    open_heads: set[str],
    open_bases: set[str],
    worktrees: set[str],
    explicit_keep: set[str],
) -> tuple[list[RefRecord], list[RefRecord]]:
    delete: list[RefRecord] = []
    protected: list[RefRecord] = []
    for item in records:
        reason = ""
        if item.branch in open_heads:
            reason = "OPEN_PR_HEAD"
        elif item.branch in open_bases:
            reason = "OPEN_PR_BASE"
        elif item.branch in worktrees:
            reason = "ACTIVE_WORKTREE"
        elif item.branch in explicit_keep:
            reason = "EXPLICIT_KEEP"
        elif item.branch == "gh-pages" or item.branch.startswith(("release/", "archive/")):
            reason = "DURABLE_BRANCH_CLASS"

        if reason:
            protected.append(
                RefRecord(
                    item.branch,
                    item.sha,
                    item.committed_at,
                    item.subject,
                    "PROTECTED_MERGED_REF",
                    reason,
                )
            )
        else:
            delete.append(
                RefRecord(
                    item.branch,
                    item.sha,
                    item.committed_at,
                    item.subject,
                    "SAFE_DELETE_MERGED_REF",
                )
            )
    return delete, protected


def write_receipt(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, records: list[RefRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(records[0]).keys()) if records else [
            "branch", "sha", "committed_at", "subject", "classification", "protected_reason"
        ])
        writer.writeheader()
        for item in records:
            writer.writerow(asdict(item))


def build_unmerged_triage(
    records: list[RefRecord], prs: list[dict], worktrees: set[str]
) -> dict:
    head_prs: dict[str, list[int]] = {}
    base_prs: dict[str, list[int]] = {}
    for item in prs:
        number = int(item["number"])
        head = item.get("headRefName")
        base = item.get("baseRefName")
        if head:
            head_prs.setdefault(head, []).append(number)
        if base:
            base_prs.setdefault(base, []).append(number)

    rows: list[dict] = []
    role_counts = {"OPEN_PR_HEAD": 0, "OPEN_PR_BASE": 0, "ACTIVE_WORKTREE": 0, "ORPHAN_UNMERGED": 0}
    for item in records:
        roles: list[str] = []
        if item.branch in head_prs:
            roles.append("OPEN_PR_HEAD")
            role_counts["OPEN_PR_HEAD"] += 1
        if item.branch in base_prs:
            roles.append("OPEN_PR_BASE")
            role_counts["OPEN_PR_BASE"] += 1
        if item.branch in worktrees:
            roles.append("ACTIVE_WORKTREE")
            role_counts["ACTIVE_WORKTREE"] += 1
        if not roles:
            roles.append("ORPHAN_UNMERGED")
            role_counts["ORPHAN_UNMERGED"] += 1
        rows.append(
            {
                **asdict(item),
                "roles": roles,
                "open_pr_head_numbers": head_prs.get(item.branch, []),
                "open_pr_base_numbers": base_prs.get(item.branch, []),
                "automatic_delete_allowed": False,
            }
        )

    return {
        "schema": "OLEANDER_GIT_BRANCH_UNMERGED_TRIAGE_v1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "repository": github_repo(),
        "origin_main_sha": run("git", "rev-parse", "refs/remotes/origin/main"),
        "open_pr_count": len(prs),
        "counts": {"remote_unmerged": len(records), **role_counts},
        "policy": {
            "age_only_delete_forbidden": True,
            "content_or_frontier_disposition_required": True,
            "branch_ref_is_not_current_authority": True,
        },
        "branches": rows,
    }


def hypothetical_merge_tree(base_ref: str, head_ref: str) -> tuple[str | None, str]:
    proc = subprocess.run(
        ["git", "merge-tree", "--write-tree", base_ref, head_ref],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        return None, "CONFLICT"
    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    if not lines:
        return None, "ERROR_NO_TREE"
    return lines[0], "CLEAN"


def build_noop_orphan_audit(
    records: list[RefRecord],
    *,
    open_heads: set[str],
    open_bases: set[str],
    worktrees: set[str],
    explicit_keep: set[str],
) -> dict:
    main_sha = run("git", "rev-parse", "refs/remotes/origin/main")
    main_tree = run("git", "rev-parse", "refs/remotes/origin/main^{tree}")
    safe: list[dict] = []
    counts = {
        "remote_unmerged": len(records),
        "dependency_protected": 0,
        "merge_conflict_or_error": 0,
        "merge_changes_main": 0,
        "safe_noop_orphan": 0,
    }

    for item in records:
        dependencies: list[str] = []
        if item.branch in open_heads:
            dependencies.append("OPEN_PR_HEAD")
        if item.branch in open_bases:
            dependencies.append("OPEN_PR_BASE")
        if item.branch in worktrees:
            dependencies.append("ACTIVE_WORKTREE")
        if item.branch in explicit_keep:
            dependencies.append("EXPLICIT_KEEP")
        if item.branch == "gh-pages" or item.branch.startswith(("release/", "archive/")):
            dependencies.append("DURABLE_BRANCH_CLASS")
        if dependencies:
            counts["dependency_protected"] += 1
            continue

        merged_tree, merge_state = hypothetical_merge_tree(
            "refs/remotes/origin/main", f"refs/remotes/origin/{item.branch}"
        )
        if merge_state != "CLEAN":
            counts["merge_conflict_or_error"] += 1
            continue
        if merged_tree != main_tree:
            counts["merge_changes_main"] += 1
            continue

        counts["safe_noop_orphan"] += 1
        safe.append(
            {
                **asdict(item),
                "classification": "SAFE_DELETE_NOOP_UNMERGED_ORPHAN",
                "hypothetical_merge_base": main_sha,
                "hypothetical_merge_result_tree": merged_tree,
                "current_main_tree": main_tree,
                "content_equivalence": "EXACT_TREE_NOOP",
            }
        )

    return {
        "schema": "OLEANDER_GIT_BRANCH_NOOP_ORPHAN_CLEANUP_AUDIT_v1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "repository": github_repo(),
        "origin_main_sha": main_sha,
        "origin_main_tree": main_tree,
        "counts": counts,
        "policy": {
            "age_only_delete_forbidden": True,
            "open_pr_heads_protected": True,
            "open_pr_bases_protected": True,
            "active_worktrees_protected": True,
            "exact_hypothetical_merge_tree_noop_required": True,
            "audit_before_delete": True,
        },
        "safe_noop_orphans": safe,
    }


def build_patch_equivalent_orphan_audit(
    records: list[RefRecord],
    *,
    open_heads: set[str],
    open_bases: set[str],
    worktrees: set[str],
    explicit_keep: set[str],
) -> dict:
    main_ref = "refs/remotes/origin/main"
    main_sha = run("git", "rev-parse", main_ref)
    safe: list[dict] = []
    counts = {
        "remote_unmerged": len(records),
        "dependency_protected": 0,
        "has_unique_merge_commits": 0,
        "empty_or_ambiguous_cherry": 0,
        "has_unabsorbed_plus": 0,
        "count_mismatch": 0,
        "safe_patch_equivalent_orphan": 0,
    }

    for item in records:
        dependencies: list[str] = []
        if item.branch in open_heads:
            dependencies.append("OPEN_PR_HEAD")
        if item.branch in open_bases:
            dependencies.append("OPEN_PR_BASE")
        if item.branch in worktrees:
            dependencies.append("ACTIVE_WORKTREE")
        if item.branch in explicit_keep:
            dependencies.append("EXPLICIT_KEEP")
        if item.branch == "gh-pages" or item.branch.startswith(("release/", "archive/")):
            dependencies.append("DURABLE_BRANCH_CLASS")
        if dependencies:
            counts["dependency_protected"] += 1
            continue

        head_ref = f"refs/remotes/origin/{item.branch}"
        range_spec = f"{main_ref}..{head_ref}"
        unique_count = int(run("git", "rev-list", "--count", range_spec))
        unique_merge_count = int(run("git", "rev-list", "--count", "--merges", range_spec))
        if unique_merge_count != 0:
            counts["has_unique_merge_commits"] += 1
            continue

        cherry_lines = [
            line.strip()
            for line in run("git", "cherry", main_ref, head_ref).splitlines()
            if line.strip()
        ]
        if not cherry_lines:
            counts["empty_or_ambiguous_cherry"] += 1
            continue
        plus = [line for line in cherry_lines if line.startswith("+")]
        minus = [line for line in cherry_lines if line.startswith("-")]
        if plus:
            counts["has_unabsorbed_plus"] += 1
            continue
        if len(cherry_lines) != unique_count or len(minus) != unique_count:
            counts["count_mismatch"] += 1
            continue

        counts["safe_patch_equivalent_orphan"] += 1
        safe.append(
            {
                **asdict(item),
                "classification": "SAFE_DELETE_PATCH_EQUIVALENT_UNMERGED_ORPHAN",
                "comparison_main_sha": main_sha,
                "unique_commit_count": unique_count,
                "unique_merge_commit_count": unique_merge_count,
                "git_cherry_minus_count": len(minus),
                "git_cherry_plus_count": len(plus),
                "patch_equivalence": "ALL_UNIQUE_NON_MERGE_COMMITS_ALREADY_ABSORBED",
            }
        )

    return {
        "schema": "OLEANDER_GIT_BRANCH_PATCH_EQUIVALENT_ORPHAN_CLEANUP_AUDIT_v1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "repository": github_repo(),
        "origin_main_sha": main_sha,
        "counts": counts,
        "policy": {
            "age_only_delete_forbidden": True,
            "dependency_refs_protected": True,
            "unique_merge_commits_forbidden": True,
            "all_git_cherry_results_must_be_absorbed_minus": True,
            "cherry_count_must_equal_unique_commit_count": True,
            "audit_before_delete": True,
        },
        "safe_patch_equivalent_orphans": safe,
    }


def delete_remote(branches: list[str]) -> None:
    for start in range(0, len(branches), 25):
        batch = branches[start : start + 25]
        if batch:
            subprocess.run(["git", "push", "origin", "--delete", *batch], check=True)


def delete_local(branches: list[str]) -> None:
    for branch in branches:
        subprocess.run(["git", "branch", "-d", branch], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Dependency-aware OLEANDER Git branch audit/cleanup.")
    parser.add_argument("--receipt", type=Path, help="Write JSON audit receipt before any mutation.")
    parser.add_argument("--csv", type=Path, help="Write CSV ref→SHA audit table before any mutation.")
    parser.add_argument("--post-receipt", type=Path, help="Write JSON post-cleanup readback receipt.")
    parser.add_argument("--triage-receipt", type=Path, help="Write JSON inventory of all unmerged remote refs; never deletes them.")
    parser.add_argument("--noop-orphan-receipt", type=Path, help="Write pre-delete audit for unmerged orphan refs whose hypothetical merge is an exact main-tree no-op.")
    parser.add_argument("--noop-orphan-post-receipt", type=Path, help="Write post-delete readback for no-op orphan cleanup.")
    parser.add_argument("--patch-equivalent-orphan-receipt", type=Path, help="Write pre-delete audit for dependency-free unmerged orphan refs whose complete unique non-merge range is patch-equivalent to main.")
    parser.add_argument("--patch-equivalent-orphan-post-receipt", type=Path, help="Write post-delete readback for patch-equivalent orphan cleanup.")
    parser.add_argument("--apply-remote", action="store_true", help="Delete safe merged remote refs.")
    parser.add_argument("--apply-local", action="store_true", help="Delete safe merged local refs.")
    parser.add_argument("--apply-noop-orphans", action="store_true", help="Delete only audited unmerged orphan refs whose clean hypothetical merge leaves main tree unchanged.")
    parser.add_argument("--apply-patch-equivalent-orphans", action="store_true", help="Delete only audited dependency-free unmerged orphan refs whose full unique non-merge commit range is already patch-equivalent in main.")
    parser.add_argument("--keep", action="append", default=[], help="Explicit branch ref to retain; repeatable.")
    args = parser.parse_args()

    root = repo_root()
    repo = github_repo()
    subprocess.run(["git", "fetch", "--prune", "origin"], cwd=root, check=True)

    prs = open_prs(repo)
    open_heads = {item["headRefName"] for item in prs if item.get("headRefName")}
    open_bases = {item["baseRefName"] for item in prs if item.get("baseRefName")}
    worktrees = active_worktree_branches()
    explicit_keep = set(args.keep)

    remote_records = remote_merged_records()
    unmerged_records = remote_unmerged_records()
    local_records = local_merged_records()
    remote_delete, remote_protected = classify(
        remote_records,
        open_heads=open_heads,
        open_bases=open_bases,
        worktrees=worktrees,
        explicit_keep=explicit_keep,
    )
    local_delete, local_protected = classify(
        local_records,
        open_heads=open_heads,
        open_bases=open_bases,
        worktrees=worktrees,
        explicit_keep=explicit_keep,
    )

    now = datetime.now(timezone.utc).isoformat()
    payload = {
        "schema": "OLEANDER_GIT_BRANCH_CLEANUP_AUDIT_v1",
        "as_of": now,
        "repository": repo,
        "origin_main_sha": run("git", "rev-parse", "refs/remotes/origin/main"),
        "delete_branch_on_merge": json.loads(run("gh", "api", f"repos/{repo}"))["delete_branch_on_merge"],
        "open_pr_count": len(prs),
        "counts": {
            "merged_remote": len(remote_records),
            "safe_remote_delete": len(remote_delete),
            "protected_merged_remote": len(remote_protected),
            "merged_local": len(local_records),
            "safe_local_delete": len(local_delete),
            "protected_merged_local": len(local_protected),
        },
        "safe_remote_delete": [asdict(item) for item in remote_delete],
        "protected_merged_remote": [asdict(item) for item in remote_protected],
        "safe_local_delete": [asdict(item) for item in local_delete],
        "protected_merged_local": [asdict(item) for item in local_protected],
        "open_pr_base_refs": sorted(open_bases),
        "worktree_branches": sorted(worktrees),
        "policy": {
            "unmerged_deleted_by_age": False,
            "open_pr_heads_protected": True,
            "open_pr_bases_protected": True,
            "active_worktrees_protected": True,
            "audit_before_delete": True,
        },
    }

    if args.receipt:
        write_receipt(root / args.receipt, payload)
    if args.csv:
        write_csv(root / args.csv, remote_delete + remote_protected)
    if args.triage_receipt:
        write_receipt(root / args.triage_receipt, build_unmerged_triage(unmerged_records, prs, worktrees))

    noop_audit = None
    if args.noop_orphan_receipt or args.apply_noop_orphans:
        noop_audit = build_noop_orphan_audit(
            unmerged_records,
            open_heads=open_heads,
            open_bases=open_bases,
            worktrees=worktrees,
            explicit_keep=explicit_keep,
        )
    if args.noop_orphan_receipt and noop_audit is not None:
        noop_path = root / args.noop_orphan_receipt
        if args.apply_noop_orphans and noop_path.exists():
            existing = json.loads(noop_path.read_text(encoding="utf-8"))
            existing_pairs = {(item["branch"], item["sha"]) for item in existing.get("safe_noop_orphans", [])}
            current_pairs = {(item["branch"], item["sha"]) for item in noop_audit.get("safe_noop_orphans", [])}
            if existing.get("origin_main_sha") != noop_audit.get("origin_main_sha") or existing_pairs != current_pairs:
                raise RuntimeError("no-op orphan audit is stale against current main/candidate set; regenerate and persist audit before mutation")
        else:
            write_receipt(noop_path, noop_audit)

    patch_audit = None
    if args.patch_equivalent_orphan_receipt or args.apply_patch_equivalent_orphans:
        patch_audit = build_patch_equivalent_orphan_audit(
            unmerged_records,
            open_heads=open_heads,
            open_bases=open_bases,
            worktrees=worktrees,
            explicit_keep=explicit_keep,
        )
    if args.patch_equivalent_orphan_receipt and patch_audit is not None:
        patch_path = root / args.patch_equivalent_orphan_receipt
        if args.apply_patch_equivalent_orphans and patch_path.exists():
            existing = json.loads(patch_path.read_text(encoding="utf-8"))
            existing_pairs = {
                (item["branch"], item["sha"])
                for item in existing.get("safe_patch_equivalent_orphans", [])
            }
            current_pairs = {
                (item["branch"], item["sha"])
                for item in patch_audit.get("safe_patch_equivalent_orphans", [])
            }
            if existing.get("origin_main_sha") != patch_audit.get("origin_main_sha") or existing_pairs != current_pairs:
                raise RuntimeError("patch-equivalent orphan audit is stale against current main/candidate set; regenerate and persist audit before mutation")
        else:
            write_receipt(patch_path, patch_audit)

    print(json.dumps(payload["counts"], ensure_ascii=False, indent=2))
    for item in remote_protected:
        print(f"KEEP remote {item.branch}: {item.protected_reason}")
    for item in local_protected:
        print(f"KEEP local  {item.branch}: {item.protected_reason}")

    if (args.apply_remote or args.apply_local) and not args.receipt:
        raise RuntimeError("mutation requires --receipt so pre-delete ref→SHA evidence is persisted first")
    if args.apply_noop_orphans and not args.noop_orphan_receipt:
        raise RuntimeError("no-op orphan mutation requires --noop-orphan-receipt so exact-tree equivalence evidence is persisted first")
    if args.apply_patch_equivalent_orphans and not args.patch_equivalent_orphan_receipt:
        raise RuntimeError("patch-equivalent orphan mutation requires --patch-equivalent-orphan-receipt so patch-equivalence evidence is persisted first")

    if args.apply_remote:
        delete_remote([item.branch for item in remote_delete])
    if args.apply_local:
        delete_local([item.branch for item in local_delete])
    noop_delete_branches: list[str] = []
    if args.apply_noop_orphans and noop_audit is not None:
        noop_delete_branches = [item["branch"] for item in noop_audit["safe_noop_orphans"]]
        delete_remote(noop_delete_branches)
    patch_delete_branches: list[str] = []
    if args.apply_patch_equivalent_orphans and patch_audit is not None:
        patch_delete_branches = [item["branch"] for item in patch_audit["safe_patch_equivalent_orphans"]]
        delete_remote(patch_delete_branches)

    if args.apply_remote or args.apply_local or args.apply_noop_orphans or args.apply_patch_equivalent_orphans:
        subprocess.run(["git", "fetch", "--prune", "origin"], cwd=root, check=True)
        remaining_remote = {item.branch for item in remote_merged_records()}
        remaining_local = {item.branch for item in local_merged_records()}
        post = {
            "schema": "OLEANDER_GIT_BRANCH_CLEANUP_READBACK_v1",
            "as_of": datetime.now(timezone.utc).isoformat(),
            "repository": repo,
            "requested_remote_delete": len(remote_delete) if args.apply_remote else 0,
            "requested_local_delete": len(local_delete) if args.apply_local else 0,
            "remote_delete_remaining": sorted(item.branch for item in remote_delete if item.branch in remaining_remote),
            "local_delete_remaining": sorted(item.branch for item in local_delete if item.branch in remaining_local),
            "protected_remote_still_present": sorted(item.branch for item in remote_protected if item.branch in remaining_remote),
            "verdict": "PASS" if not any(item.branch in remaining_remote for item in remote_delete) and not any(item.branch in remaining_local for item in local_delete) else "FAIL",
        }
        if args.post_receipt:
            write_receipt(root / args.post_receipt, post)
        print(json.dumps(post, ensure_ascii=False, indent=2))
        if post["verdict"] != "PASS":
            return 2

    if args.apply_noop_orphans:
        existing_remote = {
            ref.removeprefix("origin/")
            for ref in run("git", "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin").splitlines()
            if ref.startswith("origin/")
        }
        noop_post = {
            "schema": "OLEANDER_GIT_BRANCH_NOOP_ORPHAN_CLEANUP_READBACK_v1",
            "as_of": datetime.now(timezone.utc).isoformat(),
            "repository": repo,
            "origin_main_sha": run("git", "rev-parse", "refs/remotes/origin/main"),
            "requested_delete": len(noop_delete_branches),
            "delete_remaining": sorted(branch for branch in noop_delete_branches if branch in existing_remote),
            "verdict": "PASS" if not any(branch in existing_remote for branch in noop_delete_branches) else "FAIL",
        }
        if args.noop_orphan_post_receipt:
            write_receipt(root / args.noop_orphan_post_receipt, noop_post)
        print(json.dumps(noop_post, ensure_ascii=False, indent=2))
        if noop_post["verdict"] != "PASS":
            return 3

    if args.apply_patch_equivalent_orphans:
        existing_remote = {
            ref.removeprefix("origin/")
            for ref in run("git", "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin").splitlines()
            if ref.startswith("origin/")
        }
        patch_post = {
            "schema": "OLEANDER_GIT_BRANCH_PATCH_EQUIVALENT_ORPHAN_CLEANUP_READBACK_v1",
            "as_of": datetime.now(timezone.utc).isoformat(),
            "repository": repo,
            "origin_main_sha": run("git", "rev-parse", "refs/remotes/origin/main"),
            "requested_delete": len(patch_delete_branches),
            "delete_remaining": sorted(branch for branch in patch_delete_branches if branch in existing_remote),
            "verdict": "PASS" if not any(branch in existing_remote for branch in patch_delete_branches) else "FAIL",
        }
        if args.patch_equivalent_orphan_post_receipt:
            write_receipt(root / args.patch_equivalent_orphan_post_receipt, patch_post)
        print(json.dumps(patch_post, ensure_ascii=False, indent=2))
        if patch_post["verdict"] != "PASS":
            return 4

    return 0


if __name__ == "__main__":
    sys.exit(main())
