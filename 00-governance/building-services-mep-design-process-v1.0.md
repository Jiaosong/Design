# OLEANDER Building Services / MEP Design Process v1.0

**Status:** CURRENT PROFESSIONAL DOMAIN PROCESS
**Domain:** Building Services / MEP Engineering
**Authority position:** subordinate to `complex-project-master-runtime-v1.0.md`, `professional-domain-process-contract-v1.0.md`, Current Knowledge Authority and applicable jurisdiction / responsible building-services engineering authority.
**External professional basis:** BSRIA BG 6/2018 *Design framework for building services* as a current responsibility/deliverable framework aligned to building-project stages; CIBSE Commissioning Code M (2022) for commissioning management from preparation/briefing through in-use; CIBSE TM54 (2022) for design-stage operational-energy evaluation and design-to-measured-performance boundaries.
**Existing OLEANDER knowledge mount owner:** `IDX-ARCH-MEP-004｜机电系统｜需求—设备—控制—调试—运维` plus the Current `MEP & Energy` domain and applicable L5/L6 sources/evidence.

---

## 1｜Why this process exists

Building services design is not the act of placing ducts, pipes, cable trays and plant into leftover architectural space.

A credible MEP claim must connect human / process demand to load basis, system boundary, topology, equipment, distribution, controls, power/water/drainage dependencies, spatial access, acoustic/vibration/fire/waterproofing interfaces, commissioning, handover and measured operation.

Existing OLEANDER MEP routing already defines the evidence chain as:

```text
USE / DEMAND
→ LOAD / CAPACITY BASIS
→ SYSTEM BOUNDARY
→ TOPOLOGY
→ EQUIPMENT
→ DISTRIBUTION
→ CONTROLS
→ ARCHITECTURAL / STRUCTURAL INTERFACES
→ COMMISSIONING
→ ACCEPTANCE
→ O&M / G9
```

This professional process turns that routing logic into a domain execution process while preserving system-specific engineering authority.

Hard non-substitution rules:

```text
PLANT FITS ≠ PLANT IS INSTALLABLE / MAINTAINABLE / REPLACEABLE
EQUIPMENT DATASHEET ≠ SYSTEM PERFORMANCE
LOAD CALCULATION ≠ MEASURED PERFORMANCE
SCHEMATIC COMPLETE ≠ DISTRIBUTION COORDINATED
CLASH-FREE ≠ COMMISSIONED
CONTROLS POINTS LIST ≠ CONTROL SEQUENCE VERIFIED
DESIGN ENERGY MODEL ≠ IN-USE ENERGY PERFORMANCE
TECHNICAL DESIGN ≠ INSTALLATION / SPECIALIST PRODUCTION INFORMATION
MEP PROCESS PASS ≠ FIRE / ELECTRICAL / STATUTORY APPROVAL
MEP PROCESS PASS ≠ DESIGN KEEP
COMMISSIONING PASS OF ONE SYSTEM ≠ WHOLE-BUILDING INTEGRATED SYSTEMS PASS
```

---

## 2｜Professional-source alignment and authentic MEP stage semantics

BSRIA BG 6/2018 is a current framework for allocating building-services design activities and deliverables. It uses building-project stage alignment and explicitly treats design responsibility, models, drawings and non-graphical deliverables as allocatable scope rather than assuming one party owns every task.

CIBSE Commissioning Code M treats commissioning as a managed lifecycle activity:

```text
PREPARATION / BRIEFING
→ DESIGN-STAGE COMMISSIONING PLANNING
→ ON-SITE COMMISSIONING / TESTING
→ TRAINING / HANDOVER
→ IN-USE REVIEW / FINE TUNING / SEASONAL TESTING
```

Therefore OLEANDER does **not** create a late single “commissioning stage”. Commissioning requirements thread through the domain process from the brief onward.

The Current MEP domain stages are intentionally named by professional decision rather than by Architecture stage number:

```text
BSP-STRATEGIC
BSP-BRIEF
BSP-CONCEPT
BSP-SPATIAL
BSP-TECHNICAL
BSP-PRODUCTION
BSP-CONSTRUCTION-CX
BSP-HANDOVER
BSP-INUSE
```

`BSP-*` is an OLEANDER internal carrier namespace for **Building Services Process**, not a claim that BSRIA/CIBSE publishes these exact identifiers. Each stage records its external alignment and authentic professional responsibilities.

Do not infer:

```text
BSP-SPATIAL = Architecture ADD-07
BSP-TECHNICAL = Architecture ADD-10
```

Cross-professional synchronization is by interface maturity and controlled variables, never matching stage names or numbers.

---

## 3｜Trigger

Trigger this process when a project makes material claims about one or more of:

- heating / cooling / ventilation / air-quality systems;
- plumbing / domestic hot water / drainage / rainwater systems;
- electrical supply / distribution / emergency power / earthing / lightning protection;
- lighting power / controls where Building Services owns the electrical/system scope;
- fire/life-safety MEP systems or their building interfaces;
- vertical transportation where assigned to the Building Services scope;
- BMS / controls / metering / sensors / system integration;
- plant rooms, risers, service zones or equipment access/replacement;
- energy strategy / operational energy / system efficiency;
- environmental conditions dependent on active building systems;
- public-health / sanitary engineering systems;
- system redundancy / resilience / standby arrangements;
- specialist services materially affecting architecture or operations;
- testing, commissioning, integrated systems testing or in-use fine tuning;
- MEP alteration / retention / replacement in existing buildings.

A generic plant placeholder or non-authoritative visualization does not trigger a completed MEP engineering claim.

---

## 4｜Knowledge Integrity / Operational Mount

Consequential MEP decisions consume task/claim-scoped mounts under `knowledge-integrity-and-operational-mount-v1.0.md`.

Mount applicable current objects for:

- current MEP routing methods;
- jurisdictional services / energy / fire / electrical / public-health requirements;
- client operational requirements;
- occupancy / use / process assumptions;
- climatic / environmental data;
- utility / infrastructure availability;
- manufacturer equipment data;
- controls / communication requirements;
- acoustic / vibration criteria;
- commissioning methods / acceptance criteria;
- operational-energy methods / benchmarks;
- existing-system surveys and measured data;
- specialist product or proprietary-system evidence.

The stage stores `knowledge_mount_refs[]` rather than copying KI/OE verdicts.

Manufacturer data proves the stated manufacturer/equipment conditions only. It does not make a system topology, network, installation, control sequence or measured building performance valid.

---

## 4.5｜Building Services / MEP Professional Stage Body / Title Contract

Every material `BSP-*` stage instance must remain recoverable as a professional building-services engineering body before it is compressed into a board, deck, coordination view, schedule extract or other presentation. The existing stage-specific sections below remain the professional authority; this cross-stage contract normalizes what the body must make findable without replacing BSRIA/CIBSE-aligned responsibilities, individual system-track semantics or commissioning continuity.

The stage-body title must identify the real system/stage decision, not merely the document type. Use a form such as:

`<project> | <BSP stage id + stage name> | <system / performance decision / cycle / baseline>`.

Titles such as `Analysis`, `Concept`, `Design Development`, `Planning`, `Review` or `Final` are incomplete by themselves because they do not identify the bounded services decision being made.

For each material stage, the body must expose these semantic responsibilities under building-services-appropriate headings:

| Shared semantic responsibility | Building Services / MEP body meaning |
|---|---|
| Professional Question / Scope | the servicing, performance, system, track, package, commissioning or in-use question and responsibility boundary being addressed |
| Current Condition / Problem | current demand, use/occupancy, environmental condition, utility, existing-system, load, capacity, operation, control, installation or performance problem/uncertainty |
| Authority / Knowledge / Evidence Inputs | current Basis of Building Services Design inputs, task/claim-scoped knowledge mounts, standards, climate/utility data, manufacturer evidence, surveys, measurements, assumptions and evidence authority state |
| Professional Criteria / Intent | required internal/external conditions, load/capacity basis, IAQ/thermal/water/power performance, resilience, maintainability, acoustic/vibration, energy, controls, commissioning and acceptance criteria as applicable |
| Development / Analysis / Comparison / Mechanism | actual load/demand development, system option/topology, plant/distribution sizing, hydraulic/electrical/air-side reasoning, controls sequence, commissioning method, measured-performance comparison or other stage-appropriate engineering mechanism |
| Cross-domain Interfaces | material Architecture, Structure, Fire, Envelope, Interior, Civil, utilities, specialist, contractor, FM/operations and commissioning dependencies and their current maturity/responsibility boundary |
| Native Output / Source of Truth | authoritative calculations, schematics, models, schedules, specifications, controls logic, commissioning/test records, trend/meter data or other required native source for the claim |
| Actual Readback / Finding | what the current native design, coordination, test, commissioning or measured operational evidence actually shows, distinguished from producer intent and interpreted as a bounded MEP finding |
| Failure / OPEN / does_not_prove | unresolved loads/conditions, coordination defects, missing access, failed tests, control/commissioning issues, unmeasured outcomes, excluded scope and explicit limits on what current evidence does not prove |
| Verdict / Claim Ceiling / Reopen / Next Action | bounded MEP disposition, current claim ceiling, reopen triggers and the next engineering, coordination, testing, commissioning or in-use action |

The visible body may combine responsibilities where the system/stage naturally does so, but none may disappear silently when material to the claim. `NOT_APPLICABLE` requires a reason; omission is not evidence of non-applicability.

Knowledge remains mounted by reference. The MEP body may state how a mounted standard, manufacturer source, measured dataset or method affects the present load, topology, control, commissioning criterion or decision, but it must not copy reusable canonical Knowledge bodies or re-award KI/OE state.

The body must distinguish the evidence chain:

```text
INTENDED SERVICES / PERFORMANCE POSITION
→ IMPLEMENTED IN NATIVE ENGINEERING / CONTROL / COMMISSIONING SOURCE
→ OBSERVED / TESTED / COMMISSIONED / MEASURED READBACK
→ INTERPRETED MEP FINDING
→ BOUNDED PROFESSIONAL VERDICT
```

Hard boundaries:

```text
PROFESSIONAL BODY STRUCTURE ≠ CANONICAL KNOWLEDGE BODY
PROFESSIONAL PROSE ≠ NATIVE MEP SOURCE
NATIVE MEP SOURCE EXISTS ≠ MEP PROFESSIONAL PASS
DESIGN CALCULATION ≠ MEASURED OPERATIONAL PERFORMANCE
COMMISSIONING RECORD EXISTS ≠ WHOLE-SYSTEM / WHOLE-BUILDING PASS
MACHINE BODY-COMPLETENESS PASS ≠ ENGINEERING JUDGMENT
MEP PROCESS PASS ≠ DESIGN KEEP
```

Machine validation may detect missing title/semantic coverage, missing native/readback references and contradictory `PASS + MISSING` states. It may not infer system adequacy, commissioned performance, statutory/certification acceptance, measured building performance or Design KEEP.

---

## 5｜Parallel MEP responsibility tracks

The process contains multiple professional tracks that may have different responsible engineers / specialists and different evidence closure.

### 5.1 HVAC / Environmental Systems

Core chain:

`SPACE / PROCESS CONDITION → LOAD → VENTILATION / IAQ DUTY → SYSTEM OPTION → PLANT → DISTRIBUTION → AIR/WATER BALANCE → CONTROL → COMMISSIONING → TREND / IN-USE`.

### 5.2 Plumbing / Public Health / Drainage

Core chain:

`DEMAND / WATER QUALITY / FIXTURES → SUPPLY / STORAGE / HEATING → DISTRIBUTION → DRAINAGE / VENT / PUMPING → ACCESS / HYGIENE → PRESSURE / FLOW / LEAK TEST → OPERATION`.

### 5.3 Electrical Power

Core chain:

`CONNECTED / DIVERSIFIED LOAD → SUPPLY / RESILIENCE → DISTRIBUTION → PROTECTION → CIRCUITS / EARTHING → EMERGENCY / LIFE-SAFETY INTERFACE → TESTING → OPERATION`.

### 5.4 Fire / Life-Safety MEP

Includes triggered fire water, smoke control, alarm, interfaces, emergency power and other systems according to jurisdiction and Fire/Life-Safety ownership. Building Services work does not replace the Fire strategy / statutory authority.

### 5.5 Vertical Transportation

Where in scope:

`TRAFFIC / USE → EQUIPMENT DUTY → SHAFT / PIT / HEADROOM / MACHINE REQUIREMENTS → POWER / CONTROL / RESCUE → COMMISSIONING / MAINTENANCE`.

### 5.6 Controls / BMS / Metering / Energy

Controls must be expressed as behavior, not “connect to BMS”.

```text
SENSOR
→ SETPOINT / LOGIC
→ ACTUATOR
→ FEEDBACK
→ ALARM
→ MANUAL OVERRIDE
→ FAIL STATE
→ TREND / METER / REVIEW
```

### 5.7 Specialist Services

Laboratory gases, commercial kitchen services, pool systems, medical systems, data-centre systems, industrial utilities and other specialist systems trigger their own applicable sources, responsible specialists and acceptance boundaries.

One track's PASS does not imply another track's PASS.

### 5.8｜Track-level engineering decision floor

Each triggered MEP track must convert its core chain into an explicit engineering decision record before a promotion-relevant `PASS`. A one-line schematic, equipment schedule or discipline label is not enough. At the current claim ceiling record, as applicable:

- **HVAC / Environmental Systems** — internal/external design conditions; occupancy/operation basis; sensible/latent/load and diversity basis; outdoor-air / IAQ / pressure relationships; zoning; plant/distribution/terminal duty; part-load and failure behavior; condensation, acoustic/vibration and access consequences; controls, measurement and commissioning points;
- **Plumbing / Public Health / Drainage** — demand/diversity and source condition; pressure/temperature/water-quality basis; storage/recovery/isolation; distribution-loss/recirculation implications where relevant; drainage/vent/pumping/invert constraints; hygiene/backflow/leak/access boundaries; waterproofing/Structure/Architecture interfaces; test/commissioning method;
- **Electrical Power** — connected/diversified demand; source/capacity/resilience; distribution topology; protection/coordination/earthing basis; voltage-quality/drop and fault assumptions as applicable; emergency/life-safety dependencies; containment/heat/access; metering; test/commissioning state;
- **Fire / Life-Safety MEP** — assigned system duty, cause/effect and dependency inputs trace to the Current Fire owner/authority; Building Services resolves its system/interface package but does not self-award Fire approval;
- **Vertical Transportation** — traffic/use duty; accessibility/rescue/fire interface; shaft/pit/headroom and structural loads; power/control/heat/replacement/maintenance implications; acceptance and commissioning evidence;
- **Controls / BMS / Metering** — every consequential mode defines trigger/input, logic/setpoint, command, proof/feedback, alarm, manual override, fail/fallback state, trend/meter evidence and acceptance test;
- **Specialist Services** — process duty, utilities/media quality, containment/segregation, hazard/failure mode, specialist equipment envelope, maintenance/replacement path, control/monitoring and acceptance boundary appropriate to the specialist system.

For every track, show at least one governing **peak / worst-case** and one relevant **part-load / degraded / failure state** when those states could change sizing, safety, comfort, resilience or commissioning. A system that works only at a nominal design point is not demonstrated as an operational system.

Where a quantitative criterion is material, preserve `criterion / value or range / unit / source / applicability / tolerance or acceptance method`. This process does not invent universal MEP values; they come from the Current brief, applicable engineering sources, manufacturer evidence, utility conditions and responsible professional decision.

Track-level closure should answer:

`demand / condition → calculation or sizing basis → topology → spatial/installation consequence → control/failure behavior → test/commissioning method → actual readback → bounded verdict`.

One track cannot borrow another track's closure. A coordinated model cannot substitute for missing engineering logic inside a triggered track.

---

## 6｜Cross-cutting MEP control objects

### 6.1 Basis of Building Services Design

Maintain a current Basis of Design / services design basis containing, as applicable:

- use / occupancy / process schedules;
- internal and external design conditions;
- load / demand methodology and key assumptions;
- utility / source availability;
- system boundaries and interfaces;
- system objectives and performance criteria;
- ventilation / IAQ / thermal / humidity / water-quality / power-quality requirements;
- resilience / redundancy requirements;
- fire/life-safety dependencies;
- space / plant / route / access / replacement requirements;
- acoustic / vibration limits;
- energy / carbon / metering / operational targets;
- control philosophy;
- commissioning requirements / success criteria;
- maintainability / access / spares / replacement assumptions;
- applicable source / standard versions;
- existing-system authority state where relevant;
- claim ceiling / open assumptions.

### 6.2 MEP Responsibility / Deliverables Matrix

Allocate responsibility for:

- load calculations;
- system concept / schematics;
- equipment selection;
- detailed routing;
- specialist design;
- builder's work;
- supports / seismic restraints where applicable;
- controls sequences / points / graphics;
- fire-system interfaces;
- installation / fabrication information;
- commissioning plan / specification / methodologies;
- testing / witnessing;
- TAB / balancing;
- Integrated Systems Tests;
- O&M / asset information;
- training;
- seasonal commissioning / fine tuning;
- post-occupancy energy / performance review.

A model author is not automatically the engineering decision owner.

### 6.3 Commissioning Plan

Commissioning is a live object beginning at brief/design.

At minimum track:

- commissioning requirements and success criteria;
- scope / systems / interfaces;
- responsible commissioning team / manager;
- design-stage Commissioning Plan;
- Commissioning Specification;
- cost / programme implications;
- commissionability review;
- commissioning clauses / contractor competence requirements;
- factory acceptance / sample inspection requirements;
- pre-functional checks;
- functional performance tests;
- balancing / regulation;
- Integrated Systems Tests (ISTs) where systems interact;
- continuous / sustained operational performance tests when applicable;
- operator / user training;
- handover documentation;
- in-use fine tuning / seasonal testing / post-project review.

### 6.4 Controls / Sequence Register

Every material control sequence identifies:

- controlled variable;
- sensors and location;
- setpoints / reset strategy;
- enable / disable logic;
- normal modes;
- degraded / fallback modes;
- safety interlocks;
- alarms;
- manual override;
- actuator response;
- feedback / proof;
- trending / metering;
- acceptance test.

#### Controls sequence engineering depth

A points list is not a controls design. For each consequential sequence, preserve the executable relation:

`operating state / trigger → prerequisites → priority / arbitration → sensed input → validity / plausibility → setpoint / reset logic → command → actuator / equipment response → proof / feedback → alarm / fallback → manual override → recovery / reset`.

Review as applicable:

- competing commands and priority when fire, emergency, frost, occupancy, demand-limit, local override, schedule and operator actions overlap;
- sensor location, range, accuracy/calibration or plausibility needs where the control decision depends on the measurement;
- deadband, delay, hysteresis, minimum-on/off time, ramp/rate limit or sequencing needed to avoid hunting, short cycling or unstable handoff;
- lead/lag and duty/standby rotation with clear failure detection and switchover behavior;
- safe/fallback state for communication loss, sensor failure, actuator failure, power restart or unavailable subsystem;
- proof-of-operation logic that distinguishes command sent from physical response achieved;
- reset / recovery after alarm, emergency override, network restart or maintenance isolation;
- manual override visibility, authority, persistence/timeout and return-to-auto behavior;
- trend points / sampling / retention sufficient to diagnose the sequence being claimed;
- commissioning script coverage for normal, transition, degraded, override and recovery states actually relied upon by design.

#### Sensor / actuator fault-diagnosis depth

When a control loop is relied upon for performance or protection, define how the system distinguishes a bad process condition from bad measurement, failed command path or failed final element. Preserve, as applicable: sensor plausibility/range/rate-of-change and cross-check source; command versus position/proof feedback; actuator travel/stiction/saturation/deadband; disagreement between redundant/related sensors; frozen/stale value behavior; local/manual override state; communication/power loss; alarm persistence; diagnostic reset/recovery condition; and the trend points needed to separate these hypotheses.

Do not treat “sensor fault” or “actuator fault” as a single fallback label when different failure modes drive different safe states. Commissioning should inject or simulate the bounded failure where competent/safe, confirm the expected diagnostic signature, fallback and recovery, and retain unresolved ambiguity as OPEN. Calibration and specialist safety limits remain with their responsible owners.

When Lighting, HCD, Fire, Security or other domains consume the user-visible consequence of a sequence, MEP/controls retains technical execution authority while R-F owns actual interface maturity/disposition.

`POINT EXISTS ≠ CONTROL FUNCTION EXISTS`.

`COMMAND ISSUED ≠ EQUIPMENT RESPONSE PROVED`.

### 6.5 Design-to-Operational Performance Register

When operational energy / performance is claimed, preserve:

- design model / methodology;
- occupancy and operating-hour assumptions;
- systems / controls representation;
- regulated and unregulated energy uses as applicable;
- sensitivity / scenario cases;
- targets / benchmarks;
- uncertainty / exclusions;
- measured-performance comparison plan;
- post-occupancy / G9 readback.

A design estimate remains a modelled estimate until measured evidence exists.

#### Performance observability and diagnostic evidence depth

When measured performance, fault diagnosis or tuning is in claim, design the observability chain before relying on BMS / meter data:

`performance question → physical variable → sensor / meter boundary and location → sampling / event / timebase → aggregation or derived value → quality / calibration / validity state → retained trend / event → comparison or diagnostic use`.

Distinguish command / setpoint, equipment proof, local sensor value, supervisory trend and independently measured process outcome; they are not interchangeable evidence.

For each decision-critical derived KPI or energy / performance comparison, preserve numerator / denominator, meter boundary, excluded loads / flows, timestamp / time-zone and synchronization basis, missing-data treatment, resets / rollovers / substitution, and whether the available points can discriminate the rival causes being investigated. A dense point list can still be unobservable if several failure mechanisms produce the same recorded signature.

Metering / controls owners retain device and data-platform technical truth; Measurement / Calibration owners retain measurement competence where triggered. Building Services defines the system variables and diagnostic evidence it needs; this process installs no universal accuracy, sampling or retention threshold.

---

## 7｜BSP-STRATEGIC — Strategic Services / Performance Definition

### Professional alignment

Pre-brief / strategic services input consistent with building-project Strategic Definition and the need to resolve services feasibility before system commitment.

### Professional question

> What servicing, utility, resilience, environmental and operational-performance consequences materially affect the strategic project decision?

### Required inputs

- client / business case;
- high-level use and operating model;
- site / utilities context;
- climate / environmental context;
- reuse vs new-build / extension options;
- high-level sustainability / energy goals.

### Building-services work

- identify major utility / infrastructure constraints;
- identify existing-system reuse / replacement questions;
- test strategic passive-active relationship with Architecture / Envelope;
- identify large plant / energy-source / resilience implications;
- identify special-use / hazardous / high-load services triggers;
- expose likely commissioning / operational-performance ambitions;
- identify surveys / metering / existing-system tests needed for briefing.

### Shared DD

`DD-01 Intent`, `DD-02 Concept`, `DD-06 Sensory` when environmental performance is material, `DD-12 Integration`.

### Native outputs

- services strategic constraints/opportunities note;
- utilities / infrastructure diagram;
- initial energy / resilience strategy options;
- survey / investigation / metering requirements;
- initial services interfaces register.

### Exit / claim ceiling

Close at strategic feasibility ceiling only.

**Does not prove:** system sizing, equipment selection, energy compliance, operational energy outcome, utility approval, installed capacity or commissionability.

---

## 8｜BSP-BRIEF — Preparation, Brief and Performance Basis

### External alignment

BSRIA BG 6 preparation / brief responsibilities; CIBSE Code M preparation-and-briefing commissioning requirements.

### Professional question

> Is there a complete enough use / performance / commissioning brief to begin system concept design without inventing hidden loads or operating assumptions?

### Required inputs

- user / process / occupancy requirements;
- architectural room / operational-state brief;
- utility information;
- climate / site data;
- current existing-system evidence;
- project sustainability / cost / procurement strategy;
- fire / accessibility / resilience requirements.

### Work

- define design conditions and performance requirements;
- establish occupancy / operating schedules;
- establish load / capacity calculation basis;
- define utility / source boundaries;
- define resilience / redundancy expectations;
- define environmental quality targets;
- define operational-energy / metering requirements;
- define maintainability / replacement / access requirements;
- establish commissioning success criteria, scope and budget basis;
- establish current Basis of Building Services Design;
- establish MEP Responsibility / Deliverables Matrix;
- establish post-occupancy / performance review targets where applicable.

### Existing-system reuse / capacity evidence depth

Where an existing service/system is proposed for retention, extension or reuse, establish an **as-found engineering baseline** before treating nameplate data, old drawings or previous schedules as available capacity.

Bind as applicable:

- observed configuration/revision and equipment identity/condition;
- actual operating schedule/load and known peak/degraded conditions;
- current control/setpoint state and isolation topology;
- distribution sizes/routes and accessible valve/damper/protection settings where material;
- utility/source condition and known constraints;
- recent maintenance, alarm, fault and repair history;
- trend / meter / spot measurement / functional-test evidence used to answer the reuse question;
- instrument / data quality and inaccessible / unsampled scope.

Separate **installed / nameplate capacity** from demonstrably available capacity under the Current design condition. Degradation, fouling, leakage, imbalance, failed controls, restricted heat rejection, changed source conditions or deteriorated equipment may reduce usable duty long before nameplate capacity is reached.

Reuse remains conditional or `HOLD` where evidence needed to establish duty, safety, hygiene, resilience or remaining serviceability is unavailable. Existing-system observation does not self-award equipment certification, electrical/fire approval or concealed-condition truth.

### Native outputs

- Basis of Building Services Design v1;
- MEP Responsibility / Deliverables Matrix;
- performance criteria / design conditions schedule;
- services survey / investigation register;
- initial load / demand basis;
- commissioning requirements / success criteria;
- initial Commissioning Plan skeleton;
- operational energy / metering brief where triggered.

### Exit / claim ceiling

Close when the services brief has sufficient bounded input to compare systems.

**Does not prove:** final load, technical design, equipment performance, coordinated routing, code compliance or commissioned operation.

---

## 9｜BSP-CONCEPT — System Concept / Options / Topology

### External alignment

BSRIA BG 6 Concept responsibilities plus early commissioning planning. BG 6 includes strategic commissioning planning at concept stage; OLEANDER therefore requires commissioning consequences during system-option selection.

### Professional question

> Which services system concept can meet the performance brief, and what spatial, energy, control, commissioning and lifecycle consequences distinguish the options?

### Work

- calculate / estimate concept-level demand and loads at appropriate fidelity;
- compare energy source / plant / distribution / terminal / public-health / electrical / controls options;
- define system boundaries and topology;
- establish zoning and major distribution strategy;
- identify major plant rooms, risers, shafts, intake/exhaust and external service routes;
- identify equipment mass / vibration / structural support consequences;
- define preliminary controls philosophy;
- define metering strategy at concept level;
- establish concept energy / operational-performance model where material;
- define phased handover / system configuration implications for commissioning;
- prepare strategic / design-stage Commissioning Plan;
- test maintenance / replacement / isolation implications;
- compare resilience and failure-state behavior.

When resilience depends on standby generation, UPS/storage, multiple utilities, duty/standby plant or staged restoration, define the **service-restoration dependency chain**, not only surviving capacity. Record initiating loss, detection/transfer condition, source availability, essential auxiliaries, controls/network power, permissives/interlocks, restart order, load pickup/staging, minimum-off/recovery constraints, proof of restored duty, failed-start branch, manual intervention and return-to-normal sequence. Identify services that must recover before others can start and loads intentionally shed/deferred.

Test whether a nominally redundant system has hidden common dependencies such as one controls network, fuel/water source, cooling/ventilation service, battery/starting system, transfer path, shared sensor or operator action. Electrical/Fire/Safety owners retain statutory/protection/emergency authority; MEP records the service sequence and requests the necessary R-F maturity. A standby capacity schedule alone does not prove recoverable service.

### Option comparison record

Each retained option states:

`demand/load basis → system concept → spatial consequence → energy/performance consequence → control consequence → resilience consequence → commissioning consequence → maintenance consequence → cost/carbon consequence → keep/reject reason`.

### Demand, load and diversity decision depth

Concept selection must expose the **basis behind the demand number**. For every selection-critical load/demand, record as applicable:

- contributing spaces/processes/equipment and whether values are measured, scheduled, manufacturer-derived, code/standard-derived, benchmarked, inferred or assumed;
- occupancy / operating hours / usage profile / simultaneity basis;
- diversity or coincidence assumption and the physical/operational reason it applies;
- sensible/latent, heating/cooling, domestic/process, connected/demand, normal/emergency or other relevant decomposition rather than one opaque total;
- weather / source / utility / groundwater / supply-state basis where external conditions govern;
- future allowance, standby/redundancy or resilience reserve and the scenario that justifies it;
- known uncertainty / range and whether a plausible value change can reverse the selected topology or plant strategy;
- current stage resolution: bounding estimate, concept calculation, technical design calculation or measured/in-use evidence.

Do not stack unrelated conservative assumptions without reading the combined consequence. Oversizing can create spatial, cost, control, cycling, part-load, acoustic, electrical and commissioning problems; undersizing can create capacity/failure risk. Compare at least one realistic operating scenario and the relevant peak / degraded or growth case where the system choice depends on them.

If diversity or schedule assumptions are copied from another project, they remain assumptions until applicability is established. A familiar factor is not a Current project fact.

`CONNECTED LOAD ≠ COINCIDENT DEMAND`.

`DESIGN PEAK ≠ NORMAL OPERATING POINT`.

### Native outputs

- services concept option set / selection record;
- concept load/demand schedule;
- system schematics / topology diagrams;
- plant / riser / zone strategy;
- concept controls philosophy;
- concept Commissioning Plan;
- operational-energy / performance option assessment where triggered;
- key Architecture / Structure / Envelope / Fire interface register.

### Required review

Attack:

- unsupported peak / diversity / schedule assumptions;
- system option chosen before system boundary is understood;
- “high efficiency equipment” used as a substitute for whole-system energy reasoning;
- plant strategy with no replacement path;
- commissioning impossible because isolation / access / measurement was not designed;
- systems relying on architectural / structural zones that do not exist.

### Exit / claim ceiling

Close when a system concept is selected at a bounded concept ceiling and controlling interfaces are explicit.

**Does not prove:** final equipment sizing, final network sizing, coordinated installation, controls verification, energy compliance, commissioning PASS or measured performance.

---

## 10｜BSP-SPATIAL — Spatial Coordination / Developed System Design

### External alignment

BSRIA BG 6 developed/spatial design responsibilities and building-project spatial coordination.

### Professional question

> Are plant, primary distribution, risers, service zones, terminals, builder's-work requirements and access/replacement routes spatially coordinated enough that other disciplines can rely on the current system geometry?

### Work

- refine loads and capacities as design information improves;
- develop system schematics and network topology;
- size major plant / main distribution / risers at current stage fidelity;
- coordinate plant-room layouts, access, lifting / replacement routes;
- coordinate risers / ceiling zones / shafts / trenches / underground services;
- coordinate structural openings, supports and major equipment loads;
- coordinate facade intakes / exhausts / louvers and roof plant;
- coordinate drainage gradients / invert constraints / condensate / waterproofing;
- coordinate acoustic / vibration separation;
- coordinate fire / smoke / emergency-power interfaces;
- refine control zones / sensing strategy;
- refine commissioning zones / isolation / test access;
- update operating-energy model and scenario assumptions where triggered;
- remove critical spatial conflicts according to actual interface requirements.

### Native outputs

- spatially coordinated services model / drawings;
- updated load / capacity schedule;
- coordinated plant-room / riser / zone layouts;
- builder's-work / penetration strategy;
- major support/load schedule to Structure;
- facade / roof services interface information;
- drainage / below-ground service coordination;
- control-zone diagram;
- current Commissioning Plan / commissionability review;
- operational-energy model/report update where triggered.

### Exit / claim ceiling

In-claim `MAJOR / CRITICAL` MEP interfaces must meet their required Integration maturity. “No detected clashes” is not enough if access, maintenance, firestopping, balancing, testing or replacement behavior is unresolved.

**Does not prove:** final detailed design, installation geometry, equipment substitution acceptability, commissioned performance or field installation.

---

## 11｜BSP-TECHNICAL — Technical Design / Detailed Engineering / Controls

### External alignment

BSRIA BG 6 Technical Design. BG 6 treats technical design as detailed building-services engineering and responsibility allocation, including coordination and specialist inputs; CIBSE commissioning management requires design-stage Commissioning Specification and commissionability planning before site execution.

### Professional question

> Is each in-scope services system technically designed, controlled, specified and coordinated at the declared responsibility boundary so installation/specialist production information can proceed?

### Work

- complete detailed load / flow / pressure / electrical / hydraulic / thermal / ventilation / protection calculations as applicable;
- finalize system topology / zoning / redundancy;
- finalize major equipment duties and selection criteria;
- finalize network sizing and routing design;
- develop electrical protection / distribution design as applicable;
- develop public-health hydraulic / drainage design;
- develop HVAC hydronic / airside design;
- develop fire/life-safety MEP interfaces within responsible scope;
- develop control sequences / points / alarms / fail states;
- develop metering / monitoring / trend requirements;
- define equipment / valve / damper / panel / access / service clearances;
- define insulation / condensation / waterproofing interfaces;
- define acoustic / vibration treatment requirements;
- define supports / loads / builder's work to Structure / Architecture;
- develop Commissioning Specification;
- develop Commissioning Cost Plan / programme requirements as applicable;
- update commissionability review;
- define FAT / inspection / test / TAB / FPT / IST requirements;
- update operational-energy model, scenario/sensitivity analysis and performance target against current design when triggered;
- review proposed specialist/manufacturer alternatives against performance and interface criteria.

### Stage 4 design-state profile

Where procurement requires staged equipment resolution, distinguish at least:

```text
FEASIBLE-GENERIC
COORDINATED-GENERIC
COORDINATED-SPECIFIC
```

These are **technical-design resolution states**, not separate universal OLEANDER stages. Responsibility and substitution boundaries must remain explicit.

### Technical calculation / network-model integrity

Detailed engineering calculations must expose the model boundary and governing failure mode. As applicable, preserve:

- system configuration / schematic revision and exact equipment / terminal / fixture set represented;
- load / demand / flow source and Current design conditions;
- pipe/duct/cable/network lengths, elevations, fittings, roughness/resistance or equivalent physical parameters where they control result;
- pump/fan/valve/damper/equipment curve or manufacturer data revision where selection depends on it;
- control position / diversity / simultaneous-use state represented by the calculation;
- boundary pressure/temperature/voltage/source conditions and utility assumptions;
- balance point / index run / critical path / worst case used for sizing;
- partial-load / minimum-load / minimum-flow / low-demand condition where system behavior can fail away from design peak;
- sensor/actuator authority and control range when the network requires active regulation;
- for staged / variable-capacity plant, map the operating envelope by active plant count, speed/capacity state, bypass or minimum-flow path, terminal demand, ambient/source condition and storage state where applicable; identify which controller owns each manipulated variable and where supervisory / local loops can fight;
- measurement / data uncertainty or tolerance when a narrow margin is being claimed;
- comparison between calculation, schematic, spatial model/drawing and specified equipment.

For staged or variable-capacity plant, do not stop at one design point and one minimum-load point. Check stage-up / stage-down trigger, persistence / hysteresis, minimum run/off constraints, lead-lag rotation, degraded unit availability, restart after outage and whether the remaining plant/network retains **controllable authority**, not merely nominal capacity. Where reset loops interact—such as plant reset versus terminal authority, pump-pressure reset versus valve authority, or supply-temperature reset versus latent/process constraints—make the priority and failure behavior explicit. A part-load energy result is not accepted when it depends on an unproven sequence or an operating region outside stable equipment/network control.

System-specific review should attack the relevant physics rather than applying one generic “calculation complete” gate. Examples include:

- air systems: pressure path, fan/system interaction, terminal/control authority, leakage, noise and low-flow behavior;
- where noise/vibration can control system acceptance, trace `source → transmission path → receiver` for each material operating state rather than attaching one equipment sound datum to the room. Preserve equipment speed/stage and duty point; airborne, duct/pipe-borne and structure-borne paths; breakout/regenerated noise where relevant; support/base/flexible-connection/isolation build-up; penetrations/bridges that can short-circuit isolation; terminal/valve/damper flow-noise state; and the receiving room/use/structure condition. Check startup, shutdown, low-load, standby/changeover and abnormal imbalance/misalignment states when they can be more disturbing than design peak. Coordinate acceptance with Acoustics/Structure/Architecture; MEP owns the service-system source/path data it controls, not specialist acoustic PASS;
- hydronic systems: pressure loss, pump/system curve, valve authority/balance, minimum flow, expansion/pressurization and part-load behavior;
- refrigerant / fuel-gas / consequential working-fluid systems where in scope: fluid identity and inventory basis; circuit / pressure-zone boundary; occupied / plant / enclosed-space relation; joints/components and relief/discharge route; isolation/recovery provision; leak detection/monitoring where required; ventilation or purge dependency; alarm/shutdown/interlock state; maintenance/recovery access; and post-leak inspection/restart condition. Model the credible design consequence of a leak or relief event without inventing universal concentration, charge or ventilation limits. Fire / Safety / Environmental / Refrigeration specialist owners retain hazard classification, statutory limits and approval; Building Services owns its equipment/network/interface consequences and requests required R-F maturity. Equipment capacity or leak-test PASS alone does not prove the occupied-space, relief-path or recovery claim;
- domestic/public-health water: demand basis, pressure/temperature, storage/turnover, dead-leg/stagnation, circulation and drainage/vent interfaces where in scope;
- where water distribution uses multiple pressure zones, boosters, break tanks, pressure-reducing/control valves or alternate sources, map the hydraulic/service boundary by zone: source condition; static/dynamic pressure basis; elevation; regulating/boosting device; cross-connection and backflow-protection boundary; isolation; lowest/highest or otherwise critical outlet; and service state during source/booster/regulator loss or maintenance. Check whether pressure-control or isolation arrangements can create unintended reverse flow, over/under-pressure, loss of downstream service, trapped section or cross-zone dependency when valves/pumps/sources change state. Backflow device selection/acceptance and water-safety criteria remain with the competent plumbing / water authority; Building Services preserves the topology, source state, test/access consequence and reopen condition. Hydraulic adequacy in one normal source state does not prove service continuity or backflow control across all claimed configurations;
- potable / process-water hygiene where in scope: source condition → storage/turnover → residence/stagnation risk → temperature/treatment regime → circulation/balancing/isolation → low-use/dead-leg state → flushing/commissioning/maintenance evidence; hydraulic capacity and hygienic operation are separate claims;
- gravity drainage: fixture/load basis, gradients/inverts, venting, backflow/flood/exceedance interfaces and access for cleaning, with civil/site outfall authority preserved;
- where drainage performance depends on air-pressure or transient behavior, preserve the hydraulic/air path rather than checking gradient alone: simultaneous-discharge scenario; branch/stack geometry and offsets; trap-seal protection dependency; vent/air-admittance route and failure state; positive/negative pressure or surcharge source; pumped-discharge start/stop interaction; downstream restriction/backwater condition; cleanout/relief path; and the receiving sewer/site-outfall boundary supplied by its owner. Where rapid valve/pump changes can create water-hammer or pressure transients in pressurized services, identify the initiating event, wave/pressure consequence, restraint/support/equipment sensitivity and mitigation/test basis under the proper hydraulic/specialist authority; no process-authored pressure or vent threshold is implied;
- electrical distribution: demand/diversity, voltage drop, fault/protection/selectivity or equivalent safety basis, power quality/harmonic/source implications and emergency/backup states according to responsible scope;
- controls/communications: data/state ownership, latency/failure/restart behavior, sensor validity and proof rather than command-only logic.

Where water-hygiene temperature, treatment, turnover or flushing criteria are authoritative, bind them to the Current specialist/source rather than process-authored values. Oversized storage/branches, seldom-used outlets, failed circulation or commissioning residue can defeat a hydraulically adequate system.

For condensation-sensitive services, preserve the air/dew-point condition, fluid/surface-temperature basis, insulation/vapour-control continuity, thermal bridges, penetrations/supports/valves, startup/shutdown/intermittent-use states and the consequence/drainage route if condensation occurs. `INSULATED ≠ CONDENSATION CONTROLLED`; reopen on humidity, source temperature, insulation build-up/continuity or operating-state change.

Where protection coordination / selectivity is within Building Services scope, bind the study to the **exact source topology and operating state**: normal source, alternate/emergency source, tie/open-bus state, generator/UPS contribution, transformer/feeder impedance basis and protective-device revision/settings. Check fault clearing and coordination across materially different source states; a setting that coordinates on a strong normal source may not behave equivalently on a weaker alternate source. Identify the protective function relied upon, the upstream/downstream pair, the region where coordination is claimed and any intentional loss of selectivity accepted by the proper Electrical/Safety owner. Device, trip-unit/firmware, cable, transformer, source or setting changes reopen the affected study.

A software calculation that returns a value is not enough. If a result is unexpectedly favorable or sensitive, attack units, defaults, omitted fittings/lengths, simultaneous states, curve selection, boundary conditions and equipment data before accepting it.

`CALCULATION PASSES ≠ NETWORK OPERATES ACROSS REQUIRED STATES`.

### Native outputs

- technical design calculations / models;
- technical schematics / single-line diagrams;
- coordinated technical model / drawings;
- plant / equipment / fixture schedules;
- control sequences / points / functional descriptions;
- metering / monitoring plan;
- specifications / performance specifications;
- builder's-work / penetration / support requirements;
- Commissioning Specification / updated Commissioning Plan;
- operational-energy evaluation report / implementation matrix when applicable;
- technical design review / checker records.

### Hard fail / revise

- major loads remain placeholder but equipment/system is claimed final;
- route / plant geometry conflicts with actual access / replacement / maintenance;
- controls exist only as points, with no sequence / fail behavior;
- fire/life-safety dependencies are contradictory;
- system design cannot be commissioned because measurement / isolation / access was omitted;
- manufacturer substitution changes capacity, spatial, electrical, acoustic, control or commissioning assumptions without reopen;
- current calculation and issued model/drawings materially disagree.

### Exit / claim ceiling

Technical design closes only within the responsible Building Services scope and current evidence.

**Does not prove:** installation/fabrication completeness, contractor workmanship, system commissioning, statutory approval, measured operational energy or field performance.

---

## 12｜BSP-PRODUCTION — Specialist / Installation / Production Integration

### Professional question

> Are technical-design requirements translated into coordinated installation / production information without losing engineering intent, access, controls, testing or system-performance requirements?

### Work

- integrate specialist / contractor / manufacturer design;
- review substitutions against system duty and interface assumptions;
- develop/review installation models / drawings;
- coordinate supports, hangers, seismic restraints where applicable, equipment bases and structural fixings;
- coordinate detailed builder's work / sleeves / penetrations / openings;
- coordinate containment / cable / pipe / duct routing and local offsets;
- coordinate valves / dampers / strainers / test points / sensors / access panels;
- preserve maintenance / replacement routes;
- coordinate firestopping / waterproofing / insulation / condensate interfaces;
- coordinate panels / controls / network integration;
- update Commissioning Plan / methodologies and test scripts as design evolves;
- maintain technical-design change / approval register.

### Installation-readiness and pre-functional quality depth

Before production information is treated as ready for installation / commissioning, read the detailed system as an **installable and inspectable assembly**.

Check as applicable:

- valve / damper / strainer / test-point / sensor orientation and maintenance access;
- pipe / duct / cable support and restraint responsibility;
- required fall / invert / air-release / drainage / condensate behavior;
- insulation / vapour / condensation continuity;
- firestopping / waterproofing / penetration build-up;
- equipment base, alignment, flexible connection and vibration interfaces;
- cable / containment termination and access;
- identification and isolation boundaries;
- for maintainable systems, show the isolation boundary needed to inspect, clean, replace or test the item without creating an uncontrolled adjacent-service condition: relevant valves/dampers/disconnects/breakers or other isolation points; upstream/downstream and cross-connection/backfeed paths; stored pressure/thermal/electrical/mechanical energy; drain/vent/bleed or depressurization route; proof-of-isolation point; essential-service consequence; temporary bypass/alternate-service need; and reinstatement/rebalancing/recommissioning step. Where lockout/tagout or permit-to-work is required, Building Services coordinates physical isolability and information needed by the competent safety/operations owner; it does not author universal LOTO procedure or workplace-safety approval. `ACCESSIBLE ISOLATOR ≠ SAFE ISOLATION PROVED`. Reopen when topology, shared service, backfeed path, isolation device or maintenance method changes;
- flushing / cleaning / pressure / leakage / electrical-test prerequisites;
- access for balancing, commissioning, inspection and future replacement;
- which conditions become concealed before required inspection or test.

Replacement readiness must identify the physical removal path, isolation / drain-down / safe-deenergization dependency, lifting/handling assumption, removable panels/doors/coils/modules, adjacent-service conflicts, temporary loss-of-service consequence and whether replacement requires rebalancing, recommissioning, readdressing or restoration of control/setpoint state. `MAINTENANCE CLEARANCE SHOWN ≠ EQUIPMENT REPLACEABLE` when the component cannot actually be extracted or returned to its accepted operating configuration.

Bind each critical item to the Current schematic, calculation, equipment data, control requirement and test / commissioning need it serves. A production model that fits geometrically but prevents inspection, cleaning, balancing, isolation, sensing, maintenance or required pre-functional verification remains `REVISE`.

Where installation sequencing would close a ceiling, riser, shaft, trench or enclosure before a critical test / inspection, define the hold point and evidence required before concealment.

### Native outputs

- installation / production model and drawings;
- specialist design packages;
- coordinated builder's-work / support package;
- final equipment data / schedules within procurement state;
- updated controls / points / graphics requirements;
- commissioning methodologies / test schedules;
- technical-deviation / substitution register;
- review / approval status according to actual contractual authority.

### Exit / claim ceiling

Close only when required production information within the Building Services responsibility boundary is coordinated and technical deviations are reconciled.

**Does not prove:** installation conformity, commissioning result, complete contractor means/methods or as-built condition.

---

## 13｜BSP-CONSTRUCTION-CX — Construction, Testing and Commissioning

### External alignment

Construction/delivery plus CIBSE Code M on-site commissioning management.

### Professional question

> Is the installed system sufficiently evidenced, tested and integrated to demonstrate the specified functions at the current commissioning / acceptance ceiling?

### Construction support

- respond to site queries / RFIs;
- review material/equipment substitutions where appointed;
- review quality / inspection records;
- assess nonconformities and design impact;
- update affected design calculations / drawings / controls when field change is accepted;
- treat each accepted field deviation as a configuration change: bind original design object/revision, observed site constraint, proposed change, affected duty/pressure/flow/voltage/control/fire/acoustic/condensation/access variables, impacted calculations/schematics/models/interfaces, required owner dispositions and exact retest/recommissioning scope;
- preserve system cleanliness / protection / access prerequisites for commissioning;
- verify current as-installed configuration basis for testing.

A local reroute or equipment substitution that preserves geometric fit but changes network resistance, protection behavior, sensor location, drainage fall, access, acoustic/vibration condition, condensation risk or controls response must reopen those dependent claims. If work proceeds under a bounded temporary state before full closure, that temporary configuration and operating restriction must be explicit rather than hidden in an RFI narrative.

### Commissioning execution

According to triggered systems and CIBSE/other applicable methods:

- construction-stage Commissioning Plan;
- commissioning methodologies;
- commissioning workshops / coordination;
- Factory Acceptance Testing where required;
- sample / installation inspections;
- pre-functional checks;
- pressure / leakage / electrical / continuity / safety / flushing / cleaning tests as applicable;
- balancing / regulation;
- functional performance tests;
- controls / sequence verification;
- alarms / fail / fallback / override tests;
- Integrated Systems Tests where multiple systems must act as one;
- sustained / continuous operational performance tests when specified;
- issue / defect / retest tracking;
- training readiness and documentation readiness checks.

### Evidence rule

```text
DESIGN CALCULATION
≠ PRE-FUNCTIONAL CHECK
≠ FUNCTIONAL PERFORMANCE TEST
≠ INTEGRATED SYSTEMS TEST
≠ SEASONAL / IN-USE PERFORMANCE
```

Each closes a different claim.

### Commissioning acceptance evidence threshold

Every test / commissioning result used to close a professional claim must bind, as applicable:

- system / equipment / zone identity;
- exact as-installed configuration and controls-sequence revision;
- test preconditions and operating mode;
- test method / script;
- instrument / sensor source and calibration or verification state where material;
- commanded condition / setpoint / simulated input;
- expected response, acceptance criterion and tolerance from the Current owner source;
- measured / observed result with units and time/context;
- witness / responsible party;
- deviation or failure;
- corrective action;
- retest ref / result;
- remaining OPEN limitation;
- claim ceiling / `does_not_prove`.

For controls, functional performance and Integrated Systems Test claims, test the material **normal, transition, degraded/fail-safe, alarm/override and recovery** behaviors that the design actually relies on. A single steady-state point, trend screenshot or “command received” observation is insufficient when sequence behavior is in claim.

Deferred / seasonal tests remain `OPEN` and cap the accepted state rather than being inferred from design intent or a previous design-stage calculation. A retest closes only the failed scope actually retested; it does not erase unrelated open deficiencies or make untested operating states pass automatically.

`TEST COMPLETED ≠ ACCEPTANCE CRITERION MET`.

`ONE MODE PASS ≠ SEQUENCE / IST PASS`.

### Design-to-TAB / measured-network reconciliation

Where balancing / regulation closes an air, water or analogous distribution claim, compare measured terminal / branch / system results with the Current design duty and network model at the **same operating/configuration state**.

Record as applicable:

- pump / fan speed or operating point;
- valve / damper / regulator positions;
- control mode and active overrides;
- relevant temperatures / pressures / electrical state;
- measured flow / pressure / air quantity / terminal result and instrument uncertainty;
- design target / tolerance source;
- index / critical path and residual imbalance;
- system effect of throttling / balancing changes.

A terminal can meet a local target while the network remains unstable, over-throttled, short of control authority or dependent on excessive plant duty. Review the distribution pattern and critical path rather than accepting isolated passing points.

If field balancing requires materially different settings, duty or topology from design, reopen the network calculation / control model and affected interfaces instead of treating the balance report as a silent design change.

`LOCAL TAB PASS ≠ NETWORK DESIGN RECONCILED`.

### Native outputs

- current as-installed system basis;
- test / commissioning records;
- TAB / balancing records;
- functional test scripts/results;
- controls / alarm / fail-state test evidence;
- IST records where required;
- deficiency / retest ledger;
- site change / re-design records;
- commissioning status matrix.

### Exit / claim ceiling

Stage may close only for systems whose required commissioning evidence and critical integrated interfaces meet the declared acceptance criteria. Open deferred / seasonal tests remain explicit and cap the claim.

**Does not prove:** every operational season, future performance, absence of hidden installation defects, statutory acceptance not separately evidenced, or operational-energy target achievement.

---

## 14｜BSP-HANDOVER — Handover, Training and Initial Aftercare

### Professional question

> Can operators / maintainers take over the systems with reliable as-built information, controls knowledge, outstanding commissioning state and maintainability responsibilities visible?

### Work

- close / transfer outstanding commissioning items;
- deliver as-built / record system information according to responsibility;
- deliver O&M / asset / equipment information;
- deliver control sequences / setpoints / alarm / override information;
- deliver commissioning / testing records;
- train operators and relevant users;
- transfer maintenance / replacement requirements;
- transfer seasonal/deferred commissioning plan;
- verify metering / trend availability needed for aftercare;
- record known limitations and open defects;
- support initial aftercare / stabilization as appointed.

### Native outputs

- building-services handover package;
- as-built / record drawings / model refs;
- equipment / asset schedules;
- O&M refs;
- commissioning completion / open-item matrix;
- controls / BMS operating description;
- operator training record;
- deferred / seasonal testing plan;
- initial aftercare issue log.

### Exit / claim ceiling

Handover closes only when the appointed information and training have been transferred and remaining commissioning / defect items are visible.

**Does not prove:** operators will achieve intended performance, seasonal performance, future maintenance quality or measured energy target.

---

## 15｜BSP-INUSE — In-use Fine Tuning / Seasonal Commissioning / Performance Evaluation

### External alignment

CIBSE Commissioning Code M in-use stage and CIBSE TM54 design-to-measured operational-energy comparison logic where operational energy is in scope.

### Professional question

> What does real operation show about system performance, controls, energy, comfort, reliability and maintainability, and which design assumptions must be tuned, reopened or returned to G9?

### Work

- review commissioning outcome after occupation;
- fine tune systems and controls;
- undertake seasonal testing where required;
- analyze BMS / meter / trend data;
- compare operational schedules / occupancy to design assumptions;
- compare measured energy / loads / temperatures / flows / pressures / IAQ / alarms to design expectations where monitored;
- investigate comfort / noise / reliability / maintenance complaints;
- review controls overrides / disabled alarms / persistent faults;
- evaluate equipment cycling / part-load operation;
- assess capacity / redundancy / resilience under actual use;
- revalidate system assumptions for change of use / occupancy / equipment;
- record lessons for future projects only after bounded Knowledge validation.

### TM54 operational-energy boundary

When TM54-type operational energy evaluation is used during design, preserve:

- modelling approach;
- assumptions / simplifications;
- occupancy / operation;
- all relevant energy uses;
- system / controls representation;
- sensitivity analysis;
- scenario testing;
- targets / benchmarks;
- QA and report / implementation matrix.

In-use comparison then distinguishes:

```text
DESIGN ESTIMATE
→ TARGET / BUDGET
→ MEASURED DATA
→ NORMALIZATION / CONTEXT
→ DIFFERENCE
→ CAUSE / UNCERTAINTY
→ TUNING / REPAIR / DESIGN LESSON
```

### In-use performance-gap diagnosis

Do not jump from measured difference to a design cause. Diagnose the gap across plausible classes:

- changed occupancy / hours / process / plug or specialist loads;
- weather / utility / source condition different from design assumption;
- installed equipment or configuration differing from design basis;
- controls setpoint, schedule, override, sensor, sequence or tuning behavior;
- balancing / commissioning / valve-damper-setting or distribution issue;
- envelope / architecture / room-use change affecting the MEP load or control response;
- maintenance condition such as dirty filters/coils, fouling, failed sensors, leaks, degraded insulation or disabled plant;
- metering boundary, missing end use, timestamp, calibration, aggregation or data-quality problem;
- model simplification / wrong diversity / part-load or standby assumption;
- actual system defect or under/over-capacity.

Use targeted discriminating evidence before changing the model or system: trend correlations, temporary measurement, functional test, recalculation, inspection, occupancy/schedule evidence or controlled setpoint/sequence change as appropriate. Preserve pre-change evidence and compare after tuning/repair.

Normalization must state what was normalized and why. Adjusting measured data or the design baseline until the curves align is not diagnosis.

When tuning changes a setpoint, schedule, reset, sequence, balance or equipment state, bind the change to the exact configuration and check downstream comfort, energy, resilience, noise, IAQ, safety and user-control consequences before declaring improvement.

`PERFORMANCE GAP ≠ DESIGN ERROR BY DEFAULT`.

`TREND CORRELATION ≠ CAUSE`.

### Native outputs

- seasonal / fine-tuning records;
- operational trend / metering analysis;
- design-vs-measured performance record;
- controls optimization / change record;
- persistent fault / maintenance issue register;
- post-project review;
- G9 candidate lessons with applicability boundaries.

### Exit / claim ceiling

In-use assessment closes by defined observation period / question, not permanently for the life of the building.

**Does not prove:** future performance, universal energy target achievement, unmeasured conditions or causal claims without supporting evidence.

## 15.5｜MEP stage acceptance thresholds and handoff content

The MEP stages above may use different calculations, schematics, models, schedules and tests, but the decision threshold follows one professional rule: a downstream consumer must be able to tell **what condition the system is designed for, how the system is expected to behave, where that behavior is implemented, how it will be verified, and what change invalidates the result**.

Before a promotion-relevant MEP stage supports `PASS`, verify where applicable:

1. **Demand and design-condition traceability** — occupancy, schedules, climate, process duty, diversity, utility/source conditions and existing-system facts match the Current project state; a stale demand basis cannot support a current equipment or capacity claim.
2. **Capacity and network basis** — plant/equipment/network duties are connected to the governing load/flow/pressure/electrical/thermal calculation and appropriate peak/part-load/degraded states; spare/redundancy assumptions are explicit rather than hidden inside oversizing.
3. **System boundary and topology** — what belongs to the system, where it starts/ends, how branches/zones/isolation operate and which adjacent systems it depends on are explicit enough for another discipline and commissioning team to consume.
4. **Spatial installability and maintainability** — plant, risers, routes, valves/dampers/panels, access zones, lifting/replacement routes, drainage falls, test points and maintenance clearances exist in the current geometry; geometric fit alone is insufficient when service access is impossible.
5. **Control and failure behavior** — normal, start-up/shutdown, standby, emergency/degraded, alarm, manual override and fail/fallback behavior are resolved for performance-critical systems; a point list without sequence/feedback/proof does not close controls.
6. **Cross-system safety/interface behavior** — Fire, Structure, Envelope, Accessibility, Acoustics, Architecture, utilities and specialist dependencies use Current controlled variables and do not contain unresolved in-claim contradictions.
7. **Material / installation consequence** — pipe/duct/cable/containment material, insulation, corrosion/water-quality/condensation/firestopping/waterproofing/seismic-support or equivalent installation consequences are resolved at the claim ceiling where they can affect performance or life safety.
8. **Commissionability** — required isolation, instrumentation, measurement points, balancing devices, access, test modes, trend points and acceptance criteria are designed before the stage claims readiness for commissioning.
9. **Energy / operational-performance boundary** — design estimates retain their model assumptions/sensitivities; measured performance claims use actual data, observation period/context and normalization where needed. Modelled and measured evidence remain distinct.
10. **Readback consistency** — calculations, schematics, model/drawings, equipment schedules, controls logic and commissioning requirements describe the same Current system state at the variables material to the claim.

Use `REVISE` when the system route remains viable but design, coordination, control, access, commissionability or evidence is materially inadequate. Use `HOLD` when required load/source/utility/fire/authority/manufacturer/field evidence or responsible specialist input is unavailable. Use `REJECT` when the current system option should not proceed because it cannot credibly satisfy the performance, spatial, resilience, operational, lifecycle or commissioning criteria within the declared constraints.

### MEP handoff payload

For each material issue to another domain or downstream package, provide as applicable:

`system/controlled-variable ID → design condition + duty/value/range + unit → source/calculation/schematic revision → geometry/location → load/opening/support/access/replacement requirement → control/fail-state dependency → commissioning/acceptance condition → recipient/owner → R-F interface ref + requested maturity → OPEN boundary → reopen trigger`.

Examples include plant loads/openings/supports to Structure; room/environmental conditions, risers, plant/ceiling/service zones and replacement routes to Architecture; intake/exhaust/penetration/condensation assumptions to Envelope; cause/effect/emergency-power/system status to Fire; access/control/fixture/lift interfaces to Accessibility; and trends/setpoints/alarm/maintenance/spares requirements to FM/Operations.

The recipient may reject an issue that lacks a governing condition, uses stale calculation/model information, omits units or access/replacement constraints, or falls below the maturity required for the receiving claim. Handoff acceptance does not certify MEP performance; it confirms only that the bounded input can be consumed.

`EQUIPMENT SELECTED ≠ SYSTEM ACCEPTED`.

`NO CLASH ≠ INSTALLABLE / MAINTAINABLE / COMMISSIONABLE`.

`TEST SCRIPT EXISTS ≠ ACCEPTANCE CRITERIA SATISFIED`.

---

## 16｜Commissioning thread by stage

Commissioning obligations are not confined to `BSP-CONSTRUCTION-CX`.

| MEP stage | Commissioning responsibility |
|---|---|
| `BSP-STRATEGIC` | identify performance / handover / operational ambition |
| `BSP-BRIEF` | establish commissioning requirements, success criteria, scope and budget basis |
| `BSP-CONCEPT` | create strategic/design-stage Commissioning Plan; select concepts that remain commissionable |
| `BSP-SPATIAL` | preserve access, isolation, measurement, test zones, phased handover and system boundaries |
| `BSP-TECHNICAL` | Commissioning Specification, programme/cost requirements, commissionability review, test/IST requirements |
| `BSP-PRODUCTION` | installation-specific methodologies, test points, access, controls and package integration |
| `BSP-CONSTRUCTION-CX` | execute pre-functional / functional / integrated testing, issue/retest closure |
| `BSP-HANDOVER` | training, documentation, deferred/seasonal test plan, open-item transfer |
| `BSP-INUSE` | fine tuning, seasonal testing, post-project review and performance readback |

A stage that makes a commissionability-dependent decision cannot say “commissioning comes later” and ignore the design prerequisites.

---

## 17｜Cross-disciplinary interface contract

Building Services consumes and issues controlled variables through Cross-Disciplinary Integration.

| Interface | Typical shared variables / decisions | MEP minimum concern |
|---|---|---|
| Architecture | room use, occupancy, plant/riser/ceiling zones, access, entrances, wet rooms, roofs | performance demand + install/maintain/replace geometry |
| Structure | equipment loads, openings, penetrations, supports, bases, vibration, builder's work | load/opening/support information current before affected closure |
| Envelope | thermal/solar/air infiltration assumptions, louvers, intakes/exhausts, penetrations, condensation | model and physical interface use same current envelope basis |
| Fire/Life Safety | smoke control, fire water, alarm, emergency power, firestopping, cause/effect | Fire authority remains separate; MEP closes its assigned systems/interfaces only |
| Accessibility | controls/alarms/fixtures/lifts/maintenance access where human use is affected | accessible operation and maintenance dependencies explicit |
| Acoustics | plant noise, breakout, ductborne noise, vibration | source/path/receiver and attenuation assumptions coordinated |
| Lighting | power, controls, emergency, daylight response, ceiling coordination | electrical/control/system ownership explicit |
| Landscape/Civil | utilities, drainage, external plant, below-ground services, heat rejection | invert/route/access/drainage/site interface coordinated |
| Interior | reflected ceiling, access panels, terminals, fixtures, controls, equipment | service design does not destroy interior clearances / finish logic |
| Cost/Procurement | equipment/system alternatives, efficiency, redundancy, maintenance | substitution changes reopen performance/interface evidence |
| FM/Operations | maintainability, replacement, staffing, controls, spares, alarms, metering | operators receive real operating and maintenance basis |

Actual required interface maturity remains per-interface / Acceptance Contract. MEP stage labels do not own Integration maturity.

---

## 18｜Shared DD / experience / design-language binding

MEP design materially shapes human experience and design quality when it affects thermal comfort, air quality, sound, light, visual clutter, ceiling depth, equipment visibility, control behavior, maintenance intrusion or architectural space.

Typical shared DD bindings:

- `BSP-STRATEGIC/BRIEF` → `DD-01 Intent`, `DD-03 Experience`, `DD-05 Human Relation`, `DD-06 Sensory`, `DD-12 Integration`;
- `BSP-CONCEPT` → `DD-02 Concept`, `DD-03 Experience`, `DD-06 Sensory`, `DD-10 Adaptation`, `DD-12 Integration`;
- `BSP-SPATIAL` → `DD-03 Experience`, `DD-04 Form/Composition`, `DD-05 Human Relation`, `DD-06 Sensory`, `DD-08 Detail`, `DD-12 Integration`;
- `BSP-TECHNICAL/PRODUCTION` → `DD-06 Sensory`, `DD-07 Design Language` where services are visually/materially expressed, `DD-08 Detail/Craft`, `DD-10 Adaptation`, `DD-12 Integration`;
- `BSP-CONSTRUCTION-CX/HANDOVER/INUSE` → `DD-03 Experience`, `DD-05 Human Relation`, `DD-06 Sensory`, `DD-10 Adaptation`, `DD-12 Integration` where actual operation changes design intent.

A technically compliant terminal layout that produces poor spatial hierarchy, noise, glare, visible service clutter or unusable maintenance access can still require Design REVISE.

---

## 19｜Content / diagram / schedule projection requirements

Professional closure should use the right representation rather than one overloaded coordination model.

Applicable artifacts include:

- Basis of Building Services Design;
- load / demand / capacity schedule;
- system schematics and single-line diagrams;
- plant / riser / distribution zone diagrams;
- plans / sections at critical pinch points;
- plant-room / equipment access and replacement diagrams;
- builder's-work / penetration / support schedule;
- equipment / fixture / panel schedules;
- controls sequence / cause-effect / points diagrams;
- commissioning plan / specification / matrix;
- operational energy / scenario / sensitivity reports;
- test / balancing / functional / IST evidence;
- O&M / handover / training information;
- in-use trend and designed-vs-measured performance plots.

Hard co-location:

```text
performance claim ↔ design condition / assumption
capacity ↔ load / diversity basis
equipment selection ↔ duty + system boundary
route ↔ access / maintenance / replacement constraint
control sequence ↔ sensor / actuator / fail state / acceptance test
commissioning status ↔ exact test / system / open issue
energy estimate ↔ occupancy / operation / model assumptions
measured performance ↔ period / context / normalization
```

A colored MEP model with no system behavior or evidence status is not professional completion evidence.

---

## 20｜Building Services professional receipt

When triggered, emit a domain process receipt compatible with `professional-domain-process.v1.schema.json` and Master Runtime summary.

Minimum receipt content:

- process / stage / cycle / baseline identity;
- current Basis of Building Services Design ref;
- MEP Responsibility / Deliverables Matrix ref;
- consequential knowledge mount refs;
- design conditions / loads / capacity basis refs;
- system boundary / topology / key equipment status;
- active MEP tracks and responsible owners;
- control / metering design state;
- Commissioning Plan / Specification / status refs;
- operational-energy model / target status if triggered;
- native outputs and actual readback refs;
- active Architecture / Structure / Envelope / Fire / FM / Cost interface refs;
- technical / professional review refs;
- professional verdict;
- open / stale / reopened items;
- claim ceiling;
- `does_not_prove`.

The process verdict may be `PASS / REVISE / REJECT / HOLD`; `CLOSED ≠ PASS`.

---

## 21｜Mandatory REVISE / HOLD conditions

Do not close a promotion-relevant MEP claim when any applicable condition remains unresolved:

- occupancy / use / schedule / process demand is materially unknown but capacity is claimed final;
- utility / source conditions contradict current system design;
- critical load / capacity calculation is stale relative to current architecture/use/equipment;
- plant, riser or route fits geometrically but lacks installation / maintenance / replacement access;
- MEP equipment loads / openings / supports are not issued to Structure where material;
- fire/life-safety system ownership / cause-effect / emergency-power interface is unresolved;
- water / drain / condensate / waterproofing interface is unresolved;
- critical acoustic / vibration impact is unresolved;
- controls sequence / fail state / interlock is undefined for a performance-critical system;
- commissioning cannot be performed because isolation / measurement / test points / access were omitted;
- specialist / manufacturer substitution changes duty / geometry / power / controls / acoustic / maintenance basis without reopen;
- current installation / production model differs materially from engineering design without reconciliation;
- functional / integrated test evidence is missing for a claimed commissioned state;
- design energy estimate is presented as measured performance;
- a Building Services process receipt is being used to imply Fire, electrical, statutory, commissioning, field or operational-performance authority it does not have.

---

## 22｜External research basis / freshness

This v1.0 is grounded in:

- BSRIA BG 6/2018, *Design framework for building services*, publication year 2018, currently indexed as Current and noting use with RIBA Plan of Work 2020; used here for responsibility allocation, design activities, technical-design resolution, model/drawing/non-graphical deliverables and building-services lifecycle coordination;
- CIBSE Commissioning Code M, *Commissioning management* (2022), Active; used for commissioning requirements from preparation/briefing through design, on-site testing, training/handover and in-use review/fine tuning/seasonal testing;
- CIBSE TM54, *Evaluating operational energy use at the design stage* (2022), Active; used for operational-energy modelling, assumptions, scenario/sensitivity testing, performance targets, QA and measured-performance comparison boundaries. Current edition incorporates later corrigenda published by CIBSE;
- Current OLEANDER `IDX-ARCH-MEP-004` routing framework and project/jurisdiction-specific sources.

Revalidate this process when BSRIA publishes a materially superseding building-services design framework, CIBSE materially revises commissioning/operational-energy guidance, applicable jurisdiction changes engineering duties, or Current Knowledge Integrity identifies a contradiction.

This process is not a substitute for system-specific technical standards, responsible-engineer appointment, equipment certification, Fire strategy / statutory review, electrical safety approval, commissioning witness authority or field verification.

---

## 23｜Canonical Building Services invariant

```text
CURRENT MEP CLAIM
= current use / demand / operating assumptions
+ task/claim-mounted professional knowledge
+ explicit responsibility
+ current Basis of Building Services Design
+ current loads / capacities / topology
+ authentic system-track engineering
+ spatial + structural + envelope + fire interfaces
+ control behavior
+ commissioning designed from the start
+ native engineering outputs
+ actual readback / testing appropriate to the claim
+ professional verdict
+ explicit claim ceiling / does-not-prove
```

A system model that omits any applicable controlling relation may remain useful coordination evidence, but it must not be promoted as a stronger Building Services engineering claim.
