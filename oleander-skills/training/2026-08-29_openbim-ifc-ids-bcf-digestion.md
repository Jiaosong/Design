# External Skill Digestion — OpenBIM / IFC / IDS / BCF / Information Requirements

Date: `2026-08-29`

Status: `SOURCE DIGESTED / CANDIDATE EXTENSIONS / NO PROMOTION`

Gap: `GAP-BIM-01 — Information requirement → semantic model exchange → machine validation → issue closure`

## Current-first audit

Current owners reviewed before extension work:

### `oleander-design-process`
Already owns:
- Need vs Goal vs Requirement vs Criterion;
- requirement/evidence/unknown map;
- source/observation → design consequence;
- specialist validation handoff and return loop;
- change propagation and design decision record.

Residual gap:
- requirement authority did not yet remain explicit through IFC/IDS/BCF carriers;
- machine-checkable subset vs non-machine-checkable residue was not explicit;
- information requirement purpose/milestone/responsibility/acceptance contract was not explicit enough for openBIM exchange.

Owner decision: **extend existing owner**, no BIM process Core Skill.

### `oleander-3d-pipeline`
Already owns:
- editable/native model identity;
- units, axes, origin and transforms;
- cross-tool exchange and reopen;
- geometry/source/derivative lineage;
- reality-capture derivative handoff.

Residual gap:
- semantic IFC fidelity (entity, PredefinedType, spatial/system/material/classification/Pset/Qto relations) was not explicit;
- native model vs IFC exchange model vs target imported model authority was not explicit;
- geometry fidelity and semantic fidelity needed separate gates.

Owner decision: **extend existing owner**.

### `oleander-delivery-qc`
Already owns:
- release/package integrity;
- 3D exchange clean-context reopen;
- cross-software handoff audit;
- source vs derivative identity;
- final claim/sign-off boundary.

Residual gap:
- IDS applicability/coverage and machine-check scope;
- `0 applicable` false-green protection;
- IDS failure→BCF issue trace;
- BCF issue state vs verified underlying correction;
- requirement/model revision revalidation before evidence closure.

Owner decision: **extend existing owner**.

### `oleander-research`
Remains source/normative evidence authority where standards, regulations or contractual documents must be interpreted. No new extension in this batch because the material delta is primarily requirement-to-delivery operationalization, not research-source evaluation.

### Technical drawing
Current Design Process still routes to `oleander-technical-drawing`, but no separate `oleander-skills/oleander-technical-drawing` directory was present in the current `oleander-skills` main listing inspected for this batch. This batch therefore does not create or modify a speculative technical-drawing owner. Drawing consumption of IFC-derived data remains downstream of governed source/geometry/information authority.

## External Skill source

Repository: `jeffersonbim/Information-Manager-IFC-skill`

Pinned inspected main SHA: `daefa9273607f8614a72bfcdfb51ef64c9c6cb1c`

License: **MIT** (`LICENSE`, copyright 2026 jeffersonbim).

Inspected:
- root `SKILL.md`;
- `references/ids.md`;
- `references/bcf.md`;
- repository structure and routed domains disclosed in the Skill.

The source is materially stronger than generic BIM-agent lists because it separates IFC mapping, IDS, bSDD, BCF, ISO 19650 and deterministic exported-model verification. It is nevertheless a source-specific Information Manager workflow, not an OLEANDER architecture to install wholesale.

## Accepted Material Delta from external Skill

Independently reformulated and transferred:

1. **Requirement source before IDS**
   - IDS operationalizes approved information requirements; machine rules do not silently become requirement authority.
   - Preserve source requirement, responsibility/milestone and acceptance context.

2. **Schema-specific semantics**
   - IFC mapping must be evaluated against the requested schema/version and the exported IFC, not assumed from authoring category/parameter labels.

3. **IFC destination distinctions**
   - Attribute, property set/property, quantity set/quantity, classification/material/relation semantics remain distinct.

4. **Deterministic export evidence before interpretation**
   - Inspect actual IFC output and explicit mapping/relations rather than infer successful exchange from authoring configuration.

5. **IDS coverage discipline**
   - A rule matching no objects cannot silently produce meaningful success when coverage was expected.
   - Runtime/version evidence matters where implementation behavior is material.

6. **IDS → BCF traceability**
   - When machine validation creates an issue, retain requirement/specification and original validation result identity.

7. **BCF closure through updated-model evidence**
   - Resubmission/status change is not enough; verify the acceptance condition on the updated model/revision.

8. **Human approval boundary**
   - automated model/requirement checks do not by themselves authorize contractual, professional or model-changing actions.

## Rejected / not transferred from external Skill

Not installed as OLEANDER defaults:
- OpenClaw orchestration or permanent agent topology;
- Revit-specific category/export recipes or `IfcExportAs` house rules;
- Docker isolation architecture;
- LGPD-specific intake as universal privacy architecture;
- Notion as the mandatory sole OpenBIM RAG/catalog;
- fixed gate questionnaire;
- source templates/spreadsheets/output JSON contract;
- fixed IfcOpenShell/IfcTester version such as `0.8.5`;
- source scripts (`privacy_ingest.py`, validators, template intake, parameter mappings, installers, smoke runtime);
- fixed paths/mounting conventions;
- author-specific parameter planning tables;
- one corporate runtime/security topology.

These are implementation/context choices, not transferable design/information-management invariants.

`EXTERNAL REFERENCE LEARNED ≠ EXTERNAL SKILL INSTALLED`.

## Primary professional sources

### buildingSMART IFC
Sources:
- `https://ifc43-docs.standards.buildingsmart.org/`
- `https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/`

Retained:
- IFC as open BIM data schema/exchange structure;
- implementation is schema/version/view specific;
- MVD/exchange scope can matter;
- semantic entities, attributes, relations, Psets/Qtos and reference data are part of fidelity, not just visible geometry.

Rejected as universal:
- one schema/version/MVD;
- one exporter or one model-authoring tool;
- IFC existence as delivery/conformance proof.

### buildingSMART IDS 1.0
Sources:
- `https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/`
- `https://technical.buildingsmart.org/projects/information-delivery-specification-ids/`
- `https://github.com/buildingSMART/IDS`

Retained:
- official IDS 1.0 as computer-interpretable information requirement standard;
- applicability + required information/value semantics;
- automated checking is scoped to what the IDS expresses and what the runtime evaluates.

Rejected as universal:
- one validator implementation/result schema;
- IDS as requirement authority without source lineage;
- IDS PASS as full model/design/ISO compliance.

### buildingSMART BCF
Sources:
- `https://technical.buildingsmart.org/standards/bcf/`
- `https://github.com/buildingSMART/BCF-XML`
- `https://github.com/buildingSMART/BCF-API`

Retained:
- issue coordination through file exchange or API;
- topic/component/viewpoint/comment context;
- issue history and round-trip coordination.

Rejected as universal:
- one status/priority taxonomy;
- one escalation flow;
- Closed status as proof of corrected model state.

### buildingSMART bSDD
Sources:
- `https://www.buildingsmart.org/users/services/buildingsmart-data-dictionary/`
- `https://technical.buildingsmart.org/services/bsdd/data-structure/`

Retained:
- dictionary/class/property definitions and identifiers can stabilize semantics;
- dictionary owner/version/status matters.

Rejected as universal:
- bSDD content as automatic project requirement;
- valid URI as correct delivered value;
- one dictionary as sole semantic authority.

### UK BIM Framework / ISO 19650 guidance
Sources:
- UK BIM Framework Guidance Part D — Developing information requirements, Edition 2 (2021);
- UK BIM Framework standards/resources pages.

Retained:
- information needs/requirements should precede and govern delivery;
- lifecycle/decision purpose matters;
- requested information should be sufficient for the purpose rather than accumulated without need.

Rejected as universal:
- UK-specific acronym/document stack as mandatory for every OLEANDER project;
- one BEP/TIDP/MIDP/CDE naming/status convention;
- named documents as proof of ISO 19650 conformity.

## Resulting candidate extensions

1. `oleander-skills/oleander-design-process/INFORMATION_REQUIREMENT_EXCHANGE_CONTRACT_EXTENSION.md`
2. `oleander-skills/oleander-3d-pipeline/IFC_SEMANTIC_EXCHANGE_HANDOFF_EXTENSION.md`
3. `oleander-skills/oleander-delivery-qc/IDS_BCF_OPENBIM_VALIDATION_EXTENSION.md`

No `oleander-bim`, `oleander-openbim`, `oleander-ifc`, `oleander-information-manager` or other parallel Core Skill was created.

## Combined flow

`INFORMATION NEED / DECISION → SOURCE REQUIREMENT → REQUIREMENT LEDGER → MACHINE-CHECKABLE SUBSET + HUMAN/PROFESSIONAL RESIDUE → NATIVE MODEL → IFC SCHEMA/VIEW EXPORT → GEOMETRY + SEMANTIC REOPEN/DIFF → IDS COVERAGE + RESULT → BCF ISSUE WHEN NEEDED → UPDATED MODEL REVISION → SAME/AUTHORIZED UPDATED REQUIREMENT RECHECK → ACCEPTANCE / HOLD`.

## Critical separations

- `IFC EXISTS ≠ OPENBIM DELIVERY PASS`
- `NATIVE MODEL ≠ IFC EXCHANGE MODEL ≠ DOWNSTREAM IMPORT`
- `GEOMETRY FIDELITY ≠ SEMANTIC FIDELITY`
- `MACHINE TRANSLATION ≠ SOURCE REQUIREMENT`
- `IDS PASS ≠ ALL INFORMATION REQUIREMENTS SATISFIED`
- `0 APPLICABLE ≠ MEANINGFUL PASS WHEN COVERAGE WAS EXPECTED`
- `BCF CLOSED ≠ CORRECTION VERIFIED`
- `bSDD REFERENCE ≠ PROJECT REQUIREMENT / CORRECT VALUE`
- `OPENBIM TECHNICAL CHECK ≠ DESIGN QUALITY / ENGINEERING / CONTRACT / ISO SIGNOFF`

## Planned adversarial eval specs

- `SK-DES-014` — source requirement is partially translated to IDS; machine-checkable subset passes while non-machine-checkable residue disappears.
- `SK-3D-007` — IFC visually reopens correctly while class/Pset/relations/units or identity semantics drift.
- `SK-QC-004` — IDS failure becomes BCF issue marked Closed after file resubmission without rerunning the affected requirement on the updated model.

Central Golden integration remains separate unless safely executed against `evals/golden/skills.jsonl`.

## Maturity

`DOCUMENTED CANDIDATE EXTENSIONS / SOURCE DIGESTED / NO PRACTICE / NO CROSS-CONTEXT / NO PROJECT USAGE / NO PROMOTION`.