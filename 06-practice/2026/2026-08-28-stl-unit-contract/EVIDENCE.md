# STL Unit Contract Validation — 2026-08-28

Status: `PRACTICE_EVIDENCE / TRAINING_MODE / NO_PROMOTION`

## GAP

Current 3D/CAD exchange evidence can prove that an STL reopens with intact numeric geometry, but STL does not carry authoritative unit semantics. A downstream consumer can therefore interpret the same `120 × 60 × 10` numeric mesh at a different physical scale while the file still appears geometrically valid.

This is materially different from the preceding DXF test: DXF has an `$INSUNITS` field that can be authored and reopened; STL has no equivalent authoritative embedded unit field.

## EXISTING OWNER / RNO

- Validation owner: existing `oleander-delivery-qc`.
- 3D source/exchange owner when project-bound: existing `oleander-3d-pipeline`.
- Technical Drawing remains the existing PR #172 Candidate lineage; no parallel Skill or validator family is created.
- Required Native Output for this bounded exercise: STL mesh + explicit external unit contract + reopen/hash/bbox validation.

## ACTUAL ARTIFACT / CAPABILITY PROBE

Execution surface:
- CadQuery `2.8.0` available.
- trimesh `4.11.1` available.

Synthetic training fixture generated as an asymmetric box with numeric extents `120 × 60 × 10`.

Observed local artifact:
- STL SHA256: `5b21f0be7bd00ebad54fafd63cefe8eae14782b15394f521da9ec6ba122ecfe0`
- reopened numeric extents: `[120.0, 60.0, 10.0]`
- reopened `trimesh.units`: `None`
- STL header: `STL Exported by Open CASCADE Technology [dev.opencascade.org]`

The exact numeric dimensions are training-only and are not project or manufacturing data.

## A / HOLD — RAW STL ONLY

Test: reopen the STL and inspect numeric bbox + available unit metadata.

Result:
- numeric geometry survives;
- embedded unit authority is absent;
- therefore `REOPEN + BBOX MATCH` is insufficient for physical-scale exchange.

Verdict: `HOLD / STL_HAS_NO_AUTHORITATIVE_UNIT_CONTRACT`.

## REPAIR

Add a sidecar JSON contract bound to the exact STL by:
- artifact filename;
- SHA256;
- declared unit;
- expected numeric bbox;
- explicit `unit_authority=EXTERNAL_MANIFEST_REQUIRED_FOR_STL`.

This does not pretend STL gained native unit semantics. It makes the missing authority explicit and machine-checkable.

## B / RETEST — STL + EXTERNAL UNIT CONTRACT

Observed sidecar fields:

```json
{
  "schema_version": "1.0",
  "artifact": "oleander_stl_unit_contract.stl",
  "sha256": "5b21f0be7bd00ebad54fafd63cefe8eae14782b15394f521da9ec6ba122ecfe0",
  "declared_unit": "mm",
  "expected_bbox": [120.0, 60.0, 10.0],
  "unit_authority": "EXTERNAL_MANIFEST_REQUIRED_FOR_STL"
}
```

Retest checks:
1. exact artifact hash matches;
2. reopened bbox matches the manifest;
3. declared unit exists and is supported;
4. unit authority is explicitly external rather than falsely reported as embedded.

Observed retest: all four checks pass.

Verdict: `PASS_FOR_BOUNDED_EXCHANGE` only.

## PROVEN

- STL can reopen with intact numeric geometry while carrying no authoritative embedded unit semantics.
- Numeric bbox preservation alone cannot prove physical scale.
- A hash-bound external unit contract can fail closed when unit authority is missing and can make a bounded STL exchange package machine-checkable.

## NOT PROVEN

- downstream CAD/slicer/importer scale handling;
- 3D-printer or CAM machine interpretation;
- mesh tolerance/facet suitability for manufacturing;
- engineering/manufacturing approval;
- field truth;
- that STL is an appropriate authoritative master when a unit-aware native/exchange format is available.

## TRANSFER RULE

`STL NUMERIC GEOMETRY ≠ PHYSICAL SCALE AUTHORITY.`

For any dimension-sensitive STL handoff, require an external, artifact-bound unit contract and reopen the exact artifact. Prefer a unit-aware authoritative native/exchange format when the workflow supports it. STL + sidecar is a bounded exchange safeguard, not a replacement for a better master format.

## MATURITY

`PRACTICE_EVIDENCE`.

Next valid evidence should be a materially different downstream consumer test (for example a slicer/CAD importer) using the same hash-bound unit contract, or real project usage with authoritative dimensions. Repeating the same CadQuery→trimesh loop is not material delta.
