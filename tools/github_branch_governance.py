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
    parser.add_argument("--apply-remote", action="store_true", help="Delete safe merged remote refs.")
    parser.add_argument("--apply-local", action="store_true", help="Delete safe merged local refs.")
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

    print(json.dumps(payload["counts"], ensure_ascii=False, indent=2))
    for item in remote_protected:
        print(f"KEEP remote {item.branch}: {item.protected_reason}")
    for item in local_protected:
        print(f"KEEP local  {item.branch}: {item.protected_reason}")

    if (args.apply_remote or args.apply_local) and not args.receipt:
        raise RuntimeError("mutation requires --receipt so pre-delete ref→SHA evidence is persisted first")

    if args.apply_remote:
        delete_remote([item.branch for item in remote_delete])
    if args.apply_local:
        delete_local([item.branch for item in local_delete])

    if args.apply_remote or args.apply_local:
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

    return 0


if __name__ == "__main__":
    sys.exit(main())
