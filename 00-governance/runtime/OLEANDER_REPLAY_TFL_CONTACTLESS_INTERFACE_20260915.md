# OLEANDER TP4 Cross-Domain Interface Replay — TfL Oyster / Contactless PAYG — 2026-09-15

Status: **DRAFT EXTERNAL REPLAY / NOT CURRENT / SOURCE-BOUNDED**.

Purpose: test whether OLEANDER P4 `Controlled Variable / Interface / Material Dependency` semantics generalize beyond architecture into a real physical-digital-service-payment system.

This replay does **not** claim access to TfL's unpublished internal architecture. It maps only publicly documented service behavior into an OLEANDER analytical model. Every internal-looking element below is marked as an **OLEANDER inferred coordination model**, not as a claim about TfL implementation topology.

## 1. Public-source basis

Primary external sources reviewed:

1. Transport for London — `Pay as you go`.
   - Oyster/contactless card/device is used across TfL services.
   - rail journeys generally require touch-in and touch-out.
   - the same card or device should be used for both ends of a journey.
   - using a different device/presentation can lead to separate journeys/higher charges.
   - mobile device battery availability can affect successful presentation.

2. Transport for London — `Contactless payment` privacy/automated processing.
   - fare calculation uses touch-in origin, touch-out destination and, where relevant, pink-reader route data.
   - incomplete journeys can in some circumstances be automatically completed.
   - refunds can be triggered automatically or reviewed through customer service.

3. Transport for London — `Touch a pink card reader when changing trains`.
   - pink-reader touches communicate route information and can affect the fare charged.

4. Transport for London — contactless-payment public statistics.
   - TfL separately publishes incomplete-journey counts/revenue and correction/refund categories, confirming incomplete journey handling is a material operational state rather than an edge-case UI label.

5. EMVCo — Payment Tokenisation use-case guidance.
   - a rider may present the same underlying payment relationship in different credential forms; some transit systems can treat those presentations as separate journeys unless explicit account-reference linkage exists.

6. EMVCo — contactless/transit operator specifications and approval context.
   - transit is a distinct operational context within contactless payment infrastructure.

Source boundary:

- public user/service behavior = source-supported fact;
- exact internal APIs, database schemas, network topology, settlement timing or proprietary risk logic = **NOT ESTABLISHED**;
- OLEANDER object/variable/interface mapping = analytical inference for replay only.

---

# 2. Why this is a strong TP4 replay

The service spans:

- physical readers/gates;
- physical cards and mobile/wearable devices;
- credential/token presentation;
- journey-entry/route/exit events;
- automated fare calculation;
- fare capping/rules;
- account/journey-history surfaces;
- refunds/customer service;
- payment network context;
- privacy/automated decision boundaries.

One journey can therefore fail even when every local component appears individually functional.

Example:

- reader A accepts a phone at entry;
- reader B accepts a watch at exit;
- both devices may be valid payment instruments;
- yet the service can interpret them as different journey identities and charge incorrectly.

This is exactly the type of cross-domain coordination failure P4 is intended to model.

---

# 3. OLEANDER inferred system map

The following is **not** asserted as TfL's internal implementation diagram. It is the minimum semantic coordination model required to explain documented behavior.

```text
RIDER / PAYMENT CREDENTIAL
        ↓ present
ENTRY READER EVENT
        ↓
JOURNEY CONTEXT
        ↙           ↘
ROUTE VALIDATION     EXIT READER EVENT
(pink reader)              ↓
        ↘           JOURNEY COMPLETION
          ↘               ↓
              FARE DETERMINATION
                    ↓
             CHARGE / CAP / REFUND
                    ↓
        ACCOUNT / HISTORY / CUSTOMER SERVICE
```

This model immediately shows why pairwise component PASS is insufficient: journey correctness depends on continuity across several interfaces and state transitions.

---

# 4. Controlled Variable replay

## 4.1 Credential presentation identity

Public behavior establishes a crucial distinction:

`same underlying bank/payment relationship` does not necessarily mean `same transit presentation identity`.

TfL instructs users to touch in and out with the **same card or device**. EMVCo's tokenisation guidance likewise describes cases where the same rider can present one underlying payment relationship through different payment credentials and be treated as separate journeys without additional linkage.

Therefore P4 requires a distinction between:

```text
ECONOMIC / ACCOUNT IDENTITY
vs
PRESENTED CREDENTIAL IDENTITY
vs
SERVICE SESSION / JOURNEY IDENTITY
```

These must not be collapsed into one generic `identity` variable.

### Replay result

`UNDERMODELED → IDENTITY SCOPE REQUIRED`.

### New Controlled Variable metadata

```yaml
identity_scope:
  ECONOMIC_ACCOUNT
  PRESENTED_CREDENTIAL
  USER_DEVICE
  SERVICE_SESSION
  JOURNEY
  CUSTOMER_ACCOUNT
  OTHER_CONTROLLED

equivalence_policy:
  EXACT_SAME_PRESENTATION
  AUTHORIZED_EQUIVALENT
  LINKED_BY_REFERENCE
  NOT_EQUIVALENT
  UNKNOWN
```

### Replay rule

`P4/VAR-RP09 SHARED_IDENTITY_VARIABLE_MUST_DECLARE_IDENTITY_SCOPE; EQUIVALENCE_AT_ONE_SCOPE_CANNOT_BE_INFERRED_AT_ANOTHER`.

---

## 4.2 Journey state is a controlled state variable

Public documentation distinguishes complete and incomplete journeys, and describes maximum fares, auto-completion and refund handling.

Therefore journey state is not merely descriptive metadata. It materially changes downstream fare/refund behavior.

Minimum analytical states:

```text
ENTRY_OBSERVED
ROUTE_PARTIALLY_OBSERVED
EXIT_OBSERVED
COMPLETE
INCOMPLETE
AUTO_COMPLETED
CORRECTED
REFUNDED / REFUND_PENDING
```

This is an OLEANDER replay abstraction, not TfL's asserted internal enum.

### Replay result

`CONFIRMED`.

### Replay rule

`P4/VAR-RP10 CONTROLLED_STATE_VARIABLE_IS_MATERIAL_WHEN_STATE_TRANSITION_CHANGES_ALLOWED_DOWNSTREAM_BEHAVIOR_OR_CHARGE_OUTCOME`.

This strengthens existing `STATE_BEHAVIOR_DEPENDENCY` semantics.

---

## 4.3 Route-observation event is not the same as journey endpoint

Pink-reader use can distinguish a route that changes fare outcome even though origin and destination are the same.

Therefore route evidence is an additional state/input dimension rather than a duplicate endpoint variable.

### Replay result

`CONFIRMED_WITH_MULTI_INPUT_DELTA`.

### Replay rule

`P4/VAR-RP11 DERIVED_CONTROLLED_OUTPUT_MAY_REQUIRE MULTIPLE NON_SUBSTITUTABLE INPUT DIMENSIONS; ORIGIN_DESTINATION CANNOT SILENTLY ABSORB ROUTE_EVIDENCE`.

---

# 5. Interface replay

## 5.1 Rider credential ↔ physical reader

Acceptance dimensions include at least:

- credential readable/presentable;
- correct semantic credential identity;
- valid timing/location context;
- user feedback sufficient to know whether touch registered;
- device operational availability where device is required.

A reader can technically detect a credential while the end-to-end journey still fails because the wrong credential identity was used for session continuity.

### Replay result

`CONFIRMED`.

### Rule

`P4/IFC-RP10 LOCAL_DEVICE_ACCEPTANCE_PASS_CANNOT_CLOSE_END_TO_END_SERVICE_IDENTITY_CONTINUITY`.

---

## 5.2 Entry / route / exit form a hub-level invariant

Pairwise checks can all pass:

- entry reader accepted credential;
- pink reader accepted credential;
- exit reader accepted credential;

and yet fare correctness can still fail if the events are not resolved into one coherent journey identity/context.

Therefore this replay confirms `HUB_WITH_SELECTIVE_PAIRWISE_EDGES` as a genuinely cross-domain model, not an architecture-specific abstraction.

### Hub invariant

```text
all material journey events required for one fare decision
must resolve to one authorized journey context under one declared identity/equivalence policy
```

### Replay result

`CONFIRMED / CROSS-DOMAIN GENERALIZATION`.

### Rule

`P4/IFC-RP11 PAIRWISE_EVENT_ACCEPTANCE_CANNOT_PROVE_HUB_LEVEL_TRANSACTION_OR_SERVICE_SESSION_COHERENCE`.

---

## 5.3 Interface acceptance is multi-dimensional

For this service, one interface can have distinct acceptance dimensions:

- credential communication;
- semantic identity continuity;
- journey-state continuity;
- route attribution;
- fare correctness;
- recovery/refund path;
- privacy/authorized use boundary;
- user-visible feedback.

A PASS in RF/contactless communication cannot close fare correctness or journey recovery.

### Replay result

`CONFIRMED`.

### New acceptance dimensions

Add to P4 starter vocabulary:

```text
CREDENTIAL_RECOGNITION
IDENTITY_CONTINUITY
TRANSACTION_SESSION_CONTINUITY
ROUTE_ATTRIBUTION
FARE_OR_RULE_OUTCOME
RECOVERY_CORRECTION
PRIVACY_AUTHORIZED_USE
USER_CONFIRMATION_FEEDBACK
```

These are examples, not universal mandatory dimensions.

### Rule

`P4/IFC-RP12 TECHNICAL_COMMUNICATION_PASS_CANNOT_CLOSE_SEMANTIC_TRANSACTION_OR_SERVICE_OUTCOME_DIMENSIONS`.

---

# 6. Material Dependency replay

The current P4 term `MATERIAL_DEPENDENCY` means **material in consequence**, not physical material.

This replay demonstrates the importance of making that explicit.

Examples:

- mobile device battery/operational availability can affect ability to present the credential;
- reader availability affects event capture;
- required journey event continuity affects correct fare determination;
- route-validation event availability can affect route attribution;
- customer/account recovery channel affects correction/refund handling.

These are not all physical-material dependencies, but failures can materially affect service outcome.

### Replay result

`TERMINOLOGY AMBIGUITY FOUND`.

### Refinement

Keep the existing semantic class for compatibility, but define:

`MATERIAL_DEPENDENCY = a dependency whose failure can materially alter allowed behavior, evidence validity, service outcome, safety, cost, authority, configuration or promotion.`

It does **not** mean `material/specification dependency`.

### Rule

`P4/DEP-RP02 MATERIAL_DEPENDENCY_IS CONSEQUENCE_MATERIALITY_NOT_PHYSICAL_MATERIAL_ONLY`.

---

# 7. Change propagation replay

Public TfL documentation shows fare outcome can depend on:

- entry/exit observations;
- route validation;
- credential/device continuity;
- fare/cap rules;
- journey correction/refund handling.

Therefore a change to one shared rule or identity-equivalence policy can affect multiple downstream consumers.

However the public sources do not establish TfL's internal change-authority assignments, so this replay must not invent owners.

### Replay result

`PROPAGATION LOGIC CONFIRMED / AUTHORITY OWNERSHIP NOT EVALUATED`.

### Rule

`P4/PROP-RP02 CHANGE_PROPAGATION_CAN_BE_DERIVED_FROM_CONSUMER_DEPENDENCY_GRAPH_WHILE CHANGE_AUTHORITY_REMAINS_NOT_EVALUATED_IF_PUBLIC_SOURCE_DOES_NOT_ESTABLISH_OWNER`.

This is important: lack of public authority data must not force guessed ownership.

---

# 8. Recovery path is part of interface acceptance

Incomplete journeys can trigger maximum-fare behavior, auto-completion, automatic refunds or customer-service review depending on circumstances.

This means failure recovery is part of the operational interface, not merely a customer-support afterthought.

### Replay result

`CONFIRMED`.

### Rule

`P4/IFC-RP13 MATERIAL_SERVICE_INTERFACE_REQUIRES_RECOVERY_OR_EXCEPTION_PATH_WHEN_NORMAL_PATH_FAILURE_HAS_USER_COST_OR_STATE_CONSEQUENCE`.

This generalizes to digital services, booking systems, access systems and operational workflows.

---

# 9. Controlled variable authority lesson

This replay exposes a subtle distinction:

`who supplies an event/value` is not necessarily `who owns the semantic rule that interprets it`.

Examples in the analytical model:

- a reader produces an observed touch event;
- journey logic interprets whether that event belongs to a particular journey context;
- fare logic interprets the resulting journey against fare rules;
- customer-service correction may alter the resulting charge outcome.

Therefore P4 should distinguish:

```yaml
value_producer:
semantic_interpreter:
change_authority:
consumer:
```

Existing `AUTHORITATIVE_PRODUCER / TRANSFORMING_CONSUMER` helps, but replay shows the semantic interpreter deserves an explicit role when transformation changes meaning rather than just format.

### Replay result

`UNDERMODELED → SEMANTIC INTERPRETER ROLE REQUIRED`.

### Rule

`P4/AUTH-RP06 VALUE_PRODUCTION_AUTHORITY_AND_SEMANTIC_INTERPRETATION_AUTHORITY_MUST_BE_DISTINGUISHABLE_WHEN_DERIVATION_CHANGES_MEANING_OR_OUTCOME`.

---

# 10. State and identity must travel together

A journey state without identity continuity is insufficient.

Example analytical failure:

```text
ENTRY_OBSERVED under credential A
EXIT_OBSERVED under credential B
```

Locally both events are valid, but they cannot necessarily produce one complete journey.

Therefore P4 needs a general invariant:

`state-bearing event must identify the semantic subject/session to which the state applies`.

### Rule

`P4/VAR-RP12 STATE_EVENT_REQUIRES_SUBJECT_OR_SESSION_BINDING; VALID_EVENT_WITH_WRONG_IDENTITY_BINDING_CANNOT_ADVANCE_TARGET_STATE_MACHINE`.

This is highly reusable across service workflows, digital sessions, physical access systems, manufacturing and clinical workflows.

---

# 11. Over-modeling checks

This replay also shows what should **not** become independent semantic objects by default.

Do not create separate canonical objects for every:

- tap event;
- fare calculation step;
- UI notification;
- derived refund amount;
- device presentation.

Event-level records may remain operational/runtime data unless they have independent lifecycle/audit/reuse responsibility.

P4 objectification threshold still applies.

### Rule

`P4/IFC-RP14 HIGH_VOLUME_EVENT_INSTANCES_REMAIN_EVENT_OR_RUNTIME_RECORDS_UNLESS_INDEPENDENT_LIFECYCLE_AUDIT_OR_DECISION_RESPONSIBILITY_REQUIRES_OBJECTIFICATION`.

---

# 12. Cross-domain findings

The replay confirms that P4 is not architecture-shaped.

Validated general concepts:

- Controlled Variable;
- STATE as a controlled variable class;
- CONTENT/SEMANTIC identity;
- hub-level Interface invariant;
- pairwise + hub hybrid topology;
- multi-dimensional interface acceptance;
- recovery/fallback continuity;
- material dependency by consequence;
- consumer-driven change propagation;
- distinction between producer and semantic interpreter;
- subject/session-bound state transitions.

New machine concepts required:

1. `identity_scope`;
2. `equivalence_policy`;
3. explicit `semantic_interpreter` role;
4. state-event subject/session binding;
5. service/transaction acceptance dimensions;
6. clearer `MATERIAL_DEPENDENCY` definition as consequence materiality.

---

# 13. Replay disposition

`TP4 CROSS-DOMAIN INTERFACE / CONTROLLED VARIABLE REPLAY = COMPLETE_WITH_DELTAS`.

This replay materially reduces the risk that P4 is only valid for architecture/geometry.

Still open:

- internal change-authority ownership was not public and remains `NOT_EVALUATED`;
- exact TfL internal architecture is not claimed;
- no inference is made from public service behavior to proprietary implementation detail.

Replay-derived rules:

- `P4/VAR-RP09`
- `P4/VAR-RP10`
- `P4/VAR-RP11`
- `P4/IFC-RP10`
- `P4/IFC-RP11`
- `P4/IFC-RP12`
- `P4/DEP-RP02`
- `P4/PROP-RP02`
- `P4/IFC-RP13`
- `P4/AUTH-RP06`
- `P4/VAR-RP12`
- `P4/IFC-RP14`

No Current promotion is authorized.