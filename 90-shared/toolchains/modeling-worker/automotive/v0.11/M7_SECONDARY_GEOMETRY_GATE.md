# Automotive v0.11｜M7 Secondary Geometry Gate

Status: `M7 OPEN / M5-M6 LOCKED / M8 BLOCKED`

## Purpose

M7 verifies that secondary geometry can be generated from the passed M6 routing/dependency architecture without modifying the validated R29A primary Source.

This is a Modeling Worker benchmark. M7 does not claim production body engineering, real wheelhouse construction, regulatory glazing design, sealing, fastening or manufacturing feasibility.

## Locked authority

Primary Source:
`R29A M5 PASS`

Canonical Source hash:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

Semantic architecture:
`M6 PASS`

M7 must not modify:
- R29A Source coordinates or topology;
- M6 routing assignments / IDs;
- R09 hard points;
- 0.700 m canonical wheel HP package;
- R25 rounded wheel-opening scale;
- R29A shoulder-fed crown relation;
- R18/R20 terminations.

## M7 benchmark families

### A｜Secondary wheelhouse liners
Required objects:
- `SEC-WHEELHOUSE-FL`
- `SEC-WHEELHOUSE-FR`
- `SEC-WHEELHOUSE-RL`
- `SEC-WHEELHOUSE-RR`

Dependencies:
- corresponding `REG-FRONT-FENDER-*` or `REG-REAR-QUARTER-*`;
- corresponding `PKG-WHEEL-*`;
- `CONTRACT-WHEEL-HP`.

Construction benchmark:
- wheel center must equal canonical hard point;
- liner arch radius = wheel radius + designer-estimate validation clearance;
- validation clearance starts at 55 mm;
- liner is a separate editable secondary mesh;
- no Boolean cut is applied to the Source;
- value is a modeling-validation estimate, not an engineering wheelhouse clearance.

### B｜Separated glazing shell
Required object:
- `SEC-GLAZING-SHELL`

Dependencies:
- `REG-GLASSHOUSE`;
- `SEC-R09-R12-GREENHOUSE`;
- `SRC-R29A`.

Construction benchmark:
- derived from exactly the M6 glasshouse routing faces;
- separated from Source as its own editable mesh;
- thin-shell thickness starts at 4 mm as a designer-estimate visualization parameter;
- shell creation must not change Source geometry;
- no claim of production glazing thickness, curvature certification or sealing design.

## Machine gate

M7 may PASS machine validation only if:
- Source hash before and after secondary construction equals canonical R29A M5 hash;
- Source topology remains 2909 vertices / 2793 faces / 4 triangles / 0 n-gons;
- M6 region assignments remain unchanged;
- all four wheel package components remain exact under `wheel_hp_contract.py`;
- four wheelhouse objects exist and are uniquely identified;
- every wheelhouse center resolves to the corresponding canonical wheel center;
- wheelhouse radial clearance equals the declared validation parameter;
- wheelhouses reference valid M6 region/package dependencies;
- glazing shell is generated from exactly the 220 `REG-GLASSHOUSE` Source faces before shell thickening;
- glazing shell is a separate object with `SECONDARY_GEOMETRY` authority;
- all secondary IDs are unique;
- no secondary object is mislabeled as primary Source authority;
- selective affected-view policy exists for each secondary object;
- lightweight M7 diagnostic renders complete.

## Human M7 review

Wheelhouse:
- visually follows the wheel package and opening;
- does not visibly protrude through the exterior fender crown in the diagnostic view;
- near/far wheel occlusion is controlled;
- clearance reads as a secondary envelope, not a new exterior design feature.

Glazing shell:
- aligns to the M6 glasshouse routing region;
- does not create obvious duplicate-surface tearing or exploded edges;
- remains visually subordinate to the locked R29A body Source.

General:
- check scale/proportion;
- check cropping/framing;
- check occlusion;
- distinguish secondary geometry from diagnostic material color;
- do not infer manufacturing seams from M6 masks.

## Gate transition

If both M7 families pass machine and Human review:
`M7 PASS → M8 DETAIL / INSTANCES MAY OPEN`

M8 remains blocked until this decision is recorded.

No Notion/Drive canonical promotion and no PR merge are implied by M7 PASS.
