# OLEANDER 3D Receipt Validator

`validate_receipt.py` is the fail-closed execution check for all 15 numbered sections of `oleander-3d-pipeline`.

It validates **structured execution evidence only**. Validator PASS does not authorize `Design KEEP`, `MAIN KEEP`, `G2/G3/Class-A`, field verification, engineering validity, manufacturing readiness or physical CMF truth.

## Canonical inputs

- schema: `../contracts/BLENDER_3D_RECEIPT_SCHEMAS_v1.json`
- templates: `../contracts/BLENDER_3D_RECEIPT_TEMPLATES_v1.json`
- authority/diagnostic contract: `../contracts/BLENDER_3D_AUTHORITY_DIAGNOSTIC_CONTRACT_v1.json`

The validator carries an explicit `SECTION_KEYS_WITH_SPECIFIC_RULES` set. Validation fails if that set and the schema's 15 sections ever diverge, so a newly added section cannot silently fall back to field-presence-only validation.

## CLI

```bash
python3 oleander-skills/oleander-3d-pipeline/tools/validate_receipt.py \
  --section 05_surface_diagnostics \
  --input path/to/DIAGNOSTIC_MATRIX.json
```

Exit codes:

- `0`: structurally and section-semantically valid for that execution receipt;
- `2`: fail-closed contract violation, malformed JSON or unreadable file.

The CLI prints JSON to stdout.

## Required envelope

Every receipt must carry the schema-level identity envelope: project, asset, task, timestamp, producer, source revision, status and `does_not_prove`.

Section-specific required fields and enums then come from `BLENDER_3D_RECEIPT_SCHEMAS_v1.json`. Presence alone is insufficient: the validator applies the semantic guards below.

## 01 Authority

A `PASS` requires:

- ordered `MASTER_PROTOCOL → PROJECT_STATE → SOURCE_AUTHORITY → CURRENT_TASK` authority prefix;
- positive real-world scale;
- explicit boolean Source-mutation authorization;
- non-empty Source identity, authoring application/version, units and coordinate convention.

An unresolved authority state must remain HOLD rather than writing through to an uncertain Source.

## 02 State classification

The object/file table rejects:

- duplicate identities;
- non-boolean edit/mutation flags;
- derived objects without a declared regeneration source;
- reference evidence marked mutable in the current task.

State classification remains separate from quality or promotion.

## 03 Blender Source Authority

A `PASS` is rejected unless:

- before/after Source SHA-256 values are valid and identical;
- `source_unchanged == true`;
- material slots were preserved;
- the expected Source object set exists;
- diagnostic proxy role is exactly `DERIVED_DIAGNOSTIC_NOT_AUTHORITY`;
- the proxy is not authoritative.

## 04 Sparse Source edit

An edit receipt requires:

- ordered numeric `[min, max]` allowed range;
- new value inside that range;
- rollback value equal to the previous value;
- before and after evidence;
- a non-no-op delta when status is PASS.

This prevents dense or arbitrary point pushing from being disguised as a controlled Source relation edit.

## 05 Surface diagnostics

A diagnostic matrix requires exactly one each of:

- `BROAD`
- `STRIP`
- `GRAZING`
- `ZEBRA`

All four rows must bind the same valid Source digest. Each row requires reference/candidate assets plus camera, rig, material, color-management, render-settings and crop identities. Reference and candidate cannot be the same file.

This prevents mixed-revision or uncontrolled evidence from being presented as one comparison. Zebra remains diagnostic evidence, not Class-A certification.

## 06 Geometry / topology

A `PASS` requires all relevant Source-structure, topology, normals, manifoldness, boundary drift, units, bounds and UV/material-ID checks to be `PASS` or explicitly not applicable.

It also requires `source_form_quality_not_inferred == true` and no retained failure codes. Clean topology therefore cannot self-promote into good form.

## 07 Spatial / architectural / landscape evidence

The spatial ledger rejects:

- duplicate geometry IDs;
- `FIELD_MEASURED` rows without measured/verified field status;
- inferred, assumed, proposal or entourage rows falsely marked field measured/verified;
- malformed numeric ranges;
- recommended numeric values outside their declared ranges.

FIELD-open work can continue, but evidence class cannot be silently promoted.

## 08 Materials / CMF

Controlled CMF comparison requires the same geometry/camera/rig across candidates.

The validator rejects:

- invalid geometry digests;
- microdetail used to mask or repair geometry;
- failed macro-form masking checks;
- `MANUFACTURER_SPEC`, `MEASURED_PHYSICAL_FINISH` or `PRODUCTION_CMF_DECISION` claims without physical evidence.

Shader appearance remains distinct from physical CMF truth.

## 09 Camera / render controls

A `PASS` requires:

- `drift_detected == false`;
- positive sample count;
- explicit camera/projection/crop, color-management, world, light, material and comparison-variable identities.

Controlled comparison cannot change hidden rig variables while attributing the result to geometry or CMF.

## 10 Technical / exploded outputs

A `PASS` requires:

- editable vector/technical master (`SVG`, `AI`, `PDF`, `DXF` or `DWG`);
- separate preview asset;
- vector text confirmation;
- assembly groups and connection logic;
- dimension-status legend;
- structured explosion-offset record.

A decorative raster-only exploded image is not accepted as the editable technical deliverable.

## 11 Exchange / round-trip

A `PASS` requires:

- valid Source/export SHA-256 values;
- Source Authority unchanged;
- units, bounds, axis, origin, hierarchy, instances, normals, materials/textures, applicable camera/animation and critical-name checks to PASS or be explicitly N/A;
- no undeclared topology/geometry drift.

An export never becomes Source merely because round-trip succeeds.

## 12 Production assets

The manifest rejects:

- duplicate paths;
- zero/negative byte assets;
- invalid SHA-256 values;
- unknown authority state classes;
- CURRENT assets without validation PASS;
- CURRENT assets declared missing, unrecoverable or not tested.

Recoverability and traceability remain independent from Design Quality.

## 13 Review gates

The validator separates Machine, Evidence and Design Quality.

It rejects:

- `Design KEEP` without independent review;
- an unnamed independent reviewer/system;
- the producer recorded as their own independent reviewer;
- MAIN promotion without independent review;
- promoted final state without an explicit MAIN request;
- promotion without Machine PASS + Evidence PASS + independent Design KEEP.

Build/CI success cannot self-promote the asset.

## 14 Failure routing

A failure-route receipt requires:

- a non-empty controlled-variable set;
- one explicitly changed variable not also listed as controlled;
- an isolation test;
- chosen edit target distinct from rejected edit targets;
- root-cause confidence and next action.

This blocks uncontrolled multi-variable edits being written up as causal diagnosis.

## 15 Completion

`COMPLETE_TO_REQUESTED_SCOPE` is rejected unless:

- authority boundaries remain intact;
- residual blockers are empty;
- Machine and Evidence gates are PASS;
- all explicitly requested deliverables are complete/pass/not-applicable;
- evidence receipts and reopen/machine checks exist.

Design Quality may remain a separately stated HOLD when independent promotion was outside the requested execution scope; completion wording must not widen that narrower truth.

## Templates and regression coverage

`BLENDER_3D_RECEIPT_TEMPLATES_v1.json` contains one minimal structurally valid placeholder receipt for each of the 15 sections. Templates are fixtures and starting structures, not project evidence.

`test_oleander_3d_pipeline_receipt_validator.py` proves both directions:

1. all 15 canonical templates validate;
2. every one of the 15 sections has at least one deliberately corrupted false-PASS example that the validator rejects.

The Blender v1.21 workflow runs these tests, compiles the validator, lints the JSON contracts, executes the Blender-native Source smoke and emits a hash-bound Skill contract receipt.
