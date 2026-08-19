# Primary Body Surface Grid Protocol v1

Status: CURRENT CANDIDATE / refined by the 992.2 V25–V57 benchmark.

## INPUT
- locked hard points and axle/wheel geometry;
- orthographic SIDE / FRONT / REAR reference envelopes;
- last-known-good per-gate baselines;
- sparse Source families for plan width, hood/deck spine, shoulder/fender crown, lower envelope and terminal return;
- declared final evaluated carrier for surface diagnostics.

## MUST CHECK
1. **Primary mass precedes detail.** Do not spend iterations on lamps, seams, CMF or trim while hood/fender/quarter/body section remains generic.
2. **Source control density ≠ evaluated surface density.** Sparse Source rails/cage own causal editability. Surface-quality density/sampling must be measured on the declared final evaluated carrier, never inferred from Source ring/control count.
3. **Dense evaluation does not replace sparse authority.** Subdivision/tessellation/evaluated sampling remains Derived. A dense evaluated surface may be regenerated from a sparse Source cage without promoting evaluated vertices to Source.
4. **Pre-SubD midpoint insertion is not neutral densification.** Adding midpoint controls to a Catmull–Clark or comparable control cage changes the control polygon and may change the limit surface, curvature distribution and fold behavior. Do not insert Source/cage points merely to satisfy an evaluated-density gate.
5. **Longitudinal and transverse causality are separate.** SIDE X/Z silhouette, plan width and Y/Z section must each be represented and independently screened.
6. **Wheel-arch / rocker / bumper lower envelope stays locked after it passes.** A new body representation cannot reopen passing lower geometry without an explicit failed-gate reason.
7. **Fender crown and rear haunch are part of the same body grid.** They are not floating volumes or detail meshes.
8. **Terminal plan curvature belongs in the body grid.** Do not close a production-like body with a constant-X flat cap and then cover it with fascia detail.
9. **Surface grid must remain locally ordered.** Adjacent rails/stations must not form bow-ties, inverted strips, stretched spikes or disconnected visible islands.
10. **Topology screening is not surface-quality proof.** Connected components = 1 and normal flips = 0 do not prove reflection flow, curvature fairness or reference fidelity.
11. **Representation experiments retain strict best-known locks.** Never widen regression thresholds because the new grid is exploratory.
12. **Actual 3/4 readback remains mandatory.** Orthographic compliance cannot prove body wrap, rear-engine mass distribution, fender-to-hood tension or shoulder flow.

## Source vs evaluated carrier contract

Persist separately:

### Source / control cage
- `source_state_class`;
- `source_semantic_rail_count`;
- `source_ring_control_count` or equivalent control-count metadata;
- protected families / Source digest.

These fields describe **causal control complexity**, not final surface quality. No universal minimum Source rail/ring count may be used as a machine surface-quality threshold.

### Final evaluated carrier
- `evaluated_carrier`;
- `evaluated_state_class`;
- evaluated vertices / edges / faces / triangles;
- evaluated connected components;
- evaluated adjacent-face normal/fold count;
- evaluated edge-spacing/sampling evidence at the declared review scale;
- optional curvature/reflection diagnostics.

The machine surface gate evaluates this carrier.

## Evaluated sampling gate

Sampling adequacy must declare its basis and review context. Examples:
- evaluated edge p95 / maximum spacing at a bounded review scale;
- tessellation chord-height / angle tolerance;
- subdivision level with verified final mesh statistics;
- screen-space or export-target sampling criterion.

The receipt must state:
- `basis`;
- `threshold_or_rule`;
- `observed`;
- `status = PASS / FAIL / HOLD`.

Forbidden basis: `SOURCE_RING_CONTROL_COUNT`.

A universal polygon count is not required. The sampling criterion must be appropriate to the target diagnostic/export and may remain HOLD if not yet justified.

## Legal densification

Allowed:
- increase SubD/evaluation level without changing Source controls when the evaluated result is verified;
- tessellate an evaluated NURBS/SubD/patch surface more finely;
- deterministically sample the already-defined evaluated/limit surface for diagnostics/export;
- regenerate a downstream mesh from unchanged Source with a tighter declared tolerance.

Not automatically legal:
- inserting midpoint controls into the Source/control cage;
- adding extra sections/rails before evaluation solely because a downstream density number is low;
- subdividing the Source representation and then claiming Source equivalence without proving the limit surface is unchanged.

If Source controls must be added, the reason must be **representation vocabulary / causal form control**, not evaluated sampling density.

## ALLOWED
- rebuild the primary body grid while preserving sparse causal Source semantics;
- use wheel/axle influence functions to create causal fender crowns;
- use Y-dependent terminal X setback for rounded nose/tail plan curvature;
- keep a simpler cabin during a body-surface experiment if aperture authority and visual review status remain explicit;
- increase evaluated sampling after Source definition when the evaluation method preserves the intended surface.

## FORBIDDEN
- `more polygons = higher fidelity`;
- `more Source cage points = denser evaluated surface` as a quality rule;
- lowering regression standards for a representation experiment;
- using separate visible blobs for front fender or rear haunch when the reference reads as one shell;
- adding detail to disguise boxy/faceted primary form;
- promoting a smoother mesh without independent visual KEEP;
- using pre-SubD midpoint insertion as a supposedly neutral evaluation-only operation.

## EVIDENCE
- Source-control digest and protected families;
- Source semantic/control counts, explicitly informational;
- final evaluated carrier identity and topology counts;
- evaluated sampling-gate basis/status;
- connected-component and adjacent-normal/fold evidence on the evaluated carrier;
- SIDE + FRONT + REAR projection receipts;
- front/rear 3/4 beauty views;
- regression receipt against best-known per-gate baselines;
- independent visual review before promotion.

Preferred current receipt schema: `oleander.3d.primary-body-surface-receipt.v2`.
Legacy v1 receipts remain provenance only and must not be used to justify new Source densification decisions.

## FAIL / HOLD
- `FAIL_PRIMARY_BODY_GRID_FOLD`
- `FAIL_PRIMARY_BODY_TERMINAL_CAP`
- `FAIL_PROTECTED_LOWER_ENVELOPE_REGRESSION`
- `FAIL_SOURCE_DENSITY_USED_AS_EVALUATED_GATE`
- `FAIL_DENSIFICATION_CHANGES_LIMIT_SURFACE`
- `REJECT_DENSE_GRID_GENERIC_FORM`
- `HOLD_EVALUATED_SAMPLING_BASIS_UNRESOLVED`
- `HOLD_REFLECTION_FLOW_NOT_REVIEWED`
- `HOLD_INDEPENDENT_VISUAL_KEEP_REQUIRED`

## 992.2 benchmark
V25–V29 showed that secondary/greenhouse topology could improve while the underlying primary body stayed generic. V30 therefore moved the causal frontier to the primary body grid.

V49 later established a sparse feature-aligned Source representation with **20 ring controls** and **0 fold inversions**. Its legacy surface receipt still failed because the old machine gate required `body_ring_vertices >= 30`.

V56 performed the causal A/B: keeping V49 Source relations unchanged and inserting one midpoint between adjacent positive-half cage controls increased the ring to 40 but produced **380 adjacent-face normal reversals**. Therefore pre-SubD cage densification was not a neutral Derived sampling operation.

V57 then audited V49 without geometry change. The same 20-control Source produced a final evaluated carrier with **4,382 vertices / 17,520 triangles / evaluated edge p95 ≈ 0.205 m / 0 normal flips**. This proves the old gate mixed Source control density with evaluated-surface density.

Transfer rule: **keep Source causally sparse; judge sampling on the final evaluated carrier; densify evaluation, not the Source cage, unless representation causality itself requires new controls.**

These benchmark findings repair machine-evidence semantics only. They do not promote V49 reference fidelity or Design Quality.
