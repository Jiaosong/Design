# C04 CH16-P01 v3.3 — RESOURCE-LED / INTERACTION-ENHANCED

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Page: `CH16-P01`  
State: `PRODUCER EXECUTED / INDEPENDENT DESIGN REVIEW PENDING`

## 0｜User authority delta

User correction 2026-08-19:

`CH16-P01 MUST BE RESOURCE-LED; INTERACTION FEEL MUST BE STRONGER.`

This changes v3.2's weighting. v3.2 over-weighted three static technical frames. v3.3 uses the design/technical resource itself as the dominant visual field and makes interaction operate **on the resource**, not around it.

ODB-02 pixel rule remains unchanged:

`ODB-02 / 可拆卸倚靠休息板.png = NOT DISPLAYABLE IN CH16`.

It remains provenance/design-source authority only; no visible use, crop, thumbnail, zoom, carousel or appendix carrier.

## 1｜Resource-led hierarchy

First-read order:

`RESOURCE → USER ACTION → INTERACTIVE REVEAL → TECHNICAL RELATION → OPEN ITEM`

Not:

`TITLE / UI → CARDS → EXPLANATION → SMALL RESOURCE`.

### Primary visible resource

`physical-memory-currentization-v1.2/assets/P02_railing_lean_rest_v1_2.svg`

Role: `DERIVED CURRENT TECHNICAL RESOURCE / INPUT + DISPLAY CANDIDATE`, not original design source and not automatic MAIN KEEP.

Presentation rule:
- full-frame;
- preserve entire 1600×1000 resource;
- `contain`, never crop / cover;
- target visual weight 70–82% of first viewport;
- UI remains peripheral and low-area;
- title/copy must not displace the resource below the fold on desktop.

## 2｜Interaction model

Interaction is a **reading instrument** for the resource.

### Direct resource interactions

1. `全图 / CLEAN` — remove all overlays and return to the complete resource.
2. `人体 / BODY` — reveal the use/body envelope and action sequence.
3. `连接 / ASSEMBLY` — reveal reversible clamp / isolation / existing-base relation.
4. `维护 / SERVICE` — reveal drain-clean / accessible-flow / FIELD-open zone.

Each state:
- keeps the whole resource visible;
- does not zoom/crop the raster/vector frame;
- uses a restrained focus veil + outline, not a replacement diagram;
- updates one concise evidence line below the resource;
- supports click/tap and keyboard `1–4`.

### Resource hotspots

Small numbered points are placed directly over eligible regions of the vector resource. Clicking/tapping a point changes the reading state. The hotspot is a locator, not a UI card.

### Mobile

- resource remains complete and uncropped;
- interaction rail becomes horizontal scroll / snap;
- supporting evidence becomes a one-at-a-time carousel when vertical space is insufficient;
- no horizontal clipping of the resource itself.

## 3｜Interaction-feel target

Use C04's existing digital interaction grammar without turning CH16 into an App:

- reveal rather than dashboard switching;
- compare / focus / trace rather than card browsing;
- subtle paper/ink transition rather than neon/game HUD;
- one strong action at a time;
- resource remains visually above UI decoration;
- UI disappears cleanly when the user chooses `全图`.

Relevant inherited principles:
- `L0 scene/resource first`;
- one strong primary action per state;
- deeper information is user-revealed;
- interaction mechanics live inside the actual scene/resource rather than abstract matrices/cards.

## 4｜Below-the-fold / carousel rule

The page does not compress required material to avoid page length.

If supporting resources or proof cannot remain readable below the main stage:

`FULL RESOURCE A → FULL RESOURCE B → FULL RESOURCE C`

via carousel / sequential full-frame presentation.

Hard constraints:
- no crop to fit;
- no cover fit;
- no card wall;
- no tiny 3-up technical thumbnails;
- no information deletion for compactness;
- carousel slide must have one clear resource as its visual center.

## 5｜What is forbidden

- visible ODB-02 pixels anywhere in CH16;
- UI occupying more visual hierarchy than the resource;
- dashboard/card-grid composition;
- generic decorative silhouettes;
- replacing the resource with a schematic only because interaction is easier to code;
- crop/zoom-as-layout-fix;
- AI-generated technical/product substitute;
- game HUD, progress score, unlock, reward, mission mechanics;
- historical concept dimensions silently promoted into field controls.

## 6｜Current production artifact

Candidate HTML:

`CH16-P01_v3_3_RESOURCE_STAGE.html`

The candidate deliberately references the merged current vector resource rather than duplicating it.

Interaction contract:

`CH16-P01_v3_3_INTERACTION_CONTRACT.json`

## 7｜Review boundary

Current state is producer execution only:

`EXECUTED / SELF-CHECKABLE / INDEPENDENT DESIGN REVIEW PENDING`.

Producer does not assign `PIXEL KEEP`, `MAIN KEEP` or `PROFESSIONAL FINISH PASS`.

Independent review must specifically test:
- does the resource dominate first-read;
- does interaction deepen reading rather than become UI decoration;
- can the whole resource always be seen uncropped;
- is BODY / ASSEMBLY / SERVICE distinction obvious without turning into a dashboard;
- desktop/mobile interaction clarity;
- technical hierarchy and project specificity;
- comparison to strongest current C04 resource-led Web/App sections.

Truth boundary remains:

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
