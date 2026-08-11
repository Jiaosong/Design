from pathlib import Path
import argparse,csv,math,re
p=argparse.ArgumentParser(); p.add_argument('--input'); p.add_argument('--out'); p.add_argument('--scheme'); p.add_argument('--sky'); p.add_argument('--role'); a=p.parse_args()
lines=Path(a.input).read_text(errors='ignore').splitlines()
vals=None
for i,line in enumerate(lines):
    if line.lower().startswith('dgp'):
        if ':' in line:
            right=line.split(':',1)[1].strip()
            if right:
                vals=right.split()
        elif i+1<len(lines):
            vals=re.split(r'\s+',lines[i+1].strip())
if not vals:
    raise SystemExit('Cannot parse evalglare output')
nums=[]
for v in vals:
    try: nums.append(float(v))
    except: nums.append(float('nan'))
keys=['dgp','av_lum','E_v','lum_backg','E_v_dir','dgi','ugr','vcp','cgi','lum_sources','omega_sources','Lveil','Lveil_cie','band_avlum']
row={'scheme':a.scheme,'sky':a.sky,'role':a.role}
for k,v in zip(keys,nums): row[k]=v
with open(a.out,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(row)); w.writeheader(); w.writerow(row)
