# Automotive v0.11｜M9 Material Binding Decision

Status: `M9 PASS / M5-M8 LOCKED / M10 MAY OPEN / NOT FINAL CMF`

## Scope

M9 PASS validates semantic material binding only. It does not approve final CMF, supplier systems, resin grades, paint stacks, glazing certification or production processes.

## Canonical machine evidence

Run: `31622919537`

Artifact: `9151984130` / `oleander-automotive-v0-11-m9-31622919537`

Digest: `sha256:ba3234f0e4912f41d42079fe50c873c7a9be237996f57eda574e21c852a82ee7`

Primary Source hash before/after binding and rendering:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

Machine gate confirms:
- Source topology unchanged: 2909 vertices / 2793 faces / 4 triangles / 2789 quads / 0 n-gons;
- M6 region assignments retained;
- M7 secondary geometry signatures unchanged;
- M8 prototype geometry unchanged;
- M8 instance transforms unchanged;
- M8 linked-mesh relationships remain one spoke prototype mesh and one rim-ring prototype mesh;
- canonical 0.700 m wheel package remains exact;
- exactly six required benchmark material IDs exist;
- all semantic binding targets resolve;
- Source material coverage is exact;
- exactly 220 `REG-GLASSHOUSE` Source faces receive `MAT-GLASSHOUSE-BACKER`;
- four wheelhouses receive `MAT-WHEELHOUSE-DARK-POLYMER`;
- four canonical HP tire objects receive `MAT-TIRE-RUBBER`;
- `SEC-GLAZING-SHELL` receives `MAT-GLAZING-NEUTRAL`;
- spoke/ring prototype mesh datablocks receive `MAT-WHEEL-DETAIL-METAL`, inherited by all 44 linked instances;
- authority labels remain unchanged;
- six material bindings have explicit affected-view policies;
- four material diagnostic renders completed.

## Human M9 review

### PASS — material completeness
No missing/pink fallback material is visible in Side, Hero Front, Hero Rear or Front Wheel diagnostics.

### PASS — body / glasshouse routing
The neutral body coat remains on non-glasshouse Source faces. The dark glasshouse backer remains confined to the 220 routed glasshouse faces and does not leak onto the body-main regions.

### PASS — separated glazing
The M7 glazing shell remains visibly subordinate to the body Source. Transparency/reflection is readable without a material exploded edge or severe duplicate-surface tearing at the current benchmark scale.

### PASS — wheelhouse / tire hierarchy
Wheelhouse binding remains inside the exterior arch. Tire binding remains on the four exact canonical HP tire objects only. The wheelhouse does not become an exterior CMF feature.

### PASS — linked detail binding
Spoke and rim-ring families share a neutral metallic benchmark through their two linked prototype mesh datablocks. All four wheels remain consistent.

### PASS — framing / lighting
The four diagnostic views provide enough broad, side and wheel-detail context to verify binding without implying final CMF approval.

## Neutral benchmark registry

- `MAT-BODY-NEUTRAL-COAT` — coated non-metal benchmark;
- `MAT-GLASSHOUSE-BACKER` — dark opaque diagnostic backer;
- `MAT-GLAZING-NEUTRAL` — transparent dielectric benchmark;
- `MAT-WHEELHOUSE-DARK-POLYMER` — rough dark secondary benchmark;
- `MAT-TIRE-RUBBER` — high-roughness tire benchmark;
- `MAT-WHEEL-DETAIL-METAL` — neutral metallic linked-detail benchmark.

All remain `BENCHMARK_MATERIAL / NOT_FINAL_CMF`.

## Gate transition

`M5 PASS → M6 PASS → M7 PASS → M8 PASS → M9 PASS → M10 MULTI-SCALE QA MAY OPEN`

No Notion/Drive canonical promotion and no PR merge are authorized yet.
