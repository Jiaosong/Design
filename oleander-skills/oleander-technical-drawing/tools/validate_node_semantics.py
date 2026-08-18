#!/usr/bin/env python3
import json, sys, xml.etree.ElementTree as ET
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit('usage: validate_node_semantics.py NODE.svg NODE_REGISTER.json')
svg_path = Path(sys.argv[1]); reg_path = Path(sys.argv[2])
root = ET.parse(svg_path).getroot()
ids = {el.attrib.get('id') for el in root.iter() if el.attrib.get('id')}
reg = json.loads(reg_path.read_text(encoding='utf-8'))

errors = []
spatial_allowed = {
 'JUNCTION','ENTRY_EXIT','TRANSFER','DECISION','STOP_REST','OBSERVATION',
 'CONTENT_READING','SERVICE','RETURN_RETREAT','THRESHOLD_TRANSITION',
 'CONFLICT_CROSSING','TERMINUS_CONTINUATION','CALLOUT_TARGET'
}
interface_allowed = {
 'JOINT','REVEAL','SETBACK','TERMINATION','LAYER_TRANSITION',
 'DRAINAGE_INTERFACE','MOVEMENT_JOINT'
}
node_modes = {'SPATIAL_EVENT','CONSTRUCTION_INTERFACE'}

nodes = reg.get('nodes', [])
edge_ids = {e['id'] for e in reg.get('edges', [])}
seen = set()
for n in nodes:
    nid=n.get('id')
    if not nid or nid in seen: errors.append(f'bad/duplicate node id: {nid}')
    seen.add(nid)
    mode=n.get('node_mode')
    if mode not in node_modes:
        errors.append(f'{nid}: node_mode must be SPATIAL_EVENT or CONSTRUCTION_INTERFACE')
        continue
    cls=n.get('node_class')
    carrier=n.get('graphic_carrier_id')
    if carrier and carrier not in ids: errors.append(f'{nid}: missing graphic carrier {carrier}')
    if n.get('truth_state') is None: errors.append(f'{nid}: truth_state required')

    if mode == 'SPATIAL_EVENT':
        if cls not in spatial_allowed: errors.append(f'{nid}: invalid spatial-event node_class {cls}')
        con=n.get('connected_edge_ids', [])
        for e in con:
            if e not in edge_ids: errors.append(f'{nid}: unknown connected edge {e}')
        if cls == 'CALLOUT_TARGET' and con:
            errors.append(f'{nid}: callout target must not enter route topology')
        if cls == 'JUNCTION' and len(con) < 3:
            errors.append(f'{nid}: junction requires degree >=3')
        if cls == 'TRANSFER':
            modes=n.get('modes', [])
            if len(set(modes)) < 2: errors.append(f'{nid}: transfer requires >=2 distinct modes')
        if cls == 'RETURN_RETREAT' and not n.get('return_edge_ids'):
            errors.append(f'{nid}: Return node requires return_edge_ids')
        if cls == 'OBSERVATION' and not (n.get('view_target_id') or n.get('view_field_id')):
            errors.append(f'{nid}: observation node requires target or view field')
        if n.get('position_confidence') is None: errors.append(f'{nid}: position_confidence required for spatial event')

    if mode == 'CONSTRUCTION_INTERFACE':
        if cls not in interface_allowed:
            errors.append(f'{nid}: invalid construction-interface node_class {cls}')
        if n.get('connected_edge_ids'):
            errors.append(f'{nid}: construction interface must not silently enter route/event topology')
        components=n.get('component_ids')
        if not isinstance(components,list) or len(set(components or [])) < 2:
            errors.append(f'{nid}: construction interface requires >=2 component_ids')
            components=[]
        for c in components:
            if c not in ids: errors.append(f'{nid}: component {c} missing from SVG')
        primary=n.get('primary_component_id')
        if primary not in components:
            errors.append(f'{nid}: primary_component_id must belong to component_ids')
        attached=n.get('attached_component_ids')
        if not isinstance(attached,list) or not attached:
            errors.append(f'{nid}: attached_component_ids required')
        else:
            for c in attached:
                if c not in components: errors.append(f'{nid}: attached component {c} not in component_ids')
                if c == primary: errors.append(f'{nid}: primary component cannot also be attached component')
        if not isinstance(n.get('interface_type'),str) or not n['interface_type'].strip():
            errors.append(f'{nid}: interface_type required')
        if not isinstance(n.get('critical_interface_claim'),str) or not n['critical_interface_claim'].strip():
            errors.append(f'{nid}: critical_interface_claim required')
        if n.get('geometry_confidence') is None:
            errors.append(f'{nid}: geometry_confidence required for construction interface')
        if not n.get('does_not_prove'):
            errors.append(f'{nid}: does_not_prove required for construction interface')

# edge endpoint registration applies only to spatial-event topology.
node_ids = {n.get('id') for n in nodes if n.get('node_mode') == 'SPATIAL_EVENT'}
for e in reg.get('edges', []):
    for k in ('start_node','end_node'):
        if e.get(k) not in node_ids: errors.append(f"{e.get('id')}: invalid {k} {e.get(k)}")

if reg.get('promotion_state') not in ('NOT_PROMOTED','CANDIDATE_NOT_PROMOTED'):
    errors.append('promotion_state must remain non-promoted for fixture/reconstruction validation')

if errors:
    print('NODE SEMANTICS: FAIL')
    for e in errors: print('-', e)
    raise SystemExit(1)
print(f'NODE SEMANTICS: STRUCTURE PASS / nodes={len(nodes)} / spatial_edges={len(edge_ids)}')
print('NOTE: node-mode structure PASS does not equal source completeness, joint correctness, Design KEEP, field truth, or project promotion.')
