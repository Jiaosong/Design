# OLEANDER 3D Pipeline — Evaluated Mesh Projection Protocol v1

Use when geometry silhouette must be measured independently of render materials, compositor, world, alpha or lighting.

Core rule:

`Final evaluated geometry projection` is valid geometry-screening evidence when it is derived from the final dependency-graph mesh after modifiers and transforms.

It does not replace beauty/reference review or surface-quality diagnostics.

## Method
For an orthographic reference axis:
1. obtain the final evaluated mesh from Blender dependency graph;
2. transform triangle vertices into world coordinates;
3. project onto the locked orthographic plane;
4. for each target scan coordinate, intersect the scan line with projected triangles;
5. compute final union top/bottom or left/right envelope from triangle intersections;
6. compare to independently calibrated reference targets.

For SIDE automotive screening use world `X/Z` projection. For FRONT/REAR use `Y/Z` projection. Camera/render state is irrelevant to this pure geometry measurement.

## Why triangle intersections, not vertices only
Vertex extrema can miss the true projected silhouette between vertices and can misread wheel openings. Projected triangle-line intersections measure the evaluated face union and correctly respect holes where no face exists.

## MUST CHECK
- evaluated dependency-graph mesh, not Source target table;
- world transforms applied;
- triangulation generated from final evaluated polygons;
- reference target provenance separate from candidate projection provenance;
- scan direction and world axes locked before seeing the result;
- final visible patch network membership explicit;
- no hidden construction/diagnostic geometry included.

## FAIL
- `FAIL_EVALUATED_MESH_PROJECTION_EMPTY`
- `FAIL_EVALUATED_MESH_PROJECTION_SOURCE_MIX`
- `FAIL_PROJECTION_AXIS_UNRESOLVED`
- `FAIL_FINAL_VISIBLE_MEMBERSHIP_UNRESOLVED`

## Gate separation
`EVALUATED_MESH_PROJECTION_SCREENING_PASS/FAIL` is geometry evidence only.
It cannot self-promote `REFERENCE_FIDELITY_REVIEW_KEEP`, `SURFACE_QUALITY_KEEP` or `DESIGN_QUALITY_KEEP`.

## 992.2 transfer
V14–V18 demonstrated that renderer-based masks can fail for reasons unrelated to geometry (buffer dimensions, alpha semantics, compositor/background, frame clipping). V19 moves SIDE silhouette screening to evaluated triangle intersection while keeping actual beauty renders for human reference review.
