#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import cadquery as cq
import trimesh

OUT = Path(__file__).resolve().parent / 'out'
OUT.mkdir(exist_ok=True)
stl = OUT / 'oleander_stl_unit_contract.stl'
manifest = OUT / 'oleander_stl_unit_contract.json'

# Training-only numeric fixture. The geometry is intentionally asymmetric in all three extents.
solid = cq.Workplane('XY').box(120, 60, 10, centered=(False, False, False))
cq.exporters.export(solid, str(stl))
raw = stl.read_bytes()
digest = hashlib.sha256(raw).hexdigest()
mesh = trimesh.load(stl, force='mesh')

meta = {
    'schema_version': '1.0',
    'artifact': stl.name,
    'sha256': digest,
    'declared_unit': 'mm',
    'expected_bbox': [120.0, 60.0, 10.0],
    'unit_authority': 'EXTERNAL_MANIFEST_REQUIRED_FOR_STL',
    'training_boundary': 'Synthetic fixture only; does not represent project or manufacturing dimensions.'
}
manifest.write_text(json.dumps(meta, indent=2) + '\n', encoding='utf-8')

print('STL=' + str(stl))
print('MANIFEST=' + str(manifest))
print('SHA256=' + digest)
print('NUMERIC_BBOX=' + ','.join(str(float(v)) for v in mesh.extents))
print('EMBEDDED_UNITS=' + repr(getattr(mesh, 'units', None)))
