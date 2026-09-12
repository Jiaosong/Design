# 2026-08-28｜Design Process / Product-System / L5｜System State → Physical Interface Consequence

STATUS: `TRAINING_MODE / CROSS_CONTEXT_EVIDENCE (STRENGTHENED) / NO_PROJECT_USAGE / NO_PROMOTION`

## GAP
Recent Design Process Practice evidence already covers:
1. spatial threshold / circulation;
2. role-bound CMF after form proof;
3. service-state → spatial consequence.

The next material transfer gap is whether **system/service truth changes the physical product interface itself** — insertion, release, blocking and misuse prevention — rather than remaining an LED, screen or service label.

## SOURCE
Existing-first:
- GitHub main `oleander-skills/oleander-design-process/SKILL.md`;
- Current Registry / REVIEW / Work Coordination Contract;
- Current Priority Queue is empty, therefore Practice/Candidate frontier only.

No external source is used because this run tests transfer of the current causal-design chain. It does not assert a real mechanism, electrical standard, safety standard or manufacturing rule.

## DESIGN QUESTION / INPUTS / CONSTRAINTS / E-I-A-D
Question:
If `RETURNED_UNCHECKED`, `VERIFIED_READY` and `QUARANTINED` are different service truths, can the physical dock prevent them from behaving as the same state when color/screens are unavailable?

Inputs:
- synthetic shared-tool dock;
- return intake;
- verified release;
- quarantine;
- low-light / color-off / screen-off / power-off / misdock adverse conditions.

Constraints:
- NTS;
- no real lock/sensor/mechanism;
- no force/tolerance;
- no electrical safety;
- no accessibility/manufacturing validation.

EVIDENCE:
Returned-unchecked, verified-ready and quarantined tools are different service states.

INFERENCE:
If all states share the same dock affordance, status display becomes the only rule and users can physically perform the wrong action.

ADVERSE CONDITIONS:
low light / color loss / screen loss / power loss / rushed misdock.

DESIGN CONSEQUENCE:
Translate service truth into different physical permissions:
- return-only intake;
- verified-only release;
- quarantine that is not user-releasable.

## ARTIFACT / OPTIONS
Editable artifact:
- `OLEANDER_SYSTEM_STATE_PHYSICAL_INTERFACE_R01.svg`
- full-size PNG;
- 50% grayscale PNG.

### A / REJECT — Same Dock, Different LED
Three physically identical slots use green/yellow/red status lights. Remove color or power and the state model disappears.

### B / KEEP candidate — State-bound Mechanical Permission
- RETURN: one-way intake geometry;
- VERIFIED: release cradle with explicit unlock/release role;
- QUARANTINE: separate blocked/non-user-release state;
- CMF is secondary.

### C / REVISE — Screen-guided Universal Slot
A screen explains the current state, but a universal physical slot still permits the wrong action before the screen is read.

## A/B / ATTACK
1. `COLOR-OFF` — hue cannot be the only state carrier.
2. `SCREEN-OFF` — display loss cannot collapse permission semantics.
3. `POWER-OFF` — no false claim that the sketch proves a safe fail-state; only check whether passive affordance still distinguishes roles.
4. `MISDOCK` — returned/unchecked must not behave like verified-ready.
5. `RUSH` — user can act before reading instructions; form should constrain the high-risk wrong action.
6. `LABEL-OFF` — physical role should remain legible without explanatory text.
7. `GRAYSCALE` — role differentiation survives without color.

## ACTUAL READBACK
Initial full-size readback found a real semantic defect in B:
- dashed lines between RETURN / VERIFIED / QUARANTINE visually implied a sequential state progression;
- quarantine is not the normal next step after verified release;
- a correct physical-permission concept was therefore represented with a false transition relationship.

## FAILURE / ROOT CAUSE
Two failures were confirmed:
1. **Design-process failure:** `displayed state ≠ enforced state`; LEDs/screens can describe truth without constraining the wrong physical action.
2. **Representation failure:** visual connectors can manufacture a state transition that the system does not own.

## REPAIR / RETEST
Repair:
- preserve B's three physical-role concepts;
- remove dashed state connectors;
- replace them with neutral separation ribs;
- label the relation as `SEPARATE PERMISSION ZONES`, not a flow.

Retest:
- full-size PNG reopened;
- 50% grayscale reopened;
- RETURN / VERIFIED / QUARANTINE remain distinct without hue;
- no normal flow from VERIFIED to QUARANTINE is implied;
- screen-off / label-off logic still differentiates insertion/release/blocking roles;
- the sketch still does **not** claim a validated passive fail-safe mechanism.

## PROFESSIONAL CRIT
Producer design-process crit:
- first read: PASS after repair;
- option differentiation: PASS;
- causal integrity: PASS — service truth changes physical affordance and permission;
- form-before-finish: PASS — B remains distinguishable without hue/screens;
- adverse-condition reasoning: PASS as conceptual design evidence;
- professional finish: sufficient for Practice evidence;
- mechanical/electrical/safety/manufacturing validity: HOLD;
- independent professional review: HOLD.

## TRANSFER RULE
`SYSTEM / SERVICE STATE → ALLOWED USER ACTION → PHYSICAL PERMISSION → FORM / INTERFACE → STATUS FEEDBACK`

A state is not fully designed into a physical product when the user can perform the same action in every state and only the LED/screen changes.

For high-consequence state differences, at least one physical permission or affordance should change before finish/status styling is credited.

## BOUNDARY
Applicable to:
- shared-tool docks;
- charging/release stations;
- return/intake products;
- maintenance/service fixtures;
- reusable container return systems;
- physical interfaces where service state changes what action should be possible.

Not sufficient for:
- mechanical interlock proof;
- sensor logic;
- electrical fail-safe behavior;
- safety certification;
- force/tolerance;
- accessibility;
- service maintenance;
- production engineering.

## STATUS
This is a materially different system/service → physical-product context.

Maturity remains:
`CROSS_CONTEXT_EVIDENCE (STRENGTHENED)`

No `PROJECT_USAGE_EVIDENCE`, `VALIDATED_CANDIDATE`, or `ACTIVE` promotion is claimed.

Under NO-CHURN, the existing Skill body is not modified; this run records Practice evidence only.
