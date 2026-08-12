# Automotive v0.11｜R28 Local Fender Patch Architecture Gate

Status: `CLOSED / MACHINE PASS / HUMAN M5 REVISE / SUPERSEDED_AS_SOURCE / AUDIT_ONLY`

## Why R28 was opened

R27A–R27E showed that direct circumferential-ring attachment into the inherited row4–row7 cage produced overshoot, hard exits, transition teeth or radial collar pinching. R28 therefore reopened the complete local fender window:

`wheel opening + fender crown + shoulder + mid-body + rocker transition`

as one local Primary patch.

## Executed R28 chain

### R28A｜Local U-boundary → polar wheel-opening patch
- 6 radial layers;
- outer U boundary reused locked body-cage anchors;
- one Source island, 4 triangles, 0 n-gons;
- Machine M5 PASS;
- Human M5 REVISE: direct attachment seam was reduced, but the patch remained folded/faceted and wheel evidence still looked inconsistent.

### Package diagnosis
A dedicated wheel-envelope audit found that the visible wheel asset implementation had an anisotropic X/Z envelope of approximately `0.71 × 1.0792 m` instead of the locked `0.70 m` wheel OD. The current R09 runtime wheel centers are retained at approximately:
- front x = `1.465 m`;
- rear x = `-1.355 m`;
- y = `±0.795 m`;
- z = `0.350 m`.

The wheel implementation defect is deterministic package/display geometry, not a body design variable.

### R28B｜Package-constrained inset crown
- visible wheel X/Z OD normalized to 0.70 m;
- R28A topology retained;
- inner crown changed from shoulder +26 mm to shoulder −18 mm;
- package lateral clearance ≈30 mm at axle center;
- Machine M5 PASS;
- Human M5 still showed folded/ridged local surface.

### R28C｜Zero-bulge radial patch
- R28B package/crown relation retained;
- R28A artificial intermediate radial bulge removed;
- Machine M5 PASS;
- Human M5 REVISE: Strip/Grazing and Hero views still show repeated comb-like/radial folds; arch lips remain hard and patch-like.

## Hard-point-correct A/B rebaseline

R25 and R28A were then rendered source-locked with the same corrected wheel package and identical 9-view evidence:
- X/Z wheel OD = `0.700 m`;
- FL/RL on `+Y`, FR/RR on `−Y`;
- wheel centers = current runtime hard points;
- Y tire thickness retained;
- far-wheel / open-cavity ambiguity isolated with derived-only wheelhouse evidence.

Both candidates Machine PASS.

Human A/B decision:

**R25 is materially stronger than R28A/R28C as the working Source baseline.**

R25 retains:
- cleaner side silhouette;
- cleaner broad/strip/grazing surface flow;
- less radial/faceted local fender distortion;
- simpler and more legible source construction.

R25 still does **not** pass Human M5. Remaining defects are smaller and better scoped:
- cap-like front/rear fender crown;
- hood–fender–shoulder pinching / local crown isolation;
- local wheel-opening endpoint cleanup.

## R28 decision

R28A/B/C are retained as **AUDIT_ONLY / SUPERSEDED_AS_SOURCE**. They are not deleted and remain valid evidence for the Modeling Worker method, especially the lesson that broader topology freedom does not justify a more complex Source if hard-point evidence was wrong upstream.

Current working baseline is:

`R25 Source geometry + wheel_hp_contract.py`

R25 Source hash is locked to:

`6ae67c33aafb6da9f64359784e0cabb4fe9fb36b5bf62b91e49a0fa5348b9adf`

## Required next gate

`R29｜Local Fender Crown Integration`

R29 must reopen a **smaller** dependency than R27/R28:
- wheel-opening proportions remain R25 unless direct evidence requires change;
- current corrected wheel package remains locked;
- non-wheel R11/R12 body source remains locked;
- only the local crown / hood–fender–shoulder relation may move initially;
- no ring-insert architecture;
- no broad shoulder-to-rocker patch rewrite;
- no Boolean / global SubD / n-gon concealment;
- same M5 visual matrix required.

`M6/M7/M8 remain BLOCKED` until Human M5 PASS.
