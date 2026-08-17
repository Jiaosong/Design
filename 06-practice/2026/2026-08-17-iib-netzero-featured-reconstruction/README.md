# IIB Netzero Featured Reconstruction — OLEANDER Practice

Status: `EXECUTED / SELF-CHECKED / REVIEW PENDING`

Reference project: **How to Get the World to Netzero by 2050** — Information is Beautiful.

Reference page:
`https://informationisbeautiful.net/visualizations/how-to-get-the-world-to-netzero-by-2050/`

Official featured image used as visual reference:
`https://infobeautiful4.s3.amazonaws.com/2021/10/CarbonZero-IIB-featured-image-960x485.png`

## Scope

This benchmark intentionally switches away from the prior Water World practice and reconstructs the Netzero project's featured visual as editable vector geometry.

Rebuilt elements:
- 512×512 dark field;
- cropped olive circle cluster at left;
- five-circle pink cluster;
- two-circle grey cluster;
- six-circle yellow cluster;
- circle centers, radii, outline-only rendering, crop relationships and approximate palette.

The source reference raster is **not embedded** in the SVG.

## Fidelity state

Current claim: `RF-C1 / GEOMETRIC-STRUCTURAL RECONSTRUCTION CANDIDATE`.

Not claimed: `RF-C3 / PIXEL-EXACT`.

Reason: the official visual can be viewed through the web reference, but its exact source raster bytes were not materialized into the local solver runtime for tolerance-zero pixel comparison. Circle coordinates, radii, stroke and color values are therefore visually measured approximations.

## What this benchmark tests

- clipped-object reconstruction at page edges;
- relative-radius fidelity;
- cluster topology and inter-circle spacing;
- thin-outline raster phase;
- palette separation on a dark field;
- semantic editability with stable circle IDs rather than a flattened path cloud.

## Artifact

`IIB_NETZERO_FEATURED_REPLICA.svg`

## Review boundary

`ARTIFACT EXISTS != RF-C3 != DESIGN KEEP`

Independent OLEANDER review remains required before promotion. This practice does not claim authorship of the reference project and does not replace the original source.
