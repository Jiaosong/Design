#!/usr/bin/env python3
"""Probe only normal public access surfaces for CC-BY 911 reference assets.
No login bypass, token scraping, private CDN discovery, or protected API circumvention.
"""
from __future__ import annotations
import json,re
from urllib.request import Request,urlopen
from urllib.error import HTTPError

UA={'User-Agent':'OLEANDER-reference-probe/1.1'}
result={'schema':'oleander.reference-asset-public-probe.v2','policy':'PUBLIC_PATH_ONLY_NO_AUTH_BYPASS','probes':[]}

def fetch(name,url,parse_html=False):
    rec={'name':name,'url':url}
    try:
        with urlopen(Request(url,headers=UA),timeout=30) as r:
            raw=r.read();rec['http_status']=getattr(r,'status',200);rec['bytes']=len(raw);rec['status']='FETCHED'
            ct=r.headers.get('content-type','');rec['content_type']=ct
            if 'json' in ct:
                try:
                    d=json.loads(raw);rec['json_keys']=sorted(d.keys())[:80]
                    for k in ('uid','name','isDownloadable','license','viewerUrl','embedUrl'):
                        if k in d: rec[k]=d[k]
                except Exception as e:rec['json_parse_error']=type(e).__name__
            elif parse_html:
                html=raw.decode('utf-8','replace');rec['mentions_download']='download' in html.lower();rec['mentions_target_file']='porsche_911.zip' in html.lower();rec['file_routes']=list(dict.fromkeys(re.findall(r'href=["\']([^"\']*(?:/file/|download)[^"\']*)["\']',html,re.I)))[:20]
    except HTTPError as e:
        rec['status']='HTTP_ERROR';rec['http_status']=e.code;rec['error']=str(e)
    except Exception as e:
        rec['status']='ERROR';rec['error_type']=type(e).__name__;rec['error']=str(e)[:300]
    result['probes'].append(rec)

fetch('itch_public_page','https://oxycodonee.itch.io/game-ready-porsche-911-asset',True)
uid='4e196689d05e4029b9c7f5ef25755b8d'
fetch('sketchfab_public_model_page',f'https://sketchfab.com/3d-models/porsche-911-992-coupe-and-cabriolet-{uid}',True)
fetch('sketchfab_public_metadata',f'https://api.sketchfab.com/v3/models/{uid}')
fetch('sketchfab_public_download_endpoint_no_auth',f'https://api.sketchfab.com/v3/models/{uid}/download')

# Fail closed: an auth-protected download endpoint is not an error; it means ground-truth ingestion is HOLD.
dl=next(x for x in result['probes'] if x['name']=='sketchfab_public_download_endpoint_no_auth')
if dl.get('http_status') in (401,403): result['ground_truth_ingestion']='HOLD_AUTH_REQUIRED_NO_BYPASS'
elif dl.get('status')=='FETCHED': result['ground_truth_ingestion']='PUBLIC_DOWNLOAD_AVAILABLE'
else: result['ground_truth_ingestion']='HOLD_PUBLIC_DOWNLOAD_UNRESOLVED'
print(json.dumps(result,indent=2))
open('PUBLIC_REFERENCE_ASSET_PROBE.json','w').write(json.dumps(result,indent=2)+'\n')
