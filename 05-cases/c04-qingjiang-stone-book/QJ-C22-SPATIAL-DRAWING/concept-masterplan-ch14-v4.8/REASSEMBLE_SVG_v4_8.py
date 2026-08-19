from pathlib import Path
import gzip,base64,hashlib
r=Path(__file__).resolve().parent
d=gzip.decompress(base64.b64decode((r/"C04_C22_CONCEPT_MASTERPLAN_CH14_v4_8.svg.gz.b64.txt").read_text("ascii")))
expected="a87fdbd180765fbe2b2b957d8c4e17fa126a9e95eafa1d460b25d670fcdb8226"
assert hashlib.sha256(d).hexdigest()==expected
(r/"C04_C22_CONCEPT_MASTERPLAN_CH14_v4_8.svg").write_bytes(d)
print(expected,len(d))
