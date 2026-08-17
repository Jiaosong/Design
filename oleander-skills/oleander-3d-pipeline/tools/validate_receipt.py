from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_SCHEMA = (
    Path(__file__).resolve().parents[1]
    / "contracts"
    / "BLENDER_3D_RECEIPT_SCHEMAS_v1.json"
)


class ReceiptValidationError(ValueError):
    """Raised when a section receipt violates the OLEANDER 3D receipt contract."""


def _require_fields(data: dict[str, Any], fields: list[str], context: str) -> None:
    missing = [field for field in fields if field not in data]
    if missing:
        raise ReceiptValidationError(
            f"{context}: missing required fields: {', '.join(missing)}"
        )


def _require_enum(value: Any, allowed: list[Any], context: str) -> None:
    if value not in allowed:
        raise ReceiptValidationError(
            f"{context}: {value!r} not in allowed values {allowed!r}"
        )


def _require_nonempty(value: Any, context: str) -> None:
    if value in (None, "", [], {}):
        raise ReceiptValidationError(f"{context}: value must be non-empty")


def _validate_common(payload: dict[str, Any], schema: dict[str, Any]) -> None:
    _require_fields(payload, schema["common_required_fields"], "common")
    for field in schema["common_required_fields"]:
        _require_nonempty(payload[field], f"common.{field}")


def _validate_rows(
    section_key: str,
    payload: dict[str, Any],
    spec: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = payload.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ReceiptValidationError(f"{section_key}: rows must be a non-empty list")
    required = spec["row_required_fields"]
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ReceiptValidationError(
                f"{section_key}.rows[{index}]: row must be an object"
            )
        _require_fields(row, required, f"{section_key}.rows[{index}]")
    return rows


def _validate_object(
    section_key: str,
    payload: dict[str, Any],
    spec: dict[str, Any],
) -> None:
    _require_fields(payload, spec["required_fields"], section_key)


def _validate_enums(
    section_key: str,
    payload: dict[str, Any],
    spec: dict[str, Any],
    rows: list[dict[str, Any]] | None,
) -> None:
    if "status_enum" in spec:
        _require_enum(payload.get("status"), spec["status_enum"], f"{section_key}.status")

    if rows is None:
        if "machine_enum" in spec:
            _require_enum(payload.get("machine_gate"), spec["machine_enum"], f"{section_key}.machine_gate")
        if "evidence_enum" in spec:
            _require_enum(payload.get("evidence_gate"), spec["evidence_enum"], f"{section_key}.evidence_gate")
        if "design_enum" in spec:
            _require_enum(payload.get("design_quality_gate"), spec["design_enum"], f"{section_key}.design_quality_gate")
        if "final_status_enum" in spec:
            _require_enum(payload.get("final_status"), spec["final_status_enum"], f"{section_key}.final_status")
        return

    enum_bindings = (
        ("state_enum", "state_class"),
        ("view_enum", "view"),
        ("evidence_class_enum", "evidence_class"),
        ("claim_level_enum", "claim_level"),
        ("evidence_result_enum", "evidence_result"),
    )
    for enum_key, field in enum_bindings:
        if enum_key not in spec:
            continue
        for index, row in enumerate(rows):
            _require_enum(
                row.get(field),
                spec[enum_key],
                f"{section_key}.rows[{index}].{field}",
            )


def _validate_section_specific(
    section_key: str,
    payload: dict[str, Any],
    spec: dict[str, Any],
    rows: list[dict[str, Any]] | None,
) -> None:
    if section_key == "03_blender_source_authority":
        if payload.get("status") == "PASS":
            if payload.get("source_unchanged") is not True:
                raise ReceiptValidationError(
                    "03_blender_source_authority: PASS requires source_unchanged=true"
                )
            if payload.get("material_slots_preserved") is not True:
                raise ReceiptValidationError(
                    "03_blender_source_authority: PASS requires material_slots_preserved=true"
                )
            if payload.get("source_before_sha256") != payload.get("source_after_sha256"):
                raise ReceiptValidationError(
                    "03_blender_source_authority: PASS requires identical before/after Source digest"
                )
            if payload.get("diagnostic_proxy_role") != "DERIVED_DIAGNOSTIC_NOT_AUTHORITY":
                raise ReceiptValidationError(
                    "03_blender_source_authority: diagnostic proxy role is not non-authoritative"
                )
            authority = payload.get("diagnostic_proxy_authority")
            if authority not in (False, "DERIVED_EXECUTION_NOT_AUTHORITY"):
                raise ReceiptValidationError(
                    "03_blender_source_authority: diagnostic proxy may not be authoritative"
                )

    elif section_key == "05_surface_diagnostics":
        assert rows is not None
        views = [row["view"] for row in rows]
        required_views = spec["view_enum"]
        if sorted(views) != sorted(required_views):
            raise ReceiptValidationError(
                "05_surface_diagnostics: exactly one BROAD/STRIP/GRAZING/ZEBRA row is required"
            )
        source_hashes = {row["source_sha256"] for row in rows}
        if len(source_hashes) != 1:
            raise ReceiptValidationError(
                "05_surface_diagnostics: all controlled views must bind the same Source digest"
            )

    elif section_key == "13_review_gates":
        main_requested = payload.get("main_promotion_requested") is True
        independent = payload.get("independent_review_present") is True
        design_gate = payload.get("design_quality_gate")
        final_state = str(payload.get("final_promotion_state", "")).upper()
        promoted_tokens = {"KEEP", "MAIN_KEEP", "PROMOTED", "APPROVED", "PASS"}
        if main_requested and not independent:
            if design_gate != "HOLD":
                raise ReceiptValidationError(
                    "13_review_gates: MAIN request without independent review must remain Design HOLD"
                )
            if final_state in promoted_tokens:
                raise ReceiptValidationError(
                    "13_review_gates: MAIN request cannot be promoted without independent review"
                )

    elif section_key == "15_completion":
        if payload.get("final_status") == "COMPLETE_TO_REQUESTED_SCOPE":
            if payload.get("authority_boundaries_intact") is not True:
                raise ReceiptValidationError(
                    "15_completion: complete status requires intact authority boundaries"
                )
            if payload.get("residual_blockers") not in ([], {}, None):
                raise ReceiptValidationError(
                    "15_completion: complete status cannot retain residual blockers"
                )


def load_schema(path: str | Path = DEFAULT_SCHEMA) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_receipt(
    section_key: str,
    payload: dict[str, Any],
    schema: dict[str, Any],
) -> dict[str, Any]:
    sections = schema.get("sections", {})
    if section_key not in sections:
        raise ReceiptValidationError(f"Unknown section: {section_key}")
    if not isinstance(payload, dict):
        raise ReceiptValidationError("Receipt payload must be a JSON object")

    _validate_common(payload, schema)
    spec = sections[section_key]
    rows: list[dict[str, Any]] | None = None
    if "row_required_fields" in spec:
        rows = _validate_rows(section_key, payload, spec)
    else:
        _validate_object(section_key, payload, spec)
    _validate_enums(section_key, payload, spec, rows)
    _validate_section_specific(section_key, payload, spec, rows)

    return {
        "status": "PASS",
        "section": section_key,
        "receipt": spec["receipt"],
        "row_count": len(rows) if rows is not None else None,
        "boundary": schema["boundary"],
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fail-closed validator for OLEANDER 3D pipeline section receipts."
    )
    parser.add_argument("--section", required=True, help="Section key, e.g. 05_surface_diagnostics")
    parser.add_argument("--input", required=True, help="Receipt JSON file")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA), help="Receipt schema JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        schema = load_schema(args.schema)
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        result = validate_receipt(args.section, payload, schema)
    except (OSError, json.JSONDecodeError, ReceiptValidationError) as exc:
        print(
            json.dumps(
                {"status": "FAIL", "section": getattr(args, "section", None), "error": str(exc)},
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2

    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
