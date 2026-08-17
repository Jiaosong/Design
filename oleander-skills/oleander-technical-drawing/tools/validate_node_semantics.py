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
allowed = {
 'JUNCTION','ENTRY_EXIT','TRANSFER','DECISION','STOP_REST','OBSERVATION',
 'CONTENT_READING','SERVICE','RETURN_RETREAT','THRESHOLD_TRANSITION',
 'CONFLICT_CROSSING','TERMINUS_CONTINUATION','CALLOUT_TARGET'
}

nodes = reg.get('nodes', [])
edge_ids = {e['id'] for e in reg.get('edges', [])}
seen = set()
for n in nodes:
    nid=n.get('id')
    if not nid or nid in seen: errors.append(f'bad/duplicate node id: {nid}')
    seen.add(nid)
    cls=n.get('node_class')
    if cls not in allowed: errors.append(f'{nid}: invalid node_class {cls}')
    carrier=n.get('graphic_carrier_id')
    if carrier and carrier not in ids: errors.append(f'{nid}: missing graphic carrier {carrier}')
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
    if n.get('truth_state') is None: errors.append(f'{nid}: truth_state required')
    if n.get('position_confidence') is None: errors.append(f'{nid}: position_confidence required')

# edge endpoint registration
node_ids = {n.get('id') for n in nodes}
for e in reg.get('edges', []):
    for k in ('start_node','end_node'):
        if e.get(k) not in node_ids: errors.append(f"{e.get('id')}: invalid {k} {e.get(k)}")

if reg.get('promotion_state') not in ('NOT_PROMOTED','CANDIDATE_NOT_PROMOTED'):
    errors.append('promotion_state must remain non-promoted for fixture/reconstruction validation')

if errors:
    print('NODE SEMANTICS: FAIL')
    for e in errors: print('-', e)
    raise SystemExit(1)
print(f'NODE SEMANTICS: STRUCTURE PASS / nodes={len(nodes)} / edges={len(edge_ids)}')
print('NOTE: structure PASS does not equal source completeness, Design KEEP, field truth, or project promotion.')
