# 2026-08-19 — Detail Callout Registration

## Training question

How can an enlarged technical detail become more informative without silently becoming a different interface from its parent plan/section?

Project trigger: C04 R06/C23 technical communication has already trained structural lineweight, activity-bearing human scale and assembly sequencing. The remaining high-impact failure is parent→child traceability: dense or polished child details can become orphan drawings when crop, orientation, anchors or sidedness drift.

## Existing method reused

- OLEANDER Technical Drawing v0.2 candidate / PR #172
- `references/DETAIL_DENSITY_CALIBRATION.md`
- `SPATIAL_TRANSLATION_PROTOCOL.md`
- `SOURCE_CARRIER_PRECEDENCE.md`
- existing Node Ladder: `CONTEXT / GA → PARENT PLAN OR SECTION → INTERFACE DETAIL → CONNECTION ENLARGEMENT → COMPONENT / FOUNDATION / EDGE DETAIL`

This training does not repeat the 2026-08-16 Structural Lineweight Hierarchy, 2026-08-17 Assembly Sequencing, or Activity-bearing Scale practices.

## Real practice asset

Local editable vector asset produced and pixel-read back:

- `OLEANDER_DETAIL_CALLOUT_REGISTRATION_R01.svg`
- 1920×1080 PNG preview
- 50% grayscale preview

Final local hashes:

- SVG SHA-256 `d762c8addcd291e3ce0b8e8540030ca5248d576788fbfe7374cc7c8bc8d2c105`
- PNG SHA-256 `00cead00ed2f0231deb78100928771dc901f380d791639b2afd526fed77c997f`
- grayscale SHA-256 `3c9801ef7e83dfd800e4dba4e09beba0d0616059e1e02d4aa3eaadfcf41f73f6`

The exercise is synthetic, NTS and FIELD OPEN. It does not claim C04 site, structural, anchor, foundation or construction geometry.

## Exercise

### REJECT — Orphan detail

A parent section circles Detail A, but the child is redrawn with changed orientation, thickness and edge relation. The child looks clearer, yet it no longer proves the same interface.

### KEEP candidate — Registered scale ladder

The parent defines:

- a crop boundary;
- two stable anchors;
- outboard orientation;
- parent/child scale relation.

The child preserves ordering, sidedness, orientation and anchor relation. It adds fixing/interface information only because that information becomes legible at the larger scale.

## Design Crit

### Gate 1 — Execution / compliance

`PASS FOR TRAINING EXECUTION`

- editable SVG exists;
- final PNG was actually rendered and opened;
- text remains vector;
- synthetic/NTS/FIELD OPEN boundary is explicit;
- no new C04 field or engineering truth is claimed.

### Gate 2 — Professional Design

Producer frozen-rubric: `KEEP-FOR-TRAINING CANDIDATE`.

- First visual: PASS — orphan vs registered child reads before explanatory text.
- Composition: PASS — parent/child comparison is balanced and relation-led.
- Proportion: PASS — parent and child scales are visually differentiated without letting the child dominate the sheet.
- Hierarchy: PASS — geometry → callout/crop → anchors/orientation → metadata.
- Typography: PASS after pixel readback; labels remain secondary to drawing geometry.
- Material/spatial realism: schematic only; not a material or engineering proof.
- Scale: NTS / proxy scale language only; no fabricated site precision.
- Node readability: PASS — parent location, crop and enlarged interface are traceable.
- Interaction/narrative: static parent→child scale jump reads coherently.
- Professional finish: training-level candidate, not construction-document finish.

Independent Professional Design Reviewer provenance is unavailable in this run. Therefore independent Gate 2 remains `HOLD / REVIEW REQUIRED`; producer review is not relabeled as independent review.

## Failure knowledge

1. `DETAIL BUBBLE EXISTS ≠ DETAIL REGISTERED`.
2. A child redrawn from memory can become an untracked design revision.
3. Adding detail is valid; changing interface ordering/sidedness/orientation is not.
4. Rotation is allowed only when explicitly marked and reversible.
5. A stated scale does not prove geometric registration.
6. The child cannot gain unsupported geometry authority merely because it is larger and more detailed.
7. If a reviewer cannot return from child to exact parent location without guessing, the detail is orphaned.

## Skill delta

Added `oleander-skills/oleander-technical-drawing/references/DETAIL_CALLOUT_REGISTRATION.md` and registered the calibration in `examples/README.md`.

New review fields:

`PARENT_VIEW_ID / PARENT_SOURCE_REVISION / CALLOUT_ID / CROP_BBOX_OR_BOUNDARY / ANCHORS / ORIENTATION / PARENT_SCALE / CHILD_SCALE / SCALE_RATIO / ALLOWED_DETAIL_ADDITIONS / PROHIBITED_GEOMETRY_CHANGES / DOES_NOT_PROVE`.

New attack tests:

`LABEL-OFF REGISTRATION / ANCHOR / ORIENTATION / SCALE-JUMP / RETURN`.

Promotion test:

**Hide labels and compare parent crop to child: orientation, ordering, sidedness and anchor positions must survive the scale jump.**

## Cross-project transfer

Reusable for:

- C04 R06/C23 parent section → node/detail communication;
- landscape platform/edge/drainage details;
- architecture section → wall/edge/interface enlargements;
- product assembly → local mating/fixing details;
- exploded axon → registered interface details;
- any technical drawing set where a child view claims to enlarge a parent condition.

Not directly applicable to:

- genuine alternative design schemes;
- before/after states where geometry intentionally changes;
- diagram-only explanatory details that explicitly do not claim parent geometric registration;
- later engineer/field authority that legitimately revises the parent geometry — in that case update the parent and provenance rather than forcing the old relation to survive.

## Truth boundary

`ARTIFACT EXISTS ≠ DRAWING PASS ≠ ENGINEERING PASS ≠ FIELD PASS ≠ MAIN KEEP`.

C04 `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION` remains unchanged.