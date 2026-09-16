# OLEANDER Systems Engineering Design Development Process v1.0

Status: **CANDIDATE PROFESSIONAL-DOMAIN PROCESS / NOT CURRENT / NO PROJECT-EXERCISE CLAIM**  
Professional-domain owner: **Systems Engineering**  
OLEANDER placement: **R-E Professional Domain Execution Process**, subordinate to the Current Professional Domain Process Contract, Knowledge Authority, Cross-Disciplinary Integration, Actual Readback/Review and human Promotion boundaries.

## 1｜Why this process exists

Systems Engineering is triggered when project success depends on the behavior of a **system of interacting parts, interfaces, states, operators, services or lifecycle conditions**, rather than on one discipline/object in isolation.

It exists to answer questions such as:

- what system purpose and stakeholder outcomes are actually in claim;
- where the system boundary is and what sits outside it;
- which needs are goals, which are authoritative requirements, and which remain assumptions;
- how requirements are allocated to functions, components, people, interfaces and evidence;
- which functional/logical architecture and physical allocation are retained, and why;
- which interfaces or coupled blocks can defeat otherwise-correct subsystems;
- what configuration is being integrated, verified or validated;
- which evidence proves requirement conformance versus actual stakeholder/context fitness;
- what change invalidates prior evidence and what must be reverified/revalidated;
- what observed in-use behavior is project feedback versus a bounded reusable-learning candidate.

The process is not a universal V-model, aerospace review sequence, MBSE tool prescription, requirements database, certification authority or replacement for Architecture/Structure/MEP/HCD/Software/Controls/Operations professional ownership.

Hard separations:

`REQUIREMENT SATISFIED ≠ STAKEHOLDER NEED VALIDATED`  
`COMPONENT PASS ≠ INTERFACE PASS ≠ INTEGRATED SYSTEM PASS`  
`MODEL / DIAGRAM EXISTS ≠ SYSTEM BEHAVIOR VERIFIED`  
`VERIFICATION PASS ≠ VALIDATION PASS ≠ OPERATIONAL / STATUTORY APPROVAL`  
`ONE PROJECT OUTCOME ≠ UNIVERSAL SYSTEMS RULE`

## 2｜Professional source and transfer boundary

This candidate compiles mechanisms already digested inside OLEANDER from:

- NASA Systems Engineering Handbook material on stakeholder expectations, technical requirements, logical decomposition/design solution, integration, verification, validation, transition, configuration/interface/change and V&V planning;
- the existing OLEANDER `REQUIREMENT_VERIFICATION_TRACEABILITY_EXTENSION.md`;
- the existing OLEANDER `SYSTEM_INTERFACE_COUPLING_EXTENSION.md`;
- the existing OLEANDER `PHYSICAL_PROTOTYPE_TEST_VV_EXECUTION_EXTENSION.md`;
- existing Current owners for Trade Study, FMEA, Simulation Protocol, Measurement Uncertainty, Human Factors, Reliability/Durability, specialist engineering and Design Quality/DD.

Accepted mechanisms:

- stakeholder/source → need → bounded requirement/constraint → object/interface → proof trace;
- explicit system purpose and boundary;
- functional/logical decomposition without forcing one notation;
- alternative architecture and trade comparison under fixed criteria;
- interface/coupling contracts with direction, exchanged quantities/states, timing, units and ownership where material;
- configuration-bound integration and evidence;
- explicit verification versus validation purpose;
- fidelity-to-claim and as-run evidence;
- anomaly/failure capture before repair;
- impact-driven reverify/revalidate after change;
- operational transition and in-use feedback with bounded G9 return.

Rejected as universal OLEANDER defaults:

- mandatory ISO/IEC/IEEE 15288 lifecycle adoption;
- one V-model as the project structure;
- fixed SRR/PDR/CDR/ORR or aerospace gate sequence;
- mandatory `shall` syntax;
- fixed T/A/I/D verification vocabulary;
- DOORS/Jama/Polarion/Cameo/SysML or any other tool as process authority;
- generic safety factors, reliability targets, sample sizes or risk matrices detached from the project/domain authority;
- NASA article-class names as OLEANDER maturity states.

## 3｜Trigger and claim ceiling

Trigger this professional process when one or more of the following is material:

- multiple subsystems/domains jointly satisfy one project requirement or stakeholder outcome;
- system behavior crosses physical, data, control, service, human, organizational or temporal interfaces;
- configuration identity affects evidence validity;
- requirements must remain traceable through design changes and verification;
- integration order or coupling can change the result;
- emergent behavior cannot be inferred by summing subsystem results;
- verification and validation planning is needed for a multi-object/multi-state design claim;
- operational transition, degraded/failure behavior or system-level change requires controlled re-evaluation.

Do **not** trigger merely because a project is complex, contains many drawings, uses software, or has a list of tasks. If one domain can own the question without a material system/interface relation, route it to that domain owner instead.

The process claim ceiling is always the lowest valid ceiling among:

`stakeholder/source authority / requirement authority / configuration identity / subsystem professional evidence / interface maturity / V&V evidence / operational context / independent review / external approval`.

## 4｜Core systems-engineering control objects

### 4.1 System Purpose / Context / Boundary Record

Minimum content:

`system purpose / stakeholders / use contexts / included objects / excluded environment / external systems / operators / lifecycle states / operating modes / degraded or failure states / assumptions / claim ceiling`.

A boundary must explain **what crosses it**. A box around a diagram with no exchanged matter, energy, information, person, service, permission, load, signal or responsibility is not a meaningful system boundary.

### 4.2 Need → Requirement → Evidence Trace

For each material obligation:

`source/stakeholder → need/goal → atomic requirement or constraint → rationale/priority → acceptance/failure condition → allocation to function/object/interface → verification method → evidence/configuration → status → change impact → reverify/waiver`.

Requirements that cannot be falsified remain goals/hypotheses until operationalized. Do not convert a design implementation detail into authority merely because it was written early.

### 4.3 Functional / Logical Architecture

Resolve, as applicable:

- functions required to satisfy needs/requirements;
- input/output/state and control relationships;
- operational scenarios and modes;
- normal, transition, degraded, failure and recovery behavior;
- sequence/timing where behavior depends on order;
- allocation boundaries that remain intentionally undecided;
- functions that depend on people/operators rather than components;
- functions crossing more than one professional owner.

The logical architecture is not a decorative block diagram. It must expose at least one consequential relation or decision.

### 4.4 Physical / Implementation Architecture and Allocation

Bind the selected logical behavior to actual system elements only at the maturity justified by evidence. Record:

`function / requirement → allocated object or human role → configuration item → interface(s) → responsible owner → native source → acceptance evidence`.

Allocation is reversible when a later trade/interface/evidence result invalidates the selected route. A selected vendor, software package, room, component or subsystem does not become a requirement unless its implementation constraint is itself authoritative.

### 4.5 Interface / Coupling Ledger

For each material interface, resolve only the fields needed by the decision:

- two-sided object/owner identity;
- interface class: physical / spatial / structural / electrical / fluid / thermal / information / control / service / human / organizational / temporal;
- exchanged quantity/state/service and direction;
- unit / coordinate frame / protocol / format where material;
- timing/order/latency or sequence where material;
- normal/degraded/failure/recovery state behavior;
- authority on both sides;
- configuration/revision on both sides;
- coupling/iteration consequence;
- verification object and evidence;
- requested R-F interface maturity;
- reopen trigger.

R-F remains the owner of actual interface maturity/disposition. Systems Engineering may issue requirements and consume accepted R-F bindings; it may not create a competing Integration truth source.

### 4.6 Configuration Baseline / Evidence Pedigree

Before a system-level verification or validation claim, identify the exact configuration being claimed:

`configuration ID / constituent revisions / interface revisions / software/controls version / data/configuration set / substitutions / test article or environment / known differences from Current / evidence ceiling`.

Evidence from another configuration is stale unless an explicit equivalence/reuse justification survives impact review.

### 4.7 V&V Matrix

For every material claim:

`requirement/need → DEVELOPMENT / VERIFICATION / VALIDATION purpose → object/interface → article/configuration → method → required fidelity/environment → setup/support equipment → variables/observables → predeclared acceptance/failure/stop condition → run/readback ID → evidence → result → anomaly/deviation → disposition → reopen/retest → claim ceiling`.

The matrix is a proof-obligation carrier, not a scorecard. Blank or unresolved rows remain OPEN.

### 4.8 Anomaly / Change / Reverification Record

On material failure or change:

`freeze observed/as-run state → capture evidence → distinguish requirement / interface / component / environment / procedure / measurement / configuration rival causes → controlled change → affected requirements/interfaces/evidence → bounded reverify/revalidate set → new evidence`.

Do not repair first and reconstruct the failure later. Do not rerun everything by habit; do not preserve every prior PASS by default.

## 5｜SYS-00 — System Purpose, Context and Boundary

### Professional question

> What system is actually being designed, for whom, in which operating contexts and states, and where do its professional/technical boundaries begin and end?

### Required inputs

- Current project authority / brief / stakeholder sources;
- known user/operator/maintainer and external-system context;
- current domain boundaries and responsibility map;
- existing-system / legacy / site / infrastructure context where applicable;
- material assumptions and unknowns.

### Systems work

- distinguish stakeholder outcome, project goal, requirement, constraint and implementation preference;
- define system-of-interest and external context;
- define normal, degraded, emergency/failure, maintenance and transition states where material;
- identify external systems/services and human roles crossing the boundary;
- identify domain owners and unresolved authority boundaries;
- identify system-level failure consequences that cannot be localized to one component;
- establish the first bounded system context / boundary model.

For each decision-critical operational scenario, record actor/role, goal, precondition, initiating event, external services available, system mode, information visible to the actor, automated actions, required human actions, transition/handoff points, degraded/failure branch, recovery/return-to-service, maintenance/support dependency and the stakeholder outcome being protected. The operating concept must expose what changes between nominal, degraded and recovery operation; a state name alone is not a usable ConOps.

For every external service whose loss, corruption or delay can change an in-claim system outcome, model it as a dependency with an owner and failure contract rather than a context label. Preserve service supplied/consumed, provider/consumer, availability/state assumptions, startup/reconnect dependency, data/time/identity/configuration dependency where relevant, degradation on loss, buffering/manual fallback, recovery/reconciliation behavior, evidence source and which downstream functions become invalid when the dependency is absent or stale.

Trace chained/common-cause dependencies across systems of systems: two “independent” subsystems may share utility, network, clock, identity provider, cloud/service endpoint, cooling, operator, maintenance resource or physical route. If a digital/network trust boundary is material, consume Cybersecurity/IT-owner requirements for identity/authentication, privilege, remote access, update/configuration integrity, logging/time source and recovery as interface inputs; Systems Engineering owns dependency/trace and system consequence, not cybersecurity control design or security PASS. R-F retains actual interface maturity/disposition. A locally verified subsystem cannot carry system availability/resilience/security consequence across an unverified external dependency.

### Native outputs

- system context / boundary model;
- stakeholder/need register;
- responsibility/authority boundary map;
- operating-state/scenario set;
- initial system-level open-risk / unknown register.

### Acceptance threshold

The stage can support bounded PASS only when another domain can tell what is inside/outside the system, what crosses each material external boundary, which operating states are in claim and which source/owner controls each material need. A generic “system diagram” without boundary consequences fails.

### Handoff / reopen

Hand off system purpose, boundary, stakeholders, operating scenarios and unresolved authority points to SYS-01 and affected professional owners. Reopen on material stakeholder, scope, environment, external-system, operational-state or authority change.

**Does not prove:** requirement completeness, architecture feasibility, integration success, verification, validation or project Promotion.

## 6｜SYS-01 — Needs, Requirements, Constraints and Acceptance Architecture

### Professional question

> Which obligations are authoritative/testable enough to govern design, and how will each material obligation be proven without collapsing verification into validation?

### Systems work

- decompose material goals into atomic requirements/constraints only where falsifiable;
- bind source/rationale and authority;
- identify derived requirements separately from externally authoritative requirements;
- declare acceptance/failure conditions before proof interpretation;
- allocate requirements initially to function/object/interface without prematurely freezing implementation;
- identify verification proof class appropriate to each claim;
- identify validation questions tied to stakeholder need/context;
- record waiver/deviation authority and residual consequence;
- establish bidirectional traceability and change-impact links.

### Native outputs

- requirement/constraint set;
- requirement-source-rationale trace;
- acceptance/failure criteria register;
- verification/validation planning matrix at current maturity;
- waiver/deviation register;
- requirement-change impact graph or equivalent trace.

### Acceptance threshold

No in-claim requirement needed for the next stage is allowed to be only “easy / robust / safe / premium / compliant / integrated” without an observable acceptance boundary. The exact proof method may remain OPEN, but the requirement and the consequence of failure must be sufficiently clear to prevent post-hoc threshold movement.

### Requirement quality and acceptance-architecture depth

Requirements must remain traceable to the **decision or obligation they protect**, not only to a document paragraph. For every material requirement / constraint, review as applicable:

- source class and controlling authority: external obligation, stakeholder need, project decision, derived engineering requirement or temporary assumption;
- exact object / function / interface / user / state to which it applies;
- observable outcome or prohibited condition;
- units, tolerance, range, environment, timing, duration or configuration where these are material;
- normal, degraded, maintenance, emergency or transition state applicability;
- rationale and the failure consequence if unmet;
- dependency on another requirement, interface or external source;
- verification proof class and whether the proposed proof can actually observe the requirement;
- validation relation to the underlying stakeholder need, where conformance alone may still miss the need;
- waiver/deviation owner and residual consequence if the requirement is relaxed.

Attack requirement defects explicitly:

- compound requirements joining several independently pass/fail conditions;
- implementation-prescriptive wording that hides the true outcome unless the implementation is actually mandated;
- unverifiable adjectives or outcome words without acceptance boundary;
- conflicting requirements whose trade-off has no authorized disposition;
- duplicated requirements with diverging thresholds;
- derived requirements with no rationale / parent trace;
- a verification method that can only test a proxy rather than the requirement itself;
- a threshold written after the result is known.

Where acceptance requires multiple proofs, define the relation among them: all required, alternative/equivalent, conditional, staged or representative-only. A requirement cannot be closed by a convenient evidence type that ignores a controlling failure mode.

`TRACE LINK EXISTS ≠ REQUIREMENT IS WELL FORMED`.

`VERIFIABLE REQUIREMENT ≠ VALID STAKEHOLDER NEED`.

### Handoff / reopen

Hand off requirement IDs, source/authority, acceptance conditions and current allocations to SYS-02/03 and professional owners. Reopen on source/brief/need change, waiver, accepted deviation, new failure mode or evidence showing the requirement is ambiguous/unverifiable.

**Does not prove:** the chosen design satisfies the requirements or that the requirements fully capture stakeholder need.

## 7｜SYS-02 — Functional / Logical Architecture and Behavior

### Professional question

> What functions, state transitions and interactions must exist for the system to satisfy the current need/requirement set without assuming a preferred physical solution too early?

### Systems work

- define material functions and functional dependencies;
- identify input/output/control/state relations;
- map operational sequences and scenarios;
- expose normal/transition/degraded/failure/recovery behavior;
- identify human/operator functions and automation boundaries;
- allocate critical human/automation work across detect → interpret/decide → command/act → confirm/prove → recover, including handover authority, mode awareness, acknowledgement failure and return-to-auto behavior where material;
- identify coupled blocks requiring iteration rather than fake linear sequencing;
- identify emergent behaviors needing system-level evidence;
- test whether functions can be allocated in more than one credible way.

### Native outputs

- functional/logical architecture;
- scenario/state/sequence models;
- function-to-requirement trace;
- preliminary function-to-owner allocation;
- emergent-behavior / system-level V&V questions.

### Acceptance threshold

The logical architecture must explain consequential behavior under the states in claim. Boxes/arrows that do not expose state, exchanged object, timing, dependency or decision consequence where those are material are insufficient.

### Behavior, timing and resource-contention depth

Functional/logical modeling must expose behavior that can fail **between boxes**. Where material, model:

- preconditions and postconditions for each critical function;
- state ownership and the event / condition that causes transition;
- sequence, concurrency and synchronization rather than only a left-to-right nominal path;
- queue, buffer, storage or inventory state where demand can accumulate;
- timing / latency / timeout / retry or deadline relationships where late behavior is failure even if the function eventually completes;
- shared resource contention, capacity or mutual exclusion where multiple functions compete for one resource;
- command / acknowledgement / proof / feedback distinction;
- human decision points, information available at the decision, workload and authority to intervene;
- automation fallback, manual takeover and return-to-auto conditions where relevant;
- startup, shutdown, maintenance, degraded, fail-safe and recovery states;
- external-service unavailability and reconnection/re-entry behavior;
- emergent behavior arising from coupled loops or independently acceptable subsystems.

Use scenario traces to attack races and hidden assumptions: two valid requests arriving together, delayed data, stale state, partial subsystem availability, interrupted sequence, duplicate command, failed acknowledgement, restart in mid-process or human intervention at an unexpected state.

The model may remain qualitative where quantitative timing/capacity is not yet authoritative, but the **dependency and failure consequence** must still be visible. Do not invent universal timing or queue thresholds.

`NOMINAL SEQUENCE WORKS ≠ CONCURRENT / DEGRADED BEHAVIOR WORKS`.

### Handoff / reopen

Hand off functions, scenarios, state relations and unresolved allocation choices to SYS-03/04. Reopen on requirement, operating scenario, human/automation responsibility, failure-state or major external-interface change.

**Does not prove:** physical feasibility, component sizing, software correctness, human factors validity or integrated performance.

## 8｜SYS-03 — Alternatives, Trade Studies and Physical Allocation

### Professional question

> Which system architecture / allocation should be retained, under what criteria and assumptions, and which choice-sensitive uncertainties could reverse it?

### Systems work

- generate materially distinct architecture/allocation options where real alternatives exist;
- compare using fixed decision criteria tied to Current goals/requirements;
- expose sensitivity to uncertain loads/demands/use/environment/interfaces;
- allocate functions and requirements to physical, digital, human and service elements;
- expose resulting spatial, technical, operational, maintenance and interface consequences;
- identify configuration items and responsibility boundaries;
- preserve rejected options and reversal conditions rather than rewriting history around the selected route.

### Required comparison form

`criterion / requirement → option difference → behavior/performance consequence → interface/coupling consequence → human/operational consequence → lifecycle/maintenance consequence → uncertainty/sensitivity → retain/reject reason → reopen condition`.

### Native outputs

- option set / trade record;
- selected system architecture / allocation model;
- allocation trace;
- decision-critical assumption/sensitivity register;
- preliminary configuration-item set.

### Acceptance threshold

The retained route must beat or deliberately trade against credible alternatives under declared criteria. “Selected because preferred / cleaner / standard / easiest to model” is insufficient unless those are authorized project criteria with real consequences.

### Trade-study sensitivity and non-compensatory constraint depth

Trade studies must distinguish **hard feasibility constraints** from preference criteria. A numerically attractive option cannot compensate for violating a requirement / interface / safety / authority constraint that is non-negotiable at the current ceiling.

For material decisions:

- keep raw option consequences visible before any normalization or weighting;
- state which criteria are hard gates, which are graded trade-offs and which are informational only;
- bind weights / priorities to Current project authority rather than analyst preference;
- show when one criterion dominates the result and whether a plausible priority change reverses selection;
- run sensitivity on uncertain demand, load, cost, reliability, human-use, maintenance or interface assumptions capable of changing the preferred option;
- identify options that are dominated, conditionally viable or only viable after another owner closes an interface;
- keep irreversible / path-dependent choices separate from options that can be deferred or staged;
- expose lifecycle consequences such as commissioning, training, spares, replacement, software/support dependency or future configuration constraints where they are selection drivers.

When a score is used, retain the underlying evidence and consequences. A weighted total must not conceal a catastrophic weakness, an unverified input or two alternatives that are practically indistinguishable within uncertainty.

`HIGHEST WEIGHTED SCORE ≠ AUTOMATIC SYSTEM DECISION`.

### Handoff / reopen

Hand off selected architecture, allocations, assumptions and reversal conditions to SYS-04 and subsystem/domain owners. Reopen when controlling criteria, requirement, demand, interface, cost/lifecycle constraint or selection-critical assumption changes materially.

**Does not prove:** subsystem technical adequacy, interface acceptance, manufacturing/installation readiness or validation.

## 9｜SYS-04 — Interface, Coupling and Configuration Architecture

### Professional question

> Are system boundaries between allocated elements explicit enough that integration can proceed without hidden unit/state/timing/geometry/ownership mismatches?

### Systems work

- establish material interface requirements and shared variables;
- identify direction, units, coordinates, timing, state, protocol/format and responsibility as applicable;
- identify mutually coupled blocks and required iteration order;
- define configuration identification needed for integration/evidence;
- identify interface failure hypotheses separately from component failure;
- define requested R-F maturity for each interface relevant to the current system claim;
- identify interfaces requiring integrated rather than component-only tests;
- establish interface change/reopen rules.

### Native outputs

- material interface ledger / interface-control carriers as appropriate;
- coupling/dependency map;
- integration sequence/iteration plan;
- configuration baseline / item-revision map;
- interface verification objects;
- R-F interface requirement set.

Treat a configuration baseline as the **minimum controlled set needed to reproduce the behavior/evidence in claim**, not merely a document revision list. For each material configuration item preserve, as applicable, item ID/owner, hardware/software/data/model/procedure identity, parameter/setting set, interface version, applicable requirement set, accepted deviation/waiver and effective state/date. Distinguish proposed, approved, implemented, as-integrated, as-tested and as-operated configuration when they differ. A later test cannot close an earlier/different baseline unless equivalence is demonstrated. Baseline changes identify superseded evidence and consuming interfaces; historical evidence remains bound to its original configuration rather than being rewritten.

Systems Engineering owns configuration architecture and trace for the system claim; domain owners retain technical truth and R-F retains actual interface maturity/disposition.

### Acceptance threshold

Every in-claim interface capable of invalidating system behavior has an identifiable source/owner, exchanged variable/state/service, current configuration and verification route. File/API/connector existence alone is not interface closure.

### Interface compatibility / tolerance and coupling depth

For each behavior-critical interface, define producer-side quantity/state/service and consumer-side admissible condition in the **same frame**. Record as applicable:

- units and scaling;
- sign / direction convention;
- coordinate / datum / reference frame;
- timing / ordering / latency / timeout;
- value tolerance / range / resolution;
- validity / quality / stale-data condition;
- update / acknowledgement / handshake semantics;
- initialization / restart / reconnect state;
- operating-mode applicability;
- configuration identity on both sides.

Where several interfaces form a coupled loop, identify what must be solved iteratively, which owner controls which variable, the convergence / stop rationale at the current claim ceiling, and what happens when convergence is not reached.

Attack end-to-end mismatches that can survive component-level checks: tolerance stack-up, unit conversion, rounding/quantization, datum drift, clock/timebase mismatch, stale state, duplicated message/command, different startup assumptions or incompatible fallback states.

Preserve the integrated evidence capable of exposing the mismatch. Systems Engineering defines compatibility requirements and coupling logic; R-F retains actual interface maturity/disposition and domain owners retain technical truth.

`BOTH SIDES LOCALLY VALID ≠ INTERFACE COMPATIBLE`.

### Handoff / reopen

Issue stage-side interface requirements to R-F; consume actual maturity/disposition only from R-F. Reopen on either-side configuration change, shared-variable/tolerance change, interface-owner change, timing/state change or new coupling/failure evidence.

**Does not prove:** actual interface maturity, subsystem PASS, integrated system PASS or external certification.

## 10｜SYS-05 — Integration and V&V Planning / Readiness

### Professional question

> Is there a credible configuration-bound plan to integrate the system and obtain the evidence needed for each in-claim verification and validation question?

### Systems work

- define integration order based on dependencies/coupling and fault-isolation value;
- identify prerequisites before each integration step;
- distinguish developmental test, requirement verification and stakeholder/context validation;
- choose evidence vehicle by claim: inspection, analysis, simulation, demonstration, browser/runtime proof, physical test, human task evidence, field observation or hybrid method;
- define test/prototype article pedigree and fidelity-to-claim;
- define setup, fixture, environment, support equipment and instrumentation where material;
- predeclare acceptance/failure/stop conditions for formal closure activities;
- identify evidence/retest dependencies and anomaly-preservation requirements;
- verify that planned evidence observes emergent system behavior where required.

### Simulation / analytical evidence credibility depth

When analysis or simulation is a planned proof vehicle, bind the model to the claim rather than treating model execution as evidence by itself. Record as applicable:

- governing equations / behavioral assumptions or logical rules;
- input, boundary and initial conditions;
- parameter sources and uncertainty;
- simplifications / omitted mechanisms and why they are acceptable at the claim ceiling;
- exact configuration represented;
- outputs / observables and how they map to the requirement or failure mode;
- numerical / temporal / spatial / logical resolution where it can change the result;
- solver / engine / model implementation revision and settings that materially affect interpretation;
- validation / credibility basis against independent reference, experiment or field evidence appropriate to the claim;
- extrapolation beyond the range where the model has been compared with reality or benchmark evidence.

Distinguish **model implementation verification** from **model validation/credibility**. A correctly solved model can still represent the wrong physics/behavior, and a model calibrated to one dataset is not independently validated by that same dataset.

Identify inputs whose uncertainty can reverse the conclusion and plan sensitivity / uncertainty treatment before interpreting a pass. Where measurement uncertainty materially overlaps the acceptance boundary, preserve that ambiguity rather than converting a marginal result into false precision.

Use the Current Simulation Protocol / Measurement-Uncertainty owners where triggered; Systems Engineering does not create a competing numerical-method authority.

`CONVERGED SOLVER / PLAUSIBLE TRACE ≠ MODEL CREDIBILITY FOR THIS CLAIM`.

### Native outputs

- integration plan / sequence;
- V&V matrix;
- test/prototype configuration and fidelity plan;
- procedure/readback plan;
- evidence ownership map;
- anomaly/change/retest plan.

### Acceptance threshold

Every in-claim requirement/need needed for the next closure has a credible proof route against the correct configuration, and every system-level behavior has an evidence vehicle capable of exposing its material failure mode. “Test later” without object/configuration/method/criterion remains HOLD.

Build verification coverage as a relation, not a test count:

`requirement / interface / emergent behavior → configuration → operating state → environment/load → failure mechanism → proof method → observable → acceptance source → evidence record`.

Where one result supports several requirements, state which observable supports each claim. Where one requirement depends on several proofs, state whether all, conditional, alternative/equivalent or representative evidence is required. Representative/sampled coverage must name the equivalence class and excluded combinations; untested state/configuration/interface combinations remain `OPEN` when they can expose a distinct failure mechanism. Coverage review should attack orphan requirements, orphan tests, repeated nominal evidence with no boundary/degraded-state evidence and proxy evidence that cannot observe the governing failure. The process installs no universal coverage percentage or sample count.

### Verification / validation experiment-design depth

Every planned proof must answer: **what configuration, which claim, under what conditions, with what observability, and what would make it fail?**

For test / simulation / demonstration / inspection / analysis evidence, define as applicable:

- exact test article / model / prototype / software / installation configuration and its fidelity to the production/operational object;
- requirement / need / interface claim being evaluated and the specific failure mode the method can expose;
- preconditions, environment, support equipment and external-service state;
- controlled variables versus nuisance / uncontrolled variables;
- stimulus / load / input range and boundary / adverse states needed for coverage;
- instrument / logging / observer source and measurement uncertainty where it could affect disposition;
- sample / repetition / scenario coverage rationale proportionate to the claim, without installing a universal sample-count rule;
- acceptance / failure / abort / stop condition declared before formal interpretation;
- independence / witness requirement where the claim requires it;
- post-test configuration inspection where the act of testing can damage or alter the article;
- equivalence rationale when evidence from one article/model/configuration is reused for another.

Simulation evidence must state model validation / calibration basis and where extrapolation exceeds observed or benchmarked behavior. Demonstration evidence may show a function once without proving margin, reliability or boundary behavior. Inspection may confirm attributes without proving performance. Select the evidence vehicle by failure mechanism, not convenience.

`TEST ARTICLE SIMILAR ≠ CONFIGURATION EQUIVALENT`.

`TEST EXECUTED ≠ CLAIM OBSERVED`.

### Handoff / reopen

Hand off evidence obligations, configuration identities and procedures to execution owners, R-H/R-I and specialist validation owners. Reopen on configuration, requirement, interface, method, environment, support-equipment or acceptance-criterion change.

**Does not prove:** any requirement verified, need validated, test competence or safe execution of a test outside its specialist owner.

## 11｜SYS-06 — Integration, Verification and Anomaly Resolution

### Professional question

> Does the integrated configuration satisfy the current verified requirement set at the declared evidence ceiling, and are anomalies understood enough to support the bounded disposition?

### Systems work

- integrate in the planned order or record justified divergence;
- preserve exact as-integrated/as-run configuration;
- execute/read back requirement verification evidence from responsible owners;
- verify material interfaces and emergent behavior rather than summing subsystem PASS;
- capture failures/anomalies before repair;
- separate rival causes: requirement, interface, component, environment, setup/procedure, measurement, configuration;
- apply controlled repair/change and impact analysis;
- determine bounded reverify/retest set;
- update requirement/interface/configuration/evidence trace.

Derive reverification scope from dependency rather than convenience. For each accepted change, trace:

`changed requirement / configuration item / parameter / interface / procedure → directly dependent functions and requirements → coupled interfaces / shared resources → emergent system behavior → prior evidence whose represented configuration/assumption is stale → regression / revalidation set`.

Preserve the rationale for evidence intentionally not rerun. A local change with no local requirement delta can still reopen system evidence when it changes timing, load, resource contention, fault containment, operator procedure or a shared interface.

### Native outputs

- integrated configuration record;
- verification evidence / requirement status;
- interface/system-level test evidence;
- anomaly/failure records;
- corrective-action/change-impact records;
- reverification/retest evidence;
- unresolved verification HOLD set.

### Acceptance threshold

System verification PASS requires the **current integrated configuration** and its in-claim requirements/interfaces to have evidence meeting predeclared criteria with no unresolved blocking anomaly. A component PASS, stale test or simulation of the wrong configuration cannot carry the system verdict.

### Anomaly diagnosis and bounded causal inference

Preserve the failure before repair. An anomaly record should retain exact configuration, state, sequence, environment, inputs, logs/measurements, observed symptom and first occurrence context before anyone resets, patches or retunes the system.

Use competing hypotheses proportionate to the failure, for example:

- requirement / acceptance criterion defect;
- interface mismatch in units, timing, state, geometry or ownership;
- component/subsystem defect;
- integration sequence or configuration error;
- software/data/control logic issue;
- human procedure / training / task interaction;
- environment / load / supply condition outside assumption;
- test fixture / support equipment / instrumentation problem;
- stale or wrong configuration / version identity.

Select discriminating checks that can separate hypotheses before changing several variables at once. If a repair is made, record the exact change and why it should affect the hypothesized mechanism, then rerun the affected verification plus any regression scope implied by coupling.

For each plausible cause, state the observable signature expected if it is true, the evidence that would weaken/contradict it, and the smallest safe test or configuration change capable of separating it from alternatives. Order checks to preserve fault isolation; do not introduce a broad repair that masks the original mechanism before enough evidence is captured.

Repeat/reproduce observations when variability, noise, timing or configuration drift could explain the symptom, and carry relevant measurement uncertainty into the disposition. Fault injection or hazardous/degraded-state testing remains with the competent specialist/test owner.

Do not erase a failure because the immediate symptom disappears after restart or because a second run passes. Intermittency, race, thermal state, residual configuration or operator sequence may remain unresolved.

Root-cause confidence must match evidence. Where only a bounded corrective fix is proven, state that ceiling rather than promoting the explanation to universal causal truth.

`ANOMALY DISAPPEARED ≠ ROOT CAUSE FOUND`.

### Handoff / reopen

Hand verified configuration, unresolved limitations and anomaly/change trace to SYS-07 and consuming professional/project owners. Reopen when configuration, requirement, interface, repair, evidence method or accepted anomaly changes materially.

**Does not prove:** stakeholder/context validation, operational acceptance, reliability population claims, statutory approval or Design KEEP.

## 12｜SYS-07 — Validation, Transition and Operational Readiness

### Professional question

> Does the verified system satisfy the actual stakeholder need and intended operational context sufficiently to transition at the current claim ceiling?

### Systems work

- validate representative user/operator/task/environment/use scenarios;
- test operational sequences, degraded/failure/recovery behavior and handoffs where material;
- compare actual stakeholder outcome to requirement conformance rather than assuming equivalence;
- confirm configuration and training/procedure/operational dependencies;
- expose remaining operating limits, deferred validation, maintenance/support and monitoring needs;
- distinguish transition readiness from statutory/release/project Promotion authority;
- capture unresolved needs or new requirements discovered through validation.

### Native outputs

- validation evidence / need disposition;
- operational-readiness / transition constraints;
- training/procedure/support dependency set;
- deferred-validation / operating-limit register;
- validated-configuration reference;
- new/reopened requirement records where actual need was missed.

### Acceptance threshold

Validation PASS is bounded to the represented stakeholder/task/environment/configuration. It requires actual evidence of the need/context in claim; verification conformance alone cannot substitute.

### Validation representativeness and operational-context depth

Validation must preserve what was actually represented:

- stakeholder / operator / maintainer groups and material exclusions;
- task / mission / service objective and failure consequence;
- physical / digital / organizational environment;
- workload, staffing, information, training and support state;
- normal plus material degraded / emergency / maintenance conditions;
- external systems / utilities / services available during the evidence;
- exact integrated configuration and operating procedure;
- observation period / repetition / scenario basis appropriate to the claim.

Distinguish **can perform**, **did perform under test**, **operators can sustain**, and **meets stakeholder outcome in real operation**. These are different validation ceilings.

When a representative environment is simulated, identify which cues, constraints, delays, consequences or social/organizational conditions are missing and whether their absence could materially change behavior or outcome.

Validation failure may reveal a bad requirement, allocation, interface, procedure, training model or original need interpretation—not merely a need for user training. Route the defect back to the causal owner instead of patching the validation script.

### Handoff / reopen

Hand validation boundaries and operational constraints to project authority, operations/FM/service and relevant professional owners. Reopen on user/task/context/operational-state/configuration/operational-procedure change or contradictory in-use evidence.

**Does not prove:** universal user acceptance, future field performance, release/statutory approval, project Promotion or every lifecycle condition.

## 13｜SYS-08 — In-use Change, Reverification and Learning

### Professional question

> What does actual operation/change reveal, which prior requirement/interface/evidence claims must reopen, and what—if anything—is reusable beyond this project?

### Systems work

- observe system behavior under declared context/time window;
- compare actual state to requirement/validation assumptions;
- assess modifications, substitutions, external-system changes and new operating modes;
- identify affected requirements/interfaces/configurations/evidence;
- run bounded reverification/revalidation as required;
- preserve anomaly, maintenance, reliability, user/operator and operational evidence;
- route project repair immediately through existing owners where needed;
- route reusable lesson only as a bounded G9/Knowledge/Evolution candidate with transfer boundary/counterevidence.

### Operational change-detection and reliability evidence depth

In-use assessment should distinguish at least:

- one-off anomaly;
- recurring failure mode;
- drift / degradation;
- maintenance- or repair-induced change;
- external-service / utility / supply change;
- demand / mission / user-context shift;
- latent configuration or version change.

Bind operational evidence to the observation window, exact configuration, exposure/opportunity denominator, duty cycle / mission / use state, maintenance/repair history and data completeness needed for the question.

Compare observed failure / availability / recovery patterns with the assumptions that supported verification and validation. Where population/reliability claims are material, consume the proper Reliability / Measurement owners rather than inferring rates from a handful of incidents.

When operational reliability evidence is used to justify a change, separate exposure/opportunity, recurring mode, repair action, configuration age, maintenance regime and common external cause. Check whether a repair merely suppresses the symptom, shifts the failure to another mode or changes the population/exposure being compared. After change, evaluate recurrence against the new configuration and equivalent operating opportunities before claiming improvement. Reliability-rate/statistical sufficiency stays with the proper Reliability/Measurement owner; Systems Engineering consumes it for configuration/change impact and reverification decisions.

Trend, change-point or before/after comparison remains bounded by data quality, configuration stability and rival explanations. A changed operating population, external dependency or maintenance regime can stale prior evidence even when the system artifact itself did not change.

Operational observation may justify targeted reverification or validation reopen immediately; it does not need to wait for reusable Knowledge promotion. Reusable learning remains candidate-only until the existing lifecycle closes.

### Native outputs

- in-use system assessment;
- change-impact / reverification record;
- designed-vs-observed behavior record;
- configuration/change history relevant to current claim;
- project reopen decision;
- bounded G9 lesson / evolution candidate refs where justified.

### Acceptance threshold

Each in-use assessment closes only its declared observation/change question. Causal claims require more than co-occurrence; transfer claims require evidence beyond one project/context.

### Handoff / reopen

Route project repair to affected owners immediately. Route Knowledge/Evolution candidates separately through R-K/R-B/Evolution without delaying necessary project reopen. Reopen on any later observation/change that invalidates the bounded assessment.

**Does not prove:** future performance, causality from one observation, transferable knowledge, Current Knowledge, Current Runtime revision or universal system validity.

## 14｜Stage acceptance and professional verdict semantics

A Systems Engineering stage may support `PASS` only when, at its claim ceiling:

1. controlling sources/needs/requirements are current or explicitly bounded;
2. configuration identity is explicit wherever a different configuration could change the conclusion;
3. every material cross-boundary dependency has an owner and evidence route;
4. native system/requirements/interface/V&V carriers are current and actual readback exists;
5. required domain-owner evidence has not been replaced by Systems Engineering prose;
6. blocking in-claim anomalies/unknowns are zero or the verdict remains `HOLD/REVISE`;
7. interface maturity/disposition used by the claim is consumed from R-F rather than invented locally;
8. the stage distinguishes verification, validation and operational observation where relevant;
9. the handoff identifies controlled variables, configuration, evidence ceiling and reopen trigger;
10. required independent/professional review is bound to the exact input revision/configuration.

Use:

- `REVISE` when the systems route is viable but requirement/architecture/interface/V&V logic or evidence is materially inadequate;
- `HOLD` when required source authority, subsystem professional evidence, interface state, configuration identity, test/validation evidence or independent review is unavailable;
- `REJECT` when the current system architecture/route cannot credibly satisfy the declared need/requirements/constraints and should not proceed;
- `PASS` only for the bounded systems-engineering question actually evidenced.

## 15｜Cross-disciplinary interface contract

Systems Engineering issues **stage-side interface requirements** to the existing Integration owner. Typical consumers/providers include:

- Project/Design Authority — stakeholder outcomes, acceptance priorities, scope and promotion boundary;
- Architecture / Interior / Landscape — physical/spatial allocation, users, operational flows and maintainability;
- Structural — loads/supports/movement/structural configuration;
- MEP / Controls — demand/capacity/state/control/failure behavior and commissioning evidence;
- Digital Product / HCD / Software — tasks, information/state behavior, human/automation boundary and runtime evidence;
- Fire / Accessibility / Safety / Specialist Engineering — externally or professionally controlled requirements/acceptance evidence;
- Manufacturing / Construction / Installation — configuration, buildability, changes and conformity evidence;
- Operations / FM / Service — operating modes, maintenance, training, support, monitoring and actual-use feedback.

Minimum outgoing handoff payload:

`requirement/function/interface ID → controlled variable/state/service → value/range/unit/condition where applicable → source/authority → configuration/revision → native source → evidence/readback → recipient → requested R-F maturity → OPEN/claim limit → change/reopen trigger`.

`SYSTEMS ENGINEERING COORDINATES ≠ SYSTEMS ENGINEERING OWNS EVERY DOMAIN DECISION`.

## 16｜Native source and actual readback

The authoritative carrier depends on the claim. Examples include:

- requirement/traceability database, table or governed structured file;
- system context / architecture / behavior model;
- interface-control data or drawings;
- configuration manifest / bill of materials / software/configuration identifiers;
- subsystem native drawings/models/calculations supplied by their real owner;
- simulation model with declared assumptions;
- prototype/test configuration and procedure;
- raw/derived test evidence;
- operational logs/trends/observations where in-use claims are made.

No single SysML diagram, dashboard, slide deck or system report can replace all of these. Presentation views are derivatives unless the profession/project explicitly establishes them as the native source for the bounded object.

Required chain:

`INTENDED NEED / REQUIREMENT / ARCHITECTURE → IMPLEMENTED IN CURRENT NATIVE CARRIERS → OBSERVED IN CONFIGURATION-BOUND READBACK → PROFESSIONAL INTERPRETATION → BOUNDED VERDICT`.

## 17｜Assurance and independence

Systems assurance must preserve separate owner truths:

- requirement/source review ≠ design review;
- subsystem technical PASS ≠ system integration PASS;
- interface acceptance ≠ system verification PASS;
- verification PASS ≠ validation PASS;
- validation PASS ≠ release/statutory/project Promotion;
- test execution quality ≠ independent professional judgment.

Independent review should attack, proportional to consequence:

- hidden stakeholder/requirement gaps;
- ambiguous or compound requirements;
- requirements whose acceptance criteria moved after evidence;
- wrong configuration evidence;
- interface/coupling gaps hidden behind component PASS;
- untested degraded/failure/recovery behavior;
- architecture options eliminated without fixed criteria;
- a verification result incorrectly promoted to validation;
- validation context not representative of the claimed need;
- changes that preserved stale verification/validation evidence.

## 18｜Mandatory REVISE / HOLD conditions

At minimum, `REVISE` or `HOLD` the affected systems claim when:

- system boundary materially omits a dependency that crosses the claim;
- a controlling requirement has no source/rationale/acceptance condition;
- mutually independent obligations are bundled into one PASS;
- requirement, interface or evidence references the wrong configuration;
- a subsystem/component PASS is used as whole-system evidence with material interfaces untested;
- an interface record omits unit/state/timing/ownership information material to behavior;
- a logical/physical architecture has no trade/selection basis where alternatives could materially change the outcome;
- an integrated configuration differs materially from the tested/verified configuration without equivalence/impact evidence;
- validation is inferred from verification;
- acceptance criteria are rewritten after a failed formal verification without change control;
- failure/anomaly evidence is overwritten by the repaired state;
- a material change leaves affected requirements/interfaces/tests marked PASS without impact analysis;
- one project success/failure is promoted directly to reusable Knowledge or Runtime change;
- Systems Engineering claims another profession's statutory/technical approval or R-F interface maturity as its own.

## 19｜Change propagation

For every material change:

`CHANGE SOURCE / REQUIREMENT / CONFIGURATION / INTERFACE / ENVIRONMENT / PROCEDURE`
`→ affected needs/requirements`
`→ affected functions/allocations`
`→ affected interfaces/coupled blocks`
`→ affected subsystem owner decisions`
`→ affected verification/validation evidence`
`→ stale scope`
`→ bounded rework / reverify / revalidate`
`→ updated readback / receipt`.

Only affected consumers become stale unless the dependency graph demonstrates a wider consequence. Historical evidence remains truthful for its original configuration/context; it simply stops supporting a changed Current claim.

## 20｜Completion and Promotion boundary

A Systems Engineering process instance may close only when:

- applicable stages have resolved their bounded exit questions;
- Current requirement/function/interface/configuration carriers exist;
- required R-F interfaces meet the maturity needed by the claim;
- required verification/validation evidence and actual readback exist;
- material anomalies and change/retest obligations are closed or explicitly outside claim;
- exact professional review/independence requirements are satisfied;
- a professional receipt records the bounded Systems Engineering verdict and `does_not_prove` ceiling.

A process PASS may satisfy only the triggered Systems Engineering dependency at its declared ceiling.

`SYSTEMS ENGINEERING PASS ≠ DESIGN KEEP`  
`SYSTEMS ENGINEERING PASS ≠ INTEGRATION PASS FOR UNCHECKED INTERFACES`  
`SYSTEMS ENGINEERING PASS ≠ PROJECT PROMOTION`  
`SYSTEMS ENGINEERING PASS ≠ STATUTORY / LICENSED APPROVAL`  
`SYSTEMS ENGINEERING PASS ≠ CURRENT KNOWLEDGE`

## 21｜Candidate adoption boundary

This file is a **candidate professional-domain process** produced under the existing OLEANDER Professional Domain Process Contract. Its existence and successful schema validation may demonstrate `FORMALIZED + MACHINE-BOUND CANDIDATE` evidence, but it does not change the Current architecture map by itself.

Until the applicable Evolution / independent review / human adoption / Current readback chain closes:

`Systems Engineering = CONTRACT_ENVELOPE_AVAILABLE / DOMAIN PROCESS OPEN in Current`.

No project-exercised claim is made by this file.
