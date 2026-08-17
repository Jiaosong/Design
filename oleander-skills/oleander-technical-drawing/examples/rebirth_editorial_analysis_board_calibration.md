# REBIRTH editorial analysis-board reconstruction calibration

Status: `CALIBRATION PROVENANCE / NOT GOLDEN / NOT PROMOTED`

Reference used in the calibration:
- title visible in source: `'REBIRTH' URBAN BROWNFIELD AND WATERFRONT REGENERATION`;
- public project source identifies the work as Jiayu Zhu / University of Sheffield landscape-planning work;
- supplied reconstruction source: `474×671` compressed JPEG;
- reference class: `R3 / partial-compressed-low-resolution`.

This calibration tests the OLEANDER Technical Drawing reconstruction system on a heterogeneous landscape/urban-design analysis board.

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
Visible bounded source carriers were used for fidelity while board-logic/site/theory objects remained separately editable semantic objects.

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

## 3. Waterfront-theory solver — V5 / V6

A small `Waterfront City Theory` icon ROI was used to test final-stage residual repair.

### V5
Semantic object + anonymous bounded residual:
- semantic-only ROI `MAE ≈ 28.81`;
- corrected ROI `MAE ≈ 0.172`;
- residual coverage ≈ `67.9%` of ROI.

Verdict: `REVISE`. The residual layer was functioning as a repaint, not a sparse correction.

### V6
Source-measured node count/positions and urban/water relations were reopened upstream before residual repair:
- semantic-only ROI `MAE ≈ 19.17`;
- corrected ROI `MAE ≈ 0.198`;
- residual coverage ≈ `61.5%`.

Verdict: semantic geometry improved, but anonymous residual remained too dense. This triggered `FINAL_STAGE_PIXEL_SOLVER` residual-density rules.

## 4. Owner-bound visual carrier — V7

The anonymous residual was removed.

The visual layer was partitioned by semantic owner:
- `NODE_FAMILY_VISUAL`;
- `PLUS_VISUAL`;
- `URBAN_EDGE_VISUAL`;
- `WATER_EDGE_VISUAL`.

Editable semantic objects remain separately present.

V7 Waterfront metrics:
- semantic-only `MAE ≈ 19.06`;
- visible-dual `MAE ≈ 0.090`;
- visible-dual `changed@t12 ≈ 0.026%`;
- anonymous residual: `NONE`.

Correct interpretation:
- target-size visible fidelity is very high;
- semantic geometry is still partial;
- the large gap between semantic-only and visible-dual metrics must be reported;
- RF-C3 remains unavailable.

This triggered:
- `references/OWNER_BOUND_VISUAL_CARRIER.md`.

## 5. Compact City Theory — V8

A second theory ROI was reconstructed to test whether the method generalizes.

Recoverable source meaning:
- mixed/compositional pie carrier;
- repeated circular pictogram family;
- horizontal sequence relation.

Unrecoverable at R3:
- exact pie values;
- exact identity/meaning of each miniature pictogram;
- microtext labels below the diagram.

The semantic SVG intentionally does **not** invent those meanings.

V8 metrics:
- semantic-only `MAE ≈ 24.59`;
- visible-dual `MAE = 0.0` at the declared ROI;
- anonymous residual: `NONE`;
- visible fidelity is carried by two owner-bound source-derived carriers: `MIX_DIAGRAM_VISUAL` and `PICTOGRAM_FAMILY_VISUAL`.

The zero visible-dual error does **not** upgrade semantic completeness or RF-C3. It only proves that the owner-bound visual carrier can reproduce the supplied R3 pixels exactly inside that ROI.

## 6. Skill gaps exposed and repaired

New/updated modules:
- `references/EDITORIAL_ANALYSIS_BOARD_RECONSTRUCTION.md`;
- `references/FINAL_STAGE_PIXEL_SOLVER.md` residual-density gate;
- `references/OWNER_BOUND_VISUAL_CARRIER.md`.

Machine gate:
- `tools/validate_editorial_analysis_board.py`.

Regression:
- `fixtures/reconstruction/BOARD-01_REGISTER.json`;
- `fixtures/reconstruction/validate_editorial_analysis_board_regression.py`.

New board-specific rules:
- reconstruct the board argument, not only the panel pixels;
- identify one dominant synthesis panel when the reference has one;
- record `why_this_carrier` for every panel;
- keep repeated-base problem maps registered to one base family;
- treat serial site photographs as ground evidence when that is their role;
- theory diagrams must link back to a diagnosed problem;
- unreadable R3 microtext cannot be invented;
- source-raster visibility cannot prove semantic completion;
- source-tile visual equality cannot claim RF-C3;
- dense anonymous residual must reopen semantic geometry;
- if R3 visual detail is irreducible, source-derived visual pixels may be partitioned by semantic owner, but visible-dual and semantic-only metrics must remain separate.

## 7. Calibration conclusion

The reconstruction loop must preserve four independent axes:

`BOARD ARGUMENT / CARRIER LOGIC`

`SEMANTIC EDITABILITY`

`OWNER-BOUND TARGET-SIZE VISUAL FIDELITY`

`FULL PIXEL / RENDER FIDELITY`

Improvement on one axis must not be silently reported as improvement on the others.

Producer state: `EXECUTED / SELF-CHECKED / INDEPENDENT REVIEW PENDING`.