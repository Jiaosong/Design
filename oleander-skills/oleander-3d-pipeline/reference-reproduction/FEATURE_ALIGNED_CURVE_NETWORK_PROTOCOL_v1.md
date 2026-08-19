# Feature-Aligned Curve Network Protocol v1

Status: CANDIDATE SPECIALIST EXTENSION / reference-reconstruction representation upgrade.

Architecture binding: this protocol is an OLEANDER 3D / Modeling Contract specialization under **K3 Execution Router**. It does not create a new Current Authority, Project Flow, Workstream, Validation object, system Gate, breaker or promotion state. R0–R7 below are internal reference-modeling stage IDs only.

Purpose: replace generic evenly sampled ring/loft refinement as the default for identity-critical reflective products. Source must align to the object's actual form logic.

## INPUT
- current Project Control Card / Decision Question when project execution is in scope;
- locked reference identity/version and allowed transfer scope resolved by K2;
- hard points / dimensions / calibrated landmarks;
- SIDE / FRONT / REAR reference evidence and at least one 3/4 validation view when available;
- current best-known comparable diagnostic baselines;
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

## Sparse Source / dense evaluated grid separation

**Source rail count is not evaluated-surface density.** Keep Source controls causally sparse, but regenerate enough Derived/evaluated rails and longitudinal stations for stable topology, curvature and rendering diagnostics.

Required checks:
- persist `source_semantic_rail_count` separately from `derived_ring_vertices` / evaluated station count;
- densification must be deterministic and regenerated from Source, never silently promoted to Source;
- failure of evaluated density/stretch must route to generated construction before adding Source controls;
- a sparse semantic network that produces stretched faces, poor local sampling or an under-resolved render mesh is not a professional surface merely because the Source vocabulary is elegant;
- increasing Derived density may repair sampling quality, but cannot repair wrong primary mass, wrong rail placement or wrong reference identity.

992.2 V49 benchmark finding: the feature-aligned Source direction improved SIDE gesture and removed fold inversions, but a 20-vertex evaluated ring failed the existing primary-body surface-density/stretch screen. V50 therefore keeps the semantic rail vocabulary sparse while adding deterministic Derived midpoint sampling. This finding is execution provenance, not proof that V50 is visually correct.

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

If a FRONT/REAR projected profile is inverted into the transverse section, its resulting low RMSE is **constraint compliance**, not independent fidelity evidence. The held-out 3/4 review must stay outside that fitted objective.

## Multi-view sparse fitting
A solver may optimize sparse Source parameters against multiple external/calibrated observations. The objective may combine silhouette/profile/landmark errors and smoothness regularization, but:
- weights and inputs must be recorded;
- protected families remain locked;
- the solver may not rewrite reference targets;
- held-out validation remains outside the fitted objective;
- visual review remains independent and routes to existing K4 Visual/Project QA.

## Gate-local best-known baselines
Representation reopen does not erase stronger earlier results. Preserve the best comparable baseline per diagnostic gate.

Example: if one candidate owns the best SIDE projection while an earlier candidate remains stronger in FRONT/REAR profile, a new candidate must be compared against those per-gate baselines rather than an averaged single revision. A candidate that improves one fitted metric may remain HOLD/REJECT because it regresses another best-known gate.

## Tiered identity
Classify form families:
- `TIER_A_IDENTITY_CRITICAL` — wrong means the object fails first-read identity;
- `TIER_B_IDENTITY_SUPPORTING` — supports recognition after Tier A;
- `TIER_C_DETAIL` — seams, internal graphics, micro-detail, CMF cues.

Tier B/C work may not be used to claim completion while Tier A is REVISE/REJECT.

## Representation reopening through existing CB-01
Do not define a separate Representation Escalation Gate. Control Plane CB-01 remains authoritative: after the same Decision Question receives 2 consecutive Visual/Project REVISE results, perform Root Cause Reclassification.

If the representation layer is identified as causal, emit `REOPEN_REPRESENTATION_MODEL` and re-evaluate curve vocabulary, section placement, patch topology, aperture architecture or measurement model. Do not relax thresholds or add detail as a substitute.

## EVIDENCE
- `FEATURE_CURVE_NETWORK_RECEIPT.json`;
- curve/section inventory and Source digest;
- Source semantic rail count + Derived/evaluated rail/station counts;
- densification/regeneration rule;
- generated patch/cage receipt;
- comparable projection/landmark results;
- gate-local best-known baseline receipt when representation experiments span multiple candidates;
- Broad/Strip/Grazing/Zebra as applicable;
- fit-view list vs held-out-view list;
- independent visual result routed through existing K4 review.

## Specialist FAIL / HOLD outputs
- `FAIL_IDENTITY_CURVE_FAMILY_MISSING`
- `FAIL_SECTION_CAUSALITY_UNCLEAR`
- `FAIL_APERTURE_NOT_IN_SOURCE_TOPOLOGY`
- `FAIL_TARGET_CANDIDATE_PROVENANCE_COLLAPSE`
- `FAIL_EVALUATED_SURFACE_DENSITY_OR_STRETCH`
- `FAIL_GATE_LOCAL_BEST_KNOWN_REGRESSION`
- `REJECT_HELD_OUT_IDENTITY`
- `REOPEN_REPRESENTATION_MODEL`

## Does not prove
Feature-aligned curves, structured patches, low projection error, dense evaluated topology or good reflection diagnostics do not prove manufacturer CAD, Class-A/G2/G3 certification, tooling, manufacturing feasibility, final design approval or Canonical promotion.
