# Automotive v0.11｜Hard-Point-Correct Source Rebaseline

Decision: `R25 WORKING_SOURCE RETAINED / R27-R28 AUDIT_ONLY / HUMAN M5 REVISE`

## Evidence correction

The visible wheel asset used through the earlier R25–R28 visual reviews did not satisfy the locked wheel OD. Its world-space X/Z envelope was approximately `0.71 × 1.0792 m` while the design hard point is `0.70 m OD`.

A reusable `wheel_hp_contract.py` now enforces, on actual rendered/evaluated wheel geometry:
- X/Z OD = `0.700 m`;
- current runtime front/rear centers and ±Y sides;
- FL/RL positive Y, FR/RR negative Y;
- original Y tire thickness retained;
- no body Source change.

## A/B

Source-locked R25 and R28A were rendered with identical HP-correct wheel package and identical 9-view diagnostic evidence.

Both Machine PASS.

Human M5 comparison retains **R25** because it has materially cleaner:
- side silhouette;
- shoulder/body continuity;
- Strip/Grazing highlight flow;
- local wheel-zone surface economy.

R28A/R28C remain more faceted and show repeated radial/comb-like folds even after wheel correction, crown inset and zero-bulge testing.

## Authority

Current source authority:

`R25 Source + wheel_hp_contract.py`

R25 Source hash:

`6ae67c33aafb6da9f64359784e0cabb4fe9fb36b5bf62b91e49a0fa5348b9adf`

This is a **working baseline**, not promotion authority.

## Remaining Human M5 defects

1. front fender crown reads as a local cap rather than a shoulder-fed volume;
2. hood–fender–shoulder relation pinches around the front wheel zone;
3. rear crown is cleaner than front but remains locally isolated;
4. wheel-opening endpoints still need bounded cleanup;
5. no evidence supports reopening the full shoulder-to-rocker patch again.

## Next

`R29｜Local Fender Crown Integration`

Only a bounded crown/shoulder dependency may reopen initially. Current wheel package, R25 opening scale, R09 hard points, non-wheel R11/R12 source, and R18/R20 terminations remain locked.

M6/M7/M8 remain blocked.
