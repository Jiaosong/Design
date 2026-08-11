#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

root = Path(__file__).resolve().parent
active = json.loads((root / 'ACTIVE.json').read_text(encoding='utf-8'))
assert active['schema'] == 'oleander.blender-surface-system.active.v2'
assert active['active_version'] == 'v1.15'
assert active['version_policy'] == 'CONTINUOUSLY_UPDATED_GLOBAL_SYSTEM'
assert active['active_track_status'] == 'C_TRACK_RENDERED_DIAGNOSTIC_PASS'


def semantic_sha(value):
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()

for key in ('material_process_archetypes', 'texture_node_recipes'):
    meta = active['components'][key]
    p = root / meta['path']
    assert p.is_file(), p
    value = json.loads(p.read_text(encoding='utf-8'))
    actual = semantic_sha(value)
    expected = meta['semantic_sha256']
    assert actual == expected, f'{key} semantic SHA mismatch: {actual} != {expected}'

binding_path = root / 'integrations' / 'xj01' / 'xj01_surface_binding.json'
binding = json.loads(binding_path.read_text(encoding='utf-8'))
expected_roles = {
    'MAT_IRON_VISIBLE', 'MAT_PP_PRIMARY_FIELD', 'MAT_PP_SECONDARY',
    'MAT_PP_UI', 'MAT_PU_CONTACT', 'MAT_METAL_HARDWARE'
}
assert binding['schema'] == 'oleander.xj01.surface-binding.v2'
assert set(binding['roles']) == expected_roles
assert binding['stage_policy'] == 'R02_SURFACE_LOCKED_COLOR_ONLY'
assert binding['surface_system_policy']['minimum_active_version'] == 'v1.15'
assert binding['c_track_integration']['automatic_application'] == 'DISABLED'
assert active['render_response_signature'] == '44a462645344c996872c5d3cf80b73e2d9a448d26d34356e8918fb60951642ac'
print(json.dumps({'status':'PASS','active_version':active['active_version'],'xj01_roles':len(expected_roles),'c_track':active['active_track_status']}))
