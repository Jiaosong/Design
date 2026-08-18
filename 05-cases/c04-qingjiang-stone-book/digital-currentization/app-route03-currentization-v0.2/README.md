# C04 App｜ROUTE-03 Currentization Module v0.2

Executable bounded App currentization for `PRJ-C04-DIGITAL-INTERACTION [P3]`.

This is **not** a full App v1.28 and does not promote v1.26, v1.27, or this module to Current. It materializes the compatible chain:

`v1.25 specialist baseline → v1.26 Product/Journey/IA/Service → v1.27 navigation/game architecture → ROUTE-03 currentization`.

## v0.2 material delta
- Restores the v1.26 start order: **fail-closed first**, then `APP_INIT → MODE(optional) → OFFLINE_PREP` when the state permits entry.
- Default project state remains `UNKNOWN`, so boot lands in SERVICE rather than pretending the route is open.
- QUICK / DEEP / FAMILY remain reading-density choices; `MODE != PERSONA`, no level/reward/route permission.
- OFFLINE PREP states what is actually embedded in this bounded build and does not claim the full R01–R13 screens are duplicated here.
- Reading mode / `setupSeen` framework state has storage code, scoped to a new currentization key; cross-reload persistence could not be verified on the CDP `about:blank` test surface because localStorage raises `SecurityError` there.
- Hidden prototype status control supports OPEN / DEGRADED / CLOSED / UNKNOWN and is labelled `NOT LIVE STATUS`.
- FULL / LIGHT / OFF digital states; OFF withdraws optional explanation and preserves route/Return continuity.
- Return Guard elevates under UNKNOWN/CLOSED and interrupts lower-priority behavior.
- Reduced Motion preserves the same state grammar; tested running-animation count = 0.
- measured visible button target minimum = 44 px on the test surface.
- route geometry remains the ROUTE-03-derived carrier; A/B/C/D only move viewport/focus.

## Bounded scope
TODAY and MY BOOK remain primary-IA placeholders from v1.27 architecture; this module intentionally does not fabricate complete screens. Full regression remains required after writable v1.27 is materialized and patched.

Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT GPS / STATUS UNKNOWN`.

Review state: producer/runtime readback only. Independent finished-pixel Design Crit remains required.
