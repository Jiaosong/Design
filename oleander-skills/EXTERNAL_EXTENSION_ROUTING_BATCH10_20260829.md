# External Extension Routing — Batch 10 — 2026-08-29

Status: `CANDIDATE ROUTING / NO NEW CORE SKILL / NO PROMOTION`

Topic: `OpenBIM / IFC / IDS / BCF / Information Requirements`

## Owner routing

| Capability | Existing Current owner | Candidate extension | Why not a new Skill |
|---|---|---|---|
| information need → explicit requirement → delivery/acceptance contract | `oleander-design-process` | `INFORMATION_REQUIREMENT_EXCHANGE_CONTRACT_EXTENSION.md` | Design Process already owns Need/Goal/Requirement distinctions, requirement/evidence maps, specialist validation handoff and change propagation. The residual gap is openBIM information-delivery traceability, not a separate process owner. |
| native model → IFC semantic exchange → downstream reopen | `oleander-3d-pipeline` | `IFC_SEMANTIC_EXCHANGE_HANDOFF_EXTENSION.md` | 3D Pipeline already owns editable source, units/axes/origin, cross-tool exchange, geometry fidelity and reopen. IFC adds semantic fidelity and schema/view-specific exchange, not a new geometry owner. |
| IDS scoped validation + BCF issue closure evidence | `oleander-delivery-qc` | `IDS_BCF_OPENBIM_VALIDATION_EXTENSION.md` | Delivery QC already owns release gates, 3D exchange checks and package/sign-off boundaries. IDS/BCF add scoped machine validation and coordination closure evidence. |
| normative/contract source interpretation | `oleander-research` | use existing owner | Source authority remains upstream; no new extension required for this batch. |
| bSDD semantic definitions | cross-reference layer under Design Process / 3D / QC | embedded bounded rules | bSDD is a service/dictionary reference, not a project requirement or delivery process owner. |

## Required combined flow

`SOURCE AUTHORITY → INFORMATION NEED / DECISION PURPOSE → REQUIREMENT ID + RESPONSIBILITY / MILESTONE / ACCEPTANCE → MACHINE-CHECKABLE SUBSET + NON-MACHINE RESIDUE → NATIVE MODEL → IFC SCHEMA / VIEW / EXPORT CONFIG → GEOMETRY + SEMANTIC REOPEN / DIFF → IDS COVERAGE + RESULT → BCF ISSUE IF REQUIRED → UPDATED MODEL REVISION → REVALIDATION → ACCEPT / REVISE / HOLD`.

## Core separations

- `IFC EXISTS ≠ OPENBIM DELIVERY PASS`
- `NATIVE MODEL ≠ IFC EXCHANGE MODEL ≠ DOWNSTREAM IMPORTED MODEL`
- `GEOMETRY FIDELITY ≠ SEMANTIC FIDELITY`
- `SOURCE REQUIREMENT ≠ IDS TRANSLATION`
- `IDS PASS ≠ ALL REQUIREMENTS / DESIGN / ENGINEERING / ISO COMPLIANCE`
- `BCF STATUS CLOSED ≠ UNDERLYING CONDITION VERIFIED`
- `bSDD DEFINITION ≠ PROJECT REQUIREMENT`
- `AUTOMATED VALIDATION ≠ ACCEPTANCE AUTHORITY`

## Source transfer

### External Skill
`jeffersonbim/Information-Manager-IFC-skill`
- inspected SHA: `daefa9273607f8614a72bfcdfb51ef64c9c6cb1c`
- license: MIT
- accepted: requirement→IDS trace, schema-specific mapping, exported IFC evidence, IDS coverage discipline, IDS→BCF trace, revalidation before closure, human approval boundary;
- rejected: OpenClaw topology, Revit-specific rules, Docker/LGPD architecture, Notion-only RAG, fixed scripts/templates/runtime versions.

### Professional sources
- buildingSMART IFC 4.3 documentation;
- buildingSMART IDS 1.0;
- buildingSMART BCF 3.0 / BCF technical docs;
- buildingSMART bSDD;
- UK BIM Framework information-requirement / ISO 19650 guidance.

These sources carry professional semantics; source-specific examples, version-dependent implementation behavior and jurisdiction-specific templates are not universal defaults.

## Anti-duplication rule

Do **not** create:
- `oleander-bim`;
- `oleander-openbim`;
- `oleander-ifc`;
- `oleander-ids`;
- `oleander-bcf`;
- `oleander-information-manager`;
- a second generic requirements or coordination Skill.

Create a new owner only if a future verified gap cannot be responsibly owned by Design Process, 3D Pipeline, Delivery QC and Research together.

## Maturity

All three extensions remain:

`CANDIDATE / SUPPORT / DOCUMENTED / NO PRACTICE / NO PROJECT USAGE / NO PROMOTION`.

A future maturity step should use a deliberately small IFC fixture with:
- at least one source requirement that becomes IDS-checkable;
- at least one non-machine-checkable residue;
- one intentional semantic export defect invisible in geometry;
- one IDS failure linked to a BCF issue;
- one corrected IFC revision;
- a rerun proving or rejecting closure.