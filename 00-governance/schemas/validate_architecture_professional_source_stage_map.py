#!/usr/bin/env python3
"""Validate Architecture -> professional source-stage companion map.

This validator checks referential/structural integrity only. It does not infer
interface maturity, professional PASS, statutory compliance, field validity,
Design KEEP or Promotion.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAP_PATH = ROOT / "architecture-professional-source-stage-map.v1.json"
STRUCT_PATH = ROOT / "structural-engineering-design-process.v1.json"
MEP_PATH = ROOT / "building-services-mep-design-process.v1.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    mapping = load(MAP_PATH)
    structural = load(STRUCT_PATH)
    mep = load(MEP_PATH)

    errors: list[str] = []
    rows = mapping.get("mappings", [])
    expected_add = {f"ADD-{i:02d}" for i in range(18)}
    actual_add = {row.get("architecture_stage_id") for row in rows}

    if actual_add != expected_add:
        missing = sorted(expected_add - actual_add)
        extra = sorted(actual_add - expected_add)
        if missing:
            errors.append("missing Architecture stage mappings: " + ", ".join(missing))
        if extra:
            errors.append("unexpected Architecture stage mappings: " + ", ".join(extra))

    if len(rows) != len(actual_add):
        errors.append("duplicate architecture_stage_id values in source-stage map")

    structural_ids = {stage["stage_id"] for stage in structural.get("stages", [])}
    mep_ids = {stage["stage_id"] for stage in mep.get("stages", [])}

    for row in rows:
        add_id = row.get("architecture_stage_id", "<unknown>")
        for field in (
            "architecture_decision",
            "structural_source_stage_refs",
            "structural_expected_sources",
            "mep_source_stage_refs",
            "mep_expected_sources",
        ):
            if field not in row:
                errors.append(f"{add_id}: missing {field}")

        for ref in row.get("structural_source_stage_refs", []):
            if ref == "CURRENT_APPLICABLE_SE_STAGE":
                continue
            if ref not in structural_ids:
                errors.append(f"{add_id}: unknown structural source stage {ref}")

        for ref in row.get("mep_source_stage_refs", []):
            if ref == "CURRENT_APPLICABLE_BSP_STAGE":
                continue
            if ref not in mep_ids:
                errors.append(f"{add_id}: unknown MEP source stage {ref}")

        if not row.get("structural_expected_sources"):
            errors.append(f"{add_id}: structural_expected_sources must be non-empty")
        if not row.get("mep_expected_sources"):
            errors.append(f"{add_id}: mep_expected_sources must be non-empty")

    forbidden = {
        "required_maturity_to_enter",
        "required_maturity_to_close",
        "disposition",
        "professional_verdict",
        "review_verdict",
    }
    text = MAP_PATH.read_text(encoding="utf-8")
    for key in forbidden:
        if f'"{key}"' in text:
            errors.append(
                f"source-stage map must not duplicate Integration/professional truth field: {key}"
            )

    if errors:
        print("ARCHITECTURE PROFESSIONAL SOURCE-STAGE MAP: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "ARCHITECTURE PROFESSIONAL SOURCE-STAGE MAP: PASS "
        f"({len(rows)} ADD mappings; {len(structural_ids)} structural stages; {len(mep_ids)} MEP stages)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
