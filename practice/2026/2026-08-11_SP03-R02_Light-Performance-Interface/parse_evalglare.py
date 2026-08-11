from pathlib import Path
import argparse, csv, math

p=argparse.ArgumentParser()
p.add_argument('--input', required=True)
p.add_argument('--out', required=True)
p.add_argument('--scheme', required=True)
p.add_argument('--sky', required=True)
p.add_argument('--role', required=True)
a=p.parse_args()

lines=Path(a.input).read_text(errors='ignore').splitlines()
header=None
values=None

# evalglare detailed output ends with a self-describing record such as:
# dgp,av_lum,E_v,...,ugp2: 0.298364 435.64 ...
# Read the schema from evalglare itself so future versions cannot silently
# shift a metric into an incorrectly hard-coded column name.
for line in reversed(lines):
    stripped=line.strip()
    if stripped.lower().startswith('dgp') and ':' in stripped:
        left,right=stripped.split(':',1)
        keys=[x.strip() for x in left.split(',') if x.strip()]
        vals=right.split()
        if keys and vals:
            header=keys
            values=vals
            break

if not header or not values:
    raise SystemExit('Cannot locate self-describing evalglare result record')
if len(header) != len(values):
    raise SystemExit(f'evalglare schema/value count mismatch: keys={len(header)} values={len(values)}')

nums=[]
for key,value in zip(header,values):
    try:
        number=float(value)
    except ValueError as exc:
        raise SystemExit(f'Non-numeric evalglare value for {key}: {value}') from exc
    if not math.isfinite(number):
        raise SystemExit(f'Non-finite evalglare value for {key}: {value}')
    nums.append(number)

required={'dgp','E_v','av_lum','lum_backg'}
missing=required.difference(header)
if missing:
    raise SystemExit(f'Missing required evalglare fields: {sorted(missing)}')

row={'scheme':a.scheme,'sky':a.sky,'role':a.role}
row.update(dict(zip(header,nums)))
with open(a.out,'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(row))
    w.writeheader()
    w.writerow(row)

print(f'parsed evalglare fields={len(header)} schema={header}')
