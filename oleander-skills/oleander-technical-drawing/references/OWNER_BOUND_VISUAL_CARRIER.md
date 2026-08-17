# OLEANDER Technical Drawing — Owner-bound Visual Carrier

Status: `candidate extension / PR #172`

Use with `FINAL_STAGE_PIXEL_SOLVER.md` when an R3 / compressed-raster reconstruction has a valid editable semantic object but target-size appearance still depends on source-derived pixels.

This module exists because a dense anonymous residual can produce excellent pixel metrics while functioning as a repaint. When that happens, do not simply keep increasing residual density.

Two valid responses exist:

1. reopen the semantic geometry and improve it;
2. when the source contains renderer/compression/detail appearance that is not independently recoverable, replace the anonymous residual with **semantic-owner-bound visual carriers**.

`DENSE RESIDUAL != OWNER-BOUND VISUAL CARRIER`

`OWNER-BOUND VISUAL CARRIER != SEMANTIC COMPLETION`

`OWNER-BOUND VISUAL CARRIER != RF-C3`

`PIXEL-ACCURATE VISUAL OWNER != EDITABLE GEOMETRY OWNER`

## 1. Required structure

Allowed dual representation:

`SEMANTIC OBJECT → OWNER ID`

`OWNER ID → BOUNDED SOURCE-DERIVED VISUAL CARRIER`

Examples:
- `NODE_FAMILY → NODE_FAMILY_VISUAL`;
- `PLUS_RELATION → PLUS_VISUAL`;
- `URBAN_EDGE → URBAN_EDGE_VISUAL`;
- `WATER_EDGE → WATER_EDGE_VISUAL`;
- `TYPOGRAPHY_RUN → GLYPH_VISUAL`.

Every visual carrier must have exactly one recoverable semantic owner or one explicitly declared repeated family owner.

## 2. When conversion from residual is allowed

A dense residual may be replaced by owner-bound visual carriers only when:
- the semantic classes inside the ROI are known;
- pixels can be partitioned by those classes without mixing unrelated objects;
- each carrier has a stable bbox and source reference;
- the source-derived carrier is marked `NON_AUTHORITY`;
- the editable semantic object remains independently present;
- the claim ceiling is not upgraded because the visual metric improves.

If pixels cannot be partitioned by semantic owner, remain `REVISE / REOPEN UPSTREAM`.

## 3. Required register

For each visual carrier record:
- `visual_carrier_id`;
- `semantic_owner_id`;
- `semantic_class`;
- `bbox`;
- `source_ref`;
- `source_class`;
- `derivation_method`;
- `contains_only_owner_class`;
- `editable_semantic_object_id`;
- `state = SOURCE_DERIVED_VISUAL_CARRIER / NON_AUTHORITY`;
- `claim_ceiling`;
- `does_not_prove`.

Also report semantic-only metrics separately from visible-dual metrics.

## 4. Pixel metrics must remain dual

Always report both:

`SEMANTIC_ONLY_RENDER ↔ REFERENCE`

and

`SEMANTIC + OWNER-BOUND VISUAL ↔ REFERENCE`.

A large gap between those two metrics is useful diagnostic evidence. It means visual fidelity is being carried mostly by the visual carrier, not by the editable semantic geometry.

Do not hide that gap with one final full-page MAE.

## 5. Calibration example

In the REBIRTH waterfront-theory icon calibration:
- V5 used one anonymous residual covering about `67.9%` of the ROI → `REVISE`;
- V6 improved semantic geometry but still required about `61.5%` anonymous residual → `REOPEN UPSTREAM`;
- V7 removed the anonymous residual and partitioned the visible source-derived layer by semantic owner: `NODE_FAMILY / PLUS / URBAN_EDGE / WATER_EDGE`;
- V7 visible-dual MAE fell to about `0.090`, while semantic-only MAE remained about `19.06`.

Correct interpretation:
- the owner-bound visual reconstruction is highly faithful at target size;
- semantic geometry is only partially reconstructed;
- RF-C3 is still unavailable;
- the metric gap must remain visible in the readback.

## 6. Hard blockers

Automatic `REVISE`:
- renaming an anonymous residual group as an owner-bound carrier without partitioning its semantic classes;
- one carrier contains node + text + base + water + route pixels;
- source-derived carrier replaces the editable semantic object;
- visible-dual metric is reported without semantic-only metric;
- RF-C3 or semantic completion is claimed because the owner-bound visual carrier is pixel-close;
- owner is invented only to legitimize a raster/path-cloud shortcut.

Producer states remain `EXECUTED / SELF-CHECKED / REVIEW PENDING / REVISE / REJECT` only.