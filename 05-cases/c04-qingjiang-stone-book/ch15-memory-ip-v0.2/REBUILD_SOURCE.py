from pathlib import Path
import base64
import hashlib

ROOT = Path(__file__).resolve().parent
PARTS = [
    ROOT / "source-b64/CH15_PORTABLE_PREVIEW_v0_2.part01.b64",
    ROOT / "source-b64/CH15_PORTABLE_PREVIEW_v0_2.part02.b64",
    ROOT / "source-b64/CH15_PORTABLE_PREVIEW_v0_2.part03.b64",
    ROOT / "source-b64/CH15_PORTABLE_PREVIEW_v0_2.part04.b64",
    ROOT / "source-b64/CH15_PORTABLE_PREVIEW_v0_2.part05a.b64",
    ROOT / "source-b64/CH15_PORTABLE_PREVIEW_v0_2.part05b.b64",
]
EXPECTED_SHA256 = "b5cad39d797efb09d6c27245e04bd41682ad8cc0a5ce48ed69176283147f9f11"
OUTPUT = ROOT / "CH15_PORTABLE_PREVIEW_v0_2.html"

encoded = "".join(p.read_text(encoding="utf-8").strip() for p in PARTS)
data = base64.b64decode(encoded, validate=True)
actual = hashlib.sha256(data).hexdigest()
if actual != EXPECTED_SHA256:
    raise SystemExit(f"SHA256 mismatch: expected {EXPECTED_SHA256}, got {actual}")
OUTPUT.write_bytes(data)
print(f"rebuilt {OUTPUT.name}: {len(data)} bytes / sha256={actual}")
