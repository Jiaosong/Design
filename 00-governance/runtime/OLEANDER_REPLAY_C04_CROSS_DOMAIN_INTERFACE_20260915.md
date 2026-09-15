# OLEANDER TP4 Cross-Domain Interface / Variable Replay — C04 Qingjiang — 2026-09-15

Status: **DRAFT REPLAY / SOURCE-BOUNDED / NOT CURRENT**.

Project: `PRJ-C04-QINGJIANG-SHISHU`.

Source basis includes:
- `C04_CURRENT_WEB_INTEGRATION_v1_1_RECEIPT.md`;
- `OLEANDER 清江 C04｜E/F 离线原型操作说明`;
- current CH08 / App / Web handoff evidence where explicitly referenced.

The replay tests whether P4 `Controlled Variable / Interface / Material Dependency` works across **physical route × service logic × App/Web × offline fallback × optional content**, rather than only architecture/geometry.

No source project authority is changed.

---

## 1. Source-supported cross-domain system

The project preserves these invariants:

- `BOAT → CABLE → WALK → RETURN` as the first-read journey/service spine;
- Service / Return priority;
- a complete no-phone route;
- physical and digital are complementary;
- Thirteen Imprints are optional and reorderable;
- no score, no `13/13` completion authority and no mandatory task-route logic;
- state family `NORMAL / DEGRADED / CLOSED / UNKNOWN` remains a behavior constraint;
- state family `FULL / LIGHT / OFF` remains an information-density constraint;
- App ROUTE is a supporting product surface, not route/source authority;
- the offline prototype needs no network, GPS, account or location permission;
- the route/network graphic is relational, not survey geometry and not “you are here” positioning;
- status demonstrations are preset states, not real-time service/open-state evidence;
- `FULL / LIGHT / OFF` changes information density, not route truth;
- no-phone path uses color band + node number + Return logic;
- current hard truth boundary remains `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.

This provides a genuine non-architectural interface network.

---

# 2. Controlled Variable replay

## 2.1 `NORMAL / DEGRADED / CLOSED / UNKNOWN`

This is a P4 `STATE` variable family, but its semantic dimension is **service/behavior availability interpretation**, not generic UI state.

Consumers include:
- App;
- Web integration;
- route/service explanation;
- potentially physical/fallback communication where the same state must be legible.

The prototype explicitly says these states are **demonstration presets**, not actual real-time site status.

Therefore the variable needs both:

```yaml
variable_class: STATE
semantic_dimension: SERVICE_BEHAVIOR_STATE
state_source_mode: DEMONSTRATION_PRESET | LIVE_AUTHORITY | MANUAL_AUTHORITY | DERIVED
```

For the current prototype:

`state_source_mode = DEMONSTRATION_PRESET`.

A consumer may demonstrate the semantics but cannot promote it to `LIVE_AUTHORITY`.

### Replay rule

`P4/VAR-RP02 SHARED_STATE_ENUM_REQUIRES_SEMANTIC_DIMENSION_AND_SOURCE_MODE; DEMONSTRATION_STATE_CANNOT_IMPERSONATE_LIVE_OPERATIONAL_STATE`.

---

## 2.2 `FULL / LIGHT / OFF`

This is also state-like, but it controls **information density/presence**, not service truth.

The source explicitly states:

`FULL / LIGHT / OFF controls reading information density and does not alter route truth.`

Therefore same-literal-class modeling (`STATE`) is insufficient by itself.

Preferred metadata:

```yaml
variable_class: STATE
semantic_dimension: INFORMATION_PRESENCE_MODE
truth_effect: PRESENTATION_OR_INFORMATION_DENSITY_ONLY
must_not_mutate: ROUTE_TOPOLOGY / SERVICE_TRUTH / SOURCE_STATUS
```

### Replay rule

`P4/VAR-RP03 STATE_VARIABLES_WITH_DIFFERENT_SEMANTIC_DIMENSIONS_MUST_NOT_BE_SUBSTITUTED_MERELY_BECAUSE_THEY_SHARE_THE_STATE_CLASS`.

No new top-level variable class is needed; semantic dimension is the missing discriminator.

---

# 3. Route spine as shared controlled semantic

`BOAT → CABLE → WALK → RETURN` appears in Web/Journey and Return logic and must remain coherent across carriers.

However it is not a survey-grade geometric path.

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
value: [BOAT, CABLE, WALK, RETURN]
geometry_authority: NTS_RELATIONAL_ONLY
```

### Replay rule

`P4/VAR-RP04 ROUTE_SERVICE_SEMANTIC_SPINE_MUST_NOT_BE_UPGRADED_TO_SURVEY_OR_POSITION_AUTHORITY_WITHOUT_GEOMETRIC_SOURCE_AUTHORITY`.

---

# 4. Producer / consumer authority at interfaces

The current Web integration explicitly consumes App behavior without redesigning or promoting App authority. App ROUTE remains support rather than route authority.

This reveals a useful P4 interface field:

```yaml
interface_binding_mode:
  AUTHORITATIVE_PRODUCER
  READ_ONLY_CONSUMER
  TRANSFORMING_CONSUMER
  BIDIRECTIONAL_COORDINATED
  FALLBACK_EQUIVALENT
```

For Web consuming App journey state:

`READ_ONLY_CONSUMER` or bounded `TRANSFORMING_CONSUMER` depending on presentation transformation.

A consumer cannot silently become producer/change authority because it renders the state more prominently.

### Replay rule

`P4/AUTH-RP05 INTERFACE_CONSUMER_BINDING_MUST_NOT_INHERIT_UPSTREAM_CHANGE_AUTHORITY_FROM_VISIBILITY_OR_IMPLEMENTATION_OWNERSHIP`.

---

# 5. Digital ↔ no-phone fallback interface

The no-phone route remains complete and uses low-tech color band + node number + Return logic.

This is not simply another presentation. It is a **fallback continuity interface**.

The digital system may offer richer state/content, but critical route/Return comprehension must retain a non-digital path.

Acceptance dimensions include:

- `ROUTE_IDENTITY_CONTINUITY`;
- `RETURN_DISCOVERABILITY`;
- `NODE_ID_CROSS_REFERENCE`;
- `NO_NETWORK_DEPENDENCE`;
- `NO_GPS_DEPENDENCE`;
- `CRITICAL_MEANING_NOT_DIGITAL_ONLY`.

### Replay rule

`P4/IFC-RP02 FALLBACK_INTERFACE_CLOSURE_REQUIRES_CRITICAL_TASK_CONTINUITY_NOT_FEATURE_PARITY`.

This is a useful cross-domain refinement: fallback systems need not duplicate every feature, but must preserve defined critical tasks/claims.

---

# 6. Optional-content interface

Thirteen Imprints are optional/reorderable and have no score/13-of-13 completion authority.

This optionality is consumed by Web/App interaction.

The interface must preserve:

- content identity;
- optionality;
- reorderability where applicable;
- no mandatory completion semantics;
- no score authority.

A UI implementation that adds progress/completion pressure would therefore violate the upstream content/service contract even if all 13 items are technically present.

### Replay rule

`P4/IFC-RP03 CONTENT_INTERFACE_ACCEPTANCE_INCLUDES_BEHAVIORAL_SEMANTICS_SUCH_AS_OPTIONALITY_ORDER_FREEDOM_AND_NO_SCORE_NOT_JUST_OBJECT_PRESENCE`.

This demonstrates that Interface acceptance is not limited to geometry/data correctness.

---

# 7. Return as cross-system invariant

Return is explicitly prioritized in journey, digital interaction and no-phone fallback.

This makes Return a candidate **cross-system controlled invariant**, not merely one screen or button.

Preferred representation:

```yaml
controlled_variable_or_policy_id: RETURN_PRIORITY
variable_class: HUMAN_FACTOR or CONTENT_SEMANTIC
semantic_dimension: RECOVERY_RETURN_PRIORITY
consumers: [ROUTE_SERVICE, APP, WEB, NO_PHONE_FALLBACK, MOTION/NARRATIVE]
change_authority: one explicit system owner
```

The exact carrier expression may differ; the semantic priority must persist.

### Replay rule

`P4/VAR-RP05 CROSS_SYSTEM_POLICY_OR_PRIORITY_MAY_BE_CONTROLLED_AS_A_SHARED_SEMANTIC_VARIABLE_WHEN_MULTIPLE_CONSUMERS_DEPEND_ON_THE_SAME_INVARIANT`.

This avoids duplicating “Return priority” as unrelated local decisions in every medium.

---

# 8. N-way Interface topology replay

The cross-domain network includes at least:

- route/service system;
- App;
- Web;
- no-phone physical fallback;
- optional content/Imprints;
- presentation/motion surfaces.

A single giant hub would hide important pairwise transformations, while fully pairwise modeling would explode maintenance.

Preferred hybrid:

```text
HUB: ROUTE_SERVICE_SEMANTIC_CONTRACT
  ↕
  consumers / subinterfaces
  - APP binding
  - WEB binding
  - NO_PHONE fallback binding
  - IMPRINT optionality binding

PAIRWISE interface only where transformation/failure/acceptance differs materially.
```

### Replay rule

`P4/IFC-RP04 N_WAY_INTERFACE_MAY_USE_HUB_PLUS_SELECTIVE_PAIRWISE_EDGES; FULL_PAIRWISE_EXPANSION_IS_REQUIRED_ONLY_WHERE_ACCEPTANCE_OR_FAILURE_SEMANTICS_DIFFER`.

This is an anti-overmodeling rule.

---

# 9. Interface acceptance dimensions from C04

The replay extends the KH46 geometric acceptance-dimension lesson into non-spatial systems.

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
- `GEOMETRY_OR_DATA` where actually applicable.

The set is interface-specific; this is not a mandatory universal checklist.

### Replay rule

`P4/IFC-RP05 ACCEPTANCE_DIMENSIONS_ARE_TYPED_BY_INTERFACE_RESPONSIBILITY_AND_MUST_NOT_DEFAULT_TO_GEOMETRY_OR_FILE_TRANSFER_ONLY`.

---

# 10. Failure propagation replay

Examples:

### App renders `UNKNOWN` as if it were live site status

Affected:
- service-state interpretation;
- public claim ceiling;
- Web/App truth boundary.

Not necessarily affected:
- route semantic spine itself.

### `FULL/LIGHT/OFF` implementation accidentally changes route data

Affected:
- controlled route semantics;
- digital interface;
- fallback consistency;
- potentially presentation release.

This is more severe because an information-density variable improperly mutated source truth.

### Web adds `13/13` completion

Affected:
- optionality interface;
- experience behavior;
- Return/service priorities if completion pressure changes route behavior.

No geometry need be wrong for the Interface to fail.

---

# 11. TP4 replay deltas

Add/clarify:

1. `semantic_dimension` on shared Controlled Variables;
2. `state_source_mode` for status-like variables;
3. `truth_effect / must_not_mutate` for presentation/information state variables;
4. `interface_binding_mode` for producer/consumer authority;
5. fallback acceptance based on critical-task continuity, not feature parity;
6. behavioral-semantic acceptance dimensions such as optionality/no-score;
7. cross-system policy/priority as valid shared semantic variable;
8. hybrid N-way hub + selective pairwise topology;
9. non-geometric Interface acceptance dimension vocabulary.

Replay-derived rules:

- `P4/VAR-RP02` shared state enum needs semantic dimension + source mode;
- `P4/VAR-RP03` same STATE class does not make variables substitutable;
- `P4/VAR-RP04` route semantic spine cannot self-promote to survey authority;
- `P4/AUTH-RP05` consumer does not inherit upstream change authority;
- `P4/IFC-RP02` fallback closure requires critical-task continuity, not feature parity;
- `P4/IFC-RP03` interface acceptance includes optionality/no-score semantics;
- `P4/VAR-RP05` cross-system policy can be a controlled shared semantic variable;
- `P4/IFC-RP04` N-way may use hub + selective pairwise modeling;
- `P4/IFC-RP05` acceptance dimensions follow interface responsibility, not geometry default.

---

# 12. TP4 disposition

`TP4 CROSS-DOMAIN INTERFACE/VARIABLE REPLAY = FIRST PASS COMPLETE WITH DELTAS`.

The replay strongly supports the P4 model as genuinely cross-domain. The principal refinement is not a new Object Class; it is richer variable/interface semantics so state, optionality, recovery, fallback and authority survive across physical/digital/service carriers.

No Current promotion is authorized.