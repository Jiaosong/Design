# OLEANDER Technical Drawing — Pixel Forensic Reconstruction Protocol

Status: `v0.3 CANDIDATE / PR #172 / RECONSTRUCTION SUBSYSTEM`

Use this reference only when the user explicitly asks for `像素级 / pixel-level / pixel perfect / exact replica / 1:1 reconstruction` or when an independent review says the current reconstruction is visually close but not exact enough.

This protocol tightens `REFERENCE_RECONSTRUCTION_FIDELITY.md`. It does not create a new Skill.

`PIXEL-EXACT CLAIM = LOCKED RENDER ENVIRONMENT + ZERO UNEXPLAINED IN-SCOPE PIXEL DIFFERENCE`

`GLOBAL SIMILARITY PERCENTAGE IS NOT AN ACCEPTANCE GATE.`

`REFERENCE FIDELITY != TECHNICAL TRUTH != DESIGN KEEP.`

---

## 1. Fidelity claim levels

Every reconstruction must state exactly one current claim level. Do not say “pixel-level” without one of these states.

### `RF-C0 / STRUCTURAL RECONSTRUCTION`
Editable object hierarchy, page composition, major geometry, text blocks, line classes and symbols are reconstructed. Pixel equality is not claimed.

### `RF-C1 / GEOMETRIC FIDELITY`
A0–A2 geometry anchors are measured and reconciled. Critical geometry is within the declared geometric tolerance. Typography/stroke rasterization may still differ.

### `RF-C2 / RENDER-LOCKED HIGH FIDELITY`
Reference and candidate are compared under a locked render environment. Remaining differences are isolated, classified and judged non-material for the declared scope. This level may still contain renderer/font antialiasing residuals and therefore must not be called pixel-exact.

### `RF-C3 / PIXEL-EXACT`
This claim is allowed only when all of the following are true:

1. same comparison canvas, crop, origin, scale and orientation;
2. same declared rasterizer/render engine and version where controllable;
3. same target pixel dimensions and DPI interpretation;
4. same alpha/background compositing rule;
5. same color space/profile handling for the comparison path;
6. exact required fonts are available and the shaping/fallback path is locked;
7. candidate is independently editable/vector where required and does not embed the reference as a hidden substitute;
8. `tolerance = 0` for the final RF-C3 comparison;
9. `changed_pixel_ratio = 0` for every in-scope pixel, or every non-zero pixel belongs to an explicitly excluded source-noise/raster-context mask declared before the final run;
10. all A0–A4 anchors have zero unresolved displacement at target rasterization;
11. no critical ROI relies on a global average to hide local error;
12. independent review confirms that the comparison setup itself is not gaming the result.

If any item above is not verifiable, the maximum claim is RF-C2. Do not soften RF-C3 with “99.8% pixel perfect”.

---

## 2. Render environment lock

Before micro-adjustment, create `RENDER_ENVIRONMENT_LOCK.json` containing at least:

- renderer name and exact version;
- operating-system family/version when it affects text rendering;
- SVG/PDF renderer path;
- target canvas width/height;
- DPI/export scale;
- alpha/background rule;
- RGB/color-profile rule;
- antialiasing setting when controllable;
- font family names and exact font file identity/hash when legally and technically available; record hashes/identity only, never distribute font files as part of the Skill;
- CJK/Latin shaping/fallback chain;
- downsampling filter if supersampling is used;
- browser engine/version when browser rasterization is the comparison authority.

Changing any locked item invalidates prior RF-C3 evidence and requires a new comparison run.

A renderer mismatch is not repaired by moving geometry until the images look closer. First lock the environment, then adjust the candidate.

---

## 3. Reference normalization is one-way

Separate two operations:

### `CAPTURE RECTIFICATION`
Allowed only on the reference when the source is a scan/photo and the transform corrects capture distortion. Record the transform matrix/parameters and preserve the untouched source.

### `CANDIDATE REGISTRATION`
May use only the declared page/canvas transform needed to place candidate and reference in the same coordinate frame. It must not use local warp, perspective deformation, non-uniform scaling or per-region alignment to hide reconstruction errors.

For clean digital R0/R1 references in exact mode, default candidate registration is identity after page/canvas setup.

Report the estimated residual translation before any candidate edit. An unexplained whole-page translation is an A0/A1 failure, not an antialiasing issue.

---

## 4. Coordinate system and sub-pixel authoring

Pixel-exact output often requires sub-pixel vector coordinates even when the final raster is integer pixels.

Rules:

- author geometry using floating-point coordinates; do not round every anchor to integers;
- record page-space coordinates independently from raster-space coordinates;
- where stroke centering matters, record centerline coordinate and visible raster coverage separately;
- do not infer SVG/CAD stroke width solely from black-pixel thickness; antialiasing and stroke alignment change visible coverage;
- for 1 px/odd-pixel strokes, test half-pixel centerline placement under the locked renderer rather than assuming integer placement;
- use 4× or 8× diagnostic supersampling when necessary to resolve whether a mismatch is true geometry or sampling-phase error;
- final RF-C3 comparison is still performed at the declared target raster size with the locked downsampling/render path.

Create `SUBPIXEL_ANCHOR_REGISTER` for any anchor whose final position depends on <1 px adjustment.

---

## 5. Object forensic register

For every visually important object or repeated class, measure the visible reference before rebuilding. Do not rely on eyeballing.

Required fields where applicable:

| field | purpose |
|---|---|
| object_id | stable comparison identity |
| role | frame/view/geometry/text/dimension/symbol/hatch/context |
| bbox_ref | x/y/w/h reference bounding box |
| bbox_candidate | x/y/w/h candidate bounding box |
| centroid_delta | local placement error |
| edge_orientation | horizontal/vertical/angled/curve |
| centerline | reconstructed vector axis where applicable |
| visible_thickness_samples | raster coverage measured across multiple perpendicular scans |
| fill/tone | visible output value/color |
| parent/group | hierarchy/context |
| criticality | CRITICAL / MAJOR / SUPPORT |
| tolerance_contract | permitted mismatch for current claim level |

For repeated items, sample multiple instances. One matched line cannot prove the whole line class.

---

## 6. Typography forensic register — stricter than style matching

For RF-C3, font family and nominal point size are insufficient. Record per text run:

- exact string, including punctuation/full-width/half-width forms;
- font family and exact face/weight;
- shaping engine/fallback path when relevant;
- font size;
- baseline y;
- start x;
- advance width of the complete run;
- visible glyph bounding box;
- line box width/height;
- line height/leading;
- tracking/letter spacing;
- word spacing where non-default;
- alignment mode;
- text-anchor/justification;
- line breaks;
- CJK punctuation behavior;
- superscript/subscript/baseline shift;
- rotation;
- fill/opacity.

Strict order of repair:

`STRING → FONT FACE → SIZE → SHAPING/FALLBACK → RUN WIDTH → BASELINE → LINE BREAK → TRACKING → LOCAL GLYPH RESIDUAL`.

Do not compensate for a wrong font by distorting text horizontally or converting it to raster while claiming editable reconstruction.

If the exact font face or shaping path is unavailable and the difference is material, RF-G3 = HOLD and RF-C3 is unavailable.

---

## 7. Stroke forensic protocol

For every line class:

1. identify semantic role;
2. sample several clean straight segments away from intersections;
3. measure visible raster coverage with perpendicular profiles;
4. infer candidate centerline and nominal vector width;
5. render under locked environment;
6. compare edge positions and coverage;
7. adjust centerline before changing width when both edges move in the same direction;
8. adjust width when the centerline matches but both edges expand/contract symmetrically.

Record at least median visible thickness and variation across samples.

For dashes, additionally lock:

- dash length;
- gap length;
- dash offset/phase;
- line cap;
- line join;
- miter limit where visible.

A visually wrong dash phase is an A4 failure even when the total dark-pixel count is correct.

---

## 8. Hatch / pattern forensic protocol

For periodic patterns record:

- angle;
- pitch/period;
- line width;
- phase/origin;
- clipping boundary;
- pattern transform;
- opacity/tone;
- overlap/order with boundary lines.

Match phase/origin after pitch and angle. A hatch can have the correct density but still create large pixel difference because its origin is shifted.

Where a hatch is only a visual reference and not current project truth, fidelity review remains separate from TD truth review.

---

## 9. Symbols, arrows and dimension terminals

Do not approximate these as generic icons.

Measure:

- bounding box;
- tip/endpoint coordinate;
- angle;
- shaft length;
- head length/width;
- stroke/fill;
- cap/join;
- label-to-symbol offset;
- rotation origin;
- repeated-instance consistency.

For dimensions, the terminal-to-extension-line relation is CRITICAL. A dimension whose text is aligned but arrow tips miss their reference edges is not a faithful reconstruction.

---

## 10. Pixel-difference decomposition

A single absolute-difference image is insufficient. The diagnostic tool/output must distinguish at least:

1. **whole-page translation suspicion** — estimated residual dx/dy;
2. **edge disagreement at 0 px**;
3. **edge disagreement after allowing 1 px neighborhood**;
4. **edge disagreement after allowing 2 px neighborhood**;
5. **critical ROI difference**;
6. **top mismatch tiles / spatial heat concentration**;
7. **changed-pixel bounding box**;
8. **row/column mismatch peaks**;
9. **exact pixel difference at tolerance 0**;
10. **declared source-noise/exclusion mask contribution**, if any.

Interpretation examples:

- large r0 edge error collapsing at r1 = likely 1 px placement/sampling phase problem;
- r0/r1/r2 all high = true geometry/stroke/form mismatch;
- high title ROI with low geometry ROI = typography problem, not global layout problem;
- narrow row/column peak = baseline/frame/long-line displacement;
- diffuse low-amplitude color residual = renderer/color-management issue only after geometry is proven aligned.

Do not average these failure modes together.

---

## 11. Critical ROI contract

Every exact reconstruction must define critical ROIs before final tuning.

Minimum recommended classes:

- `PAGE_FRAME`
- `PRIMARY_VIEW`
- `PRIMARY_GEOMETRY`
- `TITLE / VIEW TITLES`
- `DIMENSION_SYSTEM`
- `CALLOUT / SYMBOL SYSTEM`
- `TITLE_BLOCK / METADATA`
- `HATCH / MATERIAL REGION` where relevant.

Each ROI may declare hard conditions. Example:

```json
{
  "id": "PRIMARY_GEOMETRY",
  "criticality": "CRITICAL",
  "rf_c3": {
    "max_changed_pixel_ratio": 0.0,
    "max_edge_unmatched_ratio_r0": 0.0
  }
}
```

For RF-C3 the default in-scope critical ROI condition is zero unexplained difference. Relaxed thresholds belong to RF-C2, not RF-C3.

---

## 12. Error budget by layer

Do not spend time micro-tuning lower layers while a higher layer is outside tolerance.

Repair order and freeze rule:

1. `E0 CANVAS` — freeze after exact page/crop/origin match;
2. `E1 MAJOR VIEW` — freeze after view boxes/datum axes match;
3. `E2 PRIMARY GEOMETRY` — freeze after critical edges/curves match;
4. `E3 TYPOGRAPHY` — freeze after run widths/baselines/line breaks match;
5. `E4 STROKE / SYMBOL / DIMENSIONS` — freeze after visible coverage and endpoints match;
6. `E5 HATCH / TONE / RASTER CONTEXT` — freeze after phase/tone/crop match;
7. `E6 RENDER RESIDUAL` — diagnose only after E0–E5 are frozen.

A material change to an earlier layer unfreezes all dependent later layers and requires rerendering.

---

## 13. Iteration stop conditions

### Stop as `REVISE`
Stop the current micro-pass and return to the responsible layer when:

- estimated residual translation is non-zero and unexplained;
- any CRITICAL A0–A2 anchor is outside its contract;
- font identity/shaping is unresolved in exact mode;
- changed pixels form a coherent cluster on a critical edge/text baseline/symbol endpoint;
- a lower-layer tweak increases error in a previously frozen higher layer.

### Stop as `RF-C2 / REVIEW PENDING`
Allowed when the locked environment still produces residuals that are demonstrated to be renderer/source noise and no meaningful geometry/typography/stroke mismatch remains. Residuals must be spatially localized and explained.

### Stop as `RF-C3 CANDIDATE / INDEPENDENT REVIEW PENDING`
Only when final tolerance-0 comparison returns zero unexplained in-scope changed pixels and all structural/vector requirements pass.

The producer still does not self-award final KEEP or promotion.

---

## 14. Source-noise and exclusion masks

Masks are dangerous because they can hide failure. Therefore:

- define masks before final candidate tuning;
- name every mask and explain why the source region is not reconstructable or intentionally excluded;
- masks may cover photographic/raster context, compression noise or intentionally out-of-scope content;
- masks must not cover primary geometry, technical text, dimensions, symbols or other content merely because it is difficult to match;
- report both raw full-frame difference and in-scope masked difference;
- any mask added after seeing a mismatch requires independent reviewer scrutiny.

RF-C3 may only apply to the declared in-scope pixels; it must never be reported as whole-page pixel-exact if excluded pixels exist.

---

## 15. Reconstruction implementation order

For high-end professional drawing replication use this concrete order:

`REFERENCE SNAPSHOT → RENDER ENV LOCK → REFERENCE RECTIFICATION → CANVAS REGISTER → OBJECT INVENTORY → A0/A1 ANCHORS → A2 PRIMARY GEOMETRY → SUBPIXEL CALIBRATION → A3 TYPOGRAPHY FORENSICS → DIMENSION/SYMBOL ENDPOINTS → A4 STROKE FORENSICS → HATCH PHASE → A5 RASTER CONTEXT → TARGET-SIZE RENDER → TOLERANCE-0 DIFF → EDGE-RADIUS DIAGNOSTICS → ROI/HEATMAP DIAGNOSIS → REPAIR ONE LAYER → RERENDER → FREEZE LAYER → FINAL RF CLAIM`

Do not jump directly from reference image to hand-tuned SVG styling.

---

## 16. Mandatory evidence for any “pixel-level” claim

A response or artifact may use the phrase `pixel-exact / 像素级一致` only when the package contains:

- immutable reference identity;
- render environment lock;
- exact target canvas;
- editable candidate source;
- object/anchor register;
- typography register;
- stroke/symbol register where applicable;
- tolerance-0 final comparison;
- changed-pixel mask;
- edge-radius metrics;
- critical ROI report;
- exclusion-mask report if used;
- RF-C0…RF-C3 current claim;
- RF-G0…RF-G6 state;
- separate TD-G0…TD-G8 state;
- independent-review state.

Without these, use `high-fidelity reconstruction` or `structural reconstruction`, not `pixel-exact`.
