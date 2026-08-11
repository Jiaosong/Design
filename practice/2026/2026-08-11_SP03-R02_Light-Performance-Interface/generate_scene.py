from pathlib import Path
import json, math, csv

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'runtime'
OUT.mkdir(exist_ok=True)
C=json.loads((ROOT/'input_contract.json').read_text())
L=C['geometry']['room_m']['length_x']; W=C['geometry']['room_m']['width_y']; H=C['geometry']['room_m']['height_z']
y0,y1=C['aperture_control']['skylight_y_range_m']
centers=C['aperture_control']['centers_x_m']

materials='''void plastic wall_mat\n0\n0\n5 0.65 0.65 0.65 0 0\n\nvoid plastic ceiling_mat\n0\n0\n5 0.80 0.80 0.80 0 0\n\nvoid plastic floor_mat\n0\n0\n5 0.25 0.25 0.25 0 0\n\nvoid glass glazing_mat\n0\n0\n3 0.60 0.60 0.60\n'''
(OUT/'materials.rad').write_text(materials)

def poly(mod,name,pts):
    vals='\n'.join(' '.join(f'{v:.6f}' for v in p) for p in pts)
    return f'{mod} polygon {name}\n0\n0\n{len(pts)*3}\n{vals}\n\n'

def room(scheme,widths):
    r=[]
    r.append(poly('floor_mat','floor',[(0,0,0),(L,0,0),(L,W,0),(0,W,0)]))
    r.append(poly('wall_mat','wall_s',[(0,0,0),(0,0,H),(L,0,H),(L,0,0)]))
    r.append(poly('wall_mat','wall_n',[(0,W,0),(L,W,0),(L,W,H),(0,W,H)]))
    r.append(poly('wall_mat','wall_w',[(0,0,0),(0,W,0),(0,W,H),(0,0,H)]))
    r.append(poly('wall_mat','wall_e',[(L,0,0),(L,0,H),(L,W,H),(L,W,0)]))
    r.append(poly('ceiling_mat','ceil_s',[(0,0,H),(0,y0,H),(L,y0,H),(L,0,H)]))
    r.append(poly('ceiling_mat','ceil_n',[(0,y1,H),(0,W,H),(L,W,H),(L,y1,H)]))
    intervals=[]
    for c,w in zip(centers,widths):
        intervals.append((c-w/2,c+w/2))
    x=0.0
    for i,(a,b) in enumerate(intervals):
        if a>x+1e-9:
            r.append(poly('ceiling_mat',f'ceil_gap_{i}',[(x,y0,H),(x,y1,H),(a,y1,H),(a,y0,H)]))
        r.append(poly('glazing_mat',f'skylight_{i}',[(a,y0,H),(a,y1,H),(b,y1,H),(b,y0,H)]))
        x=b
    if x<L-1e-9:
        r.append(poly('ceiling_mat','ceil_gap_end',[(x,y0,H),(x,y1,H),(L,y1,H),(L,y0,H)]))
    return ''.join(r), intervals

areas={}
for scheme,key in [('A','scheme_A_uniform_widths_m'),('B','scheme_B_sequence_widths_m')]:
    widths=C['aperture_control'][key]
    txt,ints=room(scheme,widths)
    (OUT/f'room_{scheme}.rad').write_text(txt)
    area=sum(widths)*(y1-y0)
    areas[scheme]=area
    (OUT/f'apertures_{scheme}.json').write_text(json.dumps({'intervals_x_m':ints,'y_range_m':[y0,y1],'total_area_m2':area},indent=2))
if not math.isclose(areas['A'],areas['B'],rel_tol=0,abs_tol=1e-9):
    raise SystemExit(f'aperture area mismatch {areas}')

step=C['geometry']['sensor_step_m']; z=C['geometry']['workplane_z_m']
xs=[]; v=step/2
while v < L-1e-9: xs.append(round(v,6)); v+=step
ys=[]; v=step/2
while v < W-1e-9: ys.append(round(v,6)); v+=step
roles=C['roles']
def role_for_x(x):
    for rr in roles:
        lo,hi=rr['x_range_m']
        if (x>=lo and x<hi) or (rr is roles[-1] and x<=hi): return rr['id']
    raise ValueError(x)
rows=[]
for x in xs:
    for y in ys:
        rows.append({'x_m':x,'y_m':y,'z_m':z,'role':role_for_x(x)})
with (OUT/'sensors.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['x_m','y_m','z_m','role']); w.writeheader(); w.writerows(rows)
with (OUT/'sensors.pts').open('w') as f:
    for rr in rows: f.write(f"{rr['x_m']} {rr['y_m']} {rr['z_m']} 0 0 1\n")

views=[]
for rr,cx in zip(roles,centers):
    views.append({'role':rr['id'],'vp':[cx,3.0,C['geometry']['eye_z_m']],'vd':[0,1,0],'vu':[0,0,1]})
(OUT/'views.json').write_text(json.dumps(views,indent=2))

summary={'sensor_count':len(rows),'aperture_area_m2':areas,'role_sensor_counts':{r['id']:sum(1 for x in rows if x['role']==r['id']) for r in roles}}
(OUT/'generation_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
