from pathlib import Path
import base64, gzip, hashlib
root=Path(__file__).resolve().parent
data=gzip.decompress(base64.b64decode((root/'index.html.gz.base64.txt').read_text(encoding='ascii')))
expected_bytes=29087
expected_sha='55446dc04b073422ad7aeb9dc3522e5f08d1f5c4bdfb31323ffa05229a2a086d'
got=hashlib.sha256(data).hexdigest()
if len(data)!=expected_bytes or got!=expected_sha:
    raise SystemExit(f'REASSEMBLY FAIL bytes={len(data)} sha256={got}')
(root/'reassembled_index.html').write_bytes(data)
print(f'REASSEMBLY EXACT bytes={len(data)} sha256={got}')
