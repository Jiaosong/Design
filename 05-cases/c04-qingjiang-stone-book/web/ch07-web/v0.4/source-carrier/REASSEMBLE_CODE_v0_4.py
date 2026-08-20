from pathlib import Path
import base64,gzip,tarfile,io,hashlib
r=Path(__file__).parent
s="".join(p.read_text().strip() for p in sorted(r.glob("CODE_BUNDLE_v0_4.part*.b85.txt")))
raw=base64.b85decode(s.encode())
expected="0d39ebcd1cf1e8a0d11bd2a91e1909f03fa170fb913aca16dd482a84e9e5207d"
assert hashlib.sha256(raw).hexdigest()==expected
tar=gzip.decompress(raw)
with tarfile.open(fileobj=io.BytesIO(tar),mode="r:") as tf: tf.extractall(r/"reassembled")
print(expected,len(raw))
