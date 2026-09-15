# OLEANDER Typed System Real-Project Replay Protocol v0.1

Status: **DRAFT REPLAY PROTOCOL / NOT CURRENT**.

This protocol is the next refinement stage after P0–P11 second-pass specification and validator compilation. It does not add a new semantic layer. It tests whether the current typed model survives a real complex multidisciplinary project without false promotion, false blocking, over-objectification, or hidden semantic collapse.

## 1. Purpose

A detailed schema is not proven merely because its internal definitions are coherent.

Replay asks:

1. Can a real project be represented without inventing facts?
2. Do P0–P11 rules classify real records correctly?
3. Do hard failures occur where they should?
4. Do local failures remain local when propagation is bounded?
5. Do support/readback artifacts remain below design/source authority?
6. Are Verification, Validation, design review, technical review and presentation review kept distinct?
7. Does change propagation reopen exactly the objects actually affected?
8. Does the system avoid turning OPEN professional questions into false HOLD or false PASS?
9. Can a practitioner understand the resulting model without excessive bookkeeping?
10. Can the same model later support machine validation without reinterpreting project truth?

Core invariant:

`SPECIFICATION QUALITY ≠ REAL-PROJECT FITNESS`.

A contract becomes promotion-eligible only after replay exposes and resolves material false positives, false negatives, semantic gaps and over-modeling.

---

## 2. Replay order

Replay follows the same prerequisite order as validator compilation:

`P0 IDENTITY/PLANE → P1 AUTHORITY → P2 ACTIVE DECISION/STATE → P3 REQUIREMENTS/CLAIMS → P4 VARIABLES/INTERFACES → P5 CONFIGURATION/CHANGE → P6 EVIDENCE/ASSURANCE → P7 RISK/ISSUE/ASSUMPTION/UNKNOWN → P8 WORK/ARTIFACT → P9 KNOWLEDGE ADMISSION → P10 PRESENTATION → P11 RETRIEVAL/READER`.

Do not begin with presentation or artifact counts and then infer upstream project truth.

---

## 3. Replay case admission

A representative replay case should contain, where available:

- a real Project identity and Project State;
- at least one candidate/current design configuration;
- locked/protected/open objects;
- one or more Requirements/Constraints;
- at least one shared variable or Interface;
- at least one material Change or repair cycle;
- actual Evidence/Readback;
- mixed PASS/REVISE/OPEN outcomes;
- at least one unresolved professional boundary;
- editable/master plus derivative artifacts;
- actual provenance/hashes or revision IDs;
- no requirement to fabricate missing records.

A case with only clean final PASS data is insufficient because it does not test reopen, contradiction, bounded promotion or uncertainty handling.

---

## 4. Replay evidence policy

Use only source-supported project facts.

For every replay fact, classify:

- `OBSERVED_FROM_CURRENT_PROJECT_RECORD`;
- `SUPPORTED_BY_PROJECT_RECEIPT`;
- `SUPPORTED_BY_ARTIFACT_HASH_OR_READBACK`;
- `HISTORICAL_ONLY`;
- `NOT_EVALUATED`;
- `UNKNOWN`.

Do not convert missing replay inputs into assumptions unless the source project itself explicitly used an assumption.

`NOT_EVALUATED ≠ FAIL`.

`UNKNOWN ≠ ASSUMPTION`.

---

## 5. Replay output record

Each replay case records:

```yaml
replay_id:
project_id:
case_name:
as_of:
source_scope:
source_authority_state:
selected_configuration:
known_baselines: []
known_locked_objects: []
known_open_objects: []
known_protected_objects: []
known_requirements: []
known_constraints: []
known_variables: []
known_interfaces: []
known_changes: []
known_evidence: []
known_assurance: []
known_uncertainty_problem_objects: []
known_artifacts: []
known_presentation: []
replay_results:
  P0: []
  P1: []
  P2: []
  P3: []
  P4: []
  P5: []
  P6: []
  P7: []
  P8: []
  P9: []
  P10: []
  P11: []
false_positives: []
false_negatives: []
overmodeling_signals: []
missing_semantics: []
contract_deltas: []
validator_deltas: []
promotion_effect:
```

---

## 6. Replay result vocabulary

For each rule/check use:

- `CONFIRMED` — the typed model represents the real condition correctly;
- `CONFIRMED_BOUNDED` — correct only with explicit scope/boundary;
- `FALSE_POSITIVE` — validator/model would block or downgrade a legitimate real condition;
- `FALSE_NEGATIVE` — validator/model would permit/promote an illegitimate real condition;
- `OVERMODELED` — requires independent object/state where project reality does not justify lifecycle/audit burden;
- `UNDERMODELED` — real project distinction is materially lost;
- `NOT_EVALUATED` — source data insufficient;
- `OPEN_DELTA` — model requires refinement before promotion.

---

## 7. P0 replay questions

- Is the record Knowledge, Project or Runtime Control?
- Does one stable object identity survive file/version/classification changes?
- Are support overlays/receipts prevented from replacing source design identity?
- Does a working candidate remain distinct from promoted authority?
- Are historical/superseded versions retained without competing as Current?

Critical replay failure:

`SUPPORT / RECEIPT / DERIVATIVE becomes source authority merely because it is newer or more detailed`.

---

## 8. P1 replay questions

Test:

- exact authority for geometry, project decision, support evidence and promotion;
- protected-object behavior;
- mutation class;
- readback level;
- stale triggers;
- claim ceiling vector;
- promotion authority.

Required attack:

A support artifact may PASS its bounded check while design authority remains unchanged.

Expected:

`support PASS → bounded evidence ceiling increase only`.

Forbidden:

`support PASS → selected design becomes promoted authority`.

---

## 9. P2 replay questions

Test:

- Project/Workstream ACTIVE/BLOCKED/HOLD separation;
- Decision Question boundedness;
- Locked/Open/Protected sets;
- local repair versus authority-changing redesign;
- Design State versus Assurance State;
- Decision closure only after required implementation/readback.

A local `REVISE` must not automatically make the whole project `HOLD` unless propagation reaches project-critical authority/baseline/claim.

---

## 10. P3 replay questions

Where explicit Requirements exist, test:

- source/derivation;
- atomicity;
- acceptance criteria;
- verification route;
- version/configuration;
- claim type/evidence ceiling.

Where a project record contains only design/program intent and no formal Requirement object, replay must record `NOT_EVALUATED` rather than manufacture a Requirement.

---

## 11. P4 replay questions

Test:

- shared-variable authority;
- no-go/clearance/corridor/area variables;
- pairwise versus N-way interface representation;
- criticality versus coupling;
- maturity versus disposition;
- host containment;
- acceptance contract;
- integrated readback.

Important distinction:

`first-order geometric/program fit ≠ operational adjacency / circulation / clean-dirty / in-use validation`.

A P4 PASS may be valid for one interface question while another interface question remains OPEN.

---

## 12. P5 replay questions

Test:

- historical baseline versus working candidate;
- source configuration fingerprints;
- whether a support-only overlay changes source configuration;
- local repair impact set;
- evidence carry-forward;
- old hashes superseded without deleting lineage;
- rollback/guard preservation.

Critical replay check:

If selected geometry/authority is unchanged while support data is regenerated, P5 must not falsely infer a design configuration change.

---

## 13. P6 replay questions

Test:

- Evidence Record versus Assurance Activity versus Assurance Decision;
- result per target;
- mixed PASS/REVISE aggregation;
- `does_not_establish`;
- geometric/program evidence versus design-quality evidence;
- field/operational ceiling.

Mixed gates must remain mixed.

`G4 PASS + G5 PASS + G1/G2/G3/G6 REVISE` cannot be collapsed to global PASS or global FAIL without an explicit higher-level aggregation rule.

---

## 14. P7 replay questions

Any unresolved professional or operational question must be classified only if the project record supports a Risk, Issue, Assumption or Unknown.

Examples:

- operational adjacency not yet demonstrated;
- changing-flow not yet demonstrated;
- clean/dirty service logic not yet demonstrated;
- fire/accessibility/MEP/daylight/energy/hydraulics/roof/snow-ice remain professionally OPEN.

Do not invent risk likelihood/severity when project records only state OPEN.

---

## 15. P8 replay questions

Test:

- editable source/master;
- support generator/data/SVG/CSV/MD roles;
- derivative lineage;
- hashes;
- acceptance/readback;
- whether one support package should be one Artifact or several linked Artifacts.

Over-objectification signal:

If every CSV/JSON/SVG is promoted into a separate semantic project object despite sharing one support evidence responsibility, use Artifact subcarriers/components rather than semantic object explosion.

---

## 16. P9 replay questions

Do not distill reusable Knowledge merely because replay reveals a successful project repair.

A project-specific rule such as a corridor/no-go coordinate remains Project truth until de-project/generalization establishes reuse.

Potential reusable learning may become G9 candidate only if it states mechanism, conditions, failure modes and transfer boundary.

---

## 17. P10 replay questions

Use actual readbacks/presentation only when source project evidence exists.

No presentation-quality inference from support-overlay SVG or technical diagram correctness alone.

Presentation can show support evidence but cannot raise selected-design authority or field/professional ceiling.

---

## 18. P11 replay questions

Reader/Agent must return:

- selected design/source status;
- support overlay status;
- mixed gate results;
- superseded hashes as provenance;
- unresolved professional OPENs;
- no false `CURRENT/PASS` synthesis.

The Reader should be able to answer both:

- “Is the P37 overlay internally valid?”
- “Is v008 professionally/design-quality approved?”

with different, non-contradictory answers.

---

## 19. Replay-driven contract refinement rule

A contract change is justified only when replay reveals one of:

- a real semantic distinction missing;
- a rule blocks valid work;
- a rule permits false promotion;
- state/relation granularity is insufficient;
- objectification creates unreasonable maintenance burden;
- two contracts claim the same semantic ownership;
- validator cannot express a necessary bounded result.

Do not change contracts simply to make a replay case PASS.

---

## 20. Promotion readiness after replay

Replay completion is not promotion.

A draft contract set becomes promotion-review eligible only after:

1. at least one real multidisciplinary project replay covers P0–P8;
2. one Knowledge-object/corpus replay covers P9/P11;
3. one Presentation target-condition replay covers P10;
4. material false positives/negatives are repaired;
5. regression corpus is updated with replay-derived cases;
6. migration impact is known;
7. independent governance review occurs;
8. explicit Current promotion/readback is authorized.