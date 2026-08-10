# -*- coding: utf-8 -*-
"""
OLEANDER / 织作 — SP04-R02 Interoperability & Topology QA
Pure Python + trimesh. No Revit required.

Builds a single connected wall-with-opening mesh from a parameter grid,
exports OBJ/STL/GLB, reloads each format, and checks:
watertightness, winding consistency, body count, analytical volume, bounding box.

All dimensions are TRAINING-ONLY HYPOTHETICAL PARAMETERS.
"""
from pathlib import Path
import json, csv
import numpy as np
import trimesh

WALL = {"length_mm":6000.0, "height_mm":3300.0, "thickness_mm":240.0}
TESTS = [
    {"id":"T01","width_mm":900.0,"height_mm":2100.0,"sill_mm":0.0},
    {"id":"T02","width_mm":1200.0,"height_mm":2100.0,"sill_mm":0.0},
    {"id":"T03","width_mm":1500.0,"height_mm":2400.0,"sill_mm":450.0},
    {"id":"T04","width_mm":1800.0,"height_mm":2400.0,"sill_mm":900.0},
    {"id":"T05","width_mm":750.0,"height_mm":1800.0,"sill_mm":300.0},
]
TOL_VOL_REL=1e-9
TOL_BBOX_MM=1e-6

def add_vertex(vmap, verts, p):
    key=tuple(round(float(x),9) for x in p)
    if key not in vmap:
        vmap[key]=len(verts); verts.append(key)
    return vmap[key]

def add_quad(vmap, verts, faces, a,b,c,d):
    idx=[add_vertex(vmap,verts,p) for p in (a,b,c,d)]
    faces.extend([[idx[0],idx[1],idx[2]],[idx[0],idx[2],idx[3]]])

def make_wall_mesh(t):
    L,H,T=WALL["length_mm"],WALL["height_mm"],WALL["thickness_mm"]
    x0=(L-t["width_mm"])/2.0; x1=x0+t["width_mm"]
    z0=t["sill_mm"]; z1=z0+t["height_mm"]
    if x0<0 or x1>L or z0<0 or z1>H:
        raise ValueError(t["id"]+" opening exceeds host")
    xs=sorted(set([0.0,x0,x1,L])); zs=sorted(set([0.0,z0,z1,H]))
    occ={}
    for i in range(len(xs)-1):
        for k in range(len(zs)-1):
            xa,xb=xs[i],xs[i+1]; za,zb=zs[k],zs[k+1]
            if xb-xa<=1e-9 or zb-za<=1e-9: continue
            cx=(xa+xb)/2.0; cz=(za+zb)/2.0
            occ[(i,k)]=not ((x0<cx<x1) and (z0<cz<z1))
    verts=[]; faces=[]; vmap={}; y0=0.0; y1=T
    for (i,k),filled in occ.items():
        if not filled: continue
        xa,xb=xs[i],xs[i+1]; za,zb=zs[k],zs[k+1]
        add_quad(vmap,verts,faces,(xa,y0,za),(xa,y0,zb),(xb,y0,zb),(xb,y0,za))
        add_quad(vmap,verts,faces,(xa,y1,za),(xb,y1,za),(xb,y1,zb),(xa,y1,zb))
        if not occ.get((i-1,k),False):
            add_quad(vmap,verts,faces,(xa,y0,za),(xa,y1,za),(xa,y1,zb),(xa,y0,zb))
        if not occ.get((i+1,k),False):
            add_quad(vmap,verts,faces,(xb,y0,za),(xb,y0,zb),(xb,y1,zb),(xb,y1,za))
        if not occ.get((i,k-1),False):
            add_quad(vmap,verts,faces,(xa,y0,za),(xb,y0,za),(xb,y1,za),(xa,y1,za))
        if not occ.get((i,k+1),False):
            add_quad(vmap,verts,faces,(xa,y0,zb),(xa,y1,zb),(xb,y1,zb),(xb,y0,zb))
    mesh=trimesh.Trimesh(vertices=np.array(verts,float),faces=np.array(faces,int),process=True)
    mesh.remove_unreferenced_vertices()
    if mesh.volume<0:
        mesh.invert()
    return mesh,{"x0":x0,"x1":x1,"z0":z0,"z1":z1}

def loaded_mesh(path):
    x=trimesh.load(path,process=True)
    if isinstance(x,trimesh.Scene):
        return trimesh.util.concatenate([g for g in x.geometry.values() if isinstance(g,trimesh.Trimesh)])
    return x

def metrics(mesh):
    return {
        "vertices":int(len(mesh.vertices)),
        "faces":int(len(mesh.faces)),
        "watertight":bool(mesh.is_watertight),
        "winding_consistent":bool(mesh.is_winding_consistent),
        "euler_number":int(mesh.euler_number),
        "body_count":int(mesh.body_count),
        "volume_mm3":float(mesh.volume),
        "bounds_mm":np.asarray(mesh.bounds).round(9).tolist(),
        "extents_mm":np.asarray(mesh.extents).round(9).tolist(),
    }

def expected_volume(t):
    return (WALL["length_mm"]*WALL["height_mm"]-t["width_mm"]*t["height_mm"])*WALL["thickness_mm"]

def run(outdir):
    outdir=Path(outdir)
    for d in ["models/obj","models/stl","models/glb","data"]:
        (outdir/d).mkdir(parents=True,exist_ok=True)
    results=[]
    for t in TESTS:
        mesh,opening=make_wall_mesh(t)
        paths={
            "obj":outdir/"models/obj"/f"{t['id']}_wall_opening_mm.obj",
            "stl":outdir/"models/stl"/f"{t['id']}_wall_opening_mm.stl",
            "glb":outdir/"models/glb"/f"{t['id']}_wall_opening_mm.glb",
        }
        for p in paths.values(): mesh.export(p)
        native=metrics(mesh); target=expected_volume(t)
        native_err=abs(native["volume_mm3"]-target)/target
        roundtrip={}
        for ext,p in paths.items():
            m=metrics(loaded_mesh(p))
            vol_err=abs(m["volume_mm3"]-target)/target
            bbox_delta=float(np.max(np.abs(np.asarray(m["bounds_mm"])-np.asarray(native["bounds_mm"]))))
            roundtrip[ext]={**m,"volume_rel_error_vs_expected":vol_err,
                            "bbox_max_delta_vs_native_mm":bbox_delta,
                            "pass":bool(m["watertight"] and m["winding_consistent"] and m["body_count"]==1
                                        and vol_err<=TOL_VOL_REL and bbox_delta<=TOL_BBOX_MM)}
        checks={
            "native_watertight":native["watertight"],
            "native_winding_consistent":native["winding_consistent"],
            "native_one_body":native["body_count"]==1,
            "native_expected_volume":native_err<=TOL_VOL_REL,
            "obj_roundtrip":roundtrip["obj"]["pass"],
            "stl_roundtrip":roundtrip["stl"]["pass"],
            "glb_roundtrip":roundtrip["glb"]["pass"],
        }
        results.append({"id":t["id"],"parameters":t,"opening_bounds_mm":opening,
                        "expected_volume_mm3":target,
                        "native":{**native,"volume_rel_error_vs_expected":native_err},
                        "roundtrip":roundtrip,"checks":checks,"pass":all(checks.values())})
    (outdir/"data/parameters.json").write_text(json.dumps({
        "status":"TRAINING-ONLY HYPOTHETICAL PARAMETERS","wall":WALL,"tests":TESTS,
        "tolerances":{"volume_relative":TOL_VOL_REL,"bbox_mm":TOL_BBOX_MM}},
        ensure_ascii=False,indent=2),encoding="utf-8")
    (outdir/"data/interoperability_qa.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
    with (outdir/"data/interoperability_qa.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["id","native_watertight","body_count","native_volume_mm3","obj_pass","stl_pass","glb_pass","overall_pass"])
        for r in results:
            w.writerow([r["id"],r["native"]["watertight"],r["native"]["body_count"],r["native"]["volume_mm3"],
                        r["roundtrip"]["obj"]["pass"],r["roundtrip"]["stl"]["pass"],r["roundtrip"]["glb"]["pass"],r["pass"]])
    return results

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("output",nargs="?",default="SP04_R02_reproduced")
    args=ap.parse_args()
    r=run(args.output)
    print("variants:",len(r))
    print("roundtrip_pass:",sum(x["roundtrip"][f]["pass"] for x in r for f in ("obj","stl","glb")),"/ 15")
    print("overall:",all(x["pass"] for x in r))
