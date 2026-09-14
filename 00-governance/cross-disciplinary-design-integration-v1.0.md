# OLEANDER Cross-Disciplinary Design Integration v1.0

**Status:** ACTIVE<br>
**Date:** 2026-09-14<br>
**Scope:** complex projects in which two or more design / engineering / content / operational disciplines materially affect one another.<br>
**Position:** project-runtime integration layer. It does not create a new L0–L7 knowledge taxonomy, does not replace discipline review lenses, and does not replace technical or evidence gates.

## 1｜Why this layer exists

Single-discipline excellence does not guarantee an integrated design.

Complex projects fail when:

- interfaces are implicit or ownerless;
- one discipline changes a shared variable without propagating the effect;
- local optimization damages the whole-system intent;
- design and engineering teams validate against different assumptions;
- responsibility gaps sit between disciplines;
- the same interface has two incompatible authorities;
- a late technical correction destroys an earlier design decision without reopening critique;
- a cross-disciplinary issue is recorded as a generic warning rather than assigned, resolved and retested.

Therefore OLEANDER treats **integration quality** as an independent project concern.

`DISCIPLINE PASS ≠ INTEGRATION PASS`

## 2｜Trigger

Trigger this system when any of the following is true:

- two or more discipline lenses own material parts of the same design decision;
- one discipline's output is another discipline's required input;
- shared geometry, dimensions, states, content, materials, controls, routes or performance targets exist;
- physical, digital, service, brand or operational touchpoints must behave as one system;
- a change in one subsystem can invalidate another subsystem;
- multiple specialists / workers / external authorities contribute to the same promoted artifact;
- the project contains high-risk interfaces such as structure × MEP, product × electronics, physical × digital, content × wayfinding, landscape × drainage, space × accessibility, brand × UI, service × operations, or data × visual communication.

A project is not exempt merely because one person or one AI agent performs several disciplines. Integration risk comes from coupled design variables, not team size.

## 3｜Canonical integration model

The integration layer sits between discipline design resolution and final independent decision:

`Design Intelligence Packet → Discipline Review Resolve → Cross-Disciplinary Integration → Execute / Prototype → Discipline + Technical Validation → Integration Readback → Independent Design Decision`

The layer has six responsibilities:

1. **System decomposition** — identify subsystems without fragmenting the design intent.
2. **Interface definition** — define where disciplines exchange geometry, information, behaviour, responsibility or performance.
3. **Dependency control** — know what changes when a shared variable changes.
4. **Joint decision control** — resolve cross-disciplinary trade-offs explicitly.
5. **Integration verification** — test assembled behaviour, not only local outputs.
6. **Change propagation** — reopen every materially affected review/gate after a change.

## 4｜Cross-Disciplinary Integration Packet

Complex projects compile a `CROSS_DISCIPLINARY_INTEGRATION_PACKET` in addition to the normal Design Intelligence Packet.

Minimum fields:

- `integration_question` — what must work as one system;
- `participating_lenses`;
- `subsystems`;
- `shared_design_intent`;
- `system_success_conditions`;
- `interface_register`;
- `shared_variables`;
- `dependency_map`;
- `authority_map`;
- `discipline_owners`;
- `integration_owner`;
- `decision_rights`;
- `cross_discipline_tensions`;
- `coupling_profile`;
- `critical_interfaces`;
- `required_maturity_by_interface`;
- `interface_acceptance_contracts`;
- `integration_test_plan`;
- `change_propagation_rules`;
- `stale_or_reopened_interfaces`;
- `open_interfaces`;
- `integration_blockers`;
- `current_integration_receipt` when one exists;
- `promotion_ceiling`.

This packet is a project-runtime object, not a new knowledge node by default.

## 5｜System decomposition

Decompose only as far as needed to make relationships reviewable.

Typical subsystem classes include:

- people / stakeholder / operational system;
- spatial / site / architecture;
- structure / construction;
- product / hardware;
- CMF / material system;
- MEP / environmental systems;
- digital interface / software;
- content / information architecture;
- brand / visual-verbal language;
- service / process / backstage operation;
- exhibition / wayfinding / interpretation;
- data / sensing / analytics;
- maintenance / logistics / replacement;
- rights / safety / accessibility / sustainability overlays.

The decomposition must preserve the project-level design intent. Do not optimize each subsystem independently and assume the combined result will be coherent.

## 6｜Interface register

Every material interface records at least:

- `interface_id`;
- `side_a` and `side_b`;
- `interface_type`;
- `purpose`;
- `owner_a` and `owner_b`;
- `integration_owner`;
- `controlling_authority`;
- `inputs_from_a` / `inputs_from_b`;
- `outputs_to_a` / `outputs_to_b`;
- `shared_variables`;
- `constraints`;
- `tolerances_or_allowed_variation` when relevant;
- `coupling_relationship`;
- `criticality`;
- `required_maturity` for the current lifecycle / claim;
- `maturity = IDENTIFIED / DEFINED / COORDINATED / EXERCISED / VERIFIED`;
- `disposition = OPEN / BLOCKED / CLOSED / OUTSIDE_CLAIM`;
- `evidence_state`;
- `validation_method`;
- `acceptance_contract_id` when required;
- `readback_refs` when evidence exists;
- `change_reopen_rule`.

Interface types may include:

- physical / geometric;
- mechanical / structural;
- electrical / data;
- hydraulic / environmental;
- human / ergonomic;
- spatial / circulation;
- visual / perceptual;
- semantic / content;
- interaction / state;
- service / operational;
- brand / language;
- information / data schema;
- maintenance / replacement;
- temporal / lifecycle.

Do not overload one `status` field with both maturity and blockage. `COORDINATED` and `VERIFIED` describe **maturity**; `OPEN`, `BLOCKED`, `CLOSED` and `OUTSIDE_CLAIM` describe **disposition**. A blocked interface may still have useful prior maturity, and a mature interface may be reopened by change.

### 6.1｜Coupling relationship

Coupling describes how strongly one side depends on the other. Use descriptive classes rather than a new numbered project namespace:

- `INFORMATIVE` — one side must be aware of the other, but no material output is consumed and no shared variable is controlled across the interface;
- `DEPENDENT` — one side consumes a material output / constraint from the other; propagation is mainly directional;
- `RECIPROCAL` — both sides materially constrain one another or consume shared variables; change can propagate in both directions;
- `TIGHTLY_COUPLED` — the relationship itself cannot be judged reliably from isolated discipline outputs; assembled behaviour, joint readback or an integrated prototype is required.

Coupling is not a quality score and does not equal risk. A one-way `DEPENDENT` interface can still be `CRITICAL`, while a `RECIPROCAL` interface can be routine.

### 6.2｜Interface criticality

Criticality determines the minimum governance burden for an interface. Use:

- `ROUTINE` — limited consequence, easy to reverse, small dependency fan-out and low claim sensitivity;
- `MATERIAL` — failure would create a visible or functional design defect or force a meaningful revision;
- `MAJOR` — failure can invalidate multiple artifacts / disciplines, damage a primary design intent, or become expensive / difficult to reverse late;
- `CRITICAL` — failure can violate a hard safety / accessibility / regulatory boundary, invalidate a core promoted claim or system success condition, or create a non-containable whole-system failure.

Assess at least:

- consequence to people, use, experience and system behaviour;
- effect on shared design intent and promoted claims;
- safety / accessibility / regulatory consequence when applicable;
- dependency fan-out;
- uncertainty and assumption load;
- reversibility;
- late-change cost / disruption;
- sensitivity to controlling authority or evidence state.

Do not average these dimensions into a score that can dilute a hard failure. Any hard critical condition is sufficient to elevate the interface regardless of otherwise low scores.

### 6.3｜Integration maturity and disposition

Maturity records what has actually been resolved:

1. `IDENTIFIED` — the interface is known and its participating sides are named;
2. `DEFINED` — exchanged variables / behaviour, ownership, constraints and acceptance question are explicit;
3. `COORDINATED` — both sides agree on the current interface definition and controlling authority;
4. `EXERCISED` — the interface has been instantiated in an integrated prototype, coordinated model, state flow, rehearsal or other relevant readback;
5. `VERIFIED` — the current evidence satisfies the interface's acceptance contract for the stated claim ceiling.

Maturity must never imply a stronger evidence class than actually exists. `VERIFIED` means verified **against the current acceptance contract and claim ceiling**; it does not mean FIELD-observed, code-compliant, fabrication-ready or operationally proven unless those are explicitly part of the contract and evidence.

Disposition records current closure state:

- `OPEN` — work remains inside the current claim;
- `BLOCKED` — closure cannot progress because authority, evidence, dependency or design conflict is unresolved;
- `CLOSED` — required maturity for the current claim is met and no in-scope blocker remains;
- `OUTSIDE_CLAIM` — deliberately unresolved because the promoted claim explicitly excludes it.

An interface may be `COORDINATED + OPEN`, `EXERCISED + BLOCKED`, or `VERIFIED + CLOSED`. It may not be `CLOSED` below its required maturity.

`COORDINATED` may satisfy the required maturity only for a claim that is itself limited to definition / coordination. A claim about actual assembled behaviour, performance, operation or experienced relationship cannot close on coordination evidence alone; it requires an exercised readback and, for Promotion of that claim, normally `VERIFIED` evidence against the Acceptance Contract.

### 6.4｜Risk-proportionate governance

Governance effort scales with criticality and coupling; do not apply the heaviest process to every interface.

| Interface condition | Minimum governance floor |
|---|---|
| `ROUTINE` + low coupling | concise register entry; owner; change rule; lightweight readback if needed |
| `MATERIAL` | explicit acceptance question, current authority, required maturity and traceable readback |
| `MAJOR` | Interface Acceptance Contract; joint decision record when a real trade-off exists; integrated readback; explicit reopen scope |
| `CRITICAL` | full Acceptance Contract; no unresolved authority conflict; required integrated verification; explicit evidence/claim ceiling; independent whole-system review before Promotion |
| any `TIGHTLY_COUPLED` interface | assembled prototype / integrated readback is mandatory even if each discipline passes separately |

Criticality establishes the governance floor. Coupling may increase the required integration method, but it must not lower a critical interface's closure requirement.

## 7｜Shared-variable authority

Every high-impact shared variable must have one current controlling authority.

Examples:

- building grid / datum;
- product envelope;
- user height / reach assumptions;
- display dimensions;
- door / equipment clearance;
- route width;
- material thickness;
- color / token / typography role;
- navigation naming;
- state names;
- asset ID;
- sensor / data schema;
- maintenance access envelope;
- environmental target;
- project-wide accessibility assumption.

If two disciplines both believe they control the same variable, the interface is `BLOCKED` until authority is resolved.

## 8｜Dependency and change-impact graph

Complex projects maintain a practical dependency graph:

`shared variable / source → affected subsystem → affected artifact → affected review → affected gate`

For every material change, ask:

1. What changed?
2. Which interfaces consume it?
3. Which artifacts become stale?
4. Which design decisions must reopen?
5. Which technical/evidence gates must rerun?
6. Which promoted object is superseded if the change is accepted?

`LOCAL CHANGE ≠ LOCAL CONSEQUENCE`

No cross-disciplinary change is considered closed until affected downstream states are reconciled or explicitly declared unaffected with reason.

### 8.1｜Change impact classes and reopen scope

Classify the accepted change by consequence, not by file size or number of edited objects:

- `NON_MATERIAL` — editorial / representational correction with no change to locked design intent, shared variable, acceptance condition or claim;
- `LOCAL_MATERIAL` — material within one subsystem but no shared variable or downstream interface contract changes;
- `INTERFACE_MATERIAL` — changes an exchanged variable, tolerance, authority, interface behaviour or acceptance condition;
- `COUPLED_SYSTEM` — propagates through multiple interfaces / subsystems or changes a system success condition;
- `PROMOTION_BREAKING` — invalidates the basis of a currently promoted claim, canonical artifact or integration receipt.

Required reopen scope:

| Change class | Minimum reopen |
|---|---|
| `NON_MATERIAL` | no interface reopen; record reason if ambiguity exists |
| `LOCAL_MATERIAL` | affected discipline review + local artifacts; interface readback only if dependency analysis shows consumption |
| `INTERFACE_MATERIAL` | affected interface to at least `DEFINED`; both sides read back; acceptance contract / test rerun as applicable |
| `COUPLED_SYSTEM` | all affected interfaces, joint decisions, Design Review dependencies and triggered technical/evidence gates |
| `PROMOTION_BREAKING` | current integration receipt becomes stale; affected promoted object is no longer valid under the old basis and must be superseded / re-promoted after revalidation |

Change impact is not chosen by the author of one discipline alone when other disciplines consume the changed variable.

## 9｜Joint design decisions

Cross-disciplinary decisions require a `JOINT_DECISION_RECORD` when no single discipline can decide without materially constraining another.

Record:

- decision question;
- alternatives considered;
- participating disciplines;
- shared success conditions;
- discipline-specific benefits;
- discipline-specific costs;
- accepted trade-off;
- rejected alternatives and reasons;
- evidence / assumptions;
- authority used;
- resulting locked variables;
- resulting open variables;
- reopen trigger.

Do not resolve a real system trade-off by averaging discipline scores.

## 10｜Cross-disciplinary design tensions

Common tensions include:

- spatial clarity ↔ engineering density;
- structural depth ↔ ceiling / spatial proportion;
- accessibility ↔ compactness;
- maintainability ↔ visual concealment;
- brand consistency ↔ task-specific affordance;
- visual calm ↔ information completeness;
- landscape expression ↔ drainage / ecology;
- product thinness ↔ durability / battery / thermal needs;
- physical immersion ↔ digital assistance;
- novelty ↔ operational reliability;
- fabrication efficiency ↔ material expression;
- privacy ↔ personalization;
- sustainability ↔ replacement / service model;
- local experience ↔ system-wide consistency.

The integration layer records the chosen position and the cost of that choice.

## 11｜Integrated prototype rule

When interfaces are material, discipline-isolated prototypes are insufficient.

At least one prototype or readback should exercise the assembled relationship at the lowest cost appropriate to the decision, for example:

- spatial model + structure / MEP zones;
- 1:1 physical detail + human reach;
- product shell + mechanism + controls;
- service blueprint + actual interface state flow;
- wayfinding content + physical decision point;
- exhibition sequence + lighting + graphic hierarchy;
- responsive UI + content + motion + accessibility;
- landscape grading + water + path + planting;
- data schema + visualization + user decision task.

Integrated prototype fidelity is determined by the decision question, not by presentation ambition.

## 12｜Integration review passes

Complex projects should conduct integration reviews at material transitions, not only at the end.

Recommended review sequence:

- **IR-01 Intent Alignment** — do disciplines share the same project-level intent?
- **IR-02 Interface Definition** — are material interfaces explicit and owned?
- **IR-03 Dependency Review** — are shared variables and downstream dependencies known?
- **IR-04 Coordinated Concept** — do discipline concepts coexist without hidden contradictions?
- **IR-05 Integrated Prototype** — does the assembled relationship work?
- **IR-06 Change Impact** — have major revisions propagated correctly?
- **IR-07 Pre-Promotion Integration** — are all critical interfaces closed to the required state?
- **IR-08 Post-Use Integration** — did real operation expose interface failures or unanticipated coupling?

These are review events, not a new G-stage namespace.

### 12.1｜Lifecycle closure expectations

These expectations are **minimum closure conditions**, not a mandatory waterfall. Reviews may interleave, repeat or move earlier when risk requires.

- **Exploration / framing** — suspected interfaces and coupling may remain provisional; heavy contracts are unnecessary unless a critical constraint is already known.
- **Candidate** — all known `MAJOR / CRITICAL` interfaces are identified; participating owners, coupling, criticality, current authority conflicts, required maturity and intended validation route are visible.
- **Coordinated concept** — critical interfaces are at least `DEFINED`; high-impact shared-variable authority is resolved; `RECIPROCAL / TIGHTLY_COUPLED` interfaces needed to prove concept coherence are at least `COORDINATED`.
- **Integrated prototype** — every interface claimed by the prototype has relevant readback; `TIGHTLY_COUPLED` and in-scope critical interfaces reach `EXERCISED` unless explicitly outside that prototype's claim.
- **Canonical production** — material changes are classified; stale interfaces / artifacts / reviews are reopened according to impact; no interface remains implicitly valid after its controlling input changed.
- **Pre-Promotion** — every in-claim `CRITICAL` interface reaches required maturity, normally `VERIFIED`; `MAJOR` interfaces meet their Acceptance Contract; no in-claim critical interface is `BLOCKED`; the Integration Receipt is current.
- **G9 / post-use** — actual field / operational observations are recorded as a separate evidence state; observed behaviour may reopen a previously `VERIFIED` interface and generate a bounded knowledge candidate.

Pre-Promotion `VERIFIED` must not be reworded as field or operational validation when those observations do not exist.

## 13｜Integration validation matrix

For every critical interface, classify validation as one or more of:

- expert design review;
- drawing / model coordination;
- geometry / clash analysis;
- calculation / simulation;
- physical prototype;
- user / human-factors test;
- field observation / measurement;
- software / state test;
- accessibility test;
- operational rehearsal;
- maintenance / replacement rehearsal;
- independent external review.

The matrix must distinguish `NOT TESTED`, `TESTED UNDER ASSUMPTION`, `PASS`, `FAIL`, and `OPEN`.

### 13.1｜Interface Acceptance Contract

Every `MAJOR / CRITICAL` interface, and any other interface whose closure cannot be stated unambiguously, uses an `INTERFACE_ACCEPTANCE_CONTRACT`.

This is a project-runtime logical contract. It may be embedded directly in the Interface Register or referenced as a compact project record; it is not a new L-level knowledge object or project-stage namespace.

Minimum fields:

- `interface_id`;
- `acceptance_question` — what integrated relationship must be true;
- `expected_behavior_or_relationship`;
- `coupling_relationship`;
- `criticality`;
- `controlling_authority` and authority state;
- `shared_variables` and `tolerances_or_allowed_variation` where relevant;
- `required_maturity` for the intended claim;
- `required_validation_method`;
- `required_readback` / artifact or observation identity;
- `assumptions_and_evidence_state`;
- `pass_condition`;
- `failure_condition`;
- `claim_ceiling`;
- `acceptance_parties` — affected interface owners plus integration owner; authority owner / independent reviewer when triggered;
- `reopen_trigger`.

Closure is joint: one side may provide the evidence, but one side alone cannot declare a material cross-disciplinary interface closed when the other side is materially affected.

For a `TIGHTLY_COUPLED` interface, discipline-isolated checks cannot satisfy the contract. The required readback must exercise the assembled relationship.

An expert opinion alone is insufficient when the acceptance question concerns behaviour that can and should be exercised, measured, simulated, rehearsed or observed at the current project stage.

## 14｜Integration issue ledger

Cross-disciplinary issues should not disappear inside discipline notes.

Each material issue records:

- issue ID;
- affected interfaces / artifacts;
- disciplines involved;
- observed conflict;
- design consequence;
- severity;
- owner;
- proposed resolution;
- authority / evidence dependency;
- required retests;
- status;
- resolved version / artifact identity.

Blockers cannot be closed by one side of the interface without readback from the other materially affected side.

### 14.1｜Cross-Disciplinary Integration Receipt

At material integration decisions and before Promotion, compile a compact `CROSS_DISCIPLINARY_INTEGRATION_RECEIPT` as the whole-system verification object.

Minimum fields:

- project / candidate / artifact / version identity;
- `integration_question` and `system_success_conditions`;
- participating disciplines / lenses and subsystems;
- `critical_interface_summary` with coupling, criticality, required maturity, actual maturity and disposition;
- unresolved `MAJOR / CRITICAL` interfaces;
- blocked interfaces and unresolved authority conflicts;
- shared-variable authority summary;
- relevant `JOINT_DECISION_RECORD` references;
- integrated prototype / model / state-flow / rehearsal / field readback references;
- acceptance-contract results and evidence state;
- material changes since prior receipt and their impact classes;
- reopened discipline reviews / technical gates / evidence reviews and results;
- stale artifact / interface status;
- `integration_findings` — strongest resolved relation plus weakest / open system relation;
- `integration_verdict = PASS / REVISE / REJECT / HOLD`;
- `promotion_ceiling`;
- `does_not_prove` — explicit exclusions such as FIELD validity, code compliance, fabrication readiness or real-use performance when they were not tested;
- integration owner / independent reviewer where required / date.

Machine checks may validate completeness and impossible combinations, including:

- no `PASS` when an in-claim `CRITICAL` interface is `BLOCKED`;
- no `PASS` when required maturity is unmet;
- no `PASS` when a high-impact shared variable has unresolved controlling authority;
- no `PASS` when a required integrated readback is missing;
- no `PASS` when a material change has made the receipt stale;
- no Promotion above the receipt's `promotion_ceiling`.

Machines must not auto-award `PASS` or whole-system design quality from counts, maturity labels or averaged interface scores. An Integration `PASS` only states that the required cross-disciplinary relationships are sufficiently closed for the claim; the independent Design Decision may still be `REVISE / REJECT / HOLD` for design-quality reasons.

The receipt is an Integration Readback object, not a new Gate or G-stage. It references discipline / technical / evidence receipts instead of duplicating their detailed findings.

## 15｜Responsibility and decision rights

Every complex project distinguishes:

- **discipline owner** — owns professional quality inside a discipline;
- **interface owners** — own both sides of a material interface;
- **integration owner** — owns whole-system coherence and unresolved interface escalation;
- **authority owner** — owns a controlling source / requirement where applicable;
- **independent reviewer / jury** — owns final design-quality judgment where required.

AI workers may detect conflicts, propose options and maintain the integration records. They must not silently settle a material cross-disciplinary trade-off by optimizing one subsystem unless the governing contract grants that authority.

## 16｜Promotion rule for complex projects

When this system is triggered, Promotion requires:

1. participating disciplines and subsystem boundaries are explicit;
2. critical interfaces are registered;
3. shared-variable authority conflicts are resolved;
4. no unresolved integration blocker contradicts the promoted claim;
5. material cross-disciplinary decisions have joint rationale;
6. required integrated prototypes / readbacks are complete;
7. affected reviews and gates were rerun after material changes;
8. each critical interface reaches its declared required maturity and is `CLOSED`, or is explicitly `OUTSIDE_CLAIM` without contradicting the promoted claim;
9. a current `CROSS_DISCIPLINARY_INTEGRATION_RECEIPT` records integration closure and promotion ceiling;
10. independent design judgment evaluates the whole system, not only discipline outputs.

`ALL DISCIPLINES PASS + INTEGRATION FAIL = NOT PROMOTION ELIGIBLE`

## 17｜G9 learning

Post-use interface failures are high-value knowledge candidates.

Capture:

`expected interface behaviour → observed behaviour → failure / success → contributing disciplines → root relation → lesson candidate`.

Reusable outcomes may become an interface pattern, anti-pattern, failure mode, trade-off rule or method update inside the existing L0–L7 Knowledge Architecture after validation.

## 18｜Canonical invariants

`MULTIDISCIPLINARY PRESENCE ≠ INTEGRATED DESIGN`<br>
`DISCIPLINE PASS ≠ INTEGRATION PASS`<br>
`MODEL FEDERATION ≠ DESIGN COHERENCE`<br>
`CLASH-FREE ≠ EXPERIENCE-COHERENT`<br>
`SHARED FILE ≠ SHARED AUTHORITY`<br>
`LOCAL OPTIMUM ≠ SYSTEM OPTIMUM`<br>
`CHANGE ISSUED ≠ CHANGE PROPAGATED`<br>
`INTERFACE DOCUMENTED ≠ INTERFACE VERIFIED`<br>
`TECHNICAL COORDINATION ≠ DESIGN SYNTHESIS`<br>
`COUPLING STRENGTH ≠ INTERFACE CRITICALITY`<br>
`VERIFIED ≠ FIELD-VALIDATED`<br>
`INTEGRATION PASS ≠ DESIGN KEEP`<br>
`RECEIPT COMPLETE ≠ WHOLE-SYSTEM EXCELLENCE`
