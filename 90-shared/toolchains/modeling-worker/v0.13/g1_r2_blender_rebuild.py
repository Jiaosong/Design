#!/usr/bin/env python3
"""Self-contained Blender Text Editor rebuild for OLEANDER v0.13 G1 R2.

Edit OL_SRC_* native source objects, then Run Script. The derived baseline mesh is rebuilt
from Blender-native Working Source objects. No repository Python modules are required.
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
    return {
        "grip": grip,
        "palm": [p[2] for p in pts(NAMES["PALM_PROFILE"])],
        "thumb": [p[1] for p in pts(NAMES["THUMB_SIDE_PLAN"])],
        "opposite": [-p[1] for p in pts(NAMES["OPPOSITE_SIDE_PLAN"])],
        "lower": [-p[2] for p in pts(NAMES["LOWER_RETURN_PROFILE"])],
        "deck": {k: float(deck[k]) for k in ("u_center","u_halfspan","theta_center_rad","theta_halfspan_rad","depth_m","core_fraction")},
        "termination_exponent": float(bpy.context.scene.get("OLEANDER_TERMINATION_ENVELOPE_EXPONENT", 0.34)),
    }


def rho(s, u, theta):
    d = s["deck"]
    return math.hypot((u-d["u_center"])/d["u_halfspan"], wrap(theta-d["theta_center_rad"])/d["theta_halfspan_rad"])


def point(s, u, theta):
    g = bezier(s["grip"], u)
    top = float(bezier(s["palm"], u)); th = float(bezier(s["thumb"], u)); op = float(bezier(s["opposite"], u)); lo = float(bezier(s["lower"], u))
    env = math.sin(math.pi*u)**s["termination_exponent"] if 0 < u < 1 else 0.0
    top*=env; th*=env; op*=env; lo*=env
    sn, cs = math.sin(theta), math.cos(theta)
    lateral = 0.5*(th+op) + 0.5*(th-op)*sn
    vertical = 0.5*(top+lo) + 0.5*(top-lo)*cs
    x, y, z = float(g[0]), float(g[1]) + lateral*sn, float(g[2]) + vertical*cs
    r = rho(s,u,theta); d = s["deck"]
    if r < 1.0:
        c = d["core_fraction"]
        mask = 1.0 if r <= c else smootherstep((1-r)/(1-c))
        z -= d["depth_m"] * mask
    return (x,y,z)


def mesh(s):
    nu = int(bpy.context.scene.get("OLEANDER_G1_R2_U_RINGS",56)); nv = int(bpy.context.scene.get("OLEANDER_G1_R2_CIRC_SAMPLES",72))
    verts = [point(s,0.0,0.0)]
    for i in range(1,nu+1):
        u = i/(nu+1)
        for j in range(nv): verts.append(point(s,u,2*math.pi*j/nv))
    back = len(verts); verts.append(point(s,1.0,0.0)); faces=[]
    for j in range(nv): faces.append((0,1+j,1+(j+1)%nv))
    for i in range(nu-1):
        a=1+i*nv; b=a+nv
        for j in range(nv):
            n=(j+1)%nv; faces.append((a+j,b+j,b+n,a+n))
    last=1+(nu-1)*nv
    for j in range(nv): faces.append((last+j,back,last+(j+1)%nv))
    return verts,faces


def rebuild():
    s=source(); verts,faces=mesh(s); old=bpy.data.objects.get(DERIVED); mats=[]; coll=None
    if old:
        mats=list(old.data.materials); coll=old.users_collection[0] if old.users_collection else None; data=old.data; bpy.data.objects.remove(old,do_unlink=True)
        if data.users==0: bpy.data.meshes.remove(data)
    if coll is None: coll=bpy.data.collections.get("OLEANDER_DERIVED_EXECUTION") or bpy.context.scene.collection
    me=bpy.data.meshes.new(DERIVED+"_MESH"); me.from_pydata(verts,[],faces); me.update(); obj=bpy.data.objects.new(DERIVED,me); coll.objects.link(obj)
    for p in me.polygons: p.use_smooth=True
    for m in mats: me.materials.append(m)
    obj["OLEANDER_AUTHORITY"]="DERIVED_EXECUTION_NOT_AUTHORITY"; obj["OLEANDER_EDITABLE"]=False; obj["OLEANDER_SOURCE_MODE"]="BLENDER_NATIVE_WORKING_SOURCE"
    live={"authority_state":"WORKING_SOURCE","source_mode":"BLENDER_NATIVE_WORKING_SOURCE","grip_axis":s["grip"],"palm_profile":s["palm"],"thumb_side_plan":s["thumb"],"opposite_side_plan":s["opposite"],"lower_return_profile":s["lower"],"interface_deck_boundary":s["deck"],"termination_envelope_exponent":s["termination_exponent"]}
    t=bpy.data.texts.get("OLEANDER_G1_R2_LIVE_SOURCE.json") or bpy.data.texts.new("OLEANDER_G1_R2_LIVE_SOURCE.json"); t.clear(); t.write(json.dumps(live,indent=2))
    bpy.context.scene["OLEANDER_LAST_NATIVE_REBUILD"]="PASS"
    print("OLEANDER_G1_R2_NATIVE_SOURCE_REBUILD_PASS",len(verts),len(faces))


if __name__ == "__main__": rebuild()
