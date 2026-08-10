# -*- coding: utf-8 -*-
"""
OLEANDER / 织作 — SP04-R03 Geometry Stress Test
Software-neutral. Requires: numpy, shapely, trimesh.

All dimensions are TRAINING-ONLY HYPOTHETICAL PARAMETERS.
"""
from pathlib import Path
import json, csv, math
import numpy as np
import trimesh
from shapely.geometry import Polygon, box, Point
from shapely.ops import triangulate, unary_union
from shapely.validation import explain_validity

WALL={"length_mm":6000.0,"height_mm":3300.0,"thickness_mm":240.0}
MIN_LIGAMENT_RULE_MM=50.0
MIN_GAP_RULE_MM=100.0
VOL_REL_TOL=2e-6
BBOX_TOL_MM=0.01

def rounded_rect(cx,sill,width,height,radius,resolution=24):
    if width<=0 or height<=0: raise ValueError("width/height must be > 0")
    if radius<=0: raise ValueError("radius must be > 0")
    if radius>min(width,height)/2: raise ValueError("radius exceeds half of minimum opening dimension")
    x0,x1=cx-width/2,cx+width/2; z0,z1=sill,sill+height
    return box(x0+radius,z0+radius,x1-radius,z1-radius).buffer(radius,resolution=resolution,join_style=1)

def arch(cx,sill,width,rect_height,radius=None,segments=48):
    if width<=0 or rect_height<=0: raise ValueError("width and rect_height must be > 0")
    r=width/2 if radius is None else radius
    if r<=0: raise ValueError("radius must be > 0")
    if abs(r-width/2)>1e-9: raise ValueError("current arch generator requires radius = width/2")
    x0,x1=cx-width/2,cx+width/2; spring=sill+rect_height
    pts=[(x0,sill),(x1,sill),(x1,spring)]
    for i in range(segments+1):
        th=i*math.pi/segments
        pts.append((cx+r*math.cos(th),spring+r*math.sin(th)))
    pts.append((x0,spring))
    return Polygon(pts)

def ellipse(cx,cz,rx,rz,resolution=64):
    if rx<=0 or rz<=0: raise ValueError("ellipse radii must be > 0")
    return Polygon([(cx+rx*math.cos(2*math.pi*i/resolution),cz+rz*math.sin(2*math.pi*i/resolution)) for i in range(resolution)])

def circle(cx,cz,r,resolution=48):
    if r<=0: raise ValueError("circle radius must be > 0")
    return Point(cx,cz).buffer(r,resolution=resolution)

def preflight(openings,require_rules=True):
    wall2d=box(0,0,WALL["length_mm"],WALL["height_mm"])
    if not openings: return {"valid":False,"reason":"no openings"}
    for i,o in enumerate(openings):
        if not o.is_valid: return {"valid":False,"reason":"opening %d invalid: %s"%(i,explain_validity(o))}
        if o.area<=0: return {"valid":False,"reason":"opening %d non-positive area"%i}
        if not wall2d.contains(o): return {"valid":False,"reason":"opening %d is not strictly inside host"%i}
    min_lig=min(o.boundary.distance(wall2d.boundary) for o in openings)
    gaps=[openings[i].distance(openings[j]) for i in range(len(openings)) for j in range(i+1,len(openings))]
    min_gap=min(gaps) if gaps else float("inf")
    if require_rules and min_lig<MIN_LIGAMENT_RULE_MM:
        return {"valid":False,"reason":"minimum host ligament %.9g mm < rule %.3f mm"%(min_lig,MIN_LIGAMENT_RULE_MM)}
    if require_rules and min_gap<MIN_GAP_RULE_MM:
        return {"valid":False,"reason":"minimum opening gap %.9g mm < rule %.3f mm"%(min_gap,MIN_GAP_RULE_MM)}
    return {"valid":True,"reason":"OK","min_ligament_mm":min_lig,"min_gap_mm":min_gap}

def _addv(vmap,verts,p):
    key=tuple(round(float(x),9) for x in p)
    if key not in vmap: vmap[key]=len(verts); verts.append(key)
    return vmap[key]

def _quad(vmap,verts,faces,a,b,c,d):
    q=[_addv(vmap,verts,p) for p in (a,b,c,d)]
    faces.extend([[q[0],q[1],q[2]],[q[0],q[2],q[3]]])

def polygon_to_mesh(poly,depth):
    if poly.geom_type!="Polygon": raise ValueError("expected Polygon, got "+poly.geom_type)
    verts=[]; faces=[]; vmap={}
    for tr in triangulate(poly):
        inter=tr.intersection(poly)
        if abs(inter.area-tr.area)<=max(1e-7,tr.area*1e-9):
            c=list(tr.exterior.coords)[:3]
            b=[_addv(vmap,verts,(x,0.0,z)) for x,z in c]
            t=[_addv(vmap,verts,(x,depth,z)) for x,z in c]
            faces.extend([[b[0],b[2],b[1]],[t[0],t[1],t[2]]])
    for ring in [poly.exterior]+list(poly.interiors):
        c=list(ring.coords)
        for (x0,z0),(x1,z1) in zip(c[:-1],c[1:]):
            _quad(vmap,verts,faces,(x0,0,z0),(x1,0,z1),(x1,depth,z1),(x0,depth,z0))
    mesh=trimesh.Trimesh(vertices=np.asarray(verts,float),faces=np.asarray(faces,int),process=True)
    mesh.remove_unreferenced_vertices()
    trimesh.repair.fix_normals(mesh,multibody=True)
    if mesh.volume<0: mesh.invert()
    return mesh

def build(openings):
    wall2d=box(0,0,WALL["length_mm"],WALL["height_mm"])
    solid=wall2d.difference(unary_union(openings))
    return polygon_to_mesh(solid,WALL["thickness_mm"]),solid

def load_mesh(path):
    x=trimesh.load(path,process=True)
    if isinstance(x,trimesh.Scene):
        x=trimesh.util.concatenate([g for g in x.geometry.values() if isinstance(g,trimesh.Trimesh)])
    trimesh.repair.fix_normals(x,multibody=True)
    if x.volume<0: x.invert()
    return x

def base_metrics(m):
    return {"watertight":bool(m.is_watertight),"winding_consistent":bool(m.is_winding_consistent),"body_count":int(m.body_count),"volume_mm3":float(m.volume),"bounds_mm":np.asarray(m.bounds).tolist()}

def export_roundtrip(case_id,mesh,solid,outdir,kind="cases"):
    expected=solid.area*WALL["thickness_mm"]; native=base_metrics(mesh); out={}
    for ext in ("obj","stl","glb"):
        folder=outdir/"models"/kind/ext if kind=="cases" else outdir/"models"/kind
        folder.mkdir(parents=True,exist_ok=True)
        p=folder/(case_id+"."+ext); mesh.export(p)
        m=load_mesh(p); met=base_metrics(m)
        verr=abs(met["volume_mm3"]-expected)/expected
        bdel=float(np.max(np.abs(np.asarray(met["bounds_mm"])-np.asarray(native["bounds_mm"]))))
        out[ext]={**met,"volume_rel_error":verr,"bbox_delta_mm":bdel,"base_pass":bool(met["watertight"] and met["winding_consistent"] and met["body_count"]==1 and verr<=VOL_REL_TOL and bdel<=BBOX_TOL_MM),"path":str(p.relative_to(outdir))}
    return native,out

def recovered_top_ligament(path):
    m=load_mesh(path); zs=np.asarray(m.vertices)[:,2]; H=WALL["height_mm"]; d=(H-zs); d=d[d>1e-12]
    return float(d.min()) if len(d) else 0.0

def recovered_center_gap(path):
    m=load_mesh(path); xs=np.asarray(m.vertices)[:,0]; c=WALL["length_mm"]/2
    lo=xs[xs<c-1e-12]; hi=xs[xs>c+1e-12]
    return float(hi.min()-lo.max()) if len(lo) and len(hi) else 0.0

def fidelity_ok(recovered,target):
    return recovered>0 and abs(recovered-target)<=max(1e-6,abs(target)*0.25)

def run(outdir):
    outdir=Path(outdir); (outdir/"data").mkdir(parents=True,exist_ok=True)
    shape_specs=[
      ("S01_ROUNDED",[rounded_rect(3000,300,1600,2200,260)]),
      ("S02_ARCH",[arch(3000,200,1400,1500)]),
      ("S03_ECCENTRIC",[ellipse(4500,1650,620,900)]),
      ("S04_MULTI",[circle(1900,1700,500),arch(3200,500,900,1000),ellipse(4550,1750,450,650)])]
    shapes=[]
    for cid,ops in shape_specs:
        pf=preflight(ops,True)
        if not pf["valid"]: shapes.append({"id":cid,"pass":False,"preflight":pf}); continue
        mesh,solid=build(ops); native,rt=export_roundtrip(cid,mesh,solid,outdir,"cases")
        shapes.append({"id":cid,"pass":all(x["base_pass"] for x in rt.values()) and native["watertight"],"preflight":pf,"native":native,"roundtrip":rt})
    thin_values=[200,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01,0.005,0.002,0.001,0.0005,0.0002,0.0001,0.00005,0.00002,0.00001]
    thin=[]
    for lig in thin_values:
        op=rounded_rect(3000,WALL["height_mm"]-lig-2000,1800,2000,250)
        mesh,solid=build([op]); cid=("THIN_%gmm"%lig).replace(".","p"); native,rt=export_roundtrip(cid,mesh,solid,outdir,"stress")
        row={"ligament_mm":lig,"native_watertight":native["watertight"]}
        for ext in ("obj","stl","glb"):
            p=outdir/rt[ext]["path"]; rec=recovered_top_ligament(p)
            row[ext+"_base_pass"]=rt[ext]["base_pass"]; row[ext+"_recovered_ligament_mm"]=rec; row[ext+"_feature_fidelity"]=fidelity_ok(rec,lig)
        row["overall_pass"]=all(row[e+"_base_pass"] and row[e+"_feature_fidelity"] for e in ("obj","stl","glb")); thin.append(row)
    gap_values=[300,200,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01,0.005,0.002,0.001,0.0005,0.0002,0.0001,0.00005,0.00002,0.00001]
    gaps=[]; r=600
    for gap in gap_values:
        ops=[circle(3000-r-gap/2,1650,r),circle(3000+r+gap/2,1650,r)]
        mesh,solid=build(ops); cid=("GAP_%gmm"%gap).replace(".","p"); native,rt=export_roundtrip(cid,mesh,solid,outdir,"stress")
        row={"gap_mm":gap,"native_watertight":native["watertight"]}
        for ext in ("obj","stl","glb"):
            p=outdir/rt[ext]["path"]; rec=recovered_center_gap(p)
            row[ext+"_base_pass"]=rt[ext]["base_pass"]; row[ext+"_recovered_gap_mm"]=rec; row[ext+"_feature_fidelity"]=fidelity_ok(rec,gap)
        row["overall_pass"]=all(row[e+"_base_pass"] and row[e+"_feature_fidelity"] for e in ("obj","stl","glb")); gaps.append(row)
    invalid=[("I01_NEGATIVE_SILL",lambda: rounded_rect(3000,-100,1400,1800,200)),("I02_RADIUS_TOO_LARGE",lambda: rounded_rect(3000,300,1000,1200,600)),("I03_ARCH_RADIUS_MISMATCH",lambda: arch(3000,300,1400,1200,500)),("I04_OUTSIDE_HOST",lambda: ellipse(5850,1700,400,700)),("I05_MULTI_OVERLAP",lambda: [circle(2800,1700,650),circle(3700,1700,650)]),("I06_ZERO_WIDTH",lambda: rounded_rect(3000,300,0,1000,100))]
    invalid_results=[]
    for cid,builder in invalid:
        rejected=False; reason=""
        try:
            b=builder(); ops=b if isinstance(b,list) else [b]; pf=preflight(ops,True)
            if not pf["valid"]: rejected=True; reason=pf["reason"]
            elif len(ops)>1 and any(ops[i].intersects(ops[j]) for i in range(len(ops)) for j in range(i+1,len(ops))): rejected=True; reason="openings overlap/intersect"
        except Exception as e: rejected=True; reason=str(e)
        invalid_results.append({"id":cid,"rejected":rejected,"reason":reason,"pass":rejected})
    def boundary(rows,key):
        lastp=None; firstf=None
        for row in rows:
            if row["overall_pass"]: lastp=row[key]
            elif firstf is None: firstf=row[key]
        return lastp,firstf
    tl,tf=boundary(thin,"ligament_mm"); gl,gf=boundary(gaps,"gap_mm")
    result={"status":"ACTUALLY EXECUTED","shape_cases":{"pass":sum(x["pass"] for x in shapes),"total":len(shapes),"results":shapes},"thin_edge_sweep":{"last_tested_pass_mm":tl,"first_tested_failure_mm":tf,"rows":thin},"multi_gap_sweep":{"last_tested_pass_mm":gl,"first_tested_failure_mm":gf,"rows":gaps},"invalid_cases":{"pass":sum(x["pass"] for x in invalid_results),"total":len(invalid_results),"results":invalid_results},"float32_spacing":{"at_3000_mm":float(np.spacing(np.float32(3000.0))),"at_3300_mm":float(np.spacing(np.float32(3300.0)))},"scope":"runtime-specific geometry/topology/interoperability stress test; not a universal design standard"}
    (outdir/"data"/"R03_results.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    for name,rows in (("thin_edge_sweep.csv",thin),("multi_gap_sweep.csv",gaps)):
        keys=sorted(set().union(*(r.keys() for r in rows)))
        with (outdir/"data"/name).open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=keys); w.writeheader(); w.writerows(rows)
    return result

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument("output",nargs="?",default="SP04_R03_reproduced"); args=ap.parse_args()
    r=run(args.output)
    print("shape:",r["shape_cases"]["pass"],"/",r["shape_cases"]["total"])
    print("invalid:",r["invalid_cases"]["pass"],"/",r["invalid_cases"]["total"])
    print("thin pass/fail boundary:",r["thin_edge_sweep"]["last_tested_pass_mm"],r["thin_edge_sweep"]["first_tested_failure_mm"])
    print("gap pass/fail boundary:",r["multi_gap_sweep"]["last_tested_pass_mm"],r["multi_gap_sweep"]["first_tested_failure_mm"])
