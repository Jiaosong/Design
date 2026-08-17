# REBIRTH editorial analysis-board reconstruction calibration

Status: `CALIBRATION PROVENANCE / NOT GOLDEN / NOT PROMOTED`

Reference used in the calibration:
- title visible in source: `'REBIRTH' URBAN BROWNFIELD AND WATERFRONT REGENERATION`;
- author/project source identified publicly as Jiayu Zhu / University of Sheffield landscape-planning project;
- supplied reconstruction source: `474×671` compressed JPEG;
- reference class: `R3 / partial-compressed-low-resolution`.

This calibration was used to test the OLEANDER Technical Drawing reconstruction system on a heterogeneous landscape/urban-design analysis board.

## 1. Board argument recovered

The board is not a neutral collage. The reading chain is:

`BACKGROUND → CITY SYSTEMS → SITE SYNTHESIS → GROUND EVIDENCE → PROBLEM LAYERS → TARGET STRATEGY → THEORY → PROJECT VISION`

Recovered major roles:
1. `BACKGROUND_EVIDENCE` — urban extension + socio-demographic pressure;
2. `CITY_SYSTEM_CONTEXT` — transport + functional quarters + green/open space;
3. `SITE_SYNTHESIS` — dominant site-context plan where city systems converge;
4. `GROUND_PHOTO_AUDIT` — current visible surface/edge/vacancy condition;
5. `PROBLEM_LAYER` — car parks/vacant land + flood risk + building use, using repeated site bases;
6. `TARGET_STRATEGY` — issue-to-planning-action handoff;
7. `THEORY_FRAME / COMPACT CITY` — mix/proximity/walkability/public transport rationale;
8. `THEORY_FRAME / WATERFRONT CITY` — urban-node + public-water-edge connectivity rationale;
9. `VISION_CLOSE` — one concise project proposition.

Dominant panel: `SITE_SYNTHESIS`.

## 2. Dual-track reconstruction result

### V1 — Visual Extraction
Bounded source-derived raster carriers were aligned to the source while frame/header were rebuilt.

Metrics at the supplied `474×671` comparison size:
- `MAE = 2.2216`;
- `RMSE = 16.6435`;
- `changed_pixel_ratio@t0 = 5.648%`;
- `changed_pixel_ratio@t12 = 2.904%`.

Result: strong visual extraction, weak semantic completion.

### V2 — Semantic Rebuild
Major board logic, theory diagrams and selected site relations were rebuilt as editable SVG objects while dense maps/photos/microtext remained bounded source context.

Metrics:
- `MAE = 6.9788`;
- `RMSE = 27.1515`;
- `changed_pixel_ratio@t0 = 17.464%`;
- `changed_pixel_ratio@t12 = 9.938%`.

Result: semantically better but pixel-worse. This proves that lower pixel error is not a reliable editability/semantic score.

### V3 — Dual Track
Visible bounded source carriers were used for fidelity while board-logic/site/theory objects remained separately editable/non-rendering semantic objects.

Metrics:
- `MAE = 0.3329`;
- `RMSE = 6.0016`;
- `changed_pixel_ratio@t0 = 1.516%`;
- `changed_pixel_ratio@t12 = 0.448%`.

Result: very high visual fidelity, but **not RF-C3**.

Why RF-C3 remains unavailable:
- supplied source is R3;
- exact font/shaping environment is unavailable;
- microtext and miniature legends are not independently recoverable;
- visible fidelity still depends on bounded source raster carriers;
- semantic editability is partial rather than complete for every in-scope analytical relation.

`LOWER MAE FROM SOURCE-DERIVED TILES != BETTER RECONSTRUCTION`

`SOURCE TILE CONTROL != RF-C3`

## 3. Skill gaps exposed and repaired

New module:
- `references/EDITORIAL_ANALYSIS_BOARD_RECONSTRUCTION.md`

New machine gate:
- `tools/validate_editorial_analysis_board.py`

New regression:
- `fixtures/reconstruction/BOARD-01_REGISTER.json`
- `fixtures/reconstruction/validate_editorial_analysis_board_regression.py`

New board-specific rules:
- reconstruct the board argument, not only the panel pixels;
- identify one dominant synthesis panel when the reference has one;
- record `why_this_carrier` for every panel;
- keep repeated-base problem maps registered to one base family;
- treat serial site photographs as ground evidence when that is their role;
- theory diagrams must link back to a diagnosed problem;
- unreadable R3 microtext cannot be invented;
- source-raster visibility cannot prove semantic completion;
- source-tile visual equality cannot claim RF-C3.

## 4. Calibration conclusion

The reconstruction loop must preserve three independent axes:

`BOARD ARGUMENT / CARRIER LOGIC`

`SEMANTIC EDITABILITY`

`PIXEL / RENDER FIDELITY`

Improvement on one axis must not be silently reported as improvement on the others.

Producer state: `EXECUTED / SELF-CHECKED / INDEPENDENT REVIEW PENDING`.