#!/usr/bin/env python3
"""Reject CRLF blobs in critical OLEANDER runtime/workflow source paths.

The check reads Git's committed object at HEAD, not the checked-out working
tree. That distinction is intentional: a GitHub/API connector can create a
blob without passing through a developer's local clean/smudge filters.
"""

from __future__ import annotations

import subprocess
import sys


CRITICAL_PATHS = (
    "00-governance/runtime",
    "90-shared/oleander-core-framework/runtime/notion_canonical_knowledge",
    ".github/workflows",
    "evals/scripts",
)


def committed_crlf_paths() -> list[str]:
    proc = subprocess.run(
        ["git", "grep", "-I", "-l", "\r$", "HEAD", "--", *CRITICAL_PATHS],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode == 1:
        return []
    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip() or "git grep failed"
        raise RuntimeError(detail)

    prefix = "HEAD:"
    paths: list[str] = []
    for raw in proc.stdout.splitlines():
        item = raw.strip()
        if not item:
            continue
        paths.append(item[len(prefix) :] if item.startswith(prefix) else item)
    return paths


def main() -> int:
    try:
        bad = committed_crlf_paths()
    except RuntimeError as exc:
        print(f"runtime line-ending check failed to inspect Git blobs: {exc}", file=sys.stderr)
        return 2

    if bad:
        print("CRLF is forbidden in critical runtime/workflow Git blobs:", file=sys.stderr)
        for path in bad:
            print(f"- {path}", file=sys.stderr)
        print("Normalize the committed blob to LF before merging.", file=sys.stderr)
        return 1


    print("critical runtime/workflow Git blobs: LF clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
