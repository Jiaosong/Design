from pathlib import Path
import base64,gzip,hashlib
root=Path(__file__).resolve().parent
data=gzip.decompress(base64.b64decode((root/"index.html.gz.base64.txt").read_text().strip()))
sha=hashlib.sha256(data).hexdigest()
expected="dba23330f9d271718e5ba754688cc75cc7b4b2884db810c9e060f58a6d5c6e50"
assert sha==expected,(sha,expected)
(root/"reassembled_index.html").write_bytes(data)
print(len(data),sha,"EXACT")
