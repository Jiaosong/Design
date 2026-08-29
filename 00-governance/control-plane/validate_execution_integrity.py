#!/usr/bin/env python3
"""Fail-closed execution-integrity validation for existing-project repair.

This extends the existing OLEANDER Control Plane. It does not create a second
project process or registry. Current Control Cards only enter this stricter gate
when they explicitly declare execution_mode=EXISTING_PROJECT_REPAIR.

Mechanisms absorbed, not dependencies imported:
- required-check / fail-closed state transition logic;
- explicit run/input/output lineage;
- dependency-digest stale propagation;
- artifact provenance with resolved inputs and outputs;
- baseline/change-impact/rollback discipline.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from scan_control_cards import is_excluded, looks_like_control_card  # noqa: E402

REPAIR_MODE = "EXISTING_PROJECT_REPAIR"
OWNERS = {"KNOWLEDGE", "DESIGN", "PRESENTATION", "VALIDATION", "GOVERNANCE"}
HANDOFF_ADVANCE_STATES = {"READY", "ACCEPTED", "CLOSED"}
UNRESOLVED_DERIVATIVE_STATES = {"STALE", "REGEN_REQUIRED", "RETEST_REQUIRED", "HOLD"}
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def fail(msg: str) -> None:
    raise SystemExit(f"execution-integrity validation failed: {msg}")


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _artifact_ids(rows: Any) -> set[str]:
    if not isinstance(rows, list):
        return set()
    return {
        row.get("artifact_id")
        for row in rows
        if isinstance(row, dict) and _nonempty(row.get("artifact_id"))
    }


def validate_execution_integrity(card: dict[str, Any]) -> list[str]:
    if card.get("execution_mode") != REPAIR_MODE:
        return []

    errors: list[str] = []
    integrity = card.get("execution_integrity")
    if not isinstance(integrity, dict):
        return ["EXISTING_PROJECT_REPAIR requires execution_integrity"]

    baseline = integrity.get("baseline") if isinstance(integrity.get("baseline"), dict) else {}
    provenance = integrity.get("run_provenance") if isinstance(integrity.get("run_provenance"), dict) else {}
    delta = integrity.get("artifact_delta") if isinstance(integrity.get("artifact_delta"), dict) else {}
    readback = integrity.get("readback") if isinstance(integrity.get("readback"), dict) else {}
    handoff = integrity.get("handoff") if isinstance(integrity.get("handoff"), dict) else {}
    edges = integrity.get("dependency_edges") if isinstance(integrity.get("dependency_edges"), list) else []
    impacts = integrity.get("change_impact") if isinstance(integrity.get("change_impact"), list) else []

    for field in ("best_existing_artifact_id", "best_existing_ref", "rollback_ref"):
        if not _nonempty(baseline.get(field)):
            errors.append(f"baseline.{field} is required in repair mode")

    input_ids = _artifact_ids(provenance.get("inputs"))
    output_ids = _artifact_ids(provenance.get("outputs"))
    if baseline.get("best_existing_artifact_id") not in input_ids:
        errors.append("best_existing_artifact_id must be present in run_provenance.inputs")

    producer = provenance.get("producer_owner")
    if producer not in OWNERS:
        errors.append("run_provenance.producer_owner must be a valid lifecycle owner")
    if not _nonempty(provenance.get("run_id")):
        errors.append("run_provenance.run_id is required")

    delta_state = delta.get("state")
    changed_ids = set(delta.get("changed_artifact_ids", [])) if isinstance(delta.get("changed_artifact_ids"), list) else set()
    binding_changed = delta.get("authority_binding_changed") is True
    if delta_state == "MATERIAL":
        if not changed_ids and not binding_changed:
            errors.append("MATERIAL artifact_delta requires changed_artifact_ids or authority_binding_changed=true")
        missing_outputs = sorted(changed_ids - output_ids)
        if missing_outputs:
            errors.append(f"changed_artifact_ids missing from run_provenance.outputs: {missing_outputs}")
    elif delta_state == "NONE":
        if changed_ids or binding_changed:
            errors.append("artifact_delta state NONE cannot declare changed artifacts or authority binding change")
    else:
        errors.append("artifact_delta.state must be NONE or MATERIAL")

    readback_state = readback.get("state")
    if readback_state == "PASS":
        if not _nonempty(readback.get("medium")):
            errors.append("readback PASS requires a real medium")
        if not readback.get("artifact_ids"):
            errors.append("readback PASS requires artifact_ids")

    handoff_state = handoff.get("state")
    if handoff_state in HANDOFF_ADVANCE_STATES:
        if delta_state != "MATERIAL":
            errors.append(f"handoff {handoff_state} requires MATERIAL artifact_delta")
        if readback_state != "PASS":
            errors.append(f"handoff {handoff_state} requires readback PASS")
        from_owner, to_owner = handoff.get("from_owner"), handoff.get("to_owner")
        if from_owner not in OWNERS or to_owner not in OWNERS:
            errors.append(f"handoff {handoff_state} requires valid from_owner and to_owner")
        elif from_owner == to_owner:
            errors.append(f"handoff {handoff_state} must cross an owner boundary")
        if not _nonempty(handoff.get("required_next_check")):
            errors.append(f"handoff {handoff_state} requires required_next_check")
        if handoff_state in {"ACCEPTED", "CLOSED"} and not _nonempty(handoff.get("receiver_master_ref")):
            errors.append(f"handoff {handoff_state} requires receiver_master_ref")

    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            continue
        current_digest = edge.get("current_input_digest")
        consumed_digest = edge.get("consumed_input_digest")
        output_status = edge.get("output_status")
        if isinstance(current_digest, str) and isinstance(consumed_digest, str):
            if current_digest != consumed_digest and output_status == "CURRENT":
                errors.append(
                    f"dependency_edges[{index}] digest drift cannot leave output CURRENT; mark STALE/REGEN_REQUIRED/RETEST_REQUIRED/HOLD"
                )

    if handoff_state == "CLOSED":
        unresolved_edges = [
            index for index, edge in enumerate(edges)
            if isinstance(edge, dict) and edge.get("output_status") in UNRESOLVED_DERIVATIVE_STATES
        ]
        if unresolved_edges:
            errors.append(f"handoff CLOSED has unresolved dependency edges: {unresolved_edges}")
        unresolved_impacts = [
            item.get("artifact_id", f"index {index}")
            for index, item in enumerate(impacts)
            if isinstance(item, dict)
            and item.get("required_action") != "NONE"
            and item.get("status") not in {"DONE", "N_A"}
        ]
        if unresolved_impacts:
            errors.append(f"handoff CLOSED has unresolved change-impact items: {unresolved_impacts}")

    return errors


def _scan_repair_cards(root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    checked: list[dict[str, Any]] = []
    invalid: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*.json")):
        rel = path.relative_to(root).as_posix()
        if is_excluded(rel):
            continue
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not looks_like_control_card(value) or value.get("execution_mode") != REPAIR_MODE:
            continue
        errors = validate_execution_integrity(value)
        row = {"path": rel, "status": "FAIL" if errors else "PASS"}
        checked.append(row)
        if errors:
            invalid.append({**row, "errors": errors})
    return checked, invalid


def _regression_card() -> dict[str, Any]:
    digest_a = "a" * 64
    digest_b = "b" * 64
    return {
        "execution_mode": REPAIR_MODE,
        "execution_integrity": {
            "baseline": {
                "best_existing_artifact_id": "BASE-01",
                "best_existing_ref": "main@abc",
                "rollback_ref": "main@abc",
                "preserve_dimensions": ["authority", "hierarchy"],
            },
            "run_provenance": {
                "run_id": "RUN-01",
                "producer_owner": "PRESENTATION",
                "skill_refs": ["oleander-design-process/EXISTING_PROJECT_REPAIR_EXTENSION.md"],
                "inputs": [{"artifact_id": "BASE-01", "digest": digest_a, "location": "base.html"}],
                "outputs": [{"artifact_id": "OUT-01", "digest": digest_b, "location": "out.html"}],
            },
            "artifact_delta": {
                "state": "MATERIAL",
                "changed_artifact_ids": ["OUT-01"],
                "authority_binding_changed": False,
                "description": "Bound authority-ready asset and preserved locked structure",
            },
            "readback": {"state": "PASS", "medium": "browser", "artifact_ids": ["OUT-01"]},
            "handoff": {
                "state": "READY",
                "from_owner": "PRESENTATION",
                "to_owner": "VALIDATION",
                "required_next_check": "desktop/mobile/reduced-motion browser validation",
                "receiver_master_ref": None,
            },
            "dependency_edges": [{
                "input_artifact_id": "BASE-01",
                "current_input_digest": digest_a,
                "consumed_input_digest": digest_a,
                "output_artifact_id": "OUT-01",
                "output_status": "CURRENT",
            }],
            "change_impact": [{
                "artifact_id": "OUT-01",
                "impact": "DIRECT",
                "required_action": "RETEST",
                "status": "OPEN",
            }],
        },
    }


def validate_regression_examples() -> None:
    good = _regression_card()
    if validate_execution_integrity(good):
        fail(f"valid regression card rejected: {validate_execution_integrity(good)}")

    no_delta = _regression_card()
    no_delta["execution_integrity"]["artifact_delta"] = {
        "state": "NONE", "changed_artifact_ids": [], "authority_binding_changed": False, "description": "no material change"
    }
    if not any("requires MATERIAL" in error for error in validate_execution_integrity(no_delta)):
        fail("regression failed to reject handoff without material artifact delta")

    stale = _regression_card()
    stale["execution_integrity"]["dependency_edges"][0]["current_input_digest"] = "c" * 64
    if not any("digest drift" in error for error in validate_execution_integrity(stale)):
        fail("regression failed to reject CURRENT derivative after input digest drift")

    closed = _regression_card()
    closed["execution_integrity"]["handoff"].update({"state": "CLOSED", "receiver_master_ref": "out.html@sha"})
    if not any("unresolved change-impact" in error for error in validate_execution_integrity(closed)):
        fail("regression failed to reject CLOSED handoff with unresolved impact")


def main() -> None:
    validate_regression_examples()
    checked, invalid = _scan_repair_cards(ROOT)
    if invalid:
        fail(json.dumps(invalid, ensure_ascii=False, indent=2))
    print("execution-integrity validation: PASS")
    print(f"current repair-mode Control Cards checked: {len(checked)}")
    print("artifact-delta handoff gate: ENFORCED WHEN repair mode is declared")
    print("explicit run/input/output provenance: ENFORCED WHEN repair mode is declared")
    print("dependency-digest stale propagation: ENFORCED WHEN repair mode is declared")
    print("baseline/change-impact/rollback closure: ENFORCED WHEN repair mode is declared")
    print("does not prove: Design KEEP, Validation PASS, Field truth, or release readiness")


if __name__ == "__main__":
    main()
