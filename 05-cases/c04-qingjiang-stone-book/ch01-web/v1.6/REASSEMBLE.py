from pathlib import Path
import base64, gzip, hashlib

ROOT = Path(__file__).resolve().parent
encoded = (ROOT / "style.css.gz.base64.txt").read_text(encoding="utf-8").strip()
css = gzip.decompress(base64.b64decode(encoded))
expected = "1a757bb763d430194514826b4a4814e7da0733668b22e6a6f54b619ff7078ef2"
actual = hashlib.sha256(css).hexdigest()
if actual != expected:
    raise SystemExit(f"SHA256 mismatch: {actual} != {expected}")
(ROOT / "style.css").write_bytes(css)
print(f"reconstructed style.css: {len(css)} bytes / sha256 {actual}")
