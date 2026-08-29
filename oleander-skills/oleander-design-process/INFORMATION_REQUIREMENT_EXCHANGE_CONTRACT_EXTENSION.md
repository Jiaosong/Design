# Information Requirement → Exchange Contract Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-design-process`

Use when a project must translate an organizational, asset, project, appointment, stakeholder, regulatory, operational or design information need into an explicit information-delivery obligation that can survive authoring, IFC/openBIM exchange, validation and coordination.

This extension governs **requirement authority and requirement→delivery traceability**. It does not create a new BIM process, does not make one jurisdiction's ISO 19650 terminology universal OLEANDER vocabulary, and does not replace contract, legal, engineering, information-management or client authority.

## Existing-owner boundary

Use with, not instead of:
- `oleander-design-process/SKILL.md` for Need vs Goal vs Requirement vs Criterion, the requirement/evidence/unknown map, design consequence and validation return loop;
- `oleander-research` for source authority, regulatory/normative evidence and unresolved source conflict;
- `oleander-3d-pipeline/IFC_SEMANTIC_EXCHANGE_HANDOFF_EXTENSION.md` when the requirement is carried through IFC;
- `oleander-delivery-qc/IDS_BCF_OPENBIM_VALIDATION_EXTENSION.md` when requirements become machine-checkable IDS rules or coordination issues;
- project/client/contractual information-management authority where requirements are formally appointed or accepted.

## Core contract

`INFORMATION NEED / DECISION PURPOSE → AUTHORITATIVE REQUIREMENT SOURCE → STABLE REQUIREMENT ID → APPLICABILITY / SUBJECT → REQUIRED INFORMATION / RELATION / GEOMETRY / DOCUMENT / STATE → DEFINITION + UNIT / VALUE / CARDINALITY / REFERENCE WHEN MATERIAL → DELIVERY MILESTONE / EXCHANGE PURPOSE → RESPONSIBLE PRODUCER + ACCEPTANCE OWNER → REQUIRED EVIDENCE / VALIDATION METHOD → MACHINE-CHECKABLE SUBSET WHEN AVAILABLE → DELIVERED EVIDENCE → RESULT / EXCEPTION / HOLD → DESIGN OR INFORMATION-MANAGEMENT CONSEQUENCE`

The requirement must remain traceable to the source and decision purpose after it is translated into an IFC property, IDS rule, spreadsheet, database field, document, BCF issue or other carrier.

`DELIVERY FORMAT ≠ REQUIREMENT AUTHORITY`.

## Requirement classes

Classify material obligations before choosing a technical carrier. Examples:
- object/entity/classification identity;
- property/attribute/quantity/value information;
- material/system/type relation;
- spatial containment or relationship;
- geometry/position/shape/clearance requirement;
- document/reference/evidence requirement;
- provenance/approval/revision requirement;
- operational/maintenance information;
- timing/milestone/exchange requirement;
- security/privacy/access requirement;
- human judgment, professional review or legal acceptance requirement.

A requirement may contain several classes. Split them when their authority, validation method or responsible owner differs.

## Requirement authority states

Keep these states distinct:

1. `SOURCE_REQUIREMENT` — explicit obligation from the authoritative source/appointment/specification.
2. `INTERPRETED_REQUIREMENT` — a reasoned clarification or decomposition of the source; must retain source link and interpretation owner.
3. `MACHINE_TRANSLATION` — requirement encoded in IDS, schema rules, code, database constraints or another executable form.
4. `DELIVERY_EVIDENCE` — the model/file/record submitted as evidence that the requirement is met.
5. `VALIDATION_RESULT` — result of a specific test against a defined requirement and artifact revision.
6. `ACCEPTANCE / DISPOSITION` — authority decision to accept, revise, waive or hold.

`MACHINE_TRANSLATION ≠ SOURCE_REQUIREMENT`.

`VALIDATION PASS ≠ CONTRACTUAL / PROFESSIONAL ACCEPTANCE` unless the governing authority explicitly defines it that way.

## Requirement ledger

For each material requirement persist, as applicable:

- `requirement_id`;
- `source_authority_and_revision`;
- `source_clause_or_location`;
- `information_need_and_decision_purpose`;
- `applicable_actor_object_system_or_population`;
- `required_information_class`;
- `semantic_definition_or_reference`;
- `required_ifc_entity_predefinedtype_classification_pset_property_qto_relation_when_applicable`;
- `datatype_unit_value_range_cardinality_or_enumeration_when_applicable`;
- `geometry_or_document_requirement_when_applicable`;
- `delivery_milestone_and_exchange_purpose`;
- `responsible_producer`;
- `acceptance_owner`;
- `validation_method_and_proof_class`;
- `machine_checkability_state`;
- `ids_or_other_rule_id_when_present`;
- `delivery_artifact_and_revision`;
- `result_exception_waiver_hold`;
- `reopen_trigger`.

Do not infer missing contractual responsibility or acceptance authority from software roles.

## Information-need-first rule

Before asking for a property, model field or document, state what decision or use it supports. The amount of requested information should be sufficient for the purpose without creating unnecessary production burden.

Ask:
- What decision/use fails if this information is absent?
- At what milestone is it needed?
- Who must produce it and who can accept it?
- What definition, unit, classification or reference makes the value unambiguous?
- What is the cheapest valid proof class?
- Is the obligation machine-checkable, partly machine-checkable or human/professional only?

Do not create fields because a template, software exporter or generic BIM checklist happens to contain them.

## Machine-checkable subset

Translate to IDS or another executable rule only what the target standard/runtime can honestly express and validate.

Maintain:

`SOURCE REQUIREMENT → MACHINE-CHECKABLE SUBSET → NON-MACHINE-CHECKABLE RESIDUE → TEST RESULT → HUMAN/PROFESSIONAL ACCEPTANCE WHEN REQUIRED`.

Rules:
1. A partial encoding must declare what was omitted.
2. An executable rule cannot silently narrow the source requirement.
3. Unsupported geometry, calculation, external-document, professional-judgment or workflow conditions remain separate requirements/HOLDs.
4. A successful automated test cannot erase non-machine-checkable residue.
5. If the executable interpretation conflicts with the source requirement, source authority wins until an authorized change is issued.

`IDS PASS ≠ ALL INFORMATION REQUIREMENTS SATISFIED`.

## ISO 19650 transfer boundary

Professional guidance was studied for the principle that information needs and requirements should be defined before delivery and tied to decisions/lifecycle use. OLEANDER may use project-specific terms such as OIR, AIR, PIR or EIR when the actual authority uses them.

Do **not** install as universal OLEANDER truth:
- one jurisdiction's acronym stack;
- one CDE status/suitability naming scheme;
- one appointment/BEP/TIDP/MIDP template;
- one file naming convention;
- one information-level or LOD/LOI shorthand;
- an assumption that ISO 19650 compliance can be proven by having named documents, IFC or IDS files.

Use the underlying invariant instead:

`PURPOSE → REQUIREMENT → RESPONSIBILITY → DELIVERY → REVIEW / ACCEPTANCE → TRACEABLE CHANGE`.

## bSDD / dictionary boundary

A dictionary/class/property URI can stabilize semantic meaning, but it is not automatically the project requirement.

When bSDD or another dictionary is used, record:
- dictionary owner/version/status;
- class/property identifier or URI;
- definition used;
- project mapping/interpretation where needed;
- requirement source that makes the term applicable.

`DEFINED TERM ≠ REQUIRED TERM`.

`bSDD REFERENCE ≠ PROJECT ACCEPTANCE`.

## Change control

When a requirement changes after delivery work has begun:

`AUTHORIZED CHANGE → AFFECTED REQUIREMENT IDS → AFFECTED MODELS / IDS / BCF / DOCUMENTS → PRODUCER DISPOSITION → REVALIDATION → ACCEPTANCE / HOLD`.

Do not edit only the machine rule while leaving the authoritative requirement ledger stale.

## Failure attacks

Reject or revise when:
- a generic BIM template becomes the requirement source;
- an IFC property exists, so the team assumes it was required;
- an IDS file is treated as the source authority although it is only a translation;
- machine-checkable facets are encoded while human/professional requirements disappear;
- a requirement is copied between IFC schemas without checking semantic availability;
- a bSDD class/property is treated as mandatory merely because it is standardized or published;
- delivery responsibility is inferred from software ownership;
- one ISO 19650 acronym/workflow is imposed on a project whose actual authority uses another structure;
- a requirement is marked satisfied because a file exists, without checking the required information and revision;
- a waiver/exception is applied without recording authority and affected claim;
- validation success is promoted to design quality, engineering approval, legal acceptance or contractual compliance.

## Source / transfer boundary

Professional sources studied:
- UK BIM Framework guidance on developing information requirements / ISO 19650 implementation — retained the information-need-first, lifecycle/decision and explicit-requirement principles; UK-specific terminology/templates are not universal defaults.
- buildingSMART IDS 1.0 — retained the requirement→computer-interpretable specification relationship and the boundary between source requirement and executable validation.
- buildingSMART bSDD — retained dictionary/class/property definition and reference semantics; dictionary content is not automatically project requirement authority.

External Skill studied:
- `jeffersonbim/Information-Manager-IFC-skill` — MIT. Retained only independently reformulated professional separations around approved requirement source, schema-specific semantics, IDS translation and human approval. OpenClaw, Revit, Docker, LGPD, Notion-RAG, fixed gate questionnaire, templates, scripts and house runtime are not installed into OLEANDER.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / OFFICIAL-SOURCE + MIT-SKILL DIGESTED / PRACTICE NOT YET RUN / NO PROJECT USAGE / NO PROMOTION`.