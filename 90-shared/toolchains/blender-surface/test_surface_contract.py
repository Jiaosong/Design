#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

root = Path(__file__).resolve().parent
active = json.loads((root / 'ACTIVE.json').read_text(encoding='utf-8'))
assert active['schema'] == 'oleander.blender-surface-system.active.v1'
assert active['version_policy'] == 'CONTINUOUSLY_UPDATED_GLOBAL_SYSTEM'
version = active['active_version']
vdir = root / 'versions' / version
assert vdir.is_dir(), version

component_files = {
    'material_process_archetypes': 'material_process_archetypes.json',
    'texture_node_recipes': 'texture_node_recipes.json',
}
for key, name in component_files.items():
    p = vdir / name
    assert p.is_file(), p
    json.loads(p.read_text(encoding='utf-8'))
    actual = hashlib.sha256(p.read_bytes()).hexdigest()
    expected_sha = active['components'][key]['raw_sha256']
    assert actual == expected_sha, f'{key} SHA mismatch: {actual} != {expected_sha}'

binding_path = root / 'integrations' / 'xj01' / 'xj01_surface_binding.json'
binding = json.loads(binding_path.read_text(encoding='utf-8'))
expected_roles = {
    'MAT_IRON_VISIBLE', 'MAT_PP_PRIMARY_FIELD', 'MAT_PP_SECONDARY',
    'MAT_PP_UI', 'MAT_PU_CONTACT', 'MAT_METAL_HARDWARE'
}
assert set(binding['roles']) == expected_roles
assert binding['stage_policy'] == 'R02_SURFACE_LOCKED_COLOR_ONLY'
print(json.dumps({'status':'PASS','active_version':version,'xj01_roles':len(expected_roles)}))
