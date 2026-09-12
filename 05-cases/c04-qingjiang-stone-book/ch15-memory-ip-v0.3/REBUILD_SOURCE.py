from pathlib import Path
import base64, hashlib
ROOT=Path(__file__).resolve().parent
parts=[ROOT/'source-b64'/f'part{i:02d}.b64' for i in range(1,8)]
data=''.join(p.read_text(encoding='utf-8').strip() for p in parts)
raw=base64.b64decode(data)
sha=hashlib.sha256(raw).hexdigest()
expected='8148002689a8f3a423728d2a3a29387cecf7307f212671bf0d09c82005d542a8'
if sha != expected:
    raise SystemExit(f'SHA256 mismatch: {sha} != {expected}')
out=ROOT/'CH15_VISUAL_LED_RUNTIME_v0_3.html'
out.write_bytes(raw)
print(f'PASS {out.name} bytes={len(raw)} sha256={sha}')
