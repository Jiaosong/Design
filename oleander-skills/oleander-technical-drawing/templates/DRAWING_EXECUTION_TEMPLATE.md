# OLEANDER Technical Drawing — Execution Template

Use this template for substantial technical drawing work. Delete non-applicable fields; do not invent values to fill blanks.

## 1. DRAWING BRIEF

- Project / object ID:
- Drawing package ID:
- Discipline profile:
- Intended audience:
- Decision to be resolved:
- Declared status: `DESIGN STUDY / TECHNICAL EXPLANATION / COORDINATION / FABRICATION / CONSTRUCTION`
- Allowed use:
- Prohibited claim/use:
- Target output size / medium:
- Units:
- Current source authority revision:

## 2. AUTHORITY MATRIX

| domain | authority | revision/date | truth state | allowed use | conflict/open item |
|---|---|---|---|---|---|
| geometry | | | | | |
| dimensions | | | | | |
| site/context | | | | | |
| structure/support | | | | | |
| material/CMF | | | | | |
| safety/access | | | | | |
| manufacturer/system | | | | | |

## 3. VIEW SET

| view_id | type | parent_id | decision/question | scale/NTS | source geometry | required child/detail |
|---|---|---|---|---|---|---|
| | GA/PLAN/SECTION/DETAIL/... | | | | | |

## 4. DIMENSION REGISTER

| dim_id | view_id | description | value/range | unit | truth state | datum/interface | basis | sensitivity | close_by |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | VERIFIED/RECOMMENDED/RANGE/REF/FIELD VERIFY/TBD | | | | |

## 5. DETAIL / CONNECTION REGISTER

| detail_id | parent_view | technical question | interfaces shown | installation/maintenance issue | specialist-open item | status |
|---|---|---|---|---|---|---|
| | | | | | | |

## 6. MATERIAL / CMF REGISTER

| material_id | substrate | finish/process | state | drawing boundary | direction/property | source | open item |
|---|---|---|---|---|---|---|---|
| | | | APPROVED/CANDIDATE/PROVISIONAL | | | | |

## 7. REALITY CHECK

For each critical item:

| item_id | design action | system | standard/reference domain | recommended value/range | sensitive factors | field/engineer verify |
|---|---|---|---|---|---|---|
| | | | | | | |

## 8. GRAPHIC SYSTEM

- L1 CUT / PRIMARY FORM:
- L2 PRIMARY RELATION / STRUCTURE:
- L3 SECONDARY CONSTRUCTION / EDGE / INTERFACE:
- L4 DIMENSION / NOTE / HUMAN / MAINTENANCE:
- L5 CONTEXT / FIELD-OPEN SUPPORT:
- Existing/proposed state encoding:
- Hatch/material encoding:
- Typography roles:
- Color-independent semantics confirmed: `YES / NO`

## 9. OUTPUTS

- Editable source:
- Vector derivative:
- Preview:
- Manifest:
- Hash/bytes when required:
- Independent-open test:
- Round-trip/export comparison:

## 10. TD-G0…TD-G8 REVIEW

| gate | result | evidence | blocker / repair |
|---|---|---|---|
| TD-G0 Intent & Status | | | |
| TD-G1 Source Authority | | | |
| TD-G2 Geometry & Projection | | | |
| TD-G3 Dimensional Intent | | | |
| TD-G4 Construction & Assembly | | | |
| TD-G5 Design Quality & Readability | | | |
| TD-G6 Vector & Annotation Integrity | | | |
| TD-G7 Output & Round-trip | | | |
| TD-G8 Independent Review & Promotion | | | |

## 11. MULTI-SCALE DESIGN CRIT

- Thumbnail / distance verdict:
- Intended physical/display size verdict:
- Near-read/detail verdict:
- First-read subject:
- Information competing with subject:
- Missing technical evidence:
- Simplification that hides evidence:
- Highest-order repair:

## 12. FINAL STATUS

`KEEP / REVISE / REJECT / HOLD`

State separately:
- Drawing Design status:
- Engineering status:
- Field status:
- Fabrication/Construction permission:
- MAIN/Support presentation status:

Never collapse these into one PASS.