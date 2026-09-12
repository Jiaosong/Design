#!/usr/bin/env python3
"""Fetch public same-revision 992.2 images for internal reference calibration only.
The images remain REFERENCE evidence and never become Source Authority.
"""
from __future__ import annotations
import hashlib,json,mimetypes,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlparse

OUT=Path('reference_images');OUT.mkdir(exist_ok=True)
UA={'User-Agent':'Mozilla/5.0 OLEANDER-reference-calibration/1.0'}
REFS=[
 {'id':'SIDE_9922','role':'SIDE_NEAR_ORTHOGRAPHIC','authority':'SUPPORT_SAME_REVISION','source':'Parkers 2025 Porsche 911 Carrera T 992.2 side shot','url':'https://parkers-images.bauersecure.com/wp-images/352444/static-exterior/1200x800/051-porsche-911-carrera-t-992-2-side-shot.jpg?mode=max&quality=90&scale=down'},
 {'id':'FRONT_9922','role':'FRONT_NEAR_ORTHOGRAPHIC','authority':'SUPPORT_SAME_REVISION','source':'Elferspot 2025 Porsche 992.2 Carrera front studio','url':'https://cdn.elferspot.com/wp-content/uploads/2025/10/22/imgi_8_ewa71f_992.2carrera-3-scaled-1.jpeg?class=xl'},
 {'id':'REAR_9922','role':'REAR_NEAR_ORTHOGRAPHIC','authority':'SUPPORT_SAME_REVISION','source':'Eurocar Porsche 911 Carrera 992 II rear studio','url':'https://eurocar-production.a.1cdn.it/photos/9362430d8b298f18b343ba5308b2bf14.jpg'},
 {'id':'REAR_9922_FALLBACK','role':'REAR_PERSPECTIVE_SUPPORT','authority':'SUPPORT_SAME_REVISION','source':'Car and Driver 2025 Porsche 911 Carrera rear','url':'https://hips.hearstapps.com/hmg-prod/images/2025-porsche-911-carrera-148-67b4ae74cf94a.jpg?crop=1xw%3A1xh%3Bcenter'}
]
receipt={'schema':'oleander.reference-image-fetch.9922.v1','reference_revision':'2025_992.2_CARRERA','policy':'PUBLIC_HTTP_ONLY_INTERNAL_CALIBRATION','records':[]}
for r in REFS:
 rec={k:r[k] for k in ('id','role','authority','source','url')}
 try:
  with urlopen(Request(r['url'],headers=UA),timeout=45) as resp:
   data=resp.read();ct=resp.headers.get('content-type','');ext='.png' if 'png' in ct else '.jpg';p=OUT/(r['id']+ext);p.write_bytes(data)
   rec.update(status='FETCHED',http_status=getattr(resp,'status',200),content_type=ct,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),local_file=str(p))
 except Exception as e:
  rec.update(status='FETCH_FAILED',error_type=type(e).__name__,error=str(e)[:400])
 receipt['records'].append(rec)
Path('REFERENCE_IMAGE_FETCH_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
