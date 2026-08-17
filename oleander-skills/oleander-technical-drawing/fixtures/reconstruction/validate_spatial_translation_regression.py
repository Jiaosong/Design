#!/usr/bin/env python3
import copy, json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "tools" / "validate_spatial_translation.py"
FIXTURE = Path(__file__).with_name("SPATIAL-TRANSLATION-01_REGISTER.json")


def run(data, should_pass, label):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        p = Path(f.name)
    cp = subprocess.run([sys.executable, str(VALIDATOR), str(p)], capture_output=True, text=True)
    p.unlink(missing_ok=True)
    ok = cp.returncode == 0
    if ok != should_pass:
        print(cp.stdout)
        print(cp.stderr)
        raise SystemExit(f"regression failed: {label}")
    print(f"PASS regression: {label}")


def main():
    base = json.loads(FIXTURE.read_text(encoding="utf-8"))
    run(base, True, "positive fixture")

    bad = copy.deepcopy(base)
    bad["items"][1]["registration_class"] = "MAP_BOUND"
    run(bad, False, "schematic route cannot claim map-bound")

    bad = copy.deepcopy(base)
    bad["items"][1]["preserved_invariants"].append("POSITION")
    run(bad, False, "topology-bound route cannot preserve exact position")

    bad = copy.deepcopy(base)
    bad["items"][3]["geometry_type"] = "SYMBOL_ONLY"
    run(bad, False, "junction cannot be symbol-only")

    bad = copy.deepcopy(base)
    bad["items"][2]["source_refs"] = []
    run(bad, False, "carrier without source binding must fail")

if __name__ == "__main__":
    main()
