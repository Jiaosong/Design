# OLEANDER Service Blueprint / Operational Dependency Extension

Status: `CANDIDATE EXTENSION / EXISTING OWNER / EXTERNAL-MECHANISM DIGESTED / NO PROJECT USAGE / NO PROMOTION`

Owner: `oleander-design-process`

## Purpose

Use when a design promise experienced by a customer, visitor, resident, patient, operator, staff member or other service actor depends on hidden people, systems, data, policies, physical evidence, handoffs or operational capacity.

This extension connects:

`USER / ACTOR JOURNEY → TOUCHPOINT → FRONTSTAGE PROMISE → BACKSTAGE ACTION → SUPPORT SYSTEM / PARTNER → HANDOFF / DATA OBJECT → FAILURE / RECOVERY → OPERATIONAL EVIDENCE → DESIGN CONSEQUENCE`

It does **not** create a second Service Design framework, a new lifecycle, a CRM/operations owner, a user-research authority or a substitute for specialist system/interface validation.

A service blueprint is a **relationship and dependency artifact**. It is not proof that the service works in reality.

`BLUEPRINT COHERENT ≠ SERVICE VALIDATED ≠ OPERATIONS READY ≠ FIELD PASS`.

---

## 1｜When to activate

Activate when one or more of these are material:

- the user-facing experience depends on staff, partners, logistics, maintenance, booking, dispatch, payment, data or other hidden work;
- one visible touchpoint makes a promise that multiple backstage actors/systems must uphold;
- a journey spans physical + digital + human channels;
- service failure/recovery matters as much as the ideal path;
- ownership of a handoff is ambiguous;
- a delayed/missing internal action changes the user-visible state;
- physical evidence such as ticket, receipt, signage, package, token, confirmation, queue display or device state affects trust/orientation;
- a project has a journey map but cannot explain how the organization/system makes each step possible;
- different operational scenarios or capacity levels materially change the service experience.

Do not activate for:
- a single isolated UI flow with no meaningful backstage dependency;
- a purely visual journey board whose purpose is presentation only;
- a system integration problem better handled directly by `SYSTEM_INTERFACE_COUPLING_EXTENSION.md`;
- a research-only journey map before the service operation is in scope.

---

## 2｜Journey map, interaction flow and service blueprint are different

Keep these carriers distinct.

### Journey map

Primary question:

`WHAT DOES THE ACTOR EXPERIENCE ACROSS TIME / CHANNELS?`

Typical content:
- actor/persona;
- stage;
- actions;
- touchpoints;
- goals;
- evidence-backed observations;
- pain/friction;
- opportunity.

### Interaction / UX flow

Primary question:

`HOW DOES THE ACTOR MOVE THROUGH ONE PRODUCT / INTERFACE / TASK SURFACE?`

Typical content:
- states;
- actions;
- transitions;
- errors;
- permissions;
- return/recovery.

### Service blueprint

Primary question:

`WHAT HIDDEN WORK, SYSTEMS, HANDOFFS AND EVIDENCE MUST ALIGN TO DELIVER THAT EXPERIENCE?`

It adds:
- frontstage;
- backstage;
- support/process/system;
- line of visibility;
- handoff;
- operational dependency;
- failure/recovery;
- capacity/time;
- responsibility.

Do not stretch one artifact until it claims all three roles without explicit layers.

---

## 3｜Canonical-source rule

The blueprint must not become a second place to invent project facts.

Prefer:

`CANONICAL JOURNEY / PROCESS / ACTOR / SYSTEM / POLICY SOURCES → NORMALIZED RELATION MODEL → BLUEPRINT VIEW`

not:

`BLUEPRINT DIAGRAM → NEW UNSOURCED FACTS`.

For each blueprint cell/relation, record or preserve a source reference when material.

Source classes may include:
- observed journey evidence;
- Current project requirement;
- process/SOP;
- system behavior;
- staffing/operations record;
- policy/rule;
- partner contract;
- design assumption;
- unknown.

A rendered HTML/SVG/board is a **derived view** when its content is compiled from canonical records. Editing the view alone must not silently alter source truth.

If the blueprint is the first place a new operational fact is discovered, record it as:
`INFERENCE / ASSUMPTION / UNKNOWN`
until the proper source owner confirms it.

---

## 4｜Blueprint scenario contract

Do not create one giant “all users / all services” blueprint by default.

Each material blueprint should resolve:

- `blueprint_id`;
- `service_or_experience_scope`;
- `scenario_id`;
- `primary_actor_or_persona`;
- `trigger_or_entry_condition`;
- `start_state`;
- `end_state_or_outcome`;
- `context / channel / location`;
- `Current vs future-state status`;
- `source_revision`;
- `known exclusions`;
- `unverified assumptions`.

Examples of materially different scenarios:
- normal arrival vs late arrival;
- staffed vs unstaffed;
- connected vs offline;
- normal payment vs payment failure;
- standard mobility vs accessibility support;
- normal weather vs closure/degraded route;
- first-time vs returning user;
- low vs peak capacity.

Do not combine scenario differences into one average lane when failure/recovery or ownership changes.

---

## 5｜Minimum lane model

Use the minimum lanes needed for the decision. Typical service-blueprint lanes:

1. **Physical / Digital Evidence**
2. **Actor / Customer Actions**
3. **Frontstage**
4. **Backstage**
5. **Support Systems / Processes / Partners**

Optional lanes:
- policy/authorization;
- data/state;
- logistics/material;
- maintenance;
- environment/location;
- capacity/resource;
- measurement/evidence.

The lane names are not sacred OLEANDER taxonomy. The invariant is that **visible experience and hidden enabling work remain distinguishable**.

---

## 6｜Visibility classes

For each action/state, classify:

### ACTOR ACTION
What the served actor actually does.

### FRONTSTAGE
Visible human/system/environment action experienced by the actor.

Examples:
- staff greeting;
- UI response;
- signage state;
- queue display;
- confirmation message;
- physical handoff.

### BACKSTAGE
Hidden action that directly supports a frontstage moment.

Examples:
- dispatch;
- content preparation;
- inventory check;
- staff coordination;
- manual approval;
- internal data entry.

### SUPPORT
System, partner, infrastructure or recurring process that enables backstage/frontstage execution.

Examples:
- payment gateway;
- scheduling;
- content management;
- maintenance;
- supplier;
- identity service;
- transport system.

If an actor/action cannot be honestly classified:

`UNCLASSIFIED / UNVERIFIED`

with:
- missing source;
- owner needed;
- why the distinction matters.

Never guess an actor into frontstage/backstage merely to make the diagram look complete.

---

## 7｜Lines are semantic boundaries, not decoration

Three useful boundaries may be represented when they clarify the service:

### Line of Interaction
Between the served actor and the service-facing interaction.

Question:
`WHERE DOES THE ACTOR DIRECTLY EXCHANGE ACTION / INFORMATION / MATERIAL?`

### Line of Visibility
Between what the actor can perceive and hidden operational work.

Question:
`WHICH ACTION / STATE IS PART OF THE EXPERIENCED SERVICE PROMISE?`

### Line of Internal Interaction
Between direct service-delivery work and enabling/supporting systems/teams.

Question:
`WHERE DOES DELIVERY DEPEND ON ANOTHER INTERNAL / PARTNER OWNER?`

Do not draw these lines merely because a service-blueprint template contains them.

---

## 8｜Touchpoint / evidence ledger

For every material touchpoint, record as applicable:

- `touchpoint_id`;
- stage/scenario;
- actor;
- channel/location;
- visible artifact/state;
- actor action;
- intended service meaning;
- source/evidence;
- frontstage owner;
- backstage dependency;
- required data/material/state;
- failure condition;
- recovery cue;
- accessibility / inclusion requirement when applicable;
- privacy/security boundary when applicable;
- design artifact carrying the touchpoint.

Physical/digital evidence can include:
- signage;
- ticket;
- email;
- receipt;
- status light;
- interface screen;
- staff script;
- uniform/badge;
- package;
- confirmation;
- queue number;
- route marker;
- closure notice.

The existence of evidence does not prove its interpretation is correct. Test the intended meaning.

---

## 9｜Frontstage promise contract

A frontstage touchpoint often makes an implicit or explicit promise.

Represent:

`VISIBLE PROMISE → REQUIRED BACKSTAGE CONDITION → SUPPORT DEPENDENCY → PROOF / UNKNOWN → FAILURE CONSEQUENCE`

Examples:
- “confirmed booking” requires inventory/state lock;
- “open route” requires current closure/status authority;
- “ready for pickup” requires actual item/preparation state;
- “payment successful” requires transaction status reconciliation;
- “accessible entrance” requires real route/door/lift conditions.

Failure attack:

`CAN THE FRONTSTAGE SAY YES WHILE THE BACKSTAGE REALITY IS NO?`

If yes, the service design has a truth-risk.

Never solve this only with wording when the underlying dependency is broken.

---

## 10｜Handoff spine

A service often fails not inside one lane but at a handoff.

For every material cross-actor/system transfer record:

- `handoff_id`;
- sender;
- receiver;
- trigger;
- thing transferred;
- type: information / state / material / responsibility / permission / person / payment / service;
- format/schema/identifier when relevant;
- required timing/order;
- acknowledgement;
- ownership after handoff;
- failure/timeout condition;
- retry/escalation;
- user-visible consequence;
- evidence/log location;
- interface-owner handoff when deeper verification is needed.

When the exchanged thing is technically material, route detailed units/protocol/timing/ownership verification to `SYSTEM_INTERFACE_COUPLING_EXTENSION.md`.

The blueprint owns the **service consequence** of the handoff, not the specialist technical proof.

---

## 11｜Data and state through the service

When service behavior depends on data/state, record:

`STATE / DATA OBJECT → SOURCE → OWNER → MUTATION EVENT → CONSUMER → USER-VISIBLE CONSEQUENCE → FAILURE / STALE CONDITION`

Examples:
- booking state;
- route status;
- consent;
- payment state;
- inventory;
- identity/permission;
- maintenance condition;
- queue position;
- content version.

Do not draw “system” as a generic black box if a specific state/data object determines the experience.

Attack:
- stale state;
- duplicate state;
- missing acknowledgement;
- race/order issue;
- conflicting owners;
- offline/degraded behavior;
- privacy/permission mismatch.

Technical protocol correctness remains with the relevant system owner.

---

## 12｜Time, wait and synchronization

Time is often a design variable, not operational trivia.

For material steps record:
- expected sequence;
- start condition;
- wait state;
- maximum tolerated delay if actually sourced;
- actual/estimated duration state;
- visible wait cue;
- timeout behavior;
- backstage escalation;
- user recovery/return path.

Do not invent universal service-time thresholds.

If time is unknown but consequential:

`TIME UNKNOWN → DESIGN WAIT / RECOVERY STATE → MEASURE LATER`

rather than pretending the service is instant.

---

## 13｜Capacity and queue relation

Use when staff, seats, vehicles, rooms, inventory, processing slots or another finite resource can bottleneck the service.

Represent:

`DEMAND SCENARIO → RESOURCE CAPACITY → QUEUE / BUFFER → SERVICE RATE ASSUMPTION → USER-VISIBLE STATE → DEGRADE / CLOSE RULE → EVIDENCE CEILING`

Possible scenario classes:
- LOW;
- NOMINAL;
- PEAK;
- DEGRADED;
- CLOSED;
- UNKNOWN.

These are project-specific if used; they are not universal service-state IDs.

Do not infer capacity from a tidy blueprint.

When quantitative operational claims matter, route to the relevant operations/data/specialist owner.

---

## 14｜Failure-point model

For each material failure point:

- `failure_id`;
- triggering condition;
- affected actor/scenario;
- failed lane/dependency;
- detectability;
- visible symptom;
- hidden cause hypotheses;
- containment;
- recovery action;
- owner;
- escalation;
- evidence required to close;
- whether prior success evidence becomes stale.

Distinguish:
- user input error;
- frontstage execution failure;
- backstage process failure;
- support/system failure;
- partner failure;
- capacity overload;
- stale/missing data;
- policy/permission denial;
- physical/environmental failure;
- ambiguous ownership;
- design-induced confusion.

Do not default to “user error.”

---

## 15｜Recovery is part of the service design

Every critical failure should answer:

`WHAT DOES THE ACTOR SEE? → WHAT CAN THEY DO? → WHO OWNS RECOVERY? → CAN THEY RETURN / RETRY / EXIT SAFELY? → WHAT STATE IS PRESERVED?`

Recovery types:
- retry;
- alternate channel;
- staff escalation;
- defer/resume;
- refund/reversal;
- offline path;
- manual override with authority;
- safe exit/return;
- degraded service;
- closure.

A recovery path is not valid merely because a staff member could “handle it somehow.”

Make the actual dependency and authority visible.

---

## 16｜Service evidence and validation

Blueprint evidence classes:

### A. Source/Process Evidence
Shows what is specified or believed to happen.

Examples:
- SOP;
- system spec;
- staff instruction;
- contract;
- policy.

### B. Observed Operational Evidence
Shows what actually happened.

Examples:
- timestamped logs;
- queue records;
- transaction records;
- support cases;
- observation;
- journey trace.

### C. User/Actor Validation Evidence
Shows whether the service met the intended need in context.

Examples:
- task observation;
- real pilot;
- usability/service walkthrough;
- interview after actual use.

### D. Specialist Verification
Shows technical compliance/performance of a dependency.

Examples:
- payment reconciliation;
- network availability;
- accessibility inspection;
- safety verification;
- engineering test.

Keep them separate.

`PROCESS DOCUMENT EXISTS ≠ OPERATION ACTUALLY OCCURS`.

`SYSTEM PASS ≠ ACTOR EXPERIENCE VALIDATED`.

---

## 17｜Current-state and future-state separation

Never silently mix “today” and “proposed”.

Each blueprint element should be classifiable as:
- CURRENT OBSERVED;
- CURRENT REPORTED;
- CURRENT SPECIFIED;
- FUTURE PROPOSED;
- ASSUMED;
- UNKNOWN / UNVERIFIED.

A future blueprint can be useful before implementation, but it proves only:
- intended relation;
- intended ownership;
- intended process;
- intended recovery.

It cannot prove:
- staffing adequacy;
- real timing;
- reliability;
- adoption;
- user success;
- partner performance.

---

## 18｜Operational ownership

For each material backstage/support action, identify the real owner when known.

Possible owner forms:
- named role;
- team;
- partner;
- system/service;
- external authority.

Do not use vague owner labels such as:
- “backend”;
- “ops”;
- “system”;
- “staff”;
when actual responsibility matters and can be resolved.

If ownership is unresolved:

`OWNER = UNRESOLVED → HOLD`

for any claim that depends on accountable execution.

---

## 19｜Cross-channel continuity

When a service crosses physical/digital/human channels, test continuity of:
- identity;
- state;
- terminology;
- status;
- instructions;
- entitlement/permission;
- return/recovery;
- accessibility;
- evidence/receipt.

Failure example:

`APP SAYS CONFIRMED → STAFF SYSTEM HAS NO RECORD`

or:

`PHYSICAL SIGN SAYS OPEN → DIGITAL ROUTE SAYS CLOSED`.

Do not treat each channel as independently correct if the actor experiences one service.

---

## 20｜Service accessibility / inclusion boundary

The blueprint may expose where accessibility/support is required, but it does not self-certify accessibility.

Record:
- actor need/context;
- touchpoint;
- accommodation/support relation;
- frontstage behavior;
- backstage preparation;
- physical/digital/system dependency;
- unknowns;
- validation owner.

Do not treat a special-assistance lane as proof that the service is inclusive.

---

## 21｜Privacy / security / consent boundary

When service flow uses identity, personal data, payment, health, location, permission or other sensitive information, record only the dependency needed for design.

Represent:
`DATA / PERMISSION NEED → USER-VISIBLE REQUEST → BACKSTAGE USE → OWNER → RETENTION / SHARING QUESTION → SECURITY/PRIVACY OWNER`

The blueprint does not authorize collection or compliance.

Route legal/security/privacy claims to proper authority.

---

## 22｜Artifact-generation rule

The blueprint should ideally be generated or maintained from structured/canonical source records when project scale warrants it.

Preferred:

`SOURCE RECORDS → NORMALIZED BLUEPRINT MODEL → EDITABLE SVG/HTML/TABLE VIEW`

Useful properties:
- stable IDs;
- explicit lane/source bindings;
- deterministic labels;
- source revision;
- regenerable view;
- unclassified items surfaced;
- no authored truth hidden only in the render.

A static manually authored blueprint is acceptable for small work if:
- source/evidence links remain explicit;
- edits are traceable;
- it does not silently fork canonical process truth.

A PNG screenshot is presentation evidence, not the canonical blueprint master.

---

## 23｜Blueprint model schema

A project may use JSON/YAML/table forms. Conceptual minimum:

`blueprint`
- id
- scenario
- actor
- state: current/future
- source revision
- phases[]

`phase`
- phase_id
- trigger
- actor_actions[]
- evidence[]
- frontstage_actions[]
- backstage_actions[]
- support_actions[]
- handoffs[]
- failures[]
- measures[]

`action`
- action_id
- lane
- owner
- source_ref
- precondition
- output/state
- visible_to_actor
- status

`handoff`
- handoff_id
- sender
- receiver
- object/state
- trigger
- acknowledgement
- failure/recovery
- evidence_ref

No one schema is mandatory across projects; the stable semantic fields are the invariant.

---

## 24｜Service-design option generation

A blueprint is not only for documenting the current service. It can support materially different service options.

Valid option deltas may change:
- ownership model;
- channel mix;
- automation/human allocation;
- frontstage/backstage boundary;
- sequencing;
- handoff architecture;
- evidence/touchpoint strategy;
- recovery strategy;
- capacity allocation;
- offline/degraded behavior.

Invalid “different service concepts”:
- same workflow with new colors;
- same operations with renamed stages;
- one extra notification with unchanged dependency structure.

For each option:

`SERVICE CONCEPT FAMILY → MATERIAL OPERATIONAL DELTA → USER CONSEQUENCE → BACKSTAGE CONSEQUENCE → FAILURE TRADE-OFF → VALIDATION NEED`

Use existing Design Process option-space and trade-study rules for selection.

---

## 25｜Scenario / adverse-condition attack

Test at least the adverse scenarios relevant to the decision, such as:
- source data unavailable;
- staff absent;
- network offline;
- payment rejected;
- item unavailable;
- late arrival;
- queue overload;
- partner delay;
- accessibility support requested;
- closure/degraded route;
- conflicting channel status;
- interrupted/resumed journey.

No fixed scenario list is universal.

Attack question:

`DOES THE SERVICE STILL TELL THE TRUTH, PRESERVE STATE AND OFFER A VALID NEXT ACTION?`

---

## 26｜Operational dependency matrix

For complex services, create a compact matrix:

`FRONTSTAGE PROMISE × BACKSTAGE ACTION × SUPPORT SYSTEM × OWNER × HANDOFF × FAILURE × RECOVERY × EVIDENCE`

Use it to find:
- single points of failure;
- unowned promises;
- duplicated ownership;
- hidden manual work;
- unsynchronized status;
- missing recovery;
- unsupported user-facing claims.

The matrix is analysis support. It is not a release score.

---

## 27｜Integration with System Interface / Coupling

Use `SYSTEM_INTERFACE_COUPLING_EXTENSION.md` when the service blueprint exposes a technical or organizational boundary needing deeper contract analysis.

Service blueprint asks:
- what does this handoff mean to the actor/service;
- where does it appear;
- what promise depends on it;
- how does failure surface/recover.

System Interface asks:
- what exactly crosses the boundary;
- units/format/protocol;
- timing;
- ownership;
- states;
- integration verification.

Do not duplicate the same interface contract in two inconsistent records. Reference the interface ID.

---

## 28｜Integration with Human Factors / accessibility / physical space

The blueprint may identify:
- staff task;
- user task;
- queue/standing/wait;
- reach/contact;
- information demand;
- route/wayfinding;
- physical evidence.

But it does not prove ergonomic or accessibility success.

Route:
- human/task validation → Human Factors owner/extension;
- spatial route/geometry → relevant spatial/CAD/design owner;
- code/safety/accessibility compliance → specialist authority.

---

## 29｜Change propagation

A change to:
- journey stage;
- frontstage message;
- backend system;
- partner;
- staffing model;
- data object;
- policy;
- capacity;
- physical route;
- touchpoint;
- recovery path;

must identify affected:
- blueprint cells;
- handoffs;
- artifacts;
- staff instructions;
- digital states;
- signage;
- downstream validation;
- user-facing promise.

Use:

`CHANGE → AFFECTED SERVICE RELATIONS → AFFECTED ARTIFACTS / SYSTEMS / ROLES → STALE EVIDENCE → RETEST / REBLUEPRINT → STATUS`

Do not update only the visible touchpoint while leaving backstage behavior stale.

---

## 30｜Failure attacks

Reject or revise when:

- a journey map is called a service blueprint without backstage/support relations;
- internal process steps are presented as if the actor directly experiences them;
- a frontstage promise has no supporting backstage condition;
- an actor is guessed into a lane despite missing identity/role evidence;
- “system” is used as a black box where a specific state/data object matters;
- handoffs omit sender/receiver/thing/trigger/acknowledgement where these are material;
- only the ideal path is modeled;
- failure/recovery is delegated to unspecified staff improvisation;
- current-state and future-state are mixed;
- a process document is called operational proof;
- a system test is called service validation;
- a pretty blueprint screenshot becomes the source of truth;
- fixed time/capacity thresholds are imported from an external template without Current authority;
- a blueprint duplicates and drifts from the actual interface/process record;
- service-design vocabulary becomes a mandatory new OLEANDER lifecycle.

---

## 31｜Required outputs

Use only those relevant to the task:

1. `service_scope_scenario_contract`
2. `journey_source_binding`
3. `blueprint_lane_model`
4. `touchpoint_evidence_ledger`
5. `frontstage_promise_dependency_map`
6. `backstage_support_map`
7. `handoff_spine`
8. `data_state_dependency_map`
9. `failure_recovery_model`
10. `capacity_time_unknowns`
11. `owner_ledger`
12. `current_future_truth_states`
13. `cross_channel_continuity_findings`
14. `derived_editable_blueprint_artifact`
15. `operational_dependency_matrix`
16. `validation_handoffs`
17. `actual_service_readback_or_NOT_RUN`
18. `reopen_trigger`
19. `claim_ceiling`

---

## 32｜Owner routing

Remain inside `oleander-design-process` for the service-design relationship.

Route:
- journey/user evidence → `oleander-research`;
- interaction states → `oleander-web-ui` / UI interaction owner when digital;
- cross-system contract → `SYSTEM_INTERFACE_COUPLING_EXTENSION.md`;
- Human Factors → `HUMAN_FACTORS_VALIDATION_EXTENSION.md`;
- physical/product relation → relevant Design Process extension;
- data visualization → `oleander-data-viz`;
- blueprint visual hierarchy → `oleander-visual-design`;
- editable web blueprint → web/UI owner if interactive;
- technical/safety/code/accessibility/privacy claims → specialist VALIDATION owner;
- release/package integrity → `oleander-delivery-qc`.

No service-blueprint renderer becomes a service-authority owner.

---

## 33｜External mechanism digestion boundary

Mechanisms studied:
- frontstage/backstage/support separation;
- line of visibility / interaction;
- physical/digital evidence;
- failure points;
- timing/bottlenecks;
- canonical-process → derived blueprint view;
- explicit unclassified actor rather than guessed lane;
- cross-actor handoff spine;
- journey-map vs blueprint distinction.

Accepted:
- visibility boundary as service relation;
- frontstage promise ↔ backstage condition;
- unclassified/unverified fail-closed behavior;
- canonical-source-derived blueprint;
- handoff/data-object spine;
- failure/recovery as first-class service design;
- current/future separation;
- operational evidence distinct from process docs;
- blueprint as living/regenerable artifact.

Rejected as universal OLEANDER defaults:
- fixed five-lane template;
- fixed six phases;
- fixed service timing;
- fixed satisfaction metric;
- fixed customer persona count;
- service-design jargon as mandatory project taxonomy;
- external template as process authority;
- “customer” as universal actor label;
- process-document existence as operational validation.

No external code is required by this extension.

---

## 34｜Maturity

On creation:

`CANDIDATE EXTENSION / EXISTING OWNER / EXTERNAL MECHANISMS DIGESTED / GOLDEN REGRESSION REQUIRED / NO REAL PROJECT USAGE / NO CROSS-CONTEXT EVIDENCE / NO PROMOTION`

Promotion requires at least one real service/hybrid project that:
- binds a real journey source;
- exposes at least one hidden dependency or ownership gap;
- includes at least one failure/recovery path;
- produces an editable/regenerable blueprint artifact;
- records one actual operational/service readback or explicit NOT_RUN;
- changes a real design decision;
- does not duplicate the system-interface owner.

`BLUEPRINT COMPLETE ≠ SERVICE COMPLETE`.
