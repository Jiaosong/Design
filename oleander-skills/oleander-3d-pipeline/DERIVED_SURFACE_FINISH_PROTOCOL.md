# DERIVED SURFACE FINISH / FINAL APERTURE BOUNDARY PROTOCOL

Status: reusable OLEANDER 3D Skill extension.

## Principle
A clean Source cage, zero pre-aperture folds and passing gross projections do not prove that the **final visible Derived surface** is professionally resolved.

`Source topology PASS ≠ Derived surface finish PASS ≠ Aperture-boundary PASS ≠ Reference fidelity KEEP`

## Topology mode must be explicit
Final display bodies may legitimately use different topologies:
- `CLOSED_SOLID_BOOLEAN`: every final body edge is expected manifold; apertures are volumetric cuts/recesses/tunnels.
- `OPEN_SURFACE_APERTURE_SHELL`: windshield/glass openings are real boundary loops in a surface shell; declared aperture boundary edges are expected and must not be counted as defects.

For open shells, distinguish:
`expected aperture boundary edges` from `unexpected non-manifold edges`.
A validator that rejects every open boundary is invalid for a true surface-shell aperture architecture.

## MUST CHECK
- Source/pre-aperture topology remains independently traceable;
- any subdivision/smoothing stage is declared as Derived execution, not new Source authority;
- final body connected-component count;
- declared topology mode;
- expected aperture boundary edge count and loop count where applicable;
- **unexpected** non-manifold edge count;
- aperture-region edge p95; report max edge but do not reject a long straight/low-curvature legal boundary on max length alone;
- aperture-region sliver-face count / minimum face area;
- boundary construction method (`BOOLEAN_CUTTER`, `DENSE_SURFACE_BOUNDARY_LOOP`, `SHARED_BOUNDARY_PATCH`, etc.);
- glazing/host relationship;
- actual broad and 3/4 visual readback.

## ALLOWED
- one or more Derived subdivision levels when the Source cage remains recoverable and dimension/profile regression is rechecked;
- continuous boolean cutters generated from calibrated aperture envelopes;
- an open surface shell with explicitly declared, localized aperture boundary loops;
- separate final-surface diagnostic receipts.

## FORBIDDEN
- treating SubD as a fix for wrong macro form;
- smoothing or beveling to hide a Source fold;
- deleting coarse host faces as final aperture construction;
- using a clean pre-aperture receipt to claim final post-operation boundary quality;
- counting legitimate declared aperture boundaries as unexpected non-manifold defects;
- rejecting a long straight boundary from max-edge length alone when p95/deviation/sliver evidence is clean;
- promoting because final topology is technically valid while aperture edges remain visibly faceted or distorted.

## EVIDENCE
`FINAL_DERIVED_SURFACE_RECEIPT.json` v2 containing at minimum:
- `candidate_revision`;
- `source_surface_revision`;
- `derived_surface_method`;
- `subdivision_level`;
- `topology_mode`;
- `final_connected_components`;
- `expected_aperture_boundary_edge_count`;
- `aperture_boundary_loop_count`;
- `unexpected_nonmanifold_edge_count`;
- `aperture_region_edge_p95_m`;
- `aperture_region_edge_max_m` (diagnostic, not a sole veto);
- `aperture_region_sliver_face_count`;
- `aperture_region_min_face_area_m2`;
- `machine_finish_state`;
- `visual_review_state`;
- `does_not_prove`.

Allowed machine states are only `MACHINE_SURFACED_VISUAL_HOLD` or `MACHINE_SURFACE_FINISH_REJECT`.

## Failure routing
- Source clean + unexpected final non-manifold/slivers → repair Derived operation order/boundary construction, not Source silhouette.
- expected open boundaries outside declared aperture regions → reject topology classification.
- aperture p95 high / boundary visibly faceted → densify Derived surface before the cut or generate explicit boundary rails.
- final surface clean but first-read object still generic → route back to Primary Form Identity Gate.
- projection regresses after SubD → reject Derived surface experiment; do not relax LKG thresholds.

## Does not prove
Class-A/G2/G3 continuity, manufacturer CAD, tooling, sealing/flange engineering, manufacturability, homologation, physical CMF or commercial IP clearance.