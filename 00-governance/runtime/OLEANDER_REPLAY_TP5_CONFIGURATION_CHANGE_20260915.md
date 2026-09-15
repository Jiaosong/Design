# OLEANDER TP5 Configuration / Change / Staleness Replay — 2026-09-15

Status: **DRAFT MULTI-CASE REPLAY / NOT CURRENT**.

Purpose: stress P5 using source-supported configuration/change cases rather than synthetic state transitions.

Real replay cases:

1. `KH46 v008 / P37` — support-only evidence regeneration while selected-A source geometry/authority/CAD remain unchanged.
2. `Timer Light Basin v3.3` — visualization/calibration iterations while canonical geometry equivalence is explicitly proven and render-profile lock is scoped away from engineering state.

Not available as real executed replay evidence in the searched corpus:

- an actual same-variable concurrent-change collision;
- an actual project rollback execution with before/after readback.

Those remain `NOT_EVALUATED / OPEN`. Governance instructions for rollback exist, but specification is not replay evidence.

---

## 1. Case A — KH46 support-only change

The KH46 replay already established:

- P37 support/program-overlay artifacts were regenerated and their hashes changed;
- old P37 hashes became superseded provenance;
- selected-A geometry remained unchanged;
- selected-A authority remained unchanged;
- CAD remained unchanged;
- selected-A guards remained unchanged;
- the new support overlay could close bounded overlap/containment/program checks without promoting design authority or professional completion.

### P5 consequence

A changed artifact hash is not sufficient evidence that the upstream design configuration changed.

The change must identify **what semantic configuration property changed**.

Preferred change scope:

```yaml
change_scope: SUPPORT_DERIVATIVE_ONLY
changed_properties:
  - SUPPORT_OVERLAY_CONTENT
  - SUPPORT_EVIDENCE_HASHES
unchanged_protected_properties:
  - SELECTED_A_GEOMETRY
  - SELECTED_A_AUTHORITY
  - CAD_SOURCE
  - SELECTED_A_GUARDS
```

### Existing replay rules confirmed

- `P5/CHG-RP01` derivative/support artifact change does not stale unchanged upstream source configuration.
- `P5/STALE-RP02` superseded support hash invalidates old support claim only within affected scope.

---

# 2. Case B — Timer v3.3 visualization/calibration change

Source: `CALIBRATION_REPORT_v3.3.md`.

The calibration was executed in a real browser/WebGL context.

The diffuser iteration chain records:

- Rounds 01–06 rejected;
- Round 07 improved but marginal;
- Round 08 reflection-card change insufficient;
- Round 09 B accepted;
- only studio-light direction/response changed in the accepted round;
- real geometry remained unchanged.

The source also records canonical geometry equivalence:

- canonical source: `assets/pbr/timer_100_pbr.glb`;
- canonical SHA256: `900e02510ab6b2b5176aa3723dba7981700dc79b5f217dbe481844a534ed7c66`;
- calibration subset: `calibration/timer_visual_calibration_subset.glb`;
- subset SHA256: `ad18d9afb489cff1eece609a1e722c5b723872e84c6a96768b0c51a9339d57b2`;
- at `1e-5 mm`, named components have identical triangle surfaces, face counts, bounds and surface areas;
- vertex welding changed indexing only, not visible geometry;
- `VISUALIZATION_State_Light` is a separate presentation layer and not structural evidence.

This creates an important configuration distinction:

```text
SOURCE / ENGINEERING GEOMETRY CONFIGURATION
≠
VISUALIZATION / CALIBRATION CONFIGURATION
≠
BROWSER / RENDER / COLOR PIPELINE CONFIGURATION
```

A visualization configuration may materially change without changing source geometry.

---

# 3. Configuration axis must be explicit

The P5 model currently distinguishes baseline types, but replay shows that change applicability also requires a **configuration axis / controlled property set**.

A source object may participate in multiple simultaneous controlled configurations:

- geometry;
- material/CMF representation;
- lighting/studio;
- camera;
- render/color pipeline;
- evidence package;
- delivery release.

The system must not infer one monolithic configuration fingerprint from every derivative/carrier hash.

### Replay-derived rule

`P5/CFG-RP03 CHANGE_AND_STALENESS_MUST_BE_SCOPED_TO_DECLARED_CONFIGURATION_AXES_OR_CONTROLLED_PROPERTIES; FILE_HASH_CHANGE_ALONE_CANNOT_DEFINE_SOURCE_CONFIGURATION_CHANGE`.

Recommended fields:

```yaml
configuration_axes: []
changed_properties: []
unchanged_protected_properties: []
source_configuration_ref:
derivative_configuration_ref:
```

---

# 4. Equivalence proof as a carry-forward mechanism

Timer shows that two different files/hashes can still be equivalent for a bounded protected property.

The canonical GLB and calibration subset have different hashes but the relevant geometry was demonstrated equivalent under a defined tolerance/test.

Therefore:

`different bytes/hash ≠ different protected semantic property`.

Equivalence must be explicit and claim-scoped.

### Replay-derived rule

`P5/EQV-RP01 EVIDENCE_OR_CONFIGURATION_CARRY_FORWARD_MAY_USE_EXPLICIT_PROTECTED_PROPERTY_EQUIVALENCE_PROOF; HASH_DIFFERENCE_ALONE_NEITHER_INVALIDATES_NOR_PROVES_EQUIVALENCE`.

Minimum equivalence record:

```yaml
equivalence_id:
source_a:
source_b:
protected_properties: []
method:
tolerance_or_criterion:
result:
does_not_establish: []
review_ref:
```

For Timer, the equivalence proof can preserve geometry-related applicability to the calibration subset, but it cannot establish optical/material/manufacturing/user performance.

---

# 5. Lock scope must be explicit

Timer records:

`FINAL HERO / CMF RENDER PROFILE LOCK = LOCKED`.

The source explicitly says this freezes the **photography visualization target**, not the product engineering state.

Therefore a `LOCKED` flag without a property/scope is unsafe.

### Replay-derived rule

`P5/LOCK-RP01 LOCK_STATE_MUST_NAME_THE_CONTROLLED_CONFIGURATION_OR_PROPERTY_SCOPE; A_VISUALIZATION_LOCK_CANNOT_IMPLY_ENGINEERING_OR_SOURCE_LOCK`.

Minimum lock fields:

```yaml
lock_id:
locks_configuration_ref:
locked_properties: []
lock_owner:
lock_basis:
reopen_triggers: []
```

---

# 6. Reopen triggers are configuration-scoped

Timer explicitly defines render-lock reopen triggers:

- approved geometry changes;
- real sample/optical evidence replaces visualization hypotheses;
- browser/render/color pipeline materially changes.

These triggers are heterogeneous and affect different parts of the evidence/configuration graph.

Examples:

### Approved geometry changes

Expected:

- visualization/render profile applicability must be rechecked/reopened;
- geometry-bound evidence may need re-verification;
- unrelated historical calibration records remain provenance.

### Real material/optical evidence arrives

Expected:

- visualization hypotheses and CMF assumptions may be superseded or narrowed;
- source geometry need not be invalidated solely because better optical evidence arrived.

### Render/color pipeline changes

Expected:

- render-profile/browser evidence reopens;
- source CAD/geometry does not automatically reopen.

### Replay-derived rule

`P5/REOPEN-RP01 REOPEN_TRIGGER_PROPAGATION_MUST_FOLLOW_AFFECTED_CONFIGURATION_AND_CLAIM_DEPENDENCIES_NOT_GLOBAL_PROJECT_INVALIDATION`.

---

# 7. Evidence carry-forward is claim-scoped

Timer demonstrates:

- geometry equivalence can be carried forward under an explicit equivalence proof;
- visual calibration PASS is only WebGL/render evidence;
- optical performance, measured material properties, thermal, DFM/DFA/tolerance, electrical and tactile/user recognition were not run;
- integrated public-browser QA is a separate gate.

Thus one evidence record may be reusable for one claim axis and unusable for another.

### Replay-derived rule

`P5/CARRY-RP02 EVIDENCE_CARRY_FORWARD_REQUIRES_CONFIGURATION_APPLICABILITY_PLUS_CLAIM_SCOPE_COMPATIBILITY; ONE_PASSED_CONFIGURATION_AXIS_CANNOT_CARRY_TO_UNTESTED_AXES`.

This complements P6 claim-ceiling rules but is owned here as configuration applicability.

---

# 8. Promotion-breaking versus local change

The two real cases show opposite ends of the same rule.

### KH46 support-only repair

- bounded support configuration changes;
- selected design authority unchanged;
- no re-promotion of selected-A required solely because support files changed;
- affected support evidence must be regenerated/read back.

### Timer approved geometry change (defined trigger, not executed in this source)

The render lock says approved geometry change would reopen the visualization target.

If source geometry actually changed, affected derivative/render evidence could no longer rely on old equivalence or old visual lock without re-evaluation.

### Replay-derived rule

`P5/IMPACT-RP03 PROMOTION_OR_REPROMOTION_EFFECT_DEPENDS_ON_WHETHER_CHANGED_PROPERTIES_INTERSECT_PROMOTION_BASIS; SUPPORT_ONLY_CHANGE_MAY_REQUIRE_LOCAL_REASSURANCE_WITHOUT_SOURCE_REPROMOTION`.

---

# 9. Supersession is not deletion

KH46 keeps old P37 hashes as superseded provenance.

Timer keeps rejected rounds as iteration lineage while the accepted Round 09 B becomes the active visualization decision basis.

Therefore supersession should preserve:

- historical configuration identity;
- prior decision/evidence state;
- replacement link;
- reason/basis;
- affected claim scope.

### Replay-derived rule

`P5/SUP-RP01 SUPERSESSION_RETIRES_CURRENT_APPLICABILITY_WITHOUT_DELETING_LINEAGE_OR_REWRITING_HISTORICAL_DECISION_STATE`.

---

# 10. Configuration fingerprint must be semantic, not file-list hash only

A useful fingerprint can include artifact hashes, but it must identify the governed property set.

Example:

```yaml
configuration_fingerprint:
  configuration_id:
  axes:
    GEOMETRY:
      source_ref:
      protected_properties:
      hash_or_digest:
    VISUALIZATION:
      lighting_ref:
      material_profile_ref:
      camera_ref:
    RENDER_PIPELINE:
      renderer:
      version:
      color_transform:
    SUPPORT_EVIDENCE:
      evidence_refs: []
```

This lets the system distinguish:

- `visualization changed / geometry same`;
- `support evidence changed / design same`;
- `geometry changed / derivatives stale`.

### Replay-derived rule

`P5/CFG-RP04 CONFIGURATION_FINGERPRINT_MUST_PRESERVE_SEMANTIC_AXES_SUFFICIENT_TO_DETERMINE_PARTIAL_INVALIDATION; OPAQUE_WHOLE_PACKAGE_HASH_IS_INSUFFICIENT_WHEN_SCOPED_REUSE_IS_REQUIRED`.

---

# 11. Rollback replay status

The searched OLEANDER corpus contains a governance **plan** for rollback:

- shared-branch rollback should use auditable reversal such as a rollback branch + `git revert` rather than destructive reset/force-push;
- Notion move rollback should restore the same page identity to its prior parent and verify the content/properties fingerprint.

This is a good rollback contract pattern, but it is **not evidence of an executed project rollback**.

Therefore:

`TP5 ACTUAL ROLLBACK REPLAY = NOT_EVALUATED / OPEN`.

No contract rule is promoted solely from that planned procedure beyond existing rollback requirements.

---

# 12. Concurrency replay status

No real executed case was found in the reviewed corpus where two approved changes concurrently targeted the same controlled variable/property and produced a recorded resolution.

Therefore:

`TP5 SAME-VARIABLE CONCURRENCY STRESS REPLAY = NOT_EVALUATED / OPEN`.

Existing concurrency rules remain draft/theoretical until a real replay is available.

Do not manufacture a concurrency collision just to close TP5.

---

# 13. TP5 replay-derived rules

Confirmed existing rules:

- `P5/CHG-RP01` support/derivative artifact change does not stale unchanged upstream source configuration;
- `P5/STALE-RP02` superseded support hash invalidates old support claim only within affected scope.

New real-replay rules:

- `P5/CFG-RP03` change/staleness scoped to configuration axes/properties; hash change alone ≠ source config change;
- `P5/EQV-RP01` explicit protected-property equivalence can support bounded carry-forward;
- `P5/LOCK-RP01` lock must name exact configuration/property scope;
- `P5/REOPEN-RP01` reopen propagation follows affected configuration/claim dependencies;
- `P5/CARRY-RP02` carry-forward requires both configuration applicability and claim-scope compatibility;
- `P5/IMPACT-RP03` re-promotion depends on intersection with promotion basis;
- `P5/SUP-RP01` supersession preserves lineage/historical decision state;
- `P5/CFG-RP04` semantic-axis fingerprint required for partial invalidation.

---

# 14. TP5 disposition

```text
PARTIAL_INVALIDATION / SUPPORT-ONLY CHANGE REPLAY = CONFIRMED
VISUALIZATION-ONLY CHANGE / SOURCE GEOMETRY EQUIVALENCE REPLAY = CONFIRMED
SCOPED LOCK / REOPEN TRIGGER REPLAY = CONFIRMED_BOUNDED
EVIDENCE CARRY-FORWARD SCOPE REPLAY = CONFIRMED_BOUNDED
ACTUAL ROLLBACK EXECUTION REPLAY = NOT_EVALUATED / OPEN
SAME-VARIABLE CONCURRENCY EXECUTION REPLAY = NOT_EVALUATED / OPEN
```

Overall:

`TP5 CONFIGURATION/CHANGE STRESS REPLAY = PARTIAL COMPLETE WITH MATERIAL DELTAS; ROLLBACK + CONCURRENCY REMAIN OPEN`.

No Current promotion is authorized.