# Automotive v0.11｜M6 Component Architecture Gate

Status: `M6 OPEN / R29A M5 SOURCE LOCKED / M7-M8 BLOCKED`

## Purpose

M6 does not add styling detail. It converts the validated R29A primary Source into a semantically addressable modeling asset so future workers can rebuild only the dependent region instead of regenerating the whole model.

## Locked authority

Canonical M5 Source:
`OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R29A`

Executed M5 Source hash:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

M6 must not change:
- Source vertex coordinates;
- Source face membership / topology;
- R09 hard points;
- canonical 0.700 m wheel HP package contract;
- R11/R12 non-wheel surface decisions;
- R18/R20 terminations;
- R25 rounded opening scale;
- R29A shoulder-fed crown relation.

## M6 semantic model

The R29A Source remains **one geometry authority**. M6 face regions are routing masks, not physical panel separations.

Required semantic regions:
- `REG-GLASSHOUSE`
- `REG-FRONT-FENDER-L`
- `REG-FRONT-FENDER-R`
- `REG-REAR-QUARTER-L`
- `REG-REAR-QUARTER-R`
- `REG-FRONT-TERMINATION`
- `REG-REAR-TERMINATION`
- `REG-BODY-MAIN-L`
- `REG-BODY-MAIN-R`
- `REG-UNDERBODY-CENTER`

Required package components:
- `PKG-WHEEL-FL`
- `PKG-WHEEL-FR`
- `PKG-WHEEL-RL`
- `PKG-WHEEL-RR`

## Meaning of a region

A region defines:
- semantic target ID;
- dependency references;
- affected-view policy;
- selective rebuild scope;
- future M7 attachment responsibility.

It does **not** imply:
- hood/door/fender physical panel seams;
- manufacturing split lines;
- separate body objects;
- thickness or fastening logic;
- detail authority.

Those belong to later gates.

## Machine gate

M6 may PASS only if:
- R29A Source shape hash before annotations == after annotations == canonical M5 hash;
- Source remains one mesh island;
- topology remains 4 triangles / 0 n-gons / no Boolean / no global SubD;
- every Source face belongs to exactly one routing region;
- every required region has non-zero coverage;
- left/right paired regions have plausible symmetric coverage;
- all component IDs are unique;
- every dependency reference resolves;
- all four wheel package components satisfy canonical HP contract;
- a selective-rebuild matrix exists for every region;
- derived diagnostic component maps are explicitly `AUTHORITY=NONE`.

## Human M6 review

Use component-map diagnostics to verify:
- front/rear wheel-zone masks follow the intended bounded crown regions;
- termination masks do not invade the main body;
- glasshouse is isolated from primary body routing;
- underbody center is not confused with left/right body regions;
- diagnostic framing/occlusion does not hide region errors;
- no routing boundary is being mistaken for a design seam.

## Gate transition

If M6 PASS:
`M6 PASS → M7 Secondary Geometry MAY OPEN`

M8 Detail / Instances remains blocked until M7 review.

No Notion/Drive canonical promotion or PR merge is implied by M6 PASS.
