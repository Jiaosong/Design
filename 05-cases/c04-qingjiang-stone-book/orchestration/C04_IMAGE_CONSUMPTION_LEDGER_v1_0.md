# C04 Image Consumption Ledger v1.0

Status: **CURRENT PROJECT REGISTER**  
Project: `PRJ-C04-QINGJIANG-SHISHU`  
Decision date: **2026-08-19**  
Current since: **OLEANDER PR #319 / merge `463a4e5c22080b1fb1205bf9eb10e547684bc3f3`**

This project register applies the OLEANDER global rule:

`ONE SEMANTIC CONTENT IMAGE → ONE CONSUMER UNIT`

It does not replace Source Authority, Design Authority, Project State or the existing Assets & Deliverables Register. It records allocation only.

## Current records

| semantic_image_id | source identity | consumer(s) | state | reuse lock |
|---|---|---|---|---|
| `IMG-C04-D-HERO-01` | `01_HERO_KEEP_QJ-D_v1.1_1920x1080.png` / SHA256 `8e54b7e58c745c6c43b528befdb3bc1d2c30f3dd62ab165d3921620c0069475c` | D v1.1 Public Display Hero; Web W00 Hero binding; F 86s film opening; CH14 contour/crop derivative | `LEGACY_MULTI_CONSUMED` | `LOCKED / NO_FURTHER_USE` |
| `IMG-C04-F01-SCENIC-01` | parent `05_C04_F01_PRODUCT_DESIGN_CURRENTIZED_v4_1.png` / parent SHA256 `4a082ca4d124ceadb82af3a30af6f80c658a4a756735eb482459af89aba78ae5`; bounds `[60,215,1600,930]`; child SHA256 `ea68ac13acc8839da0754477c899cdfdcbafb28261c8f6b84c16af7347bac3d4` | CH13-01 v4 attempted use only; current Physical Recovery board no longer retains it as active design proof | `REJECTED_NOT_ELIGIBLE` | `DO_NOT_REUSE` |
| `IMG-C04-PHYS-RECOVERY-TECH-01` | parent `14_C04_PHYSICAL_RECOVERY_CURRENTIZED_v4.png` / parent SHA256 `0dc1cfc89b0499e3a74fcfcc867da5f8e9e4c014dcf3c9b8a5d879ecbe82ee1c`; bounds `[55,450,1270,930]`; child SHA256 `08ae30e2b1fb2046bf3cdd16f9e66598a5e0d8332fa3ec244acef83ed6c68943` | previous CH13-01 producer candidate | `RELEASED` | `RELEASED AFTER ODB-02 SOURCE MATERIALIZATION` |
| `IMG-C04-ODB02-S01-HERO-DEPLOYED` | parent `ODB-02 / 可拆卸倚靠休息板.png` / parent SHA256 `e3801e63c725de34e463510c3e3c41ad40e4ece692b4290667c7e06a4085eca6`; bounds `[1600,360,3370,1325]`; child SHA256 `1d18aa9682f23bbed96e9ee0dd624197e349bfbdad2d2da98e1a71b862b07a6b` | `CH13-S01-PAIRED-01` dominant deployed-state first visual | `RESERVED` | `LOCKED TO CH13-S01 PAIRED CONSUMER` |
| `IMG-C04-ODB02-S01-FOLDED-SUPPORT` | parent `ODB-02 / 可拆卸倚靠休息板.png` / same parent SHA; bounds `[3770,4260,4390,5710]`; child SHA256 `6d3d669521daf4e4656c36d81c9510659fd02050a1638376269ac693b499a987` | `CH13-S01-PAIRED-01` secondary folded-state support | `RESERVED` | `LOCKED TO CH13-S01 PAIRED CONSUMER` |

## CH13 S01 source-bound reservation swap｜PR #330

The original ODB-02 board was materialized into the active runtime from the user-provided source. The previous currentized descendant reservation is released **only because** two genuinely distinct original-board child figures are now recorded with explicit parent SHA, bounds, child SHA and semantic roles.

Both ODB-02 child figures share one paired consumer unit: `CH13-S01-PAIRED-01`. They may coexist only inside that S01 consumer. Neither may be reused on S03 or any other independent page/surface unless S01 is explicitly rejected and the reservation is released.

This reservation delta is a PR #330 candidate until merged. It does not promote the page or prove design quality.

## Historical correction

`IMG-C04-D-HERO-01` already violates the new ideal state because it was historically reused before this gate existed. The correction is **not** to erase those surfaces. It is marked `LEGACY_MULTI_CONSUMED`, frozen as provenance, and prohibited from any additional project use.

Rejected CH13 attempts using D Hero remain provenance only and do not create a new consumer right.

## Lookup rule

Before any C04 visual-producing task binds a content image:

1. derive or recover `semantic_image_id`;
2. check this ledger by exact source hash, parent source, child crop/figure hash and semantic identity;
3. if another consumer is `RESERVED / CONSUMED / LEGACY_MULTI_CONSUMED / REJECTED_NOT_ELIGIBLE`, stop and select another image;
4. reserve the new image **before** composing the surface;
5. convert `RESERVED → CONSUMED` only when the project presentation use is selected/current;
6. release only with explicit `REJECT / NOT ENTER PROJECT / SUPERSEDED AND RELEASED` authority.

Crop / resize / recolor / mask / contour / screenshot / derivative frame do not reset identity.

A multi-image original board may expose distinct child figures only when each has independent bounds, child hash and semantic role. Same-board paired views must remain inside one explicitly named paired consumer unit.

## SYSTEM_REUSABLE

Only explicitly classified logo / wordmark / icon / operational state symbol / navigation symbol / brand pattern / design token may repeat. They must not be used as chapter content-image substitutes.

## Does not prove

This ledger records asset allocation only. It does not prove Design PASS, field truth, engineering validity, rights clearance, source correctness or Promotion.
