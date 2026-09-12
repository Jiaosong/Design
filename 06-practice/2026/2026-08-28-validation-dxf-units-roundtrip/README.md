# OLEANDER Validation Practice — DXF Units Roundtrip

Status: PRACTICE_EVIDENCE / TRAINING_MODE / NO PROJECT CURRENT MUTATION / NO PROMOTION

## GAP
Current shared runtime evidence proves DXF create/save/reopen, but not that a supplier-facing technical drawing preserves explicit unit semantics. Numeric geometry alone is insufficient because `120 × 60` can reopen unchanged while `$INSUNITS` is unitless.

## TEST / SOURCE
Existing owner: `oleander-delivery-qc`; Technical Drawing remains PR #172 Candidate lineage. Runtime: ezdxf. Required Native Output: DXF with explicit millimeter unit semantics plus reopened geometry readback.

## ARTIFACT / READBACK
- BAD case: closed 120 × 60 LWPOLYLINE, `$INSUNITS=0` Unitless → HOLD.
- REPAIRED case: same geometry, `$INSUNITS=4` Millimeters → PASS for this bounded test.
- Reopen confirms bbox remains 120 × 60 and polyline remains closed.

## FAILURE / ROOT CAUSE
A DXF can preserve numeric coordinates while leaving unit semantics undefined. File existence and successful reopen therefore do not prove dimension authority survives exchange.

## REPAIR / RETEST
Set document units explicitly to millimeters before save. Reopen and assert both geometry and `$INSUNITS`.

## PROVEN
- Unitless DXF can roundtrip numeric geometry without conveying mm authority.
- Explicit millimeter units persist through ezdxf save/reopen as `$INSUNITS=4`.
- Geometry remains 120 × 60 and closed after repair.

## NOT PROVEN
Supplier/CAD import scaling behavior; paper/model-space plotting scale; tolerance/GD&T correctness; engineering/manufacturing approval.

## TRANSFER BOUNDARY
Use for DXF exchange preflight whenever dimensions matter. It does not replace supplier-specific import tests, field measurement, engineering signoff, tolerance validation, or production approval.

## MATURITY
PRACTICE_EVIDENCE. Next missing evidence: materially different CAD consumer/import roundtrip or project usage with authoritative dimensions.
