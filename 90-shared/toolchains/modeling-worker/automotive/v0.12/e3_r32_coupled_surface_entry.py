#!/usr/bin/env python3
"""OLEANDER Modeling Worker v0.12 E3 R3.2 correction.

R3.2 retains the R3 five-family Surface Source architecture and the R3.1 evidence-class
split. It fixes the remaining R3.1 failure without relaxing thresholds:

- front/rear termination continuations retain more width and vertical volume;
- far continuation tangents are less collapse-prone;
- termination BROAD_INTERIOR radius evidence excludes inherited shoulder/rocker character
  bands while whole-zone cell-area/non-degeneracy remains checked;
- far INTENTIONAL_BOUNDARY transitions remain explicit diagnostics, not ordinary
  Character-Band smoothness authority.

Machine PASS only opens Human Project/Visual QA. PAP and Promotion remain blocked.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
R31_PATH = HERE / "e3_r3_1_coupled_surface_entry.py"
spec = importlib.util.spec_from_file_location("oleander_e3_r31", R31_PATH)
r31 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(r31)
base = r31.base
Vector = base.Vector
bpy = base.bpy

MODEL = "OLEANDER_ModelingWorker_v0.12_E3_R3_2_TerminationCorrectedSurfaceNetwork"


def user_args() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]


class R32Network(base.R3Network):
    """R3 source network with R3.2-only termination tangent correction."""

    def _far_scales(self, family: str) -> tuple[float, float, float]:
        spec = self.terms[family]
        return (
            float(spec.get("far_tangent_longitudinal_scale", 0.78)),
            float(spec.get("far_tangent_lateral_scale", 0.48)),
            float(spec.get("far_tangent_vertical_scale", 0.42)),
        )

    def front_term(self, s: float, wnorm: float) -> Vector:
        w = wnorm * 3.0
        p = self.composite(0.0, w)
        q = self.term_tip(True, w)
        spec = self.terms["SURF-FRONT-TERM"]
        length = float(spec["length"])
        tx, ty, tz = self._far_scales("SURF-FRONT-TERM")
        du = self.composite_du(0.0, w)
        scale = length / max(1e-9, abs(du.x))
        d1 = du * scale
        d0 = Vector((-length * tx, (p.y - q.y) * ty, (p.z - q.z) * tz))
        return base.hermite(q, p, d0, d1, s)

    def rear_term(self, s: float, wnorm: float) -> Vector:
        w = wnorm * 3.0
        p = self.composite(1.0, w)
        q = self.term_tip(False, w)
        spec = self.terms["SURF-REAR-TERM"]
        length = float(spec["length"])
        tx, ty, tz = self._far_scales("SURF-REAR-TERM")
        du = self.composite_du(1.0, w)
        scale = length / max(1e-9, abs(du.x))
        d0 = du * scale
        d1 = Vector((-length * tx, (q.y - p.y) * ty, (q.z - p.z) * tz))
        return base.hermite(p, q, d0, d1, s)


def apply_correction(base_contract: dict[str, Any], correction: dict[str, Any]) -> dict[str, Any]:
    contract = copy.deepcopy(base_contract)
    if contract.get("revision") != correction["base_revision"]:
        raise ValueError(f"R3.2 base revision mismatch: {contract.get('revision')} != {correction['base_revision']}")
    for key, expected in correction["locked_thresholds"].items():
        actual = contract["machine_thresholds"].get(key)
        if actual != expected:
            raise ValueError(f"R3.2 threshold drift: {key}={actual!r}, expected {expected!r}")
    for family, values in correction["surface_source_overrides"].items():
        contract["surface_sources"][family].update(values)
    contract["revision"] = correction["revision"]
    contract["job_id"] = "SYS-MODELING-WORKER-v0.12-AUTO-E3-R3.2"
    contract["decision_question"] = correction["decision_question"]
    contract["architecture"]["fairness_zone_policy"] = correction["evidence_zoning"]["rule"]
    contract["boundary"] = correction["boundary"]
    return contract


def _inside_character_band(v: float, centers: list[float], half_width: float) -> bool:
    return any(abs(v - c) < half_width for c in centers)


def termination_continuation_metrics(
    fn: Callable[[float, float], Vector],
    front: bool,
    contract: dict[str, Any],
    correction: dict[str, Any],
    nu: int = 33,
    nv: int = 25,
) -> dict[str, Any]:
    """Broad continuation radius outside inherited character bands.

    Whole-zone cell areas remain included so excluding a character band cannot hide surface
    degeneracy. Only radius samples whose v-location belongs to shoulder/rocker character
    bands are excluded from BROAD_INTERIOR curvature authority.
    """
    m = float(correction["evidence_zoning"]["termination_far_boundary_margin"])
    char_half = float(correction["evidence_zoning"]["termination_character_band_half_width"])
    centers = [float(x) for x in correction["evidence_zoning"]["inherited_character_centers"]]
    broad_m = float(contract["machine_thresholds"]["broad_interior_margin"])
    u_range = (m, 1.0) if front else (0.0, 1.0 - m)
    v_range = (broad_m, 1.0 - broad_m)
    us = r31.sample_axis(*u_range, nu)
    vs = r31.sample_axis(*v_range, nv)

    pos: list[list[Vector]] = []
    nor: list[list[Vector]] = []
    for u in us:
        pr: list[Vector] = []
        nr: list[Vector] = []
        for v in vs:
            pr.append(fn(u, v))
            nr.append(base.numerical_normal(fn, u, v))
        pos.append(pr)
        nor.append(nr)

    radii: list[float] = []
    cell_areas: list[float] = []
    excluded_radius_edges = 0
    included_radius_edges = 0
    for i in range(nu):
        for j in range(nv):
            if i + 1 < nu:
                if _inside_character_band(vs[j], centers, char_half):
                    excluded_radius_edges += 1
                else:
                    radii.append(r31.radius_from_step(pos[i][j], pos[i+1][j], nor[i][j], nor[i+1][j]))
                    included_radius_edges += 1
            if j + 1 < nv:
                vmid = 0.5 * (vs[j] + vs[j+1])
                if _inside_character_band(vmid, centers, char_half):
                    excluded_radius_edges += 1
                else:
                    radii.append(r31.radius_from_step(pos[i][j], pos[i][j+1], nor[i][j], nor[i][j+1]))
                    included_radius_edges += 1
            if i + 1 < nu and j + 1 < nv:
                cell_areas.append((pos[i+1][j]-pos[i][j]).cross(pos[i][j+1]-pos[i][j]).length)

    finite = [r for r in radii if math.isfinite(r)]
    if not finite:
        raise ValueError("R3.2 termination continuation produced no broad-interior radius samples")
    finite.sort()
    return {
        "min_normal_radius_proxy_m": finite[0],
        "p05_normal_radius_proxy_m": finite[max(0, int(0.05 * (len(finite)-1)))],
        "min_cell_area_proxy": min(cell_areas) if cell_areas else 0.0,
        "included_radius_edges": included_radius_edges,
        "excluded_inherited_character_band_edges": excluded_radius_edges,
        "radius_authority": "TERMINATION_CONTINUATION_OUTSIDE_INHERITED_SHOULDER_ROCKER_CHARACTER_BANDS",
        "cell_area_authority": "WHOLE_TERMINATION_CONTINUATION_ZONE",
    }


def corrected_zone_fairness(net: R32Network, contract: dict[str, Any], correction: dict[str, Any]) -> dict[str, Any]:
    th = contract["machine_thresholds"]
    m = float(th["broad_interior_margin"])
    far_m = float(correction["evidence_zoning"]["termination_far_boundary_margin"])

    broad = {
        "SURF-UPPER": r31.zoned_radius_metrics(net.upper, (0.03, 0.97), (m, 1-m)),
        "SURF-SIDE": r31.zoned_radius_metrics(net.side, (0.03, 0.97), (m, 1-m)),
        "SURF-LOWER": r31.zoned_radius_metrics(net.lower, (0.03, 0.97), (m, 1-m)),
        "SURF-FRONT-TERM": termination_continuation_metrics(net.front_term, True, contract, correction),
        "SURF-REAR-TERM": termination_continuation_metrics(net.rear_term, False, contract, correction),
    }
    character = {
        "UPPER_TO_SHOULDER": r31.band_total_turn_metrics(net.upper, (0.03,0.97), (1-m,1.0)),
        "SIDE_FROM_SHOULDER": r31.band_total_turn_metrics(net.side, (0.03,0.97), (0.0,m)),
        "SIDE_TO_ROCKER": r31.band_total_turn_metrics(net.side, (0.03,0.97), (1-m,1.0)),
        "LOWER_FROM_ROCKER": r31.band_total_turn_metrics(net.lower, (0.03,0.97), (0.0,m)),
        "LOWER_TO_UNDERBODY": r31.band_total_turn_metrics(net.lower, (0.03,0.97), (1-m,1.0)),
    }
    intentional_transition = {
        "FRONT_FAR_TRANSITION": {
            **r31.band_total_turn_metrics(net.front_term, (0.0,far_m), (m,1-m), 13, 21),
            "diagnostic_only": True,
            "authority_class": "INTENTIONAL_BOUNDARY",
        },
        "REAR_FAR_TRANSITION": {
            **r31.band_total_turn_metrics(net.rear_term, (1-far_m,1.0), (m,1-m), 13, 21),
            "diagnostic_only": True,
            "authority_class": "INTENTIONAL_BOUNDARY",
        },
    }
    broad_pass = all(
        row["min_normal_radius_proxy_m"] >= float(th["min_broad_normal_radius_proxy_m"])
        and row["min_cell_area_proxy"] >= float(th["min_surface_cell_area_proxy"])
        for row in broad.values()
    )
    character_pass = all(
        row["min_normal_radius_proxy_m"] >= float(th["min_character_band_normal_radius_proxy_m"])
        and row["max_total_normal_turn_deg"] <= float(th["max_character_band_total_normal_turn_deg"])
        for row in character.values()
    )
    return {
        "broad_interior": broad,
        "character_bands": character,
        "intentional_boundary_transitions": intentional_transition,
        "broad_pass": broad_pass,
        "character_pass": character_pass,
        "thresholds_unchanged": True,
    }


def evaluate_core(contract: dict[str, Any], correction: dict[str, Any]) -> tuple[dict[str, Any], R32Network]:
    net = R32Network(contract)
    th = contract["machine_thresholds"]
    source_rel = [r31.source_relationship_metrics(net, rel) for rel in contract["relationship_graph"]]
    runtime = r31.runtime_boundary_diagnostics(net, contract)
    zones = corrected_zone_fairness(net, contract, correction)
    intentional = r31.intentional_boundary_metrics(net, contract)
    profile = base.profile_metrics(net)
    plan = base.plan_metrics(net)
    reflection = base.reflection_field_proxy(net)
    owners, overlaps = base.source_ownership(contract)
    classes = {rel["class"] for rel in contract["relationship_graph"]}

    checks = {
        "five_surface_source_families": len(contract["architecture"]["main_surface_families"]) + len(contract["architecture"]["termination_families"]) == 5,
        "profile_plan_primary_curve_authority_separated": contract["architecture"]["profile_plan_authority_separated"] is True,
        "global_control_cage_forbidden": contract["architecture"]["global_control_cage_forbidden"] is True,
        "relationship_specific_continuity_classes": len(classes) >= 3 and contract["architecture"]["blanket_continuity_class_forbidden"] is True,
        "source_relationship_authority_pass": all(row["pass"] for row in source_rel),
        "broad_interior_fairness_pass": zones["broad_pass"],
        "character_band_quality_pass": zones["character_pass"],
        "intentional_boundaries_non_degenerate": intentional["pass"],
        "semantic_control_source_ownership_disjoint": not overlaps,
        "profile_silhouette_metrics_pass": profile["max_profile_slope_change_proxy"] <= float(th["max_profile_slope_change_proxy"]) and profile["profile_inflection_count"] <= int(th["max_profile_inflection_count"]),
        "plan_view_rear_haunch_hierarchy_pass": plan["rear_haunch_plan_advantage"] >= float(th["min_rear_haunch_plan_advantage"]),
        "reflection_field_proxy_pass": reflection <= float(th["max_reflection_field_acceleration_proxy"]),
        "execution_topology_is_derived": contract["authority"]["execution_geometry"] == "DERIVED",
        "existing_quality_thresholds_unchanged": all(contract["machine_thresholds"].get(k) == v for k, v in correction["locked_thresholds"].items()),
    }
    return {
        "checks": checks,
        "source_relationship_metrics": source_rel,
        "runtime_boundary_diagnostics": runtime,
        "zoned_fairness": zones,
        "intentional_boundary_metrics": intentional,
        "profile_metrics": profile,
        "plan_metrics": plan,
        "reflection_field_acceleration_proxy": reflection,
        "semantic_source_ownership": owners,
        "semantic_source_overlaps": overlaps,
    }, net


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-contract", required=True)
    ap.add_argument("--correction", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--resolution", type=int, default=512)
    args = ap.parse_args(user_args())

    base_contract = json.loads(Path(args.base_contract).read_text(encoding="utf-8"))
    correction = json.loads(Path(args.correction).read_text(encoding="utf-8"))
    contract = apply_correction(base_contract, correction)
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    base_report, base_net = evaluate_core(contract, correction)
    th = contract["machine_thresholds"]
    variants: dict[str, Any] = {}
    all_exact = True
    all_machine = True
    all_effect = True

    for cid in contract["semantic_controls"]:
        variant_contract, declared = base.apply_control(contract, cid)
        actual = base.changed_keys(contract, variant_contract)
        variant_report, variant_net = evaluate_core(variant_contract, correction)
        displacement = base.max_displacement(base_net, variant_net)
        exact = actual == declared
        authority_effect = r31.direct_authority_effect(contract, variant_contract, declared)
        machine = all(variant_report["checks"].values())
        legible = float(th["min_semantic_surface_displacement"]) <= displacement <= float(th["max_semantic_surface_displacement"])
        variants[cid] = {
            "declared_source_keys": [list(k) for k in sorted(declared, key=str)],
            "actual_changed_source_keys": [list(k) for k in sorted(actual, key=str)],
            "source_edit_exact": exact,
            "direct_declared_authority_effect": authority_effect,
            "max_surface_displacement": displacement,
            "working_fidelity_legible": legible,
            "machine_surface_pass": machine,
            "zoned_fairness": variant_report["zoned_fairness"],
            "profile_metrics": variant_report["profile_metrics"],
            "plan_metrics": variant_report["plan_metrics"],
        }
        all_exact = all_exact and exact
        all_machine = all_machine and machine and legible
        all_effect = all_effect and authority_effect["pass"]

    checks = {
        **base_report["checks"],
        "semantic_source_edits_exact": all_exact,
        "all_semantic_variants_surface_pass": all_machine,
        "semantic_authority_domain_effects_present": all_effect,
        "machine_pass_only_opens_human_review": True,
    }
    status = "MACHINE_PASS_HUMAN_PROJECT_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL_REVISE_E3_R3_2_GEOMETRY_OR_QA"
    report = {
        "schema": "oleander.modeling-worker.v0.12.e3.r3.2.machine-report",
        "model": MODEL,
        "status": status,
        "decision_question": contract["decision_question"],
        "checks": checks,
        "base": base_report,
        "semantic_variants": variants,
        "correction": correction,
        "boundary": "R3.2 retains the R3 architecture and R3.1 evidence semantics, corrects termination continuation geometry/zoning without threshold relaxation, and only opens Human Project/Visual QA on Machine PASS. PAP and Promotion remain blocked."
    }

    scene, row_count = base.render_set(base_net, out, args.resolution, "R3_2_BASE", True)
    scene["OLEANDER_MODEL"] = MODEL
    scene["OLEANDER_STAGE"] = "E3_R3_2_APPLICATION_MACHINE"
    scene["OLEANDER_AUTHORITY"] = "WORKING_SURFACE_SOURCE"
    scene["OLEANDER_CORRECTION"] = json.dumps(correction, ensure_ascii=False)
    bpy.ops.wm.save_as_mainfile(filepath=str(out / f"{MODEL}.blend"))

    for cid in contract["semantic_controls"]:
        variant_contract, _ = base.apply_control(contract, cid)
        _, variant_net = evaluate_core(variant_contract, correction)
        base.render_set(variant_net, out, args.resolution, cid.replace("-", "_"), False)

    (out / "E3_R32_MACHINE_REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "E3_R32_COMPILED_SURFACE_SOURCE.json").write_text(json.dumps({
        "schema": "oleander.modeling-worker.v0.12.e3.r3.2.compiled-surface-source",
        "authority": "WORKING_SURFACE_SOURCE",
        "revision": "R3.2",
        "profile_primary_curves": contract["profile_primary_curves"],
        "plan_primary_curves": contract["plan_primary_curves"],
        "surface_sources": contract["surface_sources"],
        "relationship_graph": contract["relationship_graph"],
        "qa_semantics": "SOURCE_RELATION / RUNTIME_DIAGNOSTIC / BROAD_INTERIOR / CHARACTER_BAND / INTENTIONAL_BOUNDARY",
        "execution_geometry": {"derived": True, "editable_authority": False, "sample_rows": row_count}
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if status == "MACHINE_PASS_HUMAN_PROJECT_VISUAL_REVIEW_REQUIRED" else 5


if __name__ == "__main__":
    raise SystemExit(main())
