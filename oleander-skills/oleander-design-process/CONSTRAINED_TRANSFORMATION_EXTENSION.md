# OLEANDER Constrained Transformation Extension

Status: `CANDIDATE EXTENSION / EXISTING DESIGN OWNER / EXTERNAL-MECHANISM DIGESTED / EXISTING-PROJECT REPAIR COMPANION / C04 PROJECT REPLAY EVIDENCE / GOLDEN REGRESSION ADDED / NO CROSS-CONTEXT EVIDENCE / NO PROMOTION`

Owner: `oleander-design-process`

Primary companion: `EXISTING_PROJECT_REPAIR_EXTENSION.md`

Related owners:
- `FUNCTION_TO_CONCEPT_SYNTHESIS_EXTENSION.md`
- `COMPUTATIONAL_OPTION_SPACE_EXTENSION.md`
- `SYSTEM_INTERFACE_COUPLING_EXTENSION.md`
- professional-domain processes when technical ownership is triggered.

Purpose: generate materially different, bounded design candidates by transforming an already-known component / relation / state system without reopening unrelated design variables or inventing unsupported external resources.

Core chain:

`CURRENT / BASELINE → CONSTRAINT-WORLD MAP → PROTECTED INVARIANTS → ONE STRUCTURAL TRANSFORMATION → VIRTUAL CONFIGURATION → CONSEQUENCE / VALUE HYPOTHESIS → ARTIFACT DELTA → READBACK → KEEP / REVISE / REJECT / HOLD`.

This extension is a **technique pack inside the existing Design Process**. It is not:
- a new lifecycle;
- a new Core Skill;
- a brainstorming quota;
- a formal Systems Engineering Functional Architecture;
- a substitute for professional-domain feasibility;
- a license to reopen a mature Current object without a Decision Question.

---

## 1｜When to trigger

Use when all are true:

1. a real object/system/service/spatial arrangement already exists as Current, Best Existing or bounded baseline;
2. its components, relations, states or interfaces can be named;
3. the design question allows some structural reconfiguration;
4. the team needs alternatives that differ by causal arrangement, not by styling;
5. preserving existing authority / protected relations matters.

Typical triggers:
- an existing product/system is over-complex and may contain removable components;
- one component may carry more than one role;
- one component/process may need spatial/temporal/functional division;
- a duplicated but differentiated element may create resilience or a new use relation;
- two variables may need a new dependency, or a harmful dependency may need to be broken;
- an existing project repair has a DESIGN LOGIC blocker and more than one plausible structural repair exists.

Do **not** trigger when:
- the problem is still “what functions must exist / which causal means can realize them?” → use Function → Concept Synthesis;
- the primary question is parametric/continuous optimization → use Computational Option Space;
- the repair is local and the correct delta is already known → use Existing Project Repair without this pack;
- technical feasibility is the material question → route to the professional owner;
- source/current authority is too unresolved to identify the baseline and protected relations;
- the desired change is only color/material/style/presentation.

---

## 2｜External mechanism digestion boundary

Research reference:
- `thinkbigleaders/claude-innovation-skills` at commit `5678aa37c0874c09d7a8b24dd5e0a239854fdfcb`;
- root license: MIT;
- reviewed `ideation-sit/SKILL.md`, `ideation-sit/references/sit-framework.md`, `variable-dependency/SKILL.md`.

Useful mechanisms:
- constrained search inside an already-known component/environment system;
- remove;
- duplicate and differentiate;
- divide/resequence;
- give an existing component another role;
- create or break dependency between variables;
- generate configuration first, then ask what consequence/value it could create.

Rejected external defaults:
- fixed idea counts such as 25–40+;
- “quantity over quality” as OLEANDER divergence evidence;
- treating the closed world as inherently feasible;
- treating external environment/user characteristics as free design resources without evidence/authority;
- generic weighted idea scoring;
- “function follows form” as a universal design direction;
- delaying all feasibility/authority checks until after ideation;
- treating every strange virtual product as a concept candidate.

OLEANDER translation:

`CONSTRAINED TRANSFORMATION ≠ UNBOUNDED BRAINSTORMING`.

`CONFIGURATION-FIRST MAY BE USED AS AN OPTIONAL IDEATION MOVE; IT DOES NOT OVERRIDE INTENT / EVIDENCE / RIGHTS / SAFETY / PROFESSIONAL AUTHORITY`.

---

## 3｜Constraint-world contract

Before transforming, bind the actual design world.

Record:

`world_id / object_id / baseline_ref / current_or_best_existing / internal_components / immediate_external_context / current_relations / current_states / current_interfaces / protected_invariants / open_design_variables / authority_refs / claim_ceiling`.

### 3.1 Internal components

Elements actually controlled by the design object:
- physical components;
- spatial zones;
- surfaces/openings;
- UI components;
- service touchpoints;
- information/data objects;
- process steps;
- media/carriers;
- state handlers;
- material layers;
- channels.

### 3.2 Immediate external context

Elements that interact with the object but are not controlled by it:
- user/body;
- climate/weather;
- site condition;
- existing infrastructure;
- operating organisation;
- device/network;
- adjacent building/system;
- regulation/authority.

External context is **not automatically available as a resource**.

Every material external variable used in a transformation must carry:

`context_item → evidence_state → owner / authority → allowed design use → unresolved risk`.

Examples:
- “sunlight exists” does not prove solar availability at the target location;
- “users have phones” does not prove reliable connectivity;
- “staff exists” does not prove staffing capacity;
- “existing railing exists” does not prove structural capacity.

### 3.3 Protected invariants

Before divergence, state what the transformation may not silently break.

Possible protected dimensions:
- source truth;
- route/safety/return relation;
- accessibility;
- privacy/rights;
- structural load path;
- fire/life safety;
- maintenance;
- user task;
- content authority;
- Current state model;
- object identity;
- field/claim ceiling.

`TRANSFORMATION FREEDOM ≠ AUTHORITY FREEDOM`.

---

## 4｜Transformation record

Every material move is one auditable record:

`transformation_id / baseline_object_id / operator / target_components_or_variables / protected_invariants / exact_delta / resulting_configuration / causal_change / hypothesized_value_or_design_consequence / affected_functions / affected_relations / affected_interfaces / affected_states / new_dependencies / removed_dependencies / unknowns / failure_conditions / artifact_required / specialist_handoffs / disposition`.

A transformation is not counted as a design candidate until a decision-relevant artifact/readback exists.

---

# 5｜Operator A — REMOVE

Question:

> What happens if one apparently necessary component / step / layer / control / carrier is removed?

Required sequence:

1. name the target;
2. identify every function/role currently carried by it;
3. remove it in the model/artifact;
4. trace lost functions and interfaces;
5. decide whether they:
   - disappear legitimately;
   - are reallocated;
   - become an unacceptable loss;
6. construct the transformed artifact;
7. read back the protected invariants.

Record:

`removed_component → lost_functions → reallocated_to → new_absence → simplification_gain → new_failure → verdict`.

Hard attacks:
- subtraction merely hides the component instead of removing the responsibility;
- a safety/service/recovery role disappears because it was “secondary”;
- removed functionality is silently pushed to a user/operator without authority;
- apparent simplification creates external operational burden;
- one interface disappears visually but persists technically.

`FEWER COMPONENTS ≠ BETTER DESIGN`.

---

# 6｜Operator B — DUPLICATE + DIFFERENTIATE

Question:

> What changes if an existing component is duplicated but the copy has a materially different role, state, location, scale, orientation or timing?

Required sequence:

1. identify original component and role;
2. create one bounded copy;
3. define the exact differentiating variable;
4. identify new relationship between original and copy;
5. test whether the duplicate creates:
   - useful redundancy;
   - specialization;
   - scale transition;
   - parallel use;
   - conflicting authority;
   - duplicated maintenance/operation;
6. construct/read back at matched fidelity.

Record:

`original → duplicate → differentiating_attribute → new_relation → new_value → duplication_cost → truth/authority risk → verdict`.

Hard attacks:
- duplicate is visually different but causally identical;
- duplicate creates two Current truth sources;
- redundant controls diverge in state;
- duplicated physical element creates maintenance or clutter without material benefit;
- variant count is mistaken for concept diversity.

---

# 7｜Operator C — SPLIT + RESEQUENCE

Question:

> What changes if a component/process/space is divided and its parts are separated spatially, temporally or functionally?

Split types:
- spatial;
- temporal;
- functional;
- informational;
- state-based;
- responsibility-based.

Required sequence:

`whole → split basis → parts → new order/location/ownership → handoffs → continuity risk → artifact delta → readback`.

Check:
- what used to be simultaneous but becomes sequential;
- what used to be co-located but becomes distributed;
- what handoff is newly introduced;
- what state/data/context must survive across the split;
- whether reassembly/recovery is possible.

Hard attacks:
- split creates a hidden handoff with no owner;
- repeated context entry increases user/operator burden;
- split breaks accessibility/wayfinding/task continuity;
- split creates two unsynchronised sources of truth;
- modularity claim is only a visual grid change.

---

# 8｜Operator D — REASSIGN ROLE

Question:

> Can an existing component legitimately carry an additional or different role?

Required sequence:

`component → current role → proposed role → shared means → capacity/conflict → failure coupling → service consequence → artifact/readback`.

Check:
- capacity;
- simultaneous demand;
- role conflict;
- failure coupling/common-mode failure;
- discoverability/affordance;
- access/service;
- owner/permission;
- state conflict.

Hard attacks:
- “one component does more” is treated as automatic efficiency;
- new role hides specialist workload;
- a visual element is given a safety function it cannot actually perform;
- a user-generated artifact is reassigned as public/marketing content without rights;
- one component becomes a single point of failure.

`TASK UNIFICATION ≠ FREE MULTIFUNCTIONALITY`.

---

# 9｜Operator E — CREATE / BREAK DEPENDENCY

Question:

> What value or risk appears if one variable begins to vary with another, or if an existing dependency is removed?

Record each variable:

`variable_id / owner / domain / range_or_states / evidence_state / controllability / observability / update_source`.

Dependency record:

`dependency_id / driver_variable / response_variable / relation_type / direction / states_or_function / data_or_sensing_need / failure_default / override / evidence / privacy_or_safety_consequence`.

Possible relation types:
- threshold;
- stepped;
- categorical/state mapping;
- continuous/monotonic;
- inverse;
- hysteresis;
- break existing link.

Required attacks:
- driver variable cannot actually be sensed/known;
- external variable is unauthoritative;
- false precision;
- feedback loop/oscillation;
- privacy/surveillance consequence;
- safety-critical response has no fail-safe;
- two axes that must remain independent are accidentally collapsed;
- manual override/UNKNOWN state is omitted.

`DEPENDENCY CREATED ≠ CONTROL LOGIC VERIFIED`.

When the relation becomes a parametric/search problem, hand it to `COMPUTATIONAL_OPTION_SPACE_EXTENSION.md`.

---

## 10｜Configuration-first consequence discovery

After a structural move is created, ask:

`WHAT NEW CONSEQUENCE / USE / RELATION COULD THIS CONFIGURATION ENABLE?`

But classify the answer:

- `SUPPORTED CONSEQUENCE` — directly supported by known project evidence;
- `DESIGN HYPOTHESIS` — plausible but untested;
- `NEW USER/OPERATION HYPOTHESIS` — requires research/operations evidence;
- `TECHNICAL HYPOTHESIS` — requires specialist proof;
- `RIGHTS/AUTHORITY HYPOTHESIS` — cannot proceed without authorization.

Do not convert a surprising configuration into a new user need, field fact or technical capability.

`VIRTUAL CONFIGURATION → VALUE HYPOTHESIS`, not `VIRTUAL CONFIGURATION → FACT`.

---

## 11｜Candidate-retention gate

A transformed result may remain a design candidate only if:

1. the baseline and exact transformation are traceable;
2. all protected invariants were attacked;
3. essential roles/functions are either preserved, deliberately removed or visibly reallocated;
4. new interfaces/dependencies are explicit;
5. unknowns and specialist handoffs are explicit;
6. it differs materially from the baseline in topology / role allocation / state / dependency / interface / sequencing;
7. it has an editable or native decision-relevant artifact at matched fidelity;
8. it has at least one falsifier or failure condition;
9. its claim ceiling does not exceed evidence;
10. it survives Existing Project Repair regression against Best Existing where applicable.

Rejected or dead transformations are evidence. Do not delete them merely to make the option set look successful.

---

## 12｜Transformation family deduplication

Do not count these as separate structural transformations:
- color/material-only change;
- font/icon-only change;
- small dimension tuning;
- same component copied with no role/state difference;
- identical dependency expressed with different labels;
- same split with cosmetic rearrangement;
- one operator applied repeatedly without a new causal consequence.

Group by:

`PRIMARY STRUCTURAL DELTA / CAUSAL CHANGE / NEW OR REMOVED RELATION / INTERFACE CONSEQUENCE`.

There is no target idea count.

---

## 13｜Integration with Existing Project Repair

When used inside repair:

`BEST EXISTING → FAILURE CLASS → PROTECTED DIMENSIONS → TRANSFORMATION SET → MATCHED ARTIFACT DELTAS → READBACK → REGRESSION CHECK → KEEP / REVISE / ROLLBACK`.

Rules:
- same Object ID;
- no unrelated redesign;
- Best Existing remains rollback baseline;
- only material transformations survive;
- new candidate does not become Current by generation;
- repair review remains comparative.

Use when a DESIGN LOGIC failure has genuine structural freedom.

Do not trigger merely to “be creative” after a clear repair is already known.

---

## 14｜Integration with Function → Concept Synthesis

Use Function → Concept first when:
- functions are open;
- causal means are open;
- concept families do not yet exist.

Use Constrained Transformation when:
- a baseline architecture exists;
- component/relationship system is known;
- the question is how to structurally mutate it.

A transformed configuration may expose:
- a new function hypothesis;
- shared means;
- missing function;
- changed allocation.

If that becomes material, route back through the Function → Concept owner rather than silently rewriting the function model.

---

## 15｜Integration with professional domains

A transformation can generate a candidate but cannot self-certify:
- structural capacity;
- fire/life safety;
- accessibility;
- drainage;
- lighting;
- MEP;
- security/privacy;
- human factors;
- manufacturing;
- field feasibility.

Example:

`REMOVE SUPPORT → NEW CANTILEVER CONFIGURATION`

is a Design candidate, not Structural PASS.

---

## 16｜Required native outputs

When triggered materially, produce as applicable:

1. `constraint_world_register`
2. `protected_invariant_register`
3. `component_relation_map`
4. `transformation_ledger`
5. `dependency_change_ledger`
6. `role_reallocation_ledger`
7. `transformed_candidate_ledger`
8. `rejected_transformation_ledger`
9. `matched_transformation_artifacts`
10. `readback_and_regression_results`
11. `specialist_handoffs`
12. `design_review_disposition`
13. `reopen_trigger`

---

## 17｜Failure attacks

Mandatory attacks include:

### FT-01 Component-list theatre
A component inventory exists, but transformations are not constructed.

### FT-02 Hidden function deletion
Removal deletes a service/safety/recovery role without disposition.

### FT-03 External-resource smuggling
A transformation relies on staff, data, site condition, user behaviour or infrastructure that is not authoritative/available.

### FT-04 Multifunction overload
Role reassignment creates capacity conflict/common-mode failure.

### FT-05 Split-handoff loss
Division creates a new handoff but no state/data/owner continuity.

### FT-06 Dependency fantasy
A new dependency relies on a driver variable that is not observable/authoritative.

### FT-07 Axis collapse
Two dimensions that must remain independent are merged into one state mapping.

### FT-08 Variant theatre
Cosmetic/parameter changes are counted as structural concepts.

### FT-09 Quantity theatre
Idea count is treated as divergence quality.

### FT-10 Configuration-as-fact
A surprising virtual configuration is treated as a user need, technical truth or field fact.

### FT-11 Best-existing regression
A transformed candidate is novel but weaker than the mature baseline in the decision-relevant dimension.

### FT-12 Current-by-generation
A generated transformation silently replaces Current before matched artifact/readback/review.

---

## 18｜Review questions

Independent Design Review should ask:

1. What exact baseline component/relation changed?
2. Which operator created the candidate?
3. What protected invariants were attacked?
4. What function/role moved or disappeared?
5. What new dependency/interface/handoff exists?
6. What evidence supports the claimed benefit?
7. What remains a hypothesis?
8. Does the candidate differ causally or only visually?
9. Is the artifact fidelity matched to the baseline/other candidates?
10. What would falsify this candidate?
11. What professional owner must validate it?
12. Should the transformation be KEEP / REVISE / REJECT / HOLD?

---

## 19｜C04 project replay evidence｜2026-09-19

A bounded retrospective replay was run against the mature C04 digital companion.

Current authority preserved:
- `TODAY / ROUTE / READ / MY BOOK` plus parallel `SERVICE / RETURN`;
- `NORMAL / DEGRADED / CLOSED / UNKNOWN`;
- `FULL / LIGHT / OFF`;
- Return/offline/no-phone/fail-closed boundaries;
- field and live-browser HOLDs.

Five transformation runs were classified:

- `CTR-01 REMOVE` top-level READ → retained as `READLESS_CONTEXTUAL_REVEAL` alternative / HOLD;
- `CTR-02 DUPLICATE+DIFFERENTIATE` dedicated top-level Return → REJECT because route/return truth is duplicated and must remain synchronized;
- `CTR-03 CREATE DEPENDENCY` reality-state → content-intensity → REJECT because Current explicitly requires those axes to remain independent;
- `CTR-04 REASSIGN ROLE` Route carries return-purpose mode → baseline reconstruction, not a new candidate;
- `CTR-05 BREAK DEPENDENCY` route/return independent from content completion → baseline reconstruction, not a new candidate.

Deduplication result:

`5 OPERATOR RUNS → 1 RETAINED NEW STRUCTURAL ALTERNATIVE + 2 REJECTED + 2 CURRENT RECONSTRUCTIONS`.

Matched artifact:

`C04_E_CONSTRAINED_TRANSFORMATION_MATCHED_v0.1.svg`.

Actual render readback first failed because the SVG contained an unescaped `&`. The editable SVG was repaired to `&amp;` and rerendered.

Second render:
- `PASS_SUPPORT`;
- 1800×1120;
- Current and CTR-A shown at matched schematic fidelity;
- rejected transformations remain directly readable;
- no clipping/overlap observed.

The replay is retrospective/non-blind and therefore does not reselect C04 E. HCD usability, accessibility, actual live browser and field evidence remain open.

## 20｜Maturity

Current maturity:

`CANDIDATE EXTENSION / EXISTING DESIGN OWNER / EXTERNAL SIT MECHANISMS DIGESTED / ONE C04 RETROSPECTIVE REPLAY / ONE RETAINED STRUCTURAL ALTERNATIVE / TWO PROTECTED-INVARIANT REJECTIONS / MATCHED EDITABLE ARTIFACT + ACTUAL RENDER READBACK / GOLDEN REGRESSION ADDED / NO CROSS-CONTEXT EVIDENCE / NO PROMOTION`.

Further promotion requires:
- cross-context use outside the C04 digital-companion family;
- at least one live or pre-Current use where the technique materially improves a consequential design decision;
- evidence that constrained transformation adds useful structural diversity without causing over-redesign or protected-invariant loss;
- continued separation from technical/professional approval and human/user validation.

`STRUCTURAL TRANSFORMATION ≠ TECHNICAL FEASIBILITY`.

`NOVELTY ≠ DESIGN QUALITY`.

`IDEA COUNT ≠ OPTION-SPACE QUALITY`.
