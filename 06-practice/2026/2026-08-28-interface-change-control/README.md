# 2026-08-28｜Design Process / Handoff / L5｜Interface Change Control

STATUS: `TRAINING_MODE / PRACTICE_EVIDENCE / EXTERNAL-SOURCE-CALIBRATED / NO_PROJECT_USAGE / NO_PROMOTION`

## GAP
The current `oleander-design-process` Validation Handoff already carries stable object/master identity, design behavior, assumptions, authority, expected validation and a PASS/REVISE/HOLD return.

Recent Design evidence also includes:
- requirement→structural-form practice;
- system-state→physical-interface practice;
- service-state→spatial-consequence practice.

A remaining handoff gap is **change control when downstream validation discovers a constraint that would alter a design invariant**.

Without an explicit change path, two opposite failures remain possible:
1. VALIDATION silently edits the design master to obtain a PASS;
2. DESIGN treats invariants as immutable and blocks evidence-based technical feedback forever.

## External discovery / source check

### Source 1 — NASA Systems Engineering Handbook: Requirements Management
- Institution: NASA
- Page: `6.2 Requirements Management`
- URL: https://www.nasa.gov/reference/6-2-requirements-management/
- Accessed: 2026-08-28
- Relevant content: bidirectional traceability; requirements/expectations, product verification and validation results mapped back into requirements management; change requests are managed across the lifecycle.
- Rights boundary: U.S. Government/NASA public reference page; use as professional process calibration only. No NASA diagrams, branding, wording, fixed project thresholds or templates are copied into OLEANDER.
- Transferable: explicit trace from upstream requirement/expectation to downstream evidence and back.
- Not transferred: NASA program governance, WBS structure, review authorities, mission-specific technical requirements.

### Source 2 — NASA Systems Engineering Handbook: Interface Management
- Institution: NASA
- Page: `6.3 Interface Management`
- URL: https://www.nasa.gov/reference/6-3-interface-management/
- Accessed: 2026-08-28
- Relevant content: interface requirements are controlled; interface changes require documented impact/approval; interface control documentation and approved interface requirement changes feed verification/validation.
- Rights boundary: U.S. Government/NASA public reference page; concepts independently reformulated. No NASA interface-document template is adopted as OLEANDER default.
- Transferable: interface change request must identify what changed, impact, responsibility/change authority and correction.
- Not transferred: formal IWG structure, unanimous approval requirement, aerospace-specific interface-document families as universal OLEANDER rules.

### Source 3 — NASA Systems Engineering Handbook: Design Solution Definition
- Institution: NASA
- Page: `4.4 Design Solution Definition`
- URL: https://www.nasa.gov/reference/4-4-design-solution-definition/
- Accessed: 2026-08-28
- Relevant content: alternative solutions are compared; design solution verification checks realizability, bidirectional traceability and consistency of assumptions/decisions with requirements; design-solution verification is distinct from later end-product verification.
- Rights boundary: public NASA reference; process distinction only.
- Transferable: DESIGN must not self-certify technical validity, and VALIDATION findings must remain traceable to the design definition they affect.
- Not transferred: aerospace lifecycle stages, peer-review hierarchy or technical data package structure as mandatory OLEANDER format.

## COMPARE WITH CURRENT
Current coverage is already >60%; therefore **EXTEND, do not create a parallel Skill**.

Already covered:
- stable Object ID / current master;
- design invariant / expected behavior;
- technical owner remains downstream;
- assumptions and authority;
- PASS / REVISE / HOLD return;
- returned evidence must feed back to design.

Material missing fields:
- upstream requirement/expectation trace attached to the affected invariant;
- explicit `INTERFACE_CHANGE_REQUEST`;
- exact `IMPACTED_INVARIANT(S)`;
- `CHANGE_AUTHORITY`;
- disposition `ACCEPT / REJECT / ALTERNATIVE / HOLD`;
- link from authorized disposition to a revised design master/version.

## DESIGN QUESTION / E-I-A-D
Question:
When validation proposes a constraint that changes the pivot position of a folding interface, can the team preserve both technical evidence and design authorship without silent master edits?

EVIDENCE:
Design master carries two synthetic invariants:
- I1 folded outer edge remains flush;
- I2 pivot relation preserves grip-clearance intent.

INFERENCE:
Moving pivot P0 can affect both invariants.

ADVERSE CONDITION:
Validator reports P0 infeasible under its technical test and proposes `P0 + 8 mm` as a **synthetic exercise proposal**, not a real dimension.

DESIGN CONSEQUENCE:
Validation owns the finding/proposal evidence; Design Owner owns disposition of a design-changing interface request.

## ARTIFACT / OPTIONS
Editable artifact:
- `OLEANDER_INTERFACE_CHANGE_CONTROL_R01.svg`
- full-size PNG;
- Gray50 PNG.

### A / REJECT — Silent Validator Edit
Validator modifies the master and returns technical PASS. Design relations have changed without an authorized design decision.

### B / KEEP candidate — Traceable Interface Change Request
`R1 → I1/I2 → F1 → CR-01 → DESIGN DISPOSITION → revised master/HOLD`.

### C / REVISE — Frozen Design, No Feedback
Design invariant is treated as permanently immutable; technical evidence can only produce indefinite HOLD and cannot propose an alternative.

## A/B / ATTACK
1. `PARTIAL PASS` — if I1 survives and I2 fails, return must point to the exact affected invariant.
2. `AUTHORITY` — validator may propose evidence/alternative but cannot silently update design master.
3. `CHANGE-REQUEST DELETION` — deleting CR-01 must visibly break the trace from finding to authorized master revision.
4. `RATIONALE DELETION` — a change with no affected requirement/invariant trace remains HOLD.
5. `FROZEN-DESIGN ATTACK` — design authority controls changes; it does not prohibit evidence-based change proposals.
6. `GRAYSCALE` — change ownership/trace must not depend on color.

## ACTUAL READBACK
Initial full-size readback exposed a real gap in B:
- the bottom trace text referenced `design disposition`;
- no explicit disposition node existed;
- the arrow returned directly from the change request to the original handoff, visually implying that the request itself could update the master.

## FAILURE / ROOT CAUSE
`RETURN STATUS ≠ CHANGE CONTROL`.

A handoff can be technically traceable and still leave authorship ambiguous when downstream evidence requires a change to the design definition.

Representation also matters: if `disposition` is not a visible state/object, the diagram can accidentally imply unauthorized auto-update.

## REPAIR / RETEST
Repair:
- preserve the same R1/I1/I2/F1/CR-01 semantics;
- add explicit `DESIGN DISPOSITION`;
- route `CR-01 → DESIGN DISPOSITION → DESIGN HANDOFF/revised master`;
- keep validator proposal separate from Design Owner disposition.

Retest:
- full-size PNG reopened after repair;
- Gray50 reopened;
- B no longer implies `CR-01` directly updates the master;
- partial-pass and authority attacks remain readable;
- A still exposes unauthorized edit;
- C still exposes blocked feedback.

## PROFESSIONAL CRIT
Producer design-process crit:
- first read: PASS after repair;
- option differentiation: PASS;
- causal integrity: PASS;
- handoff/change ownership: PASS as Practice evidence;
- external-source mapping: PASS — NASA contributes bidirectional traceability + controlled interface changes, not copied templates;
- technical validity: HOLD;
- independent professional review: HOLD.

## TRANSFER RULE
`UPSTREAM REQUIREMENT → DESIGN INVARIANT → VALIDATION FINDING → INTERFACE CHANGE REQUEST → IMPACT → CHANGE AUTHORITY → DISPOSITION → REVISED MASTER / HOLD`

When downstream evidence would change a design invariant, **do not silently edit and do not permanently freeze**. Return a traceable change proposal to the owner of the design decision.

## BOUNDARY
Applicable to:
- design→engineering handoff;
- product mechanism/interface development;
- architecture/landscape detail validation;
- web/product state contracts where a downstream constraint changes upstream behavior;
- supplier/manufacturing feedback that would alter an approved design relation.

Not sufficient for:
- engineering approval;
- supplier authority;
- configuration-management certification;
- contractual change boards;
- field truth;
- safety approval;
- actual mechanism/dimension validity.

## STATUS
`PRACTICE_EVIDENCE / EXTERNAL-SOURCE-CALIBRATED`

This is a new professional-source change-control attack on an existing handoff capability. It does not itself establish project usage.

Because current capability coverage is already >60%, this run proposes a **bounded reference extension** under the existing Candidate rather than a parallel Skill or immediate main-rule change.
