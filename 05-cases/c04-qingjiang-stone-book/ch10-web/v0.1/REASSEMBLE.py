from pathlib import Path
import base64, gzip, hashlib

root = Path(__file__).resolve().parent
enc = (root / 'index.html.gz.base64.txt').read_text(encoding='utf-8').strip()
raw = gzip.decompress(base64.b64decode(enc))
expected_bytes = 30869
expected_sha = '82195183f2e1a1e6fb112f49daa72466be0ccf5dc0de5de6f4bd3264a2a5cae7'
if len(raw) != expected_bytes:
    raise SystemExit(f'byte mismatch: {len(raw)} != {expected_bytes}')
sha = hashlib.sha256(raw).hexdigest()
if sha != expected_sha:
    raise SystemExit(f'sha mismatch: {sha} != {expected_sha}')
(root / 'index.html').write_bytes(raw)
print('index.html', len(raw), sha, 'EXACT')
