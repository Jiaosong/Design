from pathlib import Path
import base64, hashlib

root = Path(__file__).parent
parts = [root / f"SOURCE_REVIEW_BUNDLE_v2_7.part{i:02d}.txt" for i in range(1, 6)]
s = "".join(p.read_text(encoding="ascii") for p in parts)
b = base64.b64decode(s)
expected = "6f8c30e261d26bea4cceb4d56f8dee6942188d6a55cf4b3f8a38e5a33bbdae16"
actual = hashlib.sha256(b).hexdigest()
assert actual == expected, (actual, expected)
out = root / "SOURCE_REVIEW_BUNDLE_v2_7.reassembled.tar.gz"
out.write_bytes(b)
print(out.name, len(b), actual)
