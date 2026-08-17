#!/usr/bin/env python3
"""Probe only normal public download surfaces for the CC-BY 911 reference asset.
No login bypass, token scraping, or protected API circumvention is allowed.
"""
from __future__ import annotations
import json,re,sys
from urllib.request import Request,urlopen

PAGE='https://oxycodonee.itch.io/game-ready-porsche-911-asset'
req=Request(PAGE,headers={'User-Agent':'OLEANDER-reference-probe/1.0'})
result={'schema':'oleander.reference-asset-public-probe.v1','page':PAGE,'policy':'PUBLIC_PATH_ONLY_NO_AUTH_BYPASS','status':'UNKNOWN'}
try:
    with urlopen(req,timeout=30) as r:
        html=r.read().decode('utf-8','replace')
        result['http_status']=getattr(r,'status',200)
        result['page_bytes']=len(html.encode())
        result['mentions_target_file']='porsche_911.zip' in html
        patterns={
            'upload_ids':r'upload_id[^0-9]{0,20}(\d+)',
            'file_routes':r'href=["\']([^"\']*(?:/file/|download)[^"\']*)["\']',
            'target_context':r'.{0,120}porsche_911\.zip.{0,180}'
        }
        for k,p in patterns.items():
            vals=list(dict.fromkeys(re.findall(p,html,re.I|re.S)))[:10]
            result[k]=vals
        result['status']='PUBLIC_PAGE_FETCHED'
except Exception as e:
    result['status']='PUBLIC_PAGE_FETCH_FAILED';result['error_type']=type(e).__name__;result['error']=str(e)[:300]
print(json.dumps(result,indent=2))
open('PUBLIC_REFERENCE_ASSET_PROBE.json','w').write(json.dumps(result,indent=2)+'\n')
