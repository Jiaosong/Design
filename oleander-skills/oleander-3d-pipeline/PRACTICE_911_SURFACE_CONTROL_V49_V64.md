# Porsche 911 Carrera 992.2 — Surface Control vs Evaluated Sampling Practice Readback

Status: **CANDIDATE L7 PRACTICE BINDING / KNOWLEDGE PRACTICE PASS / DESIGN REJECT / NO SILENT PROMOTION**

Purpose: reuse the existing Porsche 911 Carrera 992.2 Blender benchmark as native-runtime evidence for the modeling-essence, differential-geometry and SubD/surface-control knowledge stack. This record does not claim that the vehicle reproduction itself passed reference fidelity or professional Design KEEP.

## 1. Immutable source identity

- source benchmark PR: `Jiaosong/Design#208` — `OLEANDER 3D Skill validation: Porsche 911 Carrera 992 reference reproduction`;
- benchmark head: `8cdcf7eefdb256fed9ea334c5dfb19db0d170254`;
- V59 runtime source commit: `5db053b1a07b9fef824b77cb2d20e5838502f3ca`;
- native runtime: Blender `5.2.0 LTS`;
- V59 Actions run: `32271258341`, conclusion `success`;
- V59 Actions artifact: `9372267675`, name `oleander-porsche-911-992-v58-v59-32271258341`;
- artifact digest: `sha256:49a709070d18b4053d7a50927e8184cb2b7d54dde6b6b655dc089593e42caa64`;
- native files confirmed inside artifact: V58 and V59 `.blend` files plus six-view rendered PNGs, source-control tables and machine/reproduction receipts.

Hard-point authority in the benchmark remains Porsche 992.2 technical/reference data; the experiment is a reference-reproduction study, not manufacturer CAD.

## 2. Knowledge exercised

Primary:
- `EVD-MODELING-SUBDIVISION-LIMIT-SURFACE-20260830-001`;
- `EVD-MODELING-REPRESENTATION-BANDWIDTH-20260830-001`;
- `EVD-CG-SURFACE-CONTINUITY-001`;
- `EVD-FORM-DIFFERENTIAL-GEOMETRY-20260830-001`;
- `KN-THEORY-3D-MODELING-ESSENCE-001`.

Supporting:
- `KN-METHOD-3D-REFERENCE-CALIBRATION-001`;
- `KN-METHOD-OLEANDER-3D-MODELING-001`;
- `KN-METHOD-DCC-POLYGON-SUBD-001`;
- `KN-METHOD-BLENDER-PRODUCTION-001`.

## 3. Decision questions

1. Does increasing the pre-SubD Source cage density necessarily improve the evaluated surface?
2. Can a sparse Source cage be valid when the evaluated surface is already densely sampled?
3. When a local metric improves but held-out visual identity worsens, which representation layer owns the failure?
4. Can machine surface PASS, reference-fidelity REJECT and professional-design REJECT all be simultaneously correct?

## 4. Controlled evidence chain

### V49 — sparse no-fold LKG

V49 established a sparse feature-aligned Source cage with no adjacent-normal folds on the evaluated body surface. It remained visually weak in front/rear identity. This is the baseline for the density experiments, not a Design KEEP.

### V53–V55 — failure localization before repair

- V53 localized folds: `FRONT 64 / MID 0 / REAR 126 = 190 total`.
- V54 showed that changing the evidence carrier can change a gross-profile conclusion; carrier scope is part of claim validity.
- V55 attempted long cabin-blend/lower-return repair and worsened to `409 folds`; the hypothesis was rejected rather than preserved because it looked smoother in one view.

### V56 — densification A/B falsification

Only one primary variable changed from the V49 relation set: insert one pre-SubD midpoint between adjacent positive-half section controls, increasing ring controls from `20 → 40`.

Result: `380 folds`.

Finding: **pre-SubD midpoint insertion is not neutral Derived sampling**. It modifies/reveals the subdivision limit-surface behavior and can make the surface worse.

`SOURCE CONTROL DENSITY ↑ ≠ SURFACE QUALITY ↑`.

### V57/V58 — representation-bandwidth separation

The stable sparse Source/evaluated relation was measured as:
- Source semantic rails: `9`;
- Source ring controls: `20`;
- evaluated carrier: `4,382 vertices / 13,140 edges / 8,760 faces / 17,520 triangles`;
- adjacent-normal folds: `0`.

This establishes the practical separation:

`SOURCE CONTROL DENSITY ≠ EVALUATED SURFACE SAMPLING ≠ SURFACE FAIRNESS ≠ DESIGN QUALITY`.

V58 additionally exposed an evidence-contract error: the older V49 surface FAIL classification was not proof that more Source controls were required. The correct repair was to fix the evidence contract, not densify the cage.

### V59 — one sparse semantic relation edit

Authorized Source edit: `FRONT_HOOD_FENDER_RELATION` only.

Machine readback:
- Source ring controls: `20`;
- evaluated triangles: `17,520`;
- adjacent-normal folds: `0`;
- hood/fender delta: `0.048726445226940474 m`;
- side regression: PASS;
- rear regression: PASS.

The local hood-center versus fender-crown hierarchy improved without breaking the fold-free evaluated surface.

Actual six-view preview readback, however, remained visually REVISE/REJECT: the held-out front 3/4 still reads as a generic/toy sports-car proxy rather than convincing 992.2 identity.

Root cause from Artifact Review: `APERTURE_ARCHITECTURE_NOT_OWNED` — windshield, side glazing, rear glass, A/C pillars and roof-rail junctions remained proxy/infill overlays rather than one shared-boundary host-opening-interface-infill-backing architecture.

Therefore the next authorized variable was **not** cage density, camera, rear primary body or cosmetic render treatment. It was `GREENHOUSE_APERTURE_ARCHITECTURE_ONLY`.

### V64 — metric improvement / design degradation counterexample

V64 retained `20` Source ring controls, `17,520` evaluated triangles and `0 folds`; rear body-only RMSE improved from `0.17242950469411836 → 0.07731869503709972` while regression locks passed.

Artifact Review still gave `professional_design_gate = REJECT` and `verdict = REJECT_EXPERIMENT_KEEP_EVIDENCE` because the upper rear pinched into longitudinal ridges and the greenhouse-to-haunch relationship remained structurally wrong.

Root cause: `RELATION_OWNERSHIP_WRONG_FOR_VISIBLE_REAR_ARCHITECTURE`.

Authorized response: rollback primary body to V59 and resolve greenhouse/aperture ownership before another rear taper attempt.

`METRIC IMPROVEMENT ≠ FORM RELATION CORRECT ≠ DESIGN KEEP`.

## 5. Native artifact readback

The V59 Actions artifact was re-retrieved on 2026-08-30 before expiry. It contains:
- `out/V58_BASELINE/OLEANDER_PORSCHE_911_CARRERA_992_REFERENCE_REPRO.blend` — 797,152 bytes;
- `out/V59_HOOD_FENDER/OLEANDER_PORSCHE_911_CARRERA_992_REFERENCE_REPRO.blend` — 798,356 bytes;
- six PNG previews for each state;
- reference, projection, regression, Source-control and surface receipts.

Direct visual readback of V59 `HERO_FRONT_3Q` and `FRONT_ORTHO` confirms the recorded Design Crit: primary body continuity is visibly cleaner than the unresolved glazing/pillar/opening architecture, and the model remains a generic proxy despite the machine-surface PASS.

This is a native-artifact practice record because the `.blend` and rendered evidence were actually produced by Blender 5.2 and re-openable artifact bytes were recovered. The current ChatGPT execution environment did not contain Blender, so no new 2026-08-30 `.blend` mutation was fabricated.

## 6. Practice conclusions promoted

The following propositions are **PRACTICED** by this benchmark:

1. Source control density and evaluated tessellation/sampling are separate variables.
2. Increasing Source cage density can worsen SubD surface behavior even when intended as 'sampling'.
3. A fold-free machine surface can still fail reference fidelity and professional form quality.
4. A local metric can improve while the visible relation becomes less correct.
5. Failure localization should precede Source edits; repair the relation-owner layer, not the most convenient geometry layer.
6. Held-out 3/4 views can reveal structural identity failures that orthographic/gross metrics do not close.
7. Artifact Review can legitimately return `MACHINE PASS + DESIGN REJECT + KEEP EVIDENCE`.

## 7. What remains HOLD

This practice does **not** prove:
- successful Porsche 992.2 reference reproduction;
- Class-A/G3 automotive surface quality;
- NURBS/CAD parity;
- aerodynamic performance;
- manufacturer CAD;
- production aperture construction;
- engineering/manufacturing readiness;
- physical CMF;
- MAIN/portfolio KEEP.

Rhino/NURBS comparison remains unexecuted until an actual `.3dm` runtime is available; do not infer NURBS superiority or parity from this Blender case.

## 8. Maturity decision

- **Practice object:** M6 PRACTICED for the seven propositions in §6.
- **Parent theory:** remains broader than this single benchmark; do not promote all differential geometry, all SubD theory or the full Bio–Math stack to M6 from one car case.
- **Artifact/design:** REJECT / REVISE, no promotion.
- **Knowledge evidence:** KEEP.

## 9. Reopen triggers

Reopen this practice conclusion only if a controlled same-source experiment demonstrates one of the following:
- a densification operator that provably preserves the same limit surface while changing only evaluated sampling;
- a different subdivision scheme/crease/boundary policy invalidating the current density conclusion;
- native NURBS/SubD same-source comparison showing a representation-specific alternative;
- new actual previews showing the prior failure was camera-only rather than structural.
