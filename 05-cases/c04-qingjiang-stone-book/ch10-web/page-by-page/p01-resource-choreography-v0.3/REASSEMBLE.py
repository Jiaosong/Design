from pathlib import Path
import base64,gzip,hashlib
r=Path(__file__).resolve().parent
d=gzip.decompress(base64.b64decode((r/'index.html.gz.base64.txt').read_text('ascii')))
assert hashlib.sha256(d).hexdigest()=='ec3e4e1f3dc02f4d19fa74516f62e7e07ddcbd923bd519293d13d14935b5153e'
(r/'index.html').write_bytes(d)
print('ec3e4e1f3dc02f4d19fa74516f62e7e07ddcbd923bd519293d13d14935b5153e',len(d))
