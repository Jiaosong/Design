#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path


def fail(msg):
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def req(o, keys, where):
    miss=[k for k in keys if k not in o]
    if miss: fail(f"{where}: missing {miss}")


def main():
    if len(sys.argv)!=4:
        print("usage: validate_effect_extension_02.py FIXTURE STATIC_RECIPES MOTION_RECIPES")
        raise SystemExit(2)
    d=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    s=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
    m=json.loads(Path(sys.argv[3]).read_text(encoding='utf-8'))
    if d.get('promotion') not in {'NO_PROMOTION','NO'}: fail('fixture must remain non-promoted')
    sids={r['recipe_id'] for r in s.get('recipes',[])}; mids={r['recipe_id'] for r in m.get('recipes',[])}
    expected_static={f'SVG-R{i:02d}-' for i in range(11,19)}
    if not all(any(rid.startswith(prefix) for rid in sids) for prefix in expected_static): fail('static extension recipes R11..R18 incomplete')
    expected_motion={f'TD-MR{i:02d}-' for i in range(13,21)}
    if not all(any(rid.startswith(prefix) for rid in mids) for prefix in expected_motion): fail('motion extension recipes MR13..MR20 incomplete')

    for i in d.get('static_instances',[]):
        where=i.get('instance_id','?'); req(i,['recipe_id','semantic_owner_id','surface_role','off_state','review'],where)
        if i['recipe_id'] not in sids: fail(f'{where}: unknown static recipe')
        if not i['semantic_owner_id']: fail(f'{where}: semantic owner required')
        if i['recipe_id']=='SVG-R12-HALFTONE':
            req(i,['mapped_variable','legend_id','domain','mapping'],where)
        if i['recipe_id']=='SVG-R14-BLEND-OVERLAY':
            req(i,['source_pass_id','pass_truth_state','blend_mode','color_space','alpha_mode'],where)
        if i['recipe_id']=='SVG-R15-DASH-RHYTHM':
            req(i,['legend_id','meaning','dash_array'],where)
            if 'direction' in i['meaning'].lower() and 'no direction' not in i['meaning'].lower(): fail(f'{where}: dash may not silently assert direction')
        if i['recipe_id']=='SVG-R16-HILLSHADE-PASS':
            req(i,['source_pass_id','source_binding','registration_ref','azimuth_deg','altitude_deg'],where)
        if i['recipe_id']=='SVG-R17-AO-DEPTH-PASS':
            req(i,['source_pass_id','camera_ref','geometry_revision_ref','object_id_mask_ref'],where)
        if i['recipe_id']=='SVG-R18-SOURCE-CLIP-REVEAL' and i.get('required_labels_preserved') is not True:
            fail(f'{where}: source clip must preserve required labels')

    for i in d.get('motion_instances',[]):
        where=i.get('instance_id','?'); req(i,['recipe_id','semantic_owner_id','motion_role','reduced_motion','runtime_state'],where)
        if i['recipe_id'] not in mids: fail(f'{where}: unknown motion recipe')
        if not i['reduced_motion']: fail(f'{where}: reduced motion required')
        if i['runtime_state'] not in {'DESIGNED_NOT_RUN','PENDING_RUNTIME','RUNTIME_REVIEWED','EXECUTED_SELF_CHECKED'}: fail(f'{where}: invalid runtime state')
        if i['recipe_id']=='TD-MR13-TOPOLOGY-SAFE-MORPH':
            req(i,['state_a_id','state_b_id','correspondence_map','topology_class','intermediate_state_policy'],where)
        if i['recipe_id']=='TD-MR14-REFRACTION-DISPLACEMENT':
            req(i,['registration_class','mask_id','scale_from_px','scale_to_px','seed'],where)
            if i['registration_class'] in {'MAP_BOUND','AUTHORITY','SOURCE_AUTHORITY'}: fail(f'{where}: refraction cannot move authoritative/map geometry')
        if i['recipe_id']=='TD-MR16-CAMERA-ORBIT-DOLLY-FOCUS':
            req(i,['model_authority_ref','camera_start','camera_end','static_projection_refs'],where)
        if i['recipe_id']=='TD-MR17-CURSOR-LINKED-RESPONSE':
            req(i,['pointer_baseline','touch_fallback','keyboard_fallback'],where)
            if i['pointer_baseline'] is not True: fail(f'{where}: pointer baseline required')
        if i['recipe_id']=='TD-MR18-SMOOTH-SCROLL-INFRA':
            req(i,['native_scroll_baseline','nested_scroll_policy','focus_keyboard_policy','rollback_plan'],where)
            if i['native_scroll_baseline'] is not True: fail(f'{where}: native scroll baseline required')
        if i['recipe_id']=='TD-MR19-VIEW-TRANSITION': req(i,['stable_anchor_id','navigation_baseline'],where)
        if i['recipe_id']=='TD-MR20-DRAG-INERTIA': req(i,['bounds','interrupt_behavior','keyboard_equivalent'],where)
    print(f"PASS: extension fixture static={len(d.get('static_instances',[]))}, motion={len(d.get('motion_instances',[]))}; no runtime/design KEEP awarded")

if __name__=='__main__': main()
