# C04｜QJ-C｜Spatial + Experience Working Pack v1.3

- Date: 2026-08-14
- Canonical home: `C04-WS-02｜体验与空间关系`
- Scope: `QJ-C12｜Prototype Test Run v1.3`
- Input: `QJ-C11｜C-line Authority Register v1.2`
- Test type: `REMOTE MODEL WALKTHROUGH / LOGICAL PROTOTYPE`
- State: `PROTOTYPE PASS / FIELD PASS NONE / NOT PROMOTED`
- Field: `FIELD OBSERVED = 0 / FIELD MEASURED = 0`
- Gate: `G1F FIELD / PROFESSIONAL SURVEY = IMPLEMENTATION HOLD`

## 01｜Validation boundary

This run is not a visitor test and not a field test. Reviewer: AI design-system reviewer. Maximum conclusion: `PROTOTYPE PASS`; no field truth is added.

## 02｜T-C10-01 Route Completeness

Scenarios:
- Normal: arrival/orientation → moving landscape → trail → continuous walk → observe/optional read → recovery if needed → design withdrawal/closure → return/re-recognition → memory later.
- Reading/Companion closed: page becomes OFF / unavailable; route continues; no completion penalty.
- Shortened journey: remove Deep Read, S-C09-03, optional Physical and part of continuous walking; preserve Route certainty, one real Landscape/Body relation, necessary Recovery/Service and Return.
- Return pressure: close new deep-reading entry; `Return > Memory > new content`.

Result: `PROTOTYPE PASS / A-DEPENDENT FOR REAL ROUTE`.

Does not prove: actual route, duration, distance, physical load, accessibility, return visibility or operating feasibility.

## 03｜T-C10-02 No-phone / Weak-network

Digital = OFF. Low-fi parallel path:
1. Arrival: physical/human responsibility for entrance, direction and return.
2. Route: paper/physical wayfinding expresses macro spine, return and shortening/retreat responsibility.
3. Observation: real landscape + one prompt.
4. Understanding: site diagram / paper / human if necessary.
5. Closure: Safety / Direction only.
6. Return: physical/human Return certainty.
7. Memory: may be entirely post-visit.

Injected states: no phone from start; battery dies mid-route; network unavailable.

Result: `PROTOTYPE PASS / NOT FIELD-SUFFICIENT`.

Does not prove: current signage, staff, paper distribution, network or live service already satisfy the system.

## 04｜T-C10-03 Failure Injection

| Injection | Expected level | Fallback | Result |
|---|---|---|---|
| Reading/Companion closed | F1 | OFF / continue Route | PASS |
| Digital offline | F1 | physical/human/paper; Memory later | PASS |
| Physical candidate unavailable | F1 or F2 | bypass → C0 / existing support | PASS |
| Fog / distant view missing | F1 or F2 | near-view / atmosphere; no fake clear-weather view | PASS |
| Rain / wet surface | F2; F3 if safety uncertain | content down; Route/Safety authority up; close segment if needed | PASS / field threshold open |
| Peak / group crowd | F2; F3 if base circulation uncertain | remove Deep Read/dwell; prioritize Flow/Return | PASS / field threshold open |
| Return-window pressure | F2 | close new content; Return first | PASS |
| Safety / Return uncertainty | F3 | stop normal-experience claim; return control to Operations/A | PASS |

Result: `PROTOTYPE PASS / FIELD THRESHOLDS OPEN`.

## 05｜Phase A Gate

T-C10-01 / 02 / 03 = `PROTOTYPE PASS`. Internal blocking contradiction: none found. Field truth: none added. This allows T-C10-04 / 05 / 06 to run.

## 06｜T-C10-04 First-reading / Attention Hierarchy

- C0: Landscape/Body first; purest first reading; may lack minimal explanation when the relation is visible but difficult to understand.
- Light Support: Landscape + one prompt / necessary service / optional simple reveal; maintains real object visibility while solving the smallest information need.
- Strong Intervention: large Hero / strong digital / strong brand as first reading; conflicts with Landscape First under current Project Kernel.

Result: `PROTOTYPE PASS`.

Authority remains: `C0 → Light Support → Strong Intervention only if future evidence proves necessity`.

Does not prove: field viewing distance, illumination, reflection, obstruction or text readability.

## 07｜T-C10-05 Recovery Candidate Comparison

Comparison under the same hypothetical Recovery problem:
1. C0 wins if no real recovery problem exists.
2. Existing context reuse precedes new construction.
3. Removable railing-leaning rest board remains the strongest Physical Support candidate only if fatigue + clear width + railing condition jointly prove need.
4. Mountain fluid rest installation has not shown a necessary gain beyond lower intervention → HOLD.
5. Qingfengyin may add sensory value but is not a generic Recovery solution; wind/noise/maintenance open → HOLD.
6. 步步生光 does not directly solve Recovery and carries the highest artificial-first-reading risk → no Recovery Primary eligibility.

Result: `PROTOTYPE PASS / NO PHYSICAL SELECTION`.

Physical authority unchanged: railing support KEEP; mountain fluid / Qingfengyin / 步步生光 HOLD.

## 08｜T-C10-06 Return Re-recognition

- Return view exists: structure can form first seeing → lived experience → second seeing/re-recognition.
- Return view partial/fog: re-recognize only what is still real and visible; do not synthesize a missing clear-weather scene.
- Return view unavailable: do not fake re-recognition; completeness falls back to Safety + Route + Return + the real relation already experienced; Memory later.

Result: `PROTOTYPE PASS / A-DEPENDENT FOR ACTUAL VISIBILITY`.

Does not prove: real return sequence necessarily reveals earlier terrain or nodes.

## 09｜C12 Final Receipt

- T-C10-01—06: `PROTOTYPE PASS` at remote model-walkthrough level.
- `FIELD PASS`: NONE.
- Architecture package: eligible to prepare field tests; no Physical candidate is selected or located.
- New field fact: NONE.
- Physical authority unchanged: railing support KEEP; mountain fluid / Qingfengyin / 步步生光 HOLD.
- Promotion: NO.

## 10｜Next

`QJ-C13｜Pre-integration Handoff v1.4`

Convert C11 Authority + C12 Test Receipt into one cross-line handoff with three buckets: `Can Integrate Now / Must Mark Provisional / Must Wait for A-G1F`.
