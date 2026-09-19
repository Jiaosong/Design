# 2026-09-19｜Constrained Transformation / SIT Digestion

Status: `DIGESTED / EXISTING DESIGN OWNER / EXISTING-PROJECT REPAIR COMPANION / C04 RETROSPECTIVE REPLAY COMPLETE / GOLDEN REGRESSION ADDED / NO PROMOTION`

## Question

OLEANDER already had strong mechanisms for:
- open concept generation;
- function → means → concept architecture;
- computational option spaces;
- Existing Project Repair;
- Best Existing First;
- matched candidate artifacts;
- Design Review and specialist handoffs.

The remaining gap was narrower:

> When a mature/bounded object already exists, how can DESIGN systematically generate structurally different alternatives without reopening the whole project or importing unrelated resources?

Accepted execution chain:

`CURRENT / BASELINE → CONSTRAINT-WORLD MAP → PROTECTED INVARIANTS → ONE STRUCTURAL TRANSFORMATION → VIRTUAL CONFIGURATION → CONSEQUENCE / VALUE HYPOTHESIS → MATCHED ARTIFACT DELTA → READBACK / REGRESSION → KEEP / REVISE / REJECT / HOLD`.

This is implemented as:

`oleander-skills/oleander-design-process/CONSTRAINED_TRANSFORMATION_EXTENSION.md`

It remains inside `oleander-design-process`.

No new Core Skill or lifecycle was created.

---

# External source reviewed

Repository:

`thinkbigleaders/claude-innovation-skills`

Pinned commit:

`5678aa37c0874c09d7a8b24dd5e0a239854fdfcb`

License:
- MIT.

Reviewed:
- `ideation-sit/SKILL.md`
- `ideation-sit/references/sit-framework.md`
- `variable-dependency/SKILL.md`
- root README / license.

## Useful mechanisms

The repository presents a constrained ideation approach using an existing product/service system and several structural operators.

Transferable mechanisms:
- constrain search to known components and immediate context;
- remove a component;
- duplicate and differentiate;
- split/resequence;
- assign an additional/different role to an existing component;
- create or break a dependency between variables;
- construct a configuration first and ask what value/consequence it could enable;
- separate generation from later evaluation.

## Rejected defaults

Not absorbed:
- fixed “25–40+ ideas” target;
- “quantity over quality” as evidence of option-space quality;
- assumption that a bounded/closed world is inherently feasible;
- treating users/weather/infrastructure as free design resources merely because they exist in the environment;
- generic multi-criteria scoring as OLEANDER selection authority;
- universal Function-Follows-Form direction;
- postponing all authority/feasibility checks until after idea generation;
- counting every operator result as a viable concept.

OLEANDER translation:

`CONSTRAINED SEARCH ≠ UNBOUNDED BRAINSTORMING`.

`OPERATOR APPLICATION ≠ CANDIDATE`.

`CONFIGURATION-FIRST ≠ FACT-FIRST OVERRIDE`.

---

# Existing owner map

## Existing Project Repair

Already owns:
- same-object identity;
- Best Existing First;
- minimum repair delta;
- repair classification;
- actual artifact repair;
- rollback;
- regression check;
- dependency/change propagation.

Material gap:
- it did not prescribe a structured way to generate several causal repair candidates when DESIGN LOGIC is open.

New extension is therefore a **technique companion**, not a replacement.

## Function → Concept Synthesis

Already owns:
- solution-neutral functions;
- function dependency;
- solution principles;
- compatibility;
- causal concept families.

Boundary:
- use Function → Concept when the architecture is still open at the function/means level;
- use Constrained Transformation when a baseline component/relation architecture already exists.

## Computational Option Space

Already owns:
- variables/domains/constraints;
- computational search;
- invalid/repair telemetry;
- Pareto/decision corridor;
- matched candidate comparison.

Boundary:
- a transformed dependency can later become computational when its variable/domain relation is explicit.

## Professional domains

Constrained Transformation may generate a design candidate.

It cannot self-certify:
- structure;
- fire/life safety;
- accessibility;
- MEP;
- drainage;
- lighting;
- privacy/security;
- human factors;
- manufacturing;
- field truth.

---

# Accepted OLEANDER operator vocabulary

Rather than importing an external methodology name as a new authority, the execution extension uses five explicit design operators:

## A — REMOVE

Remove a component/step/layer/control/carrier.

Required:
- role/function inventory first;
- lost-function disposition;
- reallocation if any;
- protected-invariant attack;
- actual artifact delta.

Failure pattern:
`REMOVE COMPONENT → HIDDEN RESPONSIBILITY DISAPPEARS`.

## B — DUPLICATE + DIFFERENTIATE

Duplicate an existing component and materially differentiate role/state/location/scale/orientation/timing.

Required:
- exact differentiating variable;
- new relation;
- synchronization/authority risk;
- maintenance/service consequence.

Failure pattern:
`DUPLICATE UI/OBJECT → TWO TRUTH SOURCES`.

## C — SPLIT + RESEQUENCE

Divide a whole spatially, temporally, functionally, informationally or by state/responsibility.

Required:
- handoff;
- context/state continuity;
- reassembly/recovery;
- access/wayfinding consequence.

Failure pattern:
`MODULARITY → HIDDEN HANDOFF LOSS`.

## D — REASSIGN ROLE

Give an existing component another/changed role.

Required:
- capacity;
- role conflict;
- common-mode failure;
- service/access;
- owner/permission;
- state conflict.

Failure pattern:
`ONE COMPONENT DOES MORE → SINGLE POINT OF FAILURE`.

## E — CREATE / BREAK DEPENDENCY

Create or remove a relation between variables.

Required per variable:
- owner;
- range/states;
- evidence state;
- controllability;
- observability;
- update source.

Required per dependency:
- driver;
- response;
- relation type;
- data/sensing need;
- failure default;
- override;
- evidence;
- privacy/safety consequence.

Failure pattern:
`SMART ADAPTATION → DRIVER VARIABLE IS NOT ACTUALLY KNOWN`.

---

# Authority correction

External “Closed World” examples often treat environment variables as ideation material.

OLEANDER adds:

`EXTERNAL CONTEXT EXISTS ≠ DESIGN MAY USE IT AS AN AUTHORITATIVE RESOURCE`.

Example:
- weather may exist but current weather feed may not;
- visitor fatigue may exist but may not be measured;
- staff may exist but staffing capacity may be unverified;
- a railing may exist but structural capacity may be unknown.

Therefore every material external variable used in a transformation must carry:
- evidence state;
- owner/authority;
- allowed design use;
- unresolved risk.

---

# Configuration-first value boundary

After a transformation:

`WHAT NEW CONSEQUENCE / USE / RELATION COULD THIS CONFIGURATION ENABLE?`

Classify the answer:
- SUPPORTED CONSEQUENCE;
- DESIGN HYPOTHESIS;
- NEW USER/OPERATION HYPOTHESIS;
- TECHNICAL HYPOTHESIS;
- RIGHTS/AUTHORITY HYPOTHESIS.

Do not promote:
- surprising configuration → user need;
- adaptive idea → live-system capability;
- physical reconfiguration → structural feasibility;
- reused user content → publication/commercial rights.

---

# C04 retrospective replay

Target:

`C04 E / Digital Companion / APP_GAME_MAP v1.2 + CH11 + Digital-Off Contract`

Replay boundary:
- retrospective;
- non-blind;
- E not restarted;
- Current authority not reopened;
- FIELD_OBSERVED=0;
- FIELD_MEASURED=0;
- G1F HOLD;
- actual live browser remains HOLD;
- HCD usability/accessibility NOT_RUN.

## Protected invariants

- UNKNOWN never appears normal/open;
- offline ≠ degraded;
- reality state and content intensity remain separate axes;
- Return may overlay NORMAL/DEGRADED/UNKNOWN;
- CLOSED requires bypass/reroute/exit;
- optional depth closes before route/safety/return;
- digital not required for route;
- digital not required for return;
- no pseudo-live status;
- relational/NTS map ≠ survey;
- MY BOOK ≠ completion score.

## Five transformation runs

### CTR-01 — REMOVE top-level READ

Delta:
- remove READ from top-level navigation;
- preserve optional R01–R13 content through contextual TODAY/ROUTE scene entry.

New family:
`READLESS_CONTEXTUAL_REVEAL`.

Potential gain:
- less top-level digital attention;
- stronger “visit first, read when relevant” relationship.

Main risk:
- deep independent browsing may become less discoverable.

Disposition:
`RETAINED ALTERNATIVE / HOLD`.

No Current reopening.

### CTR-02 — DUPLICATE RETURN

Delta:
- add a dedicated top-level RETURN while retaining Route-return mode and Service/Return.

Result:
- route/return truth appears on multiple overlapping surfaces.

Disposition:
`REJECT`.

Reason:
- synchronization;
- duplicated authority;
- maintenance burden;
- unclear truth owner.

### CTR-03 — CREATE DEPENDENCY reality-state → content-intensity

Proposed mapping:
- NORMAL → FULL
- DEGRADED → LIGHT
- CLOSED/UNKNOWN → OFF

Disposition:
`REJECT`.

Reason:
Current explicitly requires the two axes to remain independent.

Examples that must remain possible:
- NORMAL × OFF;
- DEGRADED × LIGHT;
- UNKNOWN × OFF.

This replay proves an important failure attack:

`NEW DEPENDENCY MAY REDUCE COMPLEXITY WHILE DESTROYING AN INTENTIONAL INDEPENDENCE`.

### CTR-04 — REASSIGN ROLE to Route

Route also carries a Return-purpose mode.

Disposition:
`BASELINE RECONSTRUCTION / NOT NEW CANDIDATE`.

Finding:
- one map carrier can legitimately serve journey + return without creating another truth source.

### CTR-05 — BREAK DEPENDENCY between content completion and route/return

Disposition:
`BASELINE RECONSTRUCTION / NOT NEW CANDIDATE`.

Finding:
- Current already deliberately breaks gamification/completion dependence from route/safety/return.

## Dedup result

`5 OPERATOR RUNS`
→ `1 RETAINED NEW STRUCTURAL ALTERNATIVE`
+ `2 REJECTED TRANSFORMATIONS`
+ `2 CURRENT RECONSTRUCTIONS`.

No cosmetic variants counted.

No idea quantity used as quality.

---

# Matched artifact and actual render readback

Produced:

`C04_E_CONSTRAINED_TRANSFORMATION_MATCHED_v0.1.svg`

It shows:
- Current baseline;
- CTR-A retained alternative;
- CTR-02 rejection;
- CTR-03 rejection.

First actual render:
`FAIL`.

Reason:
- raw `&` in SVG text caused XML parse failure.

Repair:
- `& → &amp;`.

Second actual render:
`PASS_SUPPORT`.

Rendered:
- 1800×1120;
- PNG bytes: 116004;
- SHA256: `a342613a99fd939f79c4e9c7668921dc062772e782b020d4e7e8572111a64ad6`.

Readback:
- Current and alternative have matched schematic fidelity;
- rejected reasons are legible;
- no clipping/overlap after repair.

This is only visual/readability support.

It does not prove:
- usability;
- accessibility;
- live runtime;
- field status;
- superiority of CTR-A.

---

# Golden regression

Added:

## SK-DES-025
Removal silently deletes return/recovery/unknown-state responsibility.

## SK-DES-026
Role unification creates overload/common-mode failure/single point of failure.

## SK-DES-027
Adaptive dependency relies on unauthoritative/unobservable external variables or collapses independent axes.

## SK-DES-028
Idea count/cosmetic variants/novelty are used as option-space quality or Current promotion.

---

# Capability integration

Existing owner:

`oleander-design-process`.

Added native outputs:
- constraint_world_register;
- protected_invariant_register;
- component_relation_map;
- transformation_ledger;
- dependency_change_ledger;
- role_reallocation_ledger;
- transformed_candidate_ledger;
- rejected_transformation_ledger;
- matched_transformation_artifacts;
- readback_and_regression_results.

Added gate:

`constrained_transformation_when_triggered`.

Added implementation path:

`oleander-skills/oleander-design-process/CONSTRAINED_TRANSFORMATION_EXTENSION.md`.

No new Skill.

---

# Maturity

Current evidence:

`CANDIDATE EXTENSION / ONE C04 RETROSPECTIVE REPLAY / ONE RETAINED STRUCTURAL ALTERNATIVE / TWO PROTECTED-INVARIANT REJECTIONS / MATCHED EDITABLE ARTIFACT + ACTUAL RENDER READBACK / NO CROSS-CONTEXT EVIDENCE / NO PROMOTION`.

Remaining before stronger maturity:
- cross-context use;
- at least one pre-Current/live design use that materially changes a consequential decision;
- evidence that it adds option diversity without causing over-redesign;
- continued professional/specialist boundaries.

`STRUCTURAL TRANSFORMATION ≠ TECHNICAL FEASIBILITY`.

`NOVELTY ≠ DESIGN QUALITY`.

`IDEA COUNT ≠ OPTION-SPACE QUALITY`.
