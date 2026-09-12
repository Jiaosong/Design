# Per-Gate Best-Known Baseline Protocol v1

Status: CURRENT CANDIDATE.

Purpose: preserve machine evidence improvements from a globally rejected experiment without promoting the whole candidate or weakening unrelated gates.

## INPUT
- current per-gate best-known baseline table;
- candidate machine receipts measured by comparable methods;
- global visual/design state;
- evidence source for every baseline value.

## MUST CHECK
1. A globally `REJECT` candidate may still establish a stronger **machine baseline for one gate** when the measurement is comparable, externally grounded, and not a self-referential target-compliance score.
2. Updating one gate does not promote the candidate revision as LKG / Design KEEP.
3. Every per-gate baseline stores revision + exact value + evidence source.
4. Future experiments compare against the strongest valid baseline for each gate, not one convenient whole-revision snapshot.
5. Do not adopt a new baseline if the measurement method changed materially or if the candidate value was generated directly from the same target without independent measurement.
6. Visual/reference/design gates remain independent and cannot be upgraded by a machine-baseline update.

## ALLOWED
- V31 may become the FRONT projected-profile machine baseline while V25 remains the stronger baseline for SIDE/rear/aperture gates and both whole models remain visual REJECT/HOLD.
- keep mixed-revision best-known tables when each gate has provenance.

## FORBIDDEN
- `one gate improved → candidate promoted`;
- replacing a stronger gate baseline with a newer-but-weaker revision;
- accepting non-comparable metrics as best-known;
- using owner visual opinion as a machine-baseline source;
- treating per-gate baseline as manufacturer truth.

## EVIDENCE
Persist `best_known_gate_baselines` in the regression receipt, with exact revision/value/evidence source. Promotion validator must fail if a weaker or mismatched baseline is supplied.

## 992.2 benchmark
V31 remained `KEEP_LKG_REJECT_EXPERIMENT`, but its FRONT projected-profile RMSE reached `0.07230088060916158`, stronger than V25 `0.07770408603407701`, with the same final evaluated Y/Z projection method. Therefore V32 uses V31 as the FRONT machine baseline while retaining V25/V23 for the other best-known gates. This does not make V31 a visual LKG and does not change the independent visual HOLD.
