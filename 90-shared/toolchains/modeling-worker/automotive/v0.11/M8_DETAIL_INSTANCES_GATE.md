# Automotive v0.11｜M8 Detail / Instances Gate

Status: `M8 OPEN / M5-M7 LOCKED / M9 BLOCKED`

## Purpose

M8 validates repeated-detail instancing and dependency routing without reopening the passed R29A primary Source or M7 secondary geometry.

This is not a wheel-design or production engineering approval. Wheel detail dimensions are designer-estimate benchmark parameters used to validate linked-instance behavior.

## Locked authority

Primary Source hash:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

M6 routing and M7 secondary component identities remain locked.

M8 must not alter:
- R29A Source geometry/topology;
- M6 routing assignments;
- M7 wheelhouse/glazing secondary meshes;
- canonical 0.700 m wheel HP package;
- wheel centers / Y thickness.

## M8 benchmark detail families

### A｜Wheel spoke instances
Prototype:
`PROTO-WHEEL-SPOKE`

Instances:
- 10 spokes per wheel;
- 40 linked instances total;
- all instances must share one mesh datablock;
- radial placement follows canonical wheel centers;
- prototype radial span begins at 115 mm and ends at 275 mm;
- nominal spoke width 28 mm;
- nominal spoke depth 16 mm.

All values are `DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION`.

### B｜Wheel rim-ring instances
Prototype:
`PROTO-WHEEL-RIM-RING`

Instances:
- one ring per wheel;
- 4 linked instances total;
- all instances must share one mesh datablock;
- nominal major radius 245 mm;
- nominal tube radius 8 mm.

All values are benchmark values, not wheel engineering specifications.

## Dependency routing

Every detail instance must resolve to:
- one `PKG-WHEEL-*` component;
- canonical `CONTRACT-WHEEL-HP`;
- no direct authority over R29A Source.

Affected-view policy must be explicit so a wheel-detail revision does not rerender unrelated Source views.

## Machine gate

M8 machine PASS requires:
- R29A Source hash before/after detail construction unchanged;
- M7 secondary mesh signatures before/after unchanged;
- canonical wheel HP package exact;
- exactly 40 spoke instances / 10 per wheel;
- all 40 spoke objects share one prototype mesh datablock;
- exactly 4 rim-ring instances;
- all 4 ring objects share one prototype mesh datablock;
- only two detail prototype mesh datablocks exist for the two instance families;
- all instance IDs unique;
- all package/dependency references resolve;
- spoke/ring radial envelopes remain inside the 0.700 m wheel OD;
- prototypes are non-rendering library objects;
- instance objects have `DETAIL_INSTANCE` authority, not primary/secondary authority;
- selective affected-view matrix exists for both families;
- lightweight detail diagnostic renders complete.

## Human M8 review

- spoke pattern is centered on each canonical wheel;
- no wheel instance is mirrored or rotated inconsistently;
- spokes/ring do not visibly exceed tire OD;
- detail scale does not overpower the vehicle benchmark;
- front/rear near-side detail views control occlusion sufficiently;
- Hero views confirm repeated details remain subordinate to Source/secondary geometry;
- no styling judgment should be inferred from the generic spoke count or proportions.

## Gate transition

If M8 PASS:
`M8 PASS → M9 MATERIAL BINDING MAY OPEN`

No Notion/Drive canonical promotion and no PR merge are implied by M8 PASS.
