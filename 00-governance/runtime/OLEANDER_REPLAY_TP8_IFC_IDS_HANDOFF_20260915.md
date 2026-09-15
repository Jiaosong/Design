# OLEANDER TP8 Cross-Software Handoff Replay — IFC / MVD / IDS / Validation Service — 2026-09-15

Status: **DRAFT EXTERNAL REPLAY / NOT CURRENT / SOURCE-BOUNDED**.

Purpose: stress-test P8 `Work / Artifact / Information Carrier / Handoff` using the public buildingSMART openBIM stack.

This replay distinguishes:

- native authoring source;
- exchange derivative;
- format/schema validity;
- workflow-specific exchange requirements;
- project-specific information requirements;
- receiving-tool task fitness;
- round-trip/editability expectations;
- project/source authority.

It does **not** claim that every IFC exchange must preserve native authoring semantics or that IFC is defective when a reference exchange intentionally omits them.

---

## 1. External source facts

Public buildingSMART material establishes:

1. IFC is an open international standard for BIM data exchanged/shared among software applications and disciplines.
2. A Model View Definition (MVD) is a subset of the schema satisfying particular exchange/data requirements and may impose additional constraints.
3. IFC Reference View is intended mainly for reference exchange and is explicitly not a full exchange of design intent.
4. The buildingSMART IFC Validation Service checks STEP syntax, IFC schema and normative IFC rules; it also reports non-normative industry-practice warnings.
5. The IFC Validation Service explicitly does **not** check project-specific, national-specific or organization-specific rules/constraints.
6. IDS defines computer-interpretable information requirements and supports automated checking of IFC models against those requirements.
7. buildingSMART's IDS example shows per-object outcomes such as objects passing, missing a required property, or carrying a non-allowed value.

Source boundary:

- the above are public buildingSMART facts;
- the P8 layer model below is an OLEANDER analytical mapping;
- no specific authoring application's import/export quality is inferred unless separately tested.

---

# 2. “The file opens” is only one layer

A receiving application opening an IFC file establishes, at most, a bounded transport/import fact.

It does not establish all of:

```text
file integrity
schema validity
normative IFC compliance
project information requirement compliance
consumer task fitness
native authoring editability
round-trip equivalence
source/project authority
```

### Replay rule

`P8/HAND-RP08 FILE_OPEN_OR_IMPORT_SUCCESS_IS_NOT_HANDOFF_PASS; HANDOFF_PASS_REQUIRES_THE_DECLARED_EXCHANGE_PURPOSE_AND_REQUIRED_INFORMATION_DIMENSIONS_TO_BE_READ_BACK`.

---

# 3. Add explicit handoff validation layers

The external stack exposes several distinct validation layers.

Recommended P8 layer vocabulary:

```text
L0_PACKAGE_INTEGRITY
L1_FORMAT_SYNTAX
L2_SCHEMA_NORMATIVE_CONFORMANCE
L3_EXCHANGE_VIEW_OR_MVD_CONFORMANCE
L4_PROJECT_INFORMATION_REQUIREMENT_CONFORMANCE
L5_CONSUMER_TASK_READBACK
L6_ROUNDTRIP_OR_EDITABILITY_EQUIVALENCE
L7_SOURCE_AUTHORITY_CONTINUITY
```

Not every handoff requires all layers.

Example:

- a Reference View coordination model may require L0–L5 but explicitly not L6;
- an editable-master transfer may require L6 and stricter semantic preservation;
- all exchanges still need L7 truth about where change authority remains.

### Replay rule

`P8/HAND-RP09 HANDOFF_VALIDATION_IS_LAYERED_AND_ROLE_SCOPED; PASS_AT_FORMAT_SCHEMA_LAYER_CANNOT_AUTO_GRANT_PROJECT_INFORMATION_TASK_ROUNDTRIP_OR_AUTHORITY_LAYERS`.

---

# 4. Exchange purpose determines permissible loss

IFC Reference View being suitable for mainly one-directional reference use confirms an important P8 principle:

`loss` is not automatically `failure`.

Loss of:

- native parametric construction history;
- authoring-tool-specific constraints;
- editing affordances;

may be acceptable for a declared reference/coordination derivative if the required geometry/properties/relations are preserved.

The same loss can be authority-breaking when the requested deliverable is an editable design master.

### Replay rule

`P8/LOSS-RP04 THE_SAME_INFORMATION_LOSS_MAY_BE_ACCEPTABLE_OR_AUTHORITY_BREAKING_DEPENDING_ON_CARRIER_ROLE_CONSUMER_PURPOSE_AND_EXCHANGE_REQUIREMENT`.

This prevents both extremes:

- “any loss means HOLD”;
- “the file opened, therefore no material loss.”

---

# 5. Native editable master and exchange derivative are different responsibilities

Preferred chain:

```text
NATIVE SOURCE / EDITABLE MASTER
        ↓ controlled export
EXCHANGE DERIVATIVE (IFC)
        ↓ format/schema/MVD/IDS checks
CONSUMER IMPORT
        ↓ consumer task readback
DOWNSTREAM USE
```

The exchange derivative may be a valid delivery carrier without becoming the source editable master.

### Replay rule

`P8/ROLE-RP03 VALID_EXCHANGE_DERIVATIVE_MAY_BE_AUTHORITATIVE_FOR_DECLARED_DELIVERY_CONTENT_WITHOUT_REPLACING_THE_NATIVE_SOURCE_MASTER_OR_EDITABLE_MASTER_ROLE`.

---

# 6. Format conformance and project information conformance are different

An IFC file may conform to IFC syntax/schema/normative rules while still missing a project-required property.

The buildingSMART separation between Validation Service and IDS directly proves this distinction.

### Replay rule

`P8/HAND-RP10 FORMAT_SCHEMA_CONFORMANCE_AND_PROJECT_INFORMATION_REQUIREMENT_CONFORMANCE_ARE_INDEPENDENT_RESULTS_AND_MUST_NOT_BE_COLLAPSED`.

Recommended receipt:

```yaml
format_conformance:
exchange_view_conformance:
information_requirement_conformance:
consumer_task_readback:
roundtrip_equivalence:
source_authority_continuity:
```

---

# 7. Per-object / per-information-class results must be preserved

IDS examples demonstrate that one exchange can contain a mixture:

- some objects satisfy a requirement;
- some omit the property;
- some provide a disallowed value.

Therefore a package-level result cannot replace per-target results where failures are material.

### Replay rule

`P8/HAND-RP11 EXCHANGE_REQUIREMENT_CHECKS_MUST_PRESERVE_PER_OBJECT_OR_PER_INFORMATION_CLASS_FAILURES_WHEN_MATERIAL; GLOBAL_PASS_FAIL_SUMMARY_REQUIRES_EXPLICIT_AGGREGATION`.

This parallels P6 multi-target Assurance but remains a P8 handoff/readback concern.

---

# 8. MVD / exchange requirement is a contract boundary

Because an MVD serves particular exchange requirements, P8 should not ask:

`Did the IFC preserve everything?`

It should ask:

`Did the exchange preserve what this declared workflow requires?`

Minimum exchange contract should include:

```yaml
exchange_requirement_id:
workflow_or_consumer_task:
required_view_or_profile:
required_information_classes:
required_semantic_relations:
required_geometry_representation:
required_units_coordinate_context:
permitted_loss:
prohibited_loss:
consumer_readback:
```

### Replay rule

`P8/HAND-RP12 CROSS_SOFTWARE_FIDELITY_MUST_BE_EVALUATED_AGAINST_DECLARED_EXCHANGE_REQUIREMENTS_NOT_AN_UNBOUNDED_EXPECTATION_OF_TOTAL_NATIVE_MODEL_EQUIVALENCE`.

---

# 9. Unknown loss requires targeted investigation, not global HOLD

Suppose the receiving tool imports geometry, but it is unknown whether a required property relation survived.

P8 disposition depends on whether that unknown intersects the declared task.

```text
unknown required property → HOLD / REVISE for that handoff scope
unknown native authoring feature outside reference-exchange claim → OUTSIDE_CLAIM / record only
```

### Replay rule

`P8/LOSS-RP05 UNKNOWN_INFORMATION_LOSS_BLOCKS_ONLY_THE_HANDOFF_SCOPE_THAT_DEPENDS_ON_THE_UNKNOWN_DIMENSION; DO_NOT_GLOBALIZE_HOLD_WHEN_THE_DIMENSION_IS_OUTSIDE_DECLARED_EXCHANGE_PURPOSE`.

---

# 10. Consumer task readback is separate from producer export success

Producer-side checks can prove:

- exported file exists;
- schema is valid;
- IDS requirements pass.

They cannot prove the receiving workflow actually works in the target application/environment.

Consumer readback should verify task-relevant outcomes such as:

- expected object population is present;
- units/coordinates are correct;
- protected geometry/dimensions are preserved;
- required properties/relations are queryable;
- intended downstream analysis/coordination task can proceed.

### Replay rule

`P8/HAND-RP13 PRODUCER_EXPORT_VALIDATION_CANNOT_SUBSTITUTE_FOR_CONSUMER_TASK_READBACK_WHEN_DOWNSTREAM_TOOL_BEHAVIOR_OR_INTERPRETATION_IS_MATERIAL`.

---

# 11. Round-trip is a separate requirement, not a default expectation

A Reference View can be entirely successful without supporting full editable round-trip.

Therefore P8 should require round-trip testing only when the declared handoff role requires downstream editing/re-authoring and return.

### Replay rule

`P8/RTRIP-RP02 ROUNDTRIP_EQUIVALENCE_IS_CONDITIONALLY_REQUIRED_BY_HANDOFF_ROLE; REFERENCE_ONLY_OR_ONE_DIRECTIONAL_EXCHANGE_MUST_NOT_FAIL_SOLELY_FOR_NOT_PRESERVING_UNCLAIMED_NATIVE_AUTHORING_SEMANTICS`.

Conversely:

`editable-master handoff` cannot cite Reference View success as proof of native/editable equivalence.

---

# 12. Authority does not follow edit capability

A downstream tool may be able to edit imported geometry or properties.

That capability does not establish project change authority.

### Replay rule

`P8/AUTH-RP03 TECHNICAL_EDITABILITY_OR_IMPORT_CAPABILITY_DOES_NOT_TRANSFER_DEFINITION_OWNER_CHANGE_AUTHORITY_OR_SOURCE_MASTER_STATUS`.

This reinforces the Project/Artifact distinction.

---

# 13. Add exchange loss observation state

Existing P8 loss types/severity need an orthogonal observation state:

```text
EXPECTED_AND_PERMITTED
EXPECTED_BUT_PROHIBITED
OBSERVED
NOT_OBSERVED
UNKNOWN_NOT_TESTED
NOT_APPLICABLE
```

Why:

- `PARAMETRIC_LOSS` may be known/allowed for Reference View;
- `SEMANTIC_PROPERTY_LOSS` may be observed and material;
- `INTERACTION_STATE_LOSS` may be irrelevant to an IFC coordination handoff;
- an untested dimension should not be marked NONE.

### Replay rule

`P8/LOSS-RP06 LOSS_TYPE_SEVERITY_AND_OBSERVATION_STATE_ARE_ORTHOGONAL; NOT_TESTED_MUST_NOT_BE_RECORDED_AS_NO_LOSS`.

---

# 14. Artifact count remains independent from semantic object count

A handoff package can contain:

- native model;
- IFC exchange file;
- IDS specification;
- validation report;
- screenshots/readback receipt.

These are multiple carriers/receipts around one handoff responsibility, not necessarily five independent Project truths.

This confirms `P8/ART-RP01` from KH46.

---

# 15. Required P8 machine refinements

Add:

1. `handoff_validation_layer`;
2. layer-specific result vector;
3. `loss_observation_state`;
4. explicit exchange view/profile requirement;
5. consumer task readback result;
6. conditional round-trip requirement;
7. format vs project-information conformance separation.

No new top-level Object Class is required.

---

# 16. Replay-derived rules

- `P8/HAND-RP08`
- `P8/HAND-RP09`
- `P8/LOSS-RP04`
- `P8/ROLE-RP03`
- `P8/HAND-RP10`
- `P8/HAND-RP11`
- `P8/HAND-RP12`
- `P8/LOSS-RP05`
- `P8/HAND-RP13`
- `P8/RTRIP-RP02`
- `P8/AUTH-RP03`
- `P8/LOSS-RP06`

---

# 17. TP8 disposition

`TP8 CROSS-SOFTWARE ARTIFACT / HANDOFF REPLAY = COMPLETE_WITH_DELTAS`.

The replay confirms that P8 should judge a handoff by **role-scoped information preservation and consumer task fitness**, not file extension, openability, byte equality or assumed round-trip fidelity.

No Current promotion is authorized.