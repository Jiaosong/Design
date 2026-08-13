#!/usr/bin/env python3
"""OLEANDER Modeling Worker v0.12 E3 R3 — Coupled Semantic Surface Network.

R3 re-enters only the Automotive application Surface Source architecture. It does not
redefine E1/E2 generic method authority. Profile and plan-view Primary Curves are separate
source authorities. Upper, Side and Lower main surface families are compiled independently
from shared declared boundary curves; Front and Rear termination networks are independent
continuation families. Boundary relationships are evaluated by their declared class rather
than a blanket C2 policy.

Machine PASS only opens Human Project/Visual QA. No Class-A, engineering, production panel,
manufacturing, PAP or Promotion authority is implied.
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
from typing import Any, Callable, Iterable

HERE = Path(__file__).resolve().parent
GENERIC_E2 = HERE.parents[1] / "v0.12" / "e2_multipatch_network.py"
_spec = importlib.util.spec_from_file_location("oleander_v012_e2", GENERIC_E2)
e2 = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(e2)
Vector = e2.Vector
bpy = e2.bpy

MODEL = "OLEANDER_ModelingWorker_v0.12_E3_R3_CoupledSemanticSurfaceNetwork"


def user_args() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]


def b(n: int, t: float) -> list[float]:
    s = 1.0 - t
    return [comb(n, i) * (t ** i) * (s ** (n - i)) for i in range(n + 1)]


def bezier(values: list[float], t: float) -> float:
    weights = b(len(values) - 1, t)
    return sum(float(v) * w for v, w in zip(values, weights))


def clamp01(x: float) -> float:
    return min(1.0, max(0.0, x))


def hermite(p0: Vector, p1: Vector, d0: Vector, d1: Vector, t: float) -> Vector:
    t2, t3 = t * t, t * t * t
    h00 = 2*t3 - 3*t2 + 1
    h10 = t3 - 2*t2 + t
    h01 = -2*t3 + 3*t2
    h11 = t3 - t2
    return p0*h00 + d0*h10 + p1*h01 + d1*h11


def angle_deg(a: Vector, b_: Vector) -> float:
    if a.length < 1e-12 or b_.length < 1e-12:
        return 180.0
    c = max(-1.0, min(1.0, a.dot(b_) / (a.length * b_.length)))
    return math.degrees(math.acos(c))


def numerical_derivative(fn: Callable[[float, float], Vector], u: float, v: float, axis: int, h: float = 2e-4) -> Vector:
    if axis == 0:
        if u <= h:
            return (fn(u+h, v) - fn(u, v)) / h
        if u >= 1-h:
            return (fn(u, v) - fn(u-h, v)) / h
        return (fn(u+h, v) - fn(u-h, v)) / (2*h)
    if v <= h:
        return (fn(u, v+h) - fn(u, v)) / h
    if v >= 1-h:
        return (fn(u, v) - fn(u, v-h)) / h
    return (fn(u, v+h) - fn(u, v-h)) / (2*h)


def numerical_normal(fn: Callable[[float, float], Vector], u: float, v: float) -> Vector:
    du = numerical_derivative(fn, u, v, 0)
    dv = numerical_derivative(fn, u, v, 1)
    n = du.cross(dv)
    if n.length < 1e-12:
        raise ValueError("degenerate numerical surface normal")
    return n.normalized()


def source_key(edit: dict[str, Any]) -> tuple:
    authority = edit["authority"]
    if authority in ("PROFILE", "PLAN"):
        return (authority, edit["curve"], int(edit["index"]))
    return (authority, edit["family"], edit["field"])


class R3Network:
    def __init__(self, contract: dict[str, Any]):
        self.contract = contract
        self.xc = [float(x) for x in contract["curve_parameterization"]["x_controls"]]
        self.profile = contract["profile_primary_curves"]
        self.plan = contract["plan_primary_curves"]
        self.bt = contract["boundary_tangent_policies"]
        self.terms = contract["surface_sources"]

    def x(self, u: float) -> float:
        return bezier(self.xc, u)

    def boundary(self, name: str, u: float) -> Vector:
        x = self.x(u)
        if name == "CENTER":
            return Vector((x, bezier(self.plan["PLAN-CENTER"], u), bezier(self.profile["PROFILE-UPPER-CENTER"], u)))
        if name == "SHOULDER":
            return Vector((x, bezier(self.plan["PLAN-SHOULDER"], u), bezier(self.profile["PROFILE-SHOULDER-HEIGHT"], u)))
        if name == "ROCKER":
            return Vector((x, bezier(self.plan["PLAN-ROCKER"], u), bezier(self.profile["PROFILE-ROCKER"], u)))
        if name == "UNDER":
            return Vector((x, bezier(self.plan["PLAN-UNDERBODY-EDGE"], u), bezier(self.profile["PROFILE-UNDERBODY-EDGE"], u)))
        raise KeyError(name)

    def shoulder_tangent(self, u: float) -> Vector:
        sh, rock = self.boundary("SHOULDER", u), self.boundary("ROCKER", u)
        return (rock - sh) * float(self.bt["BND-SHOULDER-TANGENT"]["scale"])

    def rocker_tangent(self, u: float) -> Vector:
        rock, under = self.boundary("ROCKER", u), self.boundary("UNDER", u)
        return (under - rock) * float(self.bt["BND-ROCKER-TANGENT"]["scale"])

    def under_tangent(self, u: float) -> Vector:
        yz = self.bt["BND-UNDERBODY-TANGENT"]["vector_yz"]
        return Vector((0.0, float(yz[0]), float(yz[1])))

    def upper(self, u: float, v: float) -> Vector:
        c, sh = self.boundary("CENTER", u), self.boundary("SHOULDER", u)
        dc = Vector((0.0, max(0.12, sh.y * 0.72), 0.0))
        return hermite(c, sh, dc, self.shoulder_tangent(u), v)

    def side(self, u: float, v: float) -> Vector:
        sh, rock = self.boundary("SHOULDER", u), self.boundary("ROCKER", u)
        return hermite(sh, rock, self.shoulder_tangent(u), self.rocker_tangent(u), v)

    def lower(self, u: float, v: float) -> Vector:
        rock, under = self.boundary("ROCKER", u), self.boundary("UNDER", u)
        return hermite(rock, under, self.rocker_tangent(u), self.under_tangent(u), v)

    def family_fn(self, family: str) -> Callable[[float, float], Vector]:
        return {"SURF-UPPER": self.upper, "SURF-SIDE": self.side, "SURF-LOWER": self.lower}[family]

    def composite(self, u: float, w: float) -> Vector:
        w = min(3.0, max(0.0, w))
        if w <= 1.0:
            return self.upper(u, w)
        if w <= 2.0:
            return self.side(u, w - 1.0)
        return self.lower(u, w - 2.0)

    def composite_du(self, u: float, w: float) -> Vector:
        h = 2e-4
        if u <= h:
            return (self.composite(u+h, w) - self.composite(u, w)) / h
        if u >= 1-h:
            return (self.composite(u, w) - self.composite(u-h, w)) / h
        return (self.composite(u+h, w) - self.composite(u-h, w)) / (2*h)

    def term_tip(self, front: bool, w: float) -> Vector:
        u = 0.0 if front else 1.0
        p = self.composite(u, w)
        family = "SURF-FRONT-TERM" if front else "SURF-REAR-TERM"
        spec = self.terms[family]
        length = float(spec["length"])
        scale = float(spec["width_scale"])
        vb = float(spec["vertical_blend"])
        direction = 1.0 if front else -1.0
        z_anchor = 0.46 if front else 0.44
        return Vector((p.x + direction*length, p.y*scale, z_anchor + (p.z-z_anchor)*vb))

    def front_term(self, s: float, wnorm: float) -> Vector:
        w = wnorm * 3.0
        p = self.composite(0.0, w)
        q = self.term_tip(True, w)
        length = float(self.terms["SURF-FRONT-TERM"]["length"])
        du = self.composite_du(0.0, w)
        scale = length / max(1e-9, abs(du.x))
        d1 = du * scale
        d0 = Vector((-length*0.78, (p.y-q.y)*0.48, (p.z-q.z)*0.42))
        return hermite(q, p, d0, d1, s)

    def rear_term(self, s: float, wnorm: float) -> Vector:
        w = wnorm * 3.0
        p = self.composite(1.0, w)
        q = self.term_tip(False, w)
        length = float(self.terms["SURF-REAR-TERM"]["length"])
        du = self.composite_du(1.0, w)
        scale = length / max(1e-9, abs(du.x))
        d0 = du * scale
        d1 = Vector((-length*0.78, (q.y-p.y)*0.48, (q.z-p.z)*0.42))
        return hermite(p, q, d0, d1, s)


def surface_fairness(fn: Callable[[float, float], Vector], nu: int = 37, nv: int = 17) -> dict[str, float]:
    normals: list[list[Vector]] = []
    positions: list[list[Vector]] = []
    min_area = float("inf")
    jumps: list[float] = []
    acceleration: list[float] = []

    for i in range(nu):
        u = i/(nu-1)
        nr, pr = [], []
        for j in range(nv):
            v = j/(nv-1)
            pr.append(fn(u,v))
            nr.append(numerical_normal(fn,u,v))
        normals.append(nr); positions.append(pr)

    for i in range(nu-1):
        for j in range(nv-1):
            a = positions[i][j]
            du = positions[i+1][j] - a
            dv = positions[i][j+1] - a
            min_area = min(min_area, du.cross(dv).length)

    for i in range(nu):
        for j in range(nv):
            if i+1 < nu:
                jumps.append(angle_deg(normals[i][j], normals[i+1][j]))
            if j+1 < nv:
                jumps.append(angle_deg(normals[i][j], normals[i][j+1]))
            if 0 < i < nu-1:
                a1 = angle_deg(normals[i-1][j], normals[i][j])
                a2 = angle_deg(normals[i][j], normals[i+1][j])
                acceleration.append(abs(a2-a1) * 6.0)
            if 0 < j < nv-1:
                a1 = angle_deg(normals[i][j-1], normals[i][j])
                a2 = angle_deg(normals[i][j], normals[i][j+1])
                acceleration.append(abs(a2-a1) * 6.0)
    return {
        "max_adjacent_normal_jump_deg": max(jumps),
        "p95_adjacent_normal_jump_deg": sorted(jumps)[int(0.95*(len(jumps)-1))],
        "max_normal_acceleration_proxy": max(acceleration) if acceleration else 0.0,
        "min_surface_cell_area_proxy": min_area
    }


def boundary_relation_metrics(net: R3Network, relation: dict[str, Any], samples: int = 41) -> dict[str, Any]:
    rid = relation["id"]
    cls = relation["class"]
    row: dict[str, Any] = {"id": rid, "class": cls, "boundary": relation["boundary"]}
    if cls == "INTENTIONAL_BOUNDARY":
        row["declared_without_smooth_continuity_claim"] = True
        row["pass"] = True
        return row

    positions, normals = [], []
    if rid == "REL-R3-01":
        for i in range(samples):
            u=i/(samples-1)
            positions.append((net.upper(u,1.0)-net.side(u,0.0)).length)
            normals.append(angle_deg(numerical_normal(net.upper,u,1.0), numerical_normal(net.side,u,0.0)))
    elif rid == "REL-R3-02":
        for i in range(samples):
            u=i/(samples-1)
            positions.append((net.side(u,1.0)-net.lower(u,0.0)).length)
            normals.append(angle_deg(numerical_normal(net.side,u,1.0), numerical_normal(net.lower,u,0.0)))
    elif rid == "REL-R3-03":
        for i in range(samples):
            w=i/(samples-1)
            positions.append((net.front_term(1.0,w)-net.composite(0.0,w*3.0)).length)
            normals.append(angle_deg(numerical_normal(net.front_term,1.0,w), numerical_normal(lambda u,v: net.composite(u,v*3.0),0.0,w)))
    elif rid == "REL-R3-04":
        for i in range(samples):
            w=i/(samples-1)
            positions.append((net.composite(1.0,w*3.0)-net.rear_term(0.0,w)).length)
            normals.append(angle_deg(numerical_normal(lambda u,v: net.composite(u,v*3.0),1.0,w), numerical_normal(net.rear_term,0.0,w)))
    elif cls == "CURVATURE_RATE":
        curve_a = relation["source"]
        curve_b = relation["target"]
        rate = curve_pair_rate_proxy(net, curve_a, curve_b)
        row["max_rate_proxy"] = rate
        row["threshold"] = float(relation["max_rate_proxy"])
        row["pass"] = rate <= row["threshold"]
        return row
    else:
        raise ValueError(f"unsupported relationship: {rid}")

    row["max_position_error"] = max(positions)
    row["max_normal_angle_deg"] = max(normals)
    row["position_threshold"] = float(relation["max_position_error"])
    row["normal_threshold"] = float(relation["max_normal_angle_deg"])
    row["pass"] = row["max_position_error"] <= row["position_threshold"] and row["max_normal_angle_deg"] <= row["normal_threshold"]
    return row


def curve_values(net: R3Network, curve_id: str, n: int = 81) -> list[Vector]:
    out=[]
    for i in range(n):
        u=i/(n-1); x=net.x(u)
        if curve_id in net.profile:
            out.append(Vector((x,0.0,bezier(net.profile[curve_id],u))))
        elif curve_id in net.plan:
            out.append(Vector((x,bezier(net.plan[curve_id],u),0.0)))
        else:
            raise KeyError(curve_id)
    return out


def curve_curvature_proxy(points: list[Vector]) -> list[float]:
    vals=[]
    for i in range(1,len(points)-1):
        a,b_,c=points[i-1],points[i],points[i+1]
        ab=b_-a; bc=c-b_
        ds=max(1e-9,0.5*(ab.length+bc.length))
        vals.append(angle_deg(ab,bc)/ds)
    return vals


def curve_pair_rate_proxy(net: R3Network, curve_a: str, curve_b: str) -> float:
    ka=curve_curvature_proxy(curve_values(net,curve_a))
    kb=curve_curvature_proxy(curve_values(net,curve_b))
    rates=[]
    for arr in (ka,kb):
        for i in range(1,len(arr)):
            rates.append(abs(arr[i]-arr[i-1]))
    return max(rates) if rates else 0.0


def profile_metrics(net: R3Network) -> dict[str, float | int]:
    pts=curve_values(net,"PROFILE-UPPER-CENTER",121)
    slopes=[]
    for a,b_ in zip(pts,pts[1:]):
        dx=b_.x-a.x
        slopes.append((b_.z-a.z)/(dx if abs(dx)>1e-9 else -1e-9))
    slope_changes=[abs(slopes[i]-slopes[i-1]) for i in range(1,len(slopes))]
    second=[slopes[i]-slopes[i-1] for i in range(1,len(slopes))]
    signs=[]
    for v in second:
        if abs(v)>1e-4: signs.append(1 if v>0 else -1)
    inflections=sum(1 for a,b_ in zip(signs,signs[1:]) if a!=b_)
    return {
        "max_profile_slope_change_proxy": max(slope_changes),
        "profile_inflection_count": inflections,
        "front_hood_height": bezier(net.profile["PROFILE-UPPER-CENTER"],0.20),
        "cabin_peak_height": max(bezier(net.profile["PROFILE-UPPER-CENTER"],i/120) for i in range(121))
    }


def plan_metrics(net: R3Network) -> dict[str, float]:
    shoulder=[bezier(net.plan["PLAN-SHOULDER"],i/120) for i in range(121)]
    front=max(shoulder[:48])
    rear=max(shoulder[66:112])
    rocker=[bezier(net.plan["PLAN-ROCKER"],i/120) for i in range(121)]
    return {
        "front_shoulder_max": front,
        "rear_shoulder_max": rear,
        "rear_haunch_plan_advantage": rear-front,
        "max_shoulder_width": max(shoulder),
        "max_rocker_width": max(rocker)
    }


def reflection_field_proxy(net: R3Network) -> float:
    vals=[]
    for family in ("SURF-UPPER","SURF-SIDE","SURF-LOWER"):
        fn=net.family_fn(family)
        normals=[]
        for i in range(41):
            u=i/40
            normals.append(numerical_normal(fn,u,0.52))
        angles=[angle_deg(normals[i],normals[i+1]) for i in range(len(normals)-1)]
        vals.extend(abs(angles[i]-angles[i-1])*6.0 for i in range(1,len(angles)))
    return max(vals) if vals else 0.0


def apply_control(contract: dict[str,Any], cid: str) -> tuple[dict[str,Any], set[tuple]]:
    out=copy.deepcopy(contract); declared=set()
    for edit in out["semantic_controls"][cid]:
        key=source_key(edit); declared.add(key)
        if edit["authority"]=="PROFILE":
            out["profile_primary_curves"][edit["curve"]][int(edit["index"])]+=float(edit["delta"])
        elif edit["authority"]=="PLAN":
            out["plan_primary_curves"][edit["curve"]][int(edit["index"])]+=float(edit["delta"])
        else:
            out["surface_sources"][edit["family"]][edit["field"]]+=float(edit["delta"])
    return out,declared


def source_snapshot(contract: dict[str,Any]) -> dict[tuple,float]:
    out={}
    for cid,vals in contract["profile_primary_curves"].items():
        for i,v in enumerate(vals): out[("PROFILE",cid,i)]=float(v)
    for cid,vals in contract["plan_primary_curves"].items():
        for i,v in enumerate(vals): out[("PLAN",cid,i)]=float(v)
    for fam in ("SURF-FRONT-TERM","SURF-REAR-TERM"):
        for field in ("length","width_scale","vertical_blend"):
            out[("TERMINATION",fam,field)]=float(contract["surface_sources"][fam][field])
    return out


def changed_keys(base: dict[str,Any], var: dict[str,Any]) -> set[tuple]:
    a,b_=source_snapshot(base),source_snapshot(var)
    return {k for k in a if abs(a[k]-b_[k])>1e-12}


def max_displacement(a: R3Network,b_: R3Network) -> float:
    m=0.0
    for i in range(31):
        u=i/30
        for j in range(25):
            w=3*j/24
            m=max(m,(a.composite(u,w)-b_.composite(u,w)).length)
    for front in (True,False):
        fa=a.front_term if front else a.rear_term
        fb=b_.front_term if front else b_.rear_term
        for i in range(13):
            s=i/12
            for j in range(13):
                w=j/12
                m=max(m,(fa(s,w)-fb(s,w)).length)
    return m


def source_ownership(contract: dict[str,Any]) -> tuple[dict[str,list[list]],list[dict]]:
    owners={}; seen={}; overlaps=[]
    for cid,edits in contract["semantic_controls"].items():
        keys={source_key(e) for e in edits}; owners[cid]=[list(k) for k in sorted(keys,key=str)]
        for k in keys:
            if k in seen: overlaps.append({"key":list(k),"controls":sorted([seen[k],cid])})
            else: seen[k]=cid
    return owners,overlaps


def family_fairness(net: R3Network) -> dict[str,dict[str,float]]:
    out={}
    for fam in ("SURF-UPPER","SURF-SIDE","SURF-LOWER"):
        out[fam]=surface_fairness(net.family_fn(fam))
    out["SURF-FRONT-TERM"]=surface_fairness(net.front_term,25,19)
    out["SURF-REAR-TERM"]=surface_fairness(net.rear_term,25,19)
    return out


def evaluate(contract: dict[str,Any]) -> tuple[dict[str,Any],R3Network]:
    net=R3Network(contract); th=contract["machine_thresholds"]
    fairness=family_fairness(net)
    fair_ok=all(
        r["max_adjacent_normal_jump_deg"]<=th["max_surface_adjacent_normal_jump_deg"]
        and r["max_normal_acceleration_proxy"]<=th["max_surface_normal_acceleration_proxy"]
        and r["min_surface_cell_area_proxy"]>=th["min_surface_cell_area_proxy"]
        for r in fairness.values()
    )
    relations=[boundary_relation_metrics(net,r) for r in contract["relationship_graph"]]
    rel_ok=all(r["pass"] for r in relations)
    profile=profile_metrics(net); plan=plan_metrics(net); refl=reflection_field_proxy(net)
    profile_ok=profile["max_profile_slope_change_proxy"]<=th["max_profile_slope_change_proxy"] and profile["profile_inflection_count"]<=th["max_profile_inflection_count"]
    plan_ok=plan["rear_haunch_plan_advantage"]>=th["min_rear_haunch_plan_advantage"]
    reflect_ok=refl<=th["max_reflection_field_acceleration_proxy"]
    owners,overlaps=source_ownership(contract)
    classes={r["class"] for r in contract["relationship_graph"]}
    checks={
        "five_surface_source_families": len(contract["architecture"]["main_surface_families"])+len(contract["architecture"]["termination_families"])==5,
        "profile_plan_primary_curve_authority_separated": contract["architecture"]["profile_plan_authority_separated"] is True,
        "global_control_cage_forbidden": contract["architecture"]["global_control_cage_forbidden"] is True,
        "relationship_specific_continuity_classes": len(classes)>=3 and contract["architecture"]["blanket_continuity_class_forbidden"] is True,
        "declared_boundary_relationships_pass": rel_ok,
        "all_surface_family_interior_fairness_pass": fair_ok,
        "semantic_control_source_ownership_disjoint": not overlaps,
        "profile_silhouette_metrics_pass": profile_ok,
        "plan_view_rear_haunch_hierarchy_pass": plan_ok,
        "reflection_field_proxy_pass": reflect_ok,
        "execution_topology_is_derived": contract["authority"]["execution_geometry"]=="DERIVED"
    }
    return {
        "checks":checks,
        "surface_fairness":fairness,
        "relationship_metrics":relations,
        "profile_metrics":profile,
        "plan_metrics":plan,
        "reflection_field_acceleration_proxy":refl,
        "semantic_source_ownership":owners,
        "semantic_source_overlaps":overlaps
    },net


def build_mesh(net: R3Network, nu_main: int=49, ns_term: int=13, nband: int=16):
    nw=nband*3+1
    rows=[]
    # front tip -> main front seam
    for i in range(ns_term):
        s=i/(ns_term-1)
        rows.append([net.front_term(s,j/(nw-1)) for j in range(nw)])
    # main, skip u=0 duplicate
    for i in range(1,nu_main):
        u=i/(nu_main-1)
        rows.append([net.composite(u,3*j/(nw-1)) for j in range(nw)])
    # rear, skip seam s=0 duplicate
    for i in range(1,ns_term):
        s=i/(ns_term-1)
        rows.append([net.rear_term(s,j/(nw-1)) for j in range(nw)])
    verts=[tuple(p) for row in rows for p in row]; faces=[]
    def idx(i,j): return i*nw+j
    for i in range(len(rows)-1):
        for j in range(nw-1):
            faces.append((idx(i,j),idx(i+1,j),idx(i+1,j+1),idx(i,j+1)))
    me=bpy.data.meshes.new("E3_R3_DERIVED_EXECUTION_MESH"); me.from_pydata(verts,[],faces); me.update()
    obj=bpy.data.objects.new("E3_R3_DERIVED_EXECUTION_SURFACE",me); bpy.context.collection.objects.link(obj)
    for p in me.polygons:p.use_smooth=True
    obj["OLEANDER_AUTHORITY"]="DERIVED_EXECUTION_GEOMETRY"; obj["OLEANDER_SURFACE_SOURCE"]="COUPLED_SEMANTIC_SURFACE_NETWORK"
    mod=obj.modifiers.new("Mirror-Symmetry","MIRROR"); mod.use_axis[0]=False; mod.use_axis[1]=True; mod.use_clip=True; mod.use_mirror_merge=True
    return obj,rows


def render_set(net:R3Network,out:Path,res:int,tag:str,full:bool):
    e2.clear_scene(); clay=e2.material(f"MAT-{tag}-CLAY",(.36,.38,.41),.30); zebra=e2.zebra_material()
    surface,rows=build_mesh(net); sc=e2.scene_setup(res); target=(0,0,.70)
    if full:
        cams={
            "HERO":e2.camera(f"CAM-{tag}-HERO",(4.5,4.7,2.8),target,6.0),
            "SIDE":e2.camera(f"CAM-{tag}-SIDE",(0,6.5,1.0),target,5.9),
            "TOP":e2.camera(f"CAM-{tag}-TOP",(0,.15,6.5),(0,0,.55),6.0),
            "ZEBRA":e2.camera(f"CAM-{tag}-ZEBRA",(4.5,4.25,2.45),target,5.9),
        }
        for name in ("HERO","SIDE","TOP"):
            e2.render(sc,out,cams[name],f"E3_R3_{name}",surface,clay)
        e2.render(sc,out,cams["ZEBRA"],"E3_R3_ZEBRA",surface,zebra)
    else:
        side=e2.camera(f"CAM-{tag}-SIDE",(0,6.5,1.0),target,5.9)
        top=e2.camera(f"CAM-{tag}-TOP",(0,.15,6.5),(0,0,.55),6.0)
        e2.render(sc,out,side,f"E3_R3_VARIANT_{tag}_SIDE",surface,clay)
        e2.render(sc,out,top,f"E3_R3_VARIANT_{tag}_TOP",surface,clay)
    return sc,len(rows)


def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--contract",required=True); ap.add_argument("--out",required=True); ap.add_argument("--resolution",type=int,default=512); args=ap.parse_args(user_args())
    contract=json.loads(Path(args.contract).read_text(encoding="utf-8")); out=Path(args.out).resolve(); out.mkdir(parents=True,exist_ok=True)
    base_report,base_net=evaluate(contract); th=contract["machine_thresholds"]

    variants={}; variants_ok=True; exact_ok=True; domain_ok=True
    base_src=source_snapshot(contract)
    for cid in contract["semantic_controls"]:
        vc,declared=apply_control(contract,cid); actual=changed_keys(contract,vc); vr,vnet=evaluate(vc); disp=max_displacement(base_net,vnet)
        exact=actual==declared
        vf=vr["checks"]["declared_boundary_relationships_pass"] and vr["checks"]["all_surface_family_interior_fairness_pass"] and vr["checks"]["profile_silhouette_metrics_pass"] and vr["checks"]["reflection_field_proxy_pass"]
        legible=th["min_semantic_surface_displacement"]<=disp<=th["max_semantic_surface_displacement"]
        has_plan=any(k[0]=="PLAN" for k in declared); has_profile=any(k[0]=="PROFILE" for k in declared); has_term=any(k[0]=="TERMINATION" for k in declared)
        domain_effect=True
        if has_plan:
            domain_effect=domain_effect and any(abs(vr["plan_metrics"][k]-base_report["plan_metrics"][k])>1e-4 for k in ("rear_haunch_plan_advantage","max_shoulder_width","max_rocker_width"))
        if has_profile:
            domain_effect=domain_effect and any(abs(float(vr["profile_metrics"][k])-float(base_report["profile_metrics"][k]))>1e-4 for k in ("front_hood_height","cabin_peak_height","max_profile_slope_change_proxy"))
        if has_term:
            domain_effect=domain_effect and disp>=th["min_semantic_surface_displacement"]
        variants[cid]={
            "declared_source_keys":[list(k) for k in sorted(declared,key=str)],
            "actual_changed_source_keys":[list(k) for k in sorted(actual,key=str)],
            "source_edit_exact":exact,
            "max_surface_displacement":disp,
            "working_fidelity_legible":legible,
            "declared_authority_domain_effect":domain_effect,
            "machine_surface_pass":vf,
            "profile_metrics":vr["profile_metrics"],
            "plan_metrics":vr["plan_metrics"],
            "reflection_field_acceleration_proxy":vr["reflection_field_acceleration_proxy"]
        }
        variants_ok=variants_ok and vf and legible; exact_ok=exact_ok and exact; domain_ok=domain_ok and domain_effect

    checks={**base_report["checks"],
        "semantic_source_edits_exact":exact_ok,
        "all_semantic_variants_surface_pass":variants_ok,
        "semantic_authority_domain_effects_present":domain_ok,
        "machine_pass_only_opens_human_review":True
    }
    status="MACHINE_PASS_HUMAN_PROJECT_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL_REVISE_E3_R3_ARCHITECTURE"
    report={
        "schema":"oleander.modeling-worker.v0.12.e3.r3.machine-report",
        "model":MODEL,
        "status":status,
        "decision_question":contract["decision_question"],
        "checks":checks,
        "base":base_report,
        "semantic_variants":variants,
        "boundary":"R3 Machine PASS validates only the benchmark Surface Source architecture, declared relationship proxies, interior fairness, source locality and working-fidelity edit effects. Human Project/Visual QA remains mandatory; no Class-A, engineering, production, PAP or Promotion authority is implied."
    }

    sc,row_count=render_set(base_net,out,args.resolution,"BASE",True)
    sc["OLEANDER_MODEL"]=MODEL; sc["OLEANDER_STAGE"]="E3_R3_APPLICATION_MACHINE"; sc["OLEANDER_AUTHORITY"]="WORKING_SURFACE_SOURCE"
    blend=out/f"{MODEL}.blend"; bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    for cid in contract["semantic_controls"]:
        vc,_=apply_control(contract,cid); _,vnet=evaluate(vc); render_set(vnet,out,args.resolution,cid.replace("-","_"),False)

    (out/"E3_R3_MACHINE_REPORT.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (out/"E3_R3_COMPILED_SURFACE_SOURCE.json").write_text(json.dumps({
        "schema":"oleander.modeling-worker.v0.12.e3.r3.compiled-surface-source",
        "authority":"WORKING_SURFACE_SOURCE",
        "profile_primary_curves":contract["profile_primary_curves"],
        "plan_primary_curves":contract["plan_primary_curves"],
        "surface_sources":contract["surface_sources"],
        "relationship_graph":contract["relationship_graph"],
        "execution_geometry":{"derived":True,"editable_authority":False,"sample_rows":row_count}
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if status=="MACHINE_PASS_HUMAN_PROJECT_VISUAL_REVIEW_REQUIRED" else 5


if __name__=="__main__":
    raise SystemExit(main())
