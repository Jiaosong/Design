from pathlib import Path
import argparse,csv
p=argparse.ArgumentParser(); p.add_argument('--raw'); p.add_argument('--sensors'); p.add_argument('--out'); p.add_argument('--scheme'); p.add_argument('--sky'); a=p.parse_args()
with open(a.sensors) as f: sensors=list(csv.DictReader(f))
raw=[]
for line in Path(a.raw).read_text().splitlines():
    if not line.strip(): continue
    vals=[float(x) for x in line.split()[:3]]
    if len(vals)!=3: continue
    raw.append(vals)
if len(raw)!=len(sensors): raise SystemExit(f'count mismatch raw={len(raw)} sensors={len(sensors)}')
rows=[]
for s,(r,g,b) in zip(sensors,raw):
    lux=179.0*(0.265*r+0.670*g+0.065*b)
    rows.append({**s,'scheme':a.scheme,'sky':a.sky,'R':r,'G':g,'B':b,'lux':lux})
with open(a.out,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
