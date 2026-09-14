# OLEANDER Knowledge Classification Detail Framework v1.0｜知识分类细则框架 v1.0

Status: **EXECUTION MIRROR / GOVERNANCE EXTENSION**. Notion Current Authority remains canonical. This file does not create a second taxonomy, Registry, Authority, Knowledge Role system, or Project Axis.

## 1｜Dynamic Corpus Contract｜动态语料规模合同

OLEANDER corpus size is dynamic. Any count such as `1215`, `1184`, or `1024` is a time-bounded census snapshot only. It is never a system limit, permanent migration denominator, or completion target.

Every census must carry at least:

`as_of + registry_scope + enumeration_basis + total_observed + unresolved + provenance/excluded_scope`.

Migration/content remediation completes only relative to an explicit snapshot through:

`enumeration closure + per-object decision + readback`.

New objects after the snapshot enter the applicable classification/content/lifecycle queue automatically. Historical hard-coded corpus totals have no authority unless explicitly labelled with date and scope.

Current correction: the previously used `1215-object` wording is interpreted only as the current reported snapshot for the 2026-09-15 remediation cycle, not as a fixed corpus size.

## 2｜Classification Axes｜分类轴分离

Resolve each applicable canonical object on independent axes:

1. `Registry / Carrier`: Domains / Notes / Projects / People / Inspiration / Resources / external Source Authority.
2. `Structural Level`: Domains `L0–L3`; Notes `L4–L7`; Projects `P0–P4`.
3. `Primary Knowledge Role`: `INDEX / THEORY / METHOD / TOOL / SOURCE / EVIDENCE / CASE / PRACTICE`; one primary role per canonical Notes object.
4. `Framework-Type`: secondary refinement for framework-like objects only.
5. `Information Role`: dominant body-use function.
6. `Domain`: one Primary Domain by default + 0..N Related Domains.
7. `Scope`: `SYSTEM / CROSS-DOMAIN / DOMAIN / TOPIC / APPLICATION / PROJECT / CASE-LOCAL`.
8. `Epistemic / Evidence`: fact/source/evidence/interpretation/inference/hypothesis/assumption/unknown + claim confidence.
9. `Application Mapping`: Business / Culture / IP / Spatial; usage only, never taxonomy.
10. `Project Axis`: P0–P4 and project relations; application never rewrites universal knowledge identity.
11. `Retrieval`: CURRENT / SUPPORT / PROVENANCE / EXCLUDED + Search Eligibility.
12. `Lifecycle`: Governance / Trust / Freshness / verification due / supersession.

No axis may silently stand in for another.

## 3｜Structural Level Contract｜层级合同

### Domain taxonomy
- `L0 System`: knowledge-system root; no professional body ownership.
- `L1 Branch`: stable navigation/routing branch.
- `L2 Domain`: formal professional domain; primary Notes routing target.
- `L3 Topic`: stable topic, deepest Current taxonomy unit.
- Legacy Domain L4/L5 identities are migration residue and must not expand the taxonomy.

### Notes knowledge layer
- `L4 Framework`: organises stable reusable L5 knowledge; does not become a bulk source/evidence archive.
- `L5 Knowledge Object`: reusable Theory / Method / Tool / professional knowledge owner.
- `L6 Evidence / Case`: Source / Evidence / Case; supports/refutes/bounds knowledge and does not automatically become a universal Current Rule.
- `L7 Practice / Output`: project use, training, test, failure repair, validation output and transferable-practice evidence frontier; does not automatically replace its L5 owner.

### Project layer
- `P0–P4` remains project identity only. Case IDs, Application Mapping and L0–L7 cannot substitute for Project identity.

## 4｜Primary Knowledge Role Contract｜主知识角色

Exactly one primary semantic role:

- `INDEX`: navigation/aggregation; normally L4; does not own professional truth by aggregation.
- `THEORY`: mechanism, principle, model, stable explanatory relation; mainly L4/L5.
- `METHOD`: executable method, workflow, decision procedure; mainly L5.
- `TOOL`: reusable tool/validator/runtime/executor identity; mainly L5. A single tool-run record is L7 PRACTICE/OUTPUT evidence.
- `SOURCE`: original paper, standard, official page, manufacturer documentation, publication or other source carrier; L6.
- `EVIDENCE`: experiment, measurement, comparison, verification result, inspectable evidence; L6.
- `CASE`: bounded real case and its documented facts; L6. Universal rules extracted from it must bind back to an L5 owner.
- `PRACTICE`: training, project use, A/B, failure repair, validation practice, reusable output evidence; L7.

`Knowledge Type` describes content form/use only and cannot override Level or Primary Role.

## 5｜Level × Role Allowed Matrix

| Level | Default roles | Conditional | Default forbidden |
|---|---|---|---|
| L4 Framework | INDEX / THEORY | METHOD only for true framework-level method systems | SOURCE / EVIDENCE / CASE / PRACTICE / one-off TOOL |
| L5 Knowledge Object | THEORY / METHOD / TOOL | INDEX for explicit MOC; current interpretation object for a professional standard | original SOURCE / single CASE / one-off PRACTICE |
| L6 Evidence / Case | SOURCE / EVIDENCE / CASE | — | THEORY / METHOD / INDEX / PRACTICE |
| L7 Practice / Output | PRACTICE | TOOL only as tool-output/run evidence, not tool identity | THEORY / METHOD / SOURCE / CASE / INDEX |

Out-of-matrix combinations require full-body evidence and enter `ROLE_DRIFT / REVIEW` until resolved.

## 6｜Framework-Type Contract｜框架类型

Framework-Type is a secondary diagnostic classification, normally for L4 and exceptional framework-like L5 MOC objects. It never creates a new taxonomy depth or a mandatory field merely for completeness.

Allowed types:

- `MOC_NAVIGATION_FRAMEWORK`
- `THEORY_FRAMEWORK`
- `METHOD_SYSTEM_FRAMEWORK`
- `APPLICATION_FRAMEWORK`
- `CROSS_DISCIPLINARY_INTEGRATION_FRAMEWORK`
- `EVALUATION_REVIEW_FRAMEWORK`
- `GOVERNANCE_RUNTIME_FRAMEWORK`
- `REFERENCE_COMPARISON_FRAMEWORK`

Rules:
- MOC/Navigation aggregates discovery but does not own truth by aggregation.
- Theory Framework organises explanatory concepts/mechanisms.
- Method System coordinates multiple executable methods/decision procedures.
- Application Framework binds reusable knowledge to a declared application context without becoming a Project object.
- Cross-Disciplinary Integration owns interfaces/shared variables/dependencies, not discipline authority.
- Evaluation/Review owns review criteria and PASS scope only; its PASS cannot imply Design/Research/Field PASS outside scope.
- Governance/Runtime remains subordinate to Current Authority and cannot become parallel authority.
- Reference/Comparison organises references/evidence dimensions; examples do not become requirements.

Mismatch → `FRAMEWORK_TYPE_DRIFT / REVIEW`.

## 7｜Information Role Contract｜信息作用

Information Role answers “what is this body primarily doing for the reader?” It is not the same as Primary Knowledge Role.

- `ORIENT`: map/index/overview.
- `EXPLAIN`: definition/mechanism/theory/interpretation.
- `INSTRUCT`: method/procedure/workflow/decision protocol.
- `REFERENCE`: stable fact/specification/glossary/source identity/technical reference.
- `PROVE`: measurement/test/experiment/comparison/evidence supporting or refuting claims.
- `EXEMPLIFY`: bounded case/precedent.
- `RECORD`: receipt/chronology/practice log/provenance/audit trace.
- `DECIDE`: authorised decision/rule/constraint within declared governance scope.
- `OUTPUT`: project/practice artifact or deliverable evidence.

Secondary functions are allowed. If two independent primary responsibilities coexist without hierarchy, route to K2 `SPLIT / RESTRUCTURE` rather than multi-role ambiguity.

## 8｜Domain & Scope Contract｜领域与适用尺度

- Primary Domain: default exactly one for Current L4/L5 objects.
- Related Domains: 0..N, semantic adjacency only.
- Cross-domain relevance is not permission to avoid selecting a primary domain.
- Scope must prevent false generalisation: `SYSTEM / CROSS-DOMAIN / DOMAIN / TOPIC / APPLICATION / PROJECT / CASE-LOCAL`.
- Application Mapping and Project relations are orthogonal to Domain.

## 9｜Object Classification Decision Tree｜对象判定树

Read the exact CURRENT full body first, then reconcile metadata/relations:

1. Domain routing identity? → Domains DB / L0–L3.
2. Project/Program/Workstream/Validation identity? → Projects DB / P0–P4.
3. Stable responsibility is organising reusable knowledge? → L4 Framework; resolve Role + Framework-Type.
4. Reusable explanatory/procedural/tool knowledge itself? → L5 THEORY / METHOD / TOOL.
5. Original source, empirical evidence or bounded real case? → L6 SOURCE / EVIDENCE / CASE.
6. Application/training/test/failure-repair/receipt/output? → L7 PRACTICE / conditional tool-output evidence.
7. No fit without semantic stretching? → `CLASSIFICATION_OPEN / REVIEW`; never force-fit for field completeness.

Then resolve Domain → Scope → Information Role → source/evidence chain → Application/Project relations → Retrieval/Lifecycle.

## 10｜Classification Precedence｜冲突优先级

For review decisions:

`Current Authority / Registry contract → canonical identity + actual CURRENT full-body semantic responsibility → applicable Level contract → Primary Role → Framework-Type / Information Role → Domain & Scope → dedicated relations → Knowledge Type → title / breadcrumb / aliases / legacy labels`.

Hard boundaries:
- title/path/legacy labels are weak evidence;
- Knowledge Type cannot overrule Level/Role;
- Application Mapping cannot overrule Domain;
- Project relation cannot overrule knowledge classification;
- `related` cannot substitute for Parent/Source/Method/Project relation;
- metadata/body contradiction yields an explicit drift state, not silent choice.

Drift states:
`LEVEL_DRIFT / ROLE_DRIFT / DOMAIN_DRIFT / FRAMEWORK_TYPE_DRIFT / RELATION_DRIFT / RETRIEVAL_DRIFT`.

## 11｜Classification Evidence & Confidence｜分类证据与置信度

Evidence classes:
- `FULL_BODY_EVIDENCE`: current body read and semantic responsibility identified.
- `STRUCTURE_EVIDENCE`: level/parent/domain/relations support classification.
- `SOURCE_CHAIN_EVIDENCE`: source/evidence/method/project lineage supports classification.
- `GRAPH_ONLY`: structural evidence without adequate body review; triage only.
- `LINEAGE_ONLY`: historical/provenance evidence only; triage/history only.

Confidence:
- `HIGH`: body + structure + relation/source chain materially agree.
- `MODERATE`: body clear, one structural/relation axis remains open.
- `LOW`: body mixed, incomplete, ambiguous, or carrier collision exists.

`GRAPH_ONLY` and `LINEAGE_ONLY` cannot independently award semantic classification closure or Content PASS.

## 12｜Atomicity / Split / Merge｜原子性、拆分与合并

Trigger `SPLIT / RESTRUCTURE` when one carrier independently owns multiple responsibilities without hierarchy, especially:
- theory + method;
- source + interpretation;
- case facts + universal rule;
- method + single project receipt;
- tool identity + tool-run log;
- framework + bulk evidence archive.

Trigger `MERGE / REDIRECT` only when carriers materially duplicate canonical responsibility, claim set, scope and current-answer function. Similar names alone are insufficient.

All split/merge operations obey `NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS`.

## 13｜Relation Closure｜关系闭合

Strong semantic owners use dedicated current relations:
- Canonical Parent: 0..1 for Current L4/L5, except root framework; conditional for L6/L7.
- Canonical Children: 0..N by real hierarchy.
- Primary Domain: default 1.
- Related Domains: 0..N.
- Source relation: 0..N; Current rules/methods need a traceable source/evidence chain unless explicitly internal governance authority.
- Method invocation: actual invocation only.
- Primary Project: 0..1 for project-specific Practice/Case.
- Related Projects: 0..N.
- Supersession: same logical identity lifecycle only.

Weak relations (`related / people / resource / inspiration`) improve discovery only and cannot repair a missing strong semantic relation.

## 14｜Classification Closure Gate

`CLASSIFICATION PASS` requires, as applicable:
- correct registry/carrier;
- valid structural Level;
- one Primary Role;
- Framework-Type resolved when framework-like;
- Information Role resolved;
- defensible Primary Domain + Related Domains;
- explicit enough Scope;
- semantic dedicated relations;
- Application/Project axes kept separate;
- Retrieval/Lifecycle compatible with evidence;
- exact CURRENT full body read;
- no unresolved identity collision or Major semantic drift;
- readback PASS.

`CLASSIFICATION PASS ≠ CONTENT PASS ≠ RESEARCH PASS ≠ KNOWLEDGE OBJECT PASS ≠ CANONICAL CURRENT`.

## 15｜Count-Agnostic Remediation Loop｜与数量无关的治理循环

`ENUMERATE CURRENT SCOPE → snapshot census → canonical collision preflight → CURRENT FULL BODY READ → multi-axis classification → content/research review → relation/provenance/lifecycle repair → bilingual repair when applicable → independent review when required → fetch/readback → explicit state → next object`.

A batch is scheduling only:

`batch complete ≠ corpus complete`.

Corpus completion is always relative to an explicit `as_of + scope + enumeration basis` snapshot.

## 16｜Authority Boundary

Canonical source: Notion `OLEANDER Knowledge Retrieval & Lifecycle｜知识库机制 v1.1`, §25 `Classification Detail Framework v1.0`, bound by Root Current Authority and Project Control Plane.

This GitHub file is an execution mirror for validators, agents and regression tests. If it conflicts with a newer Notion Current Authority/readback, stop and rebind; do not create a parallel truth.