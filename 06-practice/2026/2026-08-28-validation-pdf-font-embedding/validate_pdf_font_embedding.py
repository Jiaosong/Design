#!/usr/bin/env python3
import subprocess, sys, json

def inspect(path):
    p=subprocess.run(['pdffonts',path],capture_output=True,text=True,check=True)
    lines=[x for x in p.stdout.splitlines() if x.strip()]
    rows=[]
    for line in lines[2:]:
        parts=line.split()
        yn=[i for i,v in enumerate(parts) if v in ('yes','no')]
        if len(yn) < 3:
            continue
        i=yn[-3]
        rows.append({'raw':line,'font':parts[0],'embedded':parts[i],'subset':parts[i+1],'unicode':parts[i+2]})
    return {'file':path,'fonts':rows,'all_embedded': bool(rows) and all(r['embedded']=='yes' for r in rows)}

results=[inspect(x) for x in sys.argv[1:]]
print(json.dumps(results,indent=2))
ok=(len(results)==2 and not results[0]['all_embedded'] and results[1]['all_embedded'])
sys.exit(0 if ok else 2)
