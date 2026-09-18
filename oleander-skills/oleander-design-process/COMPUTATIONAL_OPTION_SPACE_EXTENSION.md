# OLEANDER Computational Option Space Extension

Status: `CANDIDATE EXTENSION / EXISTING OWNER / EXTERNAL-MECHANISM DIGESTED / NO PROJECT USAGE / NO PROMOTION`

## Purpose

Use this extension when the open design question can be expressed as a bounded but materially large solution space whose variables, relationships, capacities, constraints or performance signals can be made explicit enough to generate and compare more options than ordinary manual divergence can reasonably cover.

This is an extension of `oleander-design-process`, not a new generative-design Skill, solver owner, architecture process, project state or approval authority.

The extension exists to make computational exploration design-useful and evidence-honest:

`DESIGN QUESTION → SEARCH-SPACE CONTRACT → CANDIDATE GENERATION → FEASIBILITY / REPAIR → OBJECTIVE EVIDENCE → DIVERSITY / TRADE-OFF SET → REAL ARTIFACT COMPARISON → DESIGN REVIEW → SELECT / REVISE / HOLD → REOPEN`

A solver may expand or interrogate the option space. It does not own the design decision.

`OPTIMIZED ≠ DESIGN KEEP ≠ PROFESSIONAL APPROVAL ≠ FIELD PASS`.

---

## 1｜When to activate

Activate only when at least one of the following is material:

- several design variables have explicit domains/ranges and their combinations create a large option space;
- room, component, route, interface or system relations can be represented as a graph / constraint problem;
- area, weight, cost, energy, power, time, attention or another finite budget must be allocated across competing uses;
- multiple measurable objectives conflict and a single scalar “best” value would hide trade-offs;
- the design must test sensitivity or robustness across ranges rather than one manually tuned point;
- topology, configuration or arrangement can change discretely rather than only through local parameter tuning;
- the team needs evidence that a candidate family was not selected merely because it was the first plausible option.

Do **not** activate merely because:
- a design has many parameters;
- a visual generator can produce many images;
- a solver/tool is available;
- the user asks for “AI-generated options” but the design problem is not yet framed;
- the Current design already has one bounded local repair and a broader search would reopen locked variables without cause.

If only one small parameter family is open, remain in the main Design Process Variable Budget rather than creating an unnecessary option-space model.

---

## 2｜Authority and claim boundary

Before search, resolve:

`CURRENT AUTHORITY → DECISION OBJECT → BASELINE → OPEN VARIABLES → LOCKED VARIABLES → SOURCE-BOUND HARD CONSTRAINTS → SOFT PREFERENCES → UNKNOWN / UNVERIFIED INPUTS → REQUIRED NATIVE OUTPUT → VALIDATION OWNERS`

### Hard rule

A computational search may only be as authoritative as its inputs and evaluation methods.

- Source-backed requirements remain requirements.
- Unknown facts remain `UNKNOWN / UNVERIFIED`.
- A missing value may not silently become a “reasonable default” when it can change feasibility, safety, compliance, capacity or the selected concept family.
- A model assumption may be used for bounded exploration only when labeled and when the output claim remains inside that assumption.
- A solver result cannot elevate an assumption into Source Authority.

When an input is authority-critical and missing:

`MISSING AUTHORITY → HOLD / BOUNDED ASSUMPTION → NO FALSE FEASIBILITY PASS`.

---

## 3｜Search-space contract

Create one machine-readable or tabular record before large-scale generation.

Minimum fields:

`decision_object_id`  
`baseline_artifact_ref`  
`baseline_hash_or_revision`  
`design_question`  
`variables[]`  
`hard_constraints[]`  
`soft_preferences[]`  
`conserved_budgets[]`  
`unknowns[]`  
`generation_method`  
`decoder_or_geometry_method`  
`evaluation_methods[]`  
`diversity_definition`  
`stop_conditions`  
`required_artifact_comparison`  
`validation_handoffs[]`

### Variable record

Each material variable should carry:

`variable_id → semantic meaning → type → domain/range/options → unit → source/authority → OPEN/LOCKED → dependency → invalid values`

Variable types may include:
- continuous parameter;
- discrete parameter;
- categorical choice;
- relation;
- topology;
- sequence/order;
- allocation;
- configuration/state;
- geometry;
- interface permission.

Do not encode the same design decision through several correlated sliders and then count their combinations as independent diversity.

### Domain discipline

For each range or option set, state why the domain exists.

Bad:

`corridor_width = 0.8–3.0 because that gives the solver room`

Better:

`corridor_width domain = bounded by Current requirement/source + project exploration ceiling; values outside are infeasible or unresolved`

The search domain is a design claim. Treat it as reviewable.

---

## 4｜Hard constraints, soft preferences and objectives

Keep these three classes separate.

### A. Hard constraints

Violation makes a candidate infeasible for the current claim.

Examples:
- source-authorized minimum/maximum geometry;
- required adjacency or separation;
- site/buildable envelope;
- required clearance;
- exact capacity;
- no-overlap;
- permitted topology;
- explicit accessibility / safety / code condition when current authority exists;
- immutable product interface;
- fixed project boundary.

Represent:

`constraint_id → source → affected variables/objects → test → PASS/FAIL/UNVERIFIED → failure consequence`

A hard requirement must not be weakened into a weighted penalty just to let an optimizer return more candidates.

### B. Soft preferences

A preference can discriminate feasible candidates but may be traded.

Examples:
- preferred proximity;
- compactness;
- lower circulation;
- daylight preference;
- visual openness;
- service convenience;
- lower cost when cost is not a hard cap.

Represent:

`preference_id → rationale/source → evaluation method → tradeable against → known blind spots`

Do not invent numerical weights merely because an optimizer expects them.

### C. Objectives / signals

An objective is a measured direction in the solution space, not the design goal itself.

Examples:
- minimize energy estimate;
- maximize adjacency satisfaction;
- minimize material mass;
- maximize usable area;
- reduce travel distance.

For every objective state:

`objective_id → design relation represented → metric → method/version → unit/normalization → direction → validity range → proxy limitations`

If the objective is a proxy, name what it does **not** measure.

---

## 5｜Conserved-resource budget

Use this gate whenever one design improvement necessarily consumes a finite total.

General contract:

`TOTAL CAPACITY → BASELINE ALLOCATION → PROPOSED DELTA → DONOR → RECEIVER → RECOMPUTED TOTAL → CONSTRAINT CHECK → ACCEPT / REJECT / HOLD`

Possible budgets:
- gross/net area;
- weight/mass;
- cost;
- power;
- energy;
- thermal capacity;
- storage;
- schedule/time;
- compute budget;
- screen/viewport attention;
- information density;
- staffing/operations capacity.

For every material change record:

`budget_id / total / units / baseline allocations / delta / donor / receiver / resulting allocations / reconciliation result`

Rules:
1. No “free” allocation. An increase must identify what gives way when the total is constrained.
2. A budget total from an assumption remains an assumption.
3. A fixed external percentage or benchmark does not become Current authority automatically.
4. Reconciliation is arithmetic/constraint evidence only; it does not prove design quality.

This generalizes zero-sum programming logic without importing external workplace ratios or fixed area percentages.

---

## 6｜Generation modes

Select the minimum mechanism that matches the problem shape.

### 6.1 Enumeration / combinatorial search

Use when:
- discrete choices are few enough to enumerate;
- every combination can be checked cheaply;
- completeness is valuable.

Record:
- total theoretical combinations;
- combinations pruned before generation and why;
- combinations actually evaluated.

### 6.2 Constraint satisfaction / CP / integer formulation

Use when:
- hard feasibility dominates;
- discrete placements/assignments/adjacencies matter;
- many combinations are invalid.

Typical design objects:
- room allocation;
- component packing;
- interface assignment;
- schedule/configuration;
- routing;
- modular assembly.

Record:
- variables/domains;
- hard constraints;
- solver/algorithm class;
- feasible/infeasible/unknown result;
- repair behavior if geometry is decoded after solving.

### 6.3 Parametric sampling / design of experiments

Use when:
- parameter influence is unknown;
- the space is continuous;
- exhaustive search is impossible;
- the main goal is understanding before optimization.

Possible strategies:
- bounded grid;
- random / stratified sampling;
- Latin-hypercube-like sampling;
- factorial / fractional-factorial-like experiments;
- targeted local samples around a baseline.

Do not overclaim statistical properties unless the actual DOE method and assumptions support them.

### 6.4 Evolutionary / multi-objective search

Use when:
- the space is too large for exhaustive search;
- variables interact nonlinearly;
- multiple objectives conflict.

Required additional records:
- population/initialization strategy;
- mutation/variation logic as applicable;
- evaluation count/budget;
- convergence evidence;
- diversity evidence;
- seed/run identity if stochastic.

A stochastic run without seed/run identity is weaker reproducibility evidence.

### 6.5 Novelty / quality-diversity search

Use when:
- normal optimization collapses into one family;
- discovering materially different behavior/topology matters;
- a single “best” point would hide design strategies.

Define the behavior/niche dimensions before claiming diversity.

Do not call random aesthetic variation “novelty search”.

### 6.6 Surrogate-assisted search

Use when:
- true evaluation is expensive;
- an approximation is needed to guide search.

Required:
- training/evaluation sample identity;
- surrogate target;
- validation error / uncertainty appropriate to the model;
- regions where surrogate use is unsafe;
- final high-value candidates rechecked with the real evaluator.

`SURROGATE PREDICTION ≠ TRUE EVALUATION`.

---

## 7｜Spatial / adjacency / program route

Use this route for architecture, interior, workplace, service-space, campus, site, equipment-room or other layout problems when relationships can be expressed before detailed geometry.

### 7.1 Relationship graph

Represent:

- nodes = rooms/zones/components/functions;
- edges = adjacency, access, containment, separation, visibility, service or another explicit relation;
- edge class = hard / soft / unknown;
- edge source = brief / code / user / specialist / assumption.

Do not collapse “adjacent”, “near”, “visible from”, “connected to” and “contained by” into one generic edge.

### 7.2 Pre-geometry arrangement

Possible representations:
- adjacency matrix;
- bubble / spring diagram;
- topological graph;
- relative-position graph;
- zoning tree;
- allocation grid.

These are relationship prototypes, not professional floor plans.

### 7.3 Geometry decoding

When relations become rooms/regions:

- enforce non-overlap where required;
- enforce site/container boundary;
- reconcile required area/capacity;
- preserve required adjacency/separation;
- record any repair needed after decoding;
- recalculate paths/circulation after geometry changes.

### 7.4 Repair log

Never hide invalid generated geometry by silently “cleaning it up.”

Record:

`candidate_id → invalid condition → repair operation → changed variables/relations → post-repair feasibility → objective values before/after if material`

A candidate heavily repaired after generation is not equivalent to a candidate generated feasibly from the start.

### 7.5 Path and egress-like checks

Route actual regulatory or engineering checks to the proper owner/current source.

The option-space layer may compute graph/path geometry, but:

`SHORTEST PATH COMPUTED ≠ EGRESS / ACCESSIBILITY / CODE PASS`.

---

## 8｜Model preflight before search

Before spending a large evaluation budget, test the model on a small known set.

Required preflight:

1. baseline reconstructs correctly;
2. at least one deliberately feasible configuration passes;
3. at least one deliberately infeasible configuration fails for the right reason;
4. objective direction behaves sensibly on simple perturbations;
5. geometry decoder produces stable identity and units;
6. invalid-candidate rate is measured on a small sample;
7. evaluator/tool versions and source revisions are bound.

If a known bad candidate scores highly, stop and repair the evaluator.

If a large fraction of sampled candidates fail due to decoder/runtime errors, treat that as a search-space/model defect. Do not simply let the solver learn to avoid software crashes.

---

## 9｜Divergence integrity

Computational generation can converge too early just as human ideation can.

### Separate generation from soft judgment

During genuine divergence:

- enforce hard constraints as needed;
- collect candidate identity;
- do not reject every unfamiliar candidate immediately because it looks worse than the baseline;
- defer soft ranking until a meaningful field exists.

This does **not** mean ignoring obvious infeasibility, safety, rights or authority failures.

### Freeze discriminating criteria

Where practical, state the main discriminating criteria and hard gates before final candidate results are visible.

Do not tune a weight after seeing the output solely to make the preferred candidate win.

### Concept-family deduplication

A large candidate count is not broad exploration if all candidates share one topology/architecture.

Define a concept-family key appropriate to the task, such as:
- topology;
- functional allocation;
- circulation model;
- interface model;
- structural system;
- support/posture;
- component architecture;
- behavior niche.

Parameter micro-variation inside one family does not satisfy option-space coverage.

### Coverage record

For each family:

`family_id → structural/material delta → candidates represented → live trade-off → strongest candidate → falsifier / next test`

No fixed number of families is required. Coverage is sufficient when the Decision Question's material trade-offs are represented or explicitly excluded by evidence.

---

## 10｜Invalid-candidate and failure telemetry

Track at minimum:

- total generated;
- valid;
- hard-infeasible;
- evaluator/runtime failed;
- repaired;
- duplicate / same-family collapsed;
- unverified due to missing authority.

Useful ratios are diagnostics, not quality scores.

Examples:
- high hard-infeasible rate may indicate a badly bounded search space;
- high runtime-failure rate indicates tool/model fragility;
- high duplicate rate indicates insufficient diversity or redundant variables;
- high repair rate indicates the decoder does not preserve feasibility.

Do not delete failure data simply because it is not visually presentable.

---

## 11｜Sensitivity before optimization when variables are unclear

If the design has many open variables and their influence is unknown, first ask:

`WHICH VARIABLES ACTUALLY MOVE THE DECISION-RELEVANT OUTPUTS?`

Use bounded sensitivity or screening appropriate to the problem.

Return:
- influential variables;
- weak variables;
- important interactions when observable;
- unstable/uncertain effects;
- variables to lock, narrow, or remove.

Do not optimize 50 variables simply because the model exposes 50 sliders.

A variable that has no meaningful leverage should not remain open merely to inflate the apparent design space.

---

## 12｜Multi-objective / Pareto route

Use when two or more legitimate objectives conflict.

### Pareto semantics

A non-dominated candidate is one for which no other evaluated candidate is at least as good on all current objectives and strictly better on one.

The Pareto set is:

`BEST OBSERVED TRADE-OFF SET UNDER THIS MODEL / SAMPLE / EVALUATION`

It is **not**:
- the professionally approved set;
- a field-verified set;
- a complete mathematical Pareto front unless search completeness justifies that claim;
- a Design KEEP list.

### Weighted-sum boundary

A weighted scalar may be useful for a local experiment, but:

- weights must have an authority/rationale;
- scale/normalization must be explicit;
- a weighted sum can hide non-convex trade-off regions;
- a high scalar score cannot override a hard gate;
- one weighted winner may not replace the trade-off set when materially different objectives exist.

### Representative candidates

For design review, select representative candidates from materially different:
- Pareto regions;
- clusters;
- concept families;
- behavior niches;
- knee/threshold regions when these are analytically meaningful.

Do not present 20 nearly identical points on one local front as 20 design options.

Each representative must carry:
- exact variables;
- objective values;
- feasibility status;
- artifact identity;
- major trade-off;
- known proxy blind spots;
- unresolved qualitative questions.

---

## 13｜Diversity and convergence

A search can improve objective score while becoming less useful for design because diversity collapses.

Track evidence appropriate to the method:

- parameter/genotype diversity;
- geometry/phenotype diversity;
- concept-family count;
- behavior-niche coverage;
- objective-space spread;
- repeated convergence across runs;
- best/average objective trend where relevant.

Stop claiming broad exploration when the population has collapsed into one family.

Premature convergence response may include:
- re-seeding;
- widening a justified variable domain;
- changing search method;
- explicitly maintaining niches;
- revisiting over-dominant objective/constraint encoding.

Do not widen domains beyond authority merely to create prettier diversity.

---

## 14｜Objective / fitness gaming

Every metric is a representation of a design relation. Generated candidates may exploit its blind spots.

Attack each important objective:

`WHAT CAN SCORE WELL WITHOUT ACTUALLY SATISFYING THE DESIGN INTENT?`

Examples:
- centroid distance “adjacency” without useful shared access;
- daylight metric improved by geometry that destroys another use relation;
- circulation minimized by producing operationally poor bottlenecks;
- surface area reduced while service access becomes impossible;
- visual proxy improved while source/evidence legibility collapses.

Required controls:
1. manually inspect known configurations;
2. compare metric result with actual artifact readback;
3. use an orthogonal evaluator for critical top candidates when feasible;
4. record false-positive / false-negative cases;
5. repair the evaluator or narrow its claim ceiling.

`FITNESS PASS ≠ DESIGN RELATION PROVEN`.

---

## 15｜Matched artifact comparison

Text parameter vectors and charts are insufficient for Design Review when the design consequence is spatial, visual, physical or interactive.

For representative candidates, create actual comparable artifacts.

Comparison contract:
- same authoritative content/program/input;
- same target scale or viewport when relevant;
- same camera/projection when comparing geometry where possible;
- same state / scenario / load case as applicable;
- same evidence labels;
- same output fidelity adequate to the Decision Question.

Examples:
- same-scale plan + section;
- same-camera massing views;
- same-state browser prototypes;
- same-scale product orthographic views;
- matched system diagrams.

Keep the strongest rejected alternative when it materially explains the trade-off or reopen condition.

`TEXT CONCEPT LIST ≠ ARTIFACT COMPARISON`.

---

## 16｜Design review after computational filtering

The solver may remove hard-infeasible candidates and organize measurable trade-offs. Design Review remains a separate owner/judgment.

For each representative candidate review:

- Does the artifact carry the intended relation?
- Did the search metric miss a critical use/spatial/form/system consequence?
- Does it introduce a false affordance, false hierarchy or brittle dependency?
- Is the candidate robust enough to continue?
- Which unresolved question could reverse selection?

Use existing OLEANDER:

`KEEP / REVISE / REJECT / HOLD`

Do not invent an “AI score” or let rank order award KEEP.

When a candidate is selected:

`SELECTED CANDIDATE → DESIGN DECISION RECORD → LOCKED VARIABLES → REMAINING OPEN VARIABLES → VALIDATION HANDOFFS → REOPEN TRIGGER`

---

## 17｜Stochastic and run identity

When generation uses randomness, preserve enough identity to reproduce or at least audit the run.

Record as applicable:
- algorithm/method;
- implementation/tool version;
- seed;
- population/sample settings;
- variable schema version;
- objective/evaluator versions;
- source/authority fingerprint;
- run start/end;
- candidate IDs;
- artifact hashes;
- failure counts.

If exact reproducibility is impossible, say so.

A path or screenshot alone is not run identity.

---

## 18｜Change propagation / stale results

A material change to any of these may invalidate prior candidate evaluation:

- source authority;
- hard constraint;
- variable domain;
- geometry decoder;
- objective definition;
- evaluator version;
- normalization;
- budget total;
- baseline;
- unit system;
- performance model;
- specialist input.

Use:

`CHANGE → AFFECTED CANDIDATES → AFFECTED OBJECTIVES / FEASIBILITY → STALE RESULTS → REQUIRED RE-EVALUATION → UPDATED REPRESENTATIVE SET`

Do not preserve an old “best option” after the evaluation problem has materially changed.

---

## 19｜Stop conditions

Stop computational expansion when one or more of these conditions are met and the Decision Question can proceed:

- all material trade-off families have representative candidates or evidence-backed exclusions;
- new samples repeat existing concept families / behavior niches;
- sensitivity shows remaining open variables have low decision leverage;
- Pareto/trade-off structure is stable enough for human review;
- computational/evaluation budget is exhausted and the remaining uncertainty is explicit;
- a decisive proof slice separates the viable alternatives;
- unresolved authority or evaluator validity creates a HOLD that more search cannot solve.

Do not equate “solver converged” with “design decision complete.”

---

## 20｜Required outputs

Return the minimum set relevant to the task:

1. `option_space_contract`
2. `baseline_artifact_identity`
3. `variables_domains_authority`
4. `hard_soft_constraint_separation`
5. `conserved_budget_reconciliation` when applicable
6. `generation_run_identity`
7. `candidate_ledger`
8. `invalid_repair_failure_telemetry`
9. `objective_evaluator_contract`
10. `sensitivity_diversity_convergence` when applicable
11. `pareto_or_tradeoff_set` when applicable
12. `representative_editable_artifacts`
13. `matched_comparison_readback`
14. `design_review_disposition`
15. `strongest_rejected_alternative` when material
16. `validation_handoffs`
17. `reopen_trigger`
18. `claim_ceiling`

---

## 21｜Owner routing

This extension remains inside `oleander-design-process`.

Route rather than absorbing specialist authority:

- source / current evidence → `oleander-research`;
- native CAD / parametric geometry / model identity → `oleander-3d-pipeline`;
- structural, environmental, MEP, code, safety or specialist calculations → relevant VALIDATION owner;
- visual composition / comparative presentation → `oleander-visual-design`;
- interaction/runtime prototypes → relevant web/UI or digital-product owner;
- released artifact/file/package integrity → `oleander-delivery-qc`.

A computational solver, spreadsheet, Grasshopper/Dynamo definition, Python optimizer or third-party platform is a tool surface. It does not become a Project authority owner.

---

## 22｜External mechanism digestion boundary

Mechanisms studied include:
- rule / graph / constraint-based design automation;
- program adjacency and resource allocation;
- parametric and multi-objective design-space exploration;
- Pareto / diversity / convergence reasoning;
- divergence-convergence separation;
- matched artifact comparison;
- architecture/product/UI multi-concept review.

Accepted into this extension:
- explicit search-space contract;
- hard/soft/objective separation;
- candidate identity and exact parameter binding;
- conserved-resource reconciliation;
- invalid/repair telemetry;
- sensitivity before over-optimization;
- diversity/convergence as design-space integrity;
- Pareto set as trade-off evidence, not winner;
- objective-gaming checks;
- matched representative artifact review;
- fail-closed unknown/source behavior.

Not transferred as OLEANDER defaults:
- fixed office/program percentages;
- fixed circulation ratio;
- fixed room sizes detached from Current source;
- fixed concept counts such as 3, 8 or 20;
- weighted Pugh/score matrix as automatic selection;
- any specific solver/vendor/tool as mandatory;
- optimization score as Design KEEP;
- taste-memory bias across unrelated projects;
- palette/font/layout difference as proof of concept diversity;
- silent default substitution for missing authority.

No external source code is required by this extension.

---

## 23｜Maturity

Current maturity on creation:

`CANDIDATE EXTENSION / EXISTING OWNER / EXTERNAL MECHANISMS DIGESTED / GOLDEN REGRESSION REQUIRED / NO REAL PROJECT USAGE / NO CROSS-CONTEXT EVIDENCE / NO PROMOTION`

Promotion requires real project reapplication showing that the extension changes an actual design decision, includes at least one non-success/failure path or invalid candidate, preserves source/technical boundaries, and improves option-space quality without becoming process overhead.

`SEARCH COMPLETE ≠ DESIGN COMPLETE`.
