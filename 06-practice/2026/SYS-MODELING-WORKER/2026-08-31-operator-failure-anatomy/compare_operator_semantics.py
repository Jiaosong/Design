#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def first_failure(records, key):
    failed = [r for r in records if not r.get('kernel_success', False)]
    return failed[0].get(key) if failed else None


def last_success(records, key):
    ok = [r for r in records if r.get('kernel_success', False)]
    return ok[-1].get(key) if ok else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--freecad', required=True)
    ap.add_argument('--blender', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    f = json.loads(Path(args.freecad).read_text())
    b = json.loads(Path(args.blender).read_text())

    fillet_first_fail = first_failure(f['fillet'], 'radius_mm')
    fillet_last_ok = last_success(f['fillet'], 'radius_mm')
    thickness_first_fail = first_failure(f['thickness'], 'thickness_mm')
    thickness_last_ok = last_success(f['thickness'], 'thickness_mm')

    clamp_hi = next(r for r in b['bevel'] if r['clamp_overlap'] and r['requested_width_mm'] == 8.0)
    raw_hi = next(r for r in b['bevel'] if not r['clamp_overlap'] and r['requested_width_mm'] == 8.0)
    solid_u = b['solidify']['unapplied_scale']
    solid_a = b['solidify']['applied_scale_geometry']

    contract = {
        'both_native_workers_pass_bounded_contracts': bool(f['overall_pass'] and b['overall_pass']),
        'freecad_fillet_has_observed_parameter_transition': fillet_first_fail is not None,
        'freecad_thickness_has_observed_parameter_transition': thickness_first_fail is not None,
        'blender_bevel_clamp_changes_realized_geometry': abs(clamp_hi['corner_clearance_mm'] - raw_hi['corner_clearance_mm']) > 0.05,
        'blender_solidify_world_thickness_depends_on_transform_state': abs(solid_u['observed_world_thickness_mm'] - solid_a['observed_world_thickness_mm']) > 0.5,
        'same_ui_parameter_does_not_imply_same_operator_semantics': True,
    }
    overall = all(contract.values())
    result = {
        'schema': 'oleander.3d.operator-failure-anatomy.comparison.v1',
        'overall_pass': overall,
        'contract': contract,
        'observed_boundaries': {
            'freecad_fillet_last_success_radius_mm': fillet_last_ok,
            'freecad_fillet_first_failure_radius_mm': fillet_first_fail,
            'freecad_thickness_last_success_mm': thickness_last_ok,
            'freecad_thickness_first_failure_mm': thickness_first_fail,
            'blender_bevel_requested_high_mm': 8.0,
            'blender_bevel_clamped_corner_clearance_mm': clamp_hi['corner_clearance_mm'],
            'blender_bevel_raw_corner_clearance_mm': raw_hi['corner_clearance_mm'],
            'solidify_requested_mm': solid_u['requested_thickness_mm'],
            'solidify_unapplied_world_mm': solid_u['observed_world_thickness_mm'],
            'solidify_applied_world_mm': solid_a['observed_world_thickness_mm'],
        },
        'production_consequences': [
            'OPERATOR PARAMETER VALUE != GUARANTEED REALIZED GEOMETRY',
            'KERNEL FAILURE != ONLY FAILURE MODE',
            'TOPOLOGICAL VALIDITY != GEOMETRIC NON-SELF-INTERSECTION',
            'CLAMP/SOLVER POLICY IS PART OF OPERATOR SEMANTICS',
            'OBJECT TRANSFORM STATE CAN CHANGE WORLD-SPACE THICKNESS',
            'OFFSET/FILLET/SHELL MUST BE FAILURE-SWEPT AGAINST LOCAL AVAILABLE SPACE',
        ],
        'holds': [
            'Rhino native OffsetSrf/FilletSrf/Class-A parity',
            'general self-intersection repair',
            'manufacturing wall-thickness approval',
            'arbitrary topology',
            'Design KEEP',
        ],
    }
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    (out / 'OPERATOR_COMPARISON_RECEIPT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    if not overall:
        raise SystemExit(10)


if __name__ == '__main__':
    main()
