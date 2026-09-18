# OLEANDER Function → Concept Synthesis Extension

Status: `CANDIDATE EXTENSION / EXISTING OWNER / CURRENT FUNCTIONAL-ARCHITECTURE ALIGNED / EXTERNAL-MECHANISM DIGESTED / PROJECT REPLAY EVIDENCE / GOLDEN REGRESSION REQUIRED / NO PROMOTION`

Owner: `oleander-design-process`

## Purpose

Use when a design question is too open to jump directly from requirements or desired experience into one form, architecture, mechanism or layout, and the team needs a disciplined way to generate **materially different concept architectures** from what the design must do.

This extension fills one narrow DESIGN-layer gap:

`NEED / INTENT → FUNCTIONS → FUNCTION RELATIONS → SOLUTION PRINCIPLES → COMPATIBLE PRINCIPLE COMBINATIONS → CONCEPT ARCHITECTURES → EMBODIMENT PROTOTYPES → DESIGN REVIEW / VALIDATION HANDOFF`

It does **not** create:
- a Systems Engineering process;
- a new Functional Architecture authority;
- a universal engineering-design lifecycle;
- a TRIZ/Pahl-and-Beitz/Pugh methodology mandate;
- a professional technical approval process;
- a replacement for Architecture zoning, Structural concept design, Product Phase Gates or the Current Trade Study owner.

The purpose is to prevent a common failure:

`REQUIREMENTS → FIRST FAMILIAR OBJECT → POLISH`

and a second failure:

`MORPHOLOGICAL TABLE → EVERY COLUMN TREATED INDEPENDENT → HUNDREDS OF IMPOSSIBLE OR COSMETIC COMBINATIONS`.

`FUNCTIONALLY COMPLETE CONCEPT ≠ TECHNICALLY FEASIBLE ≠ DESIGN KEEP ≠ PROFESSIONAL APPROVAL`.

---

## 1｜When to activate

Activate when one or more are true:

- the object/system has several distinct functions whose means are still open;
- multiple architectures can satisfy the same need through different causal mechanisms;
- a product/mechanism/spatial/service system is being prematurely represented by one familiar object type;
- the team has a list of features/components but cannot explain what functions they satisfy;
- solution principles interact and compatibility must be reasoned before detailed embodiment;
- a concept family needs to be differentiated by mechanism/architecture rather than visual styling;
- an existing Current concept needs retrospective function/principle readback without reopening its authority;
- a contradiction such as compactness vs access, stiffness vs weight, visibility vs privacy or simplicity vs redundancy needs alternative principle families.

Do **not** activate when:

- the professional process already owns the same question at higher fidelity, such as Architecture ADD-04/05 zoning;
- the task is a bounded repair with one locked architecture and no meaningful concept freedom;
- the open question is primarily parameter optimization inside one concept family; use `COMPUTATIONAL_OPTION_SPACE_EXTENSION.md`;
- the issue is an interface failure between already-defined subsystems; use `SYSTEM_INTERFACE_COUPLING_EXTENSION.md`;
- the task is only visual expression / presentation of an already-defined concept;
- source/requirements are too unresolved to state even provisional functions.

---

## 2｜Authority position

Before synthesis resolve:

`CURRENT AUTHORITY → DECISION OBJECT → USER / SYSTEM NEED → DESIGN INTENT → REQUIREMENTS / CONSTRAINTS → LOCKED DESIGN DNA → OPEN CONCEPT VARIABLES → PROFESSIONAL / TECHNICAL OWNERS → CLAIM CEILING`

Function synthesis may organize design reasoning. It may not create authority that upstream sources do not provide.

Keep separate:

- **Need** — why the object/service/system exists for an actor or larger system.
- **Function** — what transformation, support, transfer, control, separation, indication or relation must occur.
- **Performance requirement** — how well a function must perform.
- **Constraint** — a boundary the concept may not violate.
- **Solution principle / means** — one causal way a function might be achieved.
- **Component / form** — an embodiment of one or more principles.
- **Interface** — a controlled relation between functions/principles/components.
- **Evidence** — what supports a function, means, feasibility or result claim.

Do not convert a component named in a precedent into a required function.

Example:

Bad:
`FUNCTION = HINGE`

Better:
`FUNCTION = ALLOW CONTROLLED ROTATION BETWEEN A AND B`

Possible means may include hinge, flexure, compliant joint, pivot bearing or another principle if allowed by project authority and physics.

---

## 3｜System Functional Architecture alignment / namespace firewall

At review time, the Current OLEANDER system-level Functional Architecture uses the `F*` namespace for OLEANDER's own system functions, including C3 Exploration functions such as candidate-direction generation, strategy-difference exposure and superficial-option detection.

This extension is an **execution mechanism under that design-exploration capability**, not another Functional Architecture.

Therefore:

- never mint project/design-object records as `F1.1 / F3.1 / F01` when they can be confused with OLEANDER system-function IDs;
- use a local namespace such as `<OBJECT>-DFN-01` or another project-authorized design-function ID;
- local design-function records do not enter or modify the OLEANDER system Function Catalogue;
- this extension may help execute system C3 Exploration but may not redefine its authority, actor allocation, traceability or lifecycle;
- if formal Systems Engineering Functional Architecture is triggered for the project/product/system itself, that professional owner remains separate.

`OLEANDER SYSTEM FUNCTION ≠ PROJECT DESIGN-OBJECT FUNCTION`.

`C3 EXPLORATION CAPABILITY → THIS EXTENSION MAY EXECUTE A BOUNDED SYNTHESIS METHOD`.

---

## 3｜Function statement contract

Write material functions in solution-neutral form where meaningful.

Preferred pattern:

`VERB + OBJECT / FLOW + CONDITION / PURPOSE`

Examples:
- support short-duration body load;
- maintain clear passage;
- transfer user input to mechanism;
- prevent water accumulation;
- isolate heat from hand contact;
- preserve route-status truth across channels;
- locate component relative to datum;
- allow service access without damaging enclosure;
- retain object during motion;
- indicate system state to user.

Avoid:
- noun-only labels such as “handle”, “screen”, “bracket”;
- vague qualities such as “premium”, “comfortable”, “innovative”;
- implementation disguised as function;
- performance numbers without source.

Each material function may record:

`function_id / statement / actor_or_system / input / output / precondition / failure_state / source_or_rationale / requirement_refs / evidence_state / owner`.

---

## 4｜Function boundary

Define what crosses the concept boundary.

Possible flows:
- material;
- energy;
- force/load;
- motion;
- signal;
- information;
- person;
- service;
- permission;
- heat;
- fluid;
- light;
- sound;
- attention;
- responsibility.

Record as applicable:

`INPUT → FUNCTION / TRANSFORMATION → OUTPUT`

plus:
- source/sink;
- state;
- direction;
- unit where authoritative;
- timing/sequence;
- uncertainty.

This is a design abstraction. Technical units/physics remain with the relevant professional owner when the claim requires them.

---

## 5｜Function decomposition

Decompose only far enough to expose alternative concept logic.

Possible levels:

### Primary function
The core outcome without which the object/system does not exist.

### Enabling function
Required to let the primary function occur.

### Protective / limiting function
Prevents unacceptable consequence or constrains operation.

### Control / feedback function
Sets, senses, communicates or regulates state.

### Service / maintenance function
Allows inspection, replacement, cleaning, reset, transport or recovery.

### Experience / semantic function
Makes use, state, hierarchy or interaction legible when that is truly part of the brief.

Do not force every project into these exact categories; they are prompts.

Stop decomposition when another level would:
- merely rename components;
- create no new solution freedom;
- exceed current claim/evidence;
- belong to a specialist domain;
- add bookkeeping without changing a design decision.

---

## 6｜Function dependency graph

Functions are rarely independent.

For each material relation classify as useful:

- `PRECEDES` — A must happen before B;
- `ENABLES` — A makes B possible;
- `CONSTRAINS` — A limits B;
- `COUPLED` — choices for A materially alter valid means for B;
- `SHARES_MEANS` — one principle/component may satisfy both;
- `CONFLICTS` — improving one relation can damage another;
- `REDUNDANT_WITH` — alternative function path exists;
- `FAILURE_PROPAGATES_TO` — A failure compromises B.

The graph must make dependencies visible **before** morphological combinations are counted.

`NUMBER OF FUNCTION ROWS ≠ NUMBER OF INDEPENDENT DESIGN DIMENSIONS`.

---

## 7｜Essential vs supporting functions

Mark a function as:

- `ESSENTIAL` — loss invalidates the current concept claim;
- `SUPPORTING` — improves or enables use but can be separated or degraded;
- `CONDITIONAL` — only applicable in certain scenarios/states;
- `UNVERIFIED` — function itself still lacks sufficient authority.

This status is not priority scoring.

A concept missing an ESSENTIAL function is incomplete even if its weighted score is high.

---

## 8｜Function provenance

Every material function should trace to at least one of:

- user/stakeholder need;
- Current brief;
- observed behavior;
- professional requirement;
- safety/accessibility/service requirement;
- system/interface necessity;
- design principle;
- evidence-backed failure mode;
- explicit assumption.

If a function exists only because a precedent product contains a feature:

`PRECEDENT FEATURE → INFERENCE / HYPOTHESIS`

not automatic requirement.

---

## 9｜Solution principle / means pool

For each open function, create a bounded pool of distinct causal means.

Record:

`means_id → function_id → causal principle → embodiment examples only if helpful → source / precedent / physics basis → maturity → dependencies → incompatible conditions → unknowns → specialist validation owner`.

Means maturity may be:
- `KNOWN / PRECEDENTED`;
- `PLAUSIBLE / UNVERIFIED`;
- `EXPERIMENTAL`;
- `OUTSIDE CURRENT CLAIM`.

Do not equate “familiar product type” with “known feasible in this project.”

### Principle before object

Prefer:
`FRICTION CLAMP`
over:
`Brand X clamp bracket`.

Prefer:
`PASSIVE GRAVITY RETURN`
over:
`spring-loaded lid`
when the actual causal question is broader.

This keeps concept freedom open while preserving technical boundaries.

---

## 10｜Morphological matrix as one carrier

A morphological matrix may be used:

| Function | Means A | Means B | Means C |
|---|---|---|---|

But it is only a **parts bin of possible principles**, not the final option space.

The naive Cartesian product is invalid unless independence is established.

If:
- F1 has 3 means;
- F2 has 3 means;
- F3 has 3 means;

do **not** automatically claim 27 viable concepts.

First evaluate:
- dependency;
- mutual exclusion;
- shared means;
- duplicated architecture;
- technical impossibility;
- authority conflicts;
- missing interface;
- scenario applicability.

---

## 11｜Compatibility matrix

For material means pairs record:

- `COMPATIBLE`;
- `CONDITIONAL`;
- `INCOMPATIBLE`;
- `UNKNOWN`.

For `CONDITIONAL`, state the condition.

For `UNKNOWN`, name the validation or evidence needed.

Possible incompatibility reasons:
- geometry;
- topology;
- kinematics;
- physics;
- process;
- environment;
- human use;
- maintenance;
- safety;
- source requirement;
- interface;
- timing/state;
- cost/schedule ceiling when authoritative.

Do not replace a technical incompatibility question with AI intuition when specialist evidence is required.

---

## 12｜Coupled means bundle

When several functions are tightly dependent, bundle them into one concept block rather than pretending they are independent matrix rows.

Example:

`ATTACH + LOAD TRANSFER + RELEASE`

may be one coupled architecture family.

Represent:

`bundle_id → member_functions → principle_family → internal dependency → interfaces → claim ceiling`.

This prevents combinatorial inflation.

---

## 13｜Shared-means economy

One principle/component may satisfy multiple functions.

Record:

`MEANS → FUNCTIONS SATISFIED → COUPLING COST → SINGLE-POINT FAILURE RISK → SERVICE CONSEQUENCE`.

Do not reward part-count reduction automatically.

A shared means can:
- improve coherence;
- reduce parts;
- simplify use;

but can also:
- increase coupling;
- create common-mode failure;
- reduce serviceability;
- make later adaptation harder.

---

## 14｜Contradiction ledger

When two functions/criteria pull in opposing directions, record the actual contradiction:

`IMPROVE A → DAMAGES B → WHY → CURRENT PRIORITY / AUTHORITY → POSSIBLE PRINCIPLE MOVES → EVIDENCE NEEDED`.

Possible concept-generation moves:
- separate in space;
- separate in time/state;
- separate by user/role;
- split function across components;
- combine functions through one principle;
- add controlled compliance;
- localize a property;
- make state reversible;
- introduce redundancy;
- change topology;
- change energy/material/information path.

These are generic contradiction moves, **not a mandatory TRIZ catalog**.

Named external inventive-principle systems may be consulted as references but do not become OLEANDER Core taxonomy.

---

## 15｜Concept architecture assembly

A concept architecture is more than one selected cell per function.

For each candidate record:

- `concept_id`;
- concept family;
- functions covered;
- selected means / bundles;
- function-means trace;
- main causal mechanism;
- physical/spatial/information architecture;
- key interfaces;
- shared variables;
- required states/configurations;
- unresolved functions;
- incompatible/conditional relations;
- primary trade-off;
- technical/professional handoffs;
- falsifier;
- expected embodiment type.

A candidate with all rows filled but no coherent causal architecture is not a concept.

---

## 16｜Concept completeness gate

Check:

1. all ESSENTIAL functions covered;
2. no known incompatible pair remains;
3. conditional pairs state their condition;
4. UNKNOWN compatibility remains visible;
5. required interfaces are identified;
6. conserved budgets are reconciled when triggered;
7. no locked design DNA is silently violated;
8. failure/recovery/service functions are not omitted where material;
9. no specialist technical claim is self-certified by the design matrix.

Result:
- `COMPLETE_FOR_CONCEPT_REVIEW`;
- `INCOMPLETE`;
- `HOLD`.

This is concept completeness only.

---

## 17｜Concept-family deduplication

Two combinations are not distinct concepts merely because their matrix cells differ.

Ask:

`DO THEY DIFFER IN PRIMARY CAUSAL MECHANISM / FUNCTION ALLOCATION / TOPOLOGY / INTERFACE STRUCTURE / SUPPORT STRATEGY / STATE MODEL?`

If not, collapse into one family with variants.

Examples of likely variants:
- same mechanism, different material;
- same architecture, different fastener type;
- same flow, different color;
- same topology, small dimensions.

Examples of possible family changes:
- dependent on existing host structure vs structurally independent;
- centralized actuation vs distributed actuation;
- passive vs powered;
- physical control vs digital mediation;
- serial process vs parallel process;
- one shared support vs multiple independent supports.

The exact family axis is project-specific.

---

## 18｜No-count theatre

Do not require a fixed number of functions, means or combinations.

Counts are diagnostics only.

Bad:
`5 FUNCTIONS × 4 MEANS = 1024 CONCEPTS → DIVERGENCE SUCCESS`.

Better:
`12 raw combinations → 7 incompatible → 2 duplicate families → 3 coherent concept families → 1 key unresolved compatibility test`.

Quality is the coverage of material causal alternatives, not combinatorial volume.

---

## 19｜Technical feasibility handoff

For each candidate identify which questions belong to a specialist.

Examples:
- structural load path;
- fatigue;
- thermal performance;
- mechanism force/torque;
- motor sizing;
- fluid behavior;
- electrical safety;
- fire;
- accessibility/code;
- manufacturing capability;
- material durability;
- software/security;
- field/site capacity.

Use:

`CONCEPT PRINCIPLE → TECHNICAL QUESTION → INPUTS REQUIRED → VALIDATION OWNER → CURRENT STATUS → DESIGN CONSEQUENCE IF FAIL`.

Do not eliminate a concept solely because technical proof is not yet run if it can remain a bounded candidate.

Do not mark it feasible either.

---

## 20｜Embodiment bridge

Once concept families are coherent, translate each retained concept into the **minimum faithful artifact** that exposes its causal architecture.

Possible embodiments:
- functional block diagram;
- mechanism sketch;
- plan/section;
- product skeleton;
- CAD envelope;
- state prototype;
- storyboard;
- service blueprint;
- system interface diagram;
- physical mockup.

The artifact should make visible:
- function allocation;
- major means;
- interfaces;
- scale/geometry relevant to the question;
- state/motion if relevant;
- failure-sensitive relation.

`MORPHOLOGICAL TABLE ≠ EMBODIED CONCEPT`.

---

## 21｜Matched concept comparison

Compare retained concept families at equivalent evidence/fidelity.

Do not compare:
- one polished render vs one text note;
- one detailed CAD model vs one rough sketch;
- one concept with technical analysis vs another without.

For matched review record:
- same decision question;
- same essential functions;
- same hard constraints;
- same source baseline;
- comparable fidelity;
- same scenario/load/use state where applicable.

Then apply existing OLEANDER option/trade-study and Design Review rules.

---

## 22｜Selection firewall

Morphological synthesis may generate candidates. It may not select by counting “best” cells.

Do not use:
- raw number of satisfied functions;
- matrix-row votes;
- arbitrary 1–5 scores;
- Pugh sum;
- weighted total;

as automatic Design KEEP.

Use the existing sequence:

`HARD GATES → DOMINANCE / PARETO / DECISION CORRIDOR → SENSITIVITY / UNCERTAINTY → DISCRIMINATING PROTOTYPE → DESIGN REVIEW → SELECT / REVISE / REJECT / HOLD`.

A weighted matrix may exist as a bounded analytic carrier only when weights/normalization have authority and no hard gate is diluted.

---

## 23｜Functional architecture boundary

This extension creates a **design-reasoning function model**, not the formal Systems Engineering Functional Architecture authority.

If a project triggers a professional Systems Engineering process, that owner may require:
- formal function decomposition;
- functional interfaces;
- allocation;
- logical architecture;
- configuration/baseline;
- requirement verification;
- system V&V.

Those professional semantics remain with R-E Systems Engineering when formalized/triggered.

The design-process extension may feed that owner but cannot replace it.

---

## 24｜Architecture boundary

For building design:

- room/program functions;
- adjacency;
- zoning alternatives;
- circulation;
- operations;
- plan/section;

remain governed by `architecture-design-development-process-v1.0.md`.

Do not use this extension to create a parallel building-zoning process.

It may still help a bounded sub-object/mechanism within architecture when the question is truly function-to-means rather than building program organization.

---

## 25｜Product boundary

For physical products, use with:
- `PHYSICAL_PRODUCT_PHASE_GATES_EXTENSION.md`;
- `PRODUCT_FORM_AFFORDANCE_SERVICEABILITY_EXTENSION.md`;
- Human Factors / DFM / Prototype V&V extensions;
- `oleander-3d-pipeline` for native geometry.

This extension can generate alternative product architectures, but it cannot certify ergonomics, manufacturing, structure, mechanism performance or safety.

---

## 26｜Service boundary

For service/hybrid systems:

- functions may include orient, authorize, reserve, transfer, recover, confirm, support;
- means may be human, digital, physical, organizational or mixed.

When the concept is assembled, route operational visibility/dependency to `SERVICE_BLUEPRINT_OPERATIONAL_DEPENDENCY_EXTENSION.md`.

Do not let a service concept hide backstage feasibility.

---

## 27｜Interface boundary

Once a concept introduces a material boundary between subsystems/components/actors, route it to `SYSTEM_INTERFACE_COUPLING_EXTENSION.md`.

This extension identifies that the interface exists and why.

System Interface owns:
- exchanged thing;
- direction;
- units/format;
- timing;
- ownership;
- maturity;
- acceptance/readback.

Do not maintain duplicate interface truth in the morphological matrix.

---

## 28｜Change propagation

A change to:
- need;
- essential function;
- requirement;
- locked DNA;
- solution principle;
- compatibility result;
- professional finding;
- interface;
- environment;
- embodiment test;

may invalidate prior concepts.

Use:

`CHANGE → AFFECTED FUNCTIONS → AFFECTED MEANS → AFFECTED COMPATIBILITY → STALE CONCEPTS → REASSEMBLY / RETEST → UPDATED DECISION`.

Do not preserve a selected concept merely because detailed work has already begun.

---

## 29｜Failure attacks

Reject or revise when:

- functions are actually component names;
- a precedent feature becomes a requirement without source;
- dependent functions are treated as independent morphological rows;
- the Cartesian product is reported as viable concepts;
- known incompatible means are combined;
- UNKNOWN compatibility silently becomes compatible;
- technical feasibility is assumed from conceptual coherence;
- one means is duplicated across rows and counted as independent diversity;
- concept families differ only by material/color/trim;
- one polished embodiment wins against rough alternatives;
- a weighted matrix overrides a hard requirement;
- architecture zoning is redundantly rebuilt inside this extension;
- formal Systems Engineering claims are made without the professional owner;
- the selected concept has no function-means trace;
- service/maintenance/recovery functions disappear because they are not part of hero use;
- detailed embodiment begins before the concept's causal architecture is coherent.

---

## 30｜Required outputs

Use only those relevant:

1. `need_intent_authority`
2. `function_ledger`
3. `function_boundary_flows`
4. `function_dependency_graph`
5. `essential_supporting_conditional_state`
6. `solution_principle_pool`
7. `morphological_matrix_or_equivalent`
8. `means_compatibility_matrix`
9. `coupled_means_bundles`
10. `contradiction_ledger`
11. `concept_architecture_ledger`
12. `concept_completeness_results`
13. `concept_family_deduplication`
14. `technical_feasibility_handoffs`
15. `matched_embodiment_artifacts`
16. `design_review_disposition`
17. `selected_and_rejected_rationale`
18. `reopen_trigger`
19. `claim_ceiling`

---

## 31｜External mechanism digestion boundary

Mechanisms studied:
- functional decomposition;
- morphological chart / matrix;
- morphological synthesis;
- contradiction-driven ideation;
- divergence before convergence;
- concept combinations;
- matched solution framing.

Accepted:
- solution-neutral function statements;
- function dependency before combination;
- principle/means pool;
- compatibility matrix;
- coupled-means bundle;
- shared-means analysis;
- contradiction ledger;
- concept architecture rather than raw combination;
- family deduplication;
- embodiment bridge;
- technical handoff and claim ceiling.

Rejected as universal OLEANDER defaults:
- fixed concept counts;
- “quantity is quality” as an absolute;
- full Cartesian-product counting as useful divergence;
- TRIZ 40 principles as Core taxonomy;
- Pugh matrix as automatic selector;
- 1–5 / 1–10 weighted-score decision;
- SRR/PDR/CDR/TRR/DCR as universal OLEANDER project gates;
- domain standards detached from current jurisdiction/source;
- one engineering design-cycle sequence as a replacement for OLEANDER runtime or professional-domain processes.

No external code or prose is required to execute this extension.

---

## 32｜Maturity

On creation:

`CANDIDATE EXTENSION / EXISTING DESIGN OWNER / EXTERNAL MECHANISMS DIGESTED / GOLDEN REGRESSION REQUIRED / PROJECT REPLAY REQUIRED / NO CROSS-CONTEXT EVIDENCE / NO PROMOTION`.

Promotion requires:
- real or bounded project use;
- at least one incompatible/unknown combination exposed;
- at least two genuine concept families when alternatives exist;
- matched embodiment comparison;
- one technical/professional handoff where feasibility is outside DESIGN authority;
- evidence that the extension prevents premature form lock without creating combinatorial/process theatre.

`MORPHOLOGICAL COVERAGE ≠ CONCEPT QUALITY`.
