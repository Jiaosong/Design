from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

DEFAULT_SCHEMA = (
    Path(__file__).resolve().parents[1]
    / "contracts"
    / "BLENDER_3D_RECEIPT_SCHEMAS_v1.json"
)

SECTION_KEYS_WITH_SPECIFIC_RULES = frozenset(
    {
        "01_authority",
        "02_state_classification",
        "03_blender_source_authority",
        "04_sparse_edit",
        "05_surface_diagnostics",
        "06_geometry_topology",
        "07_spatial_models",
        "08_materials_cmf",
        "09_camera_render",
        "10_technical_outputs",
        "11_exchange_roundtrip",
        "12_production_artifacts",
        "13_review_gates",
        "14_failure_routing",
        "15_completion",
    }
)

KNOWN_STATE_CLASSES = {
    "SOURCE_OR_WORKING_SOURCE",
    "DERIVED_EXECUTION",
    "DERIVED_DIAGNOSTIC_NOT_AUTHORITY",
    "VISUALIZATION_OR_RENDER_SCENE",
    "REFERENCE_EVIDENCE",
}

PROMOTED_TOKENS = {"KEEP", "MAIN_KEEP", "PROMOTED", "APPROVED", "PASS"}
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


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


def _require_bool(value: Any, context: str) -> None:
    if not isinstance(value, bool):
        raise ReceiptValidationError(f"{context}: value must be boolean")


def _require_positive_number(value: Any, context: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ReceiptValidationError(f"{context}: value must be numeric")
    if not math.isfinite(float(value)) or float(value) <= 0:
        raise ReceiptValidationError(f"{context}: value must be finite and > 0")


def _require_sha256(value: Any, context: str) -> None:
    text = str(value)
    if text.startswith("sha256:"):
        text = text.split(":", 1)[1]
    if not HEX64.fullmatch(text):
        raise ReceiptValidationError(f"{context}: expected a 64-hex SHA-256 digest")


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


def _pass_or_na(value: Any) -> bool:
    return str(value).upper() in {"PASS", "N/A", "NA", "NOT_APPLICABLE"}


def _validate_section_specific(
    section_key: str,
    payload: dict[str, Any],
    spec: dict[str, Any],
    rows: list[dict[str, Any]] | None,
) -> None:
    if section_key == "01_authority":
        if payload.get("status") == "PASS":
            chain = payload.get("current_authority_chain")
            if not isinstance(chain, list) or not chain:
                raise ReceiptValidationError(
                    "01_authority: PASS requires a non-empty authority chain"
                )
            expected_prefix = ["MASTER_PROTOCOL", "PROJECT_STATE", "SOURCE_AUTHORITY", "CURRENT_TASK"]
            if chain[:4] != expected_prefix:
                raise ReceiptValidationError(
                    "01_authority: PASS requires MASTER_PROTOCOL → PROJECT_STATE → SOURCE_AUTHORITY → CURRENT_TASK order"
                )
            _require_positive_number(payload.get("scale"), "01_authority.scale")
            _require_bool(
                payload.get("source_mutation_authorized"),
                "01_authority.source_mutation_authorized",
            )
            for field in (
                "source_path_or_id",
                "source_revision",
                "authoring_application",
                "authoring_version",
                "units",
                "coordinate_convention",
            ):
                _require_nonempty(payload.get(field), f"01_authority.{field}")

    elif section_key == "02_state_classification":
        assert rows is not None
        ids = [row["object_or_file_id"] for row in rows]
        if len(ids) != len(set(ids)):
            raise ReceiptValidationError(
                "02_state_classification: object_or_file_id values must be unique"
            )
        for index, row in enumerate(rows):
            _require_bool(row.get("editable"), f"02_state_classification.rows[{index}].editable")
            _require_bool(
                row.get("may_mutate_in_current_task"),
                f"02_state_classification.rows[{index}].may_mutate_in_current_task",
            )
            _require_nonempty(row.get("owner"), f"02_state_classification.rows[{index}].owner")
            state = row["state_class"]
            if state in {"DERIVED_EXECUTION", "DERIVED_DIAGNOSTIC_NOT_AUTHORITY"}:
                if row.get("regenerated_from") in (None, "", "N/A", "NA"):
                    raise ReceiptValidationError(
                        f"02_state_classification.rows[{index}]: derived state requires regenerated_from"
                    )
            if state == "REFERENCE_EVIDENCE" and row.get("may_mutate_in_current_task") is True:
                raise ReceiptValidationError(
                    f"02_state_classification.rows[{index}]: reference evidence may not mutate in the task"
                )

    elif section_key == "03_blender_source_authority":
        _require_sha256(payload.get("source_before_sha256"), "03_blender_source_authority.source_before_sha256")
        _require_sha256(payload.get("source_after_sha256"), "03_blender_source_authority.source_after_sha256")
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
            if not isinstance(payload.get("expected_source_objects"), list) or not payload["expected_source_objects"]:
                raise ReceiptValidationError(
                    "03_blender_source_authority: PASS requires expected Source object set"
                )

    elif section_key == "04_sparse_edit":
        allowed_range = payload.get("allowed_range")
        if (
            not isinstance(allowed_range, list)
            or len(allowed_range) != 2
            or any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in allowed_range)
            or allowed_range[0] > allowed_range[1]
        ):
            raise ReceiptValidationError(
                "04_sparse_edit: allowed_range must be [min, max] numeric and ordered"
            )
        for field in ("previous_value", "new_value", "rollback_value"):
            value = payload.get(field)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ReceiptValidationError(f"04_sparse_edit.{field}: value must be numeric")
        if not (allowed_range[0] <= payload["new_value"] <= allowed_range[1]):
            raise ReceiptValidationError(
                "04_sparse_edit: new_value must remain inside allowed_range"
            )
        if payload["rollback_value"] != payload["previous_value"]:
            raise ReceiptValidationError(
                "04_sparse_edit: rollback_value must reproduce previous_value"
            )
        _require_nonempty(payload.get("before_evidence_ids"), "04_sparse_edit.before_evidence_ids")
        _require_nonempty(payload.get("after_evidence_ids"), "04_sparse_edit.after_evidence_ids")
        if payload.get("status") == "PASS" and payload["new_value"] == payload["previous_value"]:
            raise ReceiptValidationError(
                "04_sparse_edit: PASS edit delta cannot be a no-op"
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
        for index, row in enumerate(rows):
            _require_sha256(
                row.get("source_sha256"),
                f"05_surface_diagnostics.rows[{index}].source_sha256",
            )
            for field in (
                "reference_asset",
                "candidate_asset",
                "camera_id",
                "rig_id",
                "material_id",
                "color_management_id",
                "render_settings_id",
                "crop_id",
            ):
                _require_nonempty(row.get(field), f"05_surface_diagnostics.rows[{index}].{field}")
            if row["reference_asset"] == row["candidate_asset"]:
                raise ReceiptValidationError(
                    f"05_surface_diagnostics.rows[{index}]: reference and candidate assets must be distinct"
                )

    elif section_key == "06_geometry_topology":
        if payload.get("status") == "PASS":
            for field in ("source_structure_checks", "derived_topology_checks"):
                value = payload.get(field)
                if isinstance(value, dict):
                    value = value.get("status")
                if not _pass_or_na(value):
                    raise ReceiptValidationError(
                        f"06_geometry_topology: PASS requires {field}=PASS/N/A"
                    )
            for field in (
                "normals_check",
                "manifoldness_check",
                "boundary_drift_check",
                "units_check",
                "bounds_check",
                "uv_material_id_check",
            ):
                if not _pass_or_na(payload.get(field)):
                    raise ReceiptValidationError(
                        f"06_geometry_topology: PASS requires {field}=PASS/N/A"
                    )
            if payload.get("source_form_quality_not_inferred") is not True:
                raise ReceiptValidationError(
                    "06_geometry_topology: topology PASS may not infer Source form quality"
                )
            if payload.get("failure_codes") not in ([], {}, None):
                raise ReceiptValidationError(
                    "06_geometry_topology: PASS cannot retain failure_codes"
                )

    elif section_key == "07_spatial_models":
        assert rows is not None
        ids = [row["geometry_id"] for row in rows]
        if len(ids) != len(set(ids)):
            raise ReceiptValidationError(
                "07_spatial_models: geometry_id values must be unique"
            )
        for index, row in enumerate(rows):
            field_status = str(row.get("field_status", "")).upper()
            evidence_class = row["evidence_class"]
            if evidence_class == "FIELD_MEASURED":
                if "OPEN" in field_status or not any(token in field_status for token in ("MEASURED", "VERIFIED")):
                    raise ReceiptValidationError(
                        f"07_spatial_models.rows[{index}]: FIELD_MEASURED requires measured/verified field status"
                    )
            elif evidence_class in {"INFERRED", "ASSUMED", "DESIGN_PROPOSAL", "VISUALIZATION_ENTOURAGE"}:
                if any(token in field_status for token in ("MEASURED", "VERIFIED")):
                    raise ReceiptValidationError(
                        f"07_spatial_models.rows[{index}]: non-measured evidence may not claim field measured/verified status"
                    )
            value_range = row.get("range_if_any")
            recommended = row.get("recommended_value_if_any")
            if value_range not in (None, [], ""):
                if (
                    not isinstance(value_range, list)
                    or len(value_range) != 2
                    or any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in value_range)
                    or value_range[0] > value_range[1]
                ):
                    raise ReceiptValidationError(
                        f"07_spatial_models.rows[{index}]: range_if_any must be ordered numeric [min, max]"
                    )
                if isinstance(recommended, (int, float)) and not isinstance(recommended, bool):
                    if not value_range[0] <= recommended <= value_range[1]:
                        raise ReceiptValidationError(
                            f"07_spatial_models.rows[{index}]: recommended value must lie inside range"
                        )

    elif section_key == "08_materials_cmf":
        assert rows is not None
        comparison_locks = {
            (row["geometry_sha256"], row["camera_id"], row["rig_id"])
            for row in rows
        }
        if len(rows) > 1 and len(comparison_locks) != 1:
            raise ReceiptValidationError(
                "08_materials_cmf: controlled CMF comparison requires identical geometry/camera/rig"
            )
        evidence_required = {
            "MANUFACTURER_SPEC",
            "MEASURED_PHYSICAL_FINISH",
            "PRODUCTION_CMF_DECISION",
        }
        for index, row in enumerate(rows):
            _require_sha256(row.get("geometry_sha256"), f"08_materials_cmf.rows[{index}].geometry_sha256")
            if str(row.get("macro_form_masking_check", "")).upper() != "PASS":
                raise ReceiptValidationError(
                    f"08_materials_cmf.rows[{index}]: macro-form masking check must PASS"
                )
            if str(row.get("microdetail_role", "")).upper() in {"MASKING", "CONCEAL_GEOMETRY", "GEOMETRY_FIX"}:
                raise ReceiptValidationError(
                    f"08_materials_cmf.rows[{index}]: microdetail may not mask or repair geometry"
                )
            if row["claim_level"] in evidence_required:
                source = str(row.get("physical_evidence_source", "")).upper()
                status = str(row.get("physical_evidence_status", "")).upper()
                if source in {"", "NONE", "NOT_PROVIDED", "N/A"} or status in {"", "NONE", "NOT_PROVIDED", "N/A"}:
                    raise ReceiptValidationError(
                        f"08_materials_cmf.rows[{index}]: claim level {row['claim_level']} requires physical evidence"
                    )

    elif section_key == "09_camera_render":
        if payload.get("status") == "PASS":
            if payload.get("drift_detected") is not False:
                raise ReceiptValidationError(
                    "09_camera_render: PASS requires drift_detected=false"
                )
            _require_positive_number(payload.get("samples"), "09_camera_render.samples")
            for field in (
                "camera_transform",
                "projection",
                "focal_length_or_ortho_scale",
                "crop_and_aspect",
                "view_transform",
                "color_management",
                "world_background",
                "light_transforms",
                "light_sizes",
                "light_energy",
                "light_shapes",
                "diagnostic_material",
                "comparison_variable",
            ):
                _require_nonempty(payload.get(field), f"09_camera_render.{field}")

    elif section_key == "10_technical_outputs":
        if payload.get("status") == "PASS":
            if payload.get("vector_text_confirmed") is not True:
                raise ReceiptValidationError(
                    "10_technical_outputs: PASS requires vector_text_confirmed=true"
                )
            editable = str(payload.get("editable_vector_asset", ""))
            allowed_extensions = (".svg", ".ai", ".pdf", ".dxf", ".dwg")
            if not editable.lower().endswith(allowed_extensions):
                raise ReceiptValidationError(
                    "10_technical_outputs: editable_vector_asset must be a vector/editable technical format"
                )
            _require_nonempty(payload.get("preview_asset"), "10_technical_outputs.preview_asset")
            _require_nonempty(payload.get("assembly_groups"), "10_technical_outputs.assembly_groups")
            _require_nonempty(payload.get("connection_logic"), "10_technical_outputs.connection_logic")
            _require_nonempty(payload.get("dimension_status_legend"), "10_technical_outputs.dimension_status_legend")
            if not isinstance(payload.get("explosion_offsets"), dict):
                raise ReceiptValidationError(
                    "10_technical_outputs: explosion_offsets must be a structured object"
                )

    elif section_key == "11_exchange_roundtrip":
        _require_sha256(payload.get("source_sha256"), "11_exchange_roundtrip.source_sha256")
        _require_sha256(payload.get("export_sha256"), "11_exchange_roundtrip.export_sha256")
        if payload.get("status") == "PASS":
            if payload.get("source_authority_unchanged") is not True:
                raise ReceiptValidationError(
                    "11_exchange_roundtrip: PASS requires source_authority_unchanged=true"
                )
            for field in (
                "units_check",
                "bounds_check",
                "axis_check",
                "origin_check",
                "hierarchy_check",
                "instance_check",
                "normals_check",
                "materials_textures_check",
                "camera_animation_check_if_applicable",
                "critical_named_objects_check",
            ):
                if not _pass_or_na(payload.get(field)):
                    raise ReceiptValidationError(
                        f"11_exchange_roundtrip: PASS requires {field}=PASS/N/A"
                    )
            drift = str(payload.get("topology_or_geometry_drift", "")).upper()
            if drift not in {"NONE", "NONE_OBSERVED", "NO", "0", "N/A", "NOT_APPLICABLE"}:
                raise ReceiptValidationError(
                    "11_exchange_roundtrip: PASS cannot retain unaccepted topology/geometry drift"
                )

    elif section_key == "12_production_artifacts":
        assert rows is not None
        paths = [row["path"] for row in rows]
        if len(paths) != len(set(paths)):
            raise ReceiptValidationError(
                "12_production_artifacts: manifest paths must be unique"
            )
        for index, row in enumerate(rows):
            _require_positive_number(row.get("bytes"), f"12_production_artifacts.rows[{index}].bytes")
            _require_sha256(row.get("sha256"), f"12_production_artifacts.rows[{index}].sha256")
            if row.get("state_class") not in KNOWN_STATE_CLASSES:
                raise ReceiptValidationError(
                    f"12_production_artifacts.rows[{index}]: unknown state_class"
                )
            if str(row.get("current_or_superseded", "")).upper() == "CURRENT":
                if str(row.get("validation_status", "")).upper() != "PASS":
                    raise ReceiptValidationError(
                        f"12_production_artifacts.rows[{index}]: CURRENT artifact requires validation_status=PASS"
                    )
                if str(row.get("recoverability", "")).upper() in {"MISSING", "UNRECOVERABLE", "NOT_TESTED"}:
                    raise ReceiptValidationError(
                        f"12_production_artifacts.rows[{index}]: CURRENT artifact must be recoverable"
                    )

    elif section_key == "13_review_gates":
        main_requested = payload.get("main_promotion_requested") is True
        independent = payload.get("independent_review_present") is True
        design_gate = payload.get("design_quality_gate")
        final_state = str(payload.get("final_promotion_state", "")).upper()
        promoted = final_state in PROMOTED_TOKENS

        _require_bool(payload.get("main_promotion_requested"), "13_review_gates.main_promotion_requested")
        _require_bool(payload.get("independent_review_present"), "13_review_gates.independent_review_present")

        if design_gate == "KEEP" and not independent:
            raise ReceiptValidationError(
                "13_review_gates: Design KEEP requires independent review"
            )
        if independent:
            reviewer = str(payload.get("design_review_system_or_reviewer", ""))
            if reviewer.upper() in {"", "NONE", "NOT_RUN"}:
                raise ReceiptValidationError(
                    "13_review_gates: independent review requires an identified review system/reviewer"
                )
            if reviewer.strip().casefold() == str(payload.get("producer", "")).strip().casefold():
                raise ReceiptValidationError(
                    "13_review_gates: producer cannot be recorded as the independent reviewer"
                )
        if main_requested and not independent:
            if design_gate != "HOLD":
                raise ReceiptValidationError(
                    "13_review_gates: MAIN request without independent review must remain Design HOLD"
                )
            if promoted:
                raise ReceiptValidationError(
                    "13_review_gates: MAIN request cannot be promoted without independent review"
                )
        if promoted:
            if not main_requested:
                raise ReceiptValidationError(
                    "13_review_gates: promoted final state requires main_promotion_requested=true"
                )
            if payload.get("machine_gate") != "PASS" or payload.get("evidence_gate") != "PASS":
                raise ReceiptValidationError(
                    "13_review_gates: promotion requires Machine PASS and Evidence PASS"
                )
            if design_gate != "KEEP" or not independent:
                raise ReceiptValidationError(
                    "13_review_gates: promotion requires independent Design KEEP"
                )

    elif section_key == "14_failure_routing":
        controlled = payload.get("controlled_variables")
        if not isinstance(controlled, list) or not controlled:
            raise ReceiptValidationError(
                "14_failure_routing: controlled_variables must be a non-empty list"
            )
        changed = payload.get("changed_variable")
        chosen = payload.get("chosen_edit_target")
        rejected = payload.get("rejected_edit_targets")
        _require_nonempty(payload.get("isolation_test"), "14_failure_routing.isolation_test")
        _require_nonempty(changed, "14_failure_routing.changed_variable")
        _require_nonempty(chosen, "14_failure_routing.chosen_edit_target")
        if changed in controlled:
            raise ReceiptValidationError(
                "14_failure_routing: changed_variable may not also be listed as controlled"
            )
        if isinstance(rejected, list) and chosen in rejected:
            raise ReceiptValidationError(
                "14_failure_routing: chosen edit target may not also be rejected"
            )
        _require_nonempty(payload.get("root_cause_confidence"), "14_failure_routing.root_cause_confidence")
        _require_nonempty(payload.get("next_action"), "14_failure_routing.next_action")

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
            if payload.get("machine_gate") != "PASS" or payload.get("evidence_gate") != "PASS":
                raise ReceiptValidationError(
                    "15_completion: complete status requires Machine PASS and Evidence PASS"
                )
            requested = payload.get("requested_deliverables")
            statuses = payload.get("deliverable_statuses")
            if not isinstance(requested, list) or not requested:
                raise ReceiptValidationError(
                    "15_completion: complete status requires requested deliverables"
                )
            if not isinstance(statuses, dict):
                raise ReceiptValidationError(
                    "15_completion: deliverable_statuses must be an object"
                )
            complete_tokens = {"COMPLETE", "PASS", "NOT_APPLICABLE", "N/A"}
            for deliverable in requested:
                if str(statuses.get(deliverable, "")).upper() not in complete_tokens:
                    raise ReceiptValidationError(
                        f"15_completion: requested deliverable {deliverable!r} is not complete"
                    )
            _require_nonempty(payload.get("evidence_receipts"), "15_completion.evidence_receipts")
            _require_nonempty(payload.get("reopen_or_machine_checks"), "15_completion.reopen_or_machine_checks")


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
    if set(sections) != SECTION_KEYS_WITH_SPECIFIC_RULES:
        raise ReceiptValidationError(
            "Validator/schema section coverage mismatch; every Skill section requires a section-specific rule"
        )
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
        "section_specific_rule": True,
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
