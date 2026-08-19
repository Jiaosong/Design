# OLEANDER 3D Stage Capability Routing Protocol v1

Status: **CANDIDATE INTEGRATION / GENERAL 3D INVARIANT / 2026-08-19**

This protocol prevents a valid modeling stage from crashing, fabricating evidence, or being falsely promoted because a downstream diagnostic still assumes objects or metrics that belong to another stage.

It is additive to `SKILL.md`; it does not create a new Project Gate, Authority state, or modeling method.

## Core rule

`STAGE → SEMANTIC CAPABILITIES → CONSUMER REQUIREMENTS → EVIDENCE`

A diagnostic, regression consumer, exporter, or review script must ask for a **semantic capability**, not for a historical object name.

Examples of semantic capabilities:

- `PRIMARY_FORM_PROJECTION`
- `SIDE_SILHOUETTE`
- `FRONT_GROSS_PROFILE`
- `REAR_GROSS_PROFILE`
- `FINAL_APERTURE_ARCHITECTURE`
- `FINAL_WINDSHIELD_FLANGE`
- `FINAL_REAR_GLASS_FLANGE`
- `SURFACE_REFLECTION_DIAGNOSTIC`
- `FINAL_EXCHANGE_MESH`

An object such as `REF_WINDSHIELD`, `BODY_V17`, or `MESH_FINAL_03` is an implementation identifier, not the capability itself.

## Capability states

Every stage-relevant capability is one of:

1. `AVAILABLE` — the stage currently provides evidence suitable for the declared consumer.
2. `NOT_APPLICABLE_STAGE_HOLD` — the current stage intentionally defers this capability and no current claim requires it.
3. `UNAVAILABLE_REQUIRED_FAIL` — the current stage/claim requires the capability but it is absent or invalid.
4. `UNRESOLVED_STAGE_HOLD` — stage applicability itself has not been resolved safely.

`NOT_APPLICABLE_STAGE_HOLD` is not a softer name for failure. It is legal only when the current task/stage explicitly defers the capability.

## Required vs held

Before a consumer runs, declare:

- `required_capabilities` — must be AVAILABLE for this consumer;
- `held_capabilities` — explicitly outside current stage scope;
- optional capabilities if useful.

Hard invariant:

`required_capabilities ∩ held_capabilities = ∅`

If a capability is required to support the current claim, it may not be hidden inside HOLD.

## Consumer behavior

### REQUIRED capability is AVAILABLE
Run the measurement/check and bind evidence to the actual evaluated carrier.

### REQUIRED capability is absent
Emit `FAIL_REQUIRED_CAPABILITY_MISSING`. Do not substitute an older object, an intermediate shell, a proxy, zero, NaN, stale receipt, or remembered value.

### Capability is `NOT_APPLICABLE_STAGE_HOLD`
- do not run a metric whose semantic carrier does not exist yet;
- record it in `not_applicable_metrics` or equivalent stage receipt;
- do not insert synthetic numeric values into a PASS/FAIL metric set;
- continue other valid stage checks;
- preserve does-not-prove boundaries.

### Stage applicability is unresolved
Emit `HOLD_STAGE_CAPABILITY_UNRESOLVED`; do not guess from file/object recency.

## Stable semantic identity

Persistent checks should resolve objects through semantic role/capability metadata or a stage registry. Stable object names may be used as one implementation, but revision prefixes/suffixes must not silently break a capability that is still present.

Forbidden:

- `candidate V48` fails only because a consumer expects `V17_*` naming;
- final-aperture metric crashes a primary-form stage where aperture is explicitly HOLD;
- renamed headlamp/rear-light objects make machine QA fail even though the semantic components are present;
- a missing required capability is relabeled `NOT_APPLICABLE` merely to keep CI green.

## Metric-set rule

Quality metrics are stage-specific.

A later-stage metric set must not be inherited wholesale by an earlier/different stage. Build the active metric set from current required capabilities.

When a prior candidate lacks comparable evidence, regression must say `NOT_COMPARABLE`; it must not reconstruct a fake baseline from stale or incompatible receipts.

`PROJECTION_MACHINE_SCREENING_FAIL` or another honest quality failure may coexist with successful runtime verification. CI should fail for runtime/evidence/provenance dishonesty, not merely because the model is visibly or numerically weak.

## Stage transitions

When the workflow advances to a stage that requires a previously held capability:

1. remove it from `held_capabilities`;
2. add it to `required_capabilities`;
3. materialize the actual semantic carrier;
4. run its diagnostics;
5. invalidate any earlier HOLD-based assumption that could now be tested.

A previous `NOT_APPLICABLE_STAGE_HOLD` never proves the later capability.

## Required evidence

`STAGE_CAPABILITY_ROUTING_RECEIPT.json` should contain at minimum:

- `candidate_revision`;
- `stage`;
- `required_capabilities`;
- `available_capabilities`;
- `held_capabilities`;
- `held_result`;
- `failed_required_capabilities`;
- `legacy_name_dependencies_not_required` when applicable;
- `result`;
- `does_not_prove`.

Recommended result vocabulary:

- `PASS_STAGE_AWARE_ROUTING`
- `FAIL_REQUIRED_CAPABILITY_MISSING`
- `HOLD_STAGE_CAPABILITY_UNRESOLVED`

## Failure routing

- object-name-only failure while semantic capability exists → repair resolver/consumer, not geometry;
- current required capability absent → construct/restore the capability or stop that claim;
- held later-stage capability requested by inherited consumer → repair consumer metric set;
- same metric exists but carrier/provenance changed → `NOT_COMPARABLE` until a valid baseline exists;
- runtime green but design weak → route to Design/Reference Fidelity review, not runtime repair.

## Benchmark provenance

The rule was exposed by the Porsche 911 992.2 V47→V48 benchmark: a primary-form stage deliberately held final aperture architecture, while inherited projection/regression consumers still required historical `REF_WINDSHIELD` / later-stage metric assumptions. V48 demonstrated that valid primary-form metrics can run while aperture-dependent metrics remain `NOT_APPLICABLE_STAGE_HOLD`.

This benchmark is provenance only; the rule applies to product, automotive, architectural, landscape, CMF, procedural and exchange workflows wherever stage capability varies.

## Does not prove

Stage-aware routing proves only that consumers use the capabilities appropriate to the current stage. It does not prove geometry quality, reference fidelity, Class-A continuity, field truth, engineering validity, manufacturability, physical CMF, usability, Design KEEP or MAIN KEEP.
