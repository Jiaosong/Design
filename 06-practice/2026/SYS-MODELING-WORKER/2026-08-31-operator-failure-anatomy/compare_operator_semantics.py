#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def first_where(records, predicate, key):
    for r in records:
        if predicate(r):
            return r.get(key)
    return None


def last_where(records, predicate, key):
    value = None
    for r in records:
        if predicate(r):
            value = r.get(key)
    return value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--freecad', required=True)
    ap.add_argument('--blender', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    f = json.loads(Path(args.freecad).read_text())
    b = json.loads(Path(args.blender).read_text())

    fillet_last_semantic = last_where(f['fillet'], lambda r: r.get('semantic_success', False), 'radius_mm')
    fillet_first_exception = first_where(f['fillet'], lambda r: r.get('failure_mode') == 'KERNEL_EXCEPTION', 'radius_mm')
    fillet_first_invalid = first_where(f['fillet'], lambda r: r.get('failure_mode') == 'INVALID_RETURNED_SHAPE', 'radius_mm')

    thickness_last_semantic = last_where(f['thickness'], lambda r: r.get('semantic_success', False), 'thickness_mm')
    thickness_first_exception = first_where(f['thickness'], lambda r: r.get('failure_mode') == 'KERNEL_EXCEPTION', 'thickness_mm')
    thickness_first_noop = first_where(f['thickness'], lambda r: r.get('failure_mode') == 'VALID_SEMANTIC_NOOP', 'thickness_mm')

    sphere_last_regular_inward = last_where(
        f['sphere_offset'],
        lambda r: r.get('semantic_success', False) and float(r.get('offset_mm', 0)) < 0,
        'offset_mm',
    )
    sphere_first_domain_failure = first_where(
        f['sphere_offset'],
        lambda r: not r.get('inside_regular_sphere_offset_domain', True),
        'offset_mm',
    )

    clamp_hi = next(r for r in b['bevel'] if r['clamp_overlap'] and r['requested_width_mm'] == 8.0)
    clamp_61 = next(r for r in b['bevel'] if r['clamp_overlap'] and r['requested_width_mm'] == 6.1)
    raw_hi = next(r for r in b['bevel'] if not r['clamp_overlap'] and r['requested_width_mm'] == 8.0)
    solid_u = b['solidify']['unapplied_scale']
    solid_a = b['solidify']['applied_scale_geometry']

    contract = {
        'both_native_workers_pass_bounded_contracts': bool(f['overall_pass'] and b['overall_pass']),
        'freecad_fillet_exception_and_invalid_return_are_distinct': fillet_first_exception is not None and fillet_first_invalid is not None,
        'freecad_thickness_valid_shape_can_be_semantic_noop': thickness_first_noop is not None,
        'freecad_thickness_exception_and_noop_are_distinct': thickness_first_exception is not None and thickness_first_noop is not None,
        'freecad_sphere_offset_hits_zero_radius_domain_boundary': sphere_first_domain_failure == -10.0,
        'blender_bevel_clamp_changes_realized_geometry': abs(clamp_hi['corner_clearance_mm'] - raw_hi['corner_clearance_mm']) > 0.05,
        'blender_bevel_clamp_saturates_realized_geometry': abs(clamp_hi['corner_clearance_mm'] - clamp_61['corner_clearance_mm']) < 1e-6,
        'blender_solidify_world_thickness_depends_on_transform_state': abs(solid_u['observed_world_thickness_mm'] - solid_a['observed_world_thickness_mm']) > 0.5,
        'same_ui_parameter_does_not_imply_same_operator_semantics': True,
    }
    overall = all(contract.values())
    result = {
        'schema': 'oleander.3d.operator-failure-anatomy.comparison.v2',
        'overall_pass': overall,
        'contract': contract,
        'observed_boundaries': {
            'freecad_fillet_last_semantic_success_radius_mm': fillet_last_semantic,
            'freecad_fillet_first_kernel_exception_radius_mm': fillet_first_exception,
            'freecad_fillet_first_invalid_return_radius_mm': fillet_first_invalid,
            'freecad_thickness_last_semantic_success_mm': thickness_last_semantic,
            'freecad_thickness_first_kernel_exception_mm': thickness_first_exception,
            'freecad_thickness_first_valid_semantic_noop_mm': thickness_first_noop,
            'freecad_sphere_last_regular_inward_offset_mm': sphere_last_regular_inward,
            'freecad_sphere_first_nonpositive_radius_offset_mm': sphere_first_domain_failure,
            'blender_bevel_requested_high_mm': 8.0,
            'blender_bevel_clamped_6_1_corner_clearance_mm': clamp_61['corner_clearance_mm'],
            'blender_bevel_clamped_8_corner_clearance_mm': clamp_hi['corner_clearance_mm'],
            'blender_bevel_raw_8_corner_clearance_mm': raw_hi['corner_clearance_mm'],
            'solidify_requested_mm': solid_u['requested_thickness_mm'],
            'solidify_unapplied_world_mm': solid_u['observed_world_thickness_mm'],
            'solidify_applied_world_mm': solid_a['observed_world_thickness_mm'],
        },
        'failure_taxonomy': [
            'KERNEL_EXCEPTION',
            'NULL_OR_NOT_DONE',
            'INVALID_RETURNED_SHAPE',
            'GEOMETRIC_EXPLOSION_OR_SELF_INTERSECTION',
            'VALID_SEMANTIC_NOOP',
            'POLICY_CLAMPED_RESULT',
            'TRANSFORM_DEPENDENT_REALIZED_VALUE',
            'SILENT_DRIFT',
        ],
        'production_consequences': [
            'OPERATOR PARAMETER VALUE != GUARANTEED REALIZED GEOMETRY',
            'KERNEL RETURN / IsValid != OPERATOR SEMANTIC SUCCESS',
            'KERNEL FAILURE != ONLY FAILURE MODE',
            'TOPOLOGICAL VALIDITY != DECLARED POSTCONDITION',
            'CLAMP/SOLVER POLICY IS PART OF OPERATOR SEMANTICS',
            'OBJECT TRANSFORM STATE CAN CHANGE WORLD-SPACE THICKNESS',
            'OFFSET/FILLET/SHELL MUST BE FAILURE-SWEPT AGAINST LOCAL AVAILABLE SPACE AND POSTCONDITIONS',
        ],
        'holds': [
            'Rhino native OffsetSrf/FilletSrf/Class-A parity',
            'general self-intersection repair',
            'manufacturing wall-thickness approval',
            'arbitrary topology',
            'all B-Rep kernels/modifier implementations',
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
