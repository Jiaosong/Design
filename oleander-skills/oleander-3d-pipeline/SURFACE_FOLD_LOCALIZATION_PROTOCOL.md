# SURFACE FOLD LOCALIZATION PROTOCOL

Status: reusable OLEANDER 3D Skill extension.

## Principle
`Projection convergence ≠ valid primary skin.` A candidate may pass SIDE / FRONT / REAR projection screens while its primary surface contains local fold reversals. Fold count alone is insufficient for efficient failure routing.

## INPUT
- pre-aperture primary-skin mesh;
- candidate revision;
- surface-quality receipt;
- semantic control families / station or rail identifiers when available.

## MUST CHECK
For every adjacent-face reversal beyond the configured normal-dot threshold, record:
- shared edge vertex IDs;
- adjacent face IDs;
- face-normal dot product;
- world-space edge center;
- nearest longitudinal / vertical station when available;
- nearest semantic rail / form family when available.

Group mirrored or spatially adjacent failures into one causal cluster before editing geometry.

## FAILURE ROUTING
- repeated folds across consecutive longitudinal stations at one rail → fix longitudinal blend / control-family transition;
- mirrored pair at one station → fix cross-section ordering / shoulder-to-side relation;
- folds created only after adding transition rails → remove the rail fan and solve the causal section function;
- clean topology but projection failure → do not edit topology; route to the relevant form envelope;
- projection gates all pass but folds remain → `MACHINE_REJECT`; never promote.

## FORBIDDEN
- treating fold count reduction alone as reference-fidelity improvement;
- smoothing / subdivision used to conceal a control-grid reversal without fixing Source/causal geometry;
- deleting the topology gate because projection metrics are green;
- reporting only a count when spatial localization is available.

## EVIDENCE
`SURFACE_FOLD_DIAGNOSTIC.json` should contain at minimum:
- `candidate_revision`;
- `fold_count`;
- `folds[].edge_vertices`;
- `folds[].face_indices`;
- `folds[].normal_dot`;
- `folds[].center_m`;
- `authority = DIAGNOSTIC_NOT_REFERENCE_AUTHORITY`.

## Does not prove
Zero localized folds does not prove Class-A/G2/G3 continuity, reflection quality, manufacturability or reference fidelity.