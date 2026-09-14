# OLEANDER Work / Artifact / Information Carrier Contract v1.0

Status: **DRAFT GOVERNANCE EXTENSION / PRIORITY P8**. Applies to Project-plane Work and Artifact objects. It does not make file structure the source of project semantics.

## 1. Core separation

- `WORK_PACKAGE` — a bounded unit of coordinated work with an outcome/responsibility;
- `TASK` — a bounded executable action;
- `ARTIFACT` — an information/physical/digital carrier produced, consumed or reviewed by work;
- semantic project truth — Requirement, Decision, Variable, Interface, Claim, Evidence, Baseline, etc.

Hard rules:

`TASK DONE ≠ WORK ACCEPTED`.

`ARTIFACT EXISTS ≠ SEMANTIC OBJECT SATISFIED`.

`LATEST FILE ≠ CURRENT AUTHORITY`.

`EXPORT SUCCESS ≠ DESIGN / TECHNICAL / PROJECT PASS`.

## 2. Work Package contract

Minimum fields:

```yaml
work_package_id:
project_id:
workstream_id:
outcome:
scope_in: []
scope_out: []
owner:
contributors: []
decision_object_ref:
input_objects: []
required_outputs: []
requirements: []
constraints: []
dependencies: []
interfaces: []
acceptance_conditions: []
required_readback: []
claim_ceiling_ref:
planned_tasks: []
open_blockers: []
status:
```

State:

`PLANNED → READY → IN_PROGRESS → REVIEW → ACCEPTED_FOR_SCOPE | CANCELLED | SUPERSEDED`.

Rules:
- Work Package is outcome-oriented, not software-oriented;
- it may contain tasks across several tools;
- acceptance depends on agreed outcome/readback, not task count;
- project Work Package is not a reusable Knowledge Method.

## 3. Task contract

Minimum fields:

```yaml
task_id:
project_id:
work_package_id:
action:
owner:
inputs: []
expected_output:
allowed_mutation_class:
protected_objects: []
dependencies: []
execution_surface:
required_readback:
stop_conditions: []
result_refs: []
status:
```

State:

`PLANNED → READY → IN_PROGRESS → REVIEW → DONE | CANCELLED | SUPERSEDED`.

`DONE` means the action completed according to its task-level execution contract. It does not grant Work Package acceptance, Artifact authority, Design KEEP or Project promotion.

## 4. Task objectification threshold

Create an independent Task record only when at least one applies:

- assignment/owner matters;
- dependency/schedule matters;
- mutation/readback scope matters;
- failure/retry must be traceable;
- task output feeds a consequential Decision/Artifact;
- the task must survive chat/session/tool interruption.

Do not create Task objects for every keystroke/tool operation.

## 5. Artifact contract

An Artifact is a carrier. It may represent or embody semantic project objects, but it does not inherit their semantic class automatically.

Minimum fields:

```yaml
artifact_id:
project_id:
artifact_type:
carrier_role:
carrier_uri:
native_format:
version_or_revision:
digest:
producer:
owner:
source_authority_ref:
represents: []
implements: []
contains_evidence_refs: []
derived_from: []
derivative_of: []
baseline_ref:
editability_state:
loss_profile:
rights_or_access_state:
target_medium:
readback_refs: []
supersedes:
status:
```

## 6. Artifact types

High-level controlled set:

`DOCUMENT | DRAWING | MODEL_3D | CAD_BIM | IMAGE | VIDEO | AUDIO | DATASET | CODE | WEB_APP | PROTOTYPE | PHYSICAL_SAMPLE | SPECIFICATION | TABLE | DIAGRAM | MAP_GIS | PRESENTATION | PUBLICATION | PACKAGE_ARCHIVE | OTHER_CONTROLLED`.

Artifact Type describes carrier form, not semantic authority.

## 7. Carrier roles

Use one primary carrier role plus optional secondary roles when materially useful:

- `SOURCE_MASTER` — authoritative source carrier for defined source truth;
- `EDITABLE_MASTER` — Current editable production master;
- `DERIVATIVE` — transformed/exported form of another master;
- `EVIDENCE_CARRIER` — carries Evidence Records but is not automatically the evidence semantic object;
- `PRESENTATION_CARRIER` — audience projection;
- `DELIVERY_PACKAGE` — packaged handoff/release form;
- `REFERENCE_INPUT` — source/reference consumed by work;
- `TEMPORARY_WORKING` — intermediate, non-authoritative carrier;
- `PROVENANCE_ARCHIVE` — retained for historical lineage.

`SOURCE_MASTER` and `EDITABLE_MASTER` may be the same carrier when authority says so, but the roles remain conceptually distinct.

## 8. Artifact state

`WORKING → REVIEWABLE → ACCEPTED_FOR_SCOPE → BASELINED | SUPERSEDED | WITHDRAWN`.

Rules:
- Artifact acceptance is scoped;
- `BASELINED` means included in an approved configuration, not inherently high design quality;
- superseded artifact can remain valid historical evidence for its configuration;
- withdrawn artifact must not silently remain Current through old links.

## 9. Editable master rule

When the deliverable requires editability, maintain one explicit Current editable/native master identity.

Examples:
- SVG/AI/source vector for graphics when editable vector is required;
- PPTX/source deck for editable presentation;
- SKP/BLEND/BIM/CAD native model when geometry editability is required;
- HTML/CSS/JS or source app for interactive deliverable;
- source publication file when production requires it.

Flattened PDF/PNG/JPG/video/screenshot is a derivative unless Current Authority explicitly defines it as source/master for its limited role.

## 10. Source / derivative relation

Every material derivative should preserve:

`upstream master identity + upstream revision + transformation + information lost/baked + target purpose + readback`.

Common transformations:
- crop;
- mask;
- rasterize;
- flatten;
- simplify;
- export;
- compress;
- color-convert;
- render;
- bake;
- transcode;
- convert geometry/file format;
- translate/localize;
- annotate.

Transformation must not silently upgrade truth authority.

## 11. Loss profile

Use explicit loss categories when cross-software/export changes matter:

- `NO_MATERIAL_LOSS`
- `EDITABILITY_LOSS`
- `SEMANTIC_STRUCTURE_LOSS`
- `PARAMETRIC_LOSS`
- `GEOMETRY_APPROXIMATION`
- `COLOR_APPEARANCE_SHIFT`
- `FONT_TEXT_LOSS`
- `INTERACTION_STATE_LOSS`
- `METADATA_PROVENANCE_LOSS`
- `UNKNOWN_LOSS`

Material unknown loss requires reopen/readback before final handoff.

## 12. Cross-software handoff

For material handoff record:

```yaml
upstream_master:
upstream_revision:
downstream_surface:
exchange_format:
editability_retained:
known_loss_or_bake: []
protected_properties: []
reopen_method:
actual_readback_ref:
```

Never assume “file opens” means the handoff preserved design/geometry/metadata correctly.

## 13. Artifact authority boundaries

### Drawing/model
Can represent current geometry/design but cannot invent a Requirement/Decision merely because the geometry exists.

### Render/image
Can show appearance/spatial relation within source fidelity but cannot establish structural/field performance unless separate evidence exists.

### Data table/chart
Can project accepted data but visual encoding does not become data authority.

### Report/deck
Can communicate Claims/Decisions/Evidence but cannot become the underlying evidence solely through publication.

### Code/app
Can implement a behavior but source code correctness does not automatically prove user outcome or visual quality.

## 14. Artifact register semantics

Artifact Register should index carriers by stable Artifact ID and relations.

Minimum registry view:
- Artifact ID;
- type;
- primary role;
- Current status;
- source/master relation;
- revision/digest;
- baseline;
- semantic objects represented;
- rights/access;
- readback status;
- supersession.

Register entry does not create authority by itself.

## 15. Information Role vs Artifact Role

Do not confuse Knowledge-plane `Information Role` with Project Artifact carrier role.

Knowledge Information Role may be:
`EXPLANATION / PROCEDURE / REFERENCE / NAVIGATION / DECISION_SUPPORT / AUDIT_READBACK / CASE_NARRATIVE`.

Artifact carrier role describes how the carrier functions in the Project configuration.

A METHOD page can have `Information Role=PROCEDURE`; a PDF export of it can still be a `DERIVATIVE` artifact.

## 16. Work acceptance

A Work Package can become `ACCEPTED_FOR_SCOPE` only when:

- required outputs exist;
- semantic target objects are updated;
- required readback is complete;
- known material issues are resolved or explicitly bounded;
- artifact/master/derivative identities are clear;
- downstream dependencies/interfaces are updated;
- claim ceiling accurately reflects the outcome.

Task completion alone is insufficient.

## 17. Rework / repeat rule

When an artifact fails review:

- name the actual Issue/root cause;
- decide whether repair belongs to carrier, semantic project object or upstream source owner;
- do not keep regenerating exports when the upstream semantic object is wrong;
- after repair, reopen/readback actual target condition.

Repeated export without material repair is not progress.

## 18. Delivery boundary

A Delivery Package may contain baselined/accepted artifacts plus manifests/hashes/instructions.

Delivery acceptance does not auto-promote:
- project design quality;
- field validity;
- reusable Knowledge;
- professional approval.

## 19. Failure modes

Fail/HOLD when:

- task DONE is used as Work Package acceptance;
- artifact existence is used as Requirement/Decision/Evidence proof;
- latest modified file is treated as Current without authority/baseline;
- derivative replaces editable master when editability is required;
- cross-software conversion has unknown material loss but no readback;
- flattened/generative presentation derivative silently becomes source authority;
- source geometry/data altered for presentation convenience without upstream Change;
- superseded/withdrawn artifact remains Current through stale pointers;
- export success is used as Design/Technical/Project PASS.

## 20. Validator floor

- `WORK-001` Work Package has outcome/scope/owner/acceptance conditions;
- `WORK-002` Task DONE cannot auto-accept Work Package;
- `WORK-003` Work Package acceptance requires required readback;
- `TASK-001` material Task has mutation/readback/protected-object contract;
- `ART-001` Artifact has stable ID/type/role/source relation/version/status;
- `ART-002` Artifact not silently promoted to Requirement/Decision/Evidence semantic class;
- `ART-003` latest file not Current without authority/baseline;
- `ART-004` editable-master requirement cannot be closed with flattened derivative only;
- `ART-005` derivative records upstream identity/revision/transformation/material loss;
- `ART-006` unknown material loss requires readback/HOLD;
- `ART-007` presentation derivative cannot rewrite authoritative geometry/data;
- `ART-008` superseded/withdrawn artifact cannot remain Current through stale pointers;
- `HANDOFF-001` material cross-software handoff records loss + actual reopen/readback;
- `DELIVERY-001` delivery/export success cannot grant unrelated quality/evidence ceilings.

## 21. P8 closure condition

P8 is sufficiently refined for draft review when Work Package/Task semantics, Artifact types/roles/state, editable-master/derivative/source authority, loss profile, cross-software handoff, register and acceptance/readback rules all have machine-readable counterparts.
