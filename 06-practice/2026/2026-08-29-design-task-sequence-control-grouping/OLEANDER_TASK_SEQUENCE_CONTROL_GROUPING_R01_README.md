# 2026-08-29｜Design Process / Product-Interface / L5｜Task Sequence → Control Grouping

STATUS: `TRAINING_MODE / PRACTICE_EVIDENCE / EXTERNAL-SOURCE-CALIBRATED / NO_PROJECT_USAGE / NO_PROMOTION`

## GAP
Recent Practice evidence covered program→massing, site constraint→placement, and environmental requirement→section. This run shifts to a materially different physical-interface gap: does task analysis change control grouping/order/prominence, or does layout default to aesthetic symmetry?

## SOURCE
Internal Current:
- Notion Current Root Authority;
- `OLEANDER Knowledge Retrieval & Lifecycle｜知识库机制 v1.0`;
- GitHub main Registry / REVIEW / Work Coordination Contract / current Priority Queue;
- `oleander-design-process` Candidate.

External:
- NASA-STD-3001 Volume 2, §10.4.1.1 Display and Control Grouping:
  https://www.nasa.gov/reference/10-0-crew-interfaces-vol-2/
- NASA Human Integration Design Handbook landing:
  https://www.nasa.gov/organizations/ochmo/human-integration-design-handbook/
Accessed 2026-08-29.

Transferred only at bounded level:
- display/control relationships should be logical and may be grouped by purpose, function, or sequence;
- criticality/grouping should follow task analysis.

Rejected:
- NASA mission-specific control standards as universal product rules;
- any fixed spacing, reach, button size, color code, safety threshold, aerospace certification method, or NASA visual/template identity.

Rights boundary:
NASA web material is used as factual professional reference and independently paraphrased. NASA identifiers/visual identity are not reused and no endorsement is implied.

## DESIGN QUESTION / E-I-A-D
Synthetic object: desktop document scanner.

Exercise task:
`LOAD → PREVIEW → ADJUST → SCAN`; `STOP` must remain independently reachable; `EXIT` is secondary.

EVIDENCE:
NASA source supports grouping by purpose/function/sequence and task-analysis-based criticality.

INFERENCE:
A symmetric panel can be visually coherent yet conceal task order and control priority.

ASSUMPTION:
The scanner sequence above is an exercise assumption, not a universal scanner workflow.

DESIGN CONSEQUENCE:
Make task sequence visible in grouping/order; separate high-priority STOP from secondary EXIT.

## ARTIFACT / OPTIONS
Editable:
- `OLEANDER_TASK_SEQUENCE_CONTROL_GROUPING_R01.svg`

Rendered readbacks:
- full PNG;
- Gray50 PNG.

A / REJECT — Aesthetic Symmetry:
six equal buttons arranged symmetrically around a display.

B / KEEP candidate — Sequence Group + Escape:
main sequence is grouped left→right; SCAN receives bounded prominence; STOP is separated and prominent; EXIT remains nearby but secondary.

C / REVISE — Function Groups, Wrong Sequence:
functional grouping exists, but task travel jumps between groups.

## ATTACKS
- `LABEL-OFF`
- `DECORATIVE-COLOR-OFF / GRAY50`
- `RUSH`
- `SEQUENCE REVERSAL`
- `FUNCTION-ONLY`
- `STOP/EXIT MERGE`

## READBACK / FAILURE / REPAIR
Initial full-size readback found a real defect in B: `STOP / EXIT` had been merged into one escape control. That collapsed two different actions and contradicted the source-backed requirement for clear control relationships.

Repair:
- split STOP and EXIT into separate controls inside one escape zone;
- keep STOP visually stronger;
- keep EXIT secondary;
- preserve the main sequence geometry.

Retest:
- reopened full-size PNG;
- Gray50 retained sequence/grouping hierarchy;
- STOP and EXIT no longer share one semantic control;
- A still collapses under label-off;
- C still requires task travel across groups.

## ROOT CAUSE
`visual symmetry ≠ task-structured interface`, and `shared escape category ≠ identical action`.

## TRANSFER CANDIDATE
`TASK ANALYSIS → PURPOSE / FUNCTION / SEQUENCE → CONTROL GROUPING → ORDER / PROMINENCE → READBACK`

Bounded Practice claim:
Before styling is credited, remove labels and decorative color. If the physical layout no longer reveals the main task sequence or critical/escape hierarchy, the control organization is not yet evidenced by task logic.

## BOUNDARY
Applicable to early physical-control and hybrid hardware/software interface layout.

Not sufficient for:
- safety engineering;
- emergency-stop certification;
- accessibility;
- reach/anthropometry;
- control force/size;
- hardware/electrical implementation;
- actual scanner usability;
- independent professional review.

## STATUS
`PRACTICE_EVIDENCE / EXTERNAL-SOURCE-CALIBRATED / UNVERIFIED`

Existing owner remains `oleander-design-process`.
No Skill body change is proposed under NO-CHURN.
Formal Notion Migration / Relation Closure remains a KNOWLEDGE responsibility.
