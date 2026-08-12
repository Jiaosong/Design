# Practice

`06-practice/` is the **current-authority Practice root** for OLEANDER／织作.

Daily practice uses Scope `PRAC` and must reference the canonical Governance v1.1.0 before creating new assets or files.

Namespace boundary:
- `P0–P4` are reserved for the project axis only.
- `B01–B04 / CU01–CU04 / IP01–IP04 / SP01–SP04` are Application Mapping / knowledge-location codes, not Project IDs and not priority labels.
- Priority uses `Priority-0…Priority-3` where a delivery priority is required.
- Historical identifiers and historical artifact filenames remain provenance only and are not rewritten.

The older top-level [`../practice/`](../practice/) path is a **Legacy artifact location**, not a second Practice authority. Existing evidence there remains traceable in place; new current Practice records must enter through `06-practice/` or an explicitly indexed legacy-location pointer.

## Mandatory Post-Generation Review

Every practice output must follow this closure:

`Generate → Automated QA → Open final artifact → Post-Generation Review → Fix → Re-review → Archive`

Status must be written explicitly as `REVIEW PENDING`, `POST-REVIEW FAIL / NEEDS REVISION`, or `POST-REVIEW PASS`.

No practice artifact may be marked DONE / PASS / Candidate before `POST-REVIEW PASS`. Automated QA, script success, file export, bbox checks, or reproducibility are necessary but not sufficient.

Canonical governance: [`../00-governance/README.md`](../00-governance/README.md)  
Canonical review gate: [`../00-governance/post-generation-review-gate.md`](../00-governance/post-generation-review-gate.md)
