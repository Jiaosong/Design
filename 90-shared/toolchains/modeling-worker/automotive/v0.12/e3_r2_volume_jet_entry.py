#!/usr/bin/env python3
"""OLEANDER Modeling Worker v0.12 E3 R2 — independent Automotive volume-jet Surface Source.

R1 failed Human Project/Visual QA because seven semantic volume names were projected onto
one 4x4 center cage. R2 changes only the application Surface Source architecture.

The authoritative source is a sequence of low-frequency semantic stations. Each station
owns transverse position, first-derivative and second-derivative jets. Adjacent quintic
Bezier surface segments are compiled from the same shared station jets, so parametric C2
continuity is established by construction while hood/cowl, cabin, rear-haunch and the two
terminations retain independent source controls. Shoulder and lower-body controls occupy
separate transverse roles within those stations.

Execution topology is sampled only after the analytic patch chain is compiled. Machine
PASS opens Human Project/Visual QA only; it does not establish Automotive design authority,
Class-A, PAP or system Promotion.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import math
import sys
from math import comb
from pathlib import Path
from typing import Any, Iterable

HERE = Path(__file__).resolve().parent
GENERIC_E2 = HERE.parents[1] / "v0.12" / "e2_multipatch_network.py"
_spec = importlib.util.spec_from_file_location("oleander_v012_e2", GENERIC_E2)
e2 = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(e2)
Vector = e2.Vector
bpy = e2.bpy

MODEL = "OLEANDER_ModelingWorker_v0.12_E3_R2_VolumeJetArchitecture"
RUNTIME_SECOND_DERIVATIVE_TOL = 5e-6


def user_args() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]


def bernstein(n: int, t: float) -> list[float]:
    s = 1.0 - t
    return [comb(n, i) * (t ** i) * (s ** (n - i)) for i in range(n + 1)]


def bernstein_d1(n: int, t: float) -> list[float]:
    low = bernstein(n - 1, t)
    out = []
    for i in range(n + 1):
        a = low[i - 1] if 0 <= i - 1 < len(low) else 0.0
        b = low[i] if i < len(low) else 0.0
        out.append(n * (a - b))
    return out


def bernstein_d2(n: int, t: float) -> list[float]:
    low = bernstein(n - 2, t)
    out = []
    for i in range(n + 1):
        a = low[i - 2] if 0 <= i - 2 < len(low) else 0.0
        b = low[i - 1] if 0 <= i - 1 < len(low) else 0.0
        c = low[i] if i < len(low) else 0.0
        out.append(n * (n - 1) * (a - 2.0 * b + c))
    return out


def p_add(a: Iterable[float], b: Iterable[float]) -> list[float]:
    aa, bb = tuple(a), tuple(b)
    return [aa[k] + bb[k] for k in range(3)]


def p_sub(a: Iterable[float], b: Iterable[float]) -> list[float]:
    aa, bb = tuple(a), tuple(b)
    return [aa[k] - bb[k] for k in range(3)]


def p_scale(a: Iterable[float], s: float) -> list[float]:
    aa = tuple(a)
    return [aa[k] * s for k in range(3)]


def station_map(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {s["id"]: s for s in contract["stations"]}


def compile_segment(a: dict[str, Any], b: dict[str, Any]) -> list[list[list[float]]]:
    """Compile one degree-5 longitudinal x degree-4 transverse Bezier patch.

    Endpoint position / first derivative / second derivative are exactly satisfied:
      P0 = A
      P1 = A + A'/5
      P2 = A''/20 + 2P1 - P0
      P5 = B
      P4 = B - B'/5
      P3 = B''/20 + 2P4 - P5
    Adjacent segments consume the same station jets, so their shared seam is C2.
    """
    rows: list[list[list[float]]] = [[] for _ in range(6)]
    for j in range(5):
        A = [float(x) for x in a["positions"][j]]
        Ad = [float(x) for x in a["tangents"][j]]
        Add = [float(x) for x in a["curvatures"][j]]
        B = [float(x) for x in b["positions"][j]]
        Bd = [float(x) for x in b["tangents"][j]]
        Bdd = [float(x) for x in b["curvatures"][j]]
        p0 = A
        p1 = p_add(A, p_scale(Ad, 1.0 / 5.0))
        p2 = p_add(p_scale(Add, 1.0 / 20.0), p_sub(p_scale(p1, 2.0), p0))
        p5 = B
        p4 = p_sub(B, p_scale(Bd, 1.0 / 5.0))
        p3 = p_add(p_scale(Bdd, 1.0 / 20.0), p_sub(p_scale(p4, 2.0), p5))
        for i, p in enumerate((p0, p1, p2, p3, p4, p5)):
            rows[i].append(p)
    return rows


def compile_network(contract: dict[str, Any]) -> dict[str, list[list[list[float]]]]:
    stations = contract["stations"]
    out: dict[str, list[list[list[float]]]] = {}
    for i in range(len(stations) - 1):
        a, b = stations[i], stations[i + 1]
        out[f"PATCH-{i+1}-{a['id']}-TO-{b['id']}"] = compile_segment(a, b)
    return out


def raw_eval(cage: list[list[list[float]]], u: float, v: float, du: int = 0) -> list[float]:
    bu = bernstein(5, u) if du == 0 else bernstein_d1(5, u) if du == 1 else bernstein_d2(5, u)
    bv = bernstein(4, v)
    out = [0.0, 0.0, 0.0]
    for i in range(6):
        for j in range(5):
            w = bu[i] * bv[j]
            for k in range(3):
                out[k] += float(cage[i][j][k]) * w
    return out


def raw_norm(a: Iterable[float]) -> float:
    return math.sqrt(sum(float(x) * float(x) for x in a))


def raw_seam_metrics(a: list[list[list[float]]], b: list[list[list[float]]], samples: int = 41) -> dict[str, float]:
    pos, d1, d2 = [], [], []
    for j in range(samples):
        v = j / (samples - 1)
        pos.append(raw_norm(p_sub(raw_eval(a, 1.0, v, 0), raw_eval(b, 0.0, v, 0))))
        va, vb = raw_eval(a, 1.0, v, 1), raw_eval(b, 0.0, v, 1)
        na, nb = raw_norm(va), raw_norm(vb)
        dot = sum(va[k] * vb[k] for k in range(3)) / max(1e-30, na * nb)
        dot = max(-1.0, min(1.0, dot))
        d1.append(math.degrees(math.acos(dot)))
        d2.append(raw_norm(p_sub(raw_eval(a, 1.0, v, 2), raw_eval(b, 0.0, v, 2))))
    return {
        "max_position_error": max(pos),
        "max_tangent_angle_deg": max(d1),
        "max_second_derivative_error": max(d2),
    }


class JetPatch:
    def __init__(self, patch_id: str, cage: list[list[list[float]]]):
        self.id = patch_id
        self.cage = [[Vector(p) for p in row] for row in cage]

    def combine(self, bu: Iterable[float], bv: Iterable[float]) -> Vector:
        p = Vector((0.0, 0.0, 0.0))
        bu, bv = tuple(bu), tuple(bv)
        for i in range(6):
            for j in range(5):
                p += self.cage[i][j] * (bu[i] * bv[j])
        return p

    def evaluate(self, u: float, v: float):
        bu, bv = bernstein(5, u), bernstein(4, v)
        du, dv = bernstein_d1(5, u), bernstein_d1(4, v)
        ddu, ddv = bernstein_d2(5, u), bernstein_d2(4, v)
        s = self.combine(bu, bv)
        su = self.combine(du, bv)
        sv = self.combine(bu, dv)
        suu = self.combine(ddu, bv)
        svv = self.combine(bu, ddv)
        suv = self.combine(du, dv)
        return s, su, sv, suu, svv, suv

    def curvature(self, u: float, v: float):
        s, su, sv, suu, svv, suv = self.evaluate(u, v)
        nraw = su.cross(sv)
        jac = nraw.length
        if jac < 1e-12:
            raise ValueError(f"{self.id}: degenerate differential")
        n = nraw.normalized()
        E, F, G = su.dot(su), su.dot(sv), sv.dot(sv)
        e, f, g = n.dot(suu), n.dot(suv), n.dot(svv)
        den = E * G - F * F
        if abs(den) < 1e-12:
            raise ValueError(f"{self.id}: degenerate first fundamental form")
        K = (e * g - f * f) / den
        H = (E * g - 2 * F * f + G * e) / (2 * den)
        return s, n, jac, H, K


def angle_deg(a: Vector, b: Vector) -> float:
    if a.length < 1e-12 or b.length < 1e-12:
        return 180.0
    c = max(-1.0, min(1.0, a.dot(b) / (a.length * b.length)))
    return math.degrees(math.acos(c))


def runtime_seam_metrics(a: JetPatch, b: JetPatch, samples: int = 41) -> dict[str, float]:
    pos, tangent, second, normal, mean = [], [], [], [], []
    for j in range(samples):
        v = j / (samples - 1)
        sa, sua, _, suua, _, _ = a.evaluate(1.0, v)
        sb, sub, _, suub, _, _ = b.evaluate(0.0, v)
        _, na, _, Ha, _ = a.curvature(1.0, v)
        _, nb, _, Hb, _ = b.curvature(0.0, v)
        pos.append((sa - sb).length)
        tangent.append(angle_deg(sua, sub))
        second.append((suua - suub).length)
        normal.append(angle_deg(na, nb))
        mean.append(abs(Ha - Hb))
    return {
        "runtime_max_position_error": max(pos),
        "runtime_max_tangent_angle_deg": max(tangent),
        "runtime_max_second_derivative_error": max(second),
        "runtime_max_normal_angle_deg": max(normal),
        "runtime_max_mean_curvature_difference": max(mean),
    }


def patch_fairness(patch: JetPatch, nu: int = 31, nv: int = 21) -> dict[str, float]:
    normals: list[list[Vector]] = []
    means: list[list[float]] = []
    positions: list[list[Vector]] = []
    min_jac = float("inf")
    for i in range(nu):
        nr, hr, pr = [], [], []
        for j in range(nv):
            s, n, jac, H, _ = patch.curvature(i / (nu - 1), j / (nv - 1))
            min_jac = min(min_jac, jac)
            nr.append(n); hr.append(H); pr.append(s)
        normals.append(nr); means.append(hr); positions.append(pr)
    jumps, rates = [], []
    for i in range(nu):
        for j in range(nv):
            if i + 1 < nu:
                jumps.append(angle_deg(normals[i][j], normals[i + 1][j]))
                ds = max(1e-9, (positions[i + 1][j] - positions[i][j]).length)
                rates.append(abs(means[i + 1][j] - means[i][j]) / ds)
            if j + 1 < nv:
                jumps.append(angle_deg(normals[i][j], normals[i][j + 1]))
                ds = max(1e-9, (positions[i][j + 1] - positions[i][j]).length)
                rates.append(abs(means[i][j + 1] - means[i][j]) / ds)
    sj = sorted(jumps)
    return {
        "min_surface_jacobian": min_jac,
        "max_adjacent_normal_jump_deg": max(jumps),
        "p95_adjacent_normal_jump_deg": sj[int(0.95 * (len(sj) - 1))],
        "max_mean_curvature_rate_proxy": max(rates),
    }


def source_keys(contract: dict[str, Any]) -> dict[tuple[str, str, int], tuple[float, float, float]]:
    out = {}
    for station in contract["stations"]:
        for field in ("positions", "tangents", "curvatures"):
            for i, value in enumerate(station[field]):
                out[(station["id"], field, i)] = tuple(float(x) for x in value)
    return out


def apply_control(contract: dict[str, Any], control_id: str) -> tuple[dict[str, Any], set[tuple[str, str, int]]]:
    out = copy.deepcopy(contract)
    smap = station_map(out)
    declared: set[tuple[str, str, int]] = set()
    for edit in out["semantic_controls"][control_id]:
        sid, field, idx = edit["station"], edit["field"], int(edit["index"])
        delta = [float(x) for x in edit["delta"]]
        key = (sid, field, idx)
        declared.add(key)
        smap[sid][field][idx] = [float(smap[sid][field][idx][k]) + delta[k] for k in range(3)]
    return out, declared


def changed_source_keys(base: dict[str, Any], variant: dict[str, Any], tol: float = 1e-12) -> set[tuple[str, str, int]]:
    a, b = source_keys(base), source_keys(variant)
    return {k for k in a if any(abs(a[k][i] - b[k][i]) > tol for i in range(3))}


def network_max_displacement(base: dict[str, list[list[list[float]]]], variant: dict[str, list[list[list[float]]]], samples: int = 13) -> float:
    maximum = 0.0
    for pid in base:
        a, b = JetPatch(pid, base[pid]), JetPatch(pid, variant[pid])
        for i in range(samples):
            for j in range(7):
                pa = a.evaluate(i / (samples - 1), j / 6)[0]
                pb = b.evaluate(i / (samples - 1), j / 6)[0]
                maximum = max(maximum, (pa - pb).length)
    return maximum


def evaluate_contract(contract: dict[str, Any]) -> tuple[dict[str, Any], dict[str, list[list[list[float]]]]]:
    thresholds = contract["fairness_thresholds"]
    network = compile_network(contract)
    ids = list(network)
    patches = {pid: JetPatch(pid, cage) for pid, cage in network.items()}
    seams = []
    seam_ok = True
    for i in range(len(ids) - 1):
        raw = raw_seam_metrics(network[ids[i]], network[ids[i + 1]])
        runtime = runtime_seam_metrics(patches[ids[i]], patches[ids[i + 1]])
        row = {"between": [ids[i], ids[i + 1]], **raw, **runtime}
        seams.append(row)
        seam_ok = seam_ok and (
            raw["max_position_error"] <= thresholds["max_seam_position_error"] and
            raw["max_tangent_angle_deg"] <= thresholds["max_seam_tangent_angle_deg"] and
            raw["max_second_derivative_error"] <= thresholds["max_seam_second_derivative_error"] and
            runtime["runtime_max_second_derivative_error"] <= RUNTIME_SECOND_DERIVATIVE_TOL
        )
    fairness = {pid: patch_fairness(patch) for pid, patch in patches.items()}
    fair_ok = all(
        row["min_surface_jacobian"] >= thresholds["min_surface_jacobian"] and
        row["max_adjacent_normal_jump_deg"] <= thresholds["max_adjacent_normal_jump_deg"] and
        row["max_mean_curvature_rate_proxy"] <= thresholds["max_mean_curvature_rate_proxy"]
        for row in fairness.values()
    )
    report = {
        "compiler_seams": seams,
        "patch_fairness": fairness,
        "checks": {
            "five_independent_source_stations": len(contract["stations"]) == 5,
            "shared_position_tangent_curvature_jets": contract["architecture"]["continuity_policy"].startswith("adjacent patches share"),
            "four_analytic_longitudinal_patches": len(network) == 4,
            "compiler_c2_seams_pass": seam_ok,
            "all_patch_interior_fairness_pass": fair_ok,
            "execution_topology_is_derived": contract["authority"]["execution_geometry"] == "DERIVED",
            "mesh_stitching_not_surface_authority": contract["architecture"]["mesh_stitching_as_surface_authority"] is False,
        }
    }
    return report, network


def build_execution_mesh(network: dict[str, list[list[list[float]]]], nu: int = 25, nv: int = 21):
    ids = list(network)
    rows: list[list[Vector]] = []
    seam_rows: list[int] = []
    for pi, pid in enumerate(ids):
        patch = JetPatch(pid, network[pid])
        for i in range(nu):
            if pi and i == 0:
                continue
            u = i / (nu - 1)
            rows.append([patch.evaluate(u, j / (nv - 1))[0] for j in range(nv)])
        if pi < len(ids) - 1:
            seam_rows.append(len(rows) - 1)
    verts = [tuple(p) for row in rows for p in row]
    faces = []
    def idx(i: int, j: int) -> int: return i * nv + j
    for i in range(len(rows) - 1):
        for j in range(nv - 1):
            faces.append((idx(i,j), idx(i+1,j), idx(i+1,j+1), idx(i,j+1)))
    me = bpy.data.meshes.new("E3_R2_DERIVED_EXECUTION_MESH")
    me.from_pydata(verts, [], faces); me.update()
    obj = bpy.data.objects.new("E3_R2_DERIVED_EXECUTION_SURFACE", me); bpy.context.collection.objects.link(obj)
    for poly in me.polygons: poly.use_smooth = True
    obj["OLEANDER_AUTHORITY"] = "DERIVED_EXECUTION_GEOMETRY"
    obj["OLEANDER_SURFACE_SOURCE"] = "E3_R2_VOLUME_JETS"
    mod = obj.modifiers.new("Mirror-Symmetry", "MIRROR")
    mod.use_axis[0] = False; mod.use_axis[1] = True; mod.use_clip = True; mod.use_mirror_merge = True
    return obj, rows, seam_rows


def diagnostics(contract: dict[str, Any], network: dict[str, list[list[list[float]]]], cage_mat, seam_mat):
    objs = []
    # Authoritative station curves.
    for station in contract["stations"]:
        pts = [Vector(p) for p in station["positions"]]
        objs.append(e2.poly_curve(station["id"], pts, cage_mat, 0.008))
    # Shared seams from the compiled network.
    ids = list(network)
    for i in range(len(ids) - 1):
        patch = JetPatch(ids[i], network[ids[i]])
        pts = [patch.evaluate(1.0, j / 80)[0] for j in range(81)]
        objs.append(e2.poly_curve(f"E3-R2-SEAM-{i+1}", pts, seam_mat, 0.012))
    return objs


def make_scene(contract: dict[str, Any], network: dict[str, list[list[list[float]]]], out: Path, resolution: int, tag: str, full_views: bool):
    e2.clear_scene()
    clay = e2.material(f"MAT-{tag}-CLAY", (0.36,0.38,0.41), 0.30)
    cage_mat = e2.material(f"MAT-{tag}-SOURCE", (0.025,0.025,0.03), 0.42)
    seam_mat = e2.material(f"MAT-{tag}-SEAM", (0.72,0.74,0.78), 0.22, 0.15)
    zebra = e2.zebra_material()
    surface, rows, seam_rows = build_execution_mesh(network)
    surface.name = f"{tag}_DERIVED_EXECUTION_SURFACE"
    diags = diagnostics(contract, network, cage_mat, seam_mat)
    scene = e2.scene_setup(resolution)
    target = (0.0, 0.0, 0.72)
    if full_views:
        cams = {
            "E3_R2_HERO": e2.camera("CAM-E3-R2-HERO", (4.3,4.5,2.8), target, 5.8),
            "E3_R2_SIDE": e2.camera("CAM-E3-R2-SIDE", (0.0,6.4,1.0), target, 5.7),
            "E3_R2_TOP": e2.camera("CAM-E3-R2-TOP", (0.0,0.2,6.5), (0.0,0.0,0.60), 5.8),
            "E3_R2_ZEBRA": e2.camera("CAM-E3-R2-ZEBRA", (4.4,4.2,2.5), target, 5.7),
        }
        e2.render(scene, out, cams["E3_R2_HERO"], "E3_R2_HERO", surface, clay)
        e2.render(scene, out, cams["E3_R2_SIDE"], "E3_R2_SIDE", surface, clay)
        e2.render(scene, out, cams["E3_R2_TOP"], "E3_R2_TOP", surface, clay)
        for obj in diags: obj.hide_render = True
        e2.render(scene, out, cams["E3_R2_ZEBRA"], "E3_R2_ZEBRA", surface, zebra)
        for obj in diags: obj.hide_render = False
    else:
        cam = e2.camera(f"CAM-{tag}-SIDE", (0.0,6.4,1.0), target, 5.7)
        e2.render(scene, out, cam, f"E3_R2_VARIANT_{tag}_SIDE", surface, clay)
    return scene, len(rows), seam_rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--resolution", type=int, default=512)
    args = ap.parse_args(user_args())
    contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))
    out = Path(args.out).resolve(); out.mkdir(parents=True, exist_ok=True)

    base_report, base_network = evaluate_contract(contract)
    base_source = source_keys(contract)
    variant_rows: dict[str, Any] = {}
    all_exact = True
    all_fair = True
    all_legible = True
    for control_id in contract["semantic_controls"]:
        variant_contract, declared = apply_control(contract, control_id)
        actual = changed_source_keys(contract, variant_contract)
        vreport, vnetwork = evaluate_contract(variant_contract)
        displacement = network_max_displacement(base_network, vnetwork)
        exact = actual == declared
        fair = all(vreport["checks"].values())
        legible = 0.04 <= displacement <= 0.30
        all_exact = all_exact and exact
        all_fair = all_fair and fair
        all_legible = all_legible and legible
        changed_patches = [pid for pid in base_network if base_network[pid] != vnetwork[pid]]
        variant_rows[control_id] = {
            "declared_source_keys": [list(x) for x in sorted(declared)],
            "actual_changed_source_keys": [list(x) for x in sorted(actual)],
            "source_edit_exact": exact,
            "derived_changed_patches": changed_patches,
            "max_surface_displacement": displacement,
            "working_fidelity_visual_legibility_proxy": legible,
            "machine_fairness_pass": fair,
            "seams": vreport["compiler_seams"],
            "patch_fairness": vreport["patch_fairness"],
        }

    checks = {
        **base_report["checks"],
        "semantic_source_edits_exact": all_exact,
        "all_semantic_variants_fair": all_fair,
        "all_semantic_variants_have_working_fidelity_effect": all_legible,
        "source_authority_is_station_jets_not_execution_mesh": contract["architecture"]["source_authority"] == "STATION_POSITION_TANGENT_CURVATURE_JETS",
        "r1_single_center_cage_not_reused": "center_patch_cage" not in contract,
    }
    status = "MACHINE_PASS_HUMAN_PROJECT_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL_REVISE_E3_R2_ARCHITECTURE"
    report = {
        "schema": "oleander.modeling-worker.v0.12.e3.r2.machine-report",
        "model": MODEL,
        "status": status,
        "decision_question": contract["decision_question"],
        "checks": checks,
        "base": base_report,
        "semantic_control_variants": variant_rows,
        "boundary": "R2 Machine PASS proves independent source-jet isolation, analytic C2 compilation, interior fairness and a minimum working-fidelity geometric effect. It does not prove Project/Visual design quality; Human review remains mandatory before any M4.5 application PASS, PAP or Promotion."
    }

    scene, sample_rows, seam_rows = make_scene(contract, base_network, out, args.resolution, "BASE", True)
    scene["OLEANDER_MODEL"] = MODEL
    scene["OLEANDER_STAGE"] = "E3_R2_APPLICATION_MACHINE"
    scene["OLEANDER_AUTHORITY"] = "WORKING_SURFACE_SOURCE"
    scene["OLEANDER_SOURCE_ARCHITECTURE"] = contract["architecture"]["type"]
    blend = out / f"{MODEL}.blend"; bpy.ops.wm.save_as_mainfile(filepath=str(blend))

    for control_id in contract["semantic_controls"]:
        variant_contract, _ = apply_control(contract, control_id)
        _, variant_network = evaluate_contract(variant_contract)
        make_scene(variant_contract, variant_network, out, args.resolution, control_id.replace("VOL-", ""), False)

    (out / "E3_R2_MACHINE_REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "E3_R2_COMPILED_SURFACE_SOURCE.json").write_text(json.dumps({
        "schema": "oleander.modeling-worker.v0.12.e3.r2.compiled-surface-source",
        "authority": "WORKING_SURFACE_SOURCE",
        "source_authority": contract["architecture"]["source_authority"],
        "source_stations": contract["stations"],
        "compiled_network": base_network,
        "execution_geometry": {"derived": True, "editable_authority": False, "sample_rows": sample_rows, "seam_row_indices": seam_rows}
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if status == "MACHINE_PASS_HUMAN_PROJECT_VISUAL_REVIEW_REQUIRED" else 5


if __name__ == "__main__":
    raise SystemExit(main())
