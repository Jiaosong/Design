# OLEANDER Structural Engineering Design Process v1.0

**Status:** CURRENT PROFESSIONAL DOMAIN PROCESS
**Domain:** Structural Engineering
**Authority position:** subordinate to `complex-project-master-runtime-v1.0.md`, `professional-domain-process-contract-v1.0.md`, Current Knowledge Authority and applicable jurisdiction / responsible structural engineer authority.
**External professional basis:** Institution of Structural Engineers (IStructE), *The Structural Plan of Work 2020* and current structural checking guidance; stage names below preserve the source plan's authentic lifecycle semantics.
**Existing OLEANDER knowledge mount owner:** `IDX-ARCH-STRUCT-SAFETY-005｜结构与生命安全｜荷载—消防—人防—无障碍` plus the Current `Structure & Life Safety` domain and applicable L5/L6 sources/evidence.

---

## 1｜Why this process exists

Structural engineering cannot be reduced to a grid overlay, member library, clash-free model, structural-analysis screenshot or a late engineering check after architecture is already frozen.

A structural claim is developed through a chain of project conditions, ground/existing-condition evidence, loads, system selection, stability/load path, serviceability, material and durability strategy, spatial coordination, member and connection design, specialist/contractor design, temporary works, construction conformity, handover and performance in use.

Canonical professional chain:

```text
PROJECT / SITE CONDITIONS
→ STRUCTURAL RESPONSIBILITY + INFORMATION NEEDS
→ BASIS OF STRUCTURAL DESIGN
→ STRUCTURAL CONCEPT / OPTIONS
→ SPATIAL COORDINATION
→ TECHNICAL DESIGN
→ PRODUCTION / SPECIALIST INFORMATION
→ MANUFACTURING + CONSTRUCTION READBACK
→ HANDOVER / DEFECT CLOSE
→ USE / PERFORMANCE EVALUATION
```

Hard non-substitution rules:

```text
STRUCTURAL GRID PRESENT ≠ STRUCTURAL SYSTEM RESOLVED
ANALYSIS MODEL RUNS ≠ ANALYSIS MODEL VALID
MEMBER SIZE PRESENT ≠ CONNECTION / STABILITY RESOLVED
CLASH-FREE ≠ STRUCTURALLY COORDINATED
CALCULATION PASS ≠ CONSTRUCTION CONFORMITY
CONCEPT DESIGN ≠ TECHNICAL DESIGN
TECHNICAL DESIGN ≠ PRODUCTION INFORMATION
PERMANENT-WORK DESIGN ≠ TEMPORARY-WORK DESIGN
STRUCTURAL PROCESS PASS ≠ STATUTORY APPROVAL
STRUCTURAL PROCESS PASS ≠ FIELD VERIFIED
STRUCTURAL PROCESS PASS ≠ DESIGN KEEP
```

---

## 2｜Professional-source alignment and stage identity

IStructE's Structural Plan of Work 2020 is coordinated with the RIBA Plan of Work 2020 but defines structural-engineering roles and deliverables. It explicitly uses:

```text
0 Strategic Definition
1 Preparation and Brief
2 Concept Design
3 Spatial Coordination
4 Technical Design
4.5 Production Information
5 Manufacturing and Construction
6 Handover
7 Use
```

OLEANDER preserves those stage meanings through internal carrier IDs:

```text
SE-SPW0
SE-SPW1
SE-SPW2
SE-SPW3
SE-SPW4
SE-SPW4.5
SE-SPW5
SE-SPW6
SE-SPW7
```

These IDs are internal references to the source-aligned structural process. They do not assert a universal OLEANDER numbering system and they do not synchronize by number with Architecture `ADD-*`, MEP or any other profession.

The source plan groups 0–1 as Briefing, 2–4.5 as Design, 5–6 as Delivery and 7 as Evaluation. OLEANDER keeps the stages individually visible because responsibility, evidence, specialist design, production information and reopen rules differ materially between them.

---

## 3｜Trigger

Trigger this process when a project makes a material claim about one or more of:

- structural feasibility or structural system selection;
- load path, stability or robustness;
- spans, grids, structural zones, transfer structures or large openings;
- foundations / soil-structure interaction;
- member sizing or structural material choice;
- deflection, vibration or other structural serviceability;
- structural fire-resistance interface;
- structural durability / design life;
- seismic, wind, snow or other jurisdiction-specific structural actions;
- retained structure, alterations, strengthening, demolition or adaptive reuse;
- equipment / facade / MEP / landscape / temporary loads on structure;
- connections, supports, fixings or structural tolerances;
- specialist / contractor-designed structural items;
- temporary works materially affecting permanent works;
- manufacture / fabrication / construction conformity;
- structural handover or in-use structural performance.

Do not trigger the full process merely for decorative massing, non-authoritative visualization or geometry whose claim explicitly excludes structural feasibility.

---

## 4｜Knowledge Integrity / Operational Mount

Consequential structural decisions must consume task/claim-scoped knowledge mounts under `knowledge-integrity-and-operational-mount-v1.0.md`.

Mount applicable current objects for:

- structural system methods and precedents;
- geotechnical / survey / existing-condition evidence;
- applicable loads and combinations;
- material standards and product/source evidence;
- jurisdictional structural code / standard versions;
- fire strategy inputs that constrain structural fire resistance;
- durability / exposure / design-life requirements;
- structural optimization / lightweighting methods when used;
- specialist product / proprietary system evidence;
- construction / inspection / testing requirements.

The Current OLEANDER routing framework states the structural object chain as:

`SITE / GEOTECH → LOAD CASES → MATERIAL / SYSTEM → ANALYSIS MODEL → ASSUMPTIONS → GLOBAL RESPONSE → MEMBER / CONNECTION → ROBUSTNESS → CONSTRUCTION STAGE → INSPECTION / TEST → CHANGE TRIGGER`.

That routing framework is an input owner, not structural approval. A stage instance stores `knowledge_mount_refs[]`; it does not re-award KI/OE state.

`SIMULATION / HYPOTHESIS ≠ VERIFIED SITE / MATERIAL / CONNECTION CONDITION`.

---

## 5｜Cross-cutting structural control objects

Maintain these objects throughout the process when applicable:

### 5.1 Structural Responsibility Matrix

Identify who owns:

- permanent works design;
- foundations / geotechnical interface;
- primary frame;
- secondary structure;
- facade-support structure;
- equipment / MEP support structure;
- connections;
- proprietary / specialist systems;
- contractor-designed items;
- temporary works;
- alteration / strengthening design;
- fabrication information;
- construction inspection / conformity review;
- as-constructed information.

A missing or contradictory responsibility boundary is an interface `BLOCKED` condition, not an administrative footnote.

### 5.2 Basis of Structural Design

The current basis should record, as applicable:

- source / site / survey / geotechnical authority;
- intended use and occupancy assumptions;
- structural design standards / versions;
- loading basis and dynamic actions;
- design life / durability / exposure;
- fire-resistance input and authority;
- serviceability criteria including deflection / vibration;
- stability and robustness basis;
- movement / tolerance assumptions;
- climate-change or future-condition assumptions where material;
- material and structural-system basis;
- foundation strategy;
- embodied-carbon target / tracking basis where in scope;
- maintenance / adaptation / deconstruction assumptions;
- specialist design boundaries;
- temporary-works dependencies;
- claim ceiling and unresolved inputs.

A material change to this object reopens every consuming stage and interface.

### 5.3 Structural Design Assurance / Checking Plan

Checking is risk-proportionate and independent to the degree required by project risk, jurisdiction, appointment and current professional guidance.

Record:

- what must be checked;
- checking category / independence basis where applicable;
- checker identity / competence / independence state;
- design stage at which the check occurs;
- model / calculation / drawing / detail / specialist information checked;
- assumptions and limitations;
- unresolved findings;
- preservation / record requirements.

A producer self-check may be valuable evidence but does not become independent review merely by being documented.

### 5.4 Structural Change Register

Track material changes to:

- use / occupancy / load;
- geometry / grid / span / height;
- openings / penetrations / voids;
- member / material / connection;
- support / restraint / movement joint;
- foundation / ground assumptions;
- equipment or facade loads;
- fire strategy;
- MEP route / builder's work;
- construction sequence / temporary works;
- specialist system or supplier;
- retained / demolished / altered existing structure.

Change propagation follows existing Master / Integration impact classes, not a separate structural taxonomy.

---

### 5.5 Analysis / Calculation Baseline & Check Register

For each consequential structural analysis/calculation package record:
- model/calculation ID and revision;
- geometry/material/load/support assumptions;
- source inputs and Basis-of-Structural-Design refs;
- governing load cases/combinations;
- checker and independence state;
- check comments;
- disposition;
- affected drawings/details;
- stale/reopen state.

`MODEL RUN COMPLETED ≠ CHECKED DESIGN BASIS`.

### 5.6 Member / Connection / Foundation Release Schedule

Track release by structural object/package:
- object/system;
- design basis;
- governing action/response;
- member/foundation/connection state;
- calculation/check ref;
- detail/drawing ref;
- specialist dependency;
- issue purpose;
- release state;
- reopen trigger.

### 5.7 Fabrication / Shop Drawing / Specialist Submittal Release Register

For delegated/specialist/fabricated structural items record:
- design responsibility;
- submitted identity/revision;
- design criteria/interfaces;
- calculation/model refs;
- tolerances/connections/supports;
- material/product evidence;
- reviewer/checker;
- disposition;
- affected permanent works;
- release state.

A reviewed shop drawing does not transfer design responsibility silently.

### 5.8 Inspection / Test / Material / ITP Evidence Register

Track:
- inspection/test/hold point;
- specification/acceptance criterion;
- sample/batch/location;
- witness/owner;
- result;
- nonconformity;
- retest/repair;
- closure;
- exact as-constructed configuration.

`TEST PASS ≠ UNOBSERVED CONSTRUCTION CONFORMITY`.

### 5.9 Structural RFI / Field Change / Nonconformity Register

Bind each field issue to:
- exact location/member/connection;
- issued source;
- actual condition;
- structural consequence;
- temporary/permanent state;
- responsible designer;
- revised calculation/model/drawing;
- site disposition;
- reinspection/retest need;
- closure state.

### 5.10 Structural Closeout / Residual Risk / Monitoring Register

At handover, track:
- as-constructed information authority;
- unresolved defects/nonconformities;
- load/use restrictions;
- inspection/maintenance/monitoring need;
- future alteration constraints;
- proprietary/specialist records;
- owner/FM handoff;
- residual risk;
- reopen condition.

---

## 6｜SE-SPW0 — Strategic Definition

**Source-aligned stage:** IStructE / RIBA Stage 0 Strategic Definition.

### Professional question

> What structural consequences, opportunities and uncertainty materially affect the strategic project decision before a structural scheme is selected?

### Required inputs

- client / project need and high-level use;
- site / existing asset context;
- known hazard / ground / climate constraints;
- reuse / extension / demolition alternatives when relevant;
- initial project claim ceiling.

### Structural work

- support strategic definition of new-build vs reuse / extension / adaptation choices;
- identify material structural constraints and fatal-risk information gaps;
- identify early investigations / surveys needed for a credible brief;
- identify high-level structural sustainability / resource / embodied-carbon opportunities;
- expose major interface dependencies to Architecture, Geotechnical, Fire, MEP, Envelope, Civil/Landscape, Cost and FM.

### Shared DD responsibilities

Primarily `DD-01 Intent`, `DD-02 Concept` and `DD-12 Integration / Coherence` where material.

### Native / authoritative outputs

- structural strategic-constraints note / diagram;
- investigation / survey need list;
- initial responsibility / authority map;
- structural strategic risk / opportunity register.

### Required readback

Read the strategic decision against actual site / existing-condition evidence state. Do not infer structural feasibility from massing alone.

### Exit / claim ceiling

May close when structural strategic constraints are sufficiently identified to support the project strategic decision and all material unknowns are explicit.

**Does not prove:** structural feasibility in technical-design terms, member adequacy, foundation adequacy, statutory compliance, existing-structure capacity or field condition.

---

## 7｜SE-SPW1 — Preparation and Brief

**Source-aligned stage:** IStructE Stage 1 Preparation and Brief.

### Professional question

> Is there a sufficiently authoritative structural brief, site-information basis and responsibility boundary to begin concept structural design?

### Required inputs

- project brief / intended use;
- current site information;
- survey and geotechnical information state;
- existing-structure records where applicable;
- jurisdiction / code route;
- fire strategy status;
- information / BIM requirements where applicable.

### Structural work

- contribute to Project Brief;
- review site information and structural constraints;
- define survey / investigation scopes;
- identify structural design information requirements;
- establish / update Structural Responsibility Matrix;
- identify contractor / specialist design candidates;
- identify statutory / third-party structural interfaces;
- establish the first current Basis of Structural Design skeleton;
- establish Design Assurance / checking strategy proportional to project consequence and complexity.

### Native outputs

- structural brief contribution;
- site-information / survey register;
- structural constraints register;
- structural responsibility matrix;
- initial Basis of Structural Design;
- design assurance / checking plan;
- structural information requirements.

### Interfaces

Architecture, Geotechnical, Fire, MEP, Envelope, Civil/Landscape, Cost, Planning, FM/Operations and specialist parties as triggered.

### Exit / claim ceiling

Close only when critical information responsibilities and investigation gaps are explicit enough to support concept design.

**Does not prove:** ground parameters, existing capacity, concept selection, structural design compliance or construction adequacy.

---

## 8｜SE-SPW2 — Concept Design

**Source-aligned stage:** IStructE Stage 2 Concept Design.

### Professional question

> Which structural concept / system is credible enough to carry forward, and what load, stability, foundation, serviceability, durability and carbon basis governs it?

### Required inputs

- current project brief;
- mounted site / ground / existing-condition information;
- architectural concept / spatial constraints;
- fire strategy inputs;
- initial MEP / plant / facade / major equipment constraints;
- current cost / procurement / sustainability strategy.

### Structural work

- develop and compare structural options;
- define scope, scale and form of the structural concept;
- define structural design standards and criteria;
- establish static / dynamic loading basis at current evidence ceiling;
- establish durability / design-life basis;
- establish structural-fire-resistance input relative to current fire strategy;
- establish ground / thermal movement assumptions;
- establish serviceability criteria including deflection and vibration where relevant;
- establish structural grids / zones and initial transfer / cantilever / long-span strategy;
- develop foundation strategy;
- develop stability / lateral-load-resisting concept and primary load paths;
- identify robustness / disproportionate-collapse questions where applicable;
- consider use, maintenance, adaptation and deconstruction;
- evaluate embodied-carbon / resource-efficient options at current design resolution;
- identify specialist and temporary-work dependencies early enough to avoid false feasibility.

### Required comparison

Retained concepts must state:

`driver → structural move → load/stability consequence → spatial consequence → interface consequence → carbon/resource consequence → cost/constructability consequence → keep/reject reason`.

### Native outputs

- current Basis of Structural Design;
- structural concept option set / selection record;
- initial structural drawings / analytical model / information model;
- stability / load-path diagram;
- foundation strategy;
- structural zone / grid information;
- concept structural sustainability / embodied-carbon assessment;
- specialist / contractor-designed item list;
- concept-stage design assurance record.

### Readback / review

Independent or appropriately separated review should attack:

- whether load paths are real rather than diagrammatic;
- whether the proposed system is stable in all material directions / states;
- whether major architectural / MEP / facade openings and loads are acknowledged;
- whether serviceability and dynamic behavior are ignored;
- whether foundation concept depends on unverified ground facts;
- whether structural optimization is being mistaken for engineering validation.

### Exit / claim ceiling

A concept may close when a structurally credible option is selected at concept claim ceiling and all material assumptions / OPEN items are explicit.

**Does not prove:** final member sizing, detailed connection adequacy, final foundation design, fabrication readiness, construction conformity, statutory approval or field validity.

---

## 9｜SE-SPW3 — Spatial Coordination

**Source-aligned stage:** IStructE Stage 3 Spatial Coordination.

### Professional question

> Is the structural design sufficiently developed and spatially coordinated that architecture, services, envelope, specialist systems and construction strategy can rely on its current geometry and movement/tolerance behavior?

### Structural work

- develop detailed form and function of structural components to current stage resolution;
- prepare calculations sufficient to facilitate and verify current design solutions;
- spatially coordinate structural design with Architecture and other disciplines;
- confirm structural grids and zones;
- confirm main spans, depths, openings, transfers and major supports;
- develop soil-structure interaction / foundation design basis as evidence allows;
- establish movement joints, anticipated movements and tolerances;
- define critical coordination clearances;
- coordinate below-ground services / foundations / structure;
- develop performance specifications for contractor-designed items;
- develop constructability and critical temporary-works briefs;
- update carbon / resource tracking and structural sustainability response;
- update design assurance and check major assumptions / stability / load paths / critical details.

### Required interfaces

At minimum when triggered:

- Architecture: grids, zones, levels, member depths, openings, transfers, movement joints, stairs/cores;
- MEP: risers, builders' work, plant/equipment loads, penetrations, service zones, support strategy;
- Envelope: edge geometry, anchors/support zones, movements, facade loads;
- Fire: structural fire-resistance assumptions / protection zones;
- Geotechnical/Civil: foundations, retaining, underground services, drainage conflicts;
- Interior/FF&E: heavy partitions, specialist equipment, vibration-sensitive uses;
- Landscape: retaining, canopies, soil/planter/water loads where structural;
- Cost/Procurement: material quantities, specialist-design packages, sequence / buildability.

### Native outputs

- spatially coordinated structural drawings / model;
- updated analytical model and calculation package at stage claim ceiling;
- movement / tolerance report;
- outline structural specification;
- contractor-designed-item performance specification;
- updated Structural Responsibility Matrix;
- current structural sustainability / carbon record;
- design assurance / checking record.

### Exit / claim ceiling

Close only when in-claim `MAJOR / CRITICAL` structural interfaces meet required Integration maturity and the spatial structure can be consumed without hidden geometry contradictions.

**Does not prove:** final technical design, final connection design, fabrication information, temporary-works completion, construction conformity or field as-built condition.

---

## 10｜SE-SPW4 — Technical Design

**Source-aligned stage:** IStructE Stage 4 Technical Design.

### Professional question

> Is the permanent structural design technically complete at the declared responsibility boundary and coordinated with specialist / contractor-designed structural work sufficiently for manufacture and construction information to be prepared?

### Structural work

- complete structural technical design for permanent works within appointment scope;
- complete design calculations / models at required level;
- design members, slabs, walls, foundations, stability systems and material-specific details;
- develop connection requirements / design within assigned responsibility;
- coordinate specialist structural contractor designs;
- prepare full setting-out information;
- review contractor-designed items and their integration;
- resolve structural openings / cast-ins / embedded plates / support interfaces;
- close movement / tolerance / differential-movement design at current technical ceiling;
- confirm structural fire / durability / robustness / serviceability response within actual evidence;
- complete required technical design checks and third-party checks where triggered;
- confirm in-use / maintenance / adaptation / deconstruction strategy where in scope;
- complete/update Structural Sustainability Report / embodied-carbon accounting at technical resolution.

### Required native outputs

- technical structural drawings / model suitable for manufacture/construction progression;
- structural specification;
- calculation / analysis package;
- connection design / performance requirements according to responsibility matrix;
- builder's-work / opening / embed / support information;
- current specialist-design integration record;
- structural sustainability report;
- technical design assurance / checking receipt.

### Hard fail / revise

- unresolved primary stability;
- uncontrolled load path;
- member or foundation design relies on stale loads / geometry / ground assumptions;
- critical penetrations / openings not incorporated;
- connection responsibility is absent or contradictory;
- specialist structural design is referenced but not integrated;
- serviceability / vibration criteria materially contradict use;
- permanent structure depends on unreviewed temporary condition where this affects permanent design;
- calculation model and issued geometry materially diverge.

### Exit / claim ceiling

Technical design may close only inside the responsible engineer's actual scope and current evidence ceiling.

**Does not prove:** production/fabrication detail completeness, temporary works adequacy outside assigned scope, statutory acceptance, manufactured quality, construction conformity, inspection pass or as-built condition.

---

## 11｜SE-SPW4.5 — Production Information

**Source-aligned stage:** IStructE Stage 4.5 Production Information.

This stage is deliberately preserved because specialist subcontractor / fabricator information and construction-production information are not interchangeable with consultant technical design.

### Professional question

> Is the technical structural design translated into coordinated production / manufacture information with specialist and temporary-works responsibilities closed to the required construction interface?

### Structural work

- develop / review production information according to responsibility matrix;
- integrate specialist-subcontractor technical information;
- prepare or review reinforcement drawings / bar bending schedules, fabrication drawings and equivalent production information as applicable;
- develop/review temporary works designs where within scope and material to permanent works;
- review proposed construction methods / sequences for complex or critical structural items when they affect permanent design;
- close production tolerances / setting-out / embed / connection interfaces;
- verify that substitutions remain inside structural design assumptions;
- update design changes and affected checking records.

### Native outputs

- production / fabrication information according to appointed scope;
- specialist technical design integration record;
- temporary-works interface record;
- production-stage structural change register;
- review / check records;
- manufacture / construction release boundary statement.

### Exit / claim ceiling

Close only when the required production information within the structural responsibility boundary is coordinated and reviewed.

**Does not prove:** all contractor means/methods, fabrication quality, erected condition, temporary works not in scope, site installation tolerance or completed construction.

---

## 12｜SE-SPW5 — Manufacturing and Construction

**Source-aligned stage:** IStructE Stage 5 Manufacturing and Construction.

### Professional question

> Does the manufactured / constructed work and change history remain consistent with the accepted structural design basis, or must design / checking reopen?

### Structural work

- review temporary works as appointed / required;
- respond to site / fabrication queries;
- undertake site visits / inspections within actual appointment and evidence scope;
- review manufacture / construction quality records where applicable;
- address non-conformities and assess whether design reanalysis is required;
- assess substitutions / field changes / penetrations / damage / sequence changes;
- maintain design change record and reopen affected calculation / interface / assurance states;
- collect as-constructed information prepared by responsible parties;
- track structural sustainability / carbon / resource outcome where required.

### Evidence boundary

A site observation proves only what was observed, where and when. It does not establish concealed conditions, unobserved work or universal construction conformity.

### Native outputs

- site / fabrication query responses;
- observation / inspection records;
- nonconformity / concession / reanalysis records;
- construction-stage design changes;
- updated calculations / drawings where required;
- as-constructed information inputs;
- construction-stage structural assurance record.

### Exit / claim ceiling

Stage 5 may close when applicable structural design support and conformity evidence required by the appointment have been completed or transferred with explicit OPEN items.

**Does not prove:** universal site conformity, complete inspection coverage, statutory completion, latent-condition absence or final as-built authority unless separately evidenced.

---

## 13｜SE-SPW6 — Handover

**Source-aligned stage:** IStructE Stage 6 Handover.

### Professional question

> Is the structural information required for safe handover, defects resolution, operation / maintenance and future change captured with clear residual-risk and authority boundaries?

### Structural work

- support defects / structural issue resolution during handover period as appointed;
- complete/update structural as-constructed / handover information according to responsibility;
- contribute to Health & Safety File / Building Log Book / O&M information where applicable;
- record design assumptions that matter to future loading, alterations, maintenance and inspection;
- identify residual risks / monitoring / inspection requirements;
- contribute to lessons learned.

### Native outputs

- structural handover record;
- current as-constructed / record information refs;
- residual-risk / future-change constraints;
- inspection / monitoring recommendations when required;
- defects / concession closure record.

### Exit / claim ceiling

Handover closes when the structural information within appointed scope is transferred and material open defects / assumptions are explicit.

**Does not prove:** future performance, absence of latent defects, full asset-management completeness, or that every as-constructed condition was independently surveyed.

---

## 14｜SE-SPW7 — Use / Evaluation

**Source-aligned stage:** IStructE Stage 7 Use.

### Professional question

> What does real use reveal about the structural system, and which observations require intervention, reopen design assumptions or become bounded G9 learning?

### Structural work

- support Plan-for-Use / post-occupancy / project-performance tasks where appointed;
- compare designed assumptions and observed structural performance where evidence exists;
- review movement / cracking / vibration / settlement / corrosion / moisture / loading changes / structural monitoring as applicable;
- review alterations / new equipment / change of use before treating old design assumptions as current;
- capture maintenance / inspection / repair evidence;
- distinguish project-specific findings from transferable structural knowledge.

### Native outputs

- in-use structural assessment / monitoring report where triggered;
- change-of-use / alteration structural brief;
- designed-vs-observed performance record;
- G9 lesson candidates with applicability / uncertainty boundaries.

### Exit / claim ceiling

Stage 7 is event- and use-triggered rather than a one-time universal close. Each assessment closes only its declared scope.

**Does not prove:** indefinite future safety, unobserved conditions, universal system performance or transferable rule validity without Knowledge validation.

---

## 15｜Cross-disciplinary interface contract

Structural Engineering consumes and issues shared variables through the existing Cross-Disciplinary Integration owner.

High-value interfaces include:

| Interface | Typical shared variables / decisions | Structural minimum concern |
|---|---|---|
| Architecture | grids, spans, levels, cores, openings, transfers, member depth, movement joints | real load path + usable spatial consequence |
| Geotechnical | ground model, bearing / settlement / lateral behavior, groundwater | foundation / retaining assumptions traceable to current ground evidence |
| MEP | plant loads, risers, penetrations, supports, builder's work, vibration | loads/openings/supports integrated before affected stage closes |
| Fire | structural fire strategy, protection, compartment interfaces | resistance/protection basis explicit; Fire approval remains separate |
| Envelope | facade loads, supports, anchors, edge geometry, movement | support/tolerance/movement responsibility explicit |
| Interior / FF&E | partitions, heavy equipment, suspended items, vibration-sensitive uses | load/serviceability/support assumptions current |
| Landscape / Civil | retaining, canopies, planters, water/soil loads, external structures | load/ground/drainage interfaces coordinated |
| Cost / Procurement | material quantities, specialist packages, fabrication / sequence | cost optimization does not erase structural performance |
| FM / Operations | inspection, maintenance, replacement, future load/change | design assumptions available to operators / future designers |

Actual required maturity is per-interface / Acceptance Contract, not derived from the structural stage number.

---

## 16｜Shared Design Quality / DD binding

Structural engineering is not exempt from design-quality responsibilities when the structural decision materially shapes the project.

Typical bindings:

- `SE-SPW0/1` → `DD-01 Intent`, `DD-12 Integration`;
- `SE-SPW2` → `DD-02 Concept`, `DD-04 Form/Composition`, `DD-08 Detail/Craft` at system level, `DD-10 Adaptation`, `DD-12 Integration`;
- `SE-SPW3` → `DD-04 Form/Composition`, `DD-05 Human Relation` where structure affects use, `DD-08 Detail/Craft`, `DD-12 Integration`;
- `SE-SPW4/4.5` → `DD-07 Design Language` where exposed structure/material expression is intentional, `DD-08 Detail/Craft`, `DD-10 Adaptation`, `DD-12 Integration`;
- `SE-SPW5/6/7` → `DD-08 Detail/Craft`, `DD-10 Adaptation`, `DD-12 Integration` where actual built/use evidence affects design.

A safe structure can still be spatially destructive, materially crude or incoherent with the project design language. Technical structural PASS therefore does not infer Design KEEP.

---

## 17｜Content / drawing / model projection requirements

At each applicable stage, the structural artifact set must project the decision without hiding uncertainty.

Required roles may include:

- load path / stability diagram;
- structural grid / zone / system plan;
- sections through critical transfers / long spans / level changes;
- member / connection / support details according to stage;
- foundation / retaining relationship;
- movement / tolerance diagram;
- opening / penetration / embed / builder's-work interface;
- specialist-design boundary diagram;
- temporary-works dependency diagram;
- design-assurance / checking status;
- calculation / model assumptions and limitations;
- carbon / material quantity / structural sustainability evidence.

Hard co-location:

```text
structural claim ↔ governing assumption / limitation
member / connection status ↔ responsibility owner
calculation result ↔ model / load / code version
movement / tolerance ↔ affected interface
design release ↔ unresolved specialist / temporary-work item
site finding ↔ location / date / observation scope
```

A rendered structural model without these decision and evidence relations is presentation, not professional closure.

---

## 18｜Structural professional receipt

When triggered, emit a domain process receipt compatible with `professional-domain-process.v1.schema.json` and the Master Runtime compact summary.

Minimum professional receipt content:

- process / stage / cycle / baseline identity;
- current structural Basis of Design ref;
- Structural Responsibility Matrix ref;
- mounted consequential knowledge / source refs;
- current loads / ground / existing-condition authority state;
- structural system / stability / load-path decision state;
- current analytical / calculation / model refs;
- design-assurance / checker state;
- specialist / contractor-design boundaries;
- temporary-work interface state;
- active Integration interface refs;
- native output refs and actual readback refs;
- professional verdict;
- open / stale / reopened items;
- claim ceiling;
- `does_not_prove`.

The professional verdict may be `PASS / REVISE / REJECT / HOLD`. A terminal `REJECT` is legitimate when evidence demonstrates the current structural route is not viable. `CLOSED ≠ PASS`.

---

## 19｜Mandatory REVISE / HOLD conditions

At minimum, do not close a promotion-relevant structural claim when any applicable condition remains unresolved:

- project use / loading basis is missing or materially stale;
- site / geotechnical / existing-condition uncertainty contradicts the claimed design certainty;
- primary stability / load path is unresolved;
- major member / foundation / connection responsibility is unowned;
- critical serviceability / vibration criterion is absent;
- structural fire-resistance input is inconsistent with current fire strategy;
- material / durability / design-life basis is unknown where consequential;
- critical Architecture / MEP / Envelope / Fire / Geotechnical interface is below required maturity;
- analytical model and issued geometry materially disagree;
- specialist / contractor design has changed without integration/readback;
- temporary works materially affect permanent works but the dependency is unresolved;
- site/fabrication nonconformity requires design reanalysis that has not closed;
- a structural approval claim exceeds the responsible professional / jurisdictional evidence actually available.

---

## 20｜External research basis / freshness

This v1.0 is grounded in:

- Institution of Structural Engineers, *The Structural Plan of Work 2020*, published 2020-07-02, including stages 0, 1, 2, 3, 4, 4.5, 5, 6 and 7, structural responsibility, stage outputs, information exchanges, collaboration and design assurance;
- IStructE, *Checking regime for permanent building works — Part 1: categories of checking* and *Part 2: what to check and when*, published 2026-02-11, for risk-proportionate structural checking and stage-aware checking focus;
- Current OLEANDER structural routing framework `IDX-ARCH-STRUCT-SAFETY-005` and applicable project/jurisdiction sources.

Revalidate this process if IStructE materially revises its Structural Plan of Work, the applicable jurisdiction introduces material structural-design responsibility changes, or current OLEANDER Knowledge Integrity identifies a contradiction.

This process is not a substitute for jurisdiction-specific structural codes, responsible-engineer appointment, signed design, third-party checking, inspection, certification or field verification.

---

## 21｜Canonical structural invariant

```text
CURRENT STRUCTURAL CLAIM
= current project conditions
+ task/claim-mounted structural knowledge
+ explicit responsibility
+ current Basis of Structural Design
+ authentic source-aligned stage work
+ native engineering outputs
+ required interface maturity
+ actual readback
+ proportionate design assurance / checking
+ professional verdict
+ explicit claim ceiling / does-not-prove
```

Anything less may still be useful design evidence, but it must not be promoted as a stronger structural-engineering claim.

---

## 2026-09-19｜Execution Binding Contract｜Structural professional-depth parity

**Status effect:** additive execution-depth binding only. This does not change the Current Structural process, engineering responsibility, checking class or statutory authority.

### Knowledge binding
- `KN-METHOD-STRUCT-LOADPATH-CONNECTION-001` — hazard/load basis → global stability → load path → members/connections/supports;
- `KN-METHOD-STRUCT-CALC-DRAWING-RELEASE-001` — analysis/calculation ↔ schedule/drawing/detail ↔ RFI/shop/change/reanalysis;
- `KN-METHOD-STRUCT-ERECTION-TEMPWORKS-001` — staged/incomplete states, temporary support, sequence, tolerance and release;
- `KN-METHOD-STRUCT-FOUNDATION-GEOTECH-001` — ground model/parameters ↔ reactions/foundation/movement/groundwater/construction QA;
- current material/code/load/seismic/fire/geotechnical/product/test SOURCE owners as applicable.

### `required_native_outputs[]`
- current structural basis/load/hazard/assumption register;
- authoritative analysis model(s) and calculation package with version identity;
- load-path/stability/diaphragm/collector/transfer reasoning carriers;
- member/element/reaction schedules and connection force/criteria;
- coordinated structural plans/sections/details and calculation↔drawing trace;
- foundation-geotechnical interface/reaction/parameter/movement/test records;
- delegated connection/shop/submittal/RFI/change/reanalysis records;
- erection-stage/staged-analysis/temporary-support/tolerance/hold-point records where triggered;
- inspection/test/NCR/as-built/residual-risk closeout evidence.

### `execution_owner_requirements[]` / `required_capabilities[]`
- `oleander-research` — current code/material/geotechnical/test/source evidence;
- `oleander-design-process` — option/interface/change reasoning only; **not structural validation or engineering approval**;
- `oleander-3d-pipeline` — geometry/exchange/coordination carrier only; its current Blender/FreeCAD bounded capabilities do not become a structural solver or constructability proof;
- `oleander-technical-drawing` — candidate PR #172 only;
- `oleander-delivery-qc` — calculation/drawing/package integrity and reopenability only.

**Specialist execution gap / routing rule:** the Current core Skill registry has no installed Structural Analysis / Engineering Checker Skill. Consequential structural claims must bind the project-authorized analysis/calculation environment, competent structural engineer and required independent checker/reviewer. Solver execution alone is not approval. If required analysis/checking cannot be executed or read back, the claim remains `CAPABILITY_HOLD / PROFESSIONAL_HOLD` as applicable.

### `tool_adapter_requirements[]`
- project-authorized structural analysis/calculation solver with model/version/load-combination readback;
- project-authorized CAD/BIM/drawing/detail environment with stable object/grid/level/member identities;
- geotechnical parameter/report/test carrier linked to foundation calculations;
- connection/delegated-design/submittal carrier with force/stiffness/geometry/tolerance handoff;
- staged/temporary-works analysis carrier where triggered;
- inspection/test/survey/as-built evidence carrier;
- independent checker/review receipt appropriate to the claim.

### `typed_handoff_contracts[]`
- Architecture → Structure: current grids/levels/geometry/openings/use/load assumptions/interfaces/revision;
- Geotechnical → Structure: ground model + parameter + scope/location/depth/condition/confidence + groundwater/hazard + recheck trigger;
- Structure → Architecture/MEP/Facade/Foundation: member zones, reactions, openings, embeds/anchors, movement/deflection/tolerance and load criteria;
- Structure → Connection/Fabricator/Erector: current forces/stiffness/geometry/tolerance/sequence/special-condition criteria + responsibility boundary;
- Field/Shop return → Structure: exact object/location/revision/deviation/test + load-path/analysis impact + engineering disposition/reopen.

### `actual_readback_requirements[]`
- load/hazard basis ↔ current analysis model and load combinations;
- complete gravity/lateral/staged load path including discontinuities/transfers/collectors;
- model assumption/fixity/stiffness ↔ connection/detail/support reality;
- member/reaction/connection criteria ↔ issued drawings/schedules;
- geotechnical parameter/reaction/foundation location and movement compatibility;
- RFI/shop/site change ↔ reanalysis trigger and propagated drawing/detail revision;
- erection-stage load path / connection completion / temporary support before release;
- inspection/test/as-built deviation and checker disposition.

### `reopen_triggers[]`
Geometry/grid/level/opening change; load/use/equipment/facade/MEP load change; code/hazard/material/source revision; geotechnical/groundwater/unexpected-ground change; member/system/connection/foundation substitution; delegated-design/shop/RFI delta; erection sequence/temporary-support change; failed inspection/test/survey; field deviation; any calculation↔drawing inconsistency.

### Professional boundary
`MODEL RUN ≠ ENGINEERING PASS`; `MEMBER CHECKS GREEN ≠ LOAD PATH CLOSED`; `CALCULATION PASS ≠ DRAWING RELEASE`; `FINAL-STATE STABLE ≠ ERECTION-STAGE STABLE`; `DELIVERY QC PASS ≠ INDEPENDENT CHECK`. Human professional/engineer-of-record/statutory authority remains external and explicit.
