from pathlib import Path
import base64,gzip,hashlib
root=Path(__file__).resolve().parent
data=gzip.decompress(base64.b64decode((root/'index.html.gz.base64.txt').read_text('ascii')))
expected='d1ec1f0ea5ab21a45ed5045048cfe13da0614947cb8b8b47892601e22e993913'
assert hashlib.sha256(data).hexdigest()==expected
(root/'index.html').write_bytes(data)
print(expected,len(data))
