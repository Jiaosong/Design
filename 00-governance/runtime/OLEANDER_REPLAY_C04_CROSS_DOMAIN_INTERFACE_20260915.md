# OLEANDER TP4 Cross-Domain Interface / Variable Replay — C04 Qingjiang — 2026-09-15

Status: **DRAFT REPLAY / SOURCE-BOUNDED / NOT CURRENT**.

Project: `PRJ-C04-QINGJIANG-SHISHU`.

Replay target: route/service semantics × App/Web × Brand Presence × optional content × Return × offline/degraded behavior × truth boundary.

Source basis:

- `C04_APP_P08_PRESENCE_BINDING_v1_0_HANDOFF.json`;
- `C04_APP_P08_PRESENCE_BINDING_v1_0.html`;
- `C04_B_EVIDENCE_TO_STORY_MAPPING_r1.json`;
- earlier C04 Web/offline/current integration evidence only where consistent with the above current replay sources.

No source project authority, route geometry, approved App master, field truth or operator state is modified by this replay.

---

## 1. Why this is a valid TP4 cross-domain replay

This case crosses multiple domains at once:

- physical route / journey logic;
- digital interaction state;
- service and Return semantics;
- brand-attention behavior;
- editorial/read-depth behavior;
- offline/degraded behavior;
- presentation truth-state;
- source/field authority boundary.

The App handoff explicitly reframes Brand Presence as an **attention-authority layer, not a page skin**. Presence may reduce or disappear while functional semantics remain stable.

Source-supported critical rules include:

- Brand Presence never mutates route geometry or route authority;
- `UNKNOWN/CLOSED` cannot visually inherit a NORMAL brand-green status reading;
- `RETURN/SERVICE/ROUTE` functional semantics survive when Brand Presence is `OFF`;
- MY BOOK remains memory-not-score;
- runtime readback passed the current prototype mappings;
- the result remains an interaction prototype, not replacement of the approved App master and not field/operator validation.

The broader C04 evidence-to-story mapping also keeps:

- route authority above reading-page authority;
- optional reading rather than 13/13 completion;
- `NORMAL / DEGRADED / CLOSED / UNKNOWN` as behavior states;
- information presence reducing to LIGHT/OFF when appropriate;
- `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION`;
- prototype logic distinct from live operations, field signage/service and safety validation.

This is therefore a real N-way coordination problem, not a styling-only example.

---

# 2. Controlled Variable replay

## 2.1 `NORMAL / DEGRADED / CLOSED / UNKNOWN`

This is a P4 `STATE` variable family, but its semantic dimension is **service/behavior availability interpretation**, not generic UI state.

Consumers include:

- App interaction;
- Web/presentation integration;
- route/service explanation;
- Return priority behavior;
- optional-content availability;
- visible truth-state communication.

The prototype uses controlled demonstration states and explicitly does not claim live operational status.

Therefore the variable needs both:

```yaml
variable_class: STATE
semantic_dimension: SERVICE_BEHAVIOR_STATE
state_source_mode: DEMONSTRATION_PRESET | LIVE_AUTHORITY | MANUAL_AUTHORITY | DERIVED
```

For the current prototype:

`state_source_mode = DEMONSTRATION_PRESET`.

A consumer may demonstrate state semantics but cannot promote the state to `LIVE_AUTHORITY`.

### Replay rule

`P4/VAR-RP02 SHARED_STATE_ENUM_REQUIRES_SEMANTIC_DIMENSION_AND_SOURCE_MODE; DEMONSTRATION_STATE_CANNOT_IMPERSONATE_LIVE_OPERATIONAL_STATE`.

---

## 2.2 Information / Brand Presence modes

Current C04 evidence uses both project-level reading/presence concepts and a later App binding with:

`FULL / LIGHT / TRACE / OFF`.

The actual App binding maps page + operating state into `effectivePresence`, for example:

```text
TODAY + NORMAL → LIGHT
ROUTE + NORMAL → LIGHT
READ + NORMAL → TRACE
MY_BOOK + NORMAL → LIGHT
RETURN → OFF
DEGRADED → TRACE except RETURN=OFF
CLOSED → OFF
UNKNOWN → OFF
```

This presence state controls **information/identity density**, not route truth or operational source truth.

Preferred metadata:

```yaml
variable_class: STATE
semantic_dimension: INFORMATION_PRESENCE_MODE
truth_effect: PRESENTATION_OR_INFORMATION_DENSITY_ONLY
must_not_mutate: [ROUTE_TOPOLOGY, ROUTE_AUTHORITY, SERVICE_SOURCE_TRUTH]
```

### Replay rule

`P4/VAR-RP03 STATE_VARIABLES_WITH_DIFFERENT_SEMANTIC_DIMENSIONS_MUST_NOT_BE_SUBSTITUTED_MERELY_BECAUSE_THEY_SHARE_THE_STATE_CLASS`.

No new top-level variable class is needed; semantic dimension is the missing discriminator.

---

# 3. Derived Controlled Variable replay

The App prototype computes `effectivePresence` from at least two upstream inputs:

- `page`;
- `state`.

`effectivePresence` is therefore not an independent source authority. It is a **derived controlled variable** produced by an explicit binding rule.

This distinction matters because a derived value can be coordination-critical without owning its inputs.

Recommended metadata:

```yaml
variable_value_origin:
  SOURCE_CONTROLLED
  DERIVED_CONTROLLED
  LOCAL_COMPUTED_NONAUTHORITATIVE

derived_from: []
derivation_rule_ref:
```

For C04:

```yaml
EFFECTIVE_BRAND_PRESENCE:
  variable_value_origin: DERIVED_CONTROLLED
  derived_from: [PAGE_CONTEXT, OPERATION_STATE]
  derivation_rule_ref: C04_APP_P08_PRESENCE_BINDING_v1_0
```

### Replay-derived rule

`P4/VAR-RP06 DERIVED_CONTROLLED_VARIABLE_MUST_DECLARE_INPUT_VARIABLES_AND_DERIVATION_RULE_AND_CANNOT_SELF_BECOME_SOURCE_AUTHORITY`.

This is a genuine cross-domain gap exposed by replay; it is not a new Object Class.

---

# 4. Route spine as shared controlled semantic

`BOAT → CABLE → WALK → RETURN` and the broader M0–M7 route/service spine are reused across digital, editorial and Return logic, while route geometry remains relational/NTS rather than survey-grade.

The controlled responsibility is primarily:

- route-stage identity/order;
- Return priority;
- branch/optional relation;
- semantic route labels;
- source/provenance boundary.

It should not be modeled as exact geometry unless an authoritative geometry source exists.

Preferred representation:

```yaml
variable_class: CONTENT_SEMANTIC
semantic_dimension: ROUTE_SERVICE_SPINE
geometry_authority: NTS_RELATIONAL_ONLY
```

### Replay rule

`P4/VAR-RP04 ROUTE_SERVICE_SEMANTIC_SPINE_MUST_NOT_BE_UPGRADED_TO_SURVEY_OR_POSITION_AUTHORITY_WITHOUT_GEOMETRIC_SOURCE_AUTHORITY`.

---

# 5. Producer / consumer authority at interfaces

The current App/Web logic consumes route/state semantics without acquiring route authority.

This reveals a useful P4 interface field:

```yaml
interface_binding_mode:
  AUTHORITATIVE_PRODUCER
  READ_ONLY_CONSUMER
  TRANSFORMING_CONSUMER
  BIDIRECTIONAL_COORDINATED
  FALLBACK_EQUIVALENT
```

A consumer cannot silently become producer/change authority because it renders a state more prominently or implements a derived behavior.

### Replay rule

`P4/AUTH-RP05 INTERFACE_CONSUMER_BINDING_MUST_NOT_INHERIT_UPSTREAM_CHANGE_AUTHORITY_FROM_VISIBILITY_OR_IMPLEMENTATION_OWNERSHIP`.

Cross-domain confirmation:

`P4/VAR-RP07 CONSUMING_A_CONTROLLED_VARIABLE_DOES_NOT_GRANT_CHANGE_AUTHORITY_OVER_THAT_VARIABLE_OR_ITS_UPSTREAM_SOURCE`.

---

# 6. Bounded propagation and protected non-propagation

When `state` changes to `CLOSED` or `UNKNOWN`, the current prototype changes:

- Brand Presence → `OFF`;
- optional content visibility;
- fail-closed state cover/copy;
- interaction availability;
- Return/service/route priority.

But the same transition must **not** mutate:

- route geometry;
- route authority;
- source truth;
- field/operator truth;
- field safety truth.

This demonstrates that a material propagation graph needs both downstream effects **and protected non-propagation boundaries**.

Recommended structure:

```yaml
controlled_variable_ref:
when_changed:
  must_affect: []
  may_affect: []
  must_not_affect: []
reopen_targets: []
readback_targets: []
```

### Replay-derived rule

`P4/PROP-RP01 MATERIAL_STATE_PROPAGATION_MUST_DECLARE_AFFECTED_CONSUMERS_AND_PROTECTED_NON_PROPAGATION_TARGETS_WHERE_AUTHORITY_BOUNDARIES_MATTER`.

This is preferable to inventing one negative relation type per forbidden mutation.

---

# 7. Material Dependency: state-behavior semantics

The current dependency classes cover input, sequence, configuration, evidence, resource, authority and availability. This replay exposes one material dependency with distinct behavior:

`operation state → allowed interaction / presence / Return priority`.

Generic `INPUT_DEPENDENCY` is too weak because the contract requires behavior to change on a controlled state transition.

One new subclass is justified:

`STATE_BEHAVIOR_DEPENDENCY` — a dependency where a controlled state transition materially changes allowed behavior/output while preserving declared non-propagation invariants.

### Replay-derived rule

`P4/DEP-RP01 STATE_BEHAVIOR_DEPENDENCY_REQUIRES_TRANSITION_BEHAVIOR_AND_NON_PROPAGATION_BOUNDARY_WHEN_MATERIAL`.

No broader dependency-family expansion is justified.

---

# 8. Digital ↔ no-phone / reduced-digital fallback interface

The C04 system is designed so critical route/Return responsibility does not depend on optional digital richness. The evidence-to-story mapping explicitly treats Digital Silence as interaction-architecture resilience, while field signage/service sufficiency remains open.

This is a **fallback continuity interface**, not feature parity.

Acceptance dimensions include, where source-supported:

- `ROUTE_IDENTITY_CONTINUITY`;
- `RETURN_DISCOVERABILITY`;
- `NODE_ID_CROSS_REFERENCE`;
- `NO_NETWORK_DEPENDENCE`;
- `CRITICAL_MEANING_NOT_DIGITAL_ONLY`.

### Replay rule

`P4/IFC-RP02 FALLBACK_INTERFACE_CLOSURE_REQUIRES_CRITICAL_TASK_CONTINUITY_NOT_FEATURE_PARITY`.

And:

`P4/IFC-RP08 OFFLINE_OR_DEGRADED_INTERFACE_PASS_PROVES_DEFINED_FALLBACK_BEHAVIOR_ONLY_AND_DOES_NOT_ESTABLISH_FIELD_FALLBACK_SUFFICIENCY_WITHOUT_FIELD_EVIDENCE`.

---

# 9. Optional-content interface

Thirteen Imprints/Reading Library are optional/reorderable and have no score/13-of-13 completion authority.

The interface must preserve:

- content identity;
- optionality;
- reorderability where applicable;
- no mandatory completion semantics;
- no score authority.

A UI that technically renders all content but adds progress pressure can therefore fail the Interface contract.

### Replay rule

`P4/IFC-RP03 CONTENT_INTERFACE_ACCEPTANCE_INCLUDES_BEHAVIORAL_SEMANTICS_SUCH_AS_OPTIONALITY_ORDER_FREEDOM_AND_NO_SCORE_NOT_JUST_OBJECT_PRESENCE`.

---

# 10. Return as cross-system invariant

Return is prioritized in journey logic, digital interaction and reduced-digital/fallback behavior.

This makes Return a candidate **cross-system controlled invariant**, not merely one screen or button.

Preferred representation:

```yaml
controlled_variable_or_policy_id: RETURN_PRIORITY
variable_class: HUMAN_FACTOR or CONTENT_SEMANTIC
semantic_dimension: RECOVERY_RETURN_PRIORITY
consumers: [ROUTE_SERVICE, APP, WEB, FALLBACK, MOTION_NARRATIVE]
change_authority: one explicit system owner
```

### Replay rule

`P4/VAR-RP05 CROSS_SYSTEM_POLICY_OR_PRIORITY_MAY_BE_CONTROLLED_AS_A_SHARED_SEMANTIC_VARIABLE_WHEN_MULTIPLE_CONSUMERS_DEPEND_ON_THE_SAME_INVARIANT`.

---

# 11. N-way Interface topology replay

The coordination network includes at least:

- route/service system;
- operation state;
- App interaction;
- Web/presentation projection;
- Brand Presence;
- reduced-digital/fallback behavior;
- optional reading/content;
- Return/service behavior;
- truth boundary.

A single giant hub would hide important pairwise transformations, while fully pairwise modeling would explode maintenance.

Preferred hybrid:

```text
HUB: STATE_TO_EXPERIENCE / ROUTE_SERVICE SEMANTIC CONTRACT
  ↕
  subinterfaces
  - APP binding
  - WEB/presentation binding
  - fallback binding
  - optional-content binding

PAIRWISE edge only where transformation/failure/acceptance differs materially.
```

Pairwise passes alone are insufficient to prove global invariants such as:

- `UNKNOWN` fails closed across all relevant channels;
- Brand Presence can disappear while functional semantics survive;
- Return priority dominates optional reading;
- route authority remains upstream and unchanged.

### Replay rules

`P4/IFC-RP04 N_WAY_INTERFACE_MAY_USE_HUB_PLUS_SELECTIVE_PAIRWISE_EDGES; FULL_PAIRWISE_EXPANSION_IS_REQUIRED_ONLY_WHERE_ACCEPTANCE_OR_FAILURE_SEMANTICS_DIFFER`.

`P4/IFC-RP06 N_WAY_INTERFACE_REQUIRES_HUB_LEVEL_INVARIANTS_WHEN_PAIRWISE_PASSES_CANNOT_PROVE_SYSTEM_LEVEL_COORDINATION`.

---

# 12. Acceptance is multi-dimensional and responsibility-specific

The runtime checks establish bounded prototype dimensions such as:

- mapping correctness;
- function visibility;
- degraded presence reduction;
- closed-state functional survival;
- unknown fail-closed visibility.

They do **not** establish:

- real operator status integration;
- field signage sufficiency;
- field service sufficiency;
- real-condition accessibility;
- actual safety performance;
- live route state correctness.

A valid result may therefore be:

```text
STATE_MAPPING = PASS
FUNCTIONAL_CONTINUITY = PASS
TRUTH_STATE_FAIL_CLOSED = PASS
AUTHORITY_NON_MUTATION = PASS_BOUNDED
OPTIONALITY_NO_SCORE = PASS_BOUNDED
OFFLINE_FALLBACK_LOGIC = PASS_BOUNDED
FIELD_OPERATIONAL_VALIDATION = OPEN
FIELD_SERVICE_SIGNAGE_SUFFICIENCY = OPEN
FIELD_SAFETY_ACCESSIBILITY = OPEN
```

Cross-domain acceptance dimensions may include:

- `SEMANTIC_IDENTITY`;
- `AUTHORITY_PRESERVATION`;
- `STATE_MEANING`;
- `OPTIONALITY`;
- `RECOVERY_RETURN`;
- `FALLBACK_CONTINUITY`;
- `OFFLINE_AVAILABILITY`;
- `INFORMATION_DENSITY_BEHAVIOR`;
- `TRUTH_BOUNDARY`;
- `ACCESSIBILITY_INPUT`;
- `VISUAL_OR_INTERACTION_READBACK`;
- `GEOMETRY_OR_DATA` where applicable.

The set is interface-specific, not a universal mandatory checklist.

### Replay rules

`P4/IFC-RP05 ACCEPTANCE_DIMENSIONS_ARE_TYPED_BY_INTERFACE_RESPONSIBILITY_AND_MUST_NOT_DEFAULT_TO_GEOMETRY_OR_FILE_TRANSFER_ONLY`.

`P4/IFC-RP07 CROSS_DOMAIN_INTERFACE_CLOSURE_MUST_PRESERVE_ACCEPTANCE_DIMENSIONS_AND_CANNOT_COLLAPSE_PROTOTYPE_RUNTIME_PASS_INTO_FIELD_OPERATIONAL_PASS`.

This independently confirms the earlier KH46 `P4/IFC-RP01` dimensional-acceptance rule outside architecture.

---

# 13. Interface maturity is scoped

The interface has actual integrated runtime execution and can therefore be called at least `EXERCISED` for the prototype configuration.

It cannot be globally called `VERIFIED` if that is interpreted as field/operator verification.

Maturity therefore needs condition/configuration scope:

```yaml
maturity: EXERCISED | VERIFIED
maturity_scope:
configuration_ref:
condition_ref:
medium_or_environment:
claim_boundary:
```

Example:

`EXERCISED @ Chromium prototype / current binding / no live operator feed`.

### Replay-derived rule

`P4/IFC-RP09 INTERFACE_MATURITY_VALUE_IS_INVALID_WITHOUT_CONFIGURATION_AND_CONDITION_SCOPE_WHERE_RESULTS_ARE_ENVIRONMENT_DEPENDENT`.

---

# 14. UNKNOWN fail-closed behavior does not rewrite source truth

The prototype maps `UNKNOWN → OFF` for Brand Presence and shows an explicit fail-closed state.

This is a derived behavior. It does not mean the underlying operational truth is now known to be `CLOSED`.

### Replay-derived rule

`P4/VAR-RP08 FAIL_CLOSED_DERIVED_BEHAVIOR_MUST_NOT_REWRITE_UNKNOWN_SOURCE_STATE_AS_KNOWN_DOMAIN_STATE`.

This keeps UI fallback logic separate from domain truth.

---

# 15. Failure propagation examples

### A. App renders `UNKNOWN` as if it were live normal/open status

Affected:
- state interpretation;
- public claim ceiling;
- App/Web truth boundary.

Not necessarily affected:
- route semantic spine itself.

### B. `FULL/LIGHT/TRACE/OFF` implementation mutates route data

Affected:
- route semantics;
- digital interface;
- fallback consistency;
- potentially release eligibility.

Severity is high because an information-density variable improperly mutated source truth.

### C. Web adds `13/13` completion

Affected:
- optionality interface;
- experience behavior;
- Return/service priority if completion pressure changes route behavior.

No geometry need be wrong for the Interface to fail.

### D. Prototype runtime PASS is presented as field safety/service PASS

Affected:
- interface claim ceiling;
- P6 evidence/assurance;
- public presentation truth boundary.

The underlying prototype mapping may remain valid while the promoted claim fails.

---

# 16. Normalized replay object model

```yaml
interface_id: C04_STATE_TO_EXPERIENCE_COORDINATION_INTERFACE
model: HUB_INTERFACE_WITH_SELECTIVE_PAIRWISE_EDGES
participants:
  - ROUTE_NETWORK
  - OPERATION_STATE
  - APP_INTERACTION
  - WEB_PRESENTATION
  - BRAND_PRESENCE
  - OPTIONAL_READING
  - RETURN_SERVICE
  - FALLBACK_LAYER
  - PRESENTATION_TRUTH_BOUNDARY
controlled_variables:
  OPERATION_STATE:
    class: STATE
    semantic_dimension: SERVICE_BEHAVIOR_STATE
    state_source_mode: DEMONSTRATION_PRESET
  PAGE_CONTEXT:
    class: STATE
    semantic_dimension: INTERACTION_CONTEXT
    value_origin: SOURCE_CONTROLLED
  EFFECTIVE_BRAND_PRESENCE:
    class: STATE
    semantic_dimension: INFORMATION_PRESENCE_MODE
    value_origin: DERIVED_CONTROLLED
    derived_from: [OPERATION_STATE, PAGE_CONTEXT]
    derivation_rule_ref: C04_APP_P08_PRESENCE_BINDING_v1_0
propagation_contract:
  must_affect: [BRAND_PRESENCE, OPTIONAL_CONTENT, FAIL_CLOSED_COVER, RETURN_SERVICE_PRIORITY]
  must_not_affect: [ROUTE_GEOMETRY, ROUTE_AUTHORITY, FIELD_TRUTH, FIELD_SAFETY_TRUTH]
acceptance_dimensions:
  STATE_MAPPING: PASS
  FUNCTIONAL_CONTINUITY: PASS
  UNKNOWN_FAIL_CLOSED: PASS
  AUTHORITY_PRESERVATION: PASS_BOUNDED
  OPTIONALITY_NO_SCORE: PASS_BOUNDED
  OFFLINE_FALLBACK_LOGIC: PASS_BOUNDED
  FIELD_OPERATIONAL_VALIDATION: OPEN
  FIELD_SERVICE_SIGNAGE_SUFFICIENCY: OPEN
  FIELD_SAFETY_ACCESSIBILITY: OPEN
maturity: EXERCISED
maturity_scope: CHROMIUM_PROTOTYPE_CURRENT_BINDING
truth_boundary: NO_FIELD_OR_OPERATOR_VALIDATION
```

---

# 17. TP4 replay deltas

Existing replay-derived rules retained and strengthened:

- `P4/VAR-RP02` state enum requires semantic dimension + source mode;
- `P4/VAR-RP03` same STATE class does not make variables substitutable;
- `P4/VAR-RP04` route semantic spine cannot self-promote to survey authority;
- `P4/AUTH-RP05` consumer does not inherit upstream change authority;
- `P4/IFC-RP02` fallback closure requires critical-task continuity, not feature parity;
- `P4/IFC-RP03` interface acceptance includes optionality/no-score semantics;
- `P4/VAR-RP05` cross-system policy can be a controlled shared semantic variable;
- `P4/IFC-RP04` N-way may use hub + selective pairwise modeling;
- `P4/IFC-RP05` acceptance dimensions follow interface responsibility, not geometry default.

New source-grounded deltas:

- `P4/VAR-RP06` derived controlled variable declares inputs + derivation rule;
- `P4/PROP-RP01` propagation declares must/may/must-not-affect where authority boundaries matter;
- `P4/DEP-RP01` state-behavior dependency;
- `P4/IFC-RP06` hub-level invariants for N-way coordination;
- `P4/IFC-RP07` prototype runtime PASS cannot collapse into field-operational PASS;
- `P4/VAR-RP07` consuming variable does not grant change authority;
- `P4/VAR-RP08` fail-closed derived behavior cannot rewrite UNKNOWN source truth;
- `P4/IFC-RP08` offline/degraded fallback logic does not prove field fallback sufficiency;
- `P4/IFC-RP09` environment-dependent maturity requires configuration/condition scope.

New orthogonal metadata:

- `semantic_dimension`;
- `state_source_mode`;
- `variable_value_origin`;
- `derived_from`;
- `derivation_rule_ref`;
- `interface_binding_mode`;
- `must_affect / may_affect / must_not_affect`;
- maturity scope fields.

One new material-dependency subclass is justified:

- `STATE_BEHAVIOR_DEPENDENCY`.

---

# 18. TP4 disposition

`TP4 CROSS-DOMAIN INTERFACE / VARIABLE REPLAY = FIRST PASS COMPLETE WITH DELTAS`.

The replay strongly supports the P4 model as genuinely cross-domain. The principal refinement is not another Object Class; it is richer variable/interface semantics so state, derivation, optionality, recovery, fallback, authority and protected non-propagation survive across physical/digital/service carriers.

No Current promotion is authorized.