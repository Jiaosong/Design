# OLEANDER Technical Drawing — Visualization Data Reconstruction Bridge

Status: `candidate extension / PR #172`

Use this bridge when an exact-reference task is not only a drawing/image reconstruction problem, but also a **chart / infographic / analytical visualization reconstruction** problem where the user expects editable data semantics.

The companion data/encoding protocol lives in `oleander-data-viz/RASTER_TO_PARAMETRIC_RECONSTRUCTION.md`.

This file keeps ownership boundaries explicit:

- `oleander-technical-drawing` owns supplied-reference identity, registration, geometry/path/typography/stroke forensics, pixel/ROI evidence and exact-reconstruction truth boundaries;
- `oleander-data-viz` owns source-data states, analytical grammar, mark/channel/scale reconstruction and deterministic data→SVG generation.

`RF-C3 PIXEL MATCH != VR-C3 SEMANTIC DATA RECONSTRUCTION`

`PIXEL PATH != RECOVERED SOURCE RELATION`

`SEGMENT PATH != SEMANTIC LAYER`

## 1. Required three-layer architecture

When reconstructing a visualization from raster reference, the editable artifact should separate:

1. `SOURCE_DATA.json` — values/categories/relations plus explicit recovery state;
2. `VISUAL_ENCODING_SPEC.json` — field→transform→mark→channel→scale/layout mapping;
3. `PARAMETRIC SVG` — generated from the two layers above.

The SVG may contain geometry IDs, but those IDs do not replace the source-data and encoding layers.

If a repair is made directly in SVG, it must be reconciled back into the data/spec/generator before calling the system reproducible.

## 2. Truth-state handoff

Technical-drawing extraction may discover:

- pixel coordinates;
- circles/radii;
- line/path geometry;
- stroke families;
- repeated symbols;
- panel boundaries;
- topology candidates.

It must pass those downstream with evidence states instead of claiming original data recovery.

Recommended states:

- `SOURCE_VISIBLE`;
- `REFERENCE_DERIVED_GEOMETRY`;
- `INFERRED_FROM_MARK`;
- `REFERENCE_TRACE_CANDIDATE`;
- `UNREADABLE`;
- `DESIGN_STRUCTURE`.

A circle radius measured from pixels is geometry evidence. It is not automatically the author's original numeric value.

## 3. Crossing identity gate for dense relation drawings

A visible crossing is not enough to determine path identity.

For alluvial / relation / network reconstructions, record per path and per crossing:

- source endpoint;
- target endpoint;
- color/relation family;
- local tangent before crossing;
- local tangent after crossing;
- crossing-order inversion;
- continuity confidence;
- identity state `HIGH / MEDIUM / LOW`.

`LOW / MEDIUM` crossing identities remain candidate topology even when the rendered path is visually close.

A global pixel score cannot promote an ambiguous crossing to a recovered source relation.

## 4. Segment → layer promotion gate

Thin-line extraction frequently produces many locally correct path fragments.

Do not promote fragments directly to semantic layers.

Use:

`REFERENCE PIXELS → SKELETON / SEGMENTS → CONTINUATION GRAPH → ORDERED/GROUPED LAYER CANDIDATES → SOURCE MEANING BINDING IF AVAILABLE`.

Editability ladder for this case:

- `L0` anonymous pixel/path evidence;
- `L1` stable geometry segments;
- `L2` ordered/grouped geometric layers;
- `L3` source-supported semantic/data layers.

A top-to-bottom order can justify L2. It cannot justify L3 when the original variable meaning remains unreadable.

## 5. Repair acceptance and rejection

The reconstruction loop must keep a CURRENT candidate and reject regressions.

Accept a repair only when it:

- improves the declared critical ROI, or produces a necessary semantic/editability gain with an explicit tradeoff;
- does not degrade a higher-confidence structure;
- does not invent missing data;
- remains recoverable in data/spec/generator form when applicable.

Practice-derived failure pattern:

A 19-layer parametric contour family produced a plausible internal mask fit but increased the actual main-reference ROI error. The correct action is `REJECT_THIS_REPAIR`, not to retain it because the algorithm is more sophisticated.

`ALGORITHM COMPLEXITY != RECONSTRUCTION QUALITY`.

## 6. Deterministic reconstruction gate

When `SOURCE_DATA.json → VISUAL_ENCODING_SPEC.json → generator → SVG` is part of the claim, regenerate twice under the same environment.

Record pixel equality between the two generated renders.

Zero-difference roundtrip proves:

- the pipeline is deterministic;
- the source/spec/generator is sufficient to reconstruct its current output.

It does not prove:

- reference fidelity;
- source data accuracy;
- correct crossing identity;
- technical truth;
- Design KEEP.

## 7. Review matrix

Do not collapse these verdicts:

| Axis | Owner | Question |
|---|---|---|
| Reference fidelity | Technical Drawing RF | Does it match the supplied reference? |
| Relationship fidelity | Technical Drawing relation gate | Are carriers/targets/topology actually reconstructed? |
| Encoding fidelity | Data Viz | Is data→mark/channel/scale grammar coherent? |
| Semantic recovery | Data Viz | Which meanings/values/relations are genuinely source-supported? |
| Editability | Both | Are important objects structured and data-bound where possible? |
| Deterministic roundtrip | Data Viz / runtime | Can the declared data/spec reproduce the same artifact? |
| Design quality | Independent OLEANDER review | Is the result professionally effective? |

## 8. Hard boundaries

`PIXEL MATCH != SOURCE DATA RECOVERY`

`GLOBAL MAE IMPROVEMENT != SEMANTIC RECOVERY`

`TRACE SUPPORT != CROSSING IDENTITY`

`SEGMENT GEOMETRY != SEMANTIC LAYER`

`GEOMETRIC LAYER ORDER != ORIGINAL VARIABLE MEANING`

`DETERMINISTIC ROUNDTRIP != REFERENCE PASS`

`RF PASS != VR PASS != DESIGN KEEP`
