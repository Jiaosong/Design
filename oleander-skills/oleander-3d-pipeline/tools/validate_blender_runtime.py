from __future__ import annotations

import json
import sys
from pathlib import Path


def fail(code: str) -> None:
    raise SystemExit(code)


def _require_keys(obj: dict, keys: list[str], code: str) -> None:
    missing = [k for k in keys if k not in obj]
    if missing:
        fail(f"{code}:{','.join(missing)}")


def validate(receipt: dict, contract: dict) -> bool:
    if receipt.get("schema") != contract.get("receipt_schema"):
        fail("FAIL_SCHEMA")

    _require_keys(receipt, contract["required_top_level"], "FAIL_REQUIRED_TOP_LEVEL")

    if receipt["source_state_class"] not in contract["allowed_source_state_classes"]:
        fail("FAIL_SOURCE_STATE_CLASS")

    runtime = receipt["runtime"]
    _require_keys(runtime, contract["required_runtime_fields"], "FAIL_RUNTIME_FIELDS")
    if runtime.get("application") != "Blender":
        fail("FAIL_APPLICATION_NOT_BLENDER")
    if runtime.get("runtime_support_state") not in contract["allowed_runtime_support_states"]:
        fail("FAIL_RUNTIME_SUPPORT_STATE")

    deps = receipt["dependencies"]
    _require_keys(deps, contract["required_dependency_fields"], "FAIL_DEPENDENCY_FIELDS")
    if deps.get("network_only_required_dependency") is True:
        fail("FAIL_NETWORK_ONLY_REQUIRED_DEPENDENCY")
    if deps.get("all_required_dependencies_recoverable") is not True:
        fail("FAIL_REQUIRED_DEPENDENCY_NOT_RECOVERABLE")
    if deps.get("remote_asset_library_used") is True and not deps.get("materialized_remote_asset_ids"):
        fail("FAIL_REMOTE_ASSET_NOT_MATERIALIZED")

    proc = receipt["procedural"]
    _require_keys(proc, contract["required_procedural_fields"], "FAIL_PROCEDURAL_FIELDS")
    if proc.get("physical_truth_claim") is True and proc.get("simulation_used") is True:
        fail("FAIL_VISUAL_SIMULATION_PROMOTED_TO_PHYSICAL_TRUTH")
    if proc.get("geometry_nodes_used") is True and not proc.get("evaluated_carrier_readback"):
        fail("FAIL_EVALUATED_CARRIER_NOT_READBACK")
    if proc.get("simulation_used") is True and not proc.get("simulation_cache_or_state_or_na"):
        fail("FAIL_SIMULATION_STATE_UNBOUND")

    color = receipt["color_management"]
    _require_keys(color, contract["required_color_fields"], "FAIL_COLOR_FIELDS")
    for key in contract["required_color_fields"]:
        if color.get(key) in (None, ""):
            fail(f"FAIL_COLOR_FIELD_EMPTY:{key}")

    render = receipt["render"]
    _require_keys(render, contract["required_render_fields"], "FAIL_RENDER_FIELDS")

    io = receipt["io"]
    _require_keys(io, contract["required_io_fields"], "FAIL_IO_FIELDS")
    requested = set(io.get("requested_formats") or [])
    verified = set(io.get("verified_operators_or_bridges") or [])
    unresolved = sorted(requested - verified)
    if unresolved:
        fail(f"FAIL_IO_ROUTE_UNVERIFIED:{','.join(unresolved)}")
    if io.get("roundtrip_status") not in contract["allowed_roundtrip_status"]:
        fail("FAIL_ROUNDTRIP_STATUS")
    if io.get("representative_roundtrip_required") is True and io.get("roundtrip_status") != "PASS":
        fail("FAIL_REQUIRED_ROUNDTRIP_NOT_PASS")

    output = receipt["output"]
    if output.get("readback_status") != "PASS":
        fail("FAIL_OUTPUT_NOT_READBACK")
    if not output.get("retained_files"):
        fail("FAIL_NO_RETAINED_OUTPUT")

    if receipt.get("machine_verdict") == "PASS" and runtime.get("runtime_support_state") == "UNKNOWN":
        fail("FAIL_MACHINE_PASS_WITH_UNKNOWN_RUNTIME")

    if not isinstance(receipt.get("does_not_prove"), list) or not receipt["does_not_prove"]:
        fail("FAIL_DOES_NOT_PROVE_MISSING")

    return True


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: validate_blender_runtime.py RECEIPT.json CONTRACT.json", file=sys.stderr)
        return 2
    receipt = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    contract = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    try:
        validate(receipt, contract)
    except SystemExit as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("PASS_BLENDER_RUNTIME_CONTRACT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
