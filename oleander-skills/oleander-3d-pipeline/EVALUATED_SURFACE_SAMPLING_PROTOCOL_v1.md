# OLEANDER 3D Evaluated Surface Sampling Protocol v1

Status: **CANDIDATE INTEGRATION / GENERAL 3D INVARIANT / 2026-08-19**

This protocol separates editable Source/control complexity from the density and quality of the final evaluated surface.

## Core separation

`SOURCE CONTROL DENSITY ≠ EVALUATED SURFACE SAMPLING ≠ SURFACE FAIRNESS ≠ DESIGN QUALITY`

A sparse NURBS/SubD/control-cage Source may produce a dense evaluated surface. Conversely, adding more Source controls may change the limit surface and make the form worse.

## Required routing

For every surface-density/sampling claim record:

`SOURCE REPRESENTATION → EVALUATION METHOD → FINAL EVALUATED CARRIER → SAMPLING METRIC → QUALITY BOUNDARY`

### Source layer
Record only causal control complexity:
- Source state/class;
- semantic rail/curve/section family count;
- control-point/ring/cage count where useful;
- Source digest/revision;
- protected relations.

These counts are **informational**, not a universal machine surface-quality threshold.

### Evaluated layer
Measure the actual carrier used by diagnostics/render/export:
- evaluated object/carrier identity;
- application/evaluation method and level/tolerance;
- evaluated vertices/edges/faces/triangles where mesh-backed;
- spacing/chord/angle/screen-space metric appropriate to the use;
- connectedness/fold/normal evidence where applicable;
- sampling gate basis, threshold/rule, observed value and status.

## Hard rule: no neutral pre-evaluation midpoint assumption

Inserting midpoint controls into a Catmull–Clark/SubD/NURBS/control cage is a **Source/representation edit** unless the representation mathematically proves limit-surface equivalence. It is not automatically a Derived sampling operation.

Therefore:
- do not add cage points merely to satisfy a downstream density number;
- do not call a subdivided control polygon Source-equivalent without proof;
- do not infer that `more Source controls = smoother or denser final surface`;
- if sampling is insufficient, first increase evaluation/tessellation/sampling **after Source definition**.

## Legal evaluation densification

Examples:
- higher SubD/evaluation level with Source unchanged;
- tighter NURBS/patch tessellation chord/angle tolerance;
- deterministic sampling of the already-defined evaluated/limit surface;
- higher export/render tessellation if verified not to change Source authority;
- screen-space sampling refinement for a declared final camera/output.

These operations remain Derived/evaluation state.

## When Source controls may increase

Only when the causal representation itself is insufficient, e.g.:
- needed identity rail/section/boundary is absent;
- curvature/termination relation cannot be expressed;
- shared-boundary/interface architecture requires a new Source family;
- repeated revise/root-cause routing proves a representation-vocabulary deficit.

The reason must be `REPRESENTATION_CAUSALITY`, not `EVALUATED_DENSITY_TARGET`.

## Sampling-gate contract

Every evaluated sampling gate must state:
- `basis`;
- `threshold_or_rule`;
- `observed`;
- `status = PASS / FAIL / HOLD`;
- review/export context.

Legal bases may include:
- evaluated edge p95/max spacing at bounded scale;
- tessellation chord-height/angle tolerance;
- screen-space projected edge length;
- evaluation subdivision level **plus verified final topology statistics**;
- domain-specific analysis sampling rule.

Forbidden basis: a raw Source control/ring count used as the evaluated surface sampling verdict.

## Quality boundary

Sampling PASS only proves the evaluated carrier is sufficiently sampled for the declared test. It does not prove:
- curvature fairness;
- reflection quality;
- G2/G3/Class-A;
- reference fidelity;
- engineering/manufacturing validity;
- Design KEEP / MAIN KEEP.

Fold-free/topologically clean evaluation remains separate from sampling adequacy, and both remain separate from design review.

## Failure routing

- sparse Source + dense/fold-free evaluated surface → do **not** densify Source;
- sparse Source + under-sampled evaluated surface → increase evaluation/tessellation first;
- evaluated surface dense but folded → route to Source/representation/topology causality, not more sampling;
- Source midpoint insertion changes folds/silhouette/curvature → classify as Source/representation edit and invalidate “sampling-only” comparison;
- sampling basis unresolved → `HOLD_EVALUATED_SAMPLING_BASIS_UNRESOLVED`.

## Evidence

`EVALUATED_SURFACE_SAMPLING_RECEIPT.json` containing:
- Source identity/state/control metadata;
- evaluated carrier/state;
- evaluation method;
- evaluated topology/sampling statistics;
- sampling gate;
- Source mutation status;
- result;
- does-not-prove.

## Benchmark provenance

Porsche 911 992.2 PR #208 exposed the invariant:
- V49: Source ring controls = 20, final evaluated mesh = 4,382 vertices / 17,520 triangles / edge p95 ≈ 0.205 m / 0 adjacent-normal folds.
- the legacy machine gate nevertheless rejected the surface because Source ring controls were below 30;
- V56 kept V49 Source relations but inserted one pre-SubD midpoint between adjacent half-section controls, raising the ring to 40 and producing 380 folds;
- V57 proved the original V49 final evaluated carrier was already dense and fold-free;
- V58 re-issued the unchanged V49 geometry with an evaluated-carrier surface gate and obtained `MACHINE_CONSTRUCTED_VISUAL_HOLD`, while Reference Fidelity remained REJECT and Design remained REVISE.

The benchmark proves an evidence/execution rule, not Porsche design quality.

## Does not prove

This protocol does not prove professional form quality, reference fidelity, physical truth, engineering validity, manufacturing readiness, Class-A continuity, Design KEEP or MAIN KEEP.
