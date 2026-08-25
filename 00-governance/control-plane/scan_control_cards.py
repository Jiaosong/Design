#!/usr/bin/env python3
"""Discover and validate current OLEANDER Control Cards across the repository.

This is a discovery wrapper around the existing Control Plane validator. It does
not create a second registry or Gate. Historical/provenance zones are excluded
from prospective fail-closed enforcement. Current cards must use the current
Control Card schema version; older versions remain readable only in excluded
historical/replay zones.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from control_plane import CURRENT_SCHEMA_VERSION, validate_card  # noqa: E402

CARD_SIGNATURE_KEYS = {
    "object",
    "mode",
    "decision_question",
    "problem_layer",
    "authority_source",
}

EXCLUDED_PREFIXES = (
    "99-archive/",
    "practice/",
    "tools/",
    "00-governance/control-plane/replays/",
    "00-governance/control-plane/examples/",
    "00-governance/control-plane/tests/",
    "00-governance/receipts/",
    "00-governance/audits/",
    "00-governance/migration/",
)


def _relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_excluded(relative_path: str) -> bool:
    return any(relative_path.startswith(prefix) for prefix in EXCLUDED_PREFIXES)


def looks_like_control_card(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and isinstance(value.get("schema_version"), str)
        and CARD_SIGNATURE_KEYS.issubset(value.keys())
    )


def scan_repository(root: Path) -> dict[str, Any]:
    root = root.resolve()
    discovered: list[dict[str, Any]] = []
    invalid: list[dict[str, Any]] = []
    parse_errors: list[dict[str, str]] = []

    for path in sorted(root.rglob("*.json")):
        rel = _relative_posix(path, root)
        if is_excluded(rel):
            continue
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            parse_errors.append({"path": rel, "error": str(exc)})
            continue
        if not looks_like_control_card(value):
            continue

        version = value.get("schema_version")
        if version != CURRENT_SCHEMA_VERSION:
            errors = [{
                "code": "CURRENT_CONTROL_CARD_VERSION_DEPRECATED",
                "message": f"Current stored Control Cards must use schema_version={CURRENT_SCHEMA_VERSION}; observed={version}. Historical/replay cards belong only in excluded provenance zones.",
            }]
        else:
            findings = validate_card(value)
            errors = [
                {"code": f.code, "message": f.message}
                for f in findings
                if f.level == "ERROR"
            ]

        record = {
            "path": rel,
            "schema_version": version,
            "problem_layer": value.get("problem_layer"),
            "change_kind": (value.get("change_scope") or {}).get("kind") if isinstance(value.get("change_scope"), dict) else None,
            "mode": value.get("mode"),
            "authority_state": (value.get("authority_source") or {}).get("state"),
            "status": "FAIL" if errors else "PASS",
        }
        discovered.append(record)
        if errors:
            invalid.append({**record, "errors": errors})

    return {
        "status": "FAIL" if invalid else "PASS",
        "current_schema_version": CURRENT_SCHEMA_VERSION,
        "discovered_current_control_cards": discovered,
        "invalid_current_control_cards": invalid,
        "excluded_prefixes": list(EXCLUDED_PREFIXES),
        "unrelated_json_parse_errors": parse_errors,
        "does_not_prove": [
            "Scan PASS is not Design PASS or MAIN status.",
            "Scan PASS does not upgrade Field, Rights, Engineering, Human, Promotion or Release state.",
            "Excluded provenance zones remain readable history and are not rewritten by this scanner.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan repository for current OLEANDER Control Cards")
    parser.add_argument("--root", default=str(HERE.parents[1]), help="Repository root; defaults to current checkout")
    args = parser.parse_args(argv)
    result = scan_repository(Path(args.root))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
