# OLEANDER Technical Drawing — Execution Template

Use this template for substantial technical drawing work. Delete non-applicable fields; do not invent values to fill blanks.

When the task is an explicit 1:1 / pixel-level / exact reference reconstruction, use both `references/REFERENCE_RECONSTRUCTION_FIDELITY.md` and `references/PIXEL_FORENSIC_PROTOCOL.md`, then complete Section 9A. Reconstruction fidelity gates never replace TD-G0…TD-G8.

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

### Claim level

- Reconstruction mode:
- Current fidelity claim: `RF-C0 STRUCTURAL / RF-C1 GEOMETRIC / RF-C2 RENDER-LOCKED HIGH FIDELITY / RF-C3 PIXEL-EXACT CANDIDATE`
- Reference source class: `R0 / R1 / R2 / R3 / R4`
- Reference file / revision / SHA-256:
- Full-sheet or ROI scope:
- Target canvas / physical size / DPI:
- Editable target format:
- Reference authority role: `VISUAL REFERENCE / TECHNICAL AUTHORITY / MIXED`
- Font state: `EXACT / INFERRED / SUBSTITUTED`
- Normalization transform: crop / rotate / deskew / dewarp / none
- Acceptance contract / reviewer:

### Render environment lock

- Renderer + exact version:
- OS/runtime where rendering depends on it:
- Canvas px:
- DPI/export scale:
- Alpha/background rule:
- Color-space/profile rule:
- Antialiasing setting/path:
- Font face identity/hash register:
- CJK/Latin shaping/fallback chain:
- Supersampling factor when used:
- Downsample filter/path:
- Browser engine/version when relevant:
- Environment-lock SHA/identity:

Any material change above invalidates previous RF-C3 evidence.

### Reference normalization / candidate registration

- Untouched reference preserved: `YES / NO`
- Reference capture rectification:
- Candidate registration transform:
- Non-uniform scale/warp used on candidate: must be `NO` for exact reconstruction
- Estimated residual whole-page translation dx/dy before repair:
- Registration evidence:

### Anchor register

| anchor_id | class | criticality | reference position/measure | candidate position/measure | delta px/page-unit | tolerance | result |
|---|---|---|---|---|---|---|---|
| | A0/A1/A2/A3/A4/A5 | CRITICAL/MAJOR/SUPPORT | | | | | |

### Sub-pixel anchor register

| anchor_id | centerline/page coordinate | target raster phase | supersample evidence | final target-render result |
|---|---|---|---|---|
| | | | | |

### Object forensic register

| object_id | role | criticality | ref bbox | cand bbox | centroid delta | visible thickness/coverage | parent/group | result |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

### Typography forensic register

| text_id | exact string | face/state | size | start x | baseline y | run width | line box | line break | tracking/shaping | delta/open item |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |

For RF-C3, unresolved exact font/shaping mismatch is a blocker rather than a percentage deduction.

### Stroke / hatch / symbol register

| style_id | role | reference visible class | candidate class | centerline | visible thickness samples | dash/phase | hatch period/origin | symbol endpoint/bbox | mismatch/open item |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

### Critical ROI contract

| roi_id | role | criticality | bounds | RF-C2 threshold | RF-C3 threshold | result |
|---|---|---|---|---|---|---|
| | PAGE_FRAME/PRIMARY_VIEW/PRIMARY_GEOMETRY/TITLE/DIMENSIONS/CALLOUT/TITLE_BLOCK/HATCH | CRITICAL/MAJOR/SUPPORT | | | default zero unexplained difference | |

### Fidelity evidence

- Registered reference preview:
- Same-size candidate preview:
- 50/50 overlay:
- Absolute-difference image:
- Changed-pixel mask at tolerance 0:
- `FIDELITY_METRICS.json`:
- Critical ROI report:
- Whole-page residual translation estimate:
- Edge disagreement r0 / r1 / r2:
- Top mismatch tiles / heat concentration:
- Changed-pixel bounding box:
- Row/column mismatch peaks:
- Source-noise/exclusion masks and pre-declared rationale:

### Layer freeze / repair register

| layer | state | blocker | last material repair | rerender evidence |
|---|---|---|---|---|
| E0 Canvas | OPEN/FROZEN | | | |
| E1 Major View | OPEN/FROZEN | | | |
| E2 Primary Geometry | OPEN/FROZEN | | | |
| E3 Typography | OPEN/FROZEN | | | |
| E4 Stroke/Symbol/Dimensions | OPEN/FROZEN | | | |
| E5 Hatch/Tone/Raster Context | OPEN/FROZEN | | | |
| E6 Render Residual | OPEN/EXPLAINED/ZERO | | | |

Changing an earlier frozen layer reopens its dependent later layers.

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

### RF-C3 hard condition

Do not write `PIXEL-EXACT / 像素级一致` unless the final locked-environment comparison uses tolerance `0` and reports zero unexplained changed pixels for every declared in-scope pixel. If exclusions exist, the claim must be scoped to the non-excluded region and must not be described as whole-page pixel-exact.

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
- Reference-fidelity status:
- RF-C0…RF-C3 claim level:
- Drawing Design status:
- Engineering status:
- Field status:
- Fabrication/Construction permission:
- MAIN/Support presentation status:

Never collapse these into one PASS.