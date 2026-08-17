# OLEANDER Technical Drawing — 1:1 Reference Reconstruction Fidelity

Use this mode only when the task explicitly requires a professional drawing, board, detail, diagram or technical figure to be **reconstructed against a supplied reference**, including requests such as `1:1`, `pixel-level`, `像素级复刻`, `exact match`, `rebuild this drawing`, `match this sheet`, or `vectorize while preserving appearance`.

This is an optional mode inside `oleander-technical-drawing`; it is not a separate Skill and it does not change technical authority.

`REFERENCE FIDELITY != TECHNICAL TRUTH`

`PIXEL MATCH != VECTOR / EDITABILITY`

`PIXEL MATCH != ENGINEERING / FIELD / FABRICATION / CONSTRUCTION APPROVAL`

A visually exact reconstruction may still be technically wrong for the current project. A technically correct adaptation may intentionally differ from the reference and therefore fail reconstruction fidelity. Review these tracks separately.

---

## 0. Reconstruction intent

Declare one mode before work starts:

- `EXACT RECONSTRUCTION` — reproduce the visible reference as closely as reasonably possible within the declared scope. Do not redesign or “improve” it unless the user separately asks for adaptation.
- `STRUCTURAL RECONSTRUCTION` — recover editable hierarchy, geometry, typography, symbols and layout while accepting small renderer-level differences.
- `SYSTEM EXTRACTION` — study the reference to extract reusable drawing rules; the output is not claimed to be a visual duplicate.
- `PROJECT ADAPTATION` — use the reference system on different authoritative project geometry/content. Similarity is secondary to project truth.

Never silently switch from `EXACT RECONSTRUCTION` to “inspired by”. Never call a project adaptation a pixel replica.

---

## 1. Reference source classes

Classify the supplied reference before measuring fidelity.

### R0 — native/vector authority available
Examples: DWG/DXF/SVG/AI, editable PDF, exported vector PDF with preserved text/paths.

Use object/vector comparison first. Raster pixel comparison is a derivative check.

### R1 — clean digital raster
Examples: direct PNG/TIFF/JPEG export or screenshot with known canvas and no perspective distortion.

Pixel registration can be meaningful after crop, size, background and color-mode normalization.

### R2 — scan / photographed sheet
Examples: scanned print, phone photograph, oblique photo, warped paper.

Deskew/dewarp/perspective correction may be required before reconstruction. Preserve the untouched original and record the correction transform. Do not claim original CAD scale or geometry from pixels alone.

### R3 — partial / compressed / low-resolution reference
Examples: web thumbnail, social-media compression, cropped screenshot.

Fidelity claims must be scoped to recoverable features. Sub-pixel typography, thin line classes, hatch pitch and exact dimensions may be unknowable.

### R4 — stylistic or non-authoritative imagery
Examples: render, AI image, mood reference, editorial image.

May guide visible graphic treatment only. It cannot become technical geometry/dimension/connection authority.

Record: source ID, file identity/hash when available, dimensions, color mode, DPI metadata if meaningful, crop state, rotation/perspective state and known provenance.

---

## 2. Reconstruction scope contract

Before redrawing, create `RECONSTRUCTION_SCOPE`:

- reference source class;
- full-sheet or named ROI scope;
- target page/canvas size;
- target physical size and DPI when raster comparison matters;
- required editable format;
- typography requirement: exact font / licensed available font / declared substitute;
- whether raster context imagery is in scope;
- whether original content itself is authoritative or only visually referenced;
- exclusions and unknowns;
- acceptance method and reviewer.

A partial reconstruction must name its ROIs. Do not report a global “99% match” when large portions were intentionally excluded.

---

## 3. Normalize before comparing

Pixel comparison is meaningless until both images share the same comparison frame.

Lock:

1. page/canvas width and height;
2. crop and page origin;
3. orientation/rotation;
4. scale / output pixel dimensions;
5. background treatment and alpha compositing;
6. color mode and alpha handling;
7. rasterizer and DPI where possible;
8. font environment and font rendering path where possible.

For scans/photos, create a recorded `NORMALIZATION_TRANSFORM` rather than destructively replacing the original.

Do not use free perspective/warp to hide reconstruction errors. Registration may correct the reference capture; it must not distort the candidate geometry simply to reduce pixel difference.

---

## 4. Anchor hierarchy — reconstruct structure before pixels

Use a hierarchical anchor register. Repair higher-order anchors before local styling.

### A0 — page / frame anchors
- sheet edge / artboard;
- drawing frame / title-block boundary;
- page origin;
- major margins;
- principal grid/rail boundaries.

### A1 — major view anchors
- plan/section/elevation bounding fields;
- section cuts and datums;
- dominant view centerlines;
- main detail frames;
- baseline relationships between views.

### A2 — technical geometry anchors
- primary profiles / cut silhouettes;
- principal axes;
- interfaces, joints and critical edge conditions;
- dimension datums and leader targets.

### A3 — typography anchors
- title and view-title baselines;
- note-column starts;
- dimension text positions;
- line breaks and text-box measures;
- alignment and reading direction.

### A4 — stroke / pattern / symbol anchors
- lineweight classes;
- dash pattern and phase where visually significant;
- hatch pitch/angle/origin;
- arrowheads, ticks, section marks, level marks, callout symbols;
- fill/tone boundaries.

### A5 — raster/context anchors
- image crop;
- image mask;
- opacity/blend;
- position relative to vector geometry.

Do not tune A4/A5 while A0–A2 are visibly wrong. A perfectly matched hatch cannot rescue a shifted section.

---

## 5. Vector reconstruction rules

The reconstructed asset must be genuinely editable when editability is required.

- technical text stays text unless delivery explicitly requires outlines;
- dimensions, leaders, symbols and linework remain vector;
- repeated symbols use reusable definitions/components when supported;
- layers/groups use stable semantic names rather than one flattened path cloud;
- a raster copy of the reference hidden inside SVG/PDF does not count as reconstruction;
- automatic tracing may be used as a temporary extraction aid, but noisy traced paths are not accepted as final professional geometry;
- when the source is vector, preserve object logic where recoverable instead of rebuilding everything from raster pixels;
- reconcile any hand-refined vector against source/reference anchors after editing.

Suggested semantic groups:

`FRAME / PRIMARY_GEOMETRY / SECONDARY_GEOMETRY / CUT / HATCH / DIMENSIONS / CALLOUTS / TEXT / SYMBOLS / CONTEXT_RASTER / METADATA`.

---

## 6. Typography forensic protocol

Typography often prevents a visually close sheet from becoming a convincing reconstruction.

Record in `TYPOGRAPHY_REGISTER`:

- family / candidate family;
- weight/style;
- font size;
- line height;
- letter spacing/tracking;
- text-box width;
- alignment;
- baseline positions;
- paragraph and list spacing;
- CJK/Latin fallback behavior;
- exact / inferred / substituted state.

Rules:

1. Use the exact font only when available and permitted.
2. If unavailable, keep text editable and record substitution. A font substitution can be acceptable for structural reconstruction but remains a blocker for strict pixel fidelity when it materially changes glyph metrics.
3. Do not solve font mismatch by converting every label to raster.
4. Compare text as grouped ROIs, not only individual glyph pixels; antialiasing can differ between rasterizers.
5. A changed line break or baseline is a structural typography mismatch even when global image error remains low.

---

## 7. Stroke / hatch / symbol calibration

Create `STROKE_REGISTER` with role, visible weight, dash pattern, opacity/tone and truth role.

Calibrate in this order:

`ROLE → RELATIVE HIERARCHY → PHYSICAL/OUTPUT WEIGHT → DASH/PATTERN → TONE/COLOR`.

For a strict reconstruction, compare visible output weight at the target raster/print condition rather than assuming SVG/CAD numeric stroke width maps identically between renderers.

Hatches/patterns require:

- pitch;
- angle;
- pattern origin/phase where visible;
- clipping boundary;
- line class;
- grayscale density.

Do not reproduce a hatch that implies geology/material certainty in a project adaptation unless the current project evidence supports it. In exact reconstruction mode the hatch may be visually reproduced but must remain labelled as reference-derived if it is not current technical authority.

---

## 8. Difference analysis — use metrics diagnostically, not as one score

Always produce visual difference evidence when strict fidelity is requested:

- registered reference;
- candidate render;
- 50/50 overlay or blink comparison;
- absolute-difference image;
- changed-pixel mask at declared tolerance;
- ROI metrics for important regions;
- anchor displacement register.

Recommended diagnostic metrics:

- canvas match;
- exact-equal pixel ratio;
- changed-pixel ratio above declared channel tolerance;
- mean absolute channel error (MAE);
- RMSE;
- maximum error;
- optional percentile error;
- edge disagreement ratio;
- anchor displacement in px and normalized page units;
- baseline displacement for text groups;
- lineweight-class mismatch count;
- ROI-specific versions of the above.

Do **not** define one universal “95% = PASS” rule. Different rasterizers, font hinting, antialiasing, color management, JPEG artifacts and scans can create pixel differences without meaningful geometric differences.

The acceptance contract must state which metrics matter for this reference class and output condition.

---

## 9. Reconstruction repair loop

Use this fixed loop:

`SOURCE SNAPSHOT → NORMALIZE → A0/A1 REGISTRATION → A2 GEOMETRY → A3 TYPOGRAPHY → A4 STROKE/HATCH/SYMBOL → A5 RASTER CONTEXT → SAME-SIZE RENDER → OVERLAY/DIFF → ROI DIAGNOSIS → ONE MATERIAL REPAIR → RE-RENDER`

Repair priority:

1. wrong canvas/crop/origin;
2. wrong major view position/scale;
3. wrong geometry/profile;
4. wrong typography measure/baseline;
5. wrong stroke hierarchy;
6. wrong dimensions/leaders/symbol placement;
7. wrong hatch/pattern/tone;
8. residual antialiasing/color-management noise.

Do not micro-tune antialiasing while the main view is 6 px out of place.

---

## 10. RF-G0…RF-G6 — optional fidelity gates

These gates activate only for reconstruction tasks and do not replace TD-G0…TD-G8.

### `RF-G0 / REFERENCE IDENTITY`
PASS when the exact reference file/snapshot, source class, crop/state and reconstruction scope are bound.

Blockers: unknown source version; comparing against a changing screenshot; missing scope; source raster embedded as “reconstruction”.

### `RF-G1 / CANVAS & REGISTRATION`
PASS when reference and candidate share declared comparison canvas/origin/orientation/scale and any scan/photo normalization is documented.

Blockers: uncontrolled crop; hidden perspective warp; mismatched output size; false scale claim.

### `RF-G2 / VECTOR STRUCTURE & GEOMETRY ANCHORS`
PASS when required visible geometry is independently reconstructed/editable and A0–A2 anchors are within the project-specific tolerance.

Blockers: major view drift; flattened raster substitute; geometry distorted only to reduce diff; parent/detail relation lost.

### `RF-G3 / TYPOGRAPHY & ANNOTATION`
PASS when typography hierarchy, baselines, text measures, dimensions, leaders and symbols visually align within declared scope while preserving editability.

Blockers: material font substitution in strict mode; changed line breaks; rasterized pseudo-text; orphaned leaders.

### `RF-G4 / STROKE, HATCH & SYMBOL FIDELITY`
PASS when relative/visible line classes, patterns and symbols match the reference at target output condition without erasing technical semantics.

Blockers: line hierarchy collapse; hatch phase/pitch materially wrong; symbol shape/scale mismatch; color-only recovery of a stroke error.

### `RF-G5 / PIXEL & ROI READBACK`
PASS when overlay/diff/ROI evidence shows no unresolved material visual mismatch under the declared acceptance contract.

Blockers: no same-size render; only subjective side-by-side review; global metric hides a failed critical ROI; unexplained large difference clusters.

### `RF-G6 / FIDELITY TRUTH BOUNDARY & INDEPENDENT REVIEW`
PASS when reviewers can distinguish `REFERENCE MATCH` from technical authority and the producer does not self-award final reconstruction/design promotion.

Blockers: reference match promoted into current engineering/site truth; producer self-KEEP; technical errors copied from the reference without disclosure in a project adaptation.

`RF PASS != TD PASS` and `TD PASS != RF PASS`.

---

## 11. Fidelity output contract

When strict reconstruction mode is active, add to the normal drawing package:

- `REFERENCE_SNAPSHOT` — immutable reference identity/hash or exact file revision;
- `RECONSTRUCTION_SCOPE` — mode, source class, full/ROI scope, target size, exclusions;
- `NORMALIZATION_TRANSFORM` — crop/rotation/dewarp/perspective record if used;
- `ANCHOR_REGISTER` — A0…A5 anchor coordinates and deltas;
- `TYPOGRAPHY_REGISTER`;
- `STROKE_REGISTER`;
- `FIDELITY_METRICS.json`;
- registered reference preview;
- candidate preview;
- overlay preview;
- difference image;
- changed-pixel mask;
- ROI report when applicable;
- `RF-G0…RF-G6` review state;
- normal `TD-G0…TD-G8` review state separately.

Preview/diff rasters are review evidence only. They do not replace the editable drawing source.

---

## 12. What “pixel-level” means by source class

### Vector/CAD/PDF reference
Target: object/geometry fidelity first, then pixel agreement at a locked renderer/output condition. This is the strongest reconstruction condition.

### Clean digital raster
Target: same-canvas geometry, typography and visible stroke/pattern agreement; pixel metrics are meaningful after normalization.

### Scan/photo
Target: registered visual geometry and typography after documented capture correction. Exact original vector geometry, physical lineweight and scale are not proven unless separately calibrated.

### Low-resolution/compressed image
Target: structural and visible-form fidelity within recoverable resolution. Do not invent microscopic details that cannot be observed.

---

## 13. Project adaptation boundary

When a professional reference is being used to improve an OLEANDER project rather than literally reproduce the reference:

- copy **operations and systems**, not unsupported project facts;
- current project geometry/dimensions/material/engineering/site authority always wins;
- preserve the reference's useful hierarchy, proportion, annotation rhythm and technical graphic logic only where compatible;
- document deliberate deviations from the reference as `PROJECT TRUTH OVERRIDE` or `DESIGN ADAPTATION`;
- never distort current project geometry to obtain a lower reference pixel-diff score.

A project adaptation may deliberately score worse on RF gates and better on TD gates. That is correct when the reference conflicts with project truth.

---

## 14. Acceptance language

Use precise status language:

- `REFERENCE MATERIALIZED`
- `CANVAS REGISTERED`
- `VECTOR RECONSTRUCTED`
- `FIDELITY SELF-CHECKED`
- `FIDELITY REVIEW PENDING`
- `REVISE — GEOMETRY`
- `REVISE — TYPOGRAPHY`
- `REVISE — STROKE/PATTERN`
- `REJECT — RASTER SUBSTITUTE`
- `HOLD — REFERENCE QUALITY INSUFFICIENT`

Do not use `PIXEL PERFECT`, `1:1 PASS` or `EXACT REPLICA` unless the declared comparison process and independent review actually support that claim.
