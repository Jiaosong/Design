# OLEANDER Technical Drawing — Theme Overlay Fidelity

Status: `candidate extension / PR #172`

Use for exact reconstruction of analytical drawings where the base geometry is close but the visible thematic layer (intervention, public-space zone, event layer, landscape, mobility, state overlay, etc.) is still materially wrong.

`THEME SEMANTICS != THEME VISUAL CARRIER`

`CORRECT COLOR != CORRECT THEME GEOMETRY`

`SEMANTIC SIMPLIFICATION != PIXEL FIDELITY`

## 1. Keep two tracks

### `THEME_SEMANTIC_LAYER`
Editable analytical objects: zones, routes, nodes, landscape groups, intervention objects, state classes, ownership and relation IDs.

### `THEME_VISUAL_CARRIER`
A reconstruction-only structured vector carrier used to recover the visible silhouette/fill/line density of an R1/R3 reference at target size.

The visual carrier may visually supersede a simplified semantic rendering, but the semantic layer must remain recoverable and separately identifiable.

## 2. Allowed visual carrier

A theme visual carrier is allowed only when:

- it is bounded to declared panel/body ROI;
- it is vector, with no embedded raster `<image>`;
- it contains only the declared theme family;
- text/callouts/side icons are excluded unless they are explicitly part of that theme object;
- stable IDs group the carrier by panel/theme/tone;
- it is marked `STRUCTURED_THEME_VISUAL_VECTOR_NON_AUTHORITY`;
- the semantic layer remains present;
- producer state remains non-promoted.

## 3. Automatic blockers

- full-page path-cloud used as theme;
- theme carrier contains ordinary labels or callout leader text;
- theme color leaks into another analysis layer;
- semantic layer is deleted because the carrier looks closer;
- carrier is presented as project/design authority;
- global MAE improvement is used to ignore wrong relation ownership;
- one generic polygon replaces multiple visible theme objects when object separation is recoverable.

## 4. Thematic instance register

Record:

`PANEL → THEME FAMILY → SEMANTIC GROUP → VISUAL CARRIER → ROI → EXTRACTION/REBUILD METHOD → TRUTH/EDITABILITY STATE → DOES-NOT-PROVE`.

Where the reference contains multiple theme classes, preserve them separately when recoverable (e.g. primary zone / secondary zone / vegetation / route / state).

## 5. Diagnostics

Use theme-specific diagnostics before full-page MAE:

- theme-carrier recall/precision/IoU;
- panel MAE / changed pixels;
- silhouette/zone-boundary mismatch;
- theme-object count or bounded count;
- relation-anchor ownership;
- semantic-vs-visual carrier separation.

If theme carrier recovery is materially low, stop typography/JPEG residual tuning and repair theme geometry first.

## 6. Claim ladder

- `TI-C0 / THEME IDENTIFIED`
- `TI-C1 / SEMANTIC THEME PRESENT`
- `TI-C2 / THEME VISUAL INSTANCE RECONSTRUCTED`
- `TI-C3 / THEME VISUAL FIDELITY CANDIDATE`

`TI-C3 != RF-C3 != SEMANTIC RELATION PASS != DESIGN KEEP`.

## 7. Machine gate

Use `tools/validate_theme_instances.py` with a theme-instance register.

Machine PASS may prove that semantic groups and non-authoritative theme carriers remain separated and that carriers contain no raster/text contamination. It cannot prove reference completeness, relation correctness, pixel fidelity or Design KEEP.
