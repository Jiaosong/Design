# OLEANDER P1 Authority / Execution Matrices v1.1

Status: **DRAFT COMPANION / PRIORITY P1 SECOND PASS**. Semantic owner remains `OLEANDER_AUTHORITY_INVOCATION_STALENESS_CLAIM_PROMOTION_CONTRACT_v1.0.*`. This file makes P1 operationally decidable; it does not create a second authority model.

## 1. Purpose

P1 exists to prevent a technically successful action from mutating the wrong truth, configuration, scope or claim.

Core invariant:

`EXECUTE ONLY WHEN AUTHORITY + SCOPE + CONFIGURATION + MUTATION + READBACK + CLAIM CEILING ARE COHERENT`.

The matrices below are normative draft routing rules for future validator compilation.

---

## 2. Authority Responsibility Matrix

Authority is property-scoped. There is no universal numeric rank.

| Governed property / question | Primary authority class | May specialize / contribute | Cannot silently override |
|---|---|---|---|
| System identity, namespace, Object Plane, canonical routing | `SYS_ROOT` | Registry-specific delegated rule | Project task, file path, runtime receipt, presentation |
| Project objective, project scope, active Project State | `PROJECT_GOV` | authorized Workstream state | Method/Skill, artifact author, presentation |
| Law, code, contract, regulator/client mandate | `EXTERNAL_MANDATE` | authorized waiver/deviation authority | ordinary design trade-off or method preference |
| Authoritative geometry/data/content/brand/spec source | `SOURCE_AUTHORITY` | authorized Decision/Change under scope | derivative, render, export, duplicate carrier |
| Current baseline, controlled value, configuration pointer | `CONFIG_AUTHORITY` | approved Change / delegated controller | newest file, most recent save, downstream consumer |
| Selection/trade-off/waiver/acceptance decision | `DECISION_AUTHORITY` | evidence and participating specialists | method, executor, runtime receipt |
| What a bounded observation/test establishes | `EVIDENCE_AUTHORITY` | accepted method + reviewer | design desire, presentation, citation count |
| Reusable execution/research/design method | `KNOWLEDGE_METHOD` | Project may narrow applicability | Project facts, requirements, Source Authority |
| Current packet/register/receipt/gate/snapshot state | `RUNTIME_CONTROL` | authoritative sources it references | source truth itself |
| Audience-facing representation | `PRESENTATION_DERIVATIVE` | source truth and release owner | source geometry/data/evidence/Project truth |

### 2.1 Conflict outcome codes

- `USE` — one authority clearly owns the property and is valid.
- `SPECIALIZE` — lower/more specific rule is inside explicit delegation.
- `SUPERSEDE` — explicit approved lineage replaces prior authority/configuration.
- `WAIVER` — externally/higher-controlled condition is lawfully excepted within bounded scope.
- `REOPEN` — prior decision/receipt/evidence must be re-evaluated because its basis changed.
- `ESCALATE` — current owner lacks authority to resolve the conflict.
- `HOLD` — conflict is unresolved or authority cannot be proven.
- `REJECT` — attempted override is outside authority.

### 2.2 Conflict Resolution Matrix

| Conflict pattern | Required decision | Allowed outcome | Forbidden shortcut |
|---|---|---|---|
| Same logical object, same property, two active change authorities | resolve delegation/joint-authority contract | one effective authority or explicit joint contract | latest timestamp wins |
| Project design conflicts with external mandate | test applicability + waiver path | conform, authorized waiver/deviation, or HOLD | trade-off score cancels mandate |
| Newer file conflicts with Current baseline | inspect Change/Baseline lineage | candidate only, or approved new baseline | newest file = Current |
| Source Authority conflicts with later authorized Decision | verify Decision had change authority for that property | Decision/Change may supersede source state | source always wins regardless of authorized change |
| Runtime receipt conflicts with source/project state | re-read referenced source revisions | receipt becomes stale/historical | receipt redefines source truth |
| Method recommendation conflicts with Project requirement | Project requirement governs project fact; method applicability narrows | adapt/choose another method | method rewrites requirement |
| Presentation derivative conflicts with exact geometry/data | source governs truth; derivative must disclose transformation | bounded projection only | presentation replaces source |
| Two standards/regulations appear contradictory | establish jurisdiction/version/applicability and controlling authority | bounded controlling rule or professional/legal escalation | choose the easier requirement |
| Old evidence conflicts with new material evidence | evaluate configuration/time/method comparability | reopen claim/decision/assurance as needed | average incompatible evidence into false certainty |
| Current task asks to change protected/locked object | compare mutation budget and authority | Change/escalation/reframe | silently widen task scope |

Hard rule: unresolved same-property authority conflict = `HOLD`, not probabilistic inference.

---

## 3. Mutation × Readback Matrix

Readback burden is determined by semantic blast radius, not tool difficulty.

| Mutation class | Minimum readback | Mandatory readback targets | Automatic escalators |
|---|---|---|---|
| `READ_ONLY` | `RB0` | none; preserve source refs | discovered contradiction may create separate issue, not mutation |
| `PRESENTATION_ONLY` | `RB1` | changed presentation + source recoverability + label/truth boundary | source crop/transform affects evidence meaning → RB2; cross-channel release pointer → RB4 |
| `LOCAL_CARRIER_EDIT` | `RB1` | edited carrier + semantic equivalence to owning object | carrier used by downstream consumers → RB2 |
| `SEMANTIC_OBJECT_EDIT` | `RB2` | object + direct typed dependents/consumers | shared variable/interface/requirement impact → RB3 |
| `CROSS_OBJECT_COORDINATION_EDIT` | `RB3` | all affected owners + interfaces + shared variables + integrated readback | baseline/current pointer or promotion basis changes → RB4 |
| `CONFIGURATION_CHANGE` | `RB3` + `RB4` for Current pointer | changed configuration + consumers + affected assurance + baseline pointer/readback | authority assignment changes → full RB4 authority scan |
| `AUTHORITY_CHANGE` | `RB4` | root/project/source/config/decision authority pointers + cross-platform drift | none lower than RB4 |

### 3.1 Readback dimensions

`RB1 LOCAL` checks:
- intended delta exists;
- unintended local delta absent;
- carrier/source link intact.

`RB2 DEPENDENCY` additionally checks:
- direct typed consumers;
- derived artifacts;
- requirement/claim/evidence bindings that consume the change.

`RB3 INTEGRATION` additionally checks:
- interface maturity/disposition;
- shared-variable agreement;
- cross-discipline assembled behaviour;
- integration receipt validity.

`RB4 AUTHORITY` additionally checks:
- Current pointer/identity;
- baseline/configuration lineage;
- promotion state;
- Notion/GitHub/Drive or other required cross-platform authority drift.

### 3.2 Mandatory expansion rules

- unknown material blast radius: expand one level until bounded; if still unknown, HOLD;
- any mutation of `change_authority`, `decision_authority`, `canonical_id`, `Current baseline pointer`, `promotion policy`, or `claim-ceiling contract`: RB4;
- any `TIGHTLY_COUPLED` interface affected: at least RB3;
- any `PROMOTION_BREAKING` change: RB4 + rerun affected required assurance;
- purely visual/local success never closes a field/technical/professional obligation.

---

## 4. Staleness Propagation Matrix

Staleness has a trigger, typed propagation path, consequence, and recovery obligation.

| Trigger | First-order affected objects | Typical second-order propagation | Minimum consequence | Minimum recovery |
|---|---|---|---|---|
| Root/Project Authority changed | snapshots, packets, Project State | decisions, promotion states, routes | `REOPEN_REQUIRED` | RB4 authority refresh |
| Current baseline superseded | baseline-bound artifacts/evidence/assurance | claims, decisions, presentation releases | `RECHECK_REQUIRED` to `INVALIDATED` | affected graph + new baseline readback |
| Controlled variable changed | consumers + interfaces | artifacts, decisions, assurance, claims | `REOPEN_REQUIRED` | RB3; RB4 if baseline pointer changes |
| Requirement changed | satisfying system elements + verification | decisions, interfaces, claims | old PASS historical | re-verification on new requirement configuration |
| Constraint/mandate changed | all in-scope compliant objects | baseline/promotion/professional state | `REOPEN_REQUIRED` | applicability + impact + assurance |
| Interface reopened | both sides + integration receipts | dependent artifacts/claims | `REOPEN_REQUIRED` | integrated readback |
| Evidence rejected/contradicted | claims/assurance decisions using it | decisions/promotion/presentation proof | `INVALIDATED` where material | evidence review + replacement/retest |
| Major assumption refuted/expired | all `depends_on` objects | decisions, claims, baseline candidate | `REOPEN_REQUIRED` | reframe/retest/contain |
| Unknown resolves adversely | dependent scope | claim ceiling + decision | bounded reopen | update scope/decision/claim ceiling |
| Software/instrument/model version materially changes | reproducibility-sensitive evidence/receipts | technical claims | `RECHECK_REQUIRED` | compatibility/reproduction test |
| Review/verification due expires | mutable knowledge/evidence | retrieval/promotion eligibility | `RECHECK_REQUIRED` | freshness review |
| Presentation source revision changes | evidence projections/releases | audience claims | presentation stale | regenerate/re-read presentation; no upstream truth change |

### 4.1 Consequence assignment

- `INFORMATIONAL`: no material validity effect.
- `RECHECK_REQUIRED`: usable for bounded work, but cannot support next promotion until rechecked.
- `REOPEN_REQUIRED`: prior closure no longer sufficient.
- `INVALIDATED`: cannot support Current claim for affected scope.

Staleness must never be propagated merely because timestamps differ; a material semantic dependency is required.

---

## 5. Claim-Ceiling Crosswalk

Claim ceilings are vectors. The table below gives **maximum default ceilings**, never automatic grants.

| Evidence / execution basis | Execution | Evidence | Technical | Field / operational | Design quality | Professional/compliance |
|---|---|---|---|---|---|---|
| file exists / script ran | `EXECUTED` | `NO_EVIDENCE` or `CONTEXTUAL` | `UNCHECKED` | `NOT_FIELD` | `UNASSESSED` | `OPEN` |
| reopened carrier/readback | `READBACK_CONFIRMED` | `CONTEXTUAL` | `UNCHECKED` | `NOT_FIELD` | `UNASSESSED` unless review | `OPEN` |
| authoritative document/source | `READBACK_CONFIRMED` | up to `DIRECT_BOUNDED` for sourced proposition | depends on proposition | `NOT_FIELD` unless field source | `UNASSESSED` | does not self-grant acceptance |
| simulation/model calculation | `READBACK_CONFIRMED` | up to `DIRECT_BOUNDED` for modeled question | up to `VERIFIED_FOR_SCOPE` if method/inputs/criteria adequate | `NOT_FIELD` | independent review required for KEEP | `OPEN` unless authority accepts |
| lab/prototype test | `READBACK_CONFIRMED` | up to `DIRECT_BOUNDED` | up to `VERIFIED_FOR_SCOPE` | still `NOT_FIELD` unless field-equivalent scope is explicitly established | independent review required | `OPEN` unless applicable authority accepts |
| field observation | `READBACK_CONFIRMED` | up to `DIRECT_BOUNDED` | bounded | `FIELD_OBSERVED` | independent review required | separate compliance authority still required |
| field measurement | `READBACK_CONFIRMED` | up to `ASSURED_FOR_SCOPE` | bounded by method/calibration | `FIELD_MEASURED` | independent review required | separate authority required |
| in-use/user operation validation | `READBACK_CONFIRMED` | up to `ASSURED_FOR_SCOPE` | bounded | `IN_USE_VALIDATED` for stated scenario/population | independent review required | separate authority required |
| independent design review | no execution upgrade by itself | no evidence upgrade by itself | no technical upgrade by itself | no field upgrade | may grant `KEEP_SUPPORT/KEEP_MAIN` | not legal/professional approval by itself |
| licensed/professional acceptance | no execution upgrade by itself | evidence still separately bounded | may accept technical/compliance scope | field remains separate | design quality remains separate | `ACCEPTED_BY_AUTHORITY` for explicit scope only |

Hard rule: no row allows a lower dimension to infer a stronger unrelated dimension.

---

## 6. Promotion Authority Matrix

| Promotion target | Minimum promoter authority | Required basis | Cannot be promoted by |
|---|---|---|---|
| Project design `CANDIDATE → PROMOTED` | Project `DECISION_AUTHORITY` | relevant review/gates + readback | executor alone, CI, presentation owner |
| Project design `PROMOTED → LOCKED` | Decision + `CONFIG_AUTHORITY` where configuration-controlled | Change/reopen path + baseline binding | visual reviewer alone |
| Requirement `AGREED → BASELINED` | requirement/change authority | provenance + acceptance/verification route | artifact author |
| Requirement `→ VERIFIED` | Assurance decision authority | verification activity + accepted evidence per target | requirement author alone |
| Interface `→ CLOSED` | integration owner + applicable acceptance authority | required maturity + acceptance contract/readback | either side unilaterally for MAJOR/CRITICAL |
| Baseline `APPROVED → CURRENT` | `CONFIG_AUTHORITY` | included revisions/hashes + approval + RB4 pointer readback | newest artifact |
| Evidence `CHECKED → ACCEPTED_FOR_USE` | evidence reviewer/authority for method | provenance/method/conditions/uncertainty | claimant alone where independence is required |
| Runtime Control `→ CURRENT_FOR_EXECUTION` | runtime owner under valid Authority Snapshot | snapshot validity + dependencies | receipt author if source refs stale |
| Knowledge Candidate `→ CURRENT` | Knowledge governance/promotion authority | classification + R1/R2/K1-K5/B1/IR as applicable | project success/G9 receipt alone |
| Presentation `→ RELEASED/KEEP_FOR_AUDIENCE` | release/presentation review authority | source binding + target-condition readback | cannot promote Project/Knowledge truth |
| Professional/compliance acceptance | authorized external/professional authority where required | scoped submission/evidence | automated validator or design reviewer |

Promotion creates no stronger state than the weakest applicable material dependency and claim ceiling.

---

## 7. Invocation Validity Matrix

An invocation is valid only when every required row is `PASS`.

| Check | PASS | HOLD/REJECT |
|---|---|---|
| Identity | one stable target logical object | collision/unresolved duplicate |
| Authority Snapshot | verified and fingerprint-current | stale/missing material source |
| Scope | target + scope_in/out explicit | implicit/widening scope |
| Mutation | requested class within budget | exceeds budget without Change/escalation |
| Protected objects | no unauthorized rewrite | lower-authority mutation attempted |
| Baseline | correct configuration identified | latest-file assumption / mismatch |
| Dependencies | material blockers classified | unknown material dependency graph |
| Evidence obligation | required proof named | result expected without proof route |
| Readback | minimum RB level declared | write success treated as validation |
| Claim target | explicit | vague “done/pass/approved” |
| Claim ceiling | vector present and sufficient | cross-ceiling promotion |
| Stop/Reopen | triggers explicit | no legal failure/reopen path |

---

## 8. Validator additions for P1 v1.1

- `P1/AUTH-M01`: same controlled property cannot have >1 effective authority unless explicit joint-authority contract exists.
- `P1/AUTH-M02`: authority conflicts cannot resolve by timestamp/file version alone.
- `P1/RB-M01`: mutation class maps to minimum readback level.
- `P1/RB-M02`: baseline/current-pointer mutation requires RB4 in addition to semantic dependency readback.
- `P1/STALE-M01`: stale trigger without typed affected-edge set is not closable for material scope.
- `P1/STALE-M02`: stale consequence must be one of INFORMATIONAL/RECHECK_REQUIRED/REOPEN_REQUIRED/INVALIDATED.
- `P1/CLAIM-M01`: evidence source class cannot populate unrelated stronger ceiling dimensions.
- `P1/PROM-M01`: each promoted state must resolve promoter authority class and scope.
- `P1/PROM-M02`: Presentation or Runtime Control promotion cannot raise Project/Knowledge truth.
- `P1/INV-M01`: material invocation missing any Identity/Authority/Scope/Mutation/Readback/Claim check fails closed.

## 9. External calibration boundary

This draft is calibrated against systems/configuration-management practice including ISO/IEC/IEEE 15288 system life-cycle process separation, ISO 10007 responsibilities/authorities + change control/status accounting, and NASA configuration/change-control guidance. External standards calibrate structure; OLEANDER Current Authority remains controlling for OLEANDER semantics.
