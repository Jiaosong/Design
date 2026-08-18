#!/usr/bin/env python3
from __future__ import annotations
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent.parent
VALIDATOR = SKILL / "tools" / "validate_effect_parameter_library.py"
PARAMS = SKILL / "references" / "VISUAL_EFFECT_PARAMETER_LIBRARY.json"
STATIC = SKILL / "recipes" / "SVG_PROCEDURAL_RECIPES.json"
MOTION = SKILL / "recipes" / "MOTION_HANDOFF_RECIPES.json"


def run(params, static=None, motion=None):
    static = static if static is not None else json.loads(STATIC.read_text(encoding="utf-8"))
    motion = motion if motion is not None else json.loads(MOTION.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        pp = td / "params.json"; sp = td / "static.json"; mp = td / "motion.json"
        pp.write_text(json.dumps(params, ensure_ascii=False, indent=2), encoding="utf-8")
        sp.write_text(json.dumps(static, ensure_ascii=False, indent=2), encoding="utf-8")
        mp.write_text(json.dumps(motion, ensure_ascii=False, indent=2), encoding="utf-8")
        cp = subprocess.run([sys.executable, str(VALIDATOR), str(pp), str(sp), str(mp)], capture_output=True, text=True)
        return cp.returncode, cp.stdout + cp.stderr


def expect_fail(name, params, static=None, motion=None, needle=None):
    rc, out = run(params, static, motion)
    if rc == 0:
        raise SystemExit(f"FAIL regression {name}: invalid library passed")
    if needle and needle not in out:
        raise SystemExit(f"FAIL regression {name}: expected {needle!r}; got {out!r}")
    print(f"PASS negative: {name}")


def main():
    params = json.loads(PARAMS.read_text(encoding="utf-8"))
    rc, out = run(params)
    if rc != 0:
        raise SystemExit(f"positive parameter library failed: {out}")
    print("PASS positive parameter library")

    d = copy.deepcopy(params)
    d["global_rules"]["semantic_owner_required"] = False
    expect_fail("semantic owner disabled", d, needle="semantic_owner_required")

    d = copy.deepcopy(params)
    d["global_rules"].pop("effect_off_rule")
    expect_fail("missing effect off rule", d, needle="effect_off_rule")

    d = copy.deepcopy(params)
    d["static_parameters"]["hatch"]["candidate_ranges"]["spacing_px"] = [24, 4]
    expect_fail("reversed hatch range", d, needle="reversed numeric range")

    d = copy.deepcopy(params)
    d["global_rules"]["required_review_scales"] = ["NEAR", "FAR"]
    expect_fail("missing MID review", d, needle="NEAR/MID/FAR")

    motion = json.loads(MOTION.read_text(encoding="utf-8"))
    bad_motion = copy.deepcopy(motion)
    bad_motion["recipes"][0]["reduced_motion"] = ""
    expect_fail("motion recipe without reduced motion", params, motion=bad_motion, needle="reduced_motion")

    static = json.loads(STATIC.read_text(encoding="utf-8"))
    bad_static = copy.deepcopy(static)
    bad_static["recipes"][0]["required_params"].remove("semantic_owner_id")
    expect_fail("static recipe without semantic owner", params, static=bad_static, needle="semantic_owner_id")

    print("PASS: effect parameter library regression suite")


if __name__ == "__main__":
    main()
