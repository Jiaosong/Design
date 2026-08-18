# DERIVED SURFACE FINISH / FINAL APERTURE BOUNDARY PROTOCOL

Status: reusable OLEANDER 3D Skill extension.

## Principle
A clean Source cage, zero pre-aperture folds and passing gross projections do not prove that the **final visible Derived surface** is professionally resolved.

`Source topology PASS ≠ Derived surface finish PASS ≠ Aperture-boundary PASS ≠ Reference fidelity KEEP`

## Trigger
Use after primary form is stable enough to evaluate the final visible shell, especially when subdivision, booleans, trims, apertures or display-only surface refinement are introduced.

## MUST CHECK
- Source/pre-aperture topology remains independently traceable;
- any subdivision/smoothing stage is declared as Derived execution, not new Source authority;
- final body connected-component count;
- final non-manifold edge count;
- aperture-region edge p95 and max lengths;
- aperture-region sliver-face count / minimum face area;
- boundary construction method (`BOOLEAN_CUTTER`, `SHARED_BOUNDARY_PATCH`, etc.);
- glazing/host relationship;
- actual broad and 3/4 visual readback.

## ALLOWED
- one or more Derived subdivision levels when the Source cage remains recoverable and dimension/profile regression is rechecked;
- continuous boolean cutters generated from calibrated aperture envelopes;
- separate final-surface diagnostic receipts.

## FORBIDDEN
- treating SubD as a fix for wrong macro form;
- smoothing or beveling to hide a Source fold;
- deleting coarse host faces as final aperture construction;
- using a clean pre-aperture receipt to claim final post-boolean boundary quality;
- promoting because the final body is manifold while aperture edges remain visibly faceted or distorted.

## EVIDENCE
`FINAL_DERIVED_SURFACE_RECEIPT.json` containing at minimum:
- `candidate_revision`;
- `source_surface_revision`;
- `derived_surface_method`;
- `subdivision_level`;
- `final_connected_components`;
- `final_nonmanifold_edge_count`;
- `aperture_region_edge_p95_m`;
- `aperture_region_edge_max_m`;
- `aperture_region_sliver_face_count`;
- `aperture_region_min_face_area_m2`;
- `machine_finish_state`;
- `visual_review_state`;
- `does_not_prove`.

Allowed machine states are only `MACHINE_SURFACED_VISUAL_HOLD` or `MACHINE_SURFACE_FINISH_REJECT`.

## Failure routing
- Source clean + final non-manifold/slivers → repair Derived modifier/boolean order, not Source silhouette.
- final boundary edges too long but topology valid → densify Derived surface before cut or increase cutter/boundary sampling.
- final surface clean but first-read object still generic → route back to Primary Form Identity Gate.
- projection regresses after SubD → reject Derived surface experiment; do not relax LKG thresholds.

## Does not prove
Class-A/G2/G3 continuity, manufacturer CAD, tooling, sealing/flange engineering, manufacturability, homologation, physical CMF or commercial IP clearance.