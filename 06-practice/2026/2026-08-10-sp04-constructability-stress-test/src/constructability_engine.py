# -*- coding: utf-8 -*-
"""
OLEANDER / 织作 — SP04-R04 Constructability Engine
Standalone reproducible rule sweep.
Requires: shapely.
All thresholds are TRAINING-ONLY HYPOTHETICAL RULES.
"""
from pathlib import Path
import json, csv, math
from shapely.geometry import box, Point, Polygon

WALL={"length_mm":6000.0,"height_mm":3300.0,"thickness_mm":240.0}
RULES={
 "min_edge_ligament_mm":50.0,
 "min_opening_gap_mm":100.0,
 "min_edge_ligament_to_wall_thickness_ratio":0.50,
 "min_gap_to_wall_thickness_ratio":0.75,
 "corner_radius_warning_ratio":0.10,
 "corner_radius_fail_ratio":0.02,
 "wall_thickness_warning_below_mm":40.0,
 "wall_thickness_fail_below_mm":20.0,
 "max_opening_count_before_warning":8
}

def rect_opening(cx,sill,width,height):
    if width<=0 or height<=0: raise ValueError("width/height must be > 0")
    return box(cx-width/2,sill,cx+width/2,sill+height)

def rounded_rect(cx,sill,width,height,radius,resolution=24):
    if width<=0 or height<=0: raise ValueError("width/height must be > 0")
    if radius<=0: raise ValueError("radius must be > 0")
    if radius>min(width,height)/2: raise ValueError("radius exceeds half of minimum opening dimension")
    x0,x1=cx-width/2,cx+width/2; z0,z1=sill,sill+height
    return box(x0+radius,z0+radius,x1-radius,z1-radius).buffer(radius,resolution=resolution,join_style=1)

def circle(cx,cz,r,resolution=48):
    if r<=0: raise ValueError("circle radius must be > 0")
    return Point(cx,cz).buffer(r,resolution=resolution)

def ellipse(cx,cz,rx,rz,segments=96):
    if rx<=0 or rz<=0: raise ValueError("ellipse radii must be > 0")
    return Polygon([(cx+rx*math.cos(2*math.pi*i/segments),
                     cz+rz*math.sin(2*math.pi*i/segments)) for i in range(segments)])

def geometry_preflight(openings,wall):
    host=box(0,0,wall["length_mm"],wall["height_mm"])
    for i,o in enumerate(openings):
        if not o.is_valid or o.area<=0: return False,"invalid opening"
        if not host.contains(o): return False,"outside/touching host boundary"
    for i in range(len(openings)):
        for j in range(i+1,len(openings)):
            if openings[i].intersects(openings[j]): return False,"overlap/intersection"
    return True,"OK"

def evaluate(openings,wall,corner_radius_mm=None):
    ok,reason=geometry_preflight(openings,wall)
    if not ok:
        return {"status":"FAIL","geometry_status":"FAIL","reasons":[reason]}
    host=box(0,0,wall["length_mm"],wall["height_mm"])
    t=wall["thickness_mm"]
    lig=min(o.boundary.distance(host.boundary) for o in openings)
    gaps=[openings[i].distance(openings[j]) for i in range(len(openings)) for j in range(i+1,len(openings))]
    gap=min(gaps) if gaps else None
    reasons=[]; status="PASS"
    req_edge=max(RULES["min_edge_ligament_mm"],RULES["min_edge_ligament_to_wall_thickness_ratio"]*t)
    if lig<req_edge: status="FAIL"; reasons.append("edge ligament rule")
    if gap is not None:
        req_gap=max(RULES["min_opening_gap_mm"],RULES["min_gap_to_wall_thickness_ratio"]*t)
        if gap<req_gap: status="FAIL"; reasons.append("opening gap rule")
    if corner_radius_mm is not None:
        ratio=corner_radius_mm/t
        if ratio<RULES["corner_radius_fail_ratio"]:
            status="FAIL"; reasons.append("corner radius fail ratio")
        elif ratio<RULES["corner_radius_warning_ratio"] and status!="FAIL":
            status="WARNING"; reasons.append("corner radius warning ratio")
    if t<RULES["wall_thickness_fail_below_mm"]:
        status="FAIL"; reasons.append("wall thickness fail")
    elif t<RULES["wall_thickness_warning_below_mm"] and status!="FAIL":
        status="WARNING"; reasons.append("wall thickness warning")
    if len(openings)>RULES["max_opening_count_before_warning"] and status=="PASS":
        status="WARNING"; reasons.append("opening count warning")
    return {"status":status,"geometry_status":"PASS","reasons":reasons or ["pass"],
            "metrics":{"min_edge_ligament_mm":lig,"min_opening_gap_mm":gap,"wall_thickness_mm":t}}

def transition(rows,key):
    lp=fw=ff=None
    for r in rows:
        if r["status"]=="PASS": lp=r[key]
        elif r["status"]=="WARNING" and fw is None: fw=r[key]
        elif r["status"]=="FAIL" and ff is None: ff=r[key]
    return {"last_pass":lp,"first_warning":fw,"first_fail":ff}

def run(outdir):
    outdir=Path(outdir); (outdir/"data").mkdir(parents=True,exist_ok=True)
    edge=[]
    for v in [500,300,200,150,120,100,80,60,50,40,30,20,10,5,1,0.1]:
        op=rect_opening(3000,WALL["height_mm"]-v-1800,1600,1800)
        edge.append({"edge_ligament_mm":v,**evaluate([op],WALL.copy())})
    gap=[]
    for v in [500,400,300,240,200,180,160,140,120,100,80,60,40,20,10,5,1,0.1]:
        r=500
        ops=[circle(3000-r-v/2,1650,r),circle(3000+r+v/2,1650,r)]
        gap.append({"gap_mm":v,**evaluate(ops,WALL.copy())})
    radius=[]
    for v in [300,200,100,50,30,24,20,10,5,4,3,2,1,0.1]:
        try: ev=evaluate([rounded_rect(3000,500,1600,2100,v)],WALL.copy(),v)
        except Exception as e: ev={"status":"FAIL","geometry_status":"FAIL","reasons":[str(e)]}
        radius.append({"radius_mm":v,**ev})
    thick=[]
    for v in [500,300,240,160,120,80,60,40,30,20,19,10]:
        w=WALL.copy(); w["thickness_mm"]=float(v)
        thick.append({"wall_thickness_mm":v,**evaluate([rounded_rect(3000,500,1600,2100,120)],w,120)})
    arr=[]
    for count in range(2,13):
        v=180.0; ow=260.0; total=count*ow+(count-1)*v
        x=(WALL["length_mm"]-total)/2+ow/2
        ops=[rect_opening(x+i*(ow+v),800,ow,1500) for i in range(count)]
        arr.append({"count":count,**evaluate(ops,WALL.copy())})
    invalid=[]
    tests=[
      ("negative sill",lambda:[rect_opening(3000,-100,1000,1500)],WALL.copy()),
      ("zero width",lambda:[rect_opening(3000,300,0,1500)],WALL.copy()),
      ("radius too large",lambda:[rounded_rect(3000,400,800,1000,500)],WALL.copy()),
      ("outside host",lambda:[ellipse(5850,1700,400,700)],WALL.copy()),
      ("overlap",lambda:[circle(2800,1700,650),circle(3600,1700,650)],WALL.copy()),
    ]
    for name,fn,w in tests:
        try: ev=evaluate(fn(),w); rejected=ev["status"]=="FAIL"
        except Exception as e: ev={"status":"FAIL","reasons":[str(e)]}; rejected=True
        invalid.append({"case":name,"pass":rejected,"evaluation":ev})
    w=WALL.copy(); w["thickness_mm"]=0.0
    ev=evaluate([rect_opening(3000,500,1000,1800)],w)
    invalid.append({"case":"zero wall thickness","pass":ev["status"]=="FAIL","evaluation":ev})
    result={"status":"ACTUALLY EXECUTED","rules":RULES,
      "boundaries":{
        "edge_ligament":transition(edge,"edge_ligament_mm"),
        "opening_gap":transition(gap,"gap_mm"),
        "corner_radius":transition(radius,"radius_mm"),
        "wall_thickness":transition(thick,"wall_thickness_mm"),
        "opening_array_count":transition(arr,"count")},
      "invalid_pass":sum(x["pass"] for x in invalid),"invalid_total":len(invalid)}
    (outdir/"data"/"reproduction_results.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    return result

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument("output",nargs="?",default="R04_reproduced")
    a=ap.parse_args(); r=run(a.output)
    print(json.dumps(r,ensure_ascii=False))
