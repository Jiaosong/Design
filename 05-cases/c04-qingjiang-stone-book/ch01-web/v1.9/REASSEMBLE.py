from pathlib import Path
import base64, tarfile, io, hashlib
root=Path(__file__).resolve().parent
raw=base64.b64decode((root/'SOURCE_REVIEW_BUNDLE_v1_9.tar.gz.base64.txt').read_text().strip())
print('bundle_sha256',hashlib.sha256(raw).hexdigest())
with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as t:
    t.extractall(root/'reassembled_v1_9')
print('reassembled', root/'reassembled_v1_9')
