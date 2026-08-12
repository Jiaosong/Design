# C04-WS-04｜R05 A Photo-dominant Research Audit v0.1

**Project:** `C04｜清江石书｜红花峰林十三印`  
**Workstream:** `C04-WS-04｜视觉阅读与身份`  
**Notion output:** `C04-WS04-OUT-004` — https://app.notion.com/p/3bab86be5c478111a9cbda76c820b52d?pvs=204  
**Evidence:** `EVD-C04-003｜Official Web Media Technical Audit v0.1`  
**Runtime:** COCOS4 Smoke #52 / run `31561027659` / artifact `9127918519`  
**Status:** `A = REVISE / NO C04-VAL-02`

## 1. Tested asset

`OW-20230616-2a923422a`

- page target: `R05 红花石林 / S0`;
- source: official/operator website;
- rights: `PASS_PROJECT_USE_APPROVED`;
- source technical evidence: `1080×525`, `120087 bytes`;
- final Hero tech: `FAIL_LT2400_FINAL_HERO`;
- experiment usage: `RESEARCH_PROTOTYPE_ONLY`;
- exact 红花石林 identity: still requires re-verification.

## 2. Runtime/materialization result

PASS:

- official URL downloaded during C04 materialization;
- SHA-256 and expected byte count verified fail-closed;
- image imported into the generated Creator project as local resource;
- pinned MCP v0.3 scene materialization created the governed Sprite node and mounted the media controller;
- `web-mobile` build passed;
- existing WS-07A 18-screen runtime/responsive baseline passed unchanged;
- R05-A extra captures passed at `1080×1920`, `390×844`, `844×390`;
- runtime failures, runtime exceptions and console errors = `0`.

This establishes:

`OFFICIAL LOW-RES MEDIA MATERIALIZATION PASS / R05-A RESEARCH RUNTIME CAPTURE PASS`.

It does not establish Final Hero or final visual approval.

## 3. Human visual audit

### PASS — Photo-dominant landscape hierarchy

- the peak/stone-forest image is the first reading in all three viewports;
- no card stack, faux-antique frame, bronze skin or decorative Mark competes with the landscape;
- both portrait viewports retain the main peak mass;
- landscape orientation preserves the strongest full relation between peak group, vegetation and cableway scale;
- the test supports the WS-04 rule that S0 may use nearly zero graphic intervention.

### FAIL — Prompt/media relation

Current runtime observation:

`收起手机，先看峰林与江面的距离关系。`

The adopted photograph contains no readable Qingjiang river surface in any of the three captured viewports.

Therefore the photograph cannot support the current observation action. A Relation Mark must not draw, imply or compensate for a river relation that is absent from the factual photograph.

Decision:

`PROMPT–MEDIA RELATION FAIL`.

### REVISE — Text legibility

- Return Guard text sits over dark green vegetation and is visibly under-contrasted;
- the white title/observation in the landscape viewport is less stable against bright sky;
- the next visual iteration should test a minimal local gradient/text-protection treatment rather than reintroducing heavy UI cards.

### HOLD — Final Hero technical quality

The published website source is only `1080×525`. EVD-C04-003 already establishes that it fails the current `>=2400 px` fallback Hero threshold.

It remains valid only as `RESEARCH / LOW-RES WEB SOURCE / NON-FINAL`.

## 4. Decision

`PIPELINE PASS / PHOTO-DOMINANT LANDSCAPE HIERARCHY PASS / PROMPT–MEDIA RELATION FAIL / LEGIBILITY REVISE / FINAL HERO HOLD`.

`A = REVISE`.

## 5. Next gate before B

Do **not** start `B｜Photo + Relation Mark` using this image yet.

First close `R05 OBSERVATION ↔ MEDIA RELATION` through one of two controlled paths:

1. **Media-first:** find an official R05 image where peak forest + Qingjiang relation is actually visible, keeping the current observation; or
2. **Prompt revision:** if WS-04 decides that R05's first reading should instead focus on peak contour, depth/rhythm and vegetation proportion, explicitly revise the R05 observation and rerun A with the same photograph.

Do not preserve the current copy by graphically inventing an absent river relation.

## 6. Validation boundary

No `C04-VAL-02` is created by this audit.

The current formal boundary remains:

- `C04-VAL-01` runtime/responsive structure = PASS;
- low-res official media pipeline = PASS;
- R05 A visual structure = PASS;
- R05 content relation = REVISE;
- Final Hero tech = HOLD;
- final Landscape First visual = NOT PASSED.
