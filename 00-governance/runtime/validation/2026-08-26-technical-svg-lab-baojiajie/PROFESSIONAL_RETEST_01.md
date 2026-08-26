# Technical SVG Lab｜Professional Retest 01

Date: 2026-08-27
Verdict: **R01–R05 REPAIR RETEST PASS / INDEPENDENT KEEP OPEN / ACTIVE NOT GRANTED**

Artifact-first readback now makes the two blocking production states visible without side-panel or receipt lookup: `TARGET 140×180 / ACTUAL 136×184 / MISMATCH` and `BLEED PATH OPEN`. The production `BLEED` layer remains empty; the warning lives in non-print status information.

- R01 PASS — target/actual mismatch is first-read and the target envelope is visibly an error/reference state.
- R02 PASS — `BLEED PATH OPEN` and supplier/converter input requirement are visible while no bleed geometry is fabricated.
- R03 PASS — finished-sheet legend distinguishes CUT / SAFE / BLEED / TARGET / NONPRINT.
- R04 PASS — SAFE reads `SUPPLIED / UNVERIFIED`.
- R05 PASS — object ID, revision, units, risk state and vendor-confirm state are present; artwork placeholder is demoted.
- Layout regression repaired — all SVG text bboxes are inside the viewBox; no clipping or overlap remains in final readback.
- Rounded-rectangle mode regression PASS; invalid custom CUT still fails closed.

Persistent readback: `/Oleander/90_Archive/Runtime-Validation/2026-08-27/Technical-SVG-Lab-Retest-01`.

Project truth remains HOLD: actual CUT is 136×184 vs target 140×180; BLEED source path is absent; vendor/converter confirmation and supplier proof/tolerance/sample remain OPEN.

This is a professional artifact retest, not an Independent KEEP. ACTIVE promotion remains withheld until a separate independent review grants KEEP.

Existing Cloud-Free CI must remain green, but `CI PASS ≠ Browser/Artifact Design PASS ≠ Independent KEEP`.