# 2026-08-28｜Design Process / Option Generation / L5｜Functional Allocation Before Selection

STATUS: `TRAINING_MODE / PRACTICE_EVIDENCE / EXTERNAL-SOURCE-CALIBRATED / NO_PROJECT_USAGE / NO_PROMOTION`

## GAP

Current `oleander-design-process` already owns option generation, deletion tests and product/spatial/system reasoning. Recent Practice evidence has focused on:
- service/system state → spatial consequence;
- system state → physical-interface permission;
- design ↔ validation interface change control.

A remaining promotion gap is **option-space quality before selection**: an A/B set can look diverse while all alternatives preserve the same functional allocation and differ only in shell/CMF/styling.

This run asks whether the option set contains materially different architectures before any preferred concept or weighted evaluation is introduced.

## EXISTING-FIRST SOURCE

Internal Current:
- `oleander-skills/oleander-design-process/SKILL.md`;
- `oleander-skills/SKILL_REGISTRY_v1.1.json`;
- `oleander-skills/REVIEW.md`;
- `00-governance/OLEANDER_WORK_COORDINATION_CONTRACT_v1.0.md`;
- `00-governance/OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT.json`;
- `00-governance/OLEANDER_HUMAN_PROFESSIONAL_VOICE_POLICY_v1.0.md`.

Current Priority Queue is empty; this run is Practice/Candidate frontier only.

## EXTERNAL DISCOVERY

### Source 1
**NASA — Design Solution Definition, Section 4.4**  
Institution: National Aeronautics and Space Administration  
URL: https://www.nasa.gov/reference/4-4-design-solution-definition/  
Page last updated: 2023-07-26  
Accessed: 2026-08-28

What it adds:
- alternative design solutions should be formed before the preferred solution is baselined;
- alternatives can arise from different functional allocations and subsystem integrations;
- plausible alternatives should cover a sufficiently broad design space for the current stage;
- alternatives are iteratively developed and compared rather than treated as fixed cosmetic variants.

### Source 2
**NASA — Decision Analysis, Section 6.8**  
Institution: National Aeronautics and Space Administration  
URL: https://www.nasa.gov/reference/6-8-decision-analysis/  
Published/current web edition: NASA Systems Engineering Handbook web reference  
Accessed: 2026-08-28

What it adds:
- define the decision and decision criteria before evaluating alternatives;
- the alternative set should cover the relevant decision space;
- record how each alternative compares to the criteria;
- a recommendation is separate from the eventual decision authority.

### Rights / license boundary
NASA public web/handbook material is used here as a factual professional reference and is independently paraphrased. No NASA logo, insignia, visual identity, template, illustration, objective-function graphic, prompt, code or trade dress is copied into the artifact.

NASA's current media/brand guidance states that NASA logos/identifiers are protected and must not be used to imply endorsement:
https://www.nasa.gov/nasa-brand-center/images-and-media/

No endorsement is claimed.

## CAPABILITY MAPPING / COMPARE WITH CURRENT

Existing OLEANDER already covers more than 60%:
- generate at least two options;
- compare alternatives;
- perform deletion/adverse-condition tests;
- preserve E/I/A/D;
- keep technical validation separate.

External sources expose one bounded missing emphasis:
**the options should differ at the functional-allocation / architecture level before styling and selection are credited.**

Therefore:
`EXTEND THROUGH PRACTICE EVIDENCE`, not a parallel Skill.

Rejected / not transferred:
- NASA aerospace lifecycle/WBS;
- NASA objective functions, MOP terminology or cost/schedule models;
- technology-readiness procedures;
- any fixed number of concepts;
- any numeric weighting, threshold or preferred-option score;
- NASA document/template identity.

## DESIGN QUESTION / INPUTS / CONSTRAINTS

Synthetic object: portable task light.

Question:
How can one product satisfy:
- one-hand carry;
- freestanding use;
- directional aiming;
- lens protection during transport?

Exercise constraints:
- functions only;
- no electrical/thermal/optical output claim;
- no stability measurement;
- no mechanism/manufacturing proof;
- no weighted scoring.

`EXERCISE CRITERIA` are trace checks only, not universal design criteria.

## E-I-A-D

**EVIDENCE / GIVEN FUNCTION SET**  
Carry / stand / aim / protect are distinct required functions in the exercise.

**INFERENCE**  
If every concept allocates those functions to the same parts and only changes finish/silhouette styling, the apparent option diversity is shallow.

**ASSUMPTION / EXERCISE ATTACK**  
Freestanding remains required unless explicitly relaxed by the exercise authority.

**DESIGN CONSEQUENCE**  
Generate alternatives by changing which component owns each function before styling and selection.

## ARTIFACT / OPTIONS

Editable:
- `OLEANDER_OPTION_SPACE_FUNCTIONAL_ALLOCATION_R01.svg`

Rendered readbacks:
- full PNG;
- 50% grayscale PNG.

### A / REJECT — One concept, three skins
Same body architecture, same function allocation; only color/radius/texture changes.

### B — Pivot head + U-frame
- frame = carry + stand;
- pivot head = aim;
- frame envelope = transport protection.

### C — Sliding head + weighted base
- handle = carry;
- weighted base = stand;
- rail/slider = aim;
- body/rail relation = parked protection.

### D / REVISE — Clip arm
- clip = carry + attach;
- articulated head = aim;
- freestanding is not satisfied.

D is not universally rejected. It becomes viable only if the freestanding requirement is explicitly relaxed by the decision authority.

## A/B / ATTACK

1. **SURFACE-OFF**
   Remove color/texture/radius styling.
   - A collapses into one concept.
   - B/C/D remain structurally different.

2. **FUNCTION-ALLOCATION**
   Map each function to the component that owns it.
   - A produces the same map three times.
   - B/C/D produce materially different maps.

3. **REQUIREMENT-RELAXATION**
   Remove `freestanding`.
   - D moves from REVISE to potentially viable.
   - This demonstrates that option status depends on requirement authority, not designer preference.

4. **HANDLE-DELETION**
   Delete C's dedicated handle.
   - carry degrades without changing stand/aim.
   - confirms that functions are independently allocated rather than rhetorically listed.

5. **GRAY50**
   Option differentiation survives without color.

## ACTUAL READBACK

First full-size readback found a real presentation failure:
- A's `FUNCTION-ALLOCATION TEST` evidence line crossed the panel boundary;
- B/C/D descriptive lines were longer than their panel-local reading role.

This weakened the comparison because the option evidence itself contaminated neighboring options.

## FAILURE / ROOT CAUSE

**Design-process root cause**  
`visual variation ≠ design alternative`.

Option generation that occurs only after architecture/function allocation is fixed does not meaningfully explore the decision space.

**Representation root cause**  
A comparison artifact loses decision clarity when evidence for one option visually crosses into another option's territory.

## REPAIR / RETEST

Repair:
- split A's functional-allocation evidence into two panel-local lines;
- shorten B/C/D description text without deleting functional information;
- retain all option geometry and exercise criteria.

Retest:
- full-size PNG reopened;
- 50% grayscale reopened;
- no option evidence crosses a panel boundary;
- A still collapses under surface-off;
- B/C/D remain architecture-distinct;
- D remains conditional on requirement relaxation;
- no preferred design or numeric winner is claimed.

## PROFESSIONAL CRIT

Producer design-process crit:
- first read: PASS after repair;
- option diversity: PASS for B/C/D;
- counterexample clarity: PASS for A;
- criteria traceability: PASS at exercise level;
- decision integrity: PASS — D's status changes when requirement authority changes;
- hierarchy: PASS — concept geometry carries the comparison before prose;
- grayscale: PASS;
- selection validity: HOLD;
- technical/product validity: HOLD;
- independent professional review: HOLD.

## TRANSFER RULE

Bounded Practice claim:

> Before selecting or polishing options, check whether the alternatives still differ after surface styling is removed. If they preserve the same functional allocation/architecture, treat them as variants of one concept rather than evidence of a broad option space.

When functional allocation differs, record which requirement each architecture satisfies or sacrifices before ranking.

This is evidence for option-generation discipline, not a universal demand that every design project use a morphology matrix or a fixed number of concepts.

## BOUNDARY

Applicable to:
- product architecture;
- spatial organization;
- service-system alternatives;
- interface/system architecture;
- mechanism/form option studies;
- early concept comparison before baselining.

Not sufficient for:
- quantitative trade-study selection;
- engineering feasibility;
- cost/schedule/risk weighting;
- ergonomic validation;
- optics/thermal/electrical performance;
- manufacturing approval;
- stakeholder preference;
- final design selection.

## STATUS

`PRACTICE_EVIDENCE / EXTERNAL-SOURCE-CALIBRATED`

This run does not claim:
- `PROJECT_USAGE_EVIDENCE`;
- `VALIDATED_CANDIDATE`;
- `ACTIVE`.

Under NO-CHURN, no Current Skill body change is proposed in this run. The existing Candidate already owns option generation; this evidence strengthens how that capability is practiced and tested.
