# CH10 Web v0.1 — Producer Implementation Readback

## Scope
Five-page Web carrier for `CH10｜十三印内容与互动系统`.

## Correct ownership
CH10 defines the upstream content/interaction grammar of R01–R13.
It does not own route geometry or App navigation. CH11 remains the digital/App implementation owner.

## Materialized pages
- CH10-P01 — 13 OPTIONAL READINGS / route ≠ content order
- CH10-P02 — R01–R13 index; unknown items stay FIELD OPEN
- CH10-P03 — S0/S1/S2/DEEP optional depth; not progress
- CH10-P04 — experience interaction verbs; screen interaction is subordinate
- CH10-P05 — R13 silence proof; PASS can turn optional content OFF

## Producer-side defects found and repaired
1. First P01 composition let the faint ROUTE-03 trace cross close to the R01–R13 circles, risking a false “13 route nodes” reading. Repaired by separating the route trace from the imprint field.
2. First fixed chapter-nav targets were 34 px. Repaired to 44 px minimum.
3. Added section scroll-margin so fixed chapter chrome does not obscure section first-read.

## Runtime evidence
1920×1080 and 390×844:
- horizontal overflow = 0
- minimum visible button target = 44 px
- tested JS/page errors = 0
- S2 depth interaction executed
- PASS experience verb executed
- R13 PASS and REOPEN state changes executed
- no continuously running animation in tested settled states

## Review boundary
Runtime/readback does not equal finished-pixel Design PASS.
Independent finished-pixel review remains required.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT GPS`
