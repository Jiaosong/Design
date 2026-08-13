# Automotive v0.11｜M7 Secondary Geometry Decision

Status: `M7 PASS / R29A + M6 LOCKED / M8 MAY OPEN`

## Scope

M7 PASS validates a Modeling Worker secondary-geometry dependency workflow. It does not validate production wheelhouse construction, glazing certification, sealing, fastening or manufacturing feasibility.

## Canonical machine evidence

Run: `31621603164`

Artifact: `9151463754` / `oleander-automotive-v0-11-m7-31621603164`

Digest: `sha256:05b4136fac444e1b683d4f53c71bf1403ecec2a85f891a72577c913201945a97`

R29A primary Source hash before M7:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

R29A primary Source hash after M6 metadata, M7 secondary construction and M7 diagnostic render:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

Machine gate confirms:
- Source topology remains 2909 vertices / 2793 faces / 4 triangles / 2789 quads / 0 n-gons;
- Source remains one island;
- M6 routing assignments remain exact;
- canonical 0.700 m wheel package remains exact;
- four wheelhouse secondary objects exist with exact canonical wheel centers;
- wheelhouse radial clearance = 55 mm, explicitly tagged `DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION`;
- all wheelhouse dependencies resolve to M6 region/package IDs;
- glazing shell starts from exactly 220 `REG-GLASSHOUSE` routing faces;
- glazing shell is a separate editable object;
- glazing thickness = 4 mm and source-surface offset = 1.5 mm, both explicitly tagged as modeling-validation estimates;
- five secondary IDs are unique;
- all secondary objects have `SECONDARY_GEOMETRY_WORKING` authority;
- affected-view routing exists for every secondary object;
- four M7 diagnostic views completed.

## Human M7 review

### PASS — front wheelhouse
The near-side front wheelhouse follows the corrected wheel package and remains visually inside the exterior fender opening. It does not project through the R29A crown or become a new exterior design feature.

### PASS — rear wheelhouse
The rear wheelhouse remains contained within the quarter/opening relation. The visible liner clearance is coherent for a modeling benchmark and does not require reopening the primary Source.

### PASS — glazing shell
The separated glazing shell remains aligned with the M6 glasshouse region in both front and rear Hero diagnostics. No material duplicate-surface tearing, exploded boundary, or obvious shell inversion is present at the current diagnostic scale.

### PASS — hierarchy
Secondary wheelhouse and glazing objects remain visually subordinate to the locked R29A body. Diagnostic colors do not imply material/CMF authority.

### PASS — framing / occlusion
Wheelhouse detail views isolate the near-side package sufficiently to judge liner/opening relation. Hero views provide enough glazing context without changing the M5 camera authority.

## Authority boundary

M7 values are benchmark estimates:
- wheelhouse radial clearance: 55 mm;
- glazing thickness: 4 mm;
- glazing diagnostic surface offset: 1.5 mm.

These values are not engineering specifications and do not imply supplier, tooling, sealing, homologation or production feasibility.

## Gate transition

`M5 PASS → M6 PASS → M7 PASS → M8 DETAIL / INSTANCES MAY OPEN`

M8 must preserve:
- canonical R29A Source hash;
- M6 routing metadata;
- M7 secondary component identities/dependencies.

No Notion/Drive canonical promotion and no PR merge are authorized yet.
