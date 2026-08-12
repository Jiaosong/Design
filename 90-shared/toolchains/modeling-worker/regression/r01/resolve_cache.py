#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
WORKER_VERSION='oleander-modeling-selective-r01'
BLENDER_VERSION='5.2.0-LTS'

def main():
    p=argparse.ArgumentParser();p.add_argument('--contract',required=True);p.add_argument('--source-sha',required=True);p.add_argument('--cache-dir',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    c=json.loads(Path(a.contract).read_text());norm=json.dumps(c,sort_keys=True,separators=(',',':'))
    key=hashlib.sha256((a.source_sha+'\n'+WORKER_VERSION+'\n'+BLENDER_VERSION+'\n'+norm).encode()).hexdigest()
    entry=Path(a.cache_dir)/key;manifest=entry/'CACHE_MANIFEST.json'
    status='HIT' if manifest.exists() else 'MISS'
    out={'schema':'oleander.content-addressed-cache-resolution.v1','status':status,'cache_key':key,'entry':str(entry),'worker_version':WORKER_VERSION,'blender_version':BLENDER_VERSION}
    Path(a.out).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))
if __name__=='__main__':main()
