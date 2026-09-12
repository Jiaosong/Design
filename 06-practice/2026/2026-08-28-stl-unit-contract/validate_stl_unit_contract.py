#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import trimesh


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def close3(a, b, tol=1e-6):
    return len(a) == 3 and len(b) == 3 and all(math.isclose(float(x), float(y), rel_tol=0.0, abs_tol=tol) for x, y in zip(a, b))


def main():
    ap = argparse.ArgumentParser(description='Fail-closed STL exchange validation: STL geometry plus explicit external unit contract.')
    ap.add_argument('stl')
    ap.add_argument('--manifest', help='JSON sidecar declaring unit, expected bbox and artifact SHA256')
    args = ap.parse_args()

    stl = Path(args.stl)
    if not stl.exists():
        print('RESULT=HOLD REASON=STL_MISSING')
        return 78

    mesh = trimesh.load(stl, force='mesh')
    extents = [float(v) for v in mesh.extents]
    embedded_units = getattr(mesh, 'units', None)
    digest = sha256(stl)

    print(f'STL_SHA256={digest}')
    print('NUMERIC_BBOX=' + ','.join(f'{v:.6f}' for v in extents))
    print(f'EMBEDDED_UNITS={embedded_units!r}')

    if not args.manifest:
        print('RESULT=HOLD REASON=STL_HAS_NO_AUTHORITATIVE_UNIT_CONTRACT')
        return 78

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print('RESULT=HOLD REASON=UNIT_MANIFEST_MISSING')
        return 78

    meta = json.loads(manifest_path.read_text(encoding='utf-8'))
    required = ['artifact', 'sha256', 'declared_unit', 'expected_bbox', 'unit_authority']
    missing = [k for k in required if k not in meta]
    if missing:
        print('RESULT=HOLD REASON=MANIFEST_FIELDS_MISSING FIELDS=' + ','.join(missing))
        return 78

    if meta['artifact'] != stl.name:
        print('RESULT=HOLD REASON=MANIFEST_ARTIFACT_ID_MISMATCH')
        return 78
    if meta['sha256'] != digest:
        print('RESULT=HOLD REASON=MANIFEST_HASH_MISMATCH')
        return 78
    if not close3(meta['expected_bbox'], extents):
        print('RESULT=HOLD REASON=NUMERIC_BBOX_MISMATCH')
        return 78
    if meta['declared_unit'] not in {'mm', 'cm', 'm', 'in'}:
        print('RESULT=HOLD REASON=UNSUPPORTED_OR_UNDECLARED_UNIT')
        return 78
    if meta['unit_authority'] != 'EXTERNAL_MANIFEST_REQUIRED_FOR_STL':
        print('RESULT=HOLD REASON=UNIT_AUTHORITY_NOT_EXPLICIT')
        return 78

    print(f'DECLARED_UNIT={meta["declared_unit"]}')
    print('RESULT=PASS_FOR_BOUNDED_EXCHANGE REASON=HASH+BBOX+EXTERNAL_UNIT_CONTRACT_MATCH')
    print('NOT_PROVEN=DOWNSTREAM_IMPORT_SCALE,PRINTER_SLICER_SCALE,MANUFACTURING_APPROVAL,FIELD_TRUTH')
    return 0


if __name__ == '__main__':
    sys.exit(main())
