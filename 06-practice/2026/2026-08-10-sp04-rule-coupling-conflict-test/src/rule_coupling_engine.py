# -*- coding: utf-8 -*-
import json
from pathlib import Path
WALL_L=6000.0
RULES={'status': 'TRAINING-ONLY HYPOTHETICAL RULES — NOT CODE / NOT STANDARD', 'min_edge_ligament_mm': 50.0, 'min_opening_gap_mm': 100.0, 'edge_to_thickness_ratio': 0.5, 'gap_to_thickness_ratio': 0.75, 'corner_radius_pass_ratio': 0.1, 'min_wall_thickness_mm': 40.0, 'max_opening_count_pass': 8}
AXES={'wall_thickness_mm': [40, 60, 80, 120, 160, 240, 300], 'edge_mm': [50, 80, 100, 120, 150, 180, 240, 300], 'gap_mm': [100, 120, 150, 180, 225, 240, 300], 'radius_mm': [12, 20, 24, 30, 40, 60, 90], 'count': [2, 4, 6, 8], 'opening_width_mm': [450, 600, 750, 900]}
OPENING_H=1800.0
WALL_H=3300.0
def single_rules(t,e,g,r,n):
    reqe=max(RULES['min_edge_ligament_mm'],RULES['edge_to_thickness_ratio']*t)
    reqg=max(RULES['min_opening_gap_mm'],RULES['gap_to_thickness_ratio']*t)
    c={'thickness':t>=RULES['min_wall_thickness_mm'],'edge':e>=reqe,'gap':g>=reqg,'radius':r/t>=RULES['corner_radius_pass_ratio'],'count':n<=RULES['max_opening_count_pass']}
    return c,reqe,reqg
def run(out):
    rows=[]
    for t in AXES['wall_thickness_mm']:
      for e in AXES['edge_mm']:
       for g in AXES['gap_mm']:
        for r in AXES['radius_mm']:
         for n in AXES['count']:
          for w in AXES['opening_width_mm']:
           c,reqe,reqg=single_rules(t,e,g,r,n); sp=all(c.values())
           span=2*e+n*w+(n-1)*g
           rad=2*r<=min(w,OPENING_H); vert=OPENING_H+2*e<=WALL_H
           cp=span<=WALL_L and rad and vert
           cat='SINGLE_PASS_COUPLED_PASS' if sp and cp else ('SINGLE_PASS_PACKING_FAIL' if sp and span>WALL_L else 'OTHER')
           rows.append({'t':t,'e':e,'g':g,'r':r,'n':n,'w':w,'single':sp,'span':span,'margin':WALL_L-span,'coupled':cp,'category':cat})
    sp=[x for x in rows if x['single']]; em=[x for x in sp if not x['coupled']]
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    result={'total':len(rows),'single_pass':len(sp),'emergent':len(em),'rate':len(em)/len(sp)}
    (out/'reproduction.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result
if __name__=='__main__':
 import sys
 print(run(sys.argv[1] if len(sys.argv)>1 else 'R05_repro'))
