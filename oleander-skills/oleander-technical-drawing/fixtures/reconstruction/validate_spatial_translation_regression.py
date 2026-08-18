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

    bad = copy.deepcopy(base)
    bad["items"][0]["redraw_justification"] = "cleaner"
    run(bad, False, "authoritative source cannot be redrawn for aesthetics only")

    bad = copy.deepcopy(base)
    bad["items"][3]["redraw_justification"] = "N/A"
    run(bad, False, "sufficient source carrier requires material justification for derived replacement")

    bad = copy.deepcopy(base)
    bad["items"][1]["carrier_precedence_decision"] = "REUSE_DIRECT"
    bad["items"][1]["geometry_type"] = "DIRECT_SOURCE_VISUAL"
    bad["items"][1]["redraw_justification"] = "N/A"
    run(bad, False, "direct reuse cannot be claimed when source carrier is insufficient")

    bad = copy.deepcopy(base)
    bad["items"][2]["decision_question_ref"] = "ANOTHER-QUESTION"
    run(bad, False, "translation item cannot drift away from upstream Decision Question")

    bad = copy.deepcopy(base)
    bad["items"][1]["task_critical_invariants"].append("POSITION")
    run(bad, False, "task-critical invariant cannot be relaxed without named external support")

    good = copy.deepcopy(base)
    good["items"][1]["task_critical_invariants"].append("POSITION")
    good["items"][1]["externally_preserved_invariants"]["POSITION"] = "GEOGRAPHIC-EVIDENCE-LAYER"
    run(good, True, "relaxed task-critical invariant may be carried by explicit external layer")

    good = copy.deepcopy(base)
    good["items"][0]["carrier_precedence_decision"] = "REUSE_DIRECT"
    good["items"][0]["geometry_type"] = "DIRECT_SOURCE_VISUAL"
    good["items"][0]["redraw_justification"] = "N/A"
    good["items"][0]["graphic_carrier_id"] = "FIXTURE-RIVER-BANKS"
    good["items"][0]["derivation_method"] = "direct source visual reuse"
    run(good, True, "authoritative source may be reused directly without redraw")

if __name__ == "__main__":
    main()
