# OLEANDER 3D Receipt Validator

`validate_receipt.py` is the fail-closed execution check for the 15-section `oleander-3d-pipeline` receipt contract.

It validates **structured execution evidence only**. A validator PASS does not authorize `Design KEEP`, `MAIN KEEP`, `G2/G3/Class-A`, field verification, engineering validity, manufacturing readiness or physical CMF truth.

## Canonical inputs

- schema: `../contracts/BLENDER_3D_RECEIPT_SCHEMAS_v1.json`
- templates: `../contracts/BLENDER_3D_RECEIPT_TEMPLATES_v1.json`
- authority/diagnostic contract: `../contracts/BLENDER_3D_AUTHORITY_DIAGNOSTIC_CONTRACT_v1.json`

## CLI

```bash
python3 oleander-skills/oleander-3d-pipeline/tools/validate_receipt.py \
  --section 05_surface_diagnostics \
  --input path/to/DIAGNOSTIC_MATRIX.json
```

Exit codes:

- `0`: structurally valid for that section;
- `2`: fail-closed contract violation, malformed JSON or unreadable file.

The CLI prints a JSON result to stdout.

## Required envelope

Every receipt must include the schema-level common fields, including project/asset/task identity, timestamp, producer, source revision, status and `does_not_prove`.

Section-specific fields are then validated from `BLENDER_3D_RECEIPT_SCHEMAS_v1.json`.

## Section-specific hard checks currently enforced

### 03 Blender Source Authority

A `PASS` is rejected unless:

- `source_unchanged == true`;
- material slots were preserved;
- Source before/after SHA-256 values match;
- diagnostic proxy role is `DERIVED_DIAGNOSTIC_NOT_AUTHORITY`;
- the proxy is not authoritative.

### 05 Surface Diagnostics

A receipt is rejected unless it contains exactly one each of:

- `BROAD`
- `STRIP`
- `GRAZING`
- `ZEBRA`

All four rows must bind the same Source digest. This prevents mixed-revision evidence from being presented as one controlled comparison.

### 13 Review Gates

When MAIN promotion is requested without independent review:

- Design Quality must remain `HOLD`;
- final promotion state may not be `KEEP`, `MAIN_KEEP`, `PROMOTED`, `APPROVED` or `PASS`.

Machine or evidence success cannot self-promote the asset.

### 15 Completion

`COMPLETE_TO_REQUESTED_SCOPE` is rejected when:

- authority boundaries are not intact; or
- residual blockers remain.

Use `PARTIAL` / `HOLD` / `FAIL` instead of widening a narrower truth.

## Templates

`BLENDER_3D_RECEIPT_TEMPLATES_v1.json` contains one minimal structurally valid placeholder receipt for every numbered Skill section. They are test fixtures and starting structures, not project evidence.

The CI regression `test_oleander_3d_pipeline_receipt_validator.py` validates all 15 templates and also proves that critical false-PASS states are rejected.
