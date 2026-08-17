# Reconstruction Fidelity Calibration Fixtures

Status: `SYNTHETIC CALIBRATION / NOT GOLDEN PROMOTED / NOT PROJECT AUTHORITY`

These fixtures prove different reconstruction contracts without conflating pixel similarity, semantic editability, technical truth or Design KEEP.

## RF-CAL-01 — pixel forensic + coupled solver

`RF-CAL-01` proves that reconstruction-fidelity tooling can detect and repair bounded drawing mismatches under a locked renderer and that a high global similarity percentage cannot substitute for a strict RF-C3 contract.

### Files

- `RF-CAL-01_REFERENCE_MASTER.svg` — synthetic editable vector reference.
- `RF-CAL-01_CANDIDATE_BAD.svg` — deliberate geometry, typography and stroke mismatch.
- `RF-CAL-01_CANDIDATE_MATCH.svg` — independently grouped editable vector candidate with the same visible geometry as the reference.
- `RF-CAL-01_ROIS.json` — critical/major title / primary geometry / dimensions / callout / title-block diagnostic regions.
- `RF-CAL-01_EXPECTED.json` — machine-readable tolerance-zero regression expectations and invariants.
- `RF-CAL-01_RF-C3_CONTRACT.json` — hard RF-C3 zero-difference contract.
- `RF-CAL-01_RUNTIME_READBACK_v0.3.json` — recorded tolerance-zero / edge-radius diagnostic readback.
- `RF-CAL-01_SOLVER_SPEC.json` — bounded E2/E3/E4 parameter search specification.
- `RF-CAL-01_SOLVER_RESULT.json` — actual coupled-solver recovery and renderer-mismatch finding.
- `../../tools/reference_fidelity.py` — same-canvas raster comparison and hard-contract tool.
- `../../tools/svg_parameter_solver.py` — bounded editable SVG parameter solver.
- `../../references/PIXEL_FORENSIC_PROTOCOL.md` — strict forensic reconstruction protocol.
- `../../references/PIXEL_SOLVER_PROTOCOL.md` — solver routing, coupling and renderer-lock protocol.

### Deliberate negative mutations

`CANDIDATE_BAD` contains four explicit reconstruction failures across three classes:

1. primary geometry shifted +5 px in X;
2. one interface rectangle stroke changed from 2.2 to 2.8 output units;
3. main title baseline moved +3 px;
4. main title size changed 32 → 31.

The rest of the fixture is intentionally held constant so the difference evidence remains attributable.

### Actual strict readback

The negative candidate demonstrated that roughly 98%+ unchanged full-canvas pixels are not a passing argument when critical geometry/typography/stroke ROIs still fail.

The matched candidate under one locked synthetic renderer produced:

- exact-equal pixel ratio: `1.0`;
- changed-pixel ratio at tolerance 0: `0.0`;
- MAE: `0.0`;
- RMSE: `0.0`;
- estimated translation: `dx=0 / dy=0`;
- edge unmatched r0/r1/r2: all `0.0`.

The coupled solver additionally demonstrated that typography/geometry/stroke parameters must be reopened across cycles and that cross-renderer optimization can choose a false optimum.

`WRONG RENDERER → WRONG OPTIMUM`.

This supports only `RF-C3 PIXEL-EXACT CANDIDATE IN THIS LOCKED SYNTHETIC FIXTURE`. It does not award independent review.

---

## ML-REL-01 — multilayer semantic relationship reconstruction

`ML-REL-01` exists because a second real calibration exposed a different failure mode: an SVG can look close to a stacked analytical reference while its repeated bases, routes, zones, leaders and symbols remain anonymous path-cloud fragments.

Files:

- `ML-REL-01_SEMANTIC.svg` — synthetic three-panel stacked reconstruction with one reusable master base, route/zone/node relations, callout topology and reused symbol component.
- `ML-REL-01_RELATION_REGISTER.json` — machine-readable panel/base/relation/symbol contract.
- `../../tools/validate_semantic_reconstruction.py` — semantic reconstruction structural gate.
- `../../references/MULTILAYER_RELATION_RECONSTRUCTION.md` — shared-base genealogy, relation evidence, semantic editability, callout topology, symbol dictionary and dual-track repair protocol.

The validator checks:

- multiple panels reuse one declared `MASTER_BASE` through `<use>`;
- panel/base genealogy is explicit;
- registered relation groups and carriers exist;
- a relation marked `DRAWN` cannot use text as its only carrier;
- targets exist;
- declared callouts contain `LABEL → LEADER → ANCHOR → TARGET`;
- repeated symbol families actually have repeated instances;
- the fixture remains non-promoted.

Current synthetic regression output:

`OLEANDER SEMANTIC RECONSTRUCTION: STRUCTURE PASS`

This does **not** mean the pixels match a reference. It proves only the editability/relationship structure that a path-cloud trace lacks.

Hard boundary:

`LOWER PIXEL ERROR ≠ BETTER EDITABLE RECONSTRUCTION`.

The correct multilayer workflow keeps visual extraction and semantic reconstruction separate until both axes are reconciled.

---

## Claim model

- `RF-C0` — structural reconstruction;
- `RF-C1` — measured geometry fidelity;
- `RF-C2` — render-locked high fidelity with explained residuals;
- `RF-C3` — pixel-exact candidate: tolerance-zero, zero unexplained in-scope changed pixels, locked renderer/font/color environment, independent review pending.

Semantic editability is reviewed separately:

`RASTER SUBSTITUTE → PATH-CLOUD TRACE → STRUCTURED VECTOR → SEMANTIC VECTOR`.

## Gate interpretation

- Pixel forensic/solver structure PASS does not imply technical or Design PASS.
- Semantic reconstruction structure PASS does not imply pixel fidelity or professional finish.
- `RF-G6` remains an independent-review boundary; this README is producer evidence only.
- `RF PASS != TD PASS`.
- A reference can be matched perfectly and still be technically unsuitable for a current OLEANDER project.
- A project adaptation may intentionally deviate from the reference when current geometry, evidence, safety, engineering or FIELD truth requires it.
