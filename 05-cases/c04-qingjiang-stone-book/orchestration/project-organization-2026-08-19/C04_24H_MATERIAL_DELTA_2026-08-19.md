# C04｜24H MATERIAL DELTA｜2026-08-19

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Window: `2026-08-18 09:08 → 2026-08-19 09:08 (UTC+8)`  
Role: `PROJECT ORGANIZATION / CURRENTIZATION INPUT`  
Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`

This file records only material changes that affect how the C04 project should now be organized. Training-only PRs, CI-green status and local artifacts do not automatically become project Current.

## 1｜Material deltas that change project organization

### A. Project architecture is now v3.2
Current `C04_CURRENT.md` declares `PROJECT ARCHITECTURE v3.2` and the mandatory hierarchy:

`PROJECT → CHAPTER → PAGE → MODULE / FIGURE / ASSET`

Current chapter containers are `CH00–CH19`. `CH14｜品牌与视觉识别系统` is now an independent professional chapter. Brand and Memory/IP are distinct systems:
- Brand = how the whole project is recognized;
- Memory/IP = what travels after the visitor leaves.

Hard count rule:
- `CHAPTER ≠ PAGE`;
- protected `C04-WEB-P001…P052` remain page identities / migration baseline;
- 20 chapters, 52 protected page identities, authoring-unit totals and Web presentation surfaces must never be collapsed into one canonical page count;
- final `canonical_page_count = NOT_YET_LOCKED` until exact PAGE REGISTER mapping closes.

### B. CH14 Brand has become a real project system, not a visual appendix
Merged main now carries the CH14 P01–P07 baseline source locks:
- P01 v5.6 — Brand Foundation / 为什么叫「清江石书」;
- P02 v5.8 — Verbal Identity / 品牌命题与语言;
- P03 v7.2 — Logo / Wordmark / VI Manual;
- P04 v1.0 — Color System;
- P05 v1.0 — Typography / Layout;
- P06 v2.0 — Map-derived Graphic Language;
- P07 v1.0 — Icon / Legend / functional information family.

P06 v1 is superseded provenance. P06 v2 is source-bound to `ROUTE-03 = LOCKED CURRENT`; no second decorative route geometry is allowed. Brand `LINE / TRACE / PAGE relation` must derive from locked route geometry. Stone Seal remains identity authority and does not become route, safety, status or map-node authority.

P08 `FULL → LIGHT → TRACE → OFF` remains an explicit cross-media Brand Presence concept/current material, but is not interpreted here as a newly merged independent Design PASS.

### C. CH02 / GIS current candidate has materially deepened but remains gated
Current stable figure namespace:
- `ENV-01` Slope / Aspect
- `ENV-02` Potential Drainage
- `ENV-03` Land Cover Evidence — HOLD
- `ENV-04` Water History Evidence — HOLD
- `ENV-05` Solar Scenarios
- `ENV-06` Operations Conflict
- `ENV-SYN-01` Environmental Synthesis

The older temporary `ENV-03 = synthesis` identity is provenance only.

Latest strict reexecution candidate is GIS v0.7.3. It reproduces source values/derivatives and repairs the derived cell-center raster transform without mutating the upstream durable package. It remains:
`EXECUTED / SOURCE REPRODUCED / PRODUCER READBACK COMPLETE / NEW-BINARY PERSISTENCE HOLD / INDEPENDENT PROFESSIONAL DESIGN REVIEW HOLD / NO_PROMOTION`.

Therefore v0.7.3 may update the candidate/evidence frontier, but must not be registered as project Design MAIN or Field authority.

### D. App lineage has moved, but project-organization may only register it
Current bounded candidate lineage now extends beyond PR #162:
`v1.25 specialist baseline → v1.26 Product/Journey/IA/Service architecture → v1.27 navigation/game architecture → PR #255 ROUTE-03 currentization candidate`.

Key source-authority correction: App route geometry must bind `ROUTE-03 = LOCKED CURRENT`; stale App-specific guide-route geometry must not return.

PR #255 remains Draft / review pending. Project-organization action = `REGISTER ONLY / USER-OWNED NEXT DESIGN DELTA / DO NOT MODIFY APP PIXELS`.

### E. OLEANDER execution baseline changed
Merged PR #263 currentized Resolver implementation to v1.2.1 and added sticky execution constraints + full-flow completion rules.

Project-organization must now treat these as execution constraints:
- an active `NO IMAGE GENERATION`, existing-first, no-new-Skill/METHOD/framework or similar explicit lock cannot be revoked by generic follow-ups such as “继续 / 优化 / 再做”;
- real existing Method/Skill/capability readback is required when reuse is requested;
- artifact existence, export, PR, CI green, self-check, render PASS or regression PASS cannot by themselves close the full OLEANDER flow;
- `FULL FLOW ≠ FULL SKILL STACK`.

## 2｜Changes that DO NOT automatically alter Current project authority

The following are material training / capability candidates but remain outside C04 project Current unless separately promoted through their own gates:
- experience ↔ technical proof co-registration;
- prompt ↔ media semantic binding;
- VI optical handoff;
- brand ↔ operational-state color separation;
- evidence-state surface grammar;
- 3D CMF interaction/lifecycle framing;
- icon optical normalization;
- responsive typography / bilingual role pairing / semantic occlusion;
- responsive-media art direction;
- mobile scene-depth grammar;
- brand ↔ wayfinding semantic firewall.

Their typical current state is `TRAINING / KEEP-FOR-TRAINING CANDIDATE / INDEPENDENT DESIGN GATE HOLD / NO_PROMOTION`.

## 3｜Required organization currentization

The 2026-08-17 project-organization package is preserved as provenance and must not be deleted. A successor organization layer must now:
1. bind to `PROJECT ARCHITECTURE v3.2`;
2. add `CHAPTER / PAGE / MODULE / FIGURE / ASSET` separation;
3. add CH14 Brand as an independent canonical project system;
4. update App candidate lineage to include PR #255 without taking App ownership;
5. update GIS candidate frontier to v0.7.3 while keeping persistence/review HOLD;
6. preserve `ROUTE-03 = LOCKED CURRENT` across Journey / App / Brand-derived graphics;
7. inherit sticky execution constraints / full-flow closure rules;
8. currentize Web storytelling as a downstream editorial contract, not project architecture authority;
9. preserve all previous canonical object IDs and no-loss rules unless an explicit supersession record exists.

## 4｜Does not prove
This 24h delta is a project-organization readback. It does not establish new Web pixels, App Design PASS, Brand Design PASS, GIS Design PASS, Field truth, engineering approval, construction readiness or project Promotion.