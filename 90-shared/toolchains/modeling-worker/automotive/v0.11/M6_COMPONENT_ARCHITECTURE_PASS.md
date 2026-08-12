# Automotive v0.11｜M6 Component Architecture Decision

Status: `M6 PASS / R29A SOURCE LOCKED / M7 MAY OPEN / M8 BLOCKED`

## Scope

M6 PASS means the validated R29A primary Source is now semantically addressable for selective rebuild and later attachment routing. It does **not** mean the routing masks are physical body panels, manufacturing split lines, thickness definitions, fasteners or detail geometry.

## Canonical machine evidence

Run: `31621035044`

Artifact: `9151237407` / `oleander-automotive-v0-11-m6-31621035044`

Digest: `sha256:3ecb7c092a88b00ce3e96ffeb5359e241eb9b52829018239dcc90ca1dabd688e`

Canonical M5 Source hash before annotations:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

Source hash after M6 face metadata:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

Machine gate confirms:
- Source geometry hash unchanged;
- one Source island before/after;
- topology unchanged: 2909 vertices / 2793 faces / 4 triangles / 2789 quads / 0 n-gons;
- no Source modifiers;
- every Source face belongs to exactly one routing region;
- all 10 required regions have non-zero coverage;
- paired front-fender / rear-quarter / body-main regions are bilaterally symmetric by face count;
- all semantic IDs are unique;
- all dependency references resolve;
- four package wheels remain exact under canonical 0.700 m wheel HP contract;
- selective-rebuild matrix covers every routing region;
- diagnostic map remains `AUTHORITY=NONE`;
- four-view diagnostic matrix completed, including ground-hidden underside view.

## Region coverage

- `REG-GLASSHOUSE`: 220 faces
- `REG-FRONT-FENDER-L`: 511 faces
- `REG-FRONT-FENDER-R`: 511 faces
- `REG-REAR-QUARTER-L`: 463 faces
- `REG-REAR-QUARTER-R`: 463 faces
- `REG-FRONT-TERMINATION`: 14 faces
- `REG-REAR-TERMINATION`: 14 faces
- `REG-BODY-MAIN-L`: 260 faces
- `REG-BODY-MAIN-R`: 260 faces
- `REG-UNDERBODY-CENTER`: 77 faces

Total: 2793 / 2793 Source faces classified exactly once.

## Human M6 review

### PASS — wheel-zone masks
Front-fender and rear-quarter routing masks remain bounded around the validated wheel-zone/crown relations. Left/right coverage is symmetric. The masks are broad dependency regions and are not interpreted as physical fender/quarter panel seams.

### PASS — glasshouse
The glasshouse routing region is visibly isolated from the body-main routing regions and follows the existing R29A diagnostic glazing band without modifying the Source.

### PASS — terminations
Front and rear termination regions remain small, discrete routing caps. They do not invade the central body-main or wheel-zone routing masks.

### PASS — body-main L/R
Left/right body-main regions remain continuous and distinct. Diagnostic color boundaries are metadata visualization only; no design seam or geometric discontinuity is created.

### PASS — underbody center
The initial Side / Front 3Q / Rear 3Q matrix did not provide enough visibility because ground and wheel occlusion hid the underbody routing strip. This was correctly classified as diagnostic-coverage REVISE, not Source or semantic-architecture failure.

The second run adds `M6_COMPONENT_UNDERSIDE_3Q` with the ground hidden. The central underbody routing strip is readable and remains distinct from left/right body-main regions. Local wheel occlusion does not prevent the central-region judgment.

### PASS — framing / occlusion / scale
All four diagnostic views are sufficient for routing review. The underside view is explicitly diagnostic-only and carries no design-camera authority.

## Authority boundary

M6 regions are `ROUTING_ONLY`.

They may be used to:
- target selective rebuilds;
- route dependencies;
- attach later secondary geometry;
- choose affected QA views.

They may not be used as evidence for:
- production body panels;
- door/hood/fender manufacturing seams;
- glazing thickness;
- wheelhouse construction;
- lamps, handles, mirrors or other detail authority.

## Gate transition

`M5 PASS → M6 PASS → M7 SECONDARY GEOMETRY MAY OPEN`

M7 must keep the R29A Source hash locked and create secondary geometry as separately auditable dependents of M6 regions.

M8 Detail / Instances remains blocked until M7 review passes.

No Notion/Drive canonical promotion and no PR merge are authorized by this gate alone.
