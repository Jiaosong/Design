# OLEANDER TP10 Target-Condition Presentation Execution Replay — C04 Qingjiang Web PR #465 — 2026-09-15

Status: **DRAFT TARGET-CONDITION REPLAY / NOT CURRENT / NO PROJECT MUTATION**.

Target project: `PRJ-C04-QINGJIANG-SHISHU`.
Target presentation frontier: GitHub PR #465 / `agent/c04-web-v1-12-currentize-20260830`.
Exact replay revision: `430e2700fa6aae80a6ebb8ce48aeb5e87fe919bd`.

Purpose: execute P10 medium/source/truth-boundary semantics against the real current Web candidate rather than only describing Style/Technique rules.

This replay does not modify C04, does not issue Design KEEP, and does not promote PR #465.

---

# 1. Exact-head authority snapshot

At replay time:

- PR #465 = OPEN / UNMERGED;
- exact head = `430e2700fa6aae80a6ebb8ce48aeb5e87fe919bd`;
- Vercel deployment statuses = success for that exact SHA;
- `C04 Web Static Integrity` workflow run `34767808121` = SUCCESS;
- `AI Governance Evals` run `34767808156` = SUCCESS;
- `OLEANDER Project Anti-Pollution Gate` run `34767808123` = SUCCESS.

These are engineering/governance facts only.

Hard boundary remains:

`CURRENTIZED FRONTIER ≠ ASSET PASS ≠ BROWSER PASS ≠ DESIGN KEEP ≠ FIELD PASS`.

The PR remains unmerged and no independent `FINAL_KEEP` is inferred by this replay.

---

# 2. Exact-head Chromium target conditions

The current exact-head browser report (`C04_CURRENTIZED_BROWSER_READBACK_V2`) records `status=PASS` with no failures at:

- `desktop-1920x1080`;
- `desktop-1366x768`;
- `mobile-390x844`.

Across all three cases:

- document width = viewport width;
- horizontal overflow = 0;
- page errors = 0;
- missing images = none;
- R13 exists;
- R13 current-location semantics are asserted;
- project route/journey interaction remains active;
- state behavior is scoped as `explanatory-simulation` rather than live operation.

Reduced-motion readback:

```text
mediaQueryMatches = true
scrollBehavior = auto
modeTransition = 0s
```

### Result

`WEB_LOCALHOST_CHROMIUM_TARGET_CONDITIONS = PASS` for the declared browser/readback scope.

This does not establish:

- independent Design KEEP;
- Vercel protected external-content readback;
- engineering/field validity;
- PDF release validity;
- video release validity;
- release approval/merge readiness by itself.

---

# 3. Medium readback vector on exact revision

P10 must now represent a release as a vector rather than one scalar PASS.

```yaml
release_id: C04-WEB-PR465-430e270
source_revision: 430e2700fa6aae80a6ebb8ce48aeb5e87fe919bd
medium_readback:
  WEB_LOCALHOST_DESKTOP_1920: PASS
  WEB_LOCALHOST_DESKTOP_1366: PASS
  WEB_LOCALHOST_MOBILE_390: PASS
  WEB_LOCALHOST_REDUCED_MOTION: PASS
  REPO_LOCAL_STATIC_INTEGRITY: PASS
  VERCEL_DEPLOYMENT_BUILD_STATUS: PASS
  VERCEL_EXTERNAL_CONTENT_READBACK: NOT_EVALUATED
  PDF_PRINT_EXACT_REVISION: NOT_EVALUATED
  VIDEO_EXACT_REVISION: NOT_APPLICABLE_TO_WEB_RELEASE
  PHYSICAL_EXHIBITION: NOT_EVALUATED
```

### Replay rule

`P10/MED-RP02 MEDIUM_READBACK_VECTOR_MUST_BIND_EACH_RESULT_TO_SOURCE_REVISION_AND_TARGET_CONDITION; ENGINEERING_DEPLOYMENT_SUCCESS_AND_CONTENT_READBACK_REMAIN_SEPARATE`.

---

# 4. Target-condition identity is more specific than medium name

“Desktop PASS” is still underspecified.

The replay proves target condition must include at least:

```yaml
target_condition_id:
medium:
viewport_or_format:
runtime_or_renderer:
interaction_mode:
motion_preference:
network_or_host_mode:
source_revision:
required_assertions:
```

For this replay:

- renderer/runtime = Chromium via Playwright;
- host mode = repo-local localhost;
- viewport = 1920×1080 / 1366×768 / 390×844;
- motion preference includes reduced-motion test;
- source revision is exact `430e...`.

### Replay rule

`P10/MED-RP03 MEDIUM_PASS_WITHOUT_TARGET_CONDITION_IDENTITY_IS_INSUFFICIENT_FOR_REUSE_OR_CARRY_FORWARD`.

---

# 5. Browser coverage and visual/design judgment remain separate

The browser report itself lists open design-review items:

- Brand/Memory MAIN surfaces exist and are browser-covered, but independent Design Crit still decides KEEP/REVISE;
- P01-B physical carrier is browser-covered but remains a candidate/development carrier without engineering/project FINAL_KEEP.

Therefore:

```text
visible + loaded + responsive + interaction covered
≠
design-quality accepted
```

### Replay rule

`P10/READ-RP02 TARGET_CONDITION_BROWSER_PASS_MAY_CLOSE_RENDERING_INTERACTION_AND_BOUNDARY_ASSERTIONS_WITHOUT_CLOSING_DESIGN_CRIT_OR_PROFESSIONAL_ACCEPTANCE`.

This is not a deficiency; it is correct scope separation.

---

# 6. Truth-boundary persistence in actual target conditions

The exact-head browser report reads the operational-state boundary as:

`EXPLANATORY SIMULATION ... does not represent real-time operational state; real opening/closure/UNKNOWN requires field operation or human confirmation.`

It is asserted in desktop and mobile readback.

This is stronger than a repository-only note because the truth boundary is present in the rendered presentation state where the simulated state logic is consumed.

### Replay result

`PRESENTATION_TRUTH_BOUNDARY = PASS_FOR_TESTED_WEB_TARGETS`.

### Replay rule

`P10/BOUND-RP02 WHEN_A_PRESENTATION_EXPOSES_SIMULATED_OR_DERIVED_STATE_AS_USER_FACING_CONTENT_THE_BOUNDARY_MUST_BE_READABLE_IN_THE_SAME_TARGET_CONDITION_NOT_ONLY_IN_REPO_GOVERNANCE_METADATA`.

Internal tokens such as `G1F HOLD` need not dominate public copy, but the semantic limitation must remain readable where required for interpretation.

---

# 7. Semantic source identity versus derivative instances

A currentized dependency manifest from an earlier PR #465 revision records two runtime files:

- `assets/qj_hero_keep_v11_b64_01.txt`;
- `assets/qj_hero_keep_v11_b64_02a.txt`;

both bound to the same semantic asset identity:

`QJ-D v1.1 / 01_HERO_KEEP_QJ-D_v1.1_1920x1080.png`.

Therefore:

```text
2 derivative chunks
=
1 semantic source asset
```

for asset-source counting.

However that manifest was observed against an older PR #465 revision and must not be treated as a complete exact-head dependency inventory for `430e...`.

### Replay result

`SEMANTIC_SOURCE_IDENTITY MODEL = CONFIRMED`.

### Replay rule

`P10/ASSET-RP02 SEMANTIC_SOURCE_IDENTITY_MAY_SURVIVE_MULTIPLE_TRANSPORT_OR_RUNTIME_CHUNKS; SOURCE_COUNT_USES_SEMANTIC_SOURCE_ID_NOT_FILE_INSTANCE_COUNT`.

And:

`P10/ASSET-RP03 ASSET_MANIFEST_APPLICABILITY_IS_REVISION_BOUND; AN_OLDER_MANIFEST_MAY_SUPPORT_LINEAGE_WITHOUT_CLAIMING_COMPLETE_CURRENT_RUNTIME_COVERAGE`.

---

# 8. Runtime asset role is not automatically design role

At current exact head the browser report identifies:

- `assets/physical_body_support_hold.svg` as a physical carrier;
- `assets/brand_system_current.svg` as the Brand MAIN asset carrier;
- `assets/memory_journal_current.svg` as the Memory MAIN asset carrier.

The same report still keeps Brand/Memory design quality open and P01-B as development candidate.

Therefore `MAIN asset carrier in runtime` must be separated from `Design KEEP / PRIMARY project truth`.

Recommended fields:

```yaml
runtime_slot_role:
visual_semantic_role:
design_review_state:
source_authority_role:
```

### Replay rule

`P10/ROLE-RP03 RUNTIME_SLOT_ROLE_AND_VISUAL_SEMANTIC_ROLE_ARE_DISTINCT_FROM_DESIGN_REVIEW_STATE_AND_SOURCE_AUTHORITY`.

This resolves ambiguity in names such as `brandMainAsset` without downgrading their actual runtime importance.

---

# 9. Current public architecture count is presentation state, not source ontology

Exact-head browser readback currently asserts 14 public section IDs:

`hero, assets, journey, brief, context, audience, idea, thinking, systems, brand-system, memory-system, development, r13, final`.

Earlier C04 records contained 11-section, 18-section, 52 protected internal identities, 111 authoring units and stale 112-surface snapshots.

These counts describe different projection/authoring/migration scopes.

### Replay rule

`P10/SEQ-RP02 SECTION_PAGE_AUTHORING_AND_PROTECTED_IDENTITY_COUNTS_REQUIRE_SCOPE_LABELS; COUNT_CHANGE_ALONE_IS_NOT_CONTENT_LOSS_OR_SOURCE_MUTATION`.

No-loss must be demonstrated through mapping/coverage, not numerical equality of presentation counts.

---

# 10. Reduced motion is a target condition, not a separate style

The same release successfully changes behavior under `prefers-reduced-motion`:

- smooth/animated behavior is reduced;
- content/meaning remains available;
- no separate visual style identity is required.

### Replay rule

`P10/MOTION-RP02 REDUCED_MOTION_IS_A_TARGET_CONDITION_OVERRIDE_WITHIN_THE_SAME_PRESENTATION_SYSTEM_UNLESS_THE_INFORMATION_ARCHITECTURE_ITSELF_CHANGES`.

This prevents unnecessary duplicate Style Profiles.

---

# 11. Deployment success versus external content readback

Vercel statuses for exact head are successful, but the repo-local Chromium receipt explicitly limits itself to localhost and does not establish protected Vercel external behavior.

Therefore:

```text
DEPLOYMENT BUILD/STATUS PASS
≠
EXTERNAL CONTENT READBACK PASS
```

### Replay rule

`P10/MED-RP04 HOST_DEPLOYMENT_STATUS_AND_USER_VISIBLE_CONTENT_READBACK_ARE_SEPARATE_TARGET_CONDITION_RESULTS`.

This applies to preview environments, protected staging, CDN deployments and authenticated portals.

---

# 12. Exact-head presentation release snapshot

Minimum normalized presentation snapshot after replay:

```yaml
presentation_release_id: C04-WEB-PR465-430e270
project_id: PRJ-C04-QINGJIANG-SHISHU
source_revision: 430e2700fa6aae80a6ebb8ce48aeb5e87fe919bd
release_state: CANDIDATE_UNMERGED
source_authority_mutated: false
truth_boundary:
  field_observed: 0
  field_measured: 0
  no_promotion: true
  state_mode: EXPLANATORY_SIMULATION
medium_readback_vector:
  localhost_chromium_1920: PASS
  localhost_chromium_1366: PASS
  localhost_chromium_390: PASS
  reduced_motion: PASS
  static_integrity: PASS
  vercel_deployment: PASS
  vercel_external_content: NOT_EVALUATED
  pdf_exact_revision: NOT_EVALUATED
independent_design_keep: NOT_EVALUATED_BY_THIS_REPLAY
field_validity: NOT_GRANTED
engineering_validity: NOT_GRANTED
```

---

# 13. New TP10 machine concepts confirmed

The prior P10 replay proposed five concepts. This execution replay now tests them:

1. semantic visual source identity — **CONFIRMED**;
2. visual semantic role — **CONFIRMED, needs separation from runtime slot and design review state**;
3. semantic position — **PARTIAL, not exhaustively evaluated**;
4. medium-specific readback vector — **CONFIRMED ON EXACT HEAD**;
5. role-scoped Style Profile assignment with invariant axes — **NOT DIRECTLY EVALUATED BY THIS TARGET-CONDITION RUN**.

Additional confirmed concepts:

6. target-condition identity;
7. revision-bound manifest applicability;
8. runtime-slot-role versus design-role separation;
9. deployment-status versus external-content-readback separation;
10. section-count scope labeling.

---

# 14. Replay-derived rules

- `P10/MED-RP02`
- `P10/MED-RP03`
- `P10/READ-RP02`
- `P10/BOUND-RP02`
- `P10/ASSET-RP02`
- `P10/ASSET-RP03`
- `P10/ROLE-RP03`
- `P10/SEQ-RP02`
- `P10/MOTION-RP02`
- `P10/MED-RP04`

---

# 15. TP10 disposition

`TP10 PRESENTATION TARGET-CONDITION EXECUTION = COMPLETE_FOR_CURRENT_WEB_LOCALHOST_SCOPE_WITH_DELTAS`.

Still not closed:

- protected Vercel external-content exact-head readback;
- exact-head PDF target condition;
- independent Design Crit / FINAL_KEEP;
- exhaustive semantic-position audit;
- role-scoped Style invariant replay.

These are explicit target-specific OPENs, not reasons to erase the completed Chromium/static results.

No project or governance Current promotion is authorized.