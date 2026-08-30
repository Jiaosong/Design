# 2026-08-28｜Design Process / Handoff / L5｜Design → Validation Relation Contract

STATUS: `TRAINING_MODE / CROSS_CONTEXT_EVIDENCE (STRENGTHENED) / NO_PROJECT_USAGE / NO_PROMOTION`

## GAP
The existing `oleander-design-process` Candidate already requires a Validation Handoff when technical proof is needed. Recent Practice evidence covered causal diagrams, product form, spatial threshold/circulation, and IA/state recovery. The remaining material gap is **handoff clarity**: a design can be coherent yet lose its intent when the downstream validator receives only dimensions or, conversely, receives invented engineering detail.

## SOURCE
Existing-first:
- `oleander-skills/SKILL_REGISTRY_v1.1.json`
- `oleander-skills/REVIEW.md`
- `00-governance/OLEANDER_WORK_COORDINATION_CONTRACT_v1.0.md`
- `00-governance/OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT.json`
- `00-governance/OLEANDER_HUMAN_PROFESSIONAL_VOICE_POLICY_v1.0.md`
- `oleander-skills/oleander-design-process/SKILL.md`

Priority Queue is empty, so this is Practice/Candidate frontier only. No project Current or production frontier is modified.

## DESIGN QUESTION / INPUTS / CONSTRAINTS / E-I-A-D
Question: Can a design handoff tell VALIDATION what relationship must survive, what variable to attack, what counts as failure, and where the result must return — without the DESIGN owner inventing engineering closure?

Synthetic object: adjustable clamp around a variable-diameter rod.

- EVIDENCE: hand clearance and rod diameter are independent constraints.
- INFERENCE: one fixed jaw span may fail across the intended range.
- ASSUMPTION / TEST RANGE: rod Ø24 / Ø28 / Ø32 mm, explicitly synthetic.
- DESIGN DECISION: adjustable jaw; finger zone remains outside the jaw travel envelope.
- Technical boundary: force, tolerance, material, thread, manufacturing and safety remain downstream VALIDATION questions.

## ARTIFACT / OPTIONS
Editable artifact: `OLEANDER_DESIGN_VALIDATION_HANDOFF_R01.svg` plus local full-size/Gray50 readback derivatives.

- **A REJECT — Dimension-only Handoff**: “validate 28 mm”; no behavior, variable, failure condition or return object.
- **B KEEP candidate — Relation + Test Variable Handoff**: locks the relation, exposes the variable, defines failure, preserves HOLD, and returns PASS/REVISE to the same master.
- **C REVISE — Premature Engineering**: DESIGN invents material, force, tolerance, thread and torque values without authority.

## A/B / ATTACK
1. `NUMBER-OFF / DELETION`: delete provisional dimensions. A/C lose useful handoff meaning; B still communicates the relation and validation task.
2. `ADVERSE CONDITION`: Ø32 rod + finger-zone requirement simultaneously; validation tests the relationship, not one nominal dimension.
3. `AUTHORITY ATTACK`: add plausible engineering numbers without source/calculation; reject DESIGN self-certification.
4. `RETURN TEST`: downstream result points back to the same design master and states which invariant failed/survived.
5. `GRAY50`: handoff hierarchy cannot depend on hue.

## READBACK → FAILURE / ROOT CAUSE → REPAIR / RETEST
First full-size readback found B's adverse-condition sentence crossing into C. Repair kept the B relation/test model unchanged, split the note into bounded lines, then re-rendered/reopened full-size and Gray50.

Root causes:
- `dimension sent ≠ design intent transferred`;
- technical-looking detail reduces handoff quality when DESIGN invents parameters owned by VALIDATION;
- correct logic still fails professionally when the representation crosses comparison boundaries.

Retest: no panel crossing; B remains legible after provisional-number deletion; `LOCKED RELATION / TEST VARIABLE / FAIL IF / RETURN / HOLD` remains explicit.

## PROFESSIONAL CRIT
Producer design-process crit: first read PASS after repair; option contrast PASS; hierarchy PASS; handoff clarity PASS for synthetic Practice; authority discipline PASS; technical validity HOLD because no engineering/physical validation was executed.

## TRANSFER RULE
**A Design→Validation handoff transfers invariants and failure logic, not just nominal dimensions.**

Minimum useful handoff:
`SAME OBJECT → LOCKED DESIGN RELATION → TEST VARIABLE → FAILURE CONDITION → REQUIRED NATIVE OUTPUT / MEASUREMENT → RETURN PATH → RESIDUAL HOLD`

DESIGN states what behavior must survive. VALIDATION chooses/proves the technical method unless higher authority already fixes it.

## BOUNDARY
Applicable to product mechanism/ergonomics, spatial clearance, technical drawing proof, browser/runtime invariants, manufacturing prototype questions and system-state validation.

Not sufficient for engineering calculation, safety approval, material specification, manufacturing tolerance, code compliance, field truth or backend correctness.

## STATUS
Fifth materially different context; maturity remains `CROSS_CONTEXT_EVIDENCE (STRENGTHENED)`. No `PROJECT_USAGE_EVIDENCE`, `VALIDATED_CANDIDATE`, or `ACTIVE` promotion. Under NO-CHURN, the Skill body is unchanged because its current Validation Handoff section already owns the required contract.