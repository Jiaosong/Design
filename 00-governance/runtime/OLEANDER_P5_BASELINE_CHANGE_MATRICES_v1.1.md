# OLEANDER P5 Baseline / Change / Staleness Matrices v1.1

Status: **DRAFT COMPANION / PRIORITY P5 SECOND PASS**. Semantic owner remains `OLEANDER_BASELINE_CHANGE_STALENESS_PROPAGATION_CONTRACT_v1.0.*`.

## 1. Purpose

P5 second pass makes configuration control explicit enough to distinguish version history, candidate branches, approved baselines, authorized change, stale evidence and historical proof.

Core invariant:

`APPROVED CONFIGURATION + CHANGE AUTHORITY + IMPACT ACCOUNTING + REASSURANCE = CONTROLLED CHANGE`.

---

## 2. Configuration-Control Threshold Matrix

| Object condition | Config-control required? |
|---|---:|
| scratch/exploration artifact with no downstream use | NO |
| Current source authority | YES |
| baselined Requirement/Constraint | YES |
| shared Controlled Variable | YES |
| MAJOR/CRITICAL Interface definition/acceptance contract | YES |
| promoted Decision basis | YES |
| Evidence/Assurance bound to exact configuration | YES for referenced configuration identity |
| release/delivery package | YES |
| presentation derivative only | usually NO; source/release refs still controlled |

Configuration control is semantic, not a requirement to put every file in a heavy CCB process.

---

## 3. Baseline Scope Matrix

| Baseline type | Primary controlled scope | Typical inclusions | Typical exclusions |
|---|---|---|---|
| `PROJECT` | project-wide governance/reference set | Project State, high-level requirements, major claims | transient task outputs |
| `DESIGN` | selected design definition | system elements, decisions, key artifacts | technical test runs unless required |
| `GEOMETRY` | exact spatial/product geometry | model revisions, grids, datums, key dimensions | unrelated content |
| `TECHNICAL` | coordinated technical definition | calculations, details, technical requirements | marketing/presentation variants |
| `DATA` | schema/dataset/config | schema, mappings, controlled datasets | visual derivatives |
| `CONTENT` | canonical content/naming | copy, taxonomy/content IDs | layout-only variants |
| `BRAND_LANGUAGE` | identity/language rules | logo/type/color/tone tokens | project-specific decorative treatment unless controlled |
| `INTEGRATION` | assembled cross-discipline state | interfaces, shared variables, integration evidence | isolated discipline drafts |
| `ASSURANCE_CONFIGURATION` | exact test/verification configuration | target revisions, setup, instruments, parameters | later mutated target |
| `DELIVERY_RELEASE` | issued external package | accepted carriers/manifests/hashes | working sources not included in release |

Scoped baselines may coexist if they do not claim the same controlled property for the same scope/configuration.

---

## 4. Baseline Current/Branch Matrix

| Situation | Legal? | Rule |
|---|---:|---|
| one Current baseline for one controlled property/scope | YES | default |
| multiple candidate baselines | YES | each marked candidate/branch; none silently Current |
| two Current baselines controlling same property/scope | NO by default | requires explicit variant/branch authority and non-overlapping applicability |
| regional/configuration variants | YES | applicability key required |
| rollback to earlier baseline | YES via new authorized Change/current-pointer decision | history remains immutable |
| edit old approved baseline in place | NO | create Change + replacement baseline |

### 4.1 Variant applicability key

Authorized parallel Current variants require explicit discriminator such as:
`region | product_variant | operating_mode | customer_contract | release_channel | experimental_branch`.

Without discriminator, parallel Current = authority conflict.

---

## 5. Change Authority Matrix

Change authority depends on **what property changes**, not who edits the file.

| Changed property | Minimum approval authority |
|---|---|
| local nonsemantic carrier metadata | carrier owner under delegated process |
| Project Requirement | requirement/change authority |
| external Constraint | external/authorized waiver-deviation authority |
| shared Controlled Variable | variable change authority; joint decision if affected owners materially constrain outcome |
| MAJOR/CRITICAL Interface | integration/change authority defined by acceptance contract |
| Current baseline pointer | configuration authority |
| project design selection | decision authority |
| professional/compliance disposition | applicable professional/external authority |
| canonical identity/authority mapping | P1 authority-change owner / governance authority |

NASA configuration/change guidance similarly separates change authority by item/control level and impact rather than treating any editor as approver.

---

## 6. Change Impact Matrix

| Impact class | Minimum affected-set proof | Minimum approval/readback |
|---|---|---|
| `NON_MATERIAL` | prove no semantic/shared/claim/authority change | local owner + RB1 as needed |
| `LOCAL_MATERIAL` | local semantic object + direct consumers checked | object/change authority + RB2 |
| `INTERFACE_MATERIAL` | affected variables/interfaces/both sides | integration/change authority + RB3 |
| `COUPLED_SYSTEM` | multi-interface/system graph bounded | cross-owner decision + RB3, plus affected assurance |
| `PROMOTION_BREAKING` | Current claims/baselines/receipts/releases identified | promotion/config authority + RB4 + re-promotion |

If impact cannot be bounded, approval remains blocked.

---

## 7. Partial Invalidation Matrix

A Change should invalidate only the claim/configuration scope it actually breaks.

| Affected relation | Default validity disposition |
|---|---|
| downstream object consumes changed property directly | `REOPEN_REQUIRED` |
| evidence target/configuration changed materially | `INVALID_FOR_CURRENT_CLAIM` |
| evidence method/source unaffected but applicability uncertain | `RECHECK_REQUIRED` |
| object proven independent of changed property | `CURRENT_VALID` with stop-boundary reason for Major/Critical branch |
| superseded configuration only | `HISTORICAL_ONLY` |
| presentation carrier source changed but underlying truth unchanged | presentation `RECHECK_REQUIRED`; source evidence unchanged |

Avoid both extremes:
- global invalidation of everything;
- local-only invalidation that ignores registered consumers.

---

## 8. Evidence / Assurance Carry-Forward Matrix

| Change condition | Prior evidence usable? | Prior assurance decision usable? |
|---|---:|---:|
| carrier-only nonsemantic change | YES | YES if target configuration identity semantically unchanged |
| formatting/presentation change | source evidence YES | assurance YES; presentation readback separate |
| tolerance/acceptance criterion changed | evidence may remain historical/contextual | NO for new criterion without re-analysis/test |
| geometry/config target changed within previously demonstrated tolerance envelope | CONDITIONAL | applicability review required |
| target changes outside tested envelope | NO for current claim | NO |
| test method changes, target same | old evidence remains historical | new decision depends on method equivalence/acceptance policy |
| requirement version changes materially | old evidence historical | old verification not Current |
| field condition changes materially | lab/model evidence may remain contextual | field/operational decision reopens |

Carry-forward is an explicit applicability decision, never automatic.

---

## 9. Configuration Status Accounting Matrix

For every controlled object/baseline/change, runtime should be able to answer:

- current revision/configuration;
- governing baseline(s);
- pending Changes;
- approved but not implemented Changes;
- implemented but not verified Changes;
- superseded revisions;
- open reassurance obligations;
- validity disposition of dependent evidence/assurance/claims;
- release packages that contain each revision.

Minimum status query outcomes:
`CURRENT | CANDIDATE | PENDING_CHANGE | IMPLEMENTED_UNVERIFIED | SUPERSEDED | HISTORICAL_ONLY | INVALID_FOR_CURRENT_CLAIM`.

A file list alone is not status accounting.

---

## 10. Change Collision / Commutativity Matrix

Two Changes overlap when they touch the same controlled property or one consumes the other's output.

| Relationship | Can run concurrently? |
|---|---:|
| disjoint controlled properties and no dependency | YES |
| same object, independent properties, proven no shared acceptance/claim impact | CONDITIONAL |
| same controlled variable | NO without serial/joint resolution |
| one changes requirement, another changes satisfying design | NO until requirement Change is dispositioned |
| one changes baseline pointer, another edits old-baseline object | NO |
| both affect same Interface acceptance condition | NO without joint impact analysis |
| presentation-only branch vs source edit | MAY proceed, but presentation becomes stale on source revision change |

No last-writer-wins for controlled overlap.

---

## 11. Rollback / Reversion Matrix

Rollback is not deletion of history.

A rollback request must record:
- current baseline;
- target historical baseline/revision;
- why reversion is proposed;
- changes since target baseline;
- which newer Requirements/Constraints/Interfaces make exact rollback impossible;
- new impact assessment;
- approval authority;
- resulting new baseline.

Outcomes:
- `EXACT_REVERSION` — historical configuration is still compatible;
- `REIMPLEMENT_PRIOR_INTENT` — old intent restored using current constraints/configuration;
- `ROLLBACK_REJECTED` — current obligations prevent legal/technical return.

Historical baseline never becomes Current merely by moving a pointer without approval/readback.

---

## 12. Release / Baseline Relation Matrix

A Release is a delivered/issued package; a Baseline is an approved configuration set. They may coincide but are not identical.

| Case | Baseline? | Release? |
|---|---:|---:|
| internal approved geometry config | YES | maybe NO |
| jury PDF exported from approved design | source baseline YES | presentation release YES, but PDF itself does not become design baseline automatically |
| issued construction package | YES for delivery scope | YES |
| temporary review render | usually NO | maybe review release |
| production software/app version | baseline/configuration YES | release YES |

Release manifest must point back to controlling baselines/source revisions.

---

## 13. Validator additions for P5 v1.1

- `P5/CFG-M01`: parallel Current baselines for same property/scope require explicit variant applicability key.
- `P5/CFG-M02`: rollback requires authorized Change and new Current baseline decision; historical baseline remains immutable.
- `P5/AUTH-M01`: change approval authority derives from changed property and scope, not editor identity.
- `P5/IMPACT-M01`: impact class requires minimum affected-set proof and mapped readback burden.
- `P5/STALE-M01`: partial invalidation must follow typed consumption/applicability, not blanket timestamp aging.
- `P5/CARRY-M01`: prior evidence/assurance carry-forward requires explicit applicability decision when target/method/criterion changes.
- `P5/CSA-M01`: controlled object must expose configuration status accounting beyond file listing.
- `P5/CONC-M01`: overlapping non-commuting Changes cannot execute concurrently.
- `P5/ROLL-M01`: exact rollback forbidden when newer controlling requirements/constraints make prior configuration invalid.
- `P5/REL-M01`: Release must identify controlling baseline/source revisions; Release existence does not create design authority.

## 14. External calibration boundary

ISO 10007 treats responsibilities/authorities, configuration identification, change control, status accounting and audit as distinct configuration-management concerns. NASA guidance similarly requires systematic proposal/evaluation/approval/implementation verification and control levels matched to impact. P5 adopts those structural principles while preserving OLEANDER's broader Project/Knowledge/Presentation separation.
