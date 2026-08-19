from pathlib import Path
import base64,gzip,hashlib
root=Path(__file__).resolve().parent
data=gzip.decompress(base64.b64decode((root/'index.html.gz.base64.txt').read_text('ascii')))
expected='7f1dc2abb1dcdd91137e933a3fed1e0db4c0f99c50cef754c79834bfcc78d445'
assert hashlib.sha256(data).hexdigest()==expected
(root/'index.html').write_bytes(data)
print(expected,len(data))
