#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path


def fail(msg):
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def check_range(value, where):
    if isinstance(value, list) and len(value) == 2 and all(isinstance(v, (int, float)) for v in value):
        if value[0] > value[1]:
            fail(f"{where}: reversed numeric range {value}")


def walk_ranges(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            here = f"{prefix}.{k}" if prefix else k
            if "range" in k or k in {"opacity", "blur_px", "spacing_px", "stroke_px", "duration_ms", "stagger_ms_per_item", "relative_displacement", "phase_rate_hz", "amplitude"}:
                check_range(v, here)
            walk_ranges(v, here)
    elif isinstance(obj, list):
        for idx, v in enumerate(obj):
            walk_ranges(v, f"{prefix}[{idx}]")


def main():
    if len(sys.argv) != 4:
        print("usage: validate_effect_parameter_library.py PARAMS STATIC_RECIPES MOTION_RECIPES")
        raise SystemExit(2)
    params, static, motion = map(load, sys.argv[1:])
    if params.get("status") not in {"CANDIDATE / NO_PROMOTION", "NO_PROMOTION"}:
        fail("parameter library must remain non-promoted")
    rules = params.get("global_rules", {})
    for key in ["effect_off_rule", "semantic_owner_required", "reduced_motion_required", "required_review_scales"]:
        if key not in rules:
            fail(f"global_rules missing {key}")
    if rules["semantic_owner_required"] is not True:
        fail("semantic_owner_required must be true")
    if rules["reduced_motion_required"] is not True:
        fail("reduced_motion_required must be true")
    scales = rules["required_review_scales"]
    if not all(s in scales for s in ["NEAR", "MID", "FAR"]):
        fail("required review scales must include NEAR/MID/FAR")
    if not params.get("static_parameters") or not params.get("motion_parameters"):
        fail("static_parameters and motion_parameters required")
    walk_ranges(params)

    static_recipes = static.get("recipes", [])
    motion_recipes = motion.get("recipes", [])
    if len(static_recipes) < 8:
        fail("static recipe library unexpectedly small")
    if len(motion_recipes) < 10:
        fail("motion recipe library unexpectedly small")
    ids = [r.get("recipe_id") for r in static_recipes + motion_recipes]
    if None in ids or len(ids) != len(set(ids)):
        fail("recipe ids must be present and unique")
    for r in static_recipes:
        for key in ["recipe_id", "roles", "mechanism", "required_params", "off_state", "failure_triggers"]:
            if key not in r:
                fail(f"{r.get('recipe_id')}: missing {key}")
        if "semantic_owner_id" not in r["required_params"]:
            fail(f"{r['recipe_id']}: semantic_owner_id must be required")
    for r in motion_recipes:
        for key in ["recipe_id", "motion_atlas_effect", "motion_role", "allowed_carriers", "required", "reduced_motion", "fail_if"]:
            if key not in r:
                fail(f"{r.get('recipe_id')}: missing {key}")
        if "semantic_owner_id" not in r["required"]:
            fail(f"{r['recipe_id']}: semantic_owner_id must be required")
        if not r.get("reduced_motion"):
            fail(f"{r['recipe_id']}: reduced_motion must be explicit")
    print(f"PASS: parameter library + {len(static_recipes)} static recipes + {len(motion_recipes)} motion recipes structurally valid; no aesthetic PASS awarded")


if __name__ == "__main__":
    main()
