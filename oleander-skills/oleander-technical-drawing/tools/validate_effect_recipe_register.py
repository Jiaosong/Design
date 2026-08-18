#!/usr/bin/env python3
"""Validate OLEANDER Technical Drawing procedural effect + motion handoff registers.

Machine PASS proves schema / contradiction consistency only. It does not award
visual quality, material truth, accessibility, runtime performance or KEEP.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

NO_PROMOTION = {"NO", "NO_PROMOTION", "CANDIDATE_NOT_PROMOTED", "CANDIDATE / NO_PROMOTION"}
SURFACE_ROLES = {
    "ANALYTICAL_FIELD", "MATERIAL_SURFACE", "HIERARCHY_RECESSION",
    "PRESENTATIONAL_ATMOSPHERE", "REFERENCE_FIDELITY", "STATE_EMISSION"
}
FORBIDDEN_MACHINE_STATES = {"KEEP", "MAIN_KEEP", "DESIGN_PASS", "PROFESSIONAL_FINISH_PASS", "PROMOTED"}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot read JSON {path}: {exc}")


def require_keys(obj, keys, where):
    missing = [k for k in keys if k not in obj]
    if missing:
        fail(f"{where}: missing {missing}")


def validate_review(review, where):
    require_keys(review, ["near", "mid", "far"], where)
    for key in ("near", "mid", "far"):
        if review[key] not in {"PASS", "ISSUE_FOUND", "HOLD", "PENDING"}:
            fail(f"{where}: invalid {key} review state {review[key]}")


def validate_static(instance, recipe_ids):
    where = f"static {instance.get('instance_id','?')}"
    require_keys(instance, ["instance_id", "recipe_id", "semantic_owner_id", "surface_role", "parameters", "off_state", "review"], where)
    if instance["recipe_id"] not in recipe_ids:
        fail(f"{where}: unknown recipe_id {instance['recipe_id']}")
    if not instance["semantic_owner_id"]:
        fail(f"{where}: semantic_owner_id required")
    role = instance["surface_role"]
    if role not in SURFACE_ROLES:
        fail(f"{where}: invalid surface_role {role}")
    if not instance["off_state"]:
        fail(f"{where}: off_state required")
    validate_review(instance["review"], where)
    p = instance["parameters"]
    rid = instance["recipe_id"]
    if role == "ANALYTICAL_FIELD":
        require_keys(instance, ["mapped_variable", "legend_id"], where)
        if not instance.get("mapped_variable") or not instance.get("legend_id"):
            fail(f"{where}: analytical effect requires mapped_variable + legend_id")
    if rid in {"SVG-R01-LINEAR-FIELD", "SVG-R02-RADIAL-FIELD"}:
        require_keys(p, ["stops"], where)
        if len(p["stops"]) < 2:
            fail(f"{where}: gradient needs >=2 stops")
    if rid == "SVG-R03-HATCH":
        require_keys(p, ["angle_deg", "spacing_px", "stroke_px", "opacity"], where)
        if p["spacing_px"] <= 0 or p["stroke_px"] <= 0:
            fail(f"{where}: hatch spacing/stroke must be positive")
    if rid == "SVG-R04-STIPPLE":
        require_keys(p, ["density", "radius_px", "jitter", "seed"], where)
        if not (0 < p["density"] <= 1):
            fail(f"{where}: stipple density must be 0..1")
        if "seed" not in p:
            fail(f"{where}: deterministic seed required")
    if rid == "SVG-R05-GRAIN":
        require_keys(p, ["base_frequency", "num_octaves", "seed", "opacity"], where)
    if rid == "SVG-R06-SHADOW-DEPTH":
        require_keys(p, ["dx_px", "dy_px", "blur_px", "opacity", "why"], where)
        if not p.get("why"):
            fail(f"{where}: shadow must explain hierarchy/spatial role")
    if rid == "SVG-R07-DISPLACEMENT":
        require_keys(p, ["scale_px", "frequency", "seed"], where)
        if instance.get("registration_class") in {"MAP_BOUND", "SOURCE_AUTHORITY", "AUTHORITY"}:
            fail(f"{where}: displacement may not distort map-bound/authoritative geometry")
    if rid == "SVG-R08-GLOW-EMISSION":
        require_keys(p, ["blur_px", "opacity"], where)
        if role not in {"STATE_EMISSION", "MATERIAL_SURFACE", "REFERENCE_FIDELITY"}:
            fail(f"{where}: glow has no allowed semantic role")
        if role == "STATE_EMISSION" and not instance.get("state_binding"):
            fail(f"{where}: STATE_EMISSION glow requires state_binding")
    if rid == "SVG-R09-CONTOUR-BANDS":
        require_keys(p, ["levels", "interval_model", "stroke_px", "fill_opacity"], where)
        if not instance.get("source_binding"):
            fail(f"{where}: contour bands require source_binding")
    if rid == "SVG-R10-EDGE-MODULATION":
        if instance.get("registration_class") in {"MAP_BOUND", "SOURCE_AUTHORITY", "AUTHORITY"}:
            fail(f"{where}: edge modulation may not change authoritative geometry")


def validate_motion(instance, motion_ids):
    where = f"motion {instance.get('instance_id','?')}"
    require_keys(instance, ["instance_id", "recipe_id", "semantic_owner_id", "motion_role", "parameters", "reduced_motion", "runtime_state", "review"], where)
    if instance["recipe_id"] not in motion_ids:
        fail(f"{where}: unknown recipe_id {instance['recipe_id']}")
    if not instance["semantic_owner_id"]:
        fail(f"{where}: semantic_owner_id required")
    if not instance["reduced_motion"]:
        fail(f"{where}: reduced_motion required")
    if instance["runtime_state"] not in {"DESIGNED_NOT_RUN", "RUNTIME_REVIEWED", "PENDING_RUNTIME", "EXECUTED_SELF_CHECKED"}:
        fail(f"{where}: invalid runtime_state")
    validate_review(instance["review"], where)
    rid = instance["recipe_id"]
    p = instance["parameters"]
    if rid == "TD-MR01-PATH-TRACE":
        require_keys(instance, ["source_state", "direction_model", "interrupt_behavior"], where)
        require_keys(p, ["duration_ms", "easing"], where)
    if rid == "TD-MR04-SHARED-CONTAINER-HANDOFF":
        require_keys(instance, ["interrupt_behavior", "reverse_behavior"], where)
        require_keys(p, ["duration_ms", "easing"], where)
    if rid == "TD-MR07-SCROLL-PROGRESS":
        require_keys(instance, ["native_scroll_baseline"], where)
        if instance["native_scroll_baseline"] is not True:
            fail(f"{where}: native_scroll_baseline must remain available")
    if rid == "TD-MR09-PARALLAX-DEPTH":
        if instance.get("registration_class") == "MAP_BOUND":
            fail(f"{where}: parallax may not distort map-bound position")
    if rid == "TD-MR11-GRAIN-EVOLUTION" and instance.get("surface_role") not in {"MATERIAL_SURFACE", "REFERENCE_FIDELITY", "TIME_ATMOSPHERE"}:
        fail(f"{where}: moving grain requires material/reference/time atmosphere role")
    if rid == "TD-MR12-PARTICLE-FIELD":
        require_keys(instance, ["particle_count_model", "truth_state"], where)
        if not instance["particle_count_model"]:
            fail(f"{where}: particle_count_model required")


def main():
    if len(sys.argv) != 4:
        print("usage: validate_effect_recipe_register.py REGISTER STATIC_RECIPES MOTION_RECIPES")
        raise SystemExit(2)
    register_path, static_path, motion_path = map(Path, sys.argv[1:])
    reg = load(register_path)
    static_lib = load(static_path)
    motion_lib = load(motion_path)
    if reg.get("promotion") not in NO_PROMOTION:
        fail("register must remain non-promoted")
    state = reg.get("producer_state", "")
    if state in FORBIDDEN_MACHINE_STATES:
        fail(f"machine register may not award {state}")
    static_ids = {r["recipe_id"] for r in static_lib.get("recipes", [])}
    motion_ids = {r["recipe_id"] for r in motion_lib.get("recipes", [])}
    if not static_ids or not motion_ids:
        fail("recipe libraries must be non-empty")
    instances = reg.get("effect_instances")
    if not isinstance(instances, list) or not instances:
        fail("effect_instances required")
    seen = set()
    for inst in instances:
        iid = inst.get("instance_id")
        if iid in seen:
            fail(f"duplicate instance_id {iid}")
        seen.add(iid)
        kind = inst.get("kind")
        if kind == "STATIC_SVG":
            validate_static(inst, static_ids)
        elif kind == "MOTION_HANDOFF":
            validate_motion(inst, motion_ids)
        else:
            fail(f"{iid}: unknown kind {kind}")
    print(f"PASS: {len(instances)} effect instances; static recipes={len(static_ids)}; motion recipes={len(motion_ids)}; no design KEEP awarded")


if __name__ == "__main__":
    main()
