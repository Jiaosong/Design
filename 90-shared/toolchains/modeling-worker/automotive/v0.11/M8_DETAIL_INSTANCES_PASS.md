# Automotive v0.11｜M8 Detail / Instances Decision

Status: `M8 PASS / M5-M7 LOCKED / M9 MAY OPEN`

## Scope

M8 PASS validates linked-instance behavior, package-centered placement and selective dependency routing. It does **not** approve the generic 10-spoke form as wheel styling or engineering design.

## Canonical machine evidence

Run: `31622289173`

Artifact: `9151727429` / `oleander-automotive-v0-11-m8-31622289173`

Digest: `sha256:da85cf98a575b06bfe13e598541f6004a75aac91c910ae49d8ede5b125a74fe9`

R29A primary Source hash before M8:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

R29A primary Source hash after detail construction and rendering:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

Machine gate confirms:
- Source topology remains 2909 vertices / 2793 faces / 4 triangles / 2789 quads / 0 n-gons;
- M6 routing assignments remain unchanged;
- M7 secondary mesh signatures remain unchanged;
- canonical 0.700 m wheel package remains exact;
- exactly 40 spoke instances exist, 10 per FL / FR / RL / RR wheel;
- all 40 spokes share one prototype mesh datablock;
- exactly 4 rim-ring instances exist;
- all 4 rim rings share one prototype mesh datablock;
- exactly two detail prototype mesh datablocks exist;
- 44 detail instance IDs are unique;
- package and HP-contract dependencies resolve;
- spoke radial envelope ≈ 0.27536 m < 0.350 m wheel radius;
- rim-ring radial envelope = 0.253 m < 0.350 m wheel radius;
- prototypes are hidden library objects;
- instance authority is `DETAIL_INSTANCE`;
- affected-view routing is complete;
- four diagnostic renders completed.

The first M8 run produced all four images but failed before QA serialization because `WHEEL_RADIUS` was omitted from the script namespace. `revise_v011_r29a_m8_gatefix.py` restored `WHEEL_RADIUS = TARGET_OD / 2` only; no geometry or detail parameters changed.

## Human M8 review

### PASS — instance centering
Front and rear near-side detail views show the spoke/ring families centered on the canonical wheel package. No individual wheel reads as translated off-axis.

### PASS — repetition / rotation
Ten spokes are distributed consistently around each wheel. Front and rear instance patterns do not show a missing, duplicated, or grossly mis-rotated member.

### PASS — radial containment
Spokes and rim ring remain materially inside the tire OD in both machine envelope checks and detail views. No generic detail element becomes the outer wheel silhouette.

### PASS — hierarchy
In Hero Front / Rear diagnostics, the generic gold detail remains subordinate to the vehicle benchmark. It does not alter the passed R29A body proportion or M7 secondary geometry.

### PASS — occlusion / framing
Near-side detail cameras are sufficient to judge centering and clipping. Hero views confirm multi-wheel consistency. The colors are diagnostic-only and carry no CMF authority.

## Benchmark-only detail values

- spoke count: 10 / wheel;
- spoke radial start: 115 mm;
- spoke radial end: 275 mm;
- spoke width: 28 mm;
- spoke depth: 16 mm;
- rim-ring major radius: 245 mm;
- rim-ring tube radius: 8 mm.

All remain `DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION`.

## Gate transition

`M5 PASS → M6 PASS → M7 PASS → M8 PASS → M9 MATERIAL BINDING MAY OPEN`

M9 must test material-to-semantic-component binding without changing primary, secondary or detail geometry authority.

No Notion/Drive canonical promotion and no PR merge are authorized yet.
