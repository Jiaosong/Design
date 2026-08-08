# 2026-08-08 | SP01 | GIS Density Sensitivity

Status: TRAINING PROTOTYPE / QGIS EXECUTION PENDING.

## Objective
Distinguish observed point pattern from analysis scale by testing kernel-density bandwidth sensitivity. This follows the current Business / Culture / IP / Spatial governance; primary node is SP01 Site & Evidence. No Legacy training-series name is used.

## Reproduce in QGIS
1. Load `training_points.csv` as a delimited point layer.
2. Replace the training plane with a projected CRS appropriate to the real site before project use.
3. Run **Heatmap (Kernel Density Estimation)** at radii 75 / 150 / 300 m and pixel size 25 m.
4. Use `weight` as weight field.
5. Compare hotspot count, continuity, edge effects and whether the spatial claim changes with bandwidth.
6. Export only after CRS, extent and parameter checks pass.

All bundled coordinates and numeric values are **exercise-only hypothetical parameters**. QGIS was not available in the automation runtime, so GeoTIFF/QGZ output is NOT RUN and must not be claimed as completed. Offline matrices are sensitivity evidence only, not QGIS output.

## Internal review
21/25 technical correctness; 15/15 file structure; 15/15 parameter/data logic; 13/15 visual expression; 9/10 check/correction; 9/10 reproducibility; 9/10 project value = **91/100**.

Candidate rule: **NO**. A score above 90 does not override the evidence gate: actual QGIS execution with real projected CRS and authoritative project data remains required.

## Authoritative references
- QGIS 3.44 Processing / Heatmap (Kernel Density Estimation): https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/interpolation.html
- QGIS 3.44 Create grid: https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/vectorcreation.html
