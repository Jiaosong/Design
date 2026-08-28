# PRESENTATION Training Evidence — Typography × Read Distance

Status: `PRACTICE_EVIDENCE / TYPOGRAPHY-READ-DISTANCE MATERIAL DELTA / NO PROJECT WRITE / NOT ACTIVE`
Date: 2026-08-28
Owner route: `oleander-visual-design/TYPOGRAPHY_SYSTEM_EXTENSION.md` (Candidate extension); PRESENTATION installed compilation owner remains `oleander-story-and-board`.

## GAP
Current Typography Candidate requires intended reading-distance, far/near, longest-string and rendered readback, but had no direct A/B evidence proving how one semantic hierarchy should adapt across near Web, desk presentation and far board conditions.

## SOURCE
1. Smithsonian Accessibility Program — *Smithsonian Guidelines for Accessible Exhibition Design* — institutional exhibition-accessibility guidance. Public PDF: https://www.sifacilities.si.edu/sites/default/files/Files/Accessibility/accessible-exhibition-design1.pdf . Visible fact used: readability is affected by combined type size, spacing and line length; type size should suit probable viewing distance; label design must remain legible. PDF currently served by Smithsonian Facilities; publication provenance is institutional and the document describes itself as a living guideline.
2. U.S. Access Board — ABA/ADA visual-character guidance — https://www.access-board.gov/aba/guides/chapter-7-signs/ . Visible fact used: covered visual signs size characters according to viewing distance, with additional requirements for contrast, conventional forms, spacing and line spacing.
3. Existing OLEANDER external digestion: `2026-08-28_external-codex-skills-editorial-typography-digestion.md` (MIT source observed) already established role-first typography, long-string/narrow stress and actual desktop/mobile readback; this run does not repeat that evidence.

## LICENSE / RIGHTS
External sources are used as standards/professional calibration only. No Smithsonian/Access Board visual identity, Helvetica choice, fixed page template, branded typography, fixed point-size ladder or aesthetic preset is copied into OLEANDER. Accessibility numeric requirements remain medium-specific validation inputs, not universal OLEANDER aesthetic rules.

## VISIBLE FACT → DESIGN INFERENCE
- Visible fact: viewing distance materially changes legibility requirements; readability is not type size alone.
- Visible fact: spacing, line length, contrast and real viewing conditions remain part of readability.
- Design inference: cross-media typography should preserve semantic priority while adapting roles differently; a larger medium does not justify enlarging every text role equally.

## ARTIFACT
Editable HTML/CSS study with the same information in three target conditions:
- near Web `390×844`;
- desk `1440×900`;
- board `1600×1000`.

Readback includes real Chromium pixels, board grayscale and a reduced-size far-read perceptual proxy. The proxy is not a physical-distance compliance test.

## A/B
- `A` — nearly identical type treatment across distances: board first-read loses authority at reduced/far proxy.
- `B1` — scale all text together: PRIMARY becomes larger, but PROOF/support also gain excessive visual mass and the hierarchy flattens.
- `B2` — role-specific adaptation: PRIMARY + ACTION scale strongly for board; PROOF remains available at full resolution but stays a near-reading layer. No facts are removed.

## READBACK
`A` fails at far proxy because the primary statement loses enough visual mass to compete with the composition. `B1` repairs raw size but creates a second failure: proof/status becomes too prominent and total page depth grows. `B2` retains the same semantic order at Web/desk/board, preserves all proof text, and keeps the primary statement recognizable at thumbnail/far proxy while proof stays available on near read.

## FAILURE / ROOT CAUSE
Reading-distance adaptation was treated first as no adaptation and then as global scaling. Both ignore type-role hierarchy.

## REPAIR / RETEST
Declare type role and reading condition first; adapt role scale / measure / density independently; preserve complete information; retest actual Web/desk/board pixels, grayscale and far/near proxies. Physical signage character height, mounting, lighting and accessibility compliance go to VALIDATION.

## TRANSFER RULE
`DECLARE TYPE ROLE + TARGET READING CONDITION → ADAPT ROLE SCALE / MEASURE / DENSITY → KEEP SEMANTIC PRIORITY → PRESERVE FULL INFORMATION → RETEST ACTUAL PIXELS + FAR/NEAR PROXIES`

Counterexample / rejection rule:
`READING-DISTANCE ADAPTATION ≠ GLOBAL TYPE SCALE`.

## BOUNDARY
This is browser-based PRESENTATION evidence, not physical signage compliance, user-study proof or accessibility certification. Reduced screenshot scale is a perceptual proxy only. Do not convert Smithsonian / Access Board measurements into universal design ratios. Real physical output dimensions and accessible character-height requirements must be validated against the applicable medium and authority.
