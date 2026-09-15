# OLEANDER Typed System Validator Contract v0.1

Status: **DRAFT VALIDATOR COMPILATION / NOT CURRENT**. Compiles the Object Plane architecture, Integration Manifest, second-pass binding and P1–P11 machine contracts into one validation order. It does not replace semantic owner documents and cannot self-promote any Project/Knowledge/Presentation object.

## 1. Compiler principle

Validation follows prerequisite consequence order:

`P0 IDENTITY/PLANE → P1 AUTHORITY/SCOPE → P2 DECISION/STATE → P3 OBLIGATION/CLAIM → P4 INTERFACE/VARIABLE → P5 CONFIG/CHANGE → P6 EVIDENCE/ASSURANCE → P7 UNCERTAINTY/ISSUE → P8 WORK/CARRIER → P9 KNOWLEDGE ADMISSION → P10 PRESENTATION → P11 RETRIEVAL/ROUTING`.

A later PASS never cancels an earlier hard failure.

Examples:
- P10 visual readback cannot repair P3 unauthorized Requirement;
- P11 relevance cannot override P1 authority conflict;
- P6 strong evidence cannot remain Current when P5 says configuration mismatch invalidates applicability;
- P9 content quality cannot create reusable Knowledge from unresolved Project provenance.

## 2. Validator outcomes

Use:
- `PASS` — machine-verifiable invariant satisfied;
- `FAIL` — hard invariant violated;
- `HOLD` — required authority/evidence/identity fact unresolved; do not guess;
- `REVIEW_SIGNAL` — machine detects condition requiring human/domain judgment;
- `NOT_APPLICABLE` — rule semantically inapplicable;
- `NOT_EVALUATED` — required input was not available.

`NOT_EVALUATED ≠ PASS`.

## 3. Severity

- `S0 INFO` — informational/no promotion effect;
- `S1 REVIEW` — review needed before next material promotion;
- `S2 MATERIAL` — affected object cannot close/promote until resolved;
- `S3 MAJOR` — multiple objects/interfaces/claims may be invalid; mandatory reopen/impact review;
- `S4 CRITICAL` — authority/safety/legal/core truth corruption risk; fail closed / project HOLD where propagation is project-critical.

Severity and semantic class remain separate.

## 4. Rule record

```yaml
rule_id:
priority:
semantic_owner:
second_pass_source:
severity:
automation_mode: HARD_CHECK | STRUCTURAL_CHECK | SIGNAL_ONLY | HUMAN_REQUIRED
target_planes: []
target_object_types: []
prerequisites: []
condition:
pass_condition:
fail_outcome:
hold_condition:
reopen_effect: []
claim_ceiling_effect: []
message_template:
```

## 5. P0 — Identity / Object Plane rules

### `P0/PLANE-001`
Every canonical semantic object resolves exactly one primary Object Plane:
`KNOWLEDGE | PROJECT | RUNTIME_CONTROL`.
Presentation remains projection, not fourth plane.

### `P0/ID-001`
Stable logical identity cannot change merely because classification, Role, Level, carrier or state changes.

### `P0/ID-002`
One logical object cannot have two unresolved `ACTIVE/CURRENT` owners for same semantic responsibility/scope.

### `P0/ID-003`
Register/receipt/view identity cannot replace the Project/Knowledge object it indexes/references.

### `P0/CARRIER-001`
Carrier/file/page identity is not semantic identity unless explicit authority contract says the logical object is the carrier.

P0 failure blocks all downstream semantic validation for affected identity.

## 6. P1 — Authority / Invocation rules

Compile:
- `P1/AUTH-M01` exactly one effective authority per controlled property unless explicit joint-authority contract;
- `P1/AUTH-M02` no latest-timestamp/file-version conflict resolution;
- `P1/RB-M01` mutation class implies minimum readback;
- `P1/RB-M02` Current/baseline/authority pointer mutation requires RB4 as applicable;
- `P1/STALE-M01` material staleness needs typed affected set;
- `P1/STALE-M02` stale consequence in controlled set;
- `P1/CLAIM-M01` no evidence basis may populate unrelated higher claim-ceiling dimension;
- `P1/PROM-M01` promotion resolves promoter authority/scope;
- `P1/PROM-M02` Presentation/Runtime promotion cannot raise Project/Knowledge truth;
- `P1/INV-M01` material invocation requires identity+authority+scope+mutation+readback+claim checks.

P1 `AUTHORITY_CONFLICT` is S4 when same property/scope is material and no delegation/joint contract exists.

## 7. P2 — Project State / Decision rules

Compile:
- `P2/DECQ-M01` consequential Decision Question passes all eight tests;
- `P2/STATE-M01` ACTIVE project has at least one executable Workstream under valid authority;
- `P2/HOLD-M01` local blocker cannot become Project HOLD without project-critical propagation basis;
- `P2/LOCK-M01` same property/scope cannot be LOCKED and OPEN;
- `P2/SCOPE-M01` mutation escalation before higher-class mutation;
- `P2/DEP-M01` OPEN_NONBLOCKING requires claim ceiling + due/reopen trigger;
- `P2/LIFE-M01` DISPOSITIONED does not close consequential cycle before implementation/readback obligations;
- `P2/FORK-M01` alternatives cannot share implicit Current status;
- `P2/MERGE-M01` merged candidate requires new compatibility/readback;
- `P2/LINEAGE-M01` reopen retains prior basis and records invalidated basis;
- `P2/FPRINT-M01` material Project State fingerprint mismatch blocks continuation.

## 8. P3 — Need / Requirement / Constraint / Claim rules

Compile:
- `P3/REQ-M01` baselined consequential Requirement passes R-Q01..R-Q12 applicable gates;
- `P3/REQ-M02` independently pass/fail clauses split;
- `P3/REQ-M03` precedent/reference/AI suggestion alone cannot create mandatory Requirement;
- `P3/ACC-M01` undefined subjective acceptance term blocks baseline until operationalized;
- `P3/CONF-M01` Requirement conflict typed before disposition;
- `P3/WVR-M01` material variance requires authorized Waiver/Deviation/Change;
- `P3/NEED-M01` one user quote cannot self-promote to universal validated Need;
- `P3/CLM-M01` Claim type compatible with evidence + P1 ceilings;
- `P3/CLM-M02` contradiction/bounds retained;
- `P3/TRACE-M01` consequential Requirement resolves origin/realization/assurance/change-impact traces;
- `P3/VERS-M01` semantic Requirement change blocks automatic verification carry-forward.

## 9. P4 — Controlled Variable / Interface rules

Compile:
- `P4/VAR-M01` one effective current change authority per active shared variable unless joint contract;
- `P4/VAR-M02` numerical shared variable has unit + relevant tolerance/reference system before COORDINATED;
- `P4/VAR-M03` configuration-specific values remain scoped;
- `P4/IF-M01` relationship crossing objectification threshold cannot remain generic edge only;
- `P4/IF-M02` N-way relation uses hub or pairwise decomposition with rationale;
- `P4/IF-M03` MAJOR/CRITICAL interface has integration owner + formal acceptance contract;
- `P4/IF-M04` TIGHTLY_COUPLED cannot close without integrated readback;
- `P4/IF-M05` CLOSED requires maturity >= required maturity + zero blocking condition;
- `P4/IF-M06` OUTSIDE_CLAIM != CLOSED;
- `P4/IF-M07` material interface change propagates to consumers/assurance;
- `P4/REG-M01` Interface Register cannot replace Project Interface object.

## 10. P5 — Baseline / Change rules

Compile:
- `P5/CFG-M01` parallel Current same property/scope requires explicit variant applicability key;
- `P5/CFG-M02` rollback uses authorized Change/new Current decision; historical baseline immutable;
- `P5/AUTH-M01` change authority follows changed property/scope, not editor;
- `P5/IMPACT-M01` impact class has minimum affected-set proof + readback;
- `P5/STALE-M01` partial invalidation follows typed consumption/applicability;
- `P5/CARRY-M01` evidence/assurance carry-forward requires applicability decision after target/method/criterion changes;
- `P5/CSA-M01` controlled object exposes configuration status accounting;
- `P5/CONC-M01` non-commuting overlapping Changes cannot run concurrently;
- `P5/ROLL-M01` exact rollback forbidden when newer controlling obligations invalidate old config;
- `P5/REL-M01` Release points to controlling baselines/revisions and does not create design authority.

## 11. P6 — Evidence / Assurance rules

Compile:
- `P6/ADM-M01` accepted evidence passes applicable identity/config/condition/method/uncertainty/provenance gates;
- `P6/ADM-M02` evidence admission is claim-specific;
- `P6/IND-M01` evidence count cannot substitute for independence;
- `P6/APP-M01` cross-context/config transfer has explicit applicability basis;
- `P6/UNC-M01` uncertainty overlapping acceptance threshold blocks unconditional PASS;
- `P6/RDY-M01` Assurance READY requires target/config/method/criteria/authority prerequisites;
- `P6/INDP-M01` required independent assurance cannot be satisfied by self-check;
- `P6/MULTI-M01` per-target results before global summary;
- `P6/CONTRA-M01` true material contradiction blocks strongest ceiling until resolved/bounded;
- `P6/CEIL-M01` Assurance Decision names granted/unchanged/excluded ceiling dimensions.

## 12. P7 — Risk / Issue / Assumption / Unknown rules

Compile:
- `P7/RSK-M01` Risk distinguishes cause/event/consequence;
- `P7/RSK-M02` numeric likelihood has defensible basis;
- `P7/RSK-M03` treatment records effectiveness/residual risk;
- `P7/ISS-M01` Material+ Issue separates containment/root cause/correction/retest;
- `P7/ROOT-M01` root-cause confidence not inferred from repair alone;
- `P7/ANTI-M01` known recurrent failure routes through anti-repeat/drift before new research unless new context;
- `P7/ASM-M01` Assumption passes admission gates;
- `P7/UNK-M01` Unknown→Assumption requires explicit conversion record;
- `P7/LINE-M01` semantic conversion preserves lineage;
- `P7/PROM-M01` Material R/I/A/U maps to promotion/ceiling effect.

## 13. P8 — Work / Artifact / Carrier rules

Compile:
- `P8/WORK-M01` Work acceptance checks outcome/semantic target/outputs/readback/dependencies/interfaces/authority/ceiling/handoff;
- `P8/TASK-M01` trivial tool steps not objectified without traceability need;
- `P8/ART-M01` Artifact state cannot set represented semantic-object state;
- `P8/MASTER-M01` Source Master and Editable Master separately resolvable when different;
- `P8/DER-M01` material derivative records source revision/transformation/loss/readback;
- `P8/LOSS-M01` unknown material conversion loss blocks final handoff/current claim;
- `P8/HAND-M01` cross-software handoff requires downstream reopen/readback;
- `P8/REG-M01` Artifact Register cannot create source authority;
- `P8/DEL-M01` Delivery Package declares controlling baselines/revisions;
- `P8/ACCESS-M01` invalid rights/access/dependency can block deliverability;
- `P8/REWORK-M01` derivative regeneration cannot substitute for upstream semantic repair.

## 14. P9 — Knowledge Admission rules

Compile:
- `P9/G9-M01` task/project success cannot create reusable Knowledge identity;
- `P9/OWN-M01` Current owner full body checked before new identity;
- `P9/OWN-M02` compatible learning patches/merges existing owner;
- `P9/DEP-M01` de-project removes runtime clutter while preserving provenance/context;
- `P9/GEN-M01` single case cannot silently generalize to broad Method/Theory;
- `P9/TRF-M01` consequential reusable rule states WHEN/DO-BECAUSE/NOT-BEYOND/REVALIDATE-WHEN;
- `P9/L4-M01` L4 requires all five gates;
- `P9/BODY-M01` operational logs cannot dominate Human Knowledge Body;
- `P9/CLM-M01` consequential Claim has typed support/contradict/bound evidence;
- `P9/GATE-M01` gates independent; genuine N/A legal;
- `P9/STATE-M01` taxonomy/retrieval/content/research/trust/freshness/bilingual/graph states separate;
- `P9/CORPUS-M01` corpus census cannot be fixed completion constant.

## 15. P10 — Presentation rules

Compile:
- `P10/STYLE-M01` profile uses observable axes;
- `P10/STYLE-M02` sparse/minimal cannot delete required proof;
- `P10/STYLE-M03` style cannot raise upstream ceiling;
- `P10/TRUTH-M01` E3 source remains E3 after formatting;
- `P10/TRUTH-M02` evidence transformation preserves source/transform/omission/recoverability;
- `P10/TECH-M01` conflicting technique combinations require bounded rationale/repair;
- `P10/COLOR-M01` color not sole critical carrier;
- `P10/MOTION-M01` motion not sole critical carrier; reduced/static path where nonessential;
- `P10/MED-M01` medium adaptation preserves semantics/source boundary;
- `P10/READ-M01` style Current-for-scope requires target-condition readback;
- `P10/BRAND-M01` presentation cannot invent Brand Authority;
- `P10/SPEC-M01` speculative visual cannot prove field/performance/compliance.

## 16. P11 — Retrieval / Reader / Automation rules

Compile:
- `P11/PLANE-M01` resolve query plane(s) before mixing candidates;
- `P11/POOL-M01` Current/Support/Provenance/Blocked pools separable;
- `P11/RANK-M01` semantic similarity cannot compensate invalid authority/scope/retrieval;
- `P11/RANK-M02` taxonomy height/popularity/citation count not generic truth rank;
- `P11/TRAV-M01` strong inference uses typed relation path;
- `P11/CLAIM-M01` consequential answer bundle preserves source/evidence/config/ceiling;
- `P11/VIEW-M01` Reader view cannot mutate source state;
- `P11/BADGE-M01` state axes not collapsed into one quality badge;
- `P11/CONTRA-M01` contradiction cannot be hidden by rank/summary;
- `P11/STALE-M01` stale reason/allowed-use visible;
- `P11/AUTO-M01` automation cannot self-certify restricted truths;
- `P11/ROUTE-M01` minimum sufficient owner set + legal NO_DEDICATED_OWNER;
- `P11/COV-M01` consequential absence claim reports retrieval coverage;
- `P11/EVAL-M01` regression suite covers minimum scenarios.

## 17. Cross-contract rules

### `INT/001`
No downstream state may exceed P1 Claim Ceiling.

### `INT/002`
P5 configuration invalidation overrides previous P6 evidence/assurance applicability for affected claim.

### `INT/003`
P3 Requirement semantic change triggers P5 impact and P6 re-assurance where material.

### `INT/004`
P4 shared-variable/interface change triggers P5 change propagation.

### `INT/005`
P7 Major/Critical refuted/expired assumption or critical unresolved Unknown triggers P1/P2 reopen/ceiling behavior.

### `INT/006`
P8 Artifact/Delivery state cannot auto-promote P2/P3/P6 semantic states.

### `INT/007`
P9 Knowledge promotion requires admissible provenance/evidence from P1/P5/P6 as applicable.

### `INT/008`
P10 Presentation state cannot modify source plane/classification/claim ceiling.

### `INT/009`
P11 retrieval cannot surface invalidated/blocked evidence as Current support.

### `INT/010`
Any unresolved P0 identity collision or P1 authority conflict fails closed before promotion.

## 18. Machine vs human boundary

Machine validator may enforce structural/hard semantic invariants. It may issue review signals for judgement-heavy conditions. It must not self-award:
- Design KEEP / aesthetic excellence;
- R1/R2 methodological validity;
- professional/legal/certification acceptance;
- B1 semantic bilingual equivalence;
- causal truth;
- field/in-use validity without admitted field evidence;
- stakeholder Need universality;
- L4 semantic sufficiency solely from filled fields.

## 19. Compilation exit

Validator v0.1 is only a contract until it has:
1. machine rule registry;
2. regression cases with expected outcomes;
3. representative real-project replay;
4. Knowledge remediation replay;
5. Presentation/Reader replay;
6. false-positive/false-negative review;
7. independent governance review.

`VALIDATOR CONTRACT EXISTS ≠ VALIDATOR PROVEN`.
