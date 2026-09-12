# OLEANDER VALIDATION Practice — IDS zero-applicability boundary

Mode: TRAINING_MODE
Status: PRACTICE_EVIDENCE / NO PROMOTION

## Gap
A machine-readable requirement can be syntactically readable yet match zero objects in the tested IFC. A green or empty result must not be promoted without coverage evidence.

## Current source
- buildingSMART IDS 1.0 Final Standard, released June 2024.
- buildingSMART IDS v1.0.0 release commit: 1effec6f419798ce09617416d258a35bdc58320a.
- Official v1.0.0 XSD blob inspected: edab179d836d0c3e9b21d93c5e2b29f86ec56885.
- Existing OLEANDER owner: oleander-delivery-qc / IDS_BCF_OPENBIM_VALIDATION_EXTENSION.md.

## Capability probe
IfcOpenShell / IfcTester were not present in the runtime. A pip install attempt was blocked by runtime DNS/network resolution. Therefore no claim of IfcTester or buildingSMART IDS Audit conformance is made.

## Artifact
The same IFC4 training fixture contains one IFCDOOR and no IFCWALL.
- A_zero_applicable.ids targets IFCWALL.
- B_one_applicable.ids targets IFCDOOR.
Both are reopened from disk with Python XML parsing. The IFC is reopened as STEP text and inventoried by explicit entity token. This inventory is a bounded probe, not a full IFC semantic validator.

## Readback
- A applicable_count = 0
- B applicable_count = 1
- Exact hashes and environment boundaries are in readback.json.

## PROVEN
Within this bounded fixture, a rule target can be read successfully while the tested IFC population contains zero matching entity records. Therefore coverage/applicability must be checked independently from mere file readability.

## NOT PROVEN / HOLD
- IDS 1.0 XSD validity of the fixtures
- IfcTester/buildingSMART IDS Audit result
- complete IDS requirement evaluation
- full IFC semantic correctness
- project requirement coverage
- universal validator behavior

Verdict: PROVEN_BOUNDED_ZERO_APPLICABILITY_DETECTION__HOLD_IDS_VALIDATOR_CONFORMANCE

Transfer boundary: use this evidence only to justify a fail-closed coverage gate. Do not promote it to an IDS conformance rule until an authoritative validator is actually run on positive and zero-applicability fixtures.
