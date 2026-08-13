# Modeling Worker v0.12｜E1 Human M4.5 Decision

Status: `E1 M4.5 PASS / SINGLE-PATCH METHOD SCOPE / M5 MAY OPEN FOR E1 ONLY / SYSTEM v0.12 REMAINS CANDIDATE`

## Decision scope

This decision reviews the first real Blender execution of the v0.12 relationship-driven freeform method.

It answers only whether the E1 single bicubic patch demonstrates the intended architectural chain:

`Design Relationship IR → sparse editable Control Cage → analytic evaluation surface → derived execution mesh → machine fairness evidence → human visual fairness review`

It does **not** approve a complete Automotive body, multi-patch continuity, termination architecture, Class-A surfacing, engineering CAD, manufacturing, production paneling or final design quality.

Automotive v0.11 R29A remains the existing promoted execution-benchmark Canonical Authority. E1 does not mutate or supersede it.

## Executed evidence

GitHub Actions run: `31662589694`

Head SHA: `5f903eef64aaa2f5c7445609d7829c62ee7a4625`

Artifact: `9166761243` / `oleander-modeling-worker-v0-12-e1-31662589694`

Artifact digest:
`sha256:dcbcbba61284774c37e9aba328e4aef283cb31ecc7a8f37aa4a993433fc0cb7d`

Artifact contains 8 files:
- `OLEANDER_ModelingWorker_v0.12_E1_Freeform.blend`;
- `E1_RELATIONSHIP_IR.json`;
- `E1_CONTROL_CAGE.json`;
- `E1_FREEFORM_FAIRNESS.json`;
- `E1_HERO_3Q.png`;
- `E1_SIDE.png`;
- `E1_TOP.png`;
- `E1_ZEBRA_NORMAL_PROXY.png`.

Machine status:
`MACHINE_PASS_HUMAN_M4_5_REVIEW_REQUIRED`

AI Governance Evals run `31662589698`: `SUCCESS`.

## Machine fairness evidence

Surface source:
- analytic single bicubic Bezier patch;
- sparse `4 × 4` Control Cage;
- `16` control points;
- evaluated grid `61 × 31`;
- execution mesh is derived geometry, not Surface Source Authority.

Measured metrics:
- minimum surface Jacobian: `3.6365913098354428` ≥ `0.20`;
- maximum adjacent-normal jump: `3.232204420564652°` ≤ `5.0°`;
- p95 adjacent-normal jump: `2.757815658446046°`;
- maximum center-silhouette tangent jump: `0.7102816490018041°` ≤ `4.0°`;
- maximum mean-curvature-rate proxy: `1.7705103240564257` ≤ `8.0`;
- maximum absolute mean curvature: `1.0566666881893336`;
- maximum absolute Gaussian curvature: `0.10642675158856049`.

All declared machine checks passed:
- Relationship IR present;
- low-frequency cage retained;
- topology derived from Surface Source;
- non-degenerate Jacobian;
- normal flow stable under the declared proxy;
- silhouette derivative stable under the declared proxy;
- curvature-rate proxy bounded;
- smooth shading explicitly excluded as fairness evidence.

These metrics are conservative benchmark proxies, not Class-A certification.

## Human M4.5 visual review

### `E1_HERO_3Q` — PASS

- broad surface reads as one coherent low-frequency volume;
- no visible faceting, topology crease, isolated local brow or uncontrolled bulge is introduced by the derived execution mesh;
- sparse cage/primary-curve diagnostics remain subordinate enough to expose the broad shape rather than conceal it;
- the transition from high center volume toward side/lower volume is visually continuous at the scale required by E1.

### `E1_SIDE` — PASS

- the evaluated silhouette is visibly smoother than the sparse cage polygon and is not simply a smoothed copy of execution topology;
- no obvious flat spot, tangent break or local crown spike is visible through the central flow;
- the result supports the intended separation between low-frequency design control and higher-resolution derived geometry.

### `E1_TOP` — PASS WITH BOUNDARY

- broad plan flow is continuous and free of local topology chatter;
- the simple near-rectilinear plan character is accepted only because E1 tests the method, not a final Automotive plan-view design;
- no claim is made that the current plan proportion or side-volume distribution is a retained Automotive design solution.

### `E1_ZEBRA_NORMAL_PROXY` — PASS FOR INTERIOR / TERMINATION OPEN

- stripes remain continuous through the principal interior surface and do not show abrupt single-line breaks or local double-kinks;
- stripe acceleration is gradual over the main patch, consistent with the machine normal/curvature-rate evidence;
- the left/open end shows strong stripe convergence/compression. This is treated as an **unvalidated termination boundary**, not hidden or promoted as a complete surface solution;
- minor jaggedness at stripe edges is attributable to the diagnostic render/raster pattern and is not used as geometry evidence.

## Human decision

`E1 M4.5 = PASS` within the explicitly bounded single-patch method scope.

The E1 result is sufficient to establish that v0.12 has moved beyond a governance-only proposal: it can compile explicit design relationships into a sparse Surface Source, derive deterministic geometry, calculate analytic differential evidence and survive human visual fairness review without relying on smooth shading as the authority.

Therefore:

`E1 M4.5 PASS → E1 M5 MAY OPEN`

This transition applies to the E1 generic freeform benchmark only.

## What remains blocked

The following are **not** unlocked by E1:
- Automotive v0.12 full-body M5;
- Automotive M6–M10;
- multi-patch G1/G2 authority;
- front/rear termination authority;
- wheel-opening / greenhouse / hood-fender / haunch surface-network authority;
- system-level Candidate → Canonical promotion.

## Required next benchmark｜E2

E2 must test a real multi-patch relationship network rather than another isolated single patch.

Minimum E2 questions:
1. Can two or more editable patches preserve declared `G1` and applicable `G2` relationships across shared boundaries?
2. Can shared boundary authority remain semantic and stable when neighboring volume controls change?
3. Can termination volumes be constructed as their own surface network rather than mesh closure?
4. Can the worker report boundary tangent/curvature mismatch numerically and fail closed before visual review?
5. Can zebra/reflection evidence distinguish interior fairness from boundary fairness?

Until E2 passes, the strongest supported system statement is:

> `Modeling Worker v0.12 can understand explicit design relationships and generate a quality-stable analytic single-patch freeform surface under a sparse control-cage workflow.`

The broader statement “quality-stable freeform model” remains a **System Candidate objective**, not yet Canonical authority.
