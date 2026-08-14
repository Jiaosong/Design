# C04｜QJ-D｜Field Gate Prep v0.4

**Date:** 2026-08-14  
**Owner:** C04-WS-04｜Visual Reading & Identity / QJ-D  
**Reality Authority:** `C04-WS-02_QJ-C_FIELD-EVIDENCE-PROTOCOL_v1.0`  
**Drive Workbook ID:** `1aahKJLDVLX97VOb33rrmKNkHNyiLISVP2k5iemmZdW4`  
**Overlay Sheet:** `07_QJ-D_FIELD-GATES`  
**Table:** `QJDFieldGatesTable`  
**Range:** `A1:L12`

## State

- `FIELD GATE PREP = CLOSED`
- `FIELD EXECUTION = NOT RUN`
- `FIELD OBSERVED = 0`
- `FIELD MEASURED = 0`
- `G-D1 REAL DISTANCE = HOLD`
- `G-D2 PHYSICAL SAMPLE = HOLD`
- `R06 FIELD GEOMETRY = HOLD / NO FIELD GEOMETRY`
- `R13 FIELD SAFETY / ACCESSIBILITY = HOLD`
- `FINAL VISUAL / CANONICAL PRODUCTION PROMOTION = NO`

This receipt closes only the preparation of executable field/physical tests. It does not claim that any field, material, safety, accessibility, geometry, durability or visitor test has occurred.

## Authority rule

D does **not** create a second Reality Authority. All future D field observations and gate receipts must write back into the existing C04 Field Evidence workbook, especially:

- `02_FIELD_OBSERVATION`
- `03_OPPORTUNITY_GATE`
- `05_TEST_PROTOCOL`
- `06_RECEIPTS`

Every executed observation must retain `What It Does NOT Prove` and must not promote remote/render/runtime evidence into field truth.

## D-specific overlay contract

Each row defines:

`D_Test_ID → Gate → Target Object → Situation Band → Execution Mode → Required Evidence → PASS → REVISE → REJECT/HOLD → What It Does NOT Prove → Current State → Record-To`

`Current_State` is constrained to:

- `HOLD / NOT RUN`
- `HOLD / NO FIELD GEOMETRY`
- `RUN / DATA PENDING`
- `PASS`
- `REVISE`
- `REJECT`

## Test matrix

| ID | Gate / object | Required real execution | Current state |
|---|---|---|---|
| D-F01 | G-D1 / R06 static distance | actual install height, viewing distances, light/glare/shadow, reading order | HOLD / NOT RUN |
| D-F02 | G-D1 / R06 moving-view hierarchy | approach-pass-exit movement, speed band, occlusion/crowd, first readable moment | HOLD / NOT RUN |
| D-F03 | G-D1 + R13 reality | no-phone before/inside/exit walkthrough; width, wetness, crowd, bypass, visibility, accessibility | HOLD / NOT RUN |
| D-F04 | G-D1 / R13 afterward timing | actual exit threshold, flow, landscape re-recognition before optional media | HOLD / NOT RUN |
| D-P01 | G-D2 / dry-wet glare | real substrate + print/lamination sample under dry/wet/oblique light | HOLD / NOT RUN |
| D-P02 | G-D2 / abrasion-cleaning | real sample cleaning/abrasion cycle with before/after evidence | HOLD / NOT RUN |
| D-P03 | G-D2 / edge-fixing-corrosion | real assembly mockup; edge, fixing, water path, corrosion/loosening observation | HOLD / NOT RUN |
| D-P04 | G-D2 / replaceability-maintenance | removal/replacement rehearsal on real sample/mockup | HOLD / NOT RUN |
| D-P05 | G-D2 / R13 paper handling | real stock print/fold/carry/light-moisture handling | HOLD / NOT RUN |
| D-X01 | R06 field geometry / exact Science Hero | exact viewpoint + visible relation + Photo↔Diagram + professional evidence | HOLD / NO FIELD GEOMETRY |
| D-X02 | R13 safety/accessibility | field run for width, surface/wetness, level, rail, visibility, crowd, bypass/closure/accessibility | HOLD / NOT RUN |

## Fail-closed acceptance logic

### G-D1
PASS is allowed only when the required real viewing/movement states show that W0/W1 outrank W2 where required, route/safety is unambiguous, Landscape First survives, and the core journey does not require a phone. Any result dependent on stopping, zooming, mandatory scanning or unsafe hesitation is REVISE/REJECT rather than PASS.

### G-D2
PASS is allowed only for the **specific sample and test condition actually run**. A dry/wet readability test does not prove abrasion, UV life, corrosion or fixing; an abrasion run does not prove unspecified lifetime; an assembly mockup does not prove structural/code compliance.

### R06 field geometry
The 2D Science Hero may only be promoted when the diagram corresponds to an actually visible/measured/verified relation at a real viewpoint and all scientific claims remain inside cited professional evidence. Broad contextual photography is insufficient for exact terrace geometry.

### R13 safety/accessibility
Any visual/digital/print layer must yield to safe passage, closure, bypass and accessibility. If an intervention causes stopping, obstruction, mandatory phone use or route conflict, it cannot pass.

## Same-iteration workbook QA

The overlay was actually written into the existing Drive workbook and then reviewed through connector readback.

- Native table present: `QJDFieldGatesTable`.
- Header row: `36 px`.
- Eleven data rows: `112 px` each.
- Long fields: `WRAP / TOP`.
- Expanded evidence/decision columns: `260 px`.
- Frozen header retained.
- Readback confirms all eleven Current State values remain HOLD; no field row was accidentally promoted.

## Promotion boundary

`FIELD PREP CLOSED` is a workflow-preparation state only. It is not a Design State promotion and not a Reality Gate PASS.

Current project state remains:

`Current Gate = G3 / Design State = CANDIDATE / Current Loop = Exploration / Final Visual Promotion = NO / Canonical Production Promotion = NO`.
