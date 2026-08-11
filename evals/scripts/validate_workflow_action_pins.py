#!/usr/bin/env python3
"""Fail closed when GitHub workflows use mutable external action references."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"
FULL_COMMIT_SHA = re.compile(r"^[0-9a-fA-F]{40}$")
USES_LINE = re.compile(r"^\s*(?:-\s*)?uses:\s*([^\s#]+)")


def external_action_ref(line: str):
    match = USES_LINE.match(line)
    if not match:
        return None
    ref = match.group(1).strip("'\"")
    if ref.startswith("./") or ref.startswith("docker://"):
        return None
    return ref


def validate():
    violations = []
    workflow_files = sorted(WORKFLOWS.glob("*.yml")) + sorted(WORKFLOWS.glob("*.yaml"))
    if not workflow_files:
        raise AssertionError("no GitHub workflow files found")

    for path in workflow_files:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            ref = external_action_ref(line)
            if ref is None:
                continue
            if "@" not in ref:
                violations.append((path, lineno, ref, "missing @ref"))
                continue
            _, revision = ref.rsplit("@", 1)
            if not FULL_COMMIT_SHA.fullmatch(revision):
                violations.append((path, lineno, ref, "mutable or non-commit ref"))

    if violations:
        details = "\n".join(
            f"- {path.relative_to(ROOT)}:{lineno}: {ref} ({reason})"
            for path, lineno, ref, reason in violations
        )
        raise AssertionError(
            "external GitHub Actions dependencies must use full 40-character immutable commit SHAs:\n"
            + details
        )

    print(f"WORKFLOW ACTION PIN AUDIT: PASS ({len(workflow_files)} workflows)")


def main():
    try:
        validate()
    except AssertionError as exc:
        print(f"WORKFLOW ACTION PIN AUDIT: FAIL\n{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
