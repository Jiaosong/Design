# C04 Web Page Register Remap v0.1

Project: `PRJ-C04-QINGJIANG-SHISHU`  
State: `DRAFT MAPPING CANDIDATE / COLLISION-SAFE / NO PID GUESS / NO_PROMOTION`  
Stacked base: Draft PR `#294` / head `aa5379bcffbb565f7262700538775be797d0a3bc`

## 0｜Purpose

This remap performs the page-identity operation that C04 has repeatedly deferred:

`PROTECTED P001–P052 → AUTHORING UNIT → CURRENT PROFESSIONAL OWNER → PRESENTATION ROLE → FUTURE PAGE-ID DECISION`

It does **not** convert chapter count, authoring-unit count, producer surface count, or Web presentation sequence into canonical project page count.

## 1｜Count contract after remap

- Chapter containers: **20** (`CH00–CH19`).
- Protected legacy PAGE identities: **52** (`C04-WEB-P001…P052`).
- Base authoring units mapped one-by-one: **111** (`v0.1 + v0.2`).
- Candidate content records retained: **39**.
- Unique candidate authoring IDs among those records: **34**.
- Candidate-ID collisions: **5**.
- N-series allocated: **0**.
- `canonical_page_count = NOT_YET_LOCKED`.
- `current_complete_integrated_web_surface_count = NOT_YET_REGISTERED`.

Historical `v1.11 / 112 surfaces` remains a downstream presentation snapshot only. It is not resurrected as Current or canonical count.

## 2｜Exact protected PAGE register

`C04_WEB_PROTECTED_PAGE_REGISTER_P001_P052_v0_1.csv` and `.json` retain **all 52 IDs**. No protected identity is deleted or silently merged.

The v1.8 52-object contact readback visibly recovers **25 legacy labels**. Those labels are treated as source evidence, not as complete semantic proof. The other **27 legacy labels remain unrecovered**.

Because `P006 / RICH Window + Return` has a visible low-confidence label but its current semantic ownership remains unresolved, the current mapping queue contains **28 `SOURCE_RECOVERY_REQUIRED` rows** in total.

Current mapping-action distribution across the 52 protected IDs:

- `PRESERVE` = 28
- `MAP_TO_LEGACY` = 16
- `EXPAND_FROM_LEGACY` = 6
- `PROCESS-SUPPORT` = 2

These actions are provisional mapping decisions, not final PAGE promotion.

## 3｜111 base authoring units

`C04_WEB_AUTHORING_BASE_111_MAPPING_v0_1.csv` contains one explicit row for every v0.1/v0.2 base authoring unit.

No chapter wildcard or mechanical chapter-to-page rule is used.

High-confidence/provisional examples include:

- `CH00-P01 → C04-WEB-P001` / Hero first-read;
- `CH03-P01 → P002` / Culture intro;
- `CH04-P06 → P024` / Audience Depth;
- `CH09-P01 → P008` but content is rewritten to current `ROUTE-03`, never to legacy `JOURNEY-04`;
- `CH11-P01 → P011 | P022` remains `ROLE_SPLIT_REVIEW` rather than merging two protected App Intro identities;
- `CH15-P02 → P029` / Qingjiang Journal;
- `CH15-P03 → P041` / My Book memory model, while CH11 still owns UI implementation;
- `CH17-P04 → P033 | P036` explicitly preserves General Assembly + Detail Atlas as two independent proof surfaces under `NO COMPRESSION`;
- `CH19-P03 → P006` remains low confidence pending legacy source recovery.

CH14 base `P01–P08` is classified `NEW_CANDIDATE / NO_N_ID_ASSIGNED` because independent Brand was added after the protected baseline. This does **not** mean eight future canonical pages: `P OWNER != ONE PAGE`, and CH14 already has multi-surface manual execution.

## 4｜Candidate-content collisions repaired without loss

Earlier bookkeeping could incorrectly imply `28 + 11 → 34 unique candidates` was a safe content count. It is not.

The current candidate register preserves **39 content records** and identifies **5 repeated authoring IDs**:

- `CH11-P09`
- `CH11-P10`
- `CH14-P09`
- `CH14-P10`
- `CH14-P11`

The repeated IDs are provenance collisions, not automatic merges.

Examples:

- `CH11-P09@v0.1` = Information Architecture;
- `CH11-P09@v0.2` = Exploration Behaviour Grammar;
- `CH14-P10@v0.1` = Naming System;
- `CH14-P10@v0.2` = Brand Governance;
- `CH14-P11@v0.1` = Editorial System;
- `CH14-P11@v0.2` = Small Mark Optical Size.

Therefore:

`CANDIDATE ID COLLISION != CONTENT MERGE`

Distinct collided content must receive a collision-free working identity before any canonical N-series decision.

## 5｜Current professional ownership applied

The remap consumes the v0.3 ownership matrix from Draft PR #294:

- CH08 = Master Experience / real Qingjiang journey orchestration;
- CH09 = `ROUTE-03`, mobility, Service and functional Return;
- CH10 = R01–R13 optional-reading content/interaction;
- CH11 = Digital Companion behaviour / IA / UI;
- CH12 = selected scene integration and temporal handoff;
- CH13 = Physical / Body / Sensory;
- CH14 = Brand / VI grammar;
- CH15 = Memory / IP / cultural product;
- CH16 = detail development;
- CH17 = technical/model proof only;
- CH18 = evolution / selection / professional judgment;
- CH19 = open items / Return closure.

Hard rule:

`ONE OBJECT = ONE PRIMARY OWNER`  
`PRIMARY OWNER != ONLY APPEARANCE`  
`SCENE APPEARANCE != SOURCE OWNERSHIP`

## 6｜Current frontiers retained

- `ROUTE-03 = LOCKED CURRENT / NO SECOND ROUTE GEOMETRY`.
- `JOURNEY-04 = PROVENANCE / NON-CURRENT`.
- `R06 = FINISHED / FROZEN / NO REOPEN`.
- CH08 current strategy authority = v0.4 on #294.
- CH12 current scene frontier = v0.4 / A01–A09.
- App remains a separate authority; Web is downstream consume-only.
- Brand never acquires Route / Safety / live operational-state authority.

Draft PR #320 currently proposes a CH08 v0.5 **presentation reframe** on the exact same #294 base and explicitly does not replace v0.4 strategy authority. Its `9 P Owners / 28 visual surfaces` is therefore recorded as downstream presentation evidence only, not page count and not a PAGE-ID migration input.

## 7｜Files in this remap

- `C04_WEB_PROTECTED_PAGE_REGISTER_P001_P052_v0_1.csv`
- `C04_WEB_PROTECTED_PAGE_REGISTER_P001_P052_v0_1.json`
- `C04_WEB_AUTHORING_BASE_111_MAPPING_v0_1.csv`
- `C04_WEB_AUTHORING_CANDIDATE_REGISTER_v0_1.csv`
- `C04_WEB_BY_CHAPTER_SURFACE_REGISTER_v0_1.csv`
- `C04_WEB_CURRENT_FRONTIER_OVERLAY_v0_1.json`
- `C04_WEB_PAGE_REGISTER_REMAP_READBACK_v0_1.json`
- `OWNER_RECEIPT_C04_WEB_PAGE_REGISTER_REMAP_v0_1.json`

## 8｜Open mapping queue before N-series allocation

1. Recover the missing legacy semantic identity for P009–P010, P012–P021, P025, P027–P028, P032, P034, P037–P039 and P046–P052.
2. Resolve P006 `RICH Window + Return` meaning/ownership.
3. Resolve P011 vs P022 App Intro role split without merging protected identities.
4. Resolve P033 / P035 / P036 technical-object identities and current namespace before final binding.
5. Resolve the five candidate-ID collisions with collision-free working IDs; do not delete either provenance record.
6. Run material-independence review on every `NEW_CANDIDATE`, especially CH14 multi-surface Brand content.
7. Only after the above, allocate genuine `C04-WEB-Nxxx` identities where content cannot be represented without compression/loss.
8. Derive canonical page count from the resolved register; never from chapter count, authoring count, or presentation-surface count.

## 9｜Gate boundary

This package proves that a collision-safe mapping register has been authored and versioned. It does not prove:

- final canonical page count;
- final integrated Web surface count;
- finished-pixel Design PASS;
- browser/live-navigation PASS;
- independent professional review;
- field validation;
- engineering approval;
- project Promotion.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`
