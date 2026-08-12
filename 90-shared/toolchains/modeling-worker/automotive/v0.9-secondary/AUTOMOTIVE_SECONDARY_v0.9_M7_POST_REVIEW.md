# OLEANDER Automotive Secondary Geometry｜v0.9｜M7 Post-Review

**Status:** `M7 PASS WITH LIMITATIONS / CANDIDATE_AUTHORITY — SECONDARY GEOMETRY BENCHMARK`
**Source Authority:** `OLEANDER_Automotive_Primary_Surface v0.8 — CANDIDATE_AUTHORITY`
**Modeling Contract:** `v0.2 / Spec Patch v0.2.1`

## Decision
M7-R03 is promoted as the automotive secondary-geometry benchmark. The promoted v0.8 primary shell remains immutable; M7 is a derived working source.

## Runtime evidence
- Blender 5.2.0 LTS / Cycles CPU
- GitHub Run `31560494368`
- Job `94001602752`
- Artifact `9127559818`
- Artifact SHA-256 `7b7a8bb82cefe6068d6ce56cb84ecd7a0e5411e2349596a80b318eb20b495476`
- 8 diagnostic renders
- all workflow steps SUCCESS

## Source-lock evidence
`BODY_PRIMARY` mesh hash before/after M7-R03:
`dce1252385bb3825d09e2d028228c063c60f10c7b2292adf633608f7795584de`
→ identical.

M7-R03 generated 28 secondary components while leaving the F1 source mesh unchanged.

## Revision chain
- M7-R01 — Method PASS / Visual REVISE: applique wheel-arch strip, weak/floating lamp/fascia reading; CI output-name bug also found.
- M7-R02 — Machine PASS / Visual REVISE: hierarchy improved, but reveal/fascia still looked detached from the source shell.
- M7-R03 — PASS WITH LIMITATIONS: rebuilt directly from promoted v0.8 F1 source; wheel-arch reveals, rocker, fascia, lamp housing/lens and panel lines are shrinkwrap/conforming dependencies rather than overlays that rewrite primary geometry.

## Visual QA
PASS:
- wheel-arch reveal follows the body curvature and no longer reads as a thick applique trim;
- rocker remains subordinate to the body mass;
- headlamp and taillamp use housing + lens hierarchy;
- front/rear fascia is legible as secondary architecture;
- door/belt/hood/hatch reveals improve panel hierarchy without requiring M8 detail;
- Clay Strip/Grazing still expose the v0.8 primary surface instead of using M7 geometry to hide it;
- no global clipping/framing failure in the eight-view review set.

LIMITATIONS:
- v0.8 front primary volume remains broad/blunt; M7 does not silently change it;
- fender crown / hood relation remains the accepted F1 primary-surface limitation;
- lamp/fascia architecture is benchmark-level rather than a resolved vehicle design language;
- wheel internals are still guide geometry; mirror/handle/interior/wheel-spoke detail remains blocked until M8;
- no Class-A / engineering CAD / package / crash / aero / homologation / manufacturing claim.

## Promotion
`WORKING_SOURCE → CANDIDATE_AUTHORITY — SECONDARY GEOMETRY BENCHMARK`

v0.9 is frozen as the M7 rollback baseline. M8 must branch from it. If M8 exposes a primary- or secondary-architecture failure, reopen the relevant Gate instead of patching the authority in place.
