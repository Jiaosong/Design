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

## 4.5｜Structural Professional Stage Body / Title Contract

Every material `SE-SPW*` stage instance must remain recoverable as a professional structural-engineering body before it is compressed into a board, deck, issue sheet, model view or other presentation. The existing stage-specific sections below remain the professional authority; this cross-stage contract normalizes what the body must make findable without replacing Structural Plan of Work semantics or forcing generic visible headings.

The stage-body title must identify the real decision object, not merely the document type. Use a form such as:

`<project> | <SE-SPW stage id + stage name> | <structural decision / package / cycle / baseline>`.

Titles such as `Analysis`, `Concept`, `Design Development`, `Planning`, `Review` or `Final` are incomplete by themselves because they do not identify the bounded structural decision being made.

For each material stage, the body must expose these semantic responsibilities under structural-engineering-appropriate headings:

| Shared semantic responsibility | Structural body meaning |
|---|---|
| Professional Question / Scope | the structural question, package, responsibility boundary and claim scope being addressed |
| Current Condition / Problem | current geometry, load, site/ground, existing-condition, construction, serviceability or other uncertainty that makes structural work necessary |
| Authority / Knowledge / Evidence Inputs | current Basis of Structural Design inputs, task/claim-scoped knowledge mounts, applicable source/code versions, surveys/investigations, assumptions and evidence authority state |
| Professional Criteria / Intent | structural safety, stability, robustness, serviceability, durability, design-life, movement/tolerance, fire-resistance and other applicable criteria at the declared stage ceiling |
| Development / Analysis / Comparison / Mechanism | actual load-path/system development, analysis/model/calculation, option comparison, member/foundation/connection reasoning, construction or checking mechanism appropriate to the stage |
| Cross-domain Interfaces | material Architecture, Geotechnical, MEP, Fire, Envelope, Interior, Civil/Landscape, procurement, specialist or temporary-works dependencies and their current maturity/responsibility boundary |
| Native Output / Source of Truth | the authoritative calculation/model/drawing/schedule/specification/checking record or other required native engineering output for the claim |
| Actual Readback / Finding | what the current native source/checking/inspection/readback actually shows, distinguished from producer intent and interpreted as a bounded structural finding |
| Failure / OPEN / does_not_prove | unresolved assumptions, nonconformity, failed checks, unverified conditions, excluded scope and explicit limits on what the current evidence does not prove |
| Verdict / Claim Ceiling / Reopen / Next Action | bounded professional disposition, current claim ceiling, required reopen triggers and the next structural action or handoff |

The visible body may combine responsibilities where the structural stage naturally does so, but none may disappear silently when material to the claim. `NOT_APPLICABLE` requires a reason; omission is not evidence of non-applicability.

Knowledge remains mounted by reference. The structural body may state how a mounted source affects the present calculation, assumption, criterion or decision, but it must not copy reusable canonical Knowledge bodies or re-award KI/OE state.

The body must distinguish the evidence chain:

```text
INTENDED STRUCTURAL POSITION
→ IMPLEMENTED IN NATIVE ENGINEERING SOURCE
→ OBSERVED / CHECKED / READ BACK
→ INTERPRETED STRUCTURAL FINDING
→ BOUNDED PROFESSIONAL VERDICT
```

Hard boundaries:

```text
PROFESSIONAL BODY STRUCTURE ≠ CANONICAL KNOWLEDGE BODY
PROFESSIONAL PROSE ≠ NATIVE STRUCTURAL SOURCE
NATIVE STRUCTURAL SOURCE EXISTS ≠ STRUCTURAL PROFESSIONAL PASS
MODEL / CALCULATION EXISTS ≠ CHECKING PASS
MACHINE BODY-COMPLETENESS PASS ≠ ENGINEERING JUDGMENT
STRUCTURAL PROCESS PASS ≠ DESIGN KEEP
```

Machine validation may detect missing title/semantic coverage, missing native/readback references and contradictory `PASS + MISSING` states. It may not infer structural adequacy, licensed responsibility, statutory acceptance, site conformity or Design KEEP.

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

Inspection and test planning must be derived from the structural mechanism and uncertainty being controlled, not from a generic quality checklist. For each critical characteristic identify what must be observed/measured/tested, when it remains accessible, which Current specification/code/product/engineer basis governs acceptance, and which structural claim reopens if it is not evidenced.

Distinguish evidence types and claim ceilings: design check, material/product certification, fabrication/shop inspection, site visual/dimensional inspection, NDT/material test, load/proof test, survey/monitoring and as-constructed record do not prove the same thing. Define hold/witness/readback points before critical work is concealed or irreversible, including connections, reinforcement/embeds, bearings/supports, fire/corrosion protection, repair substrate/preparation and temporary-to-permanent load-transfer states where applicable.

State the sampling/coverage rationale for repeated elements and how anomalies expand inspection/test scope; one conforming sample cannot silently represent a population whose fabrication, location, batch, detail or construction state materially differs. For any test capable of influencing acceptance, bind specimen/element identity, preparation, method/equipment/calibration state, loading/environmental condition, acceptance source and retest/nonconformity route to the exact design configuration. Inspection/testing/statutory witnessing remains with appointed/responsible owners; this process requires a structurally credible evidence plan without taking over their authority.

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

For reuse, strengthening, extension or alteration, treat record drawings and prior calculations as hypotheses about the existing structure until reconciled with Current physical evidence needed by the intervention. Build an evidence ladder by decision: record information → measured geometry/survey → visible condition/damage/repair history → targeted opening-up or scan/test → material/property evidence → connection/reinforcement/support/foundation verification where the feature controls the claim.

Reconcile known alterations, penetrations, removed/added members, previous strengthening, corrosion/deterioration, fire/damage events and change-of-use/load history with the model used for appraisal. An original-design model cannot stand as the Current as-is model after material change. State which uncertainty blocks reuse, which can be bounded conservatively and which requires further investigation; one exposed bay/sample cannot represent repeated elements without a defensible representativeness basis.

Compare reuse/strengthening options on intervention extent, load redistribution, temporary stability, buildability/access, reversibility, retained architectural value, future inspection/maintenance and deconstruction consequence as well as calculated capacity. Historic compliance does not prove current capacity/condition, and missing records do not by themselves prove reuse impossible.

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

#### Concept option decision depth

Each retained structural option must be compared, as applicable, on:

- primary gravity and lateral load path;
- grid / span / structural depth and usable-space consequence;
- transfer, cantilever or long-span dependency;
- foundation / ground sensitivity;
- serviceability including deflection and vibration;
- robustness and disproportionate-collapse questions where applicable;
- structural fire-resistance strategy input;
- durability / design-life / exposure condition;
- movement / tolerance behavior;
- major openings / penetrations / builder's-work consequence;
- material system and connection / fabrication logic;
- erection and temporary-condition dependency;
- adaptability, strengthening, disassembly or deconstruction consequence where relevant;
- embodied-resource / carbon consequence at the available resolution;
- cost / procurement / supply-chain or specialist-package consequence;
- Architecture / MEP / Envelope / Fire / Geotechnical interfaces capable of reversing the selection.

Mark any assumption whose resolution could reverse the preferred concept as **selection-critical**. Until that assumption is bounded by Current evidence, the structural concept remains conditional or `HOLD` at the affected claim; it is not made unconditional merely because a plausible analysis model can be run.

### Concept analysis and load-model integrity

Concept analysis must be strong enough to **falsify** an option, not merely illustrate it. Preserve the reasoning chain:

`action / load source → load path → idealization → restraint / stiffness assumption → response → serviceability / strength / stability consequence → interface consequence → concept decision`.

Resolve as applicable:

- which actions, combinations, accidental conditions and construction states are material under the Current governing basis;
- tributary/distribution assumptions and where redistribution or continuity is being relied upon;
- diaphragm, collector, transfer and discontinuity behavior rather than treating stability arrows as proof;
- support/fixity/release assumptions that materially alter span, moment, vibration, movement or foundation reaction;
- cracked/uncracked, composite/non-composite, staged/long-term or other stiffness assumptions where they could change concept selection;
- second-order / instability sensitivity when sway, compression, slenderness or geometry makes it selection-critical;
- dynamic excitation source, frequency-sensitive occupancy/equipment and damping assumptions when vibration can govern use;
- differential settlement/heave, shrinkage, creep, thermal or other movement mechanisms capable of damaging the structure or adjacent systems;
- load introduction from facade, plant, equipment, partitions, storage, crowds, soil, water or landscape where localized actions matter;
- erection / temporary states where the final load path or restraint does not yet exist.

Run sensitivity or bounding checks when a credible variation in support, stiffness, load, ground condition, transfer behavior or connection assumption could reverse the decision. One apparently precise solver result must not hide an assumption-sensitive concept.

Unexpectedly favorable results require a deliberate model attack: check units, self-weight, duplicated/missing members, releases, supports, load application, member orientation, mesh/idealization and effective stiffness before treating margin as real.

`SOLVER CONVERGED ≠ STRUCTURAL MODEL CREDIBLE`.

`GLOBAL MODEL PASS ≠ LOAD PATH / LOCAL DETAIL / FOUNDATION PASS`.

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

### Spatial-coordination engineering depth

Spatial coordination must preserve the **physical behavior implied by the coordinated geometry**. At critical zones, review as applicable:

- transfer zones and discontinuities in plan/section with the actual supported elements above and below;
- openings, penetrations and recesses against shear, punching, torsion, local reinforcement, edge/support zones and buildability at the current responsibility ceiling;
- stair, ramp, atrium, core, facade-edge and cantilever geometry where support eccentricity, movement or differential deflection affects another discipline;
- plant, equipment, facade and interior point/line loads at actual support positions rather than generic area loads where localization is material;
- foundation, retaining and below-ground structure against utilities, waterproofing, drainage, excavation support and future maintenance access;
- movement joints against diaphragm continuity, services, envelope, finishes, partitions and circulation;
- predicted deflection / camber / settlement / movement against facade, drainage falls, brittle finishes, operable partitions, doors, MEP gradients and equipment alignment;
- tolerance zones around embeds, anchors, openings and prefabricated/specialist interfaces where nominal coordination can still fail during manufacture or erection.

For each selection-critical opening, notch, penetration, cast-in or support interface, the handoff should carry geometry/location, affected member/system, load/movement consequence, permitted tolerance or design allowance, owner and reopen condition. A clash marker or coordination comment is not an engineering acceptance object.

Where structural movement is deliberately accommodated by another system, the **expected movement range and direction** must be available to that system's owner. “Allow for movement” without a structural basis is insufficient.

`MODEL COORDINATED ≠ MOVEMENT / TOLERANCE COORDINATED`.

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

### Technical analysis / checking integrity

Technical calculations and finite-element / frame / plate / foundation models must be reviewable as **engineering arguments**, not opaque software outputs. Preserve where applicable:

- exact geometry, section, material, support, release and stiffness basis;
- Current action/load source and governing combinations used for the in-claim check;
- material/geometric nonlinear, staged, cracked, long-term or soil/support behavior assumptions when they materially affect response;
- meshing/member idealization and the boundary between global and local/submodel behavior;
- effective length, restraint, imperfection and governing stability mode where relevant;
- serviceability criteria tied to the actual user, facade, MEP, finish or equipment consequence that makes them controlling;
- connection/joint/bearing/anchorage stiffness assumptions where global force distribution depends on them;
- foundation/soil parameters and uncertainty at the actual geotechnical evidence ceiling;
- sensitivity to any input whose credible range materially changes utilization, movement, stability or selected detail;
- comparison with equilibrium/load-path checks, hand checks, benchmark/submodel or other independent reasoning proportionate to risk;
- exact correspondence between the calculated member/zone/configuration and the issued drawing/model revision.

Select the analysis formulation from the governing mechanism rather than software availability. Where response depends materially on second-order effects, contact/gap, yielding, cracking, changing restraint, large displacement or other path-dependent behavior, record why linearized analysis remains adequate or what nonlinear representation is used.

For nonlinear work, state the initial geometry/imperfection, constitutive/stiffness idealization, support/contact state, load/application sequence and convergence/equilibrium interpretation that govern the result. Numerical convergence does not prove that the physically relevant equilibrium path or failure mechanism has been captured.

Where construction sequence changes stiffness, support, continuity or load introduction, model or bound the relevant stages: addition/removal of props or members, composite activation, prestress/post-tension sequence, staged loading, temporary support, shrinkage/creep or other history effects as applicable. Final-state analysis must not erase locked-in force/deformation that materially changes permanent response. Attack sensitivity with alternate increment/step, stiffness/support or idealization assumptions where they can change the governing mode; reconcile a local nonlinear/submodel result back to the global model when it changes global stiffness or force redistribution.

For vibration/dynamic work, state the excitation model, mass, stiffness, damping and frequency/time-domain basis appropriate to the claim, then relate predicted response to the actual occupancy/equipment sensitivity. A static deflection check cannot clear a dynamic-use claim.

For robustness / disproportionate-collapse or alternate-load-path claims, make explicit the initiating local-damage assumption, continuity/tie/redistribution mechanism, affected configuration and claim limit. Ordinary gravity utilization alone does not establish robustness.

For each robustness/local-damage case required by the Current governing basis, identify the initiating local loss/degradation, the function removed, the immediately affected tributary load and the intended alternate transfer path through diaphragms/collectors/members/connections/supports/foundations. Check the deformation, rotation, slip, anchorage, membrane/catenary or other component behavior that the alternate path actually requires; a diagrammatic redundant path is not credible if joints/supports fail before redistribution develops.

Identify brittle/local mechanisms and shared/common-mode dependencies capable of defeating nominal redundancy: one support line, connection family, collector, diaphragm edge, foundation element or fire/damage zone may control several apparently independent members. Distinguish prevention/protection, local resistance, tying/continuity and alternate-path strategies and state which mechanism is in claim. Consume initiating hazard/fire/security/accidental-action assumptions from their controlling authority rather than inventing scenarios in the structural process. Where local-damage response materially redistributes force or stiffness, reconcile changed demand back into the global model, connections and foundations and read the exact damaged configuration rather than only the intact model. No universal damage scenario or acceptance value is introduced here.

For fire/durability/exposure, consume the controlling specialist/code basis and translate it into section, cover/protection, material and detail consequences; Structure does not invent fire scenarios or exposure classes outside its authority.

Where repeated loading, vibration, thermal movement, machinery, traffic, wind-induced response or other cyclic action is material, treat fatigue as a distinct mechanism rather than relying on static utilization. Bind action/cycle history, stress-range or equivalent demand representation, detail geometry/category, connection/weld/bolt/reinforcement condition and Current source/method to the actual element in claim. Identify stress concentrations, attachment details, abrupt stiffness changes, weld toes/terminations, holes/cut-outs or other local features that can govern cyclic performance even when nominal section stress is modest.

Treat durability as a deterioration path:

`exposure/source → transport/attack or wear mechanism → vulnerable material/detail → protection/drainage/detailing response → inspection/maintenance access → repair/replacement consequence`.

Where corrosion, moisture, freeze/thaw, chemical attack, abrasion or protection-system loss can amplify fatigue, section loss, cracking, bond or connection degradation, make the interaction explicit and carry it into inspection/replaceability strategy. Structure consumes controlling exposure/fatigue/product/protection criteria from Current sources; this process installs no universal cycle, category, coating-life or exposure threshold.

Technical PASS requires unresolved differences between model, drawings, responsibility matrix and specialist interfaces to be either closed or explicitly bounded. A complete-looking calculation package cannot rescue stale inputs or mismatched issued geometry.

`CALCULATION PACKAGE COMPLETE ≠ TECHNICAL DESIGN VERIFIED`.

### Foundation / ground-structure coupling depth

Where foundations, retaining or ground interaction are material, reconcile structural reactions and stiffness assumptions with the Current geotechnical ground model rather than treating soil parameters as fixed inputs.

Record as applicable:

- strata / groundwater / existing-foundation / investigation authority and evidence ceiling;
- bearing, settlement, uplift, lateral and retaining mechanisms relevant to the selected system;
- construction / excavation / temporary support state where it changes the ground-structure relation;
- neighboring / retained-structure sensitivity;
- the credible range of ground response capable of changing foundation type, stiffness, force distribution or movement;
- interface consequences for waterproofing, drainage, utilities, access, retained structures and excavation sequence.

Return reactions, contact pressures and movement requirements to Geotechnical/Civil and consume their updated response; iterate when either side changes. Carry differential movement into frame, envelope, MEP, drainage and brittle-finish interfaces rather than stopping the analysis at the foundation reaction table.

Treat soil-structure interaction as an **uncertainty-bearing coupled model**, not a one-way table of soil parameters. Where the structural decision is sensitive to foundation/support stiffness, contact, uplift, settlement, lateral restraint or retaining behavior, carry the Current Geotechnical evidence range/ground-model alternatives into structural sensitivity or bounding cases and identify which variation can reverse foundation type, force distribution, stability, movement or a downstream interface decision.

Preserve the iteration chain where material:

`Geotechnical ground model / evidence ceiling → structural foundation/support idealization → reactions + contact/movement demand → Geotechnical response / revised assumption → structural redistribution + movement → interface consequence / reopen`.

Do not tune spring stiffness, fixity, contact or settlement assumptions merely to obtain a favorable frame result. Where an assumed support distribution or stiffness is not directly supported by the Current Geotechnical basis, mark it as a structural sensitivity/OPEN item and state what investigation, geotechnical response or bounded envelope is required before the affected claim can close. Structural Engineering owns the structural idealization, sensitivity and consequence; Geotechnical/Civil retain ground model, parameter validity, ground-improvement, earthworks/excavation and geotechnical acceptance authority.

Structure does not self-award geotechnical parameter validity, ground-improvement acceptance or excavation/retaining approval outside its owner boundary.

### Connection and local-force transfer depth

Where system behavior depends on local transfer, trace governing global actions into actual joint/support geometry and back-check any joint stiffness/continuity assumption used by the global model.

Resolve as applicable:

- load introduction, eccentricity and bearing path;
- anchorage, bolt/weld/reinforcement/plate or equivalent force transfer;
- local punching, buckling, prying, splitting, breakout or other governing local mechanism;
- fit-up, fabrication/erection tolerance and access for installation/inspection;
- rotation/slip/stiffness behavior where the global analysis assumes more than nominal pin/fixity;
- robustness/ductility and alternate-load-path role where material;
- fire, durability, corrosion/protection and replaceability/inspectability consequences;
- erection / temporary restraint sequence when continuity develops progressively.

Specialist-designed connections must receive explicit design actions, movement/tolerance, required behavior and interface geometry. `CONNECTION BY SPECIALIST` is not closure when connection behavior controls the primary model or downstream interface.

Connection adequacy must distinguish **strength present** from the deformation, ductility and local-stability behavior needed by the structural system. Where redistribution, robustness, cyclic/dynamic response, staged continuity or a global stiffness assumption depends on connection behavior, state the required force-deformation/rotation/slip role and the intended sequence of component response rather than checking only peak nominal resistance.

Attack local weak-link mechanisms across the actual joint geometry: plate/member slenderness or local buckling, bearing/crushing, prying, block/tear-out/splitting-type paths, anchor/reinforcement development, weld/bolt group eccentricity, panel/support-zone deformation and loss of restraint as applicable to the material/system. The retained detail must not depend on a nominally ductile global mechanism if a brittle or unstable local component can terminate that mechanism first.

Where the global model assumes connection stiffness, continuity or redistribution, reconcile the detailed joint response back to that model and to adjacent member/local stability checks. Where the specialist owns detailed connection design, the Structural owner must still issue the required actions, deformation/stiffness/ductility role, geometry/tolerance and governing system consequence; the specialist retains detailed component design and product/process responsibility within appointment.

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

### Production, fabrication and erection-state depth

Production review must attack states that do not exist in the final permanent-works model. As applicable, check:

- lifting, transport, temporary support and erection sequence where stability/load path changes before continuity is complete;
- temporary eccentricity, unbraced length, incomplete diaphragm, wet concrete, construction loading, backpropping or staged prestress where they influence permanent design or a critical interface;
- connection fit-up, bolt/weld access, reinforcement congestion, placement/compaction space, splice/coupler geometry and inspection access;
- fabrication / erection tolerances and how they accumulate across repeated bays, long runs, embeds, precast units, steelwork, facade supports or equipment interfaces;
- datum / setting-out strategy and survey control for geometry whose mislocation creates a critical interface failure;
- coating/protection, weld preparation, galvanizing/paint/fire-protection or other process effects on connection geometry and tolerance where material;
- substitution of section, grade, fastener, reinforcement, connector or proprietary system against the exact assumptions that made the technical design pass;
- hold / witness / inspection points where later enclosure would make a critical structural condition unobservable.

Represent each selection-critical erection/construction sequence as structural state transitions, identifying which supports/restraints/connections/composite actions are active, what load has been introduced and which permanent-work assumptions are not yet valid in each state. Define the evidence needed before a critical transition or release—such as removal/relocation of temporary support, transfer of load, activation of composite/continuity behavior, stressing or loading of a new element—using the Current responsible-engineer/temporary-works/specification basis rather than generic timing rules.

Reconcile temporary-works reactions, imposed restraint and construction deformation with permanent-work camber/geometry, connection fit, facade/MEP tolerances and any locked-in force or movement that survives the transition. If the contractor/specialist proposes a sequence materially different from the Basis of Structural Design, reopen the affected staged/nonlinear analysis, permanent member/connection checks and downstream interface handoffs before treating the revised sequence as equivalent. The temporary-works designer owns temporary-work adequacy within appointment; the permanent-works structural owner must expose every temporary-state assumption on which permanent behavior, geometry or release depends and require the corresponding interface readback before release.

Site or shop observation is **sampled evidence**. Bind it to location/item/date/revision and observed condition; do not infer whole-structure conformity from one sample. A defect affecting load path, connection, durability, fire protection, geometry/tolerance or downstream interface remains open until the accepted repair and its readback are evidenced at the appropriate responsibility boundary.

`FABRICATION DRAWING APPROVED ≠ FABRICATED CONDITION PASS`.

`ONE INSPECTION SAMPLE ≠ WHOLE STRUCTURE CONFORMITY`.

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

### Site / fabrication observation evidence threshold

Every site, fabrication or inspection observation used to support a structural finding or closure must bind, as applicable:

- observation / inspection ID and exact element, connection, zone or fabrication item;
- date/time, construction/fabrication stage and accessible/exposed condition;
- Current drawing/model/specification/calculation or acceptance basis reviewed;
- observed condition and measurement/test method, units and instrument calibration/verification state where material;
- photograph / scan / test / fabrication-quality record refs;
- deviation / nonconformity and whether it can affect load path, member/connection behavior, support/restraint, tolerance/movement, fire protection or durability;
- responsible observer/witness and competence/appointment boundary where required;
- corrective action or design reanalysis required;
- reinspection/retest reference and closure state;
- concealed, unobserved or unsampled scope not covered;
- affected interface / professional receipt and smallest truthful reopen scope;
- claim ceiling / `does_not_prove`.

Spot or sample observation must not be generalized beyond its recorded coverage. When an observed deviation can change the governing structural mechanism, model assumption or issued controlled variable, reopen the affected design/checking/interface before accepting the work or carrying the prior professional claim forward.

Classify a deviation by the **structural mechanism it can change**, not visual severity alone. Compare the observed state with Current controlled geometry/material/detail and identify effects on load path, stiffness/restraint, local force transfer, stability, serviceability, durability/fire protection, tolerance/movement and downstream interfaces.

Use an explicit disposition route: accept-as-is only with a recorded technical basis at the responsible authority ceiling; otherwise rework, repair, strengthen, replace, test/inspect further or reanalyse as applicable. A contractor concession request or marked-up photograph is not structural acceptance.

Treat the proposed repair itself as a new structural condition. Drilling, heat/welding, section removal, added restraint, local stiffness, grout/patch material, temporary unloading/support, access and sequence can create new actions/damage and may require their own calculation/check/interface review. When an accepted deviation changes the design basis, update the affected calculation/model/drawing/specification/as-constructed record and reopen downstream interfaces that consumed the superseded variable.

Closure requires readback of the actual repaired/as-accepted state and required test/reinspection against the exact disposition. `REPAIR INSTRUCTION ISSUED ≠ REPAIR VERIFIED`. Repeated similar deviations should trigger systemic review of setting-out, fabrication process, tolerance assumption, inspection point, material supply or sequencing when a common cause is plausible.

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

### In-use diagnostic / monitoring depth

An in-use symptom is a trigger for hypothesis-led assessment, not a cause.

For cracking, movement, vibration, settlement, corrosion/moisture or unexpected loading, bind as applicable:

- exact location / element / zone and date/time;
- environmental / occupancy / load / operational state;
- baseline and as-built geometry/material/configuration;
- measurement / monitoring / inspection method, calibration/precision and sampling frequency where material;
- trend/history and known interventions, repairs or load/use changes;
- current drawings/calculations/model revision and any known divergence from as-built condition.

State competing structural and non-structural explanations, then choose monitoring/tests that can discriminate among them. Preserve raw time-series/inspection evidence before repair or tuning.

Compare observed response with the original design prediction or a bounded updated model representing the Current configuration, including uncertainty. A local observation closes only its sampled question; unexplained change, accelerating trend or configuration mismatch reopens the affected structural model/check and interface owners.

Where monitoring is used for decision-making, define the action threshold from the Current professional/source basis and the consequence of exceedance. A dashboard trace without a decision rule is observation, not structural control.

Interpret a monitoring trigger as a **decision signal**, not automatic proof of structural damage or adequacy. Bind each material trigger to its baseline/configuration, sensor or inspection validity, environmental/load context, persistence or rate/trend condition where relevant, spatial correlation with other observations and the structural mechanism it is intended to discriminate. A single excursion can be instrumentation, operational or environmental noise; a value below a nominal trigger cannot clear an unexplained adverse trend or configuration mismatch.

When a trigger is approached or crossed, use the Current responsible-engineer/source basis to define the next bounded action: verify data quality/instrument state, inspect, obtain corroborating measurement/test evidence, restrict or change use where professionally required, update the structural model, or reopen the affected design/interface. Do not infer root cause from the trigger alone, and do not silently revise the threshold after an adverse observation to preserve a prior PASS.

After repair, strengthening, sensor replacement, load/use change or other intervention, record whether the original baseline and trigger remain comparable. If a new baseline is established, preserve the pre-intervention record and the rationale/authority for the reset so trend discontinuity is not mistaken for structural recovery. Numerical trigger values remain bound to Current professional/source/project evidence; this process introduces none.

`OBSERVED CRACK / VIBRATION / MOVEMENT ≠ ROOT CAUSE`.

### Native outputs

- in-use structural assessment / monitoring report where triggered;
- change-of-use / alteration structural brief;
- designed-vs-observed performance record;
- G9 lesson candidates with applicability / uncertainty boundaries.

### Exit / claim ceiling

Stage 7 is event- and use-triggered rather than a one-time universal close. Each assessment closes only its declared scope.

**Does not prove:** indefinite future safety, unobserved conditions, universal system performance or transferable rule validity without Knowledge validation.

## 14.5｜Structural decision thresholds and handoff content

The stage descriptions above define work and outputs; this section defines the minimum **engineering-decision substance** required before those outputs are safe to consume downstream. The process does not impose generic member sizes, deflection limits, vibration criteria, factors, fire ratings, tolerances or foundation parameters. Every numerical criterion must be bound to the Current project brief, applicable code/standard, Basis of Structural Design, responsible-engineer decision or verified project evidence, with units and applicability explicit.

For every promotion-relevant structural stage, review the following relations where material:

1. **Load and demand basis** — permanent/imposed/environmental/dynamic/equipment/construction loads, combinations and diversity are traceable to Current assumptions; a changed occupancy, equipment duty or temporary condition cannot remain hidden behind an unchanged analysis model.
2. **Load-path continuity and stability** — gravity and lateral actions have a credible path through members/connections/supports/foundations to the ground or retained structure; transfers, discontinuities and robustness-critical elements are explicit.
3. **Model-to-physical-system equivalence** — supports, releases, stiffness, diaphragm behavior, member offsets, eccentricities, boundary conditions and staged assumptions represent the actual system closely enough for the claimed decision. Numerical convergence does not compensate for a physically wrong model.
4. **Serviceability and human-use consequence** — deflection, movement, vibration, drift, cracking or other serviceability behavior is checked against the use, finishes, envelope, partitions, equipment and human experience actually affected.
5. **Connection / local-force transfer** — where the claim depends on continuity, anchorage, bearing, fixings, embeds, plates, reinforcement, local punching/buckling or similar local mechanisms, responsibility and the required stage resolution are explicit rather than left as a generic “connection by specialist”.
6. **Ground / existing-condition dependency** — foundation, retaining, strengthening or reuse decisions state which ground/existing facts are verified, assumed or awaiting investigation and what claim is blocked if those assumptions move outside their accepted envelope.
7. **Movement / tolerance / interface behavior** — expected structural movement and construction tolerance are translated into joint, facade, MEP, partition, finish, bearing and equipment interface consequences; “no clash” is not movement compatibility.
8. **Durability / fire / exposure / design life** — material choice, cover/protection, corrosion/moisture/freeze/chemical exposure, structural fire input and replaceability/inspection implications are resolved at the stage claim ceiling.
9. **Constructability / sequence / temporary condition** — the permanent design does not depend on an impossible erection sequence, unowned temporary restraint or unreviewed construction state where that condition materially changes forces, stability or geometry.
10. **Material and resource consequence** — optimization/carbon/resource reduction remains subordinate to structural performance and constructability; a lighter option is not retained when its increased complexity, fire protection, vibration, connection, transport or maintenance consequence defeats the project criterion.

### Stage acceptance threshold

A structural stage may support `PASS` only when:

- every **in-claim controlling assumption** is Current or explicitly conditional at a ceiling that still permits the decision;
- every **MAJOR / CRITICAL structural mechanism** needed for the stage question has a resolved owner and native evidence path;
- the analysis/model/drawing relation has been read back against the same Current geometry/load/boundary-condition basis;
- required checking has addressed the **failure modes that control the decision**, not merely arithmetic or software warnings;
- every outgoing controlled variable needed by another domain has an explicit value/range/state, source carrier and reopen rule;
- no unresolved in-claim contradiction remains between stability, strength, serviceability, durability/fire, constructability and current interface requirements.

Use `REVISE` when the structural route remains viable but one or more material mechanisms, details, interfaces or evidence relations require redesign. Use `HOLD` when a necessary authority, ground/existing fact, load basis, specialist input, native source or required independent check is unavailable. Use `REJECT` when the current structural route should not proceed under the declared brief/constraints because the governing mechanism or trade-off is unacceptable, not merely because documentation is incomplete.

### Structural handoff payload

Every material outgoing handoff should provide, at minimum:

`decision / controlled variable → value or bounded range + units → governing assumption/source → native model/drawing/calculation ref → movement/tolerance or load condition where relevant → recipient → required interface maturity → OPEN limit → requested change/reopen rule`.

Examples include grid/level/member-zone geometry to Architecture, opening/support/load data to MEP, movement/anchor/load envelopes to Envelope, fire-resistance/protection assumptions to Fire, foundation actions/movement requirements to Geotechnical, and inspection/maintenance/load-change constraints to FM.

The receiving domain may reject a handoff that is internally inconsistent, based on stale geometry/loading, lacks units/tolerance, or is below the maturity required for its claim. Acceptance confirms only that the input is usable at the agreed interface ceiling; it does not transfer structural professional responsibility.

`ANALYSIS RESULT ≠ STRUCTURAL DECISION UNTIL PHYSICAL MECHANISM + BASIS + READBACK AGREE`.

`COORDINATED GEOMETRY ≠ TOLERANCE / MOVEMENT COMPATIBILITY`.

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

### 15.1｜Minimum structural interface issue payload

For each material structural handoff, issue the smallest sufficient owner-native payload needed by the consumer:

- shared variable / decision ID;
- Current structural source / revision;
- geometry / location;
- value or bounded range and units when measurable;
- load / reaction / action direction where relevant;
- support / restraint / stiffness assumption where governing;
- movement / tolerance envelope;
- opening / penetration / embed / support requirement;
- sequence / temporary-condition dependency when it affects permanent works;
- responsibility owner;
- required R-F interface / Acceptance Contract ref and requested maturity;
- unresolved assumption / OPEN boundary;
- claim ceiling;
- requested change / reopen trigger.

Do not hand off “coordinate with Structure” as a substitute for these variables. A model view without the governing load, movement, tolerance and source relation is a representation, not a complete structural interface issue.

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
