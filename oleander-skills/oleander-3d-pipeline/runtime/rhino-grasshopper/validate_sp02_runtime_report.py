#!/usr/bin/env python3
"""Validate a report produced inside a real Rhino/Grasshopper SP02 execution.

This validator never creates runtime evidence. It only checks an already-produced report.
The report itself must contain Rhino/Grasshopper versions and exact Data Tree topology.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED = {
    "BASE": {"branch_count": 4, "item_count": 24, "items_per_branch": [6, 6, 6, 6]},
    "GRAFT": {"branch_count": 24, "item_count": 24, "items_per_branch": [1] * 24},
    "FLATTEN": {"branch_count": 1, "item_count": 24, "items_per_branch": [24]},
    "TRANSPOSE_BY_ITEM": {"branch_count": 6, "item_count": 24, "items_per_branch": [4, 4, 4, 4, 4, 4]},
}


def validate(report: dict) -> list[str]:
    errors: list[str] = []
    if report.get("marker_version") != "OLEANDER-SP02-HEADLESS-REPORT-v1":
        errors.append("unexpected marker_version")
    if not report.get("runtime"):
        errors.append("runtime missing")
    if not report.get("rhino_version"):
        errors.append("rhino_version missing")
    if not report.get("grasshopper_assembly_version"):
        errors.append("grasshopper_assembly_version missing")

    params = report.get("parameters") or {}
    if params.get("provenance") != "SIMULATED_EXERCISE_ASSUMPTION":
        errors.append("parameter provenance mismatch")

    states = report.get("states") or {}
    for name, expected in EXPECTED.items():
        actual = states.get(name)
        if not isinstance(actual, dict):
            errors.append(f"{name}: state missing")
            continue
        for field, expected_value in expected.items():
            if actual.get(field) != expected_value:
                errors.append(f"{name}.{field}: expected {expected_value!r}, got {actual.get(field)!r}")

    checks = report.get("checks") or {}
    if not all(checks.get(name) is True for name in EXPECTED):
        errors.append("embedded runtime checks are not all true")
    if report.get("cp2_candidate") is not True:
        errors.append("cp2_candidate is not true")
    if report.get("cp4") != "OPEN_HEADLESS_NO_GUI":
        errors.append("cp4 headless boundary mismatch")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--receipt", required=False)
    args = parser.parse_args()

    report_path = Path(args.report)
    if not report_path.exists():
        raise SystemExit(f"runtime report missing: {report_path}")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    errors = validate(report)
    valid = not errors

    result = {
        "validator_id": "OLEANDER-SP02-RUNTIME-REPORT-VALIDATOR-v0.1",
        "report_path": str(report_path),
        "valid_exact_tree_contract": valid,
        "errors": errors,
        "runtime": report.get("runtime"),
        "rhino_version": report.get("rhino_version"),
        "grasshopper_assembly_version": report.get("grasshopper_assembly_version"),
        "cp2_candidate": bool(valid),
        "cp4": "OPEN",
        "note": "Validation success is meaningful only if the input report was actually emitted inside a supported real Rhino/Grasshopper runtime."
    }
    if args.receipt:
        receipt_path = Path(args.receipt)
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if valid else 2


if __name__ == "__main__":
    raise SystemExit(main())
