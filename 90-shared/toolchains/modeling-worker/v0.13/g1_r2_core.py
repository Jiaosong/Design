#!/usr/bin/env python3
from __future__ import annotations

import copy
import math

import g1_geometry_core as base

CAP_LAW = "C2_MATCHED_ELLIPTIC_PARABOLOID_POLE"
CAP_SEMANTICS = "EXPLICIT_SPARSE_TERMINATION_CAP_RELATION"
CAP_ENDPOINT_SECTION = "SYMMETRIC_ELLIPSE_DERIVED_FROM_ONSET_MEANS"


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def apply(src, fix):
    out = copy.deepcopy(src)
    for fam, ov in fix["source_overrides"].items():
        item = {"role": out["ownership"][fam]["role"], "editable": out["ownership"][fam]["editable"]}
        item.update(copy.deepcopy(ov))
        out["ownership"][fam] = item
    out["revision"] = "G1-R2"
    return out


def center(d):
    return 0.0 if d.get("theta_center") == "TOP_MERIDIAN" else float(d.get("theta_center_rad", 0.0))


def rho(s, u, t):
    d = base.own(s, "INTERFACE_DECK_BOUNDARY")
    return math.hypot(
        (u - float(d["u_center"])) / float(d["u_halfspan"]),
        wrap(t - center(d)) / float(d["theta_halfspan_rad"]),
    )


def _bezier_scalar_triplet(values, u):
    vals = [float(v) for v in values]
    n = len(vals) - 1
    value = float(base.bezier(vals, u))
    if n <= 0:
        return value, 0.0, 0.0
    d1_cp = [n * (vals[i + 1] - vals[i]) for i in range(n)]
    d1 = float(base.bezier(d1_cp, u))
    if n <= 1:
        return value, d1, 0.0
    d2_cp = [(n - 1) * (d1_cp[i + 1] - d1_cp[i]) for i in range(n - 1)]
    d2 = float(base.bezier(d2_cp, u))
    return value, d1, d2


def _base_envelope_triplet(s, u):
    exponent = float(base.own(s, "LOWER_RETURN_PROFILE").get("termination_envelope_exponent", 0.55))
    if not 0.0 < u < 1.0:
        return 0.0, 0.0, 0.0
    sn = math.sin(math.pi * u)
    cs = math.cos(math.pi * u)
    value = sn**exponent
    d1 = exponent * math.pi * cs * sn ** (exponent - 1.0)
    d2 = exponent * math.pi**2 * ((exponent - 1.0) * cs * cs * sn ** (exponent - 2.0) - sn**exponent)
    return value, d1, d2


def _revision_triplet(u):
    sn = math.sin(math.pi * u)
    cs = math.cos(math.pi * u)
    value = 1.0 + 0.12 * sn * sn
    d1 = 0.24 * math.pi * sn * cs
    d2 = 0.24 * math.pi**2 * (cs * cs - sn * sn)
    return value, d1, d2


def _profile_radius_triplet(s, family, u, revision=False):
    value, d1, d2 = _bezier_scalar_triplet(base.own(s, family)["control_values"], u)
    if revision and family == "THUMB_SIDE_PLAN":
        m, m1, m2 = _revision_triplet(u)
        value, d1, d2 = value * m, d1 * m + value * m1, d2 * m + 2.0 * d1 * m1 + value * m2
    env, env1, env2 = _base_envelope_triplet(s, u)
    return (
        value * env,
        d1 * env + value * env1,
        d2 * env + 2.0 * d1 * env1 + value * env2,
    )


def _baseline_radial_triplet(s, u, t, revision=False):
    top = _profile_radius_triplet(s, "PALM_PROFILE", u, revision)
    thumb = _profile_radius_triplet(s, "THUMB_SIDE_PLAN", u, revision)
    opposite = _profile_radius_triplet(s, "OPPOSITE_SIDE_PLAN", u, revision)
    lower = _profile_radius_triplet(s, "LOWER_RETURN_PROFILE", u, revision)
    sn = math.sin(t)
    cs = math.cos(t)

    def combine(a, b, trig):
        return tuple(0.5 * (a[i] + b[i]) + 0.5 * (a[i] - b[i]) * trig for i in range(3))

    lateral = combine(thumb, opposite, sn)
    vertical = combine(top, lower, cs)
    value = (0.0, lateral[0] * sn, vertical[0] * cs)
    d1 = (0.0, lateral[1] * sn, vertical[1] * cs)
    d2 = (0.0, lateral[2] * sn, vertical[2] * cs)
    return value, d1, d2, top, thumb, opposite, lower


def _cap_relation(s):
    lower = base.own(s, "LOWER_RETURN_PROFILE")
    if "termination_cap_onset_u" not in lower:
        return None
    onset = float(lower["termination_cap_onset_u"])
    law = str(lower.get("termination_cap_law", CAP_LAW))
    semantics = str(lower.get("termination_cap_semantics", CAP_SEMANTICS))
    endpoint = str(lower.get("termination_cap_endpoint_section", CAP_ENDPOINT_SECTION))
    if law != CAP_LAW:
        raise ValueError(f"Unsupported termination cap law: {law}")
    if semantics != CAP_SEMANTICS:
        raise ValueError(f"Unsupported termination cap semantics: {semantics}")
    if endpoint != CAP_ENDPOINT_SECTION:
        raise ValueError(f"Unsupported termination cap endpoint section: {endpoint}")
    if not 0.0 < onset < 1.0:
        raise ValueError(f"termination_cap_onset_u out of range: {onset}")
    return onset


def _vadd(a, b):
    return tuple(float(a[i]) + float(b[i]) for i in range(3))


def _vscale(a, scale):
    return tuple(float(v) * float(scale) for v in a)


def _quintic_hermite_zero_end_derivatives(t, y0, m0, k0, y1):
    a0 = y0
    a1 = m0
    a2 = _vscale(k0, 0.5)
    a3 = tuple(-1.5 * k0[i] - 6.0 * m0[i] - 10.0 * y0[i] + 10.0 * y1[i] for i in range(3))
    a4 = tuple(1.5 * k0[i] + 8.0 * m0[i] + 15.0 * y0[i] - 15.0 * y1[i] for i in range(3))
    a5 = tuple(-0.5 * k0[i] - 3.0 * m0[i] - 6.0 * y0[i] + 6.0 * y1[i] for i in range(3))
    return tuple(
        a0[i] + a1[i] * t + a2[i] * t * t + a3[i] * t**3 + a4[i] * t**4 + a5[i] * t**5
        for i in range(3)
    )


def _cap_radial(s, u, t, revision=False):
    baseline, _, _, _, _, _, _ = _baseline_radial_triplet(s, u, t, revision)
    onset = _cap_relation(s)
    if onset is None or u <= onset:
        return baseline
    if u >= 1.0:
        return (0.0, 0.0, 0.0)

    length = 1.0 - onset
    tau = (u - onset) / length
    q = math.sqrt(max(0.0, 1.0 - tau))
    h0, radial_u, radial_uu, top, thumb, opposite, lower = _baseline_radial_triplet(s, onset, t, revision)
    h1_s = _vadd(_vscale(radial_u, length), _vscale(h0, 0.5))
    h2_s = _vadd(_vscale(radial_uu, length * length), _vadd(_vscale(h0, 0.25), h1_s))

    side_radius = 0.5 * (thumb[0] + opposite[0])
    vertical_radius = 0.5 * (top[0] + lower[0])
    h_end = (0.0, side_radius * math.sin(t), vertical_radius * math.cos(t))
    h = _quintic_hermite_zero_end_derivatives(tau, h0, h1_s, h2_s, h_end)
    return _vscale(h, q)


def point(s, u, t, revision=False, deck=True):
    g = base.bezier(base.own(s, "GRIP_AXIS")["control_points"], u)
    radial = _cap_radial(s, u, t, revision)
    x = float(g[0]) + radial[0]
    y = float(g[1]) + radial[1]
    z = float(g[2]) + radial[2]
    if deck:
        d = base.own(s, "INTERFACE_DECK_BOUNDARY")
        r = rho(s, u, t)
        if r < 1:
            c = float(d["core_fraction"])
            mask = 1.0 if r <= c else base.smootherstep((1 - r) / (1 - c))
            z -= float(d["depth_m"]) * mask
    return (x, y, z)


def _u_values(s):
    nu = int(s["derived_execution"]["u_rings"])
    values = [i / (nu + 1) for i in range(1, nu + 1)]
    onset = _cap_relation(s)
    if onset is not None:
        for tau in (0.25, 0.50, 0.70, 0.82, 0.90, 0.95, 0.975, 0.99, 0.995):
            values.append(onset + (1.0 - onset) * tau)
    return sorted(set(v for v in values if 0.0 < v < 1.0))


def mesh(s, revision=False):
    nv = int(s["derived_execution"]["circumferential_samples"])
    u_values = _u_values(s)
    v = [point(s, 0, 0, revision)]
    faces = []
    labels = []
    for u in u_values:
        for j in range(nv):
            v.append(point(s, u, 2 * math.pi * j / nv, revision))
    back = len(v)
    v.append(point(s, 1, 0, revision))
    for j in range(nv):
        faces.append((0, 1 + j, 1 + (j + 1) % nv))
        labels.append("BODY")
    for i in range(len(u_values) - 1):
        a = 1 + i * nv
        b = a + nv
        um = 0.5 * (u_values[i] + u_values[i + 1])
        for j in range(nv):
            n = (j + 1) % nv
            tm = 2 * math.pi * (j + 0.5) / nv
            faces.append((a + j, b + j, b + n, a + n))
            labels.append("DECK" if rho(s, um, tm) < 1 else "BODY")
    last = 1 + (len(u_values) - 1) * nv
    for j in range(nv):
        faces.append((last + j, back, last + (j + 1) % nv))
        labels.append("BODY")
    return v, faces, labels
