# 2026-09-18｜Service Blueprint / Operational Dependency Digestion

Status: `DIGESTED / EXISTING-OWNER MAPPED / CANDIDATE EXTENSION IMPLEMENTED / GOLDEN REGRESSION ADDED / REAL-PROJECT REAPPLICATION PENDING / NO PROMOTION`

## Question

OLEANDER already has:
- journey/service project artifacts;
- UI/interaction state;
- System Interface / Coupling;
- Information Requirement / Exchange;
- Human Factors;
- option-space / trade study;
- source/evidence/validation governance.

The missing question was:

> Can OLEANDER explicitly connect a user-visible service promise to the hidden people, systems, data, handoffs, capacity and failure-recovery relations required to deliver it?

The answer was: **not yet at reusable Skill granularity**.

C04 contains service/journey project artifacts, but no reusable service-blueprint execution contract existed in `oleander-design-process`.

---

## Sources reviewed

### 1. bbrewington/software-data-and-ai-tools

Pinned commit:

`38c562684a20d0a048783345ead9671b696ef0a1`

Reviewed:
- `skills/service-design/SKILL.md`
- `skills/service-design/references/service-blueprints.md`

License boundary:
- no readable root LICENSE was found during this review;
- research reference only;
- no source prose/code/template copied.

Useful mechanisms:
- actor/location/props/associates/process scope;
- customer action / frontstage / backstage / support layering;
- line of interaction / visibility / internal interaction;
- physical evidence;
- failure point marking;
- time / bottleneck / metrics;
- journey first, blueprint second;
- operational sustainability as distinct from visible experience.

Rejected:
- fixed lane/template form as universal OLEANDER structure;
- generic service-design lifecycle as a new OLEANDER method;
- generic customer-satisfaction metrics as proof;
- template examples as project authority.

### 2. VictorHueni/homemade-claude-kit

Pinned commit:

`5b8e134df4b1f0463ba355fea162325dee5c334a`

License: MIT.

Reviewed:

`plugins/delivery-comms/skills/com-artefact-viz/SKILL.md`

This source is particularly useful because it treats a service blueprint as a **derived composition view**:

`canonical process/value-stream/persona artefacts → normalized model → HTML blueprint view`

rather than as a second authored source.

Useful mechanisms:
- source artifacts remain canonical;
- blueprint view is regenerable;
- actor classification is derived from source;
- unresolved classification becomes an explicit `Unclassified` band;
- line of visibility is derived, not manually beautified;
- cross-actor handoff spine lists data objects;
- source changes require re-render;
- visual renderer does not author operational truth.

OLEANDER transfer:
- blueprint artifact should preserve source bindings;
- derived visual must not become authority;
- unresolved actor/visibility classification must remain `UNCLASSIFIED / UNVERIFIED`;
- handoff objects deserve stable identity;
- rendering PASS is not service validation.

Rejected:
- their exact directory architecture;
- their parser/template schema;
- CSS/design token implementation;
- business artifact naming conventions;
- renderer itself as an OLEANDER required tool.

### 3. argen/hornero

Pinned commit:

`68a686cd07251ffe15683295aae6f724e143fd69`

License: MIT.

Reviewed:

`roles/product-manager/skills/customer-journey-map/SKILL.md`

Useful boundary:
- journey map = actor experience across time/touchpoints;
- service blueprint = hidden organizational/process relation behind that experience;
- UX flow = path through a particular product/interface.

Useful evidence discipline:
- inferred thoughts/emotions must remain inferred rather than findings;
- touchpoints include non-owned channels;
- opportunities should remain outcome/problem statements rather than prematurely hard-coded features;
- journey artifacts go stale after material service/product change.

OLEANDER transfer:
- do not merge journey, UX flow and service blueprint into one ambiguous artifact;
- Current/Future and evidence/inference boundaries must remain explicit;
- blueprint reopens after relevant service changes.

---

# Existing-first mapping

## Already owned — not duplicated

### Journey/user evidence

Owner:
`oleander-research` + project Current evidence.

No new customer-research Skill.

### Interaction states

Owner:
`oleander-web-ui` / existing UI interaction candidate when applicable.

No new interaction/state-machine owner.

### System interfaces

Owner:
`SYSTEM_INTERFACE_COUPLING_EXTENSION.md`.

Service blueprint may reference an interface ID but does not duplicate protocol/unit/state/timing verification.

### Information exchange

Owner:
`INFORMATION_REQUIREMENT_EXCHANGE_CONTRACT_EXTENSION.md` when formal information delivery obligations apply.

### Human factors

Owner:
`HUMAN_FACTORS_VALIDATION_EXTENSION.md`.

### Visual blueprint composition

Owner:
`oleander-visual-design`, or `oleander-web-ui` for an interactive blueprint.

### Release / package integrity

Owner:
`oleander-delivery-qc`.

---

# Material gap accepted

The new extension owns only the **service relationship layer**:

`JOURNEY / TOUCHPOINT → FRONTSTAGE PROMISE → BACKSTAGE CONDITION → SUPPORT DEPENDENCY → HANDOFF → FAILURE / RECOVERY → OPERATIONAL EVIDENCE → DESIGN CONSEQUENCE`

Implemented:

`oleander-skills/oleander-design-process/SERVICE_BLUEPRINT_OPERATIONAL_DEPENDENCY_EXTENSION.md`

No new Core Skill was created.

---

# Granular accepted mechanisms

## 1. Scenario contract

Each blueprint declares:
- service scope;
- actor/persona;
- trigger;
- start/end state;
- context/channel/location;
- Current vs Future;
- source revision;
- exclusions;
- unknowns.

This prevents “all users / all scenarios” averaging.

## 2. Lane semantics

Potential lanes:
- physical/digital evidence;
- actor action;
- frontstage;
- backstage;
- support.

They are semantic roles, not fixed graphic rows.

## 3. Visibility boundary

Useful questions:
- what is directly experienced;
- what is hidden;
- what crosses from hidden work into visible promise.

The line itself is not important; the boundary is.

## 4. Frontstage promise contract

`VISIBLE PROMISE → REQUIRED BACKSTAGE CONDITION → SUPPORT DEPENDENCY → PROOF / UNKNOWN → FAILURE CONSEQUENCE`

This is the main design mechanism.

## 5. Handoff spine

Record:
- sender;
- receiver;
- trigger;
- object/state/responsibility;
- acknowledgement;
- timing where material;
- failure;
- recovery;
- user-visible consequence;
- evidence.

## 6. Data/state dependency

Avoid “system” black boxes.

Record the exact:
- booking state;
- route status;
- permission;
- payment status;
- inventory;
- maintenance state;
- queue state;
etc., when it changes user-facing behavior.

## 7. Failure point model

Failure is first-class:
- trigger;
- lane/dependency;
- visible symptom;
- hidden cause hypotheses;
- containment;
- recovery;
- owner;
- evidence to close.

## 8. Recovery path

A service failure must answer:
- what user sees;
- what they can do;
- who owns recovery;
- what state is preserved;
- whether retry/return/exit exists.

“Staff will help” is not sufficient unless the actual role, authority and process are known.

## 9. Current/Future truth state

Every material blueprint element should be distinguishable as:
- Current observed;
- Current reported;
- Current specified;
- Future proposed;
- Assumed;
- Unknown/unverified.

## 10. Cross-channel continuity

The actor experiences one service even when implementation spans:
- app;
- web;
- signage;
- staff;
- email;
- physical environment.

Local channel PASS cannot override cross-channel contradiction.

## 11. Capacity/time boundary

The blueprint may expose capacity/time dependencies but does not invent numbers.

Unknown consequential timing becomes:
`UNKNOWN → wait/recovery design → measure later`

rather than fake instantaneous service.

## 12. Operational evidence class

Separate:
- process/spec source;
- observed operational evidence;
- user/actor validation;
- specialist verification.

## 13. Derived artifact rule

Preferred at scale:

`canonical records → normalized blueprint model → editable SVG/HTML/table`

The render remains derivative.

## 14. Change propagation

A change to journey/state/staff/system/partner/policy/capacity/touchpoint/recovery must reopen affected blueprint relations and evidence.

---

# Failure knowledge retained

1. Journey map presented as service blueprint despite missing hidden delivery relations.
2. Internal process described as if it were directly experienced.
3. Visible service promise without backstage condition.
4. Unknown actor guessed into a lane.
5. “System” black box hides the state/data object that actually controls the experience.
6. Handoff lacks sender/receiver/thing/trigger/acknowledgement.
7. Ideal path only.
8. Recovery delegated to unspecified staff improvisation.
9. Current and future state mixed.
10. Process document called operational proof.
11. System PASS called user/service validation.
12. Pretty blueprint screenshot becomes source of truth.
13. Generic service template injects fixed timing/capacity assumptions.
14. Blueprint duplicates/drifts from actual interface/process record.
15. “Customer” vocabulary becomes universal when actual actor is visitor/operator/patient/resident/etc.

---

# Explicitly rejected from OLEANDER Core

Do not promote:
- fixed five-lane blueprint;
- fixed phase count;
- fixed service time targets;
- NPS/CSAT/CES as universal measures;
- fixed persona count;
- service-design jargon as mandatory taxonomy;
- generic service design lifecycle as Project State;
- one renderer/parser implementation;
- one customer-centric worldview where provider/operator/system safety may be equally material.

---

# Machine and regression integration

Existing owner:
`oleander-design-process`

Machine capability additions:
- `service_blueprint_contract`;
- `frontstage_promise_dependency_map`;
- `handoff_spine`;
- `failure_recovery_model`;
- `operational_dependency_matrix`;
- `derived_editable_blueprint_artifact`.

Gate:
`service_blueprint_operational_dependency_when_triggered`.

Golden cases:
- `SK-DES-017` — false confirmation vs delayed backstage reservation;
- `SK-DES-018` — unclassified actors + Current/Future mixing;
- `SK-DES-019` — cross-channel OPEN/CLOSED contradiction + offline degraded path;
- `SK-DES-020` — polished complete blueprint falsely promoted to operations-ready.

---

# Maturity boundary

Current batch target:

`EXTERNAL SERVICE-BLUEPRINT MECHANISMS DIGESTED → EXISTING OWNER MAPPED → CANDIDATE EXTENSION → MACHINE CAPABILITY SYNC → GOLDEN REGRESSION → REAL C04 REAPPLICATION → CI / READBACK → NO PROMOTION WITHOUT EVIDENCE`

A blueprint is a design reasoning artifact.

It does not prove:
- live service performance;
- staffing adequacy;
- partner reliability;
- accessibility compliance;
- privacy/legal compliance;
- field status;
- user validation;
- operational readiness.

`BLUEPRINT COMPLETE ≠ SERVICE COMPLETE`.
