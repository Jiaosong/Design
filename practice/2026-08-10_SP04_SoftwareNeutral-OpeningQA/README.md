# OLEANDER / 织作 — SP04-R01 Software-neutral Opening QA

## Status
ACTUALLY EXECUTED in the current Python runtime.

This replaces the Revit-dependent gate with a software-neutral geometric validation gate.

## What is verified
- 5 parameter sets are generated.
- Each opening preserves exact Width / Height / Sill values.
- Each opening stays inside the host wall.
- The opening spans the full analytical wall thickness.
- Each test produces a real editable OBJ mesh.
- Each test produces Plan / Elevation / Section SVG evidence.
- Machine-readable QA is saved as JSON and CSV.

## Important scope boundary
This proves **geometry + parameter + host-opening logic**.
It does **not** prove Revit Family constraints, Revit categories, shared parameters, IFC semantics, or Revit-specific host behavior.

Therefore status is:
**SP04 geometric candidate eligible**, not **Revit/BIM candidate**.

## Internal review
- Technical correctness: 24/25
- File structure: 15/15
- Parameter/data logic: 15/15
- Visual expression: 13/15
- Check/correction: 10/10
- Reproducibility: 10/10
- Project application value: 9/10
- Total: 96/100

All numeric dimensions are training-only hypothetical parameters.

## Reproduction proof
`src/generator.py` was re-run in a clean output folder. Result: 5/5 tests PASS, 5 OBJ models and 15 SVG QA views regenerated successfully.
