# 2026-08-28｜Design Process / IA / L5｜State Consequence + Recovery

STATUS: `TRAINING_MODE / CROSS_CONTEXT_EVIDENCE (STRENGTHENED) / NO_PROJECT_USAGE / NO_PROMOTION`

## GAP
The existing `oleander-design-process` Candidate already owns information architecture, user flow and state models before final UI polish. Recent Practice evidence covered:
1. causal relation diagrams;
2. product requirement → form;
3. spatial threshold / circulation.

The next material gap is whether the same Evidence → Finding → Design Consequence logic survives a non-spatial system context: **state semantics and recovery**.

## SOURCE
Existing-first:
- GitHub main `oleander-skills/oleander-design-process/SKILL.md`;
- Current Registry / REVIEW / Work Coordination Contract;
- Current Priority Queue is empty, therefore Practice/Candidate frontier only.

No external source was needed because this run tests transfer of an existing design-process claim rather than introducing a new service/backend rule.

## DESIGN QUESTION / INPUTS / CONSTRAINTS / E-I-A-D
Question:
When inventory verification is asynchronous, can the IA distinguish user intent from committed success and preserve a truthful recovery path under offline/stale conditions?

Inputs:
- synthetic tool-library reservation;
- browse / select / verify / commit;
- offline and stale-inventory adverse states;
- user may return and revise selection.

Constraints:
- no real service/inventory/backend/payment claim;
- no persistence or concurrency implementation;
- no accessibility certification.

EVIDENCE:
Inventory confirmation and user selection do not necessarily happen at the same moment.

INFERENCE:
`SELECTED` can represent tentative intent but cannot honestly equal reservation success.

ADVERSE CONDITIONS:
- network loss during verification;
- stale inventory;
- user returns before commit.

DESIGN CONSEQUENCE:
Separate `selection / verification / commit / recovery` as distinct states with different allowed claims/actions.

## ARTIFACT / OPTIONS
Editable artifact:
- `OLEANDER_IA_STATE_CONSEQUENCE_R01.svg`
- rendered full-size PNG;
- 50% grayscale PNG.

Options:
- **A REJECT — Happy-path Wizard**: SELECT → CONFIRM → DONE, with generic Error added afterward.
- **B KEEP candidate — Stateful Commit + Recovery**: `BROWSE → SELECTED → CHECKING → COMMITTED`, plus bounded `UNKNOWN/OFFLINE` and `UNAVAILABLE` recovery states.
- **C REVISE — State Explosion**: every exception becomes a separate screen, obscuring the actual commitment/recovery semantics.

## A/B / ATTACK
1. `NETWORK-OFF`: failure during verification must not imply success and must preserve tentative intent where policy allows.
2. `STALE-INVENTORY`: stale availability must route to `UNAVAILABLE`, not generic Error/Retry.
3. `SCREEN-NAME DELETION`: remove page titles/error copy; the model should still expose commitment level and recovery.
4. `RETURN/REVISION`: returning before commit must not be represented as cancellation of an already-completed reservation.
5. `GRAYSCALE`: semantic state structure cannot depend on hue alone.

## ACTUAL READBACK
Initial full-size readback found a real representation defect in B:
- recovery transition lines crossed;
- the model was logically correct but the crossing paths weakened first-read state semantics.

## FAILURE / ROOT CAUSE
Two failures were confirmed:
1. **IA failure** — `screen sequence ≠ state model`; happy-path pages do not express commitment, uncertainty or recovery.
2. **representation failure** — correct state logic can still become visually ambiguous if transition routing crosses and competes with state nodes.

## REPAIR / RETEST
Repair:
- retain the same B state set and state meaning;
- reroute transitions orthogonally;
- separate `OFFLINE` and `STALE` paths;
- keep `COMMITTED` as the only success state.

Retest:
- full-size PNG reopened after repair;
- 50% grayscale reopened;
- `SELECTED` remains tentative;
- `UNKNOWN/OFFLINE` preserves intent but blocks success claim;
- `UNAVAILABLE` returns to selection;
- `COMMITTED` alone owns success;
- transition paths no longer cross materially.

## PROFESSIONAL CRIT
Producer design-process crit:
- first read: PASS after transition repair;
- composition: PASS — A/B/C compare different system structures rather than styling variants;
- hierarchy: PASS — commitment/recovery semantics dominate support copy;
- IA integrity: PASS for synthetic training;
- adverse-state consequence: PASS — failures change next actions, not only message text;
- grayscale: PASS;
- technical/runtime validity: HOLD — no backend/persistence/concurrency/service policy proven.

## TRANSFER RULE
**Model commitment level, truth state and recovery before deciding how many screens exist.**

A failure state is a real design consequence only when it changes:
- what the system may truthfully claim;
- what user intent is preserved;
- what next action is permitted;
- what returns to the prior state.

Adding an Error page after the happy path is not equivalent.

## BOUNDARY
Applicable to:
- reservations / checkout;
- form submission and asynchronous verification;
- offline-first workflows;
- service booking;
- upload/sync;
- transaction-like flows with tentative vs committed states.

Not sufficient for:
- payment ledger correctness;
- distributed consistency;
- legal cancellation policy;
- backend retry semantics;
- accessibility;
- security;
- real inventory/service SLA.

## STATUS
This is a fourth materially different design context after relation-diagram, product-form and spatial-threshold evidence.

Maturity remains:
`CROSS_CONTEXT_EVIDENCE (STRENGTHENED)`

No `PROJECT_USAGE_EVIDENCE`, `VALIDATED_CANDIDATE`, or `ACTIVE` promotion is claimed.

Under NO-CHURN, the existing Skill body is not modified: it already explicitly owns IA / user-flow / state models. This run records Practice evidence only.
