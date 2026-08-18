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
VALIDATOR = SKILL / "tools" / "validate_effect_recipe_register.py"
FIXTURE = HERE / "EFFECT-RECIPE-01_REGISTER.json"
STATIC = SKILL / "recipes" / "SVG_PROCEDURAL_RECIPES.json"
MOTION = SKILL / "recipes" / "MOTION_HANDOFF_RECIPES.json"


def run(data):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "register.json"
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        cp = subprocess.run([sys.executable, str(VALIDATOR), str(p), str(STATIC), str(MOTION)], capture_output=True, text=True)
        return cp.returncode, (cp.stdout + cp.stderr)


def mutate(base, instance_id):
    d = copy.deepcopy(base)
    return d, next(i for i in d["effect_instances"] if i["instance_id"] == instance_id)


def expect_fail(name, data, needle=None):
    rc, out = run(data)
    if rc == 0:
        raise SystemExit(f"FAIL regression {name}: invalid register passed")
    if needle and needle not in out:
        raise SystemExit(f"FAIL regression {name}: expected {needle!r} in output; got {out!r}")
    print(f"PASS negative: {name}")


def main():
    base = json.loads(FIXTURE.read_text(encoding="utf-8"))
    rc, out = run(base)
    if rc != 0:
        raise SystemExit(f"positive fixture failed: {out}")
    print("PASS positive fixture")

    d, i = mutate(base, "FX-01")
    i.pop("legend_id")
    expect_fail("analytical gradient without legend", d, "mapped_variable + legend_id")

    d, i = mutate(base, "FX-03")
    i["parameters"].pop("seed")
    expect_fail("stipple without deterministic seed", d, "missing")

    d, i = mutate(base, "FX-05")
    i["parameters"]["why"] = ""
    expect_fail("shadow without role explanation", d, "shadow must explain")

    d, i = mutate(base, "FX-06")
    i["surface_role"] = "PRESENTATIONAL_ATMOSPHERE"
    expect_fail("generic glow", d, "glow has no allowed semantic role")

    d, i = mutate(base, "FX-02")
    i["semantic_owner_id"] = ""
    expect_fail("effect without owner", d, "semantic_owner_id required")

    d, i = mutate(base, "MX-01")
    i["reduced_motion"] = ""
    expect_fail("motion without reduced alternative", d, "reduced_motion required")

    d, i = mutate(base, "MX-03")
    i["native_scroll_baseline"] = False
    expect_fail("scroll recipe without native baseline", d, "native_scroll_baseline")

    d, i = mutate(base, "MX-04")
    i["particle_count_model"] = ""
    expect_fail("particle field without count model", d, "particle_count_model")

    d = copy.deepcopy(base)
    d["producer_state"] = "KEEP"
    expect_fail("machine KEEP", d, "may not award")

    # Directly construct a displacement attack using an otherwise valid static shell.
    d, i = mutate(base, "FX-02")
    i["recipe_id"] = "SVG-R07-DISPLACEMENT"
    i["surface_role"] = "REFERENCE_FIDELITY"
    i["registration_class"] = "MAP_BOUND"
    i["parameters"] = {"scale_px": 6, "frequency": 0.04, "seed": 5}
    expect_fail("displacement on map-bound geometry", d, "may not distort map-bound")

    print("PASS: effect recipe regression suite")


if __name__ == "__main__":
    main()
