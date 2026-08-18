# OLEANDER Technical Drawing — Detail Callout Registration

Status: `v0.1 / companion to oleander-technical-drawing v0.2 candidate`

Purpose: prevent a parent section/plan and its enlarged child detail from silently describing different geometry. A detail may add information at a larger scale; it may not redesign the interface simply to become clearer.

`ENLARGEMENT ≠ REDRAW`.

`MORE DETAIL ≠ NEW GEOMETRY AUTHORITY`.

## 1. Registered scale ladder

Use the smallest ladder needed:

`CONTEXT / GA → PARENT PLAN OR SECTION → CROP / CALLOUT → CHILD DETAIL → CONNECTION / COMPONENT DETAIL`

Every child must bind back to a parent view. Record:

- `PARENT_VIEW_ID`
- `PARENT_SOURCE_REVISION`
- `CALLOUT_ID`
- `CROP_BBOX_OR_BOUNDARY`
- `ANCHOR_A / ANCHOR_B` or other stable invariant points
- `ORIENTATION / SIDEDNESS`
- `PARENT_SCALE`
- `CHILD_SCALE`
- `SCALE_RATIO`
- `ALLOWED_DETAIL_ADDITIONS`
- `PROHIBITED_GEOMETRY_CHANGES`
- `DOES_NOT_PROVE`

If the drawing is NTS, replace numerical scale with a declared relative enlargement ratio or `NTS / RELATIVE ENLARGEMENT`; do not invent precision.

## 2. Invariants that must survive the scale jump

Unless a documented design revision changes them, parent and child must preserve:

1. ordering of components;
2. sidedness / inside-outside relation;
3. attachment or support location;
4. edge and boundary ownership;
5. local orientation;
6. datum relationship;
7. anchor positions relative to the interface;
8. cut/beyond relationship when the child derives from a section.

A rotated child is allowed only when the rotation is explicitly marked and the relation remains recoverable.

## 3. What a child detail may add

A child can legitimately reveal information that is invisible or unreadable at the parent scale:

- fixing / bracket / fastener geometry;
- material build-up;
- seal / isolation / drainage layer;
- local clearance / tolerance when authorized;
- maintenance / removal envelope;
- connection sequence;
- local verification or FIELD/engineer/manufacturer open state.

The child may not move a support, widen a platform, mirror an edge, swap material order, change slope direction, or invent a foundation/anchor arrangement unless the design authority itself has changed and the parent is updated accordingly.

## 4. Parent-to-child tests

### LABEL-OFF REGISTRATION TEST
Hide titles, notes and callout text. Parent crop and child must still be recognizably the same interface by geometry.

### ANCHOR TEST
Choose 2–3 stable anchors and verify that their ordering and relation are unchanged after enlargement.

### ORIENTATION TEST
Check inside/outside, uphill/downhill, left/right, inboard/outboard, flow direction or assembly axis as relevant.

### SCALE-JUMP TEST
The child must answer a question the parent cannot answer at its scale. If it only repeats the parent, remove it. If it changes the relation, revise it.

### RETURN TEST
A reviewer must be able to travel from child back to the exact parent location without guessing.

## 5. Hard failures — automatic REVISE

- detail bubble exists but no recoverable crop/parent location;
- child detail is redrawn from memory rather than registered to the parent;
- rotation/mirroring is unmarked;
- a child contains a different component order or sidedness;
- unsupported dimensions or realistic fasteners appear only in the child and visually upgrade its authority;
- enlargement is used to hide a parent-view contradiction;
- a child detail has greater geometry authority than its declared source;
- multiple children use the same callout ID for different interfaces;
- scale is stated but the child geometry is not actually registered to the parent.

## 6. Review record

For each material detail ladder record:

- `DETAIL_ID`
- `PARENT_VIEW_ID`
- `SOURCE_REVISION`
- `CALLOUT_BOUNDARY`
- `ANCHORS`
- `ORIENTATION`
- `PARENT_SCALE`
- `CHILD_SCALE`
- `ADDED_INFORMATION`
- `UNCHANGED_INVARIANTS`
- `LABEL_OFF_RESULT`
- `RETURN_RESULT`
- `TRUTH_STATE`
- `DOES_NOT_PROVE`

## 7. Promotion test

**Hide labels and compare parent crop to child: orientation, ordering, sidedness and anchor positions must survive the scale jump.**

A beautifully drafted child that cannot pass this test is an orphan detail and must be `REVISE`, even if its linework, typography and density are professional.

This gate complements `DETAIL_DENSITY_CALIBRATION.md`: density asks whether the child proves enough; registration asks whether it still proves the same interface.