from pathlib import Path
import json
import ezdxf
from ezdxf import units

OUT = Path('/mnt/data/oleander_dxf_units_validation')


def make_case(path: Path, with_units: bool):
    doc = ezdxf.new('R2018', setup=True)
    doc.units = units.MM if with_units else 0
    msp = doc.modelspace()
    pts = [(0, 0), (120, 0), (120, 60), (0, 60)]
    msp.add_lwpolyline(pts, close=True, dxfattribs={'layer': 'CUT'})
    doc.saveas(path)


def inspect_case(path: Path):
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    poly = next(iter(msp.query('LWPOLYLINE')))
    pts = [(float(x), float(y)) for x, y, *_ in poly.get_points('xy')]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    width = max(xs) - min(xs)
    height = max(ys) - min(ys)
    insunits = int(doc.header.get('$INSUNITS', 0))
    return {
        'file': path.name,
        'insunits': insunits,
        'unit_name': units.unit_name(insunits) if insunits in range(0, 25) else 'unknown',
        'bbox_numeric': [width, height],
        'closed': bool(poly.closed),
        'geometry_ok': abs(width - 120) < 1e-9 and abs(height - 60) < 1e-9 and bool(poly.closed),
        'units_explicit_mm': insunits == units.MM,
    }


bad = OUT / 'DXF_UNITS_BAD_UNDEFINED.dxf'
good = OUT / 'DXF_UNITS_REPAIRED_MM.dxf'
make_case(bad, False)
make_case(good, True)
results = {'before': inspect_case(bad), 'after': inspect_case(good)}
results['before_verdict'] = 'HOLD' if results['before']['geometry_ok'] and not results['before']['units_explicit_mm'] else 'UNEXPECTED'
results['after_verdict'] = 'PASS' if results['after']['geometry_ok'] and results['after']['units_explicit_mm'] else 'REVISE'
results['proven'] = [
    'DXF numeric geometry can roundtrip while units remain explicitly unitless',
    'Setting document units to millimeters persists as $INSUNITS=4 after save/reopen',
    'Geometry bbox remains 120 x 60 and polyline remains closed after repair',
]
results['not_proven'] = [
    'supplier/CAD application import scaling behavior',
    'paper/model-space plotting scale',
    'tolerance/GD&T correctness',
    'manufacturing or engineering approval',
]
(OUT / 'DXF_UNITS_ROUNDTRIP_RESULT.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
print(json.dumps(results, indent=2))
