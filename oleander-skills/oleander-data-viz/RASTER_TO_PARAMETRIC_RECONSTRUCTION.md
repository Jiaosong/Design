# OLEANDER Data Viz — Raster Visualization → Parametric Reconstruction

Status: `candidate extension / PR #176`

Use when the only available source is a raster/screenshot/JPEG/PNG of an existing chart, infographic, analytical poster or mixed editorial visualization and the task is to reconstruct it as editable, data-driven output.

This protocol was hardened after a real reconstruction exercise exposed a recurring error: a visualization can become visually close while its underlying data grammar is still invented or opaque.

`PIXEL MATCH != SOURCE DATA RECOVERY`

`PATH TRACE != SEMANTIC EDITABILITY`

`MARK GEOMETRY != ORIGINAL VARIABLE MEANING`

`GLOBAL FIDELITY IMPROVEMENT != SEMANTIC RECOVERY`

## 1. Mandatory reconstruction chain

For in-scope raster visualization reconstruction, prefer:

`REFERENCE SNAPSHOT → ROI SEGMENTATION → MARK-FAMILY DETECTION → SOURCE_DATA.json → VISUAL_ENCODING_SPEC.json → PARAMETRIC GENERATOR → EDITABLE SVG → SAME-SIZE RENDER → ROI FIDELITY READBACK → SEMANTIC AUDIT → DETERMINISTIC ROUNDTRIP`

Do not hand-edit the final SVG after the data/spec stage and then call the pipeline data-driven. If a manual repair is necessary, encode the repair back into data/spec/generator before promotion.

## 2. Source-data truth states

Every recovered field/value/mark must carry one of these states:

- `SOURCE_VISIBLE` — the supplied source directly supports the text/value/relation.
- `REFERENCE_DERIVED_GEOMETRY` — coordinates, radius, length, angle, path or area are measured from reference pixels.
- `INFERRED_FROM_MARK` — a normalized/proxy value is inferred only to regenerate a visible mark.
- `REFERENCE_TRACE_CANDIDATE` — topology/path continuity is machine-traced but crossings/occlusion remain ambiguous.
- `UNREADABLE` — the raster does not support reliable recovery. Keep null/open; do not invent.
- `DESIGN_STRUCTURE` — layout, grouping or visual-system structure, not source data.

Never silently upgrade `REFERENCE_DERIVED_GEOMETRY` or `INFERRED_FROM_MARK` into original research data.

## 3. Claim ladder

Use separate reconstruction claims:

### `VR-C0 / VISUAL STRUCTURE`
Major panels, hierarchy, palette and mark families reconstructed.

### `VR-C1 / MARK GEOMETRY`
Reference-derived positions/sizes/angles/paths exist for the main marks.

### `VR-C2 / ENCODING RECONSTRUCTION`
A machine-readable mapping exists from fields → transforms → marks → channels → scales, and the SVG is generated from it.

### `VR-C3 / SEMANTIC DATA RECONSTRUCTION`
Original field meanings, category identities, values/topology and units are source-supported rather than inferred from appearance.

`VR-C3` is unavailable when the original variables/labels are unreadable or when only pixel geometry has been recovered.

## 4. Semantic editability levels

Do not call every SVG path “editable”.

- `L0 PIXEL/PATH EXTRACTION` — anonymous raster/path evidence.
- `L1 GEOMETRY SEGMENTS` — stable circles/lines/path segments with IDs.
- `L2 ORDERED / GROUPED OBJECTS` — segments are grouped into stable layers, series, route families, rows/columns or symbol instances.
- `L3 DATA-BOUND SEMANTICS` — object identity is bound to a source-supported field/category/relation and can be regenerated from data.

For professional information-visualization reconstruction, important claim-bearing structures should reach L3 when source evidence permits it. When source evidence does not permit it, keep the honest ceiling at L1/L2.

## 5. Mark-specific recovery rules

### Bubble / matrix

Recover:
- grid origin and spacing;
- row/column indices;
- circle centers;
- raster-equivalent radius/area.

If the original quantitative value is unknown, render the measured radius directly and mark it `REFERENCE_DERIVED_GEOMETRY`. Do not reverse-engineer a fabricated percentage/value.

If the original value is known and circle area encodes magnitude, use area scaling, e.g. `r ∝ sqrt(value)`, not linear radius scaling.

### Radial / polar bars

Recover separately:
- center;
- inner/outer radii;
- category angles;
- per-series radial length;
- stroke/bar width;
- series color.

Angle is a category channel unless the source proves continuous angular meaning.

### Trend / area overlays

Separate visible annotations from inferred shape profiles. A mountain/area silhouette may be `INFERRED_FROM_MARK` while readable percentages remain `SOURCE_VISIBLE`.

### Alluvial / relation field

Do not infer flow magnitude from a uniform-width relation line.

Recover:
- source row identity/position;
- target row identity/position;
- color/relation family;
- source→target topology;
- path geometry;
- crossing identity confidence.

At raster crossings, add `HIGH / MEDIUM / LOW` identity confidence based on continuity evidence such as local tangent separation, color continuity and endpoint consistency. Low-confidence crossings remain candidates.

`CURVE VISIBLE != CROSSING IDENTITY RESOLVED`.

### Layered contour / stacked field

A skeletonized contour fragment is L1 geometry, not automatically one semantic layer.

Use:
`SEGMENT EXTRACTION → CONTINUATION/STITCHING → TOP-TO-BOTTOM OR OTHER STABLE ORDER → LAYER CANDIDATE → SOURCE MEANING BINDING IF AVAILABLE`.

`SEGMENT PATH != SEMANTIC LAYER`.

`GEOMETRIC ORDER != ORIGINAL VARIABLE MEANING`.

## 6. Reference-derived parameter extraction

Prefer objective extraction before eyeballed coordinates:

- connected components for isolated circles/symbol fields;
- Hough/radial analysis for circle centers/radii;
- color-separated masks for series/line families;
- projection/autocorrelation for grids;
- skeletonization + graph-chain decomposition for thin line structures;
- path tracing with continuity/tangent constraints for dense relation fields;
- bounded parameter optimization against reference masks for compact parametric families.

Every detector must expose its confidence and known ambiguity. Detection complexity does not grant correctness.

## 7. Repair acceptance is metric-bound but not metric-only

A proposed repair is accepted only if:

1. it preserves or improves source/semantic truth;
2. its target ROI fidelity improves, or a documented semantic/editability gain justifies a controlled visual tradeoff;
3. it does not make a higher-confidence structure worse;
4. it does not fabricate missing data to obtain a closer-looking image.

If a more sophisticated tracker or parameter family worsens the declared target ROI and provides no necessary semantic gain, mark the repair `REJECT` and retain the previous CURRENT.

`MORE SOPHISTICATED ALGORITHM != BETTER RECONSTRUCTION`.

## 8. Deterministic roundtrip gate

For a data-driven reconstruction, run the generator twice from the same:

- `SOURCE_DATA.json`;
- `VISUAL_ENCODING_SPEC.json`;
- generator code;
- renderer/version/environment.

The two outputs must rasterize identically under the locked environment for the declared canvas.

Record:
- changed-pixel ratio;
- MAE;
- maximum channel error;
- generator/source/spec identities.

A zero-difference deterministic roundtrip proves reproducibility only. It does not prove reference fidelity or source-data correctness.

## 9. Multi-axis review

Review at least four axes independently:

1. `REFERENCE FIDELITY` — does the rendered candidate match the supplied visual source?
2. `ENCODING FIDELITY` — are mark/channel/scale relationships reconstructed coherently?
3. `SEMANTIC RECOVERY` — which original values/categories/relations are actually source-supported?
4. `EDITABILITY / ROUNDTRIP` — can data/spec regenerate the artifact deterministically?

Do not collapse them into one score.

## 10. Practice-derived blockers

Automatic `REVISE / REJECT / HOLD` triggers include:

- replacing unreadable labels with invented text;
- using a proxy numeric value as if it were original data;
- treating a uniform-width relation drawing as a weighted Sankey;
- calling 52 visually traced alluvial paths fully recovered topology when crossing identity is still ambiguous;
- calling skeleton fragments semantic layers before continuation/grouping;
- accepting a contour-fitting algorithm because its internal mask objective improves while actual reference ROI error worsens;
- modifying generated SVG manually without writing the change back into data/spec/generator;
- a generator that cannot reproduce its own output deterministically;
- lower global MAE masking a broken critical series/relationship ROI.

## 11. Cross-skill boundary

`oleander-data-viz` owns source-data states, analytical grammar, encoding semantics and parameterized visualization generation.

When reconstruction also requires exact supplied-reference fidelity, typography/stroke forensics, pixel/ROI diagnostics, or relation-path reconstruction from a technical/editorial drawing, use `oleander-technical-drawing` reconstruction modules as companion gates.

Neither skill may upgrade the other's truth state:

`RF-C3 PIXEL MATCH != VR-C3 SEMANTIC DATA RECONSTRUCTION`.
