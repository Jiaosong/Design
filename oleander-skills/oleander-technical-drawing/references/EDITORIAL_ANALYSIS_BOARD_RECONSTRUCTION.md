# OLEANDER Technical Drawing — Editorial Analysis Board Reconstruction

Status: `candidate extension / PR #172`

Use with `REFERENCE_RECONSTRUCTION_FIDELITY.md`, `MULTILAYER_RELATION_RECONSTRUCTION.md`, `SPATIAL_TRANSLATION_PROTOCOL.md` and `ANALYSIS_DRAWING_SYSTEM.md` when the reference is a **heterogeneous landscape / urban-design analysis board** rather than one drawing.

Typical boards mix:
- historic/background evidence;
- demographic or quantitative charts;
- transport / land-use / green-system maps;
- one dominant site synthesis plan;
- repeated problem maps;
- site photographs;
- planning-problem icons;
- theory/concept diagrams;
- project vision or design proposition.

The board is not a collage. It is an argument.

`PIXEL PANEL != ANALYTICAL CLAIM`

`PANEL TITLE != PANEL PURPOSE`

`MANY SMALL DIAGRAMS != DEEP ANALYSIS`

`VISUAL SIMILARITY != ARGUMENT RECONSTRUCTION`

`SOURCE TILE MOSAIC != SEMANTIC RECONSTRUCTION`

---

## 1. Reconstruct the board argument before panel styling

Create `BOARD_ARGUMENT_REGISTER` before micro-tracing.

For every major panel record:
- `panel_id`;
- visible title / recoverable title state;
- `panel_role`;
- `question_answered`;
- `claim`;
- `source_refs`;
- `carrier_family`;
- dominant spatial/data objects;
- relation to previous panel;
- relation to next panel;
- truth / inference state;
- whether the panel is required for the argument or only support;
- pixel-reconstruction state;
- semantic-reconstruction state.

Recommended panel roles:
- `BACKGROUND_EVIDENCE`;
- `CITY_SYSTEM_CONTEXT`;
- `SITE_SYNTHESIS`;
- `GROUND_PHOTO_AUDIT`;
- `PROBLEM_LAYER`;
- `TARGET_STRATEGY`;
- `THEORY_FRAME`;
- `DESIGN_PROPOSITION`;
- `VISION_CLOSE`.

A panel with no recoverable analytical purpose is not automatically part of the semantic rebuild merely because it occupies pixels in the reference.

---

## 2. Board reading chain

Many strong landscape/urban-design boards follow a reasoning sequence such as:

`BACKGROUND → CITY SYSTEMS → SITE CONDITION → GROUND EVIDENCE → PROBLEM → TARGET STRATEGY → THEORY / PRINCIPLE → PROJECT VISION`

This is not a universal content template. It is a diagnostic for reading the reference.

For exact reconstruction, preserve the reference's actual chain.
For project adaptation, do not import a chain that does not fit current evidence.

Create one `READING_CHAIN` and identify:
- where the board enters;
- where the dominant synthesis occurs;
- where evidence becomes diagnosis;
- where diagnosis becomes strategy;
- where theory is used as justification;
- where the board closes into a proposition.

If the board contains multiple chains, register them separately.

---

## 3. Dominant synthesis panel

Heterogeneous boards usually have one panel with much greater visual and analytical weight.

Examples:
- site-context/masterplan map;
- large section;
- strategy axon;
- composite hydrology/ecology plan.

Record:
- `dominant_panel_id`;
- area ratio relative to page;
- relationship to surrounding support panels;
- what information converges there;
- what must remain legible at 3-second read.

Do not equalize all panels during reconstruction. Making every panel the same visual weight destroys the source argument even if each panel is individually accurate.

---

## 4. Carrier families are heterogeneous

A board may intentionally use different carrier families because different questions require different spatial models.

Examples:
- history → chronological map series;
- demographics → graph / icon / density diagram;
- transport → network map;
- functional quarters → categorical area map;
- green open space → field / patch map;
- site synthesis → combined relational plan;
- flood risk → extent / gradient field;
- building use → categorical parcel/building map;
- ground condition → photographs;
- compact-city theory → ratio / proximity / walking-access diagram;
- waterfront theory → network + edge + public-space relation.

Do not normalize these into one generic diagram style.

`ONE BOARD SYSTEM != ONE CARRIER TYPE`

---

## 5. Repeated-base analysis maps

When several problem panels reuse the same site footprint—parking/vacancy, flood risk, building use, vegetation, ownership, etc.—treat them as a repeated-base family.

Use `BASE_GENEALOGY_REGISTER`:
- one site/base identity;
- repeated panel transforms;
- what each overlay changes;
- what stays constant;
- whether comparison depends on consistent orientation/extent.

Panel-by-panel redrawing that changes the base footprint invalidates comparative analysis.

---

## 6. Why-this-panel test

For each panel complete:

`SOURCE / CONDITION → WHY THIS CARRIER → WHAT IT SHOWS → WHAT DECISION IT ENABLES`

Examples:
- historic urban extension maps exist because the claim concerns **change through time**;
- transport map exists because access/connectivity is a **network problem**;
- green open-space map exists because continuity/deficit is a **field/patch problem**;
- serial photographs exist because map abstraction cannot prove **current ground material/edge condition**;
- flood-risk map exists because vulnerability is an **extent/field relation**;
- compact-city theory diagram exists to connect the site diagnosis to **density/mix/walkability principles**;
- waterfront-city theory diagram exists to justify **connected public waterfront + urban function**, not merely to decorate the footer.

If the producer cannot explain why the carrier type matches the question, reconstruction is `REVISE` even if the pixels are close.

---

## 7. R3 / low-resolution microtext policy

Dense boards are often supplied as social-media thumbnails where microtext is unreadable.

Rules:
1. Do not invent unreadable paragraphs, legends or numeric labels.
2. Mark text as `RECOVERABLE / PARTIAL / UNRECOVERABLE / SUBSTITUTE`.
3. A bounded source raster may remain as `CONTEXT_RASTER` for unrecoverable microtext or miniature cartography.
4. When a source raster carries unreadable text, create a separate semantic summary of the panel purpose; do not pretend the original copy has been reconstructed.
5. Exact typography/pixel claims for that ROI remain unavailable unless a higher-resolution source is obtained.
6. OCR failure does not authorize guessing.

`UNREADABLE SOURCE TEXT != PERMISSION TO WRITE PLAUSIBLE TEXT`

---

## 8. Dual-track reconstruction for boards

Maintain:

### `VISUAL_EXTRACTION_TRACK`
May use bounded source-derived raster carriers for maps, photographs and unrecoverable microtext while establishing panel geometry and pixel registration.

### `SEMANTIC_REBUILD_TRACK`
Must reconstruct:
- board argument;
- major panel roles;
- dominant synthesis relation;
- repeated-base genealogy;
- major analytical lines/nodes/fields where recoverable;
- major theory objects;
- titles and text that are recoverable/editable.

The two tracks may temporarily score differently.

A bounded source carrier is allowed as extraction/fidelity evidence, but:

`BOUNDED SOURCE RASTER != SEMANTIC COMPLETION`

`LOWER MAE FROM SOURCE CROP != BETTER EDITABLE RECONSTRUCTION`

The visible exact-fidelity candidate may use bounded source visual carriers while the semantic layer remains separate, but RF-C3 is unavailable if in-scope visible analytical content is still carried by the reference raster rather than independently reconstructed editable content.

---

## 9. Source-tile mosaic blocker

An exact or near-exact image can be produced by cutting the source board into tiles and reassembling them.

This is useful only as:
- registration control;
- crop/transform calibration;
- panel-boundary verification;
- extraction baseline.

It is not reconstruction.

Automatic blocker:

> if pixel equality is achieved primarily because the visible candidate reuses source raster tiles for the same analytical content, record `VISUAL EXTRACTION / SOURCE TILE CONTROL`, not `RF-C3`, `SEMANTIC VECTOR`, or professional editable completion.

The existence of many bounded crops instead of one full-sheet image does not change this rule.

---

## 10. Board-level fidelity metrics

In addition to full-page pixel metrics, record:
- major column/grid boundary displacement;
- dominant panel bbox/area ratio;
- inter-panel gutters;
- title hierarchy baselines;
- repeated-base transforms;
- panel-specific changed-pixel metrics;
- one critical semantic relation ROI per major analytical panel;
- 3-second reading-order check;
- grayscale hierarchy check.

Do not allow one large raster-perfect map to hide a failed theory/footer or title hierarchy.

---

## 11. Reconstruction acceptance ladder

`AB-C0 / PANEL SEGMENTED`
- major panels and page grid recovered.

`AB-C1 / BOARD ARGUMENT RESOLVED`
- panel purposes and reading chain registered.

`AB-C2 / CARRIER LOGIC RESOLVED`
- each major panel's carrier family matches the analytical question and source condition.

`AB-C3 / SEMANTIC BOARD REBUILT`
- dominant synthesis, repeated-base relations, major analytical objects, theory objects and recoverable text are editable/structured.

`AB-C3 != RF-C3 != DESIGN KEEP`.

---

## 12. Hard blockers

Automatic `REVISE / HOLD`:
- reconstructing each panel as a decorative card without recovering the board argument;
- visually equalizing a deliberately dominant site/masterplan panel;
- guessing unreadable microtext;
- redrawing repeated-base maps with drifting footprints/orientation;
- treating photographs as decoration when they are ground-condition evidence;
- theory diagrams copied as icons with no relation to the diagnosis;
- using one generic arrow grammar for transport, hydrology, chronology and causal reasoning;
- source tile mosaic presented as semantic or editable reconstruction;
- near-zero full-page pixel error used to override incomplete panel semantics;
- panel titles reconstructed but their actual claims/relations remain unknown.

Producer states remain `EXECUTED / SELF-CHECKED / REVIEW PENDING / REVISE / REJECT` only.