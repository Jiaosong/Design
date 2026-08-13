# Modeling Worker v0.12｜E2 Human M4.5 Decision

Status: `E2 M4.5 PASS / MULTI-PATCH C2 METHOD SCOPE / GENERIC E2 M5 MAY OPEN / SYSTEM v0.12 REMAINS CANDIDATE`

## Decision scope

E2 tests whether explicit design relationships can compile a sparse editable center surface plus independent front/rear termination surfaces into a deterministic multi-patch freeform network with declared C2 seam behavior.

It validates the method chain:

`Relationship Contract → sparse Surface Sources → C2 seam compiler → independent termination patches → derived execution topology → quantitative seam/interior fairness evidence → Human Zebra/Reflection review`

It does **not** validate a complete Automotive body, final termination styling, Class-A production surfacing, engineering CAD, manufacturing, tooling, production paneling, crash/aero, homologation or final design quality.

Automotive v0.11 R29A remains the existing promoted execution-benchmark Canonical Authority. E2 does not mutate or supersede it.

## Executed evidence

GitHub Actions run: `31663588785`

Head SHA: `12bcfc466508d6734f575186c346303eda56eeef`

AI Governance Evals run: `31663588767` — `SUCCESS`.

Relationship + Surface Fairness Contract job: `SUCCESS`.

E1 + E2 Blender Freeform Surface job: `SUCCESS`.

E2 artifact:
- ID: `9167130592`;
- name: `oleander-modeling-worker-v0-12-e2-31663588785`;
- digest: `sha256:80027998682c61da92244a3998ee2cfccc9ac96074a14613dea298827f7fc178`;
- size: `860570 bytes`.

Artifact contains:
- `OLEANDER_ModelingWorker_v0.12_E2_MultiPatch.blend`;
- `E2_COMPILED_PATCH_NETWORK.json`;
- `E2_FREEFORM_FAIRNESS.json`;
- `E2_HERO_NETWORK.png`;
- `E2_SIDE_NETWORK.png`;
- `E2_TOP_NETWORK.png`;
- `E2_ZEBRA_NETWORK.png`.

Machine status:
`MACHINE_PASS_HUMAN_M4_5_REVIEW_REQUIRED`.

## Precision classification retained

The failed predecessor run was not retroactively converted into PASS.

The successful run separates:
1. `COMPILER_C2_RESIDUAL` from raw JSON/Python-float cages;
2. `BLENDER_MATHUTILS_REPRESENTATION_RESIDUAL` as bounded runtime evidence.

The original compiler design threshold remains:
`max_second_derivative_error <= 1e-06`.

Observed compiler-space seam evidence:

### Front seam
- max position error: `0.0`;
- max tangent angle: `1.2074182697257333e-06°`;
- max second-derivative error: `1.679699752964552e-15`.

### Rear seam
- max position error: `0.0`;
- max tangent angle: `1.2074182697257333e-06°`;
- max second-derivative error: `1.679699752964552e-15`.

Observed Blender runtime residuals remain separately bounded:
- front runtime second-derivative residual: `1.7560624912567418e-06`;
- rear runtime second-derivative residual: `2.068203875171837e-06`;
- candidate runtime representation tolerance: `5e-06`.

Runtime representation evidence does not replace or relax compiler-space C2 evidence.

## Patch interior machine fairness

### Front termination patch
- minimum Jacobian: `1.004175969082566`;
- max adjacent-normal jump: `3.8578290795561863°`;
- p95 adjacent-normal jump: `3.5707534623411514°`;
- max mean-curvature-rate proxy: `0.9666564997312844`.

### Center patch
- minimum Jacobian: `1.658784099568289`;
- max adjacent-normal jump: `3.9817546776087185°`;
- p95 adjacent-normal jump: `3.9059671376198675°`;
- max mean-curvature-rate proxy: `0.6391215524360361`.

### Rear termination patch
- minimum Jacobian: `0.9931158567036804`;
- max adjacent-normal jump: `3.857828935784673°`;
- p95 adjacent-normal jump: `3.574684031588301°`;
- max mean-curvature-rate proxy: `1.3050627125121832`.

All declared E2 machine checks passed, including termination-edit stability: front/rear far boundaries can change while the center cage remains unchanged and the compiled seams retain the declared relation.

## Human M4.5 visual review

### `E2_HERO_NETWORK` — PASS

- the three-patch construction reads as one continuous broad freeform volume rather than three visibly stitched mesh pieces;
- neither center↔termination seam produces a visible crease, isolated ridge or abrupt highlight event;
- sparse control-cage diagnostics remain readable without becoming the shape authority;
- front/rear terminations are visibly broad surface continuations rather than triangulated center-point mesh caps.

### `E2_SIDE_NETWORK` — PASS

- the principal silhouette passes across both seam locations without an observable tangent kink;
- center crown progression into both termination patches remains gradual;
- the seam positions are visible as diagnostic cage/guide locations, but the evaluated surface silhouette does not inherit those guide discontinuities;
- far front/rear edges remain open/truncated benchmark boundaries and are not treated as finished termination styling.

### `E2_TOP_NETWORK` — PASS WITH APPLICATION BOUNDARY

- plan-flow remains continuous across both compiled seams;
- no waist, bulge or local narrowing is introduced at the seam locations;
- the simple symmetric plan is accepted only as a multi-patch method benchmark, not as an Automotive design proposal.

### `E2_ZEBRA_NETWORK` — PASS FOR SEAMS / FAR TERMINATION BOUNDARIES OPEN

- reflection stripes cross the two center↔termination seams without a visible break, double kink or sudden phase shift;
- stripe flow over the principal center region is continuous and consistent with the numeric C2/normal evidence;
- front/rear far termination boundaries exhibit strong stripe compression and local loop/convergence behavior;
- this far-boundary behavior is explicitly classified as **termination styling / open-boundary work still required**, not a seam failure and not a finished product-surface result.

## Human decision

`E2 M4.5 = PASS` within the bounded multi-patch C2 method scope.

The strongest supported method statement is now:

> `Modeling Worker v0.12 can compile explicit design relationships into sparse editable multi-patch Surface Sources, preserve declared C2 seam relationships, keep independent termination controls, derive execution topology after surface compilation, and produce machine + human fairness evidence without relying on smooth shading as surface authority.`

Therefore:

`E2 M4.5 PASS → GENERIC E2 M5 MAY OPEN`.

## What remains blocked

E2 does **not** by itself authorize:
- system-level Candidate → Canonical promotion;
- Automotive v0.12 full-body M5;
- Automotive M6–M10;
- final front/rear termination styling;
- multi-patch production Class-A authority;
- product-specific human/design approval;
- PAP/production persistence closure.

## Required next step｜E3 application benchmark

Before v0.12 may be considered for system promotion, a real application benchmark must consume the generic system rather than redefine it.

E3 must demonstrate at minimum:
1. an application-specific Relationship Graph with multiple independent low-frequency volumes;
2. Primary Curves and sparse cage edits that respond to a real design decision rather than synthetic continuity alone;
3. multi-patch surface compilation with seam/interior fairness evidence;
4. Human Project/Visual QA on application-level proportion and form, not only mathematical continuity;
5. deterministic editable Surface Source and derived execution geometry kept as separate authorities;
6. durable persistence/readback under PAP before Promotion review.

Until E3 closes, `Modeling Worker v0.12` remains `SYSTEM CANDIDATE / NOT CANONICAL`.
