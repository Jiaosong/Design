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

## Practitioner object contracts｜执业对象合同层

Machine carrier: `00-governance/schemas/structural-engineering-design-process.v1.json`

The earlier execution-depth object lists are an index only. The objects below are the field-level practitioner contracts used to make Structural Engineering executable at professional depth. The machine carrier is authoritative for validation; this prose mirrors the same substance for human review.

A named register/schedule/model is not considered sufficient unless its source, required fields, owner, revision identity, release/readback, HOLD and reopen semantics are all resolved.

### STR-OBJ-01｜Basis of Structural Design / Design Criteria Record

- **Parity dimension:** `PROFESSIONAL_PROBLEM_AND_JUDGMENT`
- **Stage refs:** `SE-SPW0`, `SE-SPW1`, `SE-SPW2`
- **Professional purpose:** Define structural performance, design situations, actions, materials, robustness/serviceability/fire/durability assumptions and responsibility basis for structural decisions.
- **Native source of truth:** Current structural brief + applicable codes/standards + geotechnical/site/architectural authority.
- **Decision owner:** Structural Engineering professional owner
- **Contributor / specialist refs:** Architecture; Geotechnical; Fire Engineering; Temporary Works where applicable
- **Revision identity:** basis_id + criteria/source revision + structural baseline revision
- **Required record fields:** `basis_id`, `structure_scope`, `design_life_or_project_basis`, `design_situations`, `actions_and_combinations_basis`, `material_systems`, `serviceability_criteria`, `robustness_and_disproportionate_collapse_basis`, `fire_durability_basis`, `geotechnical_basis`, `temporary_stage_dependencies`, `interfaces`, `assumptions`, `open_items`, `owner`, `checker`
- **Release / retention rule:** Retain only when controlling criteria/sources and consequential assumptions are explicit; unresolved inputs cap downstream claims.
- **Required readback:**
  - criteria/source readback
  - load/action basis trace
  - interface assumption attack
- **Failure / HOLD conditions:**
  - design criteria inferred from precedent
  - geotechnical/site input absent but treated final
  - temporary/construction state ignored where material
- **Reopen triggers:**
  - code/standard change
  - brief/use/load change
  - geotechnical change
  - architecture/grid change
  - construction method change
- **Downstream handoffs:** SE-SPW2 options; analysis/calculation baseline; member/connection/foundation design
- **Independent review:** Independent checker must review the governing basis proportionate to consequence before final structural reliance.
- **Does not prove:** code approval; geotechnical PASS; construction-stage safety approval

### STR-OBJ-02｜Analysis / Calculation Assumption & Baseline Register

- **Parity dimension:** `ASSUMPTION_UNCERTAINTY`
- **Stage refs:** `SE-SPW2`, `SE-SPW3`, `SE-SPW4`
- **Professional purpose:** Control analytical model assumptions, idealisations, boundary conditions, stiffness/load paths and calculation revisions.
- **Native source of truth:** Owner-native calculation/model sources + Basis of Structural Design + current geometry/material inputs.
- **Decision owner:** Structural Engineering professional owner
- **Contributor / specialist refs:** Analysis specialist; Geotechnical; Architecture
- **Revision identity:** analysis_id + exact model/calculation revision/hash + input baseline
- **Required record fields:** `analysis_id`, `model_or_calc_ref`, `revision`, `purpose`, `geometry_source`, `material_properties_source`, `supports_boundary_conditions`, `loads_combinations`, `stiffness_release_idealisation`, `second_order_or_nonlin_basis`, `imperfection_basis`, `sensitivity_or_handcheck`, `assumptions`, `limitations`, `checker`, `status`
- **Release / retention rule:** No final member/connection/foundation release may rely on an analysis whose consequential assumptions or source geometry are stale/unread.
- **Required readback:**
  - model input audit
  - equilibrium/load-path sanity check
  - independent hand/sensitivity check appropriate to risk
  - result ↔ member/detail trace
- **Failure / HOLD conditions:**
  - wrong geometry/load revision
  - unstated support idealisation
  - solver convergence/result accepted without engineering check
  - local model used beyond validity
- **Reopen triggers:**
  - geometry/load/material/support change
  - analysis method change
  - field/nonconformity change
  - review contradiction
- **Downstream handoffs:** design packages; release schedule; checking record
- **Independent review:** Independent structural checker must inspect inputs/assumptions and representative critical outputs, not only final ratios.
- **Does not prove:** structural adequacy beyond analysed scope; construction conformity; geotechnical validity

### STR-OBJ-03｜Structural System / Load-path Option Study

- **Parity dimension:** `OPTION_COMPARISON`
- **Stage refs:** `SE-SPW2`
- **Professional purpose:** Compare materially different structural systems, stability strategies, spans/grids, materials and foundation concepts under common criteria.
- **Native source of truth:** Editable structural option diagrams/models/calculations tied to same architectural/site/BOSD baseline.
- **Decision owner:** Structural Engineering professional owner
- **Contributor / specialist refs:** Architecture; Geotechnical; MEP; Cost/Construction
- **Revision identity:** option_id + common basis revision + option source revision
- **Required record fields:** `option_id`, `system_family`, `gravity_load_path`, `lateral_stability`, `grid_span_depth`, `material_system`, `foundation_strategy`, `movement_robustness`, `construction_sequence_implication`, `MEP_architecture_consequence`, `carbon_cost_programme_consequence`, `critical_risks`, `required_tests`, `retained_rejected_reason`
- **Release / retention rule:** Selection requires explicit load-path/stability/foundation logic; optimization score or member tonnage alone cannot select the system.
- **Required readback:**
  - load-path diagram readback
  - representative order-of-magnitude checks
  - spatial coordination consequence comparison
- **Failure / HOLD conditions:**
  - same system with member-size variants counted as families
  - stability path omitted
  - foundation consequence ignored
  - unsupported precision in early option
- **Reopen triggers:**
  - architecture/grid/span change
  - geotechnical change
  - material/procurement change
  - new robustness/fire requirement
- **Downstream handoffs:** SE-SPW3 coordination; Architecture; MEP; Geotechnical
- **Independent review:** Independent review must attack the selected system's governing stability/load-path/foundation assumptions and compare strongest alternative.
- **Does not prove:** final analysis PASS; fabrication readiness; code/statutory approval

### STR-OBJ-04｜Controlled Structural Analysis / Drawing / Design Package

- **Parity dimension:** `NATIVE_WORK`
- **Stage refs:** `SE-SPW3`, `SE-SPW4`, `SE-SPW4.5`
- **Professional purpose:** Carry the actual structural design through coordinated models, calculations, drawings, schedules and details with traceable input/output identity.
- **Native source of truth:** Controlled structural analysis/calculation models + drawings/BIM/details/specifications.
- **Decision owner:** Structural Engineering professional owner
- **Contributor / specialist refs:** BIM/CAD; Connection specialist; Geotechnical; Architecture
- **Revision identity:** package_id + exact native model/calculation/drawing revision
- **Required record fields:** `package_id`, `analysis_refs`, `calculation_refs`, `drawing_model_refs`, `member_schedule_refs`, `connection_detail_refs`, `foundation_refs`, `grid_level_source`, `material_grade_refs`, `load_case_refs`, `interface_refs`, `revision`, `author`, `checker`, `issue_status`
- **Release / retention rule:** Downstream use requires coordinated calculation/model/drawing identity; extracted PDFs do not replace native analytical/design sources.
- **Required readback:**
  - analysis ↔ drawing/member schedule trace
  - critical connection/foundation detail readback
  - grid/level/interface consistency
- **Failure / HOLD conditions:**
  - analysis and drawing revisions diverge
  - member schedule not tied to calc
  - connection load not traceable
  - foundation assumption stale
- **Reopen triggers:**
  - analysis revision
  - architecture/grid/level change
  - material/connection/foundation change
  - field deviation
- **Downstream handoffs:** fabrication/shop drawing; construction; record structure
- **Independent review:** Independent checker reviews exact controlled package or bounded subset with explicit limits.
- **Does not prove:** fabrication conformity; site installation; temporary works adequacy unless included

### STR-OBJ-05｜Member / Connection / Foundation Release & Specialist Submittal Register

- **Parity dimension:** `RELEASE_CONTROL`
- **Stage refs:** `SE-SPW4`, `SE-SPW4.5`
- **Professional purpose:** Control which structural elements/details/specialist designs are sufficiently checked and coordinated for downstream manufacture/construction reliance.
- **Native source of truth:** Current structural design package + checked specialist/fabrication/submittal information.
- **Decision owner:** Structural Engineering professional owner
- **Contributor / specialist refs:** Fabricator/Specialist designer; Independent checker; Architecture; MEP
- **Revision identity:** release_id + exact design/submittal revision
- **Required record fields:** `release_id`, `element_or_scope`, `design_action_demand_ref`, `native_design_ref`, `specialist_submittal_ref`, `revision`, `checking_class_or_plan_ref`, `interfaces`, `review_comments`, `conditions`, `release_authority`, `release_state`, `supersedes`, `downstream_receiver`
- **Release / retention rule:** Release cannot exceed checked scope; conditional release retains open conditions and may not imply whole-structure approval.
- **Required readback:**
  - submittal ↔ design load/geometry/material comparison
  - checker disposition readback
  - downstream revision acknowledgement
- **Failure / HOLD conditions:**
  - shop drawing accepted against stale design
  - connection load unavailable
  - conditional item treated closed
  - different revision fabricated
- **Reopen triggers:**
  - design change
  - fabricator proposal
  - RFI
  - material/substitution
  - interface change
- **Downstream handoffs:** fabrication; construction; inspection/test
- **Independent review:** Independent checking per declared structural assurance plan and consequence class.
- **Does not prove:** fabrication workmanship; site installation conformity; statutory approval

### STR-OBJ-06｜Inspection / Test / Material / Field Nonconformity Register

- **Parity dimension:** `IMPLEMENTATION_FIELD`
- **Stage refs:** `SE-SPW5`
- **Professional purpose:** Bind observed/tested construction evidence, material certification, nonconformities and field changes to the exact structural design scope.
- **Native source of truth:** ITP/test/material/site evidence + issued structural information.
- **Decision owner:** Structural Engineering professional owner
- **Contributor / specialist refs:** Contractor; Fabricator; Testing laboratory; Site inspector; Independent checker
- **Revision identity:** field_item_id + exact element/location + design revision + evidence date
- **Required record fields:** `field_item_id`, `element_location`, `inspection_or_test_type`, `date`, `issued_design_ref`, `material_heat_batch_or_product_ref`, `measured_test_result`, `acceptance_basis`, `nonconformity`, `engineering_assessment`, `disposition`, `repair_or_retest`, `affected_design_refs`, `owner`, `closure_evidence`
- **Release / retention rule:** Observed/tested evidence closes only the inspected/tested scope; material field changes require design/calculation/readback updates.
- **Required readback:**
  - test certificate/result audit
  - field condition ↔ design detail
  - repair/retest readback
- **Failure / HOLD conditions:**
  - test result without sample/location trace
  - site photo generalized to all work
  - repair not rechecked
  - field change not fed back to model/drawing
- **Reopen triggers:**
  - failed test
  - nonconformity
  - material substitution
  - site geometry deviation
  - construction-stage condition change
- **Downstream handoffs:** closeout/as-constructed; future monitoring
- **Independent review:** Independent/specialist witness required when stated by assurance/ITP/statutory/contractual basis.
- **Does not prove:** uninspected work; hidden work conformity; whole-structure PASS

### STR-OBJ-07｜Structural Closeout / Residual Risk / Monitoring Register

- **Parity dimension:** `HANDOVER_INUSE`
- **Stage refs:** `SE-SPW6`, `SE-SPW7`
- **Professional purpose:** Transfer as-constructed structural information, residual risks, inspection/maintenance/monitoring requirements and future-change constraints.
- **Native source of truth:** Accepted as-constructed structural records + unresolved items + monitoring/use evidence.
- **Decision owner:** Structural Engineering professional owner
- **Contributor / specialist refs:** Operations/FM; Client; Contractor; Monitoring specialist
- **Revision identity:** closeout_id + as-constructed baseline revision
- **Required record fields:** `closeout_id`, `structure_scope`, `as_constructed_refs`, `material_and_product_refs`, `residual_risks`, `load_or_use_constraints`, `inspection_maintenance_requirements`, `monitoring_points_and_baseline`, `open_items`, `owner`, `future_change_restrictions`, `inuse_observations`, `closure_state`
- **Release / retention rule:** Handover must distinguish design intent, accepted as-constructed information and unverified field conditions; monitoring criteria remain configuration-specific.
- **Required readback:**
  - as-constructed ↔ design baseline comparison
  - open-item closure
  - monitoring baseline/result readback where claimed
- **Failure / HOLD conditions:**
  - design drawings mislabeled as record
  - residual risk omitted
  - future penetration/load change not controlled
  - monitoring result without baseline/configuration
- **Reopen triggers:**
  - future loading/change
  - damage/incident
  - monitoring threshold
  - alteration/penetration
  - new inspection evidence
- **Downstream handoffs:** Operations/FM; future structural engineer; G9 bounded learning
- **Independent review:** Independent closeout/checking review when required by assurance plan or consequence.
- **Does not prove:** future performance; all hidden construction conformity; fitness for unassessed future change

### STR-OBJ-08｜Structural Design Assurance / Independent Check Record

- **Parity dimension:** `INDEPENDENT_REVIEW`
- **Stage refs:** `SE-SPW1`, `SE-SPW4`, `SE-SPW4.5`, `SE-SPW5`
- **Professional purpose:** Provide risk-proportionate independent checking of basis, analysis, design, details and material changes on exact baselines.
- **Native source of truth:** Structural assurance/checking plan + controlled design/calculation/submittal/field evidence.
- **Decision owner:** Independent Structural checker
- **Contributor / specialist refs:** Structural professional owner; Specialist reviewers
- **Revision identity:** check_id + exact checked baseline revision
- **Required record fields:** `check_id`, `check_scope`, `consequence_or_check_basis`, `reviewer_independence`, `baseline_refs`, `methods`, `critical_elements`, `independent_calculation_or_review_refs`, `findings`, `severity`, `repair_required`, `recheck_refs`, `verdict`, `claim_ceiling`
- **Release / retention rule:** Check applies only to declared scope/revision; material changes stale affected check conclusions.
- **Required readback:**
  - independent calc/review readback
  - critical load-path/stability/detail attack
  - repair/recheck evidence
- **Failure / HOLD conditions:**
  - checker not independent where required
  - review only final utilization ratios
  - changed baseline not rechecked
  - major contradiction unresolved
- **Reopen triggers:**
  - design/calculation/detail change
  - new field evidence
  - material/nonconformity
  - load/criteria change
- **Downstream handoffs:** release register; professional receipt
- **Independent review:** Reviewer independence and method must be proportionate to consequence/risk and declared in the assurance plan.
- **Does not prove:** construction conformity; statutory approval; Design KEEP

### STR-OBJ-09｜Structural Change / Reanalysis / Reverification Ledger

- **Parity dimension:** `CHANGE_PROPAGATION`
- **Stage refs:** `CROSS_STAGE`
- **Professional purpose:** Propagate structural changes to affected calculations, models, drawings, releases, checks and field evidence.
- **Native source of truth:** Controlled change event + dependency links from structural models/design packages/releases.
- **Decision owner:** Structural Engineering professional owner
- **Contributor / specialist refs:** Architecture; MEP; Geotechnical; Fabricator/Contractor; Independent checker
- **Revision identity:** change_id + source revision
- **Required record fields:** `change_id`, `trigger`, `changed_parameter_or_object`, `old_revision`, `new_revision`, `affected_load_paths`, `affected_analysis_models`, `affected_members_connections_foundations`, `affected_drawings_schedules`, `affected_interfaces`, `affected_checks_releases`, `required_reanalysis`, `required_reinspection_or_retest`, `owner`, `closure`
- **Release / retention rule:** No closure until affected analytical/design/release/check scopes are re-established or explicitly retained by evidence.
- **Required readback:**
  - dependency impact trace
  - reanalysis/recheck readback
  - affected submittal/field notification
- **Failure / HOLD conditions:**
  - change recorded only in drawing
  - calculation not reopened
  - released fabrication not assessed
  - inspection/test applicability assumed unchanged
- **Reopen triggers:**
  - any material geometry/load/material/support/connection/foundation/site change
- **Downstream handoffs:** all affected structural stages/interfaces
- **Independent review:** Independent checker involvement when changed scope falls within prior independent-check basis.
- **Does not prove:** unaffected scope invalidation; automatic adequacy after change

The practitioner-object layer does not change this domain's Current/Candidate authority status and does not by itself prove project execution or professional PASS.
