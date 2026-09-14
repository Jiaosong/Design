#!/usr/bin/env python3
"""Self-contained Blender Text Editor rebuild for OLEANDER v0.13 G1 R2.

Edit OL_SRC_* native source objects, then Run Script. The derived baseline mesh is rebuilt
from Blender-native Working Source objects. No repository Python modules are required.
Locked relationship semantics remain fail-closed and do not become new source DOFs.
"""
from __future__ import annotations
import json
import math

import bpy

NAMES = {
    "GRIP_AXIS": "OL_SRC_GRIP_AXIS",
    "PALM_PROFILE": "OL_SRC_PALM_PROFILE",
    "THUMB_SIDE_PLAN": "OL_SRC_THUMB_SIDE_PLAN",
    "OPPOSITE_SIDE_PLAN": "OL_SRC_OPPOSITE_SIDE_PLAN",
    "LOWER_RETURN_PROFILE": "OL_SRC_LOWER_RETURN_PROFILE",
    "INTERFACE_DECK_BOUNDARY": "OL_SRC_INTERFACE_DECK_BOUNDARY",
}
DERIVED = "OL_DERIVED_G1_R2_BASELINE"
R451B_CONFIRM_DERIVED = "OL_DERIVED_G1_R4_5_1B_CONFIRM_SCALE_086"
CAP_LAW = "C2_MATCHED_ELLIPTIC_PARABOLOID_POLE"
CAP_SEMANTICS = "EXPLICIT_SPARSE_TERMINATION_CAP_RELATION"
CAP_ENDPOINT_SECTION = "SYMMETRIC_ELLIPSE_DERIVED_FROM_ONSET_MEANS"


def pts(name):
    return [tuple(float(v) for v in p.co[:3]) for p in bpy.data.objects[name].data.splines[0].points]


def bezier(values, u):
    n = len(values) - 1
    if isinstance(values[0], (list, tuple)):
        out = [0.0] * len(values[0])
        for i, p in enumerate(values):
            w = math.comb(n, i) * u**i * (1-u)**(n-i)
            for j, v in enumerate(p): out[j] += w * float(v)
        return out
    return sum(math.comb(n,i) * u**i * (1-u)**(n-i) * float(v) for i,v in enumerate(values))


def smootherstep(x):
    x = max(0.0, min(1.0, x))
    return x*x*x*(x*(x*6.0-15.0)+10.0)


def wrap(a): return (a + math.pi) % (2*math.pi) - math.pi


def source():
    grip = pts(NAMES["GRIP_AXIS"])
    deck = bpy.data.objects[NAMES["INTERFACE_DECK_BOUNDARY"]]
    lower_obj = bpy.data.objects[NAMES["LOWER_RETURN_PROFILE"]]
    theta = float(deck.get("theta_center_rad", 0.0))
    if bool(bpy.context.scene.get("OLEANDER_LOCKED_THETA_CENTER_TOP", True)):
        tol = float(bpy.context.scene.get("OLEANDER_NATIVE_READBACK_TOLERANCE_M", 1e-8))
        if abs(theta) > tol:
            raise RuntimeError("Locked INTERFACE_DECK_BOUNDARY.theta_center=TOP_MERIDIAN was modified; re-enter Relation / Surface Source to unlock it")
    out = {
        "grip": grip,
        "palm": [p[2] for p in pts(NAMES["PALM_PROFILE"])],
        "thumb": [p[1] for p in pts(NAMES["THUMB_SIDE_PLAN"])],
        "opposite": [-p[1] for p in pts(NAMES["OPPOSITE_SIDE_PLAN"])],
        "lower": [-p[2] for p in pts(NAMES["LOWER_RETURN_PROFILE"])],
        "deck": {
            "u_center":float(deck["u_center"]),"u_halfspan":float(deck["u_halfspan"]),"theta_center_rad":theta,
            "theta_halfspan_rad":float(deck["theta_halfspan_rad"]),"depth_m":float(deck["depth_m"]),"core_fraction":float(deck["core_fraction"])
        },
        "termination_exponent": float(lower_obj.get("termination_envelope_exponent", bpy.context.scene.get("OLEANDER_TERMINATION_ENVELOPE_EXPONENT", 0.34))),
    }
    if "termination_cap_onset_u" in lower_obj:
        onset = float(lower_obj["termination_cap_onset_u"])
        scale = float(lower_obj.get("termination_cap_pole_curvature_scale", 1.0))
        law = str(lower_obj.get("termination_cap_law", CAP_LAW))
        semantics = str(lower_obj.get("termination_cap_semantics", CAP_SEMANTICS))
        endpoint = str(lower_obj.get("termination_cap_endpoint_section", CAP_ENDPOINT_SECTION))
        if not 0.0 < onset < 1.0: raise RuntimeError("termination_cap_onset_u out of range")
        if not 0.25 <= scale <= 2.0: raise RuntimeError("termination_cap_pole_curvature_scale out of bounded range")
        if law != CAP_LAW or semantics != CAP_SEMANTICS or endpoint != CAP_ENDPOINT_SECTION:
            raise RuntimeError("Unsupported Blender-native termination cap semantics")
        out["termination_cap"] = {
            "onset_u": onset,
            "pole_curvature_scale": scale,
            "law": law,
            "semantics": semantics,
            "endpoint_section": endpoint,
        }
    return out


def rho(s, u, theta):
    d = s["deck"]
    return math.hypot((u-d["u_center"])/d["u_halfspan"], wrap(theta-d["theta_center_rad"])/d["theta_halfspan_rad"])


def bezier_scalar_triplet(values, u):
    n = len(values) - 1
    value = bezier(values, u)
    if n <= 0: return float(value), 0.0, 0.0
    d1_values = [n * (float(values[i+1]) - float(values[i])) for i in range(n)]
    d1 = bezier(d1_values, u)
    if n <= 1: return float(value), float(d1), 0.0
    d2_values = [(n-1) * (d1_values[i+1] - d1_values[i]) for i in range(n-1)]
    return float(value), float(d1), float(bezier(d2_values, u))


def envelope_triplet(s, u):
    exponent = float(s["termination_exponent"])
    if u <= 0.0 or u >= 1.0: return 0.0, 0.0, 0.0
    sn = math.sin(math.pi*u); cs = math.cos(math.pi*u)
    value = sn**exponent
    d1 = exponent * math.pi * cs * sn**(exponent-1.0)
    d2 = exponent * math.pi**2 * ((exponent-1.0)*cs*cs*sn**(exponent-2.0) - sn**exponent)
    return value, d1, d2


def profile_triplet(s, key, u):
    value, d1, d2 = bezier_scalar_triplet(s[key], u)
    env, env1, env2 = envelope_triplet(s, u)
    return value*env, d1*env + value*env1, d2*env + 2.0*d1*env1 + value*env2


def baseline_radial_triplet(s, u, theta):
    top = profile_triplet(s, "palm", u)
    thumb = profile_triplet(s, "thumb", u)
    opposite = profile_triplet(s, "opposite", u)
    lower = profile_triplet(s, "lower", u)
    sn, cs = math.sin(theta), math.cos(theta)
    def combine(a, b, trig): return tuple(0.5*(a[i]+b[i]) + 0.5*(a[i]-b[i])*trig for i in range(3))
    lateral = combine(thumb, opposite, sn); vertical = combine(top, lower, cs)
    value = (0.0, lateral[0]*sn, vertical[0]*cs)
    d1 = (0.0, lateral[1]*sn, vertical[1]*cs)
    d2 = (0.0, lateral[2]*sn, vertical[2]*cs)
    return value, d1, d2, top, thumb, opposite, lower


def vadd(a, b): return tuple(float(a[i]) + float(b[i]) for i in range(3))
def vscale(a, scale): return tuple(float(v) * float(scale) for v in a)


def quintic_zero_end_derivatives(t, y0, m0, k0, y1):
    a0=y0; a1=m0; a2=vscale(k0,0.5)
    a3=tuple(-1.5*k0[i]-6.0*m0[i]-10.0*y0[i]+10.0*y1[i] for i in range(3))
    a4=tuple(1.5*k0[i]+8.0*m0[i]+15.0*y0[i]-15.0*y1[i] for i in range(3))
    a5=tuple(-0.5*k0[i]-3.0*m0[i]-6.0*y0[i]+6.0*y1[i] for i in range(3))
    return tuple(a0[i]+a1[i]*t+a2[i]*t*t+a3[i]*t**3+a4[i]*t**4+a5[i]*t**5 for i in range(3))


def cap_radial(s, u, theta):
    baseline, _, _, _, _, _, _ = baseline_radial_triplet(s, u, theta)
    relation = s.get("termination_cap")
    if relation is None: return baseline
    onset = float(relation["onset_u"]); scale = float(relation["pole_curvature_scale"])
    if u <= onset: return baseline
    if u >= 1.0: return (0.0,0.0,0.0)
    length = 1.0-onset; tau=(u-onset)/length; q=math.sqrt(max(0.0,1.0-tau))
    h0, radial_u, radial_uu, top, thumb, opposite, lower = baseline_radial_triplet(s,onset,theta)
    h1=vadd(vscale(radial_u,length),vscale(h0,0.5))
    h2=vadd(vscale(radial_uu,length*length),vadd(vscale(h0,0.25),h1))
    side=0.5*(thumb[0]+opposite[0])*scale; vertical=0.5*(top[0]+lower[0])*scale
    hend=(0.0,side*math.sin(theta),vertical*math.cos(theta))
    return vscale(quintic_zero_end_derivatives(tau,h0,h1,h2,hend),q)


def point(s, u, theta):
    g = bezier(s["grip"], u)
    radial = cap_radial(s,u,theta)
    x, y, z = float(g[0])+radial[0], float(g[1])+radial[1], float(g[2])+radial[2]
    r = rho(s,u,theta); d = s["deck"]
    if r < 1.0:
        c = d["core_fraction"]
        mask = 1.0 if r <= c else smootherstep((1-r)/(1-c))
        z -= d["depth_m"] * mask
    return (x,y,z)


def u_values(s):
    nu=int(bpy.context.scene.get("OLEANDER_G1_R2_U_RINGS",56))
    values=[i/(nu+1) for i in range(1,nu+1)]
    relation=s.get("termination_cap")
    if relation is not None:
        onset=float(relation["onset_u"])
        for tau in (0.25,0.50,0.70,0.82,0.90,0.95,0.975,0.99,0.995): values.append(onset+(1.0-onset)*tau)
    return sorted(set(v for v in values if 0.0 < v < 1.0))


def mesh(s):
    uv=u_values(s); nv = int(bpy.context.scene.get("OLEANDER_G1_R2_CIRC_SAMPLES",72))
    verts = [point(s,0.0,0.0)]
    for u in uv:
        for j in range(nv): verts.append(point(s,u,2*math.pi*j/nv))
    back = len(verts); verts.append(point(s,1.0,0.0)); faces=[]
    for j in range(nv): faces.append((0,1+j,1+(j+1)%nv))
    for i in range(len(uv)-1):
        a=1+i*nv; b=a+nv
        for j in range(nv):
            n=(j+1)%nv; faces.append((a+j,b+j,b+n,a+n))
    last=1+(len(uv)-1)*nv
    for j in range(nv): faces.append((last+j,back,last+(j+1)%nv))
    return verts,faces


def derived_name():
    if bpy.context.scene.get("OLEANDER_STAGE") == "R4_5_1B_EXACT_SCALE_086_CONFIRMATION":
        return R451B_CONFIRM_DERIVED
    return DERIVED


def rebuild():
    s=source(); verts,faces=mesh(s); target=derived_name(); old=bpy.data.objects.get(target); mats=[]; coll=None
    if old:
        mats=list(old.data.materials); coll=old.users_collection[0] if old.users_collection else None; data=old.data; bpy.data.objects.remove(old,do_unlink=True)
        if data.users==0: bpy.data.meshes.remove(data)
    if coll is None: coll=bpy.data.collections.get("OLEANDER_DERIVED_EXECUTION") or bpy.context.scene.collection
    me=bpy.data.meshes.new(target+"_MESH"); me.from_pydata(verts,[],faces); me.update(); obj=bpy.data.objects.new(target,me); coll.objects.link(obj)
    for p in me.polygons: p.use_smooth=True
    for m in mats: me.materials.append(m)
    obj["OLEANDER_AUTHORITY"]="DERIVED_EXECUTION_NOT_AUTHORITY"; obj["OLEANDER_EDITABLE"]=False; obj["OLEANDER_SOURCE_MODE"]="BLENDER_NATIVE_WORKING_SOURCE"
    live={"authority_state":"WORKING_SOURCE","source_mode":"BLENDER_NATIVE_WORKING_SOURCE","locked_semantics":{"interface_theta_center":"TOP_MERIDIAN"},"grip_axis":s["grip"],"palm_profile":s["palm"],"thumb_side_plan":s["thumb"],"opposite_side_plan":s["opposite"],"lower_return_profile":s["lower"],"interface_deck_boundary":s["deck"],"termination_envelope_exponent":s["termination_exponent"],"termination_cap":s.get("termination_cap")}
    t=bpy.data.texts.get("OLEANDER_G1_R2_LIVE_SOURCE.json") or bpy.data.texts.new("OLEANDER_G1_R2_LIVE_SOURCE.json"); t.clear(); t.write(json.dumps(live,indent=2))
    bpy.context.scene["OLEANDER_LAST_NATIVE_REBUILD"]="PASS"; bpy.context.scene["OLEANDER_LAST_NATIVE_REBUILD_CAP_AWARE"]=s.get("termination_cap") is not None
    print("OLEANDER_G1_R2_NATIVE_SOURCE_REBUILD_PASS",target,len(verts),len(faces),"CAP_AWARE",s.get("termination_cap") is not None)


if __name__ == "__main__": rebuild()
