from pathlib import Path
import hashlib, json
root=Path(__file__).resolve().parent
man=json.loads((root/'SOURCE_CHUNK_MANIFEST_v1_30.json').read_text(encoding='utf-8'))
data=b''.join((root/'source-chunks'/c['file']).read_bytes() for c in man['chunks'])
if len(data)!=man['reassembled_bytes'] or hashlib.sha256(data).hexdigest()!=man['reassembled_sha256']:
    raise SystemExit('source reconstruction mismatch')
(root/'reassembled').mkdir(exist_ok=True)
(root/'reassembled'/'index.html').write_bytes(data)
print('EXACT',len(data),hashlib.sha256(data).hexdigest())
