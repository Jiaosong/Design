# OLEANDER Technical Drawing — Source Carrier Precedence

Status: `candidate extension / PR #172`

Use this module with `SPATIAL_TRANSLATION_PROTOCOL.md` whenever the source itself already contains decision-relevant spatial geometry: an official guide, survey, CAD/model view, GIS/map, section, annotated photograph, technical diagram, or other authoritative/first-party visual carrier.

This module closes a second-order translation failure:

> the producer correctly identifies the source and the spatial phenomenon, but redraws the relation anyway because a cleaner custom line/shape looks more like an analysis diagram.

`SOURCE EXISTS != REDRAW REQUIRED`

`CLEANER GRAPHIC != BETTER SPATIAL TRANSLATION`

`SOURCE-CARRIER ADEQUACY > EDITORIAL DESIRE TO REDRAW`

`REDRAW != NEUTRAL`

Every redraw can alter position, adjacency, topology, extent, width, orientation, continuity, branch/merge structure, or uncertainty. Therefore redraw is a transformation that must be justified, not a default presentation step.

## 1. Precedence question before abstraction

Before Stage 3 of `SPATIAL_TRANSLATION_PROTOCOL.md`, ask:

> Does the source itself already carry the spatial relation needed for this claim at the required decision level?

Classify the answer as:

- `SOURCE_CARRIER_ABSENT` — source has facts/text but no usable visual/spatial carrier.
- `SOURCE_CARRIER_INSUFFICIENT` — source carrier exists but cannot express the required decision without a bounded translation.
- `SOURCE_CARRIER_SUFFICIENT` — source carrier already expresses the needed relation at the claim level.
- `SOURCE_CARRIER_AUTHORITY` — source carrier is the current controlling geometry for that claim/scope.

When `SUFFICIENT` or `AUTHORITY`, default to **reuse / crop / mask / highlight / annotate**, not redraw.

## 2. Allowed carrier-precedence decisions

Every translation item with an available source carrier must declare one of:

- `REUSE_DIRECT` — use the source carrier itself; add only editorial annotation/highlight that does not replace geometry.
- `TRACE_BOUNDED` — trace/reuse geometry because editable geometry is required; preserve declared invariants and keep source visible/auditable.
- `DERIVE_REQUIRED` — compute a new carrier because the source relation must be transformed analytically (for example catchment from DEM, offset/clearance from CAD, visibility from 3D geometry).
- `GENERALIZE_REQUIRED` — simplify source geometry because target scale/readability requires it; the preserved/relaxed invariants are explicit.
- `SCHEMATIZE_SEPARATELY` — create a topology/sequence diagram that is intentionally detached from map registration.
- `REDRAW_JUSTIFIED` — redraw for a specific downstream need not covered above; requires explicit justification and must not imply higher authority.

`REDRAW_JUSTIFIED` is exceptional. “Cleaner”, “more dynamic”, “more professional”, “better composition”, “matches reference style”, or “easier to color” are not sufficient justification.

## 3. Direct-source carrier rule

If `SOURCE_CARRIER_SUFFICIENT` or `SOURCE_CARRIER_AUTHORITY`:

1. do not replace a source path/network with a custom path/network solely for styling;
2. do not replace a source field with a cleaner blob/polygon solely for composition;
3. do not move source nodes to improve label spacing;
4. do not straighten/curve a source carrier unless the action is declared `GENERALIZE_REQUIRED` and preserves the claim invariants;
5. do not overlay a schematic sequence on the source in a way that visually inherits map authority;
6. use editorial devices — crop, mask, fade, highlight, leader, bracket, label, inset, keyed callout — before inventing replacement geometry;
7. keep annotation lines semantically separate from the source geometry they identify.

A direct-source visual may be raster and still be the correct **spatial authority carrier** for a relational analysis. This does not make the raster editable geometry, measured geometry, or construction authority.

`DIRECT SOURCE CARRIER != VECTOR EDITABILITY`

`DIRECT SOURCE CARRIER != SURVEY ACCURACY`

`DIRECT SOURCE CARRIER != FIELD PASS`

## 4. When redraw is actually justified

Redraw/derive/generalize is justified when at least one decision-relevant requirement cannot be met by direct source reuse, for example:

- geometry must be edited parametrically or coordinated with another authoritative model;
- multiple source layers must be registered into one spatial base;
- a quantitative measurement/offset/catchment/visibility operation requires derived geometry;
- the source resolution is insufficient at the output scale but its geometry can be boundedly reconstructed;
- a source network is too visually dense for the target scale and must be generalized while preserving topology;
- a sequence/topology must be explained separately from geographic shape;
- accessibility, drainage, construction, or maintenance analysis requires a different projection/section generated from controlling geometry.

The register must state **what requirement cannot be satisfied by direct reuse**.

## 5. Required register extension

Add these fields to every decision-relevant `SPATIAL_TRANSLATION_REGISTER` item:

- `source_carrier_state`: `SOURCE_CARRIER_ABSENT | SOURCE_CARRIER_INSUFFICIENT | SOURCE_CARRIER_SUFFICIENT | SOURCE_CARRIER_AUTHORITY`
- `source_carrier_scope`: what exact relation the source carrier already expresses;
- `carrier_precedence_decision`: `REUSE_DIRECT | TRACE_BOUNDED | DERIVE_REQUIRED | GENERALIZE_REQUIRED | SCHEMATIZE_SEPARATELY | REDRAW_JUSTIFIED`
- `redraw_justification`: explicit reason when the decision is not `REUSE_DIRECT`; may be `N/A` only for direct reuse.

Hard rule:

> If `source_carrier_state` is `SOURCE_CARRIER_SUFFICIENT` or `SOURCE_CARRIER_AUTHORITY`, any decision other than `REUSE_DIRECT` requires a material analytical/editability/output reason. Aesthetic preference is insufficient.

## 6. Landscape-specific examples

### Official scenic guide already shows river + cable + path network

Valid:
`FIRST-PARTY GUIDE → SOURCE_CARRIER_SUFFICIENT → REUSE_DIRECT → editorial anchors / masks / labels`.

Invalid:
`FIRST-PARTY GUIDE → redraw a cleaner blue river + straight cable + invented smooth route → call it landscape analysis`.

If only route order must be clarified:
`FIRST-PARTY GUIDE + route-order evidence → SCHEMATIZE_SEPARATELY / SEQUENCE_BOUND`.

### Survey contours

If contour geometry itself is the analytical evidence:
`SURVEY → SOURCE_CARRIER_AUTHORITY → REUSE_DIRECT / TRACE_BOUNDED`.

Do not draw decorative contour-like lines for visual atmosphere.

### Existing vegetation map

If mapped community polygons are usable:
`VEGETATION SOURCE → SOURCE_CARRIER_SUFFICIENT → REUSE_DIRECT + management overlay`.

Only redraw/generalize if target-scale or analytical transformation requires it.

## 7. Review questions

Before accepting a custom carrier, ask:

1. Did the source already show this relation?
2. If yes, why was direct reuse insufficient?
3. What invariant could the redraw accidentally alter?
4. Is the new geometry visibly distinguishable from source authority?
5. Does the redraw solve an analytical/editability/scale problem, or only a styling problem?
6. Can the same claim be made more truthfully by highlighting the source instead?
7. If the custom carrier were deleted, would the source still communicate the relation? If yes, the redraw needs stronger justification.

Any critical failure keeps the object at `REVISE / REVIEW PENDING`.

## 8. Automatic blockers

Automatic `REVISE`:

- source carrier marked sufficient/authoritative but custom redraw has no material justification;
- redraw justification is only aesthetics, cleanliness, style matching, layout, or color control;
- custom route alters source branch/merge structure;
- custom field changes source extent/edge while still appearing source-bound;
- node is moved away from its source relation for label convenience;
- direct source is hidden so completely that the reviewer cannot audit what was preserved;
- a schematic abstraction visually inherits map/survey authority from the source base;
- a raster source is rejected merely because it is not vector, even though the task only requires relational reading;
- editorial callout/leader is treated as replacement spatial geometry.

Producer may self-check source-carrier precedence but cannot self-award `KEEP`, `PROFESSIONAL FINISH`, `FIELD PASS` or Promotion.
