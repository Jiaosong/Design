# OLEANDER 3D Evidence Carrier Congruence Protocol v1

Status: **CANDIDATE INTEGRATION / GENERAL 3D INVARIANT / 2026-08-19**

This protocol prevents a numerically valid measurement from supporting the wrong spatial/semantic claim because the reference and candidate were measured on different carriers.

## Core rule

`CLAIM → REQUIRED CARRIER SCOPE → REFERENCE CARRIER → CANDIDATE CARRIER → METRIC`

A metric is interpretable only when the candidate carrier represents the same claim scope as the reference carrier, or when an explicitly declared proxy is sufficient for that narrower claim.

Examples:
- whole-visible silhouette claim → whole-visible reference vs whole-visible candidate;
- primary-shell fairness claim → primary shell vs primary shell;
- aperture-host relation → host boundary + opening/interface carrier, not a dark overlay;
- local material/interface claim → local interface carrier, not an orphan macro without parent context;
- assembly clearance → relevant moving/static component pair, not the beauty-render silhouette.

## Carrier scopes

Use one or a more specific project-defined equivalent:
- `WHOLE_VISIBLE_GROSS`
- `PRIMARY_FORM_OR_SHELL`
- `ASSEMBLY_OR_COMPONENT_SET`
- `APERTURE_OR_INTERFACE`
- `LOCAL_CONTEXT`
- `DETAIL_OR_MICRO`
- `FIELD_OR_MEASURED_PHYSICAL`
- `VISUAL_PROXY`

`VISUAL_PROXY` is a state qualifier, not permission to widen a claim. A visual proxy may support a gross silhouette screen if it actually carries that silhouette; it cannot become engineering aperture truth, physical material truth, or manufacturing evidence.

## Required checks

For each metric or evidence claim record:
1. claim id and claim scope;
2. reference carrier identity/scope;
3. candidate carrier identity/scope;
4. whether the candidate is authoritative, derived, diagnostic, or visual proxy;
5. coverage relation: `CONGRUENT / SUFFICIENT_PROXY_FOR_DECLARED_SCOPE / MISMATCH / UNRESOLVED`;
6. measurement method and normalization frame;
7. explicit does-not-prove boundary.

If a measurement changes carrier between revisions, preserve the prior result and mark comparability. Do not overwrite history as if only the number changed.

## Hard failures

- `WHOLE_VISIBLE_GROSS` reference measured against a body-only candidate while cabin/roof/major visible members are excluded;
- a primary-shell curvature claim measured on a post-Boolean/post-opening display mesh when the openings themselves create the observed discontinuity;
- a local interface claim inferred from overall silhouette RMSE;
- a detail crop used to claim whole-product lifecycle severity;
- a visual proxy presented as final physical/engineering carrier;
- a changed normalization frame hidden inside a regression comparison;
- carrier mismatch repaired by widening/narrowing geometry rather than repairing the evidence carrier.

## Allowed proxy use

A proxy is legal only when all are true:
- the claim is explicitly bounded to what the proxy can carry;
- the proxy state is visible in the receipt;
- the corresponding higher-order truth remains HOLD/NOT PROVEN;
- the metric is not reused under a wider claim id.

Example: calibrated greenhouse proxy + primary body may screen `WHOLE_VISIBLE_GROSS` width-by-height, while `FINAL_APERTURE_ARCHITECTURE` remains `NOT_APPLICABLE_STAGE_HOLD`.

## Regression rule

Comparable regression requires both:
- same metric semantics;
- congruent/equivalent carrier scope and normalization.

If not, use `NOT_COMPARABLE_CARRIER_CHANGED` or another explicit HOLD state. Never synthesize a fake baseline from a differently scoped carrier.

## Required evidence

`EVIDENCE_CARRIER_RECEIPT.json` should contain:
- `claim_id`;
- `claim_scope`;
- `reference_carrier` + `reference_carrier_scope`;
- `candidate_carrier` + `candidate_carrier_scope`;
- `candidate_state_class`;
- `coverage_relation`;
- `measurement_method`;
- `normalization_frame`;
- `regression_comparability`;
- `result`;
- `does_not_prove`.

Recommended result vocabulary:
- `PASS_CARRIER_CONGRUENCE`
- `PASS_SUFFICIENT_PROXY_FOR_DECLARED_SCOPE`
- `HOLD_CARRIER_MISMATCH`
- `HOLD_CARRIER_UNRESOLVED`

## Failure routing

- reference/candidate scope mismatch → repair evidence carrier before editing geometry;
- post-opening topology contaminates primary-skin diagnostic → create/use a pre-opening diagnostic carrier;
- proxy sufficient for gross claim but not precise construction claim → keep gross metric; HOLD construction claim;
- carrier changed between candidates → mark regression non-comparable until a common carrier is reconstructed.

## Benchmark provenance

The Porsche 911 992.2 V51→V54 benchmark exposed the rule while auditing FRONT/REAR projected-profile evidence. The benchmark is provenance only; this protocol applies across product, automotive, spatial, architectural, landscape, CMF and technical 3D evidence.

## Does not prove

Carrier congruence only proves that the evidence is scoped to the claim appropriately. It does not prove the metric is good, the design is correct, reference fidelity, Class-A continuity, field truth, engineering validity, physical CMF, manufacturability, Design KEEP or MAIN KEEP.
