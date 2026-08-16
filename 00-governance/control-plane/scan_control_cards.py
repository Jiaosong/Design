#!/usr/bin/env python3
"""Discover and validate current OLEANDER Control Cards across the repository.

This is a discovery wrapper around the existing Control Plane validator. It does
not create a second registry or Gate. Historical/provenance zones are excluded
from prospective fail-closed enforcement.
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

from control_plane import validate_card  # noqa: E402

CARD_SIGNATURE_KEYS = {
    "object",
    "mode",
    "decision_question",
    "problem_layer",
    "authority_source",
}

# Explicit provenance / frozen legacy zones. These are readable history, not
# prospective Current Control Cards that should be rewritten by a new policy.
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
        and value.get("schema_version") == "0.2"
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
            # Unrelated malformed JSON is outside this scanner's authority; it
            # becomes relevant only if it can be identified as a Control Card.
            parse_errors.append({"path": rel, "error": str(exc)})
            continue
        if not looks_like_control_card(value):
            continue

        findings = validate_card(value)
        errors = [
            {"code": f.code, "message": f.message}
            for f in findings
            if f.level == "ERROR"
        ]
        record = {
            "path": rel,
            "problem_layer": value.get("problem_layer"),
            "mode": value.get("mode"),
            "authority_state": (value.get("authority_source") or {}).get("state"),
            "status": "FAIL" if errors else "PASS",
        }
        discovered.append(record)
        if errors:
            invalid.append({**record, "errors": errors})

    return {
        "status": "FAIL" if invalid else "PASS",
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
