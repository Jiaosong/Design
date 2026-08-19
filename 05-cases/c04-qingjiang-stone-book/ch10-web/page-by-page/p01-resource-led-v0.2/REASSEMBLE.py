from pathlib import Path
import base64,gzip,hashlib
root=Path(__file__).resolve().parent
data=gzip.decompress(base64.b64decode((root/'index.html.gz.base64.txt').read_text('ascii')))
expected='1f5a4cd295bfe2409a3ae10405c421474f3e07aac33b65722a0ded28864392c1'
assert hashlib.sha256(data).hexdigest()==expected
(root/'index.html').write_bytes(data)
print(expected,len(data))
