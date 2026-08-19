from pathlib import Path
import base64,gzip,hashlib
r=Path(__file__).resolve().parent
d=gzip.decompress(base64.b64decode((r/'C04_C22_CONCEPT_MASTERPLAN_CH14_v4_7.svg.gz.base64.txt').read_text('ascii')))
expected='2cb5a373d31c6ba78853bd3dbd8c13e522de9f66e5c2710093da938688a18776'
assert hashlib.sha256(d).hexdigest()==expected
(r/'C04_C22_CONCEPT_MASTERPLAN_CH14_v4_7.svg').write_bytes(d)
print(expected,len(d))
