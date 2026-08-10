# -*- coding: utf-8 -*-
from pathlib import Path
import json, csv, hashlib

TESTS=[
 {"id":"T01","width_mm":900,"height_mm":2100,"sill_mm":0},
 {"id":"T02","width_mm":1200,"height_mm":2100,"sill_mm":0},
 {"id":"T03","width_mm":1500,"height_mm":2400,"sill_mm":450},
 {"id":"T04","width_mm":1800,"height_mm":2400,"sill_mm":900},
 {"id":"T05","width_mm":750,"height_mm":1800,"sill_mm":300},
]
WALL={"length_mm":6000,"height_mm":3300,"thickness_mm":240}
EPS=1e-6

def box(x0,x1,y0,y1,z0,z1):
 v=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
 f=[(1,2,3,4),(5,8,7,6),(1,5,6,2),(2,6,7,3),(3,7,8,4),(5,1,4,8)]
 return v,f

def export_obj(parts,path):
 lines=["# OLEANDER SP04-R01","# Units: millimeters","# TRAINING-ONLY HYPOTHETICAL PARAMETERS"]
 off=0
 for name,dims in parts:
  v,f=box(*dims); lines.append("o "+name)
  lines += ["v %.3f %.3f %.3f"%p for p in v]
  lines += ["f "+" ".join(str(i+off) for i in face) for face in f]
  off+=len(v)
 path.write_text("\n".join(lines)+"\n",encoding="utf-8")

def opening_parts(w,h,sill):
 L,H,T=WALL["length_mm"],WALL["height_mm"],WALL["thickness_mm"]
 cx=L/2.0; x0,x1=cx-w/2.0,cx+w/2.0; z0,z1=sill,sill+h
 if min(x0,z0)<0 or x1>L or z1>H: raise ValueError("Opening exceeds wall host")
 p=[]
 if x0>0:p.append(("wall_left",(0,x0,0,T,0,H)))
 if x1<L:p.append(("wall_right",(x1,L,0,T,0,H)))
 if z0>0:p.append(("wall_below",(x0,x1,0,T,0,z0)))
 if z1<H:p.append(("wall_above",(x0,x1,0,T,z1,H)))
 return p,(x0,x1,z0,z1)

def svg(test,r,path,kind):
 L,H,T=WALL["length_mm"],WALL["height_mm"],WALL["thickness_mm"]
 x0,x1,z0,z1=r; M=40
 if kind=="elevation":
  sx=(900-2*M)/L; sy=(500-2*M)/H; yy=lambda z:500-M-z*sy
  body=f'<rect x="{M}" y="{yy(H)}" width="{L*sx}" height="{H*sy}" fill="none" stroke="black"/><rect x="{M+x0*sx}" y="{yy(z1)}" width="{(x1-x0)*sx}" height="{(z1-z0)*sy}" fill="white" stroke="black"/>'; W,Hpx=900,500
 elif kind=="plan":
  sx=(900-2*M)/L; body=f'<rect x="{M}" y="100" width="{L*sx}" height="60" fill="none" stroke="black"/><rect x="{M+x0*sx}" y="95" width="{(x1-x0)*sx}" height="70" fill="white" stroke="black"/>'; W,Hpx=900,260
 else:
  body=f'<rect x="160" y="60" width="120" height="360" fill="none" stroke="black"/><rect x="150" y="{420-(z1/H)*360}" width="140" height="{((z1-z0)/H)*360}" fill="white" stroke="black"/>'; W,Hpx=520,500
 title=f"{test['id']} {kind.title()} QA"
 path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hpx}"><rect width="100%" height="100%" fill="white"/>{body}<text x="30" y="28" font-size="18">{title}</text><text x="30" y="{Hpx-15}" font-size="12">TRAINING-ONLY HYPOTHETICAL PARAMETERS</text></svg>',encoding="utf-8")

def run(outdir):
 out=Path(outdir)
 for d in ["models","views","data"]:(out/d).mkdir(parents=True,exist_ok=True)
 results=[]
 for t in TESTS:
  parts,r=opening_parts(t["width_mm"],t["height_mm"],t["sill_mm"]); obj=out/"models"/f"{t['id']}_wall_opening.obj"; export_obj(parts,obj)
  x0,x1,z0,z1=r
  checks={"width_exact":abs((x1-x0)-t["width_mm"])<EPS,"height_exact":abs((z1-z0)-t["height_mm"])<EPS,"sill_exact":abs(z0-t["sill_mm"])<EPS,"within_host":x0>=0 and x1<=WALL["length_mm"] and z0>=0 and z1<=WALL["height_mm"],"through_thickness":True,"obj_exists":obj.exists() and obj.stat().st_size>0}
  for kind in ["plan","elevation","section"]:svg(t,r,out/"views"/f"{t['id']}_{kind}.svg",kind)
  results.append({"id":t["id"],**t,"checks":checks,"pass":all(checks.values()),"obj":obj.name})
 (out/"data"/"parameters.json").write_text(json.dumps({"status":"TRAINING-ONLY HYPOTHETICAL PARAMETERS","wall":WALL,"tests":TESTS},ensure_ascii=False,indent=2),encoding="utf-8")
 (out/"data"/"qa_results.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
 with (out/"data"/"qa_results.csv").open("w",newline="",encoding="utf-8") as f:
  w=csv.writer(f); w.writerow(["id","width_mm","height_mm","sill_mm","pass","model"])
  for r in results:w.writerow([r["id"],r["width_mm"],r["height_mm"],r["sill_mm"],r["pass"],r["obj"]])
 manifest=[]
 for p in sorted(out.rglob("*")):
  if p.is_file() and p.name!="MANIFEST.json":manifest.append({"path":str(p.relative_to(out)).replace("\\","/"),"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size})
 (out/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
 return results

if __name__=="__main__":
 import argparse
 ap=argparse.ArgumentParser(); ap.add_argument("output",nargs="?",default="SP04_R01_regenerated"); a=ap.parse_args(); r=run(a.output)
 print("tests:",len(r)); print("all_pass:",all(x["pass"] for x in r))
