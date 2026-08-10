# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd
import numpy as np
import math,json
WALL_L=6000.0; WALL_H=3300.0; OPEN_H=1800.0; WALL_AREA=WALL_L*WALL_H; RATIO=0.10
def run(csv_path,outdir):
    df=pd.read_csv(csv_path); f=df[df["overall_pass"]==True].copy().reset_index(drop=True)
    f["openness_ratio"]=f["count"]*(f["opening_width_mm"]*OPEN_H-(4-math.pi)*f["radius_mm"]**2)/WALL_AREA
    f["edge_slack"]=(f["edge_mm"]-f["required_edge_mm"])/f["required_edge_mm"]
    f["gap_slack"]=(f["gap_mm"]-f["required_gap_mm"])/f["required_gap_mm"]
    f["radius_slack"]=((f["radius_mm"]/f["wall_thickness_mm"])-RATIO)/RATIO
    f["packing_slack"]=f["packing_margin_mm"]/WALL_L
    f["vertical_slack"]=(WALL_H-(OPEN_H+2*f["edge_mm"]))/WALL_H
    cols=["edge_slack","gap_slack","radius_slack","packing_slack","vertical_slack"]
    f["robustness_margin"]=f[cols].min(axis=1)
    f.loc[f["robustness_margin"]<=1e-12,"robustness_margin"]=0.0
    loc=[]
    for count,g in f.groupby("count"):
        g=g.sort_values(["openness_ratio","robustness_margin"],ascending=[False,False])
        best=-1e99; idx=[]
        for i,r in g.iterrows():
            if r["robustness_margin"]>best+1e-12:
                idx.append(i); best=r["robustness_margin"]
        loc.append(f.loc[idx])
    c=pd.concat(loc,ignore_index=True)
    a=c[["openness_ratio","robustness_margin","count"]].to_numpy(float)
    p=np.ones(len(c),dtype=bool)
    for i in range(len(c)):
        oi,ri,ci=a[i]
        dom=(a[:,0]>=oi-1e-12)&(a[:,1]>=ri-1e-12)&(a[:,2]<=ci+1e-12)&((a[:,0]>oi+1e-12)|(a[:,1]>ri+1e-12)|(a[:,2]<ci-1e-12))
        dom[i]=False
        if dom.any(): p[i]=False
    q=c[p].sort_values(["openness_ratio","robustness_margin","count","packing_margin_mm","wall_thickness_mm"],ascending=[False,False,True,False,True]).drop_duplicates(["openness_ratio","robustness_margin","count"]).reset_index(drop=True)
    result={"source_total":len(df),"feasible_count":len(f),"pareto_count":len(q)}
    out=Path(outdir); out.mkdir(parents=True,exist_ok=True)
    (out/"reproduction_summary.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    q.to_csv(out/"reproduction_pareto.csv",index=False)
    return result
if __name__=="__main__":
 import sys
 print(run(sys.argv[1],sys.argv[2]))
