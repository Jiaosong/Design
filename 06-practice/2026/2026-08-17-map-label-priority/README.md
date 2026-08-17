# 2026-08-17 Map Label Priority Training

## Training question
How should OLEANDER route maps preserve critical decision labels under dense small-scale conditions without redrawing or simplifying authoritative topology?

## Existing skill reused
`oleander-data-viz` spatial authority preservation remains the geometry gate. This training adds a presentation-layer label gate rather than a new framework.

## Practice
A synthetic 13-node route network was rendered at the same topology through four iterations:

- v1 `SHOW EVERYTHING`: REJECT — all labels visible, weak decision hierarchy.
- v2 `PRIORITY + VARIABLE ANCHOR`: REVISE — typography hierarchy improved but all 13 labels still fit, so density strategy was not really tested.
- v3 compact: REVISE — density pressure caused P2 `R12 / EXIT` to be suppressed with a P4 label; this exposed a retention-policy bug.
- v4 compact: KEEP FOR TRAINING — P1/P2 receive retention rights; P3–P5 may move or suppress first. 12/13 labels remain visible; only P4 `R08 / STONE READ` is suppressed; no P1/P2 labels are hidden.

## Failure modes learned

1. Priority is not merely font weight or placement order. It must govern which labels are allowed to disappear.
2. `All labels visible` is not a completeness proof. Complete source data may require selective presentation at dense scales.
3. Label suppression must remain presentation-only; topology and source rows stay unchanged.
4. A compact-scale proof is necessary. Large authoring canvases can hide collision failures.
5. A lower-priority label must not survive by displacing Entry / Exit / Return / Safety / Decision labels.

## Transfer rule

`SOURCE TOPOLOGY → LABEL CLASS → RETENTION RIGHT → VARIABLE ANCHOR → COLLISION CHECK → SUPPRESS LOWER PRIORITY → COMPACT-SCALE REOPEN`

## External calibration

Mapbox symbol-layer documentation was used only as implementation precedent: collision handling, variable anchors, padding and sort-key are existing production mechanisms. The OLEANDER gate remains tool-agnostic.

## Boundary
Synthetic calibration network only. It does not represent C04 site geometry, measured distance, route availability, or field verification.

## Verdict
Practice: `v1 REJECT → v2 REVISE → v3 REVISE → v4 KEEP FOR TRAINING`.

Design quality and execution evidence remain separate; successful SVG/PNG export does not itself produce KEEP.
