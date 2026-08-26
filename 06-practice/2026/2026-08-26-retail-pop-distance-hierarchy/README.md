# 2026-08-26｜Retail POP / Visual Communication / L5｜Viewing-Distance Hierarchy

Status: **TRAINING EXECUTED / EXISTING CANDIDATE EXTENDED v0.2 / PRODUCER KEEP-FOR-TRAINING CANDIDATE / INDEPENDENT DESIGN REVIEW HOLD / NO_PROMOTION**

## Type Classification

- Primary Domain: Brand / Visual Communication
- Primary Type: Packaging & Retail POP
- Subtype / Output: die-cut jump card / shelf-talker visual hierarchy
- Stage / Purpose: design development → retail-read validation → prototype production handoff
- Viewer Task: FAR = first commercial claim; MID = claim + one reason/technology; NEAR = Logo / portrait / product / support proof
- Source Authority: Baojiajie Brand Program current locks; official Logo / portrait bytes are not rematerialized here, therefore editable `LOCKED ... SLOT` placeholders only
- DESIGN-led with print-production supporting type
- Skill Target: `physical size → distance-dependent claim hierarchy → 1:1 retail readback`

## Type Brief Check

**PARTIAL.**

Existing Current knowledge already covers:
- `FW-DESIGN-VISUAL-COMM-001`: CONTEXT/viewing distance, HIERARCHY and PRODUCTION;
- `PRAC-20260816-05 Dominant Field & First-read`: distance / near-read visual dominance;
- `oleander-print-production CANDIDATE v0.1`: die-cut handoff and far-read / near-read viewer task.

Missing before this round: a repeatable physical-size FAR / MID / NEAR ladder and an explicit distinction between diagnostic screen scaling and physical retail proof. A `DESIGN-TYPE KNOWLEDGE GAP` is registered in Notion K06 with status `OPEN_FOR_KNOWLEDGE_COMPLETION`.

## Current Project Gap

Project: Baojiajie / 欧科棉 `100天不发硬` retail jump-card.

The current design problem is not just dieline structure. A 140×180 mm carrier contains claim, technology, portrait, Logo, product and support copy. If these remain close to equal visual weight, the card may be complete at arm's length but weak during aisle approach.

## Existing Skill First

Owner retained: `oleander-skills/candidates/oleander-print-production`.

No parallel Retail POP framework is created. This round extends the same Candidate from v0.1 to v0.2.

## Professional calibration

- SEGD wayfinding practice: readable copy size depends on viewing distance and affects physical sign design.
- SEGD street-sign precedent: increasing physical blade size and choosing legible type improved distance visibility.
- SEGD wayfinding evaluation: development-stage evaluation includes legibility, sign size, position and fabrication; full-size/context testing is distinct from studio inspection.

These calibrate context and verification only. They do not supply Baojiajie aesthetics or universal retail-distance dimensions.

## Real A/B Execution

Both A and B use:
- the same 140×180 mm finished carrier;
- the same die silhouette;
- the same brand-blue / neutral palette;
- the same protected portrait / Logo / product slots;
- the same commercial claim vocabulary.

### A — equal-weight baseline

`100`, `天不发硬`, technology, support copy, portrait, Logo and product remain relatively close in visual weight.

### B — distance hierarchy candidate

**ONE BOLD MOVE:** `100天不发硬` becomes the dominant FAR-read visual mass. `欧科棉黑科技` becomes the MID-read reason. Logo / portrait / product remain present but move to NEAR-read proof roles.

This is hierarchy redistribution, not content deletion.

## Diagnostic Distance Readback

Finished card height = 180 mm. Diagnostic angular size was calculated only to create a normalized comparison board:
- 0.5 m ≈ 20.4° vertical visual angle;
- 1.5 m ≈ 6.9°;
- 3.0 m ≈ 3.4°.

These distances are **training diagnostics, not universal Retail POP standards**.

Screen simulation is not physical retail proof.

## Actual Readback → Root Cause → Fix → Retest

### Readback failure

The first diagnostic board directly mapped angular scale into the board canvas. At 0.5 m the A/B cards clipped outside their review cells, invalidating near-read comparison even though the source SVGs themselves were correct.

### Root Cause

The diagnostic carrier confused **relative angular scale** with unconstrained review-board size. This was a review-artifact composition defect, not a source-design defect.

### Feedback Action

Cap the 0.5 m diagnostic preview to the board's available review field while preserving the normalized scale ratios for 1.5 m and 3 m. Keep the exact physical size and calculated angles as metadata rather than allowing them to break the review composition.

### Retest

Re-rendered the distance board and grayscale board; final pixels were reopened. No clipping remains. The B candidate keeps a substantially stronger `100天不发硬` first read at MID/FAR diagnostic sizes and retains Logo / portrait / product at NEAR size.

## Design Crit

### Evidence / Execution Gate

**PASS FOR TRAINING EXECUTION**

- editable 140×180 mm SVG A/B exist;
- vector text remains editable;
- PDF derivatives exist locally;
- high-resolution PNG and grayscale diagnostic boards were actually reopened;
- no AI-generated image is used;
- protected brand/portrait/product remain source slots, not redrawn assets.

### Producer Design Quality Readback

**KEEP-FOR-TRAINING CANDIDATE**

- First-read: B > A for a single commercial claim.
- Composition: B establishes one upper dominant field and a quieter proof field.
- Proportion: claim-to-card mass is materially stronger without eliminating proof objects.
- Typography: claim, technology and near-read copy have distinct roles; no missing glyphs observed.
- Brand: working Baojiajie blue is used as context; official Logo geometry is not redrawn.
- Production: same dieline maintained; actual printer/converter proof remains OPEN.
- Grayscale: hierarchy remains visible without blue/pink hue dependence.
- Professional finish: sufficient for Candidate calibration, not final campaign artwork.

### Independent Design Quality Gate

**HOLD / REVIEW REQUIRED.**

No independently attributable professional reviewer is available in this run. Producer review is not promoted to independent KEEP.

### Physical Retail Readback

**HOLD.**

No printed 1:1 sample, real shelf/aisle clutter, mounting angle, glare or actual viewer walk-by test was executed. Therefore no real retail visibility PASS is claimed.

## Failure Knowledge

1. `CONTENT COMPLETE ≠ DISTANCE HIERARCHY COMPLETE`.
2. Enlarged artboard review can hide the fact that the commercial claim has insufficient physical mass.
3. A screen thumbnail is a diagnostic proxy, not a 1:1 retail visibility test.
4. Far-read cannot be repaired by deleting Logo/product/proof; information should release by distance.
5. `large type` is not automatically a valid solution; it must answer the first commercial decision.
6. Logo/portrait may be important brand assets but should not automatically compete with the primary retail claim.
7. Color cannot be the sole far-read carrier.

## Skill Delta

`oleander-print-production` **CANDIDATE v0.1 → v0.2**.

Added `Retail viewing-distance hierarchy extension`:
- FAR / MID / NEAR information ladder;
- fixed dieline/palette/asset-slot A/B discipline;
- diagnostic visual-angle readback with explicit physical-proof boundary;
- FAR-READ / MID-READ / NEAR-READ / GRAY50 / CLUTTER / LOCKED-ASSET / PRINT-1:1 tests;
- hard failures for screen-only validation, universal distance assumptions and evidence deletion;
- physical printed shelf/aisle readback required before VALIDATED.

Promotion test:

> At the intended physical size, the far read must expose one claim, the mid read may add one reason, and the near read must recover brand/product/proof without changing or deleting locked source assets.

## Project Re-application

Applied directly to Baojiajie 欧科棉 jump-card as B candidate. The modification is limited to visual hierarchy and slot proportion; it does not alter official Logo/portrait bytes or supplier dieline truth.

## Cross-project Transfer

Applicable:
- flat die-cut jump cards;
- shelf-talkers;
- hangtags / promotional cards;
- exhibition/retail information where physical viewing distance changes reading order.

Not sufficient for:
- packaging panels primarily read at hand distance;
- regulatory/safety signage governed by higher-authority standards;
- large environmental wayfinding requiring its own sign-system engineering;
- e-commerce/web where CSS viewport rather than physical viewing distance governs size;
- any retail validation without 1:1 print/context proof.

## Execution Receipt

- Skill owner: `oleander-print-production` Candidate
- Skill version: `v0.2`
- Skill update commit: `c264b048718bba4fb9b6fae4d1c2f88f92d47e76`
- A artifact commit: `e3d555efaa9c5d9e23d65d97fd236649d98fa3e8`
- B artifact commit: `ddca77697fc1d2db4aed35c1efdeb0c9f8ea92b3`
- Branch / current training frontier: `training/20260826-retail-pop-dieline-handoff`
- PR owner/frontier: `#370`
- Evidence Gate: `TRAINING EXECUTED / PHYSICAL RETAIL PROOF HOLD`
- Design Quality Gate: `INDEPENDENT REVIEW HOLD`
- Status: `CANDIDATE / NOT VALIDATED / NOT ACTIVE / NO_PROMOTION`

## Cleanup / Assimilation

No second Skill or second PR is created. This delta is assimilated into the existing Retail POP Candidate owner. The K06 gap remains OPEN because real 1:1 retail testing and wider professional knowledge completion are still missing.
