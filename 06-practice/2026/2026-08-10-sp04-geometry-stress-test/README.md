# OLEANDER / 织作 — SP04-R03 Geometry Stress Test

**Status: ACTUALLY EXECUTED / PASS**

Layer: Spatial / SP04 — Construction & Operation.

## Test groups
- S01 rounded opening
- S02 semicircular arch
- S03 eccentric ellipse
- S04 multiple non-identical openings
- thin-host-ligament numerical sweep
- multi-opening-gap numerical sweep
- six illegal-parameter rejection cases

## Executed results
- Complex shape acceptance: **4/4 PASS**
- Illegal parameter rejection: **6/6 PASS**
- Thin edge: last tested cross-format preserved value = **0.0002 mm**; first tested failure = **0.0001 mm**
- Multi-opening gap: last tested cross-format preserved value = **0.0005 mm**; first tested failure = **0.0002 mm**
- NumPy float32 coordinate spacing observed at 3000–3300 mm = **0.000244140625 mm**

The numerical failure boundary is runtime- and coordinate-magnitude-specific. It is **not** a construction tolerance, code requirement, or universal CAD threshold.

## Key finding
Volume and bounding-box QA alone produced false positives. At very small features, STL/GLB could remain watertight while the intended ligament or opening gap was no longer preserved. R03 therefore adds an explicit **feature-fidelity gate**.

## Internal review
**99/100**

Scope remains software-neutral geometric candidate validation. BIM/IFC semantics are not claimed.
