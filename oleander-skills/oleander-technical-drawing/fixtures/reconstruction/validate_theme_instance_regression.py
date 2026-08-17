#!/usr/bin/env python3
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SVG = ROOT / "THEME-01_INSTANCE.svg"
REG = ROOT / "THEME-01_INSTANCE_REGISTER.json"
VALIDATOR = ROOT.parents[1] / "tools" / "validate_theme_instances.py"


def run(svg, reg):
    return subprocess.run(["python", str(VALIDATOR), "--svg", str(svg), "--register", str(reg)], capture_output=True, text=True).returncode


def main():
    assert run(SVG, REG) == 0
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # raster contamination must fail
        bad_svg = td / "bad.svg"
        s = SVG.read_text(encoding="utf-8").replace('<g id="THEME-01-VIS-A" data-role="STRUCTURED_THEME_VISUAL_VECTOR_NON_AUTHORITY">', '<g id="THEME-01-VIS-A" data-role="STRUCTURED_THEME_VISUAL_VECTOR_NON_AUTHORITY"><image href="x.png"/>')
        bad_svg.write_text(s, encoding="utf-8")
        assert run(bad_svg, REG) != 0
        # text contamination must fail
        bad_svg2 = td / "bad2.svg"
        s2 = SVG.read_text(encoding="utf-8").replace('<g id="THEME-01-VIS-B" data-role="STRUCTURED_THEME_VISUAL_VECTOR_NON_AUTHORITY">', '<g id="THEME-01-VIS-B" data-role="STRUCTURED_THEME_VISUAL_VECTOR_NON_AUTHORITY"><text>label</text>')
        bad_svg2.write_text(s2, encoding="utf-8")
        assert run(bad_svg2, REG) != 0
        # false authority must fail
        bad_reg = td / "bad.json"
        r = json.loads(REG.read_text(encoding="utf-8")); r["themes"][0]["authority"] = "PROJECT_AUTHORITY"; bad_reg.write_text(json.dumps(r), encoding="utf-8")
        assert run(SVG, bad_reg) != 0
    print("OLEANDER THEME INSTANCE REGRESSION: POSITIVE + NEGATIVE CONTRACT PASS")
    print("blocked=raster-contamination,text-contamination,false-authority")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
