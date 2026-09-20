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

---

### 6.6 Equipment / System Submittal & Substitution Release Register

For consequential equipment/system selections record:
- system/tag;
- design duty and critical attributes;
- specified/reference basis;
- submitted identity/revision;
- manufacturer evidence;
- capacity/efficiency/acoustic/electrical/control/interface checks;
- access/replacement consequence;
- deviation/substitution impact;
- reviewer;
- release state;
- affected calculations/schedules/drawings/sequences.

`DATASHEET ACCEPTED ≠ SYSTEM PERFORMANCE VERIFIED`.

### 6.7 Builder's Work / Installation / Access Coordination Register

Track:
- opening/penetration/support/base;
- route/clearance;
- equipment access and replacement path;
- maintenance working space;
- structural/fire/acoustic/waterproofing interface;
- coordinated drawing/model ref;
- owner;
- site verification requirement;
- change state.

### 6.8 Inspection / Test / TAB / Commissioning Witness Matrix

For each system/acceptance criterion record:
- prerequisite;
- inspection/test/TAB/Cx step;
- method/procedure;
- configuration tested;
- witness/owner;
- acceptance criterion;
- result;
- defect/nonconformity;
- retest;
- closure evidence.

This matrix links the Commissioning Plan to executed evidence.

### 6.9 MEP RFI / Field Change / Defect Register

Track:
- exact system/tag/location;
- issued design relation;
- field/RFI condition;
- capacity/control/fire/access/commissioning consequence;
- responsible owner;
- revised source;
- retest/recommission requirement;
- closure state.

### 6.10 O&M / Asset / Training / Seasonal Closeout Register

Track:
- installed asset identity;
- O&M source;
- setpoints/sequences;
- warranties/spares;
- operator training;
- unresolved defects;
- seasonal/deferred tests;
- trend/monitoring requirement;
- replacement/access information;
- FM owner acceptance;
- reopen condition.

`O&M FILE RECEIVED ≠ OPERABLE SYSTEM HANDOVER`.

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

### Option comparison record

Each retained option states:

`demand/load basis → system concept → spatial consequence → energy/performance consequence → control consequence → resilience consequence → commissioning consequence → maintenance consequence → cost/carbon consequence → keep/reject reason`.

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
- preserve system cleanliness / protection / access prerequisites for commissioning;
- verify current as-installed configuration basis for testing.

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

### Machine professional receipt

Triggered Building Services / MEP process closure compiles `BUILDING_SERVICES_MEP_DESIGN_PROCESS_RECEIPT` through:

- `00-governance/schemas/building-services-mep-design-process-receipt.v1.schema.json`;
- `00-governance/schemas/building-services-mep-design-process-receipt.v1.template.json`;
- `00-governance/schemas/validate_project_closure_objects.py`.

The receipt is fail-closed: `PASS` requires non-stale triggered-stage closure, native outputs plus actual readback, closed required interfaces, current professional review, and every in-claim system track to close its required commissioning / integrated-test evidence. Explicit seasonal/deferred tests may remain only when marked outside the current claim and must continue to cap the claim.

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

---

## 2026-09-19｜Execution Binding Contract｜Building Services / MEP professional-depth parity

**Status effect:** additive execution-depth binding only. This does not change the Current MEP process, commissioning responsibility, statutory authority or existing SYS object ownership.

### Knowledge binding
- `KN-METHOD-MEP-DESIGN-TRACE-001` — demand/load → calculation → duty point → equipment → distribution → terminal/interface;
- `KN-METHOD-MEP-CALC-RELEASE-001` — calculation/version ↔ schedule ↔ selected product/substitution ↔ recalc/release;
- `KN-METHOD-MEP-COORDINATION-ACCESS-001` — route/size/slope/radius/insulation/support/access/replacement/penetration/installation sequence;
- `KN-METHOD-MEP-CONTROL-CX-001` — points/sensors/actuators → sequence → interlock/fail state → TAB/FPT → issue/retest → systems manual;
- current HVAC/electrical/plumbing/fire/BMS/energy/product/commissioning SOURCE and SYS owners as triggered.

### `required_native_outputs[]`
- current basis of design, operating/design-condition and responsibility/deliverables records;
- native load/flow/pressure/static/electrical/hydraulic/thermal/ventilation/protection calculations as applicable;
- system schematics/single-lines/riser/zone/network models and coordinated plans/sections;
- equipment/terminal/fixture schedules with current duty/operating points;
- calculation↔schedule↔drawing↔selected-product trace and substitution/recalc register;
- coordination/access/replacement/support/opening/penetration/firestop interface records;
- controls point/I-O/address/setpoint/alarm/sequence/interlock/C&E records;
- Commissioning Plan/Specification, pre-functional/TAB/FPT/IST/test scripts and issue/retest records;
- as-built settings/points/sequences, systems manual, training, trend/seasonal/in-use evidence where in scope.

### `execution_owner_requirements[]` / `required_capabilities[]`
- `oleander-research` — codes/standards/product/commissioning/source evidence;
- `oleander-design-process` — system-option/interface/change reasoning; not MEP engineering validation;
- `oleander-data-viz` — load/energy/trend/monitoring analytical visualization only when useful; not source values or measured-performance authority;
- `oleander-3d-pipeline` — spatial coordination/exchange where fit; does not prove sizing, commissioning or constructability;
- `oleander-technical-drawing` — candidate PR #172 only;
- `oleander-delivery-qc` — package/native-master/export integrity only.

**Specialist execution gap / routing rule:** the Current core Skill registry has no installed HVAC/Electrical/Plumbing/Fire/BMS engineering solver family. Consequential calculations and commissioning claims must bind project-authorized discipline calculation tools, manufacturer selection tools where appropriately source-bounded, field instruments/test procedures and responsible MEP professionals. Missing callable capability must remain explicit `CAPABILITY_HOLD`; a diagram or selected datasheet cannot substitute for engineering.

### `tool_adapter_requirements[]`
- discipline calculation/model runtime appropriate to the current HVAC/electrical/plumbing/fire/BMS claim;
- project CAD/BIM/coordination runtime with units/levels/zones/IDs and access-envelope readback;
- exact manufacturer selection/submittal data linked to current duty points;
- controls/BMS configuration/address/sequence carrier when controls are consequential;
- TAB/balancing/commissioning instrument/test records and configuration identity;
- trend/metering/in-use data carrier for operational claims;
- format-specific native reopen/readback and issue/revision comparison.

### `typed_handoff_contracts[]`
- Architecture/Interior/Operations → MEP: room/zone/process/occupancy/schedule/performance/access/plant-space requirements + revision;
- MEP → Architecture/Structure/Fire/Interior/Lighting: loads, openings, supports, plant/riser/ceiling zones, heat/noise/drainage, power/control, access/replacement and penetration criteria;
- Calculation → Procurement: exact duty/operating point + design condition + interface + approved deviation envelope;
- Submittal return → MEP: exact model/configuration/performance/electrical/control/dimensional delta + affected calculations/drawings/sequences;
- Controls → Commissioning: point/address/sequence/setpoint/fail-state + expected measurable result;
- Field/Cx return → MEP: test configuration + measured result + issue/root cause + repair/retest + as-built update.

### `actual_readback_requirements[]`
- source room/process data and design conditions ↔ current calculation inputs;
- critical demand/result/duty point ↔ equipment/terminal schedule and selected product;
- system schematic/network ↔ coordinated route/zone/plant/terminal geometry;
- slope/radius/insulation/support/access/replacement/penetration reality, not clash count only;
- point list ↔ physical sensor/actuator ↔ sequence/interlock/fail state;
- commissioning prerequisites/TAB/settings ↔ FPT/IST expected and measured results;
- substitution/site change ↔ recalculation/recoordination/retest propagation;
- as-built settings/trends/seasonal/in-use evidence where operational performance is claimed.

### `reopen_triggers[]`
Programme/occupancy/process/design-condition change; load/diversity/redundancy assumption change; utility/source change; network/routing/level change; equipment/terminal/control substitution; Architecture/Structure/fire interface change; manufacturer data revision; field coordination deviation; TAB/FPT/IST failure; sensor/point/sequence/setpoint change; energy/trend/in-use evidence materially contradicting the design basis.

### Professional boundary
`LOAD CALC PASS ≠ SYSTEM PASS`; `DATASHEET ACCEPTED ≠ DUTY PASS`; `CLASH-FREE ≠ COORDINATED`; `POINT LIST COMPLETE ≠ SEQUENCE VERIFIED`; `STARTUP ≠ COMMISSIONING`; `ONE-SYSTEM CX PASS ≠ WHOLE-BUILDING INTEGRATION PASS`; `DELIVERY QC PASS ≠ ENGINEERING APPROVAL`.

### Object-level invocation matrix

`PROJECT_SPECIALIST_REQUIRED` preserves the boundary between OLEANDER design reasoning/coordination and discipline engineering/commissioning authority.

#### A｜Demand–Calculation–Equipment–Distribution
- Knowledge: `KN-METHOD-MEP-DESIGN-TRACE-001` + current discipline code/system/product sources.
- Skills: research + design-process; discipline engineering solver/professional = `PROJECT_SPECIALIST_REQUIRED`; 3d-pipeline only for geometry/coordination.
- Tool class: HVAC/electrical/plumbing/fire/BMS calculation/model appropriate to the claim.
- Native carrier: load/demand schedule, calculation package, duty-point equipment schedule, schematics/network, terminal/interface records.
- Readback: source demand/design conditions → critical result/duty point → network critical point → equipment envelope → terminal/end use.
- Reopen: programme/load/diversity/source/network/equipment/terminal/design-condition change.

#### B｜Calculation–Schedule–Substitution Release
- Knowledge: `KN-METHOD-MEP-CALC-RELEASE-001`.
- Skills: discipline engineer + calculation runtime; research for exact manufacturer data; delivery-qc for package integrity.
- Tool class: calculation model + equipment/terminal schedule + manufacturer selection/submittal + drawing/control interface.
- Native carrier: calc register, input/source ledger, duty-point trace, selected-product/substitution delta, recalc trigger and affected-output register.
- Readback: schedule value ↔ current calc; exact product curve/envelope; substitution effects on pressure/static/head/power/noise/heat/control/space; Cx baseline.
- Reopen: room/load/network/design condition/manufacturer/product/control/interface substitution or field delta.

#### C｜Coordination–Clearance–Access
- Knowledge: `KN-METHOD-MEP-COORDINATION-ACCESS-001`.
- Skills: design-process + 3d-pipeline for spatial exchange; project CAD/BIM/coordination owner; discipline professional owns technical acceptability.
- Tool class: combined-services model/drawings with access/removal/support/opening/penetration data.
- Native carrier: coordination sections, route/zone allocation, access/replacement envelopes, opening/embed/support and firestop/acoustic registers.
- Readback: route size + insulation + slope/radius; actual valve/filter/damper/panel access; replacement path; structural support/opening; installation sequence; field delta.
- Reopen: system size/routing/ceiling/structure/firestop/access/equipment/support/site change.

#### D｜Controls–Points–Sequence–Commissioning
- Knowledge: `KN-METHOD-MEP-CONTROL-CX-001` + current control/Cx system sources.
- Skills: design-process for intent/change; controls/commissioning professional and actual BMS/test tools = `PROJECT_SPECIALIST_REQUIRED`; data-viz only for trend evidence.
- Tool class: point/I-O/address configuration, sequence/C&E, TAB/balancing records, FPT/IST scripts, field instruments and trend logs.
- Native carrier: point schedule, I/O map, sequence/interlock/fail-state, prefunctional/TAB baseline, FPT/fault-injection, issues/retest, as-built/system manual.
- Readback: each sequence statement ↔ actual point/device; fail/manual/network/power states; prerequisites; measurable expected result ↔ test result; retest and as-built update.
- Reopen: point/device/address/setpoint/sequence/interlock/system configuration, TAB prerequisite, FPT failure, site tuning or trend/in-use contradiction.
