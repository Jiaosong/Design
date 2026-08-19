#!/usr/bin/env python3
"""Validate OLEANDER 3D v2 MODELING_ROUTE_RECEIPT files without third-party dependencies."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTRACT = HERE.parent / "contracts" / "3D_MODELING_ROUTE_CONTRACT_v1.json"


def validate_receipt(receipt: dict, contract: dict) -> list[str]:
    errors: list[str] = []
    required = contract["required_receipt_fields"]
    for key in required:
        if key not in receipt:
            errors.append(f"MISSING_FIELD:{key}")

    route = receipt.get("route")
    if route not in contract["routes"]:
        errors.append(f"INVALID_ROUTE:{route}")
    rep = receipt.get("representation_family")
    if rep not in contract["representation_families"]:
        errors.append(f"INVALID_REPRESENTATION_FAMILY:{rep}")

    for key in ("hard_constraints", "functional_constraints", "design_decisions", "assumptions", "required_stage_graph", "required_diagnostics", "does_not_prove"):
        if key in receipt and not isinstance(receipt[key], list):
            errors.append(f"FIELD_NOT_LIST:{key}")

    if route in contract["route_requirements"]:
        expected = contract["route_requirements"][route]["required_stage_prefix"]
        actual = receipt.get("required_stage_graph", [])
        if actual[: len(expected)] != expected:
            errors.append(f"STAGE_PREFIX_MISMATCH:{route}")

    if not receipt.get("source_authority_owner"):
        errors.append("SOURCE_OWNER_EMPTY")
    if not receipt.get("does_not_prove"):
        errors.append("DOES_NOT_PROVE_EMPTY")

    # A no-reference original-design route must expose structural/package causality.
    if route == "STRUCTURE_TO_FORM":
        stages = set(receipt.get("required_stage_graph", []))
        for stage in ("S2_COMPONENT_GRAPH", "S3_INTERFACE_MOTION_GRAPH", "S4_PACKAGE_CLEARANCE", "S5_STRUCTURAL_TOPOLOGY"):
            if stage not in stages:
                errors.append(f"STRUCTURE_STAGE_MISSING:{stage}")

    # Reference route must not omit identity curves/sections before primary surface.
    if route == "REFERENCE_RECONSTRUCTION":
        stages = set(receipt.get("required_stage_graph", []))
        for stage in ("R3_IDENTITY_FEATURE_CURVES", "R4_SECTION_NETWORK"):
            if stage not in stages:
                errors.append(f"REFERENCE_STAGE_MISSING:{stage}")

    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("receipt", type=Path)
    ap.add_argument("--contract", type=Path, default=CONTRACT)
    args = ap.parse_args()
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    errors = validate_receipt(receipt, contract)
    out = {
        "schema": "oleander.3d.modeling-route-validation.v1",
        "receipt": str(args.receipt),
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "does_not_prove": ["design quality", "engineering release", "reference fidelity"]
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
