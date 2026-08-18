#!/usr/bin/env python3
import json, sys
from pathlib import Path

ROLES = {
    'ANALYTICAL_FIELD', 'MATERIAL_SURFACE', 'HIERARCHY_RECESSION',
    'PRESENTATIONAL_ATMOSPHERE', 'REFERENCE_FIDELITY'
}
TECHNIQUES = {
    'GRADIENT','HATCH','LINE_TEXTURE','STIPPLE','POINT_TEXTURE','PATTERN','GRAIN',
    'MACRO_VEIN_LAYER_ABRASION','OPACITY','SHADOW','BLUR','GLOW','EDGE_MODULATION'
}
MATERIAL_STATES = {
    'SOURCE_CONFIRMED','DESIGN_HYPOTHESIS','REFERENCE_VISIBLE_ONLY','NON_MATERIAL_PRESENTATION'
}
TRUTH_STATES = {'SOURCE','INFERENCE','ASSUMPTION','DECISION','NON_EVIDENCE','REFERENCE'}
REQUIRED = {
    'surface_id','semantic_owner_id','surface_role','source_basis','truth_state',
    'technique','does_not_prove','off_state_result','near_mid_far_review'
}
TEXTURE_TECHNIQUES = {
    'HATCH','LINE_TEXTURE','STIPPLE','POINT_TEXTURE','PATTERN','GRAIN','MACRO_VEIN_LAYER_ABRASION'
}


def fail(msg):
    print('FAIL:', msg)
    raise SystemExit(1)


def nonempty(v):
    return v is not None and v != '' and v != [] and v != {}


def main():
    if len(sys.argv) != 2:
        fail('usage: validate_visual_surface_treatment.py VISUAL_SURFACE_REGISTER.json')
    data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    if data.get('promotion') not in {'NO','NO_PROMOTION','CANDIDATE_NOT_PROMOTED'}:
        fail('surface register must remain non-promoted')
    items = data.get('surfaces')
    if not isinstance(items, list) or not items:
        fail('surfaces must be a non-empty list')

    seen = set()
    for i, s in enumerate(items):
        miss = REQUIRED - set(s)
        if miss:
            fail(f'surface {i} missing fields: {sorted(miss)}')
        sid = s['surface_id']
        if not sid or sid in seen:
            fail(f'bad/duplicate surface_id: {sid}')
        seen.add(sid)
        if not nonempty(s['semantic_owner_id']):
            fail(f'{sid}: semantic_owner_id required')
        if s['surface_role'] not in ROLES:
            fail(f'{sid}: invalid surface_role')
        if s['technique'] not in TECHNIQUES:
            fail(f'{sid}: invalid technique')
        if s['truth_state'] not in TRUTH_STATES:
            fail(f'{sid}: invalid truth_state')
        if not nonempty(s['source_basis']):
            fail(f'{sid}: source_basis required')
        if not nonempty(s['does_not_prove']):
            fail(f'{sid}: does_not_prove required')
        nmp = s['near_mid_far_review']
        if not isinstance(nmp, dict) or set(('near','mid','far')) - set(nmp):
            fail(f'{sid}: near_mid_far_review must include near/mid/far')
        if any(not nonempty(nmp[k]) for k in ('near','mid','far')):
            fail(f'{sid}: near/mid/far review entries cannot be empty')

        role = s['surface_role']
        tech = s['technique']

        # Presentation-only surface cannot claim evidentiary truth.
        if role == 'PRESENTATIONAL_ATMOSPHERE' and s['truth_state'] != 'NON_EVIDENCE':
            fail(f'{sid}: PRESENTATIONAL_ATMOSPHERE must be NON_EVIDENCE')

        # Analytical fields require an actual variable and a legend/scale reference.
        if role == 'ANALYTICAL_FIELD':
            if not nonempty(s.get('mapped_variable')):
                fail(f'{sid}: ANALYTICAL_FIELD requires mapped_variable')
            if not nonempty(s.get('legend_or_scale_ref')):
                fail(f'{sid}: ANALYTICAL_FIELD requires legend_or_scale_ref')
        elif role in {'HIERARCHY_RECESSION','PRESENTATIONAL_ATMOSPHERE'}:
            if nonempty(s.get('mapped_variable')) and str(s.get('mapped_variable')).upper() != 'NONE':
                fail(f'{sid}: {role} must not masquerade as mapped data')

        # Gradient needs explicit formation logic and an OFF-state attack test.
        if tech == 'GRADIENT':
            for k in ('gradient_axis','gradient_stops','interpolation','why_gradient'):
                if not nonempty(s.get(k)):
                    fail(f'{sid}: gradient requires {k}')
            if not isinstance(s['gradient_stops'], list) or len(s['gradient_stops']) < 2:
                fail(f'{sid}: gradient_stops requires >=2 stops')
            attacks = s.get('attack_tests', {})
            if not nonempty(attacks.get('gradient_off')):
                fail(f'{sid}: gradient requires gradient_off attack test')

        # Texture/pattern/grain needs scale/density/direction/mask/variation logic.
        if tech in TEXTURE_TECHNIQUES:
            for k in ('texture_scale','density_range','directionality','local_mask','variation_strategy'):
                if not nonempty(s.get(k)):
                    fail(f'{sid}: {tech} requires {k}')
            attacks = s.get('attack_tests', {})
            if not nonempty(attacks.get('texture_off')):
                fail(f'{sid}: texture technique requires texture_off attack test')

        # Material surfaces must declare what kind of material truth they have.
        if role == 'MATERIAL_SURFACE':
            ms = s.get('material_truth_state')
            if ms not in MATERIAL_STATES:
                fail(f'{sid}: MATERIAL_SURFACE requires valid material_truth_state')

        # Uncertainty opacity must be explicitly explained with a scale/legend.
        if tech == 'OPACITY' and s.get('opacity_maps_uncertainty'):
            if not nonempty(s.get('legend_or_scale_ref')):
                fail(f'{sid}: uncertainty opacity requires legend_or_scale_ref')

        # Glow as analysis must have a luminous/light-field basis, otherwise it is presentation.
        if tech == 'GLOW' and role == 'ANALYTICAL_FIELD' and not nonempty(s.get('physical_light_basis')):
            fail(f'{sid}: analytical GLOW requires physical_light_basis')

        # Explicit off-state cannot say core geometry disappears.
        if str(s['off_state_result']).upper() in {'CORE_GEOMETRY_LOST','TOPOLOGY_LOST','GEOMETRY_DEPENDS_ON_SURFACE'}:
            fail(f'{sid}: surface treatment may not be sole carrier of core geometry/topology')

    print(f'PASS: {len(items)} visual-surface contracts structurally valid')
    print('NOTE: PASS does not award visual quality, material truth, professional finish, Design KEEP, Engineering PASS, Field PASS or Promotion.')

if __name__ == '__main__':
    main()
