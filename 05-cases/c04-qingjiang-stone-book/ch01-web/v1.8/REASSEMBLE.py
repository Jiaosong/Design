from pathlib import Path
import base64, tarfile, io, hashlib

root = Path(__file__).parent
raw = base64.b64decode((root / 'SOURCE_REVIEW_BUNDLE_v1_8.tar.gz.base64.txt').read_text().strip())
expected = '269450be8645a26d4d32b266b0cabe60fe642b77f00b9034e96b0fd459f1203f'
actual = hashlib.sha256(raw).hexdigest()
assert actual == expected, (actual, expected)
with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as t:
    t.extractall(root / 'reconstructed')
print('OK', len(raw), actual)
