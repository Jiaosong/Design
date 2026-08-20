from pathlib import Path
import base64,gzip,json,hashlib
root=Path(__file__).parent
ext=json.loads((root/'SOURCE_CARRIER_MANIFEST_v0_5.json').read_text())
s=''.join(p.read_text().strip() for p in sorted((root/'source-parts').glob('part-*.txt')))
blob=gzip.decompress(base64.b64decode(s))
assert hashlib.sha256(blob).hexdigest()==ext['carrier_blob_sha256']
line,payload=blob.split(b"\n",1)
m=json.loads(line.decode())
out=root/'reconstructed'; out.mkdir(exist_ok=True)
for f in m['source_files']:
 b=payload[f['offset']:f['offset']+f['length']]
 assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
 p=out/f['path']; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)
print('PASS',len(m['source_files']))
