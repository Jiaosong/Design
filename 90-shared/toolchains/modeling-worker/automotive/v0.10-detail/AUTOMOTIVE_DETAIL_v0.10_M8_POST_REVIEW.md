# OLEANDER Automotive Detail｜v0.10｜M8 Post-Review

**Status:** `M8 PASS WITH LIMITATIONS / CANDIDATE_AUTHORITY — DETAIL & INSTANCE BENCHMARK`
**Source Authority:** `OLEANDER Automotive Secondary v0.9 — CANDIDATE_AUTHORITY`
**Modeling Contract:** `v0.2 / Spec Patch v0.2.1`

## Runtime evidence
- Blender 5.2.0 LTS / Cycles CPU
- Run `31561128705`
- Job `94003451816`
- Artifact `9127774318`
- Artifact SHA-256 `6d0bd90f0d84a17697b3c157165d9e0fd222e8640a9991f455b5e828cba0ea4f`
- M8-R02 execution `72 s`
- 8 diagnostic renders

## Source lock
The full promoted v0.9 model scene hash is unchanged:
`824f5d124c0afb4bc52cab098d2ea668a155462346ed133a4bc1b0e556dc3ae8`
→ identical.
The v0.9 source object set is also unchanged (`31` source objects).

## Revision chain
- M8-R01 — Machine PASS / Visual REVISE: mirror too large, handle too contrasty/sticker-like, 40 split spokes + large hub made wheel center too heavy.
- M8-R02 — clean rebuild directly from promoted v0.9 source: smaller mirror; shorter/thinner/lower-offset handle; five clean spokes per wheel (`20` spoke objects total); smaller hub; restrained brake/caliper response.

## Visual QA
PASS:
- mirror is subordinate to glazing/body hierarchy;
- handle no longer reads as a large black rectangular applique;
- five-spoke wheel has clearer rim / hub / brake hierarchy and lower visual density;
- detail remains legible locally without destabilizing Hero scale;
- Clay Strip / Grazing continue to expose M5/M7 surface quality instead of hiding it;
- no global framing, clipping or occlusion failure in the eight-view set.

LIMITATIONS:
- front primary volume remains the accepted v0.8 broad/blunt limitation;
- mirror / handle / wheel design is benchmark-level, not a resolved vehicle design language;
- no interior package, production wheel architecture, door mechanism or sealing detail;
- M9 CMF / material binding has not been executed;
- no Class-A / engineering CAD / crash / aero / homologation / manufacturing claim.

## Promotion
`WORKING_SOURCE → CANDIDATE_AUTHORITY — DETAIL & INSTANCE BENCHMARK`

v0.10 is the M8 rollback baseline. M9/M10 must derive from it. Any later failure attributable to M5/M7 must reopen the appropriate Gate rather than mutate this authority in place.
