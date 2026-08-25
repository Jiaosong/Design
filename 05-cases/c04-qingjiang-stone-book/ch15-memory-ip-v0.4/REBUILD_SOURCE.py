from pathlib import Path
import hashlib
root=Path(__file__).parent
parts=sorted(root.glob('source-part*.txt'))
s=''.join(p.read_text(encoding='utf-8') for p in parts)
out=root/'index.html'
out.write_text(s,encoding='utf-8')
sha=hashlib.sha256(out.read_bytes()).hexdigest()
expected='58bab14eb0b58d6f8859141ee3cd2649dfd3d2ad48ff13bd58a7abf1d5c7c4eb'
print(out, out.stat().st_size, sha)
if sha!=expected: raise SystemExit(f'SHA mismatch: {sha} != {expected}')
