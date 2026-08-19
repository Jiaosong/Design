# Feature-Aligned Curve Network Protocol v1

Status: CURRENT CANDIDATE / reference-reconstruction representation upgrade.

Purpose: replace generic evenly sampled ring/loft refinement as the default for identity-critical reflective products. Source must align to the object's actual form logic.

## INPUT
- locked reference identity/version and allowed transfer scope;
- hard points / dimensions / calibrated landmarks;
- SIDE / FRONT / REAR reference evidence and at least one 3/4 validation view when available;
- current best-known gate baselines;
- representation route receipt.

## Principle
`Reference landmarks → identity curves → critical sections → boundary ownership → structured patch cage → evaluated surface`.

Equal station spacing is not a design virtue. Put Source controls where form behavior changes.

## Identity curve families
Use only families supported by the target; typical families include:
- center spine / crown;
- outer silhouette / side gesture;
- shoulder / belt / rocker rails;
- fender / haunch crowns;
- valleys or channels;
- aperture boundaries;
- wheel/opening boundaries;
- nose/tail terminal rails;
- real part/interface boundaries.

Every curve records:
- semantic id;
- authority/evidence source;
- locked or editable state;
- interpolation/degree;
- endpoint/tangent behavior;
- controlled dimensions/parameters;
- affected views/regions;
- does-not-prove.

## Critical sections
Place transverse/longitudinal sections at causal transitions, not uniform intervals. Examples:
- terminal extremes;
- feature centers;
- axle/hinge/major interface positions;
- cowl/shoulder transitions;
- roof/crown apex;
- pillar/sail transitions;
- maximum haunch/crown regions;
- aperture terminations.

A section must answer a form question. Extra sections that only densify the mesh are Derived construction, not new Source authority.

## Structured patch generation
Preferred surface stack for reflective product work:
1. sparse Source curves/sections/boundaries;
2. generated shared-boundary quad cage or CAD/NURBS patch network;
3. evaluated SubD/tessellated surface;
4. diagnostics on final evaluated geometry.

Patch count and Blender object count are implementation details. Boundary ownership and reflection continuity are the meaningful properties.

## Aperture rule
If an opening materially defines the product identity or assembly, its boundary must exist in Source topology before final surfacing. Do not finish a full opaque host and later imitate a window/screen/vent/opening with dark overlays or coarse face deletion.

Aperture Source should define as applicable:
`host boundary → opening rail → pillar/frame/interface → infill/glass/lens → backing/void`.

## Curvature intent
Coordinates alone may be insufficient. Identity curves/patches may carry qualitative or quantitative curvature intent, e.g.:
- broad convex / slow release;
- monotonic curvature increase/decrease;
- controlled inflection permitted/forbidden;
- crown location;
- tangent direction;
- radius band when evidence supports it.

These are design/surface constraints, not Class-A proof.

## Fit vs held-out validation
Do not validate a representation solely against the same observations used to construct it.

Preferred split when evidence allows:
- fit/calibration: SIDE + FRONT + REAR orthographic-like evidence;
- held-out validation: front 3/4 + rear 3/4 + elevated/top 3/4 or another independent view.

`Target compliance ≠ held-out visual identity`.

## Multi-view sparse fitting
A solver may optimize sparse Source parameters against multiple external/calibrated observations. The objective may combine silhouette/profile/landmark errors and smoothness regularization, but:
- weights and inputs must be recorded;
- protected families remain locked;
- the solver may not rewrite reference targets;
- held-out validation remains outside the fitted objective;
- visual review remains independent.

## Tiered identity
Classify form families:
- `TIER_A_IDENTITY_CRITICAL` — wrong means the object fails first-read identity;
- `TIER_B_IDENTITY_SUPPORTING` — supports recognition after Tier A;
- `TIER_C_DETAIL` — seams, internal graphics, micro-detail, CMF cues.

Tier B/C work may not be used to claim completion while Tier A is REVISE/REJECT.

## Representation Escalation
Emit `STOP_PARAMETER_TUNING_REOPEN_REPRESENTATION` if the same identity failure survives three controlled Source edits without material improvement, or if one fitted view repeatedly causes another locked view to regress. Reopen curve vocabulary, section placement, patch topology, aperture architecture or measurement model.

## EVIDENCE
- `FEATURE_CURVE_NETWORK_RECEIPT.json`;
- curve/section inventory and Source digest;
- generated patch/cage receipt;
- per-gate projection/landmark results;
- Broad/Strip/Grazing/Zebra as applicable;
- fit-view list vs held-out-view list;
- independent visual result.

## FAIL / HOLD
- `FAIL_IDENTITY_CURVE_FAMILY_MISSING`
- `FAIL_SECTION_CAUSALITY_UNCLEAR`
- `FAIL_APERTURE_NOT_IN_SOURCE_TOPOLOGY`
- `FAIL_TARGET_CANDIDATE_PROVENANCE_COLLAPSE`
- `REJECT_HELD_OUT_IDENTITY`
- `STOP_PARAMETER_TUNING_REOPEN_REPRESENTATION`

## Does not prove
Feature-aligned curves, structured patches, low projection error or good reflection diagnostics do not prove manufacturer CAD, Class-A/G2/G3 certification, tooling, manufacturing feasibility or final design approval.
