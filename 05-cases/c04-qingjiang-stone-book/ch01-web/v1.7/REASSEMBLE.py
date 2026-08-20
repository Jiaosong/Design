from pathlib import Path
import base64, tarfile, io, hashlib

root = Path(__file__).resolve().parent
b64 = (root / 'SOURCE_REVIEW_BUNDLE_v1_7.tar.gz.base64.txt').read_text(encoding='utf-8')
data = base64.b64decode(b64)
expected = '552f4b894411f404647bed1c32fa59630ca21a48dc5505645da0f6e90cfcb785'
actual = hashlib.sha256(data).hexdigest()
assert actual == expected, (actual, expected)
with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as tf:
    tf.extractall(root)
print('reassembled', actual)
