"""Professional-parity promotion guard for OLEANDER Blender Runtime.

This guard is intentionally independent from runtime layer count. A runtime may
have many validated internal layers and still be ineligible to become the
OLEANDER default modeling environment until the professional workflow gates in
PROFESSIONAL_PARITY_GATE.md are actually passed.
"""

from __future__ import annotations

import json
from pathlib import Path


PIPELINE_ROOT = Path(__file__).resolve().parents[2]
STATUS_PATH = PIPELINE_ROOT / "PROFESSIONAL_PARITY_STATUS.json"
GATE_PATH = PIPELINE_ROOT / "PROFESSIONAL_PARITY_GATE.md"


def fail(message: str) -> None:
    raise SystemExit(f"PROFESSIONAL_PARITY_STATIC_FAIL: {message}")


def main() -> None:
    if not STATUS_PATH.exists():
        fail("missing PROFESSIONAL_PARITY_STATUS.json")
    if not GATE_PATH.exists():
        fail("missing PROFESSIONAL_PARITY_GATE.md")

    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    gate_text = GATE_PATH.read_text(encoding="utf-8")

    if status.get("schema") != "OLEANDER_BLENDER_PROFESSIONAL_PARITY_STATUS_v0.1":
        fail("unexpected parity status schema")
    if status.get("runtime_id") != "oleander-blender-runtime":
        fail("runtime id mismatch")

    p0 = status.get("p0") or {}
    expected_p0 = {
        "P0_A_PARAMETRIC_CAD",
        "P0_B_DIRECT_BREP",
        "P0_C_NURBS_CLASS_A",
        "P0_D_PROCEDURAL",
        "P0_E_BIM_IFC",
        "P0_F_TECHNICAL_DRAWING",
        "P0_G_MODELING_INTERACTION",
        "P0_H_ASSEMBLY_CONFIGURATION",
        "P0_I_PRODUCT_VISUALIZATION",
    }
    if set(p0) != expected_p0:
        fail(f"P0 gate set mismatch: expected {sorted(expected_p0)}, got {sorted(p0)}")

    allowed = set(status.get("allowed_states") or [])
    if allowed != {"BLOCKED", "PARTIAL", "PASS"}:
        fail("allowed P0 states must be exactly BLOCKED/PARTIAL/PASS")

    bad_states = {
        key: value.get("state")
        for key, value in p0.items()
        if value.get("state") not in allowed
    }
    if bad_states:
        fail(f"invalid P0 states: {bad_states}")

    all_p0_pass = all(item.get("state") == "PASS" for item in p0.values())
    eligible = bool(status.get("default_environment_eligible"))
    promotion_state = status.get("default_promotion_state")

    if eligible and not all_p0_pass:
        fail("default_environment_eligible=true while one or more P0 gates are not PASS")
    if not all_p0_pass:
        if promotion_state != "BLOCKED_UNTIL_PROFESSIONAL_PARITY":
            fail("promotion state must remain BLOCKED while P0 gates are incomplete")
        if eligible:
            fail("default promotion must remain ineligible while P0 gates are incomplete")

    if "Default-promotion state: **BLOCKED**" not in gate_text:
        fail("parity gate document does not visibly declare default promotion BLOCKED")
    if "Until then the runtime status must remain **CANDIDATE / NOT DEFAULT**." not in gate_text:
        fail("parity gate document lost the CANDIDATE / NOT DEFAULT boundary")

    dependency_states = set(status.get("dependency_states") or [])
    required_dependency_states = {
        "DISCOVERED_NOT_PROBED",
        "RUNTIME_PROBED",
        "ADAPTER_IMPLEMENTED_UNVERIFIED",
        "VALIDATED_FOR_BOUNDED_SCOPE",
        "REJECTED_WITH_REASON",
    }
    if dependency_states != required_dependency_states:
        fail("dependency lifecycle states drifted")

    candidates = status.get("reuse_candidates") or {}
    if not candidates:
        fail("reuse-first candidate registry is empty")
    for name, candidate in candidates.items():
        state = candidate.get("state")
        if state not in dependency_states:
            fail(f"invalid dependency state for {name}: {state}")
        if not candidate.get("source"):
            fail(f"missing source provenance for dependency candidate {name}")
        if state == "VALIDATED_FOR_BOUNDED_SCOPE" and not candidate.get("validation_receipt"):
            fail(f"validated dependency candidate {name} lacks validation_receipt")

    print(json.dumps({
        "status": "PASS",
        "default_environment_eligible": eligible,
        "default_promotion_state": promotion_state,
        "p0_pass_count": sum(1 for item in p0.values() if item.get("state") == "PASS"),
        "p0_total": len(p0),
        "note": "Professional parity guard is independent of runtime layer count; incomplete P0 gates keep OLEANDER Blender CANDIDATE / NOT DEFAULT.",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
