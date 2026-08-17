# OLEANDER Golden Drawing Fixtures

Status: `GOLDEN CANDIDATE / NOT PROMOTED`

These fixtures are editable vector calibration assets for `oleander-technical-drawing`. They define repeatable drawing-quality and reasoning conditions; they are not project evidence, engineering approval, field evidence, construction details or a universal house style.

## Suite

| ID | Fixture | Primary regression target |
|---|---|---|
| GD-01 | `GD-01_ARCH_SECTION.svg` | section cut hierarchy, secondary build-up, parent → detail traceability, truth boundary |
| GD-02 | `GD-02_LANDSCAPE_NODE.svg` | existing/proposed/FIELD OPEN distinction, slope/path/support, drainage, safety edge, maintenance |
| GD-03 | `GD-03_PRODUCT_ASSEMBLY_CMF.svg` | exploded order, exact mating detail, service/removal path, CMF state separation |
| GD-04 | `GD-04_CONNECTION_FOUNDATION.svg` | load/support path, base/anchor/foundation relationship, water/corrosion intent, access, engineering/field boundary |
| GD-05 | `GD-05_SPATIAL_ANALYSIS_PLAN.svg` | SOURCE / EVIDENCE / INFERENCE / DECISION spatial overlay grammar |
| GD-06 | `GD-06_EVIDENCE_SPATIAL_CONSEQUENCE.svg` | traceable Evidence → Spatial Finding → Design Consequence reasoning |

## What is locked

The fixtures use intentionally locked training geometry and a common `1800 × 1200` canvas so regressions can be compared without project-content noise.

Locked conditions include:

- stable fixture IDs and named SVG groups;
- vector technical text and core geometry;
- visible truth/status boundary;
- first-read → intended-size → near-read hierarchy;
- distinction between source, design, recommendation/inference and open conditions;
- parent/detail or evidence/finding/decision traceability appropriate to the fixture;
- no self-promotion to engineering, field, fabrication, construction or MAIN approval.

## What may change in a transfer variant

A project transfer may change:

- geometry and dimensions when bound to the project's authority;
- material and CMF system;
- jurisdictional standard set;
- view count and scales;
- typography family where the delivery system requires it;
- lineweight values when physical output scale changes;
- language and annotation density;
- analysis overlays and conclusions when supported by project evidence.

Do not copy training dimensions into a project simply because the fixture looks professional.

## Regression modes

### 1. Structure regression

Run:

`python oleander-skills/oleander-technical-drawing/fixtures/validate_fixtures.py`

This checks required groups, unique IDs, fixed fixture canvas, vector-only core content and explicit candidate/non-promotion state.

`STRUCTURE PASS ≠ DESIGN PASS`.

### 2. Visual regression

For each fixture, review actual rendered/exported output at:

1. thumbnail / distance;
2. intended sheet/display size;
3. near-read/detail scale;
4. grayscale or color-independent semantic read where relevant.

A structural fixture that becomes visually flat, noisy, illegible or decorative remains a design regression even if CI passes.

### 3. Truth regression

Check that no change:

- turns FIELD OPEN into resolved geometry;
- turns candidate CMF into approved CMF;
- lets a render/AI image override geometry authority;
- removes a source/inference distinction;
- turns a design explanation into fabrication/construction permission;
- deletes an unknown merely to make the sheet cleaner.

### 4. Reasoning regression for analysis drawings

For GD-05/GD-06:

- source geometry remains recoverable;
- inference cannot use the same semantics as source evidence;
- design decisions do not redraw history/source to make the conclusion fit;
- each conclusion has a traceable evidence/finding chain;
- quantities/statistical uncertainty that become primary must route to `oleander-data-viz`.

## Promotion rule

The fixture suite may become `GOLDEN` only after:

1. actual SVG open/readback;
2. structural validator PASS;
3. independent OLEANDER design review of all six rendered fixtures;
4. no blocker regressions in truth state, line hierarchy, typography, composition, node readability, analysis traceability or professional finish;
5. promotion receipt that identifies exact fixture revision/hash.

The production author must not self-promote the suite.
