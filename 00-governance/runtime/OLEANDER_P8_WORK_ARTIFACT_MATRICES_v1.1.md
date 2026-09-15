# OLEANDER P8 Work / Artifact / Carrier Matrices v1.1

Status: **DRAFT COMPANION / PRIORITY P8 SECOND PASS**. Semantic owner remains `OLEANDER_WORK_ARTIFACT_INFORMATION_CARRIER_CONTRACT_v1.0.*`.

## 1. Purpose

P8 second pass makes work acceptance and information-carrier semantics explicit enough to prevent file-centric project control.

Core invariant:

`WORK OUTCOME ≠ TASK COMPLETION ≠ ARTIFACT EXISTENCE ≠ SOURCE AUTHORITY ≠ BASELINE ≠ DELIVERY RELEASE`.

---

## 2. Work Package Admission Matrix

Create a Work Package when the work has:
- bounded outcome;
- accountable owner;
- material inputs/outputs;
- acceptance conditions;
- one or more dependencies/interfaces;
- meaningful completion independent of individual tool actions.

Do not create a Work Package solely because:
- software/tool differs;
- file format differs;
- work lasts several days;
- a meeting occurred;
- one export needs to be made.

---

## 3. Work Package Acceptance Matrix

| Acceptance dimension | Required condition |
|---|---|
| outcome | stated outcome materially achieved |
| semantic target | affected Requirement/Decision/Variable/Interface/etc. updated as needed |
| required outputs | carriers exist in required roles/formats |
| readback | actual result reopened/read back under target condition |
| issues | material issues closed/bounded |
| dependencies | downstream state updated |
| interfaces | affected interface state reconciled |
| authority | source/master/current roles clear |
| claim ceiling | outcome claim does not exceed evidence |
| handoff | receiver can use required native/editable representation when promised |

Task count/completion percentage is not acceptance evidence.

---

## 4. Task Granularity Matrix

| Task pattern | Independent Task object? |
|---|---:|
| consequential mutation with owner/readback | YES |
| resumable across sessions/tools | YES |
| retry/failure history matters | YES |
| output feeds material Decision | YES |
| trivial keystroke/export substep | NO |
| routine tool command inside already-scoped Task | NO |
| read-only inspection that generates a consequential finding | MAYBE; often evidence/review record rather than Task |

Over-tasking increases runtime noise and weakens retrieval.

---

## 5. Artifact Role Matrix

| Carrier role | Authority meaning | Typical examples | Cannot imply |
|---|---|---|---|
| `SOURCE_MASTER` | authoritative carrier for a defined source truth | canonical dataset, approved geometry source, brand master | professional/field truth beyond source scope |
| `EDITABLE_MASTER` | current production-editable carrier | SKP/BLEND/CAD/AI/PPTX/source app | source authority unless explicitly assigned |
| `DERIVATIVE` | transformed/exported view | PDF/PNG/JPG/render/transcode | replacement of editable/source master |
| `EVIDENCE_CARRIER` | carries an Evidence Record | test report, measurement file, screenshot set | Evidence admissibility/PASS automatically |
| `PRESENTATION_CARRIER` | audience-facing projection | board/deck/site/video | Project truth/Design KEEP automatically |
| `DELIVERY_PACKAGE` | issued handoff bundle | ZIP/IFC package/PDF set/app build | Current baseline automatically |
| `REFERENCE_INPUT` | consumed source/reference | precedent, external file | requirement/constraint authority automatically |
| `TEMPORARY_WORKING` | intermediate | scratch export/cache | Current status |
| `PROVENANCE_ARCHIVE` | historical lineage | superseded package/source | default retrieval/current authority |

---

## 6. Source Master × Editable Master Matrix

These roles may coincide or differ.

| Case | SOURCE_MASTER | EDITABLE_MASTER |
|---|---|---|
| native CAD/BIM is authoritative geometry | same file/model may serve both | same |
| external survey PDF is source truth, rebuilt CAD used for design | PDF/source survey | editable CAD derivative/model |
| approved image/photo is evidence source, PSD is retouch working file | original file | PSD/working master |
| spreadsheet data is authoritative, dashboard code visualizes it | dataset/table | dashboard/source code |
| client-supplied logo master is locked, project AI/SVG layout uses copy | client master | project composition file |

Editable master cannot re-author upstream source truth unless authority explicitly transfers.

---

## 7. Artifact State × Semantic State Matrix

Artifact state and represented-object state remain independent.

Examples:
- Artifact `REVIEWABLE`; represented design still `EXPLORE`.
- Artifact `BASELINED`; Project Claim still `REVISE`.
- Artifact `SUPERSEDED`; historical Evidence still valid for old configuration.
- Artifact `ACCEPTED_FOR_SCOPE`; Requirement remains `FAILED`.

Validator must not infer semantic state from carrier state.

---

## 8. Derivative Transformation Risk Matrix

| Transformation | Typical loss | Minimum record/readback |
|---|---|---|
| crop | context loss | crop bounds + source ref + claim boundary |
| mask/retouch | visibility/source fidelity change | transformation disclosure when evidentiary |
| rasterize | editability/vector semantics | retain editable master |
| flatten | layer/provenance/editability loss | source master link |
| simplify geometry | detail/accuracy loss | tolerance/claim boundary |
| export/transcode | metadata/color/codec/state loss | target-condition readback |
| format conversion | parametric/semantic/geometry loss | loss profile + reopen in downstream tool |
| render/bake | material/light/state baked | source geometry/material refs |
| localization/translation | semantic/text/layout drift | semantic + longest-string readback |
| compression | quality/data loss | fit-for-purpose threshold/readback |

Unknown material loss = `HOLD/RECHECK`, not `NO_MATERIAL_LOSS`.

---

## 9. Loss Severity Matrix

Use orthogonal loss flags plus severity:

Loss flags:
`EDITABILITY_LOSS | SEMANTIC_STRUCTURE_LOSS | PARAMETRIC_LOSS | GEOMETRY_APPROXIMATION | COLOR_APPEARANCE_SHIFT | FONT_TEXT_LOSS | INTERACTION_STATE_LOSS | METADATA_PROVENANCE_LOSS | UNKNOWN_LOSS`.

Severity:
- `NONE`
- `NON_MATERIAL`
- `MATERIAL_BOUNDED`
- `CLAIM_AFFECTING`
- `AUTHORITY_BREAKING`

Examples:
- PDF losing editable layers may be `MATERIAL_BOUNDED` when editable handoff required;
- IFC conversion changing geometry beyond tolerance is `CLAIM_AFFECTING` or `AUTHORITY_BREAKING`;
- web screenshot losing interaction is expected derivative loss but invalid as interaction proof.

---

## 10. Cross-Software Handoff Matrix

A material handoff must preserve:

`upstream identity + upstream revision + exchange format + protected properties + known loss + downstream target + actual reopened result + discrepancy disposition`.

| Readback finding | Disposition |
|---|---|
| no material difference | ACCEPT handoff |
| bounded expected loss within claim | ACCEPT_WITH_LIMITATION |
| fixable transformation error | REVISE conversion |
| source semantic/geometry change | reject derivative; repair upstream/change authority |
| unknown discrepancy | HOLD until bounded |

`file opens successfully` is never sufficient readback.

---

## 11. Artifact Register vs Source of Truth Matrix

Artifact Register may index:
- stable Artifact ID;
- carrier role;
- URI/revision/hash;
- source/derivative relations;
- represented semantic objects;
- baseline/release membership;
- status/readback/rights.

Register cannot:
- manufacture source authority;
- replace Project semantic objects;
- declare design/evidence/professional PASS from file metadata;
- make a stale pointer Current.

---

## 12. Delivery Package Matrix

Every consequential Delivery Package should declare:

`delivery_id + recipient/audience + purpose + source baselines + included artifacts/revisions + editable masters included? + known loss + manifests/hashes + required software/dependencies + rights/access + acceptance/readback`.

Package types may include:
`REVIEW_PACKAGE | CLIENT_HANDOFF | FABRICATION_PACKAGE | CONSTRUCTION_ISSUE | PUBLICATION_RELEASE | WEB_APP_RELEASE | ARCHIVE_PACKAGE`.

Delivery package acceptance only means the delivery contract is met.

---

## 13. Rights / Access / Security Matrix

Artifact usability also depends on access/rights.

Track when applicable:
- access owner;
- license/usage restriction;
- confidential/sensitive state;
- expiration/signed URL risk;
- external dependency availability;
- font/plugin/software dependency;
- personal/sensitive data restrictions.

An artifact can be technically valid yet non-deliverable because access/rights/dependency is invalid.

ISO 19650-1:2018 remains current while a second edition is under development; its emphasis on exchanging, recording, versioning and organizing information across the asset lifecycle supports this information-management separation without making BIM file conventions universal OLEANDER semantics.

---

## 14. Rework Routing Matrix

| Failure observed in | Repair owner |
|---|---|
| wrong project truth/geometry | upstream semantic/source owner |
| correct source, bad export | carrier/conversion owner |
| correct carrier, weak visual communication | Presentation owner |
| missing evidence provenance | Evidence owner |
| wrong requirement/decision | P3/P2 owner, not artifact producer alone |
| stale baseline pointer | P5 configuration owner |

Do not regenerate derivatives repeatedly when upstream truth is wrong.

---

## 15. Validator additions for P8 v1.1

- `P8/WORK-M01`: Work Package acceptance requires outcome + semantic target + outputs + readback + dependency/interface reconciliation.
- `P8/TASK-M01`: trivial tool operations must not be objectified into runtime noise unless traceability need exists.
- `P8/ART-M01`: Artifact state cannot auto-set represented semantic-object state.
- `P8/MASTER-M01`: editable master and source master roles must be separately resolvable where they differ.
- `P8/DER-M01`: material derivative records source revision + transformation + loss + readback.
- `P8/LOSS-M01`: unknown material conversion loss blocks final handoff/claim until bounded.
- `P8/HAND-M01`: cross-software handoff requires actual downstream reopen/readback, not file-open success.
- `P8/REG-M01`: Artifact Register metadata cannot create source authority.
- `P8/DEL-M01`: Delivery Package declares controlling baselines and included revisions.
- `P8/ACCESS-M01`: invalid rights/access/dependency state can block deliverability even if artifact content is correct.
- `P8/REWORK-M01`: downstream carrier failure must not be repeatedly regenerated when root cause is upstream semantic truth.

## 16. P8 v1.1 closure test

P8 second pass is ready for validator compilation when test cases can distinguish:
- Task DONE vs Work accepted;
- Source Master vs Editable Master;
- Artifact state vs semantic-object state;
- derivative loss vs authority break;
- successful file-open vs valid handoff;
- artifact register vs authority;
- delivery acceptance vs Project/Design/Professional promotion.
