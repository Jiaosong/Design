#!/usr/bin/env python3
import copy, json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / 'tools' / 'validate_visual_surface_treatment.py'
FIXTURE = Path(__file__).with_name('VISUAL-SURFACE-01_REGISTER.json')


def run(data, should_pass, label):
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        p = Path(f.name)
    cp = subprocess.run([sys.executable, str(VALIDATOR), str(p)], capture_output=True, text=True)
    p.unlink(missing_ok=True)
    if (cp.returncode == 0) != should_pass:
        print(cp.stdout)
        print(cp.stderr)
        raise SystemExit('regression failed: ' + label)
    print('PASS regression:', label)


def main():
    base = json.loads(FIXTURE.read_text(encoding='utf-8'))
    run(base, True, 'positive surface fixture')

    bad = copy.deepcopy(base)
    bad['surfaces'][0]['mapped_variable'] = ''
    run(bad, False, 'analytical gradient requires mapped variable')

    bad = copy.deepcopy(base)
    bad['surfaces'][0]['gradient_stops'] = ['ONE']
    run(bad, False, 'gradient requires at least two stops')

    bad = copy.deepcopy(base)
    bad['surfaces'][0]['attack_tests']['gradient_off'] = ''
    run(bad, False, 'gradient requires OFF-state review')

    bad = copy.deepcopy(base)
    bad['surfaces'][1]['semantic_owner_id'] = ''
    run(bad, False, 'texture without semantic owner must fail')

    bad = copy.deepcopy(base)
    bad['surfaces'][1]['density_range'] = ''
    run(bad, False, 'texture requires density range')

    bad = copy.deepcopy(base)
    bad['surfaces'][1]['material_truth_state'] = 'REAL_BECAUSE_IT_LOOKS_REAL'
    run(bad, False, 'material texture cannot self-promote material truth')

    bad = copy.deepcopy(base)
    bad['surfaces'][2]['mapped_variable'] = 'risk'
    run(bad, False, 'hierarchy opacity cannot masquerade as mapped data')

    bad = copy.deepcopy(base)
    bad['surfaces'][2]['off_state_result'] = 'CORE_GEOMETRY_LOST'
    run(bad, False, 'surface treatment cannot be sole carrier of core geometry')

    bad = copy.deepcopy(base)
    bad['surfaces'][3]['near_mid_far_review']['far'] = ''
    run(bad, False, 'multi-scale review must include far read')

    bad = copy.deepcopy(base)
    bad['surfaces'][3]['promotion'] = 'KEEP'
    run(bad, True, 'nested irrelevant promotion key does not alter top-level non-promotion')

    bad = copy.deepcopy(base)
    bad['promotion'] = 'KEEP'
    run(bad, False, 'machine surface register cannot award KEEP/promotion')

if __name__ == '__main__':
    main()
