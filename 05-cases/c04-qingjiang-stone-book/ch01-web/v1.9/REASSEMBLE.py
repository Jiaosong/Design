from pathlib import Path
import base64, tarfile, io, hashlib
root = Path(__file__).resolve().parent
parts = [root / f'SOURCE_REVIEW_BUNDLE_v1_9.part{i:02d}.txt' for i in range(1,5)]
b64 = ''.join(p.read_text().strip() for p in parts)
assert len(b64) == 22484, len(b64)
raw = base64.b64decode(b64, validate=True)
sha = hashlib.sha256(raw).hexdigest()
expected = 'a99c215c5deb3ebeb7bb62719b3309ad09c6aebcab8edf911943c59c8c906102'
assert sha == expected, (sha, expected)
out = root / 'reassembled_v1_9'
out.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as t:
    t.extractall(out)
print('base64_chars', len(b64))
print('bundle_bytes', len(raw))
print('bundle_sha256', sha)
print('reassembled', out)
