# IDS + BCF OpenBIM Validation Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-delivery-qc`

Use when an IFC/openBIM delivery must be checked against machine-interpretable information requirements and/or when nonconformities are coordinated through BIM Collaboration Format (BCF).

This extension governs **scoped automated requirement validation + issue coordination closure evidence**. It does not create the source requirement, does not prove complete model/design quality, and does not make a BCF status change equivalent to verified correction.

## Existing-owner boundary

Use with:
- `oleander-delivery-qc/SKILL.md` for package integrity, 3D exchange reopen, dependency/source identity and final release claims;
- `oleander-design-process/INFORMATION_REQUIREMENT_EXCHANGE_CONTRACT_EXTENSION.md` for requirement authority and machine-checkable/non-machine-checkable separation;
- `oleander-3d-pipeline/IFC_SEMANTIC_EXCHANGE_HANDOFF_EXTENSION.md` for source→IFC semantic fidelity;
- actual project coordination/information-management authority for status workflow, responsibility, approvals and contractual acceptance.

## Core contract

### IDS
`AUTHORITATIVE REQUIREMENT ID → IDS TRANSLATION ID → APPLICABILITY → REQUIREMENT FACETS / CONSTRAINTS → IDS SCHEMA / VERSION → VALIDATOR + VERSION → TEST ARTIFACT REVISION → APPLICABLE POPULATION / COVERAGE → PASS / FAIL / NOT EVALUATED / TOOL LIMIT → SOURCE-REQUIREMENT RESIDUE → DISPOSITION / HOLD`

### BCF
`VALIDATION / COORDINATION FINDING → STABLE ISSUE ID → REQUIREMENT / FINDING SOURCE → AFFECTED MODEL REVISION + COMPONENT IDS → VIEWPOINT / CONTEXT WHEN NEEDED → RESPONSIBLE PARTY + STATUS → PROPOSED / IMPLEMENTED CHANGE → UPDATED MODEL REVISION → REVALIDATION / READBACK → ACCEPTANCE EVIDENCE → CLOSE / REOPEN / HOLD`

`IDS RESULT ≠ BCF ISSUE STATE ≠ UNDERLYING MODEL TRUTH`.

## IDS authority boundary

IDS 1.0 is a buildingSMART standard for expressing information requirements in a computer-interpretable form and checking IFC delivery against them. Treat an IDS file as a **translation carrier**, not the source requirement unless project authority explicitly designates it as such.

For every material IDS rule retain:
- source requirement ID and revision;
- IDS specification/identifier;
- target IFC schema(s);
- applicability population intention;
- requirement facets/constraints;
- what source requirement is not represented;
- validation runtime/tool/version;
- tested IFC identity/revision;
- coverage/result evidence.

`IDS FILE EXISTS ≠ REQUIREMENT COVERAGE`.

## Coverage gate

A validation report must show enough population context to know what was actually tested.

Record, where available:
- intended population;
- applicable count;
- passed count;
- failed count;
- not evaluated / unsupported count;
- exclusions and reason;
- validator/runtime warnings;
- rule/specification IDs linked to failures.

A `0 applicable / 0 tested` style result cannot silently become PASS when the rule was expected to cover objects. It is a coverage warning/HOLD until the absence of applicable objects is understood.

Do not generalize one validator's exact output labels or statistics as universal OLEANDER schema; preserve equivalent evidence.

## What IDS does not prove

Do not promote IDS validation to claims outside the encoded and supported scope. Depending on the actual standard/runtime, separate requirements may still be needed for:
- geometry quality or clash/clearance logic not represented by the specification;
- aggregate calculations;
- linked/external document existence/content;
- professional judgment;
- discipline engineering correctness;
- authoring-model health;
- visual/design quality;
- information management process/contract compliance;
- security/privacy obligations;
- complete inter-model coordination.

`IDS PASS ≠ MODEL CORRECT`.

`IDS PASS ≠ ISO 19650 COMPLIANCE`.

## Positive / negative validation evidence

When generating or maintaining a machine-checkable requirement, prefer at least one known-positive and one known-negative test condition where practical. This helps detect a rule that passes everything, matches nothing or encodes the wrong applicability.

For a production release, distinguish:
- rule/schema validity;
- validator/runtime operability;
- coverage validity;
- actual delivery result.

A valid XML/XSD document can still represent the wrong requirement.

## BCF coordination semantics

BCF is a communication/issue coordination standard and can be exchanged as file-based BCF or through web/API workflows. Record the version/mode when it matters.

A material issue should preserve:
- stable issue/topic ID;
- source finding / requirement / clash / review reference;
- project/model/federation identity and revision;
- affected IFC `GlobalId` or other controlled component identity when available;
- viewpoint/snapshot only as context, not as model authority;
- issue type/priority/status if the workflow uses them;
- responsible party / owner;
- comments/history without destructive rewrite;
- proposed/implemented correction;
- updated model/IFC revision;
- validation/readback evidence after correction;
- closure authority and date/state.

Do not install one status taxonomy, priority vocabulary or escalation sequence as universal OLEANDER truth.

## BCF closure gate

A BCF issue can close operationally only according to the actual project workflow, but OLEANDER evidence closure must additionally ask whether the underlying condition was retested.

Use:

`ISSUE STATUS CHANGE → TARGET REVISION EXISTS → AFFECTED CONDITION RECHECKED → ORIGINAL REQUIREMENT/FINDING NO LONGER FAILS OR AUTHORIZED WAIVER EXISTS → CLOSURE EVIDENCE`.

`BCF CLOSED ≠ CORRECTION VERIFIED`.

`FILE RESUBMITTED ≠ ISSUE RESOLVED`.

If a model changes after closure and may reopen the condition, preserve the reopen trigger or link to the relevant requirement regression test.

## IDS → BCF handoff

When an IDS failure becomes a BCF issue, preserve:

`IDS SPEC/RULE ID + SOURCE REQUIREMENT ID + VALIDATION RESULT + TESTED IFC REVISION → BCF ISSUE ID → AFFECTED COMPONENTS → CORRECTION → NEW IFC REVISION → RE-RUN SAME OR AUTHORIZED UPDATED RULE → RESULT`.

Do not copy only the human-readable error text and lose the original requirement/validation identity.

## bSDD / semantic reference gate

If an IDS or IFC requirement references bSDD or another dictionary:
- record dictionary/version/status and identifier/URI where material;
- confirm the project requirement actually adopts that definition;
- verify delivered class/property/value independently of the fact that a URI exists.

`VALID URI ≠ VALID PROJECT DATA`.

bSDD is a buildingSMART service for term/class/property definitions; it is not itself proof that a project requirement is met.

## Release package evidence

For a scoped openBIM validation release, preserve as applicable:
- authoritative requirement ledger revision;
- source/native model identity;
- IFC identity/hash/schema/view/scope;
- IDS identity/version/hash and source-requirement mapping;
- validator/runtime identity/version;
- machine-readable and human-readable validation result when available;
- coverage summary;
- unresolved non-machine-checkable requirements;
- BCF issue set identity/version/mode;
- issue→model revision links;
- closure/reopen evidence;
- known exporter/validator/viewer limitations;
- final claim ceiling.

## Failure attacks

Reject or revise when:
- IDS PASS is used as full BIM/model/design/contractual compliance;
- rule applicability matches no objects but the report is marked green;
- the source requirement changed but IDS did not;
- the IDS encodes only easy properties and silently drops geometry/professional obligations;
- validator version/tool behavior is material but unrecorded;
- one failed IFC revision is replaced and the issue is closed without rerunning the requirement;
- BCF status `Closed/Resolved` is accepted as proof without model/readback evidence;
- viewpoint screenshot is treated as underlying model authority;
- BCF issue loses the requirement/rule/model revision that created it;
- bSDD reference existence is used as data correctness proof;
- one BCF status/priority workflow becomes universal;
- one IfcTester/IfcOpenShell result schema, threshold or script becomes universal OLEANDER truth;
- automated validation replaces final release checks for source identity, package integrity and known losses.

## Source / transfer boundary

Professional sources studied:
- buildingSMART IDS 1.0 — retained machine-interpretable information requirement and IFC compliance-checking semantics, plus explicit scope/coverage boundary.
- buildingSMART BCF 3.0 / BCF technical documentation — retained file/API issue coordination and round-trip communication semantics.
- buildingSMART bSDD — retained term/class/property reference semantics; bSDD is a service, not a project acceptance state.
- buildingSMART IFC documentation — retained schema/version/view-specific exchange context.

External Skill studied:
- `jeffersonbim/Information-Manager-IFC-skill` — MIT. Retained independently reformulated principles: IDS source-requirement traceability, no silent `0/0` success, runtime/version evidence, IDS failure→BCF linkage, and close only after updated model validation. Source-specific OpenClaw, Docker, Revit, Notion-RAG, LGPD pipeline, scripts/templates and fixed runtime versions are not imported.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / OFFICIAL-SOURCE + MIT-SKILL DIGESTED / PRACTICE NOT YET RUN / NO PROJECT USAGE / NO PROMOTION`.