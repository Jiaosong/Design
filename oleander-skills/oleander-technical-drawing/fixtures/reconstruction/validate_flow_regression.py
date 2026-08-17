#!/usr/bin/env python3
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
VALIDATOR = ROOT / "oleander-skills" / "oleander-technical-drawing" / "tools" / "validate_flow_network.py"
SVG = HERE / "FLOW-01_NETWORK.svg"
REGISTER = HERE / "FLOW-01_NETWORK_REGISTER.json"


def run(register):
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "register.json"
        p.write_text(json.dumps(register, ensure_ascii=False, indent=2), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--svg", str(SVG), "--register", str(p)],
            text=True,
            capture_output=True,
        )


def expect_pass(register, label):
    result = run(register)
    if result.returncode != 0:
        raise AssertionError(f"{label} expected PASS but failed:\n{result.stdout}\n{result.stderr}")


def expect_fail(register, label, needle):
    result = run(register)
    if result.returncode == 0:
        raise AssertionError(f"{label} expected FAIL but passed")
    combined = result.stdout + result.stderr
    if needle not in combined:
        raise AssertionError(f"{label} failed for wrong reason; expected {needle!r}:\n{combined}")


def main():
    base = json.loads(REGISTER.read_text(encoding="utf-8"))
    expect_pass(base, "positive fixture")

    oversized = copy.deepcopy(base)
    oversized["direction_markers"][0]["marker_to_stroke_ratio"] = 12.0
    expect_fail(oversized, "oversized generic arrow", "marker/stroke ratio out of contract")

    wrong_tangent = copy.deepcopy(base)
    wrong_tangent["direction_markers"][1]["marker_angle_deg"] = 40.0
    expect_fail(wrong_tangent, "wrong route tangent", "not tangent to route")

    wrong_label = copy.deepcopy(base)
    wrong_label["route_labels"][0]["route_edge"] = "E-P02"
    expect_fail(wrong_label, "route label bound to wrong edge", "svg route binding mismatch")

    collapsed_class = copy.deepcopy(base)
    collapsed_class["route_classes"].pop("secondary")
    expect_fail(collapsed_class, "collapsed secondary route class", "missing route classes")

    missing_marker = copy.deepcopy(base)
    missing_marker["direction_markers"] = [m for m in missing_marker["direction_markers"] if m["route_edge"] != "E-S01"]
    expect_fail(missing_marker, "directed edge without direction evidence", "has no direction marker")

    print("OLEANDER FLOW REGRESSION: POSITIVE + NEGATIVE CONTRACT PASS")
    print("blocked=oversized-arrow,wrong-tangent,wrong-label-binding,collapsed-route-class,missing-direction-marker")
    print("NOTE: regression PASS does not equal visual/pixel fidelity, route truth, or Design KEEP.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
