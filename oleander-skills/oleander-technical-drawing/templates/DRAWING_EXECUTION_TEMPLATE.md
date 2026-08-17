# OLEANDER Technical Drawing — Execution Template

Use this template for substantial technical drawing work. Delete non-applicable fields; do not invent values to fill blanks.

When the task is an explicit 1:1 / pixel-level / exact reference reconstruction, also use `references/REFERENCE_RECONSTRUCTION_FIDELITY.md` and complete the optional Section 9A. Reconstruction fidelity gates never replace TD-G0…TD-G8.

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

## 9A. OPTIONAL REFERENCE RECONSTRUCTION FIDELITY

Complete only for `EXACT RECONSTRUCTION / STRUCTURAL RECONSTRUCTION / SYSTEM EXTRACTION / PROJECT ADAPTATION` work.

- Reconstruction mode:
- Reference source class: `R0 / R1 / R2 / R3 / R4`
- Reference file / revision / SHA-256:
- Full-sheet or ROI scope:
- Target canvas / physical size / DPI:
- Editable target format:
- Reference authority role: `VISUAL REFERENCE / TECHNICAL AUTHORITY / MIXED`
- Font state: `EXACT / INFERRED / SUBSTITUTED`
- Normalization transform: crop / rotate / deskew / dewarp / none
- Acceptance contract / reviewer:

### Anchor register

| anchor_id | class | reference position/measure | candidate position/measure | delta | tolerance | result |
|---|---|---|---|---|---|---|
| | A0/A1/A2/A3/A4/A5 | | | | | |

### Typography register

| text_id | role | family/state | size | baseline/box | line break | delta/open item |
|---|---|---|---|---|---|---|
| | | | | | | |

### Stroke / hatch / symbol register

| style_id | role | reference visible class | candidate class | pattern/symbol | mismatch/open item |
|---|---|---|---|---|---|
| | | | | | |

### Fidelity evidence

- Registered reference preview:
- Same-size candidate preview:
- 50/50 overlay:
- Absolute-difference image:
- Changed-pixel mask + declared tolerance:
- `FIDELITY_METRICS.json`:
- ROI report:

### RF-G0…RF-G6

| gate | result | evidence | blocker / repair |
|---|---|---|---|
| RF-G0 Reference Identity | | | |
| RF-G1 Canvas & Registration | | | |
| RF-G2 Vector Structure & Geometry Anchors | | | |
| RF-G3 Typography & Annotation | | | |
| RF-G4 Stroke, Hatch & Symbol Fidelity | | | |
| RF-G5 Pixel & ROI Readback | | | |
| RF-G6 Fidelity Truth Boundary & Independent Review | | | |

State explicitly: `RF PASS != TD PASS` and `TD PASS != RF PASS`.

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
- Reference-fidelity status when applicable:
- Drawing Design status:
- Engineering status:
- Field status:
- Fabrication/Construction permission:
- MAIN/Support presentation status:

Never collapse these into one PASS.