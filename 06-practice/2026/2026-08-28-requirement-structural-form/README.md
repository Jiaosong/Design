# 2026-08-28｜Design Process / Product Structure / L5｜Requirement → Structural Form

STATUS: `TRAINING_MODE / CROSS_CONTEXT_EVIDENCE (STRENGTHENED) / NO_PROJECT_USAGE / NO_PROMOTION`

## GAP
Recent Practice evidence covers role-bound CMF, service-state → spatial consequence, and system-state → physical-interface consequence. A remaining Product Design gap is earlier in the chain: **does a moving/folding requirement become support geometry before finish and CMF?**

## SOURCE
Existing-first:
- GitHub main `oleander-design-process/SKILL.md`;
- Current Registry / REVIEW / Work Coordination Contract;
- Current Priority Queue is empty.

No external engineering source is used because the exercise stops before structural validation. The load paths are conceptual design diagrams only.

## DESIGN QUESTION / INPUTS / CONSTRAINTS / E-I-A-D
Question:
If a carry handle must fold flat and also carry an upward lifting action when deployed, can the form visibly distinguish motion geometry from support/lock geometry?

Inputs:
- synthetic folding carry handle;
- two pivots;
- deployed and folded requirement;
- conceptual lifting load;
- one-side load / incomplete deployment / lock deletion attacks.

Constraints:
- NTS;
- no load value;
- no hinge/pin size;
- no material;
- no fatigue/pinch/tolerance/manufacturing proof.

EVIDENCE:
The handle must reduce stored height and still transfer a lifting action when deployed.

INFERENCE:
Pivots solve motion but do not by themselves prove a deployed support condition.

ADVERSE CONDITION:
one-side load / incomplete deployment / missing stop.

DESIGN CONSEQUENCE:
Separate `PIVOT / STOP / SEAT` roles before shell styling.

## ARTIFACT / OPTIONS
Editable artifact: `OLEANDER_REQUIREMENT_STRUCTURAL_FORM_R01.svg`.

### A / REJECT — Folding as Silhouette
Two pivots make the handle visibly foldable, but deployed support is only implied.

### B / KEEP candidate — Pivot + Stop + Seat
- pivot owns motion;
- stop owns deployed angle;
- seat owns the conceptual transfer into the body support zone;
- load path is explicitly labelled conceptual.

### C / REVISE — Overbuilt Bridge
A thick continuous bridge makes support look obvious but cancels folding and invades grip clearance.

## A/B / ATTACK
1. `LOCK-DELETION` — delete stop geometry; deployed support relation should visibly fail.
2. `ONE-SIDE LOAD` — expose asymmetric support risk rather than hiding it in a symmetric hero view.
3. `FOLD ATTACK` — support geometry may not cancel the storage requirement.
4. `GRIP DELETION / CLEARANCE` — structural reinforcement may not consume the hand zone.
5. `LABEL-OFF` — pivot/stop/seat roles should remain visible without explanatory copy.
6. `GRAYSCALE` — reasoning cannot depend on color.

## ACTUAL READBACK
Full-size and 50% grayscale artifacts were reopened.

- A remains visually plausible as a product silhouette but fails the lock-deletion test: no actual lock role was designed.
- B separates pivot, stop and seat. The conceptual load path terminates at support zones rather than at the pivot alone.
- C proves the opposite failure: reinforcement is so dominant that folding and grip clearance are lost.
- Gray50 preserves the A/B/C structural distinction.

No new finished-pixel collision or clipping defect was found. The material repair in this run is the **design repair from A → B**, not a cosmetic post-export patch.

## FAILURE / ROOT CAUSE
`MOTION GEOMETRY ≠ SUPPORT GEOMETRY`.

A form can convincingly depict movement while leaving the deployed load/support condition unresolved.

The opposite error is `VISIBLE STRENGTH ≠ REQUIREMENT FIT`: adding a large bridge can make support look credible while cancelling folding or grip clearance.

## REPAIR / RETEST
Repair:
- introduce distinct stop geometry at the deployed condition;
- introduce body seats/support zones;
- keep pivots as motion elements rather than asking them to visually prove the entire load path;
- preserve the folding envelope and grip clearance.

Retest:
- `LOCK-DELETION`: B visibly loses its deployed-angle/support relation when stops are removed;
- `FOLD ATTACK`: B does not add a continuous bridge across the folding envelope;
- `ONE-SIDE LOAD`: B exposes the asymmetric case as a Validation question rather than claiming closure;
- `GRAYSCALE`: form roles remain legible.

## PROFESSIONAL CRIT
Producer design-process crit:
- first read: PASS;
- option differentiation: PASS — alternatives change structural/form logic, not finish;
- requirement traceability: PASS;
- form-before-finish: PASS;
- deletion/adverse-condition evidence: PASS;
- representation: PASS at current training scale;
- engineering validity: HOLD;
- independent professional review: HOLD.

## TRANSFER RULE
`REQUIREMENT → MOTION ROLE → DEPLOYED SUPPORT CONDITION → STOP / SEAT / LOAD-PATH CONCEPT → FORM → VALIDATION HANDOFF`

When a product changes state mechanically, do not let the moving joint carry every design responsibility. Motion, deployed constraint, support and user clearance should be visible as separate roles before finish is credited.

## BOUNDARY
Applicable to folding handles, hinges, deployable stands, latches, collapsible product parts, and covers/arms that must move and then carry or resist an action.

Not sufficient for structural capacity, pin/hinge sizing, fatigue, pinch safety, force, tolerance, material selection or manufacturing approval.

## STATUS
This is a materially different Product Design context focused on pre-CMF structural-form reasoning.

Maturity remains: `CROSS_CONTEXT_EVIDENCE (STRENGTHENED)`.

No `PROJECT_USAGE_EVIDENCE`, `VALIDATED_CANDIDATE`, or `ACTIVE` promotion is claimed.

Under NO-CHURN, the existing Skill body is not modified because main already owns `form → structure → material/interaction` and Validation Handoff. Practice evidence only.
