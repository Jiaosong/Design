# OLEANDER Real-Project Replay — KH46 v008 — 2026-09-15

Status: **DRAFT REPLAY / SOURCE-BOUNDED / NOT CURRENT**.

Replay target: `R3-B ARCH_BA3 v008 / CIVIC WINTER COMMONS`.

Purpose: test the OLEANDER typed operating-system contracts against a real multidisciplinary design project with mixed geometric, program, interface, support-evidence and professional-review states.

This replay does **not** modify KH46 selected-A geometry, authority or CAD. It uses the latest available project records and marks unavailable facts `NOT_EVALUATED` rather than guessing.

---

## 1. Source-bounded current facts

### Design/source status

- `v008` remains a **WORKING DESIGN CANDIDATE / no authority promotion**.
- Selected A geometry/authority/CAD were explicitly protected during P37 support repair.
- P32 `V008 FIRST BUILD` exists and explicitly did not pre-judge later G1–G6 review.
- Historical v007 SHA guard remains a provenance/configuration guard, not current v008 authority.

### Area/program state

- v008 GFA proxy/current reconciliation basis: `8854 m²`.
- Floor totals recorded in prior closure: `Ground 3730 m² / L2 2576 m² / L3 2548 m²`.
- P36 distinction remained important: geometry-layer area accounted by design rebalance; program/net closure still had open interpretation where source bindings were not explicit.

### Final P37 support evidence

Final P37 result:

`PASS_SUPPORT_ONLY_PROGRAM_OVERLAY`.

Confirmed:

- `29/29` R22 rows represented;
- `72` pieces;
- program-program overlap = `0`;
- no-go overlap = `0`;
- host containment failures = `0`;
- usability/contiguity failures = `0`;
- sports-support = `180 m²`;
- L2/L3 north corridor `[-40,18.1]–[32,20.5]` explicitly represented as no-go;
- carried west corridor `[-30.5,-12]–[-27.5,14]` explicitly represented as `CARRIED_CIRCULATION_INTENT / SUPPORT-NO-GO`;
- selected-A guards unchanged;
- selected A / authority / CAD unchanged.

P37 final hashes:

- MD SHA256: `8D7FADC8EC5C783084CCA92F3A049DEC61FBA3A7AD0CEE473EA92434595CFF1A`;
- generator SHA256 begins `136996703…E16875E`;
- JSON SHA256 begins `A51BDB2C…C93A13D`;
- row CSV SHA256 `6955D551…E32200`;
- pieces CSV SHA256 `827F4668…70E62B`;
- SVG SHA256 `DD5EA21B…8B3F3A`.

Old P37 hashes are superseded provenance.

### P37 does not establish

The final overlay explicitly remains first-order zoning/program evidence only. It does **not** establish:

- sports-hall operational adjacency;
- changing-flow adequacy;
- clean/dirty service logic;
- fire approval;
- accessibility approval;
- shelter/MEP closure;
- daylight/energy performance;
- hydraulics;
- roof-access safety;
- snow/ice operational performance;
- field/in-use validation.

### P38 professional/design review

Latest P38 mixed verdict:

- `G1 REVISE`;
- `G2 REVISE`;
- `G3 REVISE`;
- `G4 PASS`;
- `G5 PASS`;
- `G6 REVISE`.

Therefore P38 is neither a global PASS nor a global FAIL. The project remains a design-quality candidate with material unresolved review obligations.

---

# 2. P0 — Object Plane / Identity replay

## Result

`CONFIRMED`.

The replay clearly distinguishes:

- selected-A design/configuration = `PROJECT` plane;
- P37 overlay artifacts = Project Artifacts/Evidence carriers;
- review receipts/gate state = `RUNTIME_CONTROL`;
- any future reusable lesson = only a G9 candidate until Knowledge admission;
- P37 SVG/CSV/JSON/MD are not independent design authorities.

### Replay-derived hard rule

`SUPPORT ARTIFACT DETAIL/RECENCY MUST NOT REPLACE SELECTED DESIGN IDENTITY/AUTHORITY`.

No P0 contract delta required; add regression coverage.

---

# 3. P1 — Authority / Invocation / Claim Ceiling replay

## Confirmed authority separation

P37 support repair had a deliberately bounded invocation:

- may regenerate support/program evidence;
- may add/repair support no-go definitions;
- must not alter selected-A geometry;
- must not promote authority;
- must not touch CAD.

This is an actual example of:

`CROSS_OBJECT_COORDINATION_EDIT` on support objects **without** `CONFIGURATION_CHANGE` to selected-A design authority.

## Claim-ceiling replay

P37 can raise the bounded evidence ceiling for:

- row representation;
- area accounting of represented pieces;
- overlap/no-go/containment checks;
- connected first-order sports-support zoning fit.

It cannot raise:

- design-quality ceiling;
- technical/professional ceiling;
- field/operational ceiling;
- selected-A authority status.

### Result

`CONFIRMED_BOUNDED`.

### Validator delta

Add a cross-axis rule:

`P1/CLAIM-RP01 SUPPORT_EVIDENCE_PASS_CANNOT_RAISE_DESIGN_AUTHORITY_OR_PROFESSIONAL_CEILING`.

---

# 4. P2 — Project State / Decision replay

## Key distinction

The support-overlay decision and the architectural design-quality decision are different decision objects.

A valid bounded question for P37 is:

`Does the support-only program overlay represent all required rows/pieces while respecting defined no-go corridors, host containment and area constraints without altering selected-A authority?`

A different P38 question is:

`Does the current v008 selected-A candidate achieve the professional/design-quality criteria required by G1–G6?`

P37 PASS cannot close P38.

## Local versus global state

P38 `G1/G2/G3/G6 REVISE` creates material work/review obligations but does not automatically mean project-wide Authority HOLD.

### Result

`CONFIRMED`.

### Validator delta

`P2/DECQ-RP01 SUPPORT_DECISION_CLOSURE_CANNOT_CLOSE_PARENT_DESIGN_QUALITY_DECISION`.

---

# 5. P3 — Need / Requirement / Constraint / Project Claim replay

The available replay record contains strong program and no-go constraints but does not expose a complete canonical Requirement set with formal source/acceptance/verification fields for every item.

Therefore:

- do **not** manufacture formal Requirements from program rows alone;
- represent the explicit P37 test conditions as bounded support constraints/acceptance conditions;
- keep professional OPEN items as OPEN unless a requirement/assurance target is explicitly present.

## Result

`CONFIRMED_BOUNDED / PARTIALLY_NOT_EVALUATED`.

### Important replay lesson

A validator must allow real legacy/current projects to enter replay with incomplete typed Requirement migration without either:

- pretending requirements exist; or
- globally failing the project merely because the new schema is not yet backfilled.

### Validator delta

`P3/MIG-RP01 MISSING_TYPED_REQUIREMENT_MIGRATION_IS_NOT_AUTOMATIC_PROJECT_FAILURE; CONSEQUENTIAL_PROMOTION_REQUIRING_THAT_REQUIREMENT_REMAINS_HOLD/NOT_EVALUATED`.

This separates migration debt from project failure.

---

# 6. P4 — Controlled Variable / Interface replay

## Strongly represented variables/constraints

- north corridor no-go geometry;
- carried west corridor support-no-go geometry;
- piece areas;
- program placement/containment;
- sports-support `180 m²`;
- floor-total/GFA accounting.

## P37 closure scope

P37 demonstrates:

- geometric support-overlay fit;
- zero registered overlap against current no-go definition;
- containment;
- represented-area consistency;
- first-order sports-support zoning connection.

It explicitly does **not** demonstrate:

- operational adjacency quality;
- changing sequence/flow;
- clean/dirty circulation/service separation.

These are separate Interface/behavior questions.

## Result

`CONFIRMED`.

### Major replay-derived rule

One Interface may require multiple acceptance dimensions. Closure of geometry/clearance dimension cannot silently close operational/service dimensions.

Add:

`P4/IFC-RP01 INTERFACE_ACCEPTANCE_IS_DIMENSIONAL; ONE_ACCEPTANCE_DIMENSION_PASS_CANNOT_CLOSE_OTHER_MATERIAL_DIMENSIONS`.

This is stronger than a generic per-target rule because the same logical interface can carry multiple acceptance dimensions.

---

# 7. P5 — Baseline / Change / Staleness replay

## Configuration distinction

P37 support repairs regenerated support evidence while explicitly preserving selected-A geometry/authority/CAD.

Therefore:

- support artifact hashes changed;
- old support hashes became superseded provenance;
- selected design authority did not change;
- selected-A guards remained unchanged.

The typed system must not infer `DESIGN CONFIGURATION CHANGE` from every changed artifact hash.

## Result

`CONFIRMED`, with one refinement.

### Validator delta

Add:

`P5/CHG-RP01 DERIVATIVE_OR_SUPPORT_ARTIFACT_CHANGE_DOES_NOT_STALE_UPSTREAM_SOURCE_CONFIGURATION_UNLESS_SEMANTIC_SOURCE_PROPERTY_CHANGED`.

And:

`P5/STALE-RP02 SUPERSEDED_SUPPORT_HASH_INVALIDATES_OLD_SUPPORT_RECEIPT_FOR_CURRENT_SUPPORT_CLAIM_BUT_NOT_UNCHANGED_SOURCE_DESIGN`.

This prevents over-propagation.

---

# 8. P6 — Evidence / Formal Assurance replay

This case strongly confirms the three-layer evidence model.

### Evidence Records

P37 row/piece/overlap/containment/no-go outputs.

### Assurance Activity

Independent checks against program/no-go/containment criteria and later P38 G1–G6 review.

### Assurance Decisions

- P37: `PASS_SUPPORT_ONLY_PROGRAM_OVERLAY`;
- P38: mixed `REVISE/PASS` per gate.

## Critical aggregation lesson

`G1 REVISE / G2 REVISE / G3 REVISE / G4 PASS / G5 PASS / G6 REVISE`

must remain a vector of per-target dispositions.

A summary may say `DESIGN QUALITY NOT YET KEEP`, but may not rewrite the two PASS gates as FAIL or the four REVISE gates as global FAIL.

## Result

`CONFIRMED`.

### Validator deltas

- `P6/ASR-RP01 MIXED_ASSURANCE_RESULTS_REQUIRE_PER_TARGET_PRESERVATION`;
- `P6/ASR-RP02 SUMMARY_DISPOSITION_MUST_BE_DERIVED_BY_EXPLICIT_AGGREGATION_POLICY_AND_PRESERVE_SUBTARGET_RESULTS`;
- `P6/EVD-RP03 SUPPORT_ONLY_GEOMETRIC_EVIDENCE_MUST_RECORD_DOES_NOT_ESTABLISH_OPERATIONAL_OR_PROFESSIONAL_CLAIMS`.

---

# 9. P7 — Risk / Issue / Assumption / Unknown replay

The project record explicitly keeps several matters OPEN.

However, replay evidence is insufficient to classify every OPEN item as Risk, Issue, Assumption or Unknown.

Examples:

- sports-hall operational adjacency OPEN;
- changing-flow OPEN;
- clean/dirty service OPEN;
- fire/accessibility/MEP/daylight/energy/hydraulics/roof/snow-ice professional OPENs.

## Result

`CONFIRMED_BOUNDED`.

### Replay-derived rule

`OPEN` is not itself a semantic class.

A legacy/project OPEN item may stay `UNCLASSIFIED_OPEN / MIGRATION_OR_REVIEW_REQUIRED` until evidence supports Risk/Issue/Assumption/Unknown classification.

Add:

`P7/OPEN-RP01 OPEN_STATUS_WITHOUT_SUFFICIENT_SEMANTIC_EVIDENCE_MUST_NOT_BE_FORCED_INTO_RISK_ISSUE_ASSUMPTION_OR_UNKNOWN`.

This avoids false certainty introduced by migration.

---

# 10. P8 — Work / Artifact / Carrier replay

P37 has multiple physical carriers:

- generator;
- JSON;
- row CSV;
- pieces CSV;
- SVG;
- Markdown receipt/report.

They share one bounded semantic responsibility: support-only program-overlay evidence.

## Result

`CONFIRMED`, with an over-objectification warning.

### Over-modeling signal

Do not automatically create six independent semantic Project objects merely because six files/hashes exist.

Preferred representation:

- one support evidence/analysis object;
- several Artifact carriers/components with hashes and roles;
- one readback/assurance lineage.

Add:

`P8/ART-RP01 MULTI_FILE_SUPPORT_PACKAGE_MAY_SHARE_ONE_SEMANTIC_EVIDENCE_RESPONSIBILITY; FILE_COUNT_DOES_NOT_DEFINE_OBJECT_COUNT`.

---

# 11. P9 — Knowledge Admission replay

Potential reusable learning exists, but this replay does not promote it.

Possible G9 candidates include:

- support-only evidence must not promote source design authority;
- interface acceptance should preserve multiple acceptance dimensions;
- derivative/support artifact changes should not automatically stale unchanged upstream source configuration;
- mixed assurance outcomes must remain per-target.

These are candidates because they generalize beyond KH46, but require de-project wording and integration with existing OLEANDER contracts before Knowledge promotion.

## Result

`G9_CANDIDATE_ONLY`.

---

# 12. P10 — Presentation replay

The P37 SVG is a support evidence projection, not evidence that the overall architectural presentation or design quality is KEEP.

No project-wide P10 Style/Profile promotion is inferred from this support SVG.

## Result

`NOT_EVALUATED_FOR_PROJECT_PRESENTATION_QUALITY`.

Rule confirmed:

`TECHNICAL_SUPPORT_VISUAL_PASS ≠ PRESENTATION_KEEP ≠ PROJECT_DESIGN_KEEP`.

---

# 13. P11 — Reader / Routing replay

A correct Reader must be able to return simultaneously:

### Question A
“Is the final P37 program overlay internally valid for its bounded support claim?”

Answer state:
`YES — PASS_SUPPORT_ONLY_PROGRAM_OVERLAY`, with 29/29 rows, 72 pieces, zero program/no-go/host/usability failures, 180 m² sports-support and explicit no-go corridors.

### Question B
“Is v008 professionally/design-quality approved?”

Answer state:
`NO — not yet`; latest P38 remains `G1/G2/G3/G6 REVISE`, `G4/G5 PASS`, with no authority promotion.

The same project can therefore contain a strong bounded evidence PASS and an unresolved design-quality state without contradiction.

## Result

`CONFIRMED`.

Add:

`P11/READ-RP01 READER_MUST_PRESERVE_DIFFERENT_SCOPE_RESULTS_INSTEAD_OF_SYNTHESIZING_SINGLE_PROJECT_PASS_FAIL_BADGE`.

---

# 14. Replay findings summary

## False positives prevented

The current model correctly avoids:

- treating newer P37 support files as selected-A authority;
- treating support overlap PASS as design KEEP;
- treating P38 mixed verdict as global PASS;
- treating every OPEN as a Risk;
- treating six support files as six semantic truths.

## False-negative / under-modeling findings

Refinements required:

1. Interface acceptance needs explicit **acceptance dimensions**.
2. Legacy/open typed-migration debt needs a legal `UNCLASSIFIED_OPEN / NOT_EVALUATED` path without false project failure.
3. Support/derivative artifact change needs an explicit **non-upstream-staling rule**.
4. Mixed assurance needs explicit aggregation policy with preserved subtarget results.
5. Reader requires scoped-result presentation instead of one project PASS badge.
6. File count must not drive semantic object count.

## Over-modeling findings

Potential over-modeling occurs if:

- every support file becomes a semantic object;
- every professional OPEN is forced into Risk/Issue/Assumption/Unknown before classification evidence exists;
- every changed derivative hash is treated as configuration change.

---

# 15. Contract deltas to compile

Replay-derived rule candidates:

- `P1/CLAIM-RP01` support evidence PASS cannot raise design/professional/source-authority ceilings;
- `P2/DECQ-RP01` support decision closure cannot close parent design-quality decision;
- `P3/MIG-RP01` missing typed Requirement migration is not automatic project failure; affected promotion may remain HOLD/NOT_EVALUATED;
- `P4/IFC-RP01` interface acceptance is dimensional;
- `P5/CHG-RP01` derivative/support artifact change does not stale unchanged upstream source truth;
- `P5/STALE-RP02` superseded support evidence invalidates old support claim only within affected scope;
- `P6/ASR-RP01` mixed results preserve per-target disposition;
- `P6/ASR-RP02` global summary requires explicit aggregation policy;
- `P6/EVD-RP03` support geometry evidence records operational/professional non-establishment;
- `P7/OPEN-RP01` generic OPEN cannot be force-classified without semantic evidence;
- `P8/ART-RP01` file count does not define semantic object count;
- `P11/READ-RP01` Reader preserves scoped results and cannot synthesize one project PASS badge.

---

# 16. Replay disposition

`REAL_PROJECT_REPLAY_P0_P8 = FIRST_PASS_COMPLETE_WITH_DELTAS`.

`P9 = G9_CANDIDATES_ONLY`.

`P10 = PROJECT_PRESENTATION_NOT_EVALUATED`.

`P11 = READER_SEMANTICS_CONFIRMED_WITH_DELTA`.

This replay does not justify Current promotion. It justifies adding the replay-derived deltas to validator/regression contracts and then replaying another project/domain before governance promotion.