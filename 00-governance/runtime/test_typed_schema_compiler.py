#!/usr/bin/env python3
from __future__ import annotations

from compile_typed_schema import compile_package


def main() -> None:
    package = compile_package()
    enums = package["enums"]

    expected = {
        "OBJECT_PLANE": {"KNOWLEDGE", "PROJECT", "RUNTIME_CONTROL"},
        "NEED_ORIGIN_KIND": {"STAKEHOLDER_STATED", "USER_OBSERVED_OR_RESEARCHED", "OPERATIONAL_SOURCE", "EXTERNAL_MANDATE_DERIVED", "PROJECT_HYPOTHESIS", "DESIGN_RESEARCH_HYPOTHESIS", "OTHER_EXPLICIT"},
        "NEED_ORIGIN_VALIDATION_STATE": {"UNVALIDATED", "PARTIALLY_VALIDATED", "AGREED_FOR_SCOPE", "REFUTED", "SUPERSEDED"},
        "INTERFACE_MATURITY": {"IDENTIFIED", "DEFINED", "COORDINATED", "EXERCISED", "VERIFIED"},
        "CONTROLLED_IDENTITY_SCOPE": {"ECONOMIC_ACCOUNT", "PRESENTED_CREDENTIAL", "USER_DEVICE", "SERVICE_SESSION", "JOURNEY", "CUSTOMER_ACCOUNT", "OTHER_CONTROLLED"},
        "CONTROLLED_IDENTITY_EQUIVALENCE_POLICY": {"EXACT_SAME_PRESENTATION", "AUTHORIZED_EQUIVALENT", "LINKED_BY_REFERENCE", "NOT_EQUIVALENT", "UNKNOWN"},
        "ASSURANCE_TYPE": {"VERIFICATION", "VALIDATION", "CERTIFICATION", "INDEPENDENT_REVIEW", "AUDIT", "ACCEPTANCE"},
        "QUERY_PLANE": {"KNOWLEDGE_QUERY", "PROJECT_QUERY", "RUNTIME_CONTROL_QUERY", "PRESENTATION_QUERY", "HISTORY_QUERY"},
        "READBACK_LEVEL": {"RB0", "RB1", "RB2", "RB3", "RB4"},
    }

    for symbol, values in expected.items():
        if symbol not in enums:
            raise SystemExit(f"typed-schema self-test failed: missing enum {symbol}")
        actual = set(enums[symbol]["values"])
        if actual != values:
            raise SystemExit(
                f"typed-schema self-test failed: {symbol} expected={sorted(values)} actual={sorted(actual)}"
            )

    claim_map = package["compatibility_mappings"]["PROJECT_CLASS_CLAIM"]
    if claim_map.get("legacy") != "CLAIM" or claim_map.get("canonical") != "PROJECT_CLAIM":
        raise SystemExit("typed-schema self-test failed: CLAIM compatibility mapping")

    stale = package["compatibility_mappings"]["STALE_STATE"]
    if stale.get("migration") != "CONTEXTUAL_NOT_ONE_TO_ONE":
        raise SystemExit("typed-schema self-test failed: STALE mapping must remain contextual")

    print(
        "typed-schema compiler self-test PASS: "
        f"enums={package['enum_count']} aliases={len(package['compatibility_mappings'])}"
    )


if __name__ == "__main__":
    main()
