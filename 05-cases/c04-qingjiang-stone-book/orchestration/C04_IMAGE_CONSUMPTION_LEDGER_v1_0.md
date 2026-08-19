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
| `IMG-C04-PHYS-RECOVERY-TECH-01` | parent `14_C04_PHYSICAL_RECOVERY_CURRENTIZED_v4.png` / parent SHA256 `0dc1cfc89b0499e3a74fcfcc867da5f8e9e4c014dcf3c9b8a5d879ecbe82ee1c`; bounds `[55,450,1270,930]`; child SHA256 `08ae30e2b1fb2046bf3cdd16f9e66598a5e0d8332fa3ec244acef83ed6c68943` | CH13-01 current producer candidate | `RESERVED` | `LOCKED TO CH13-01 UNTIL EXPLICIT RELEASE` |
| `IMG-C04-C22-MACRO-01` | official Enshi Tourism Group source `nb983qsaoo.jpg`; C22 persisted materialization `C22_QINGJIANG_CABLE_PEAK_SOURCE_nb983qsaoo.jpg` / SHA256 `9c68159a8897f33373e3d41f4347e071b8d2860958df84e41a682aa79d69cc2f`; source URL `https://www.eslygroup.com/uploadfile/image/20230809/nb983qsaoo.jpg` | C22 Concept Masterplan CH14 v4.7 | `RESERVED` | `LOCKED TO C22 CONCEPT MASTERPLAN UNTIL EXPLICIT RELEASE` |
| `IMG-C04-CH07-P01-LANDSCAPE-01` | official Enshi Tourism Group source `k9zsdud798.png`; CH07 persisted materialization `CH07_P01_QINGJIANG_CLIFF_RIVER_SOURCE_k9zsdud798.png` / SHA256 `efb640e3fd0ac01ecc77925c901076f8ed65dac313e37e05d020838d0da39fa3`; source URL `https://www.eslygroup.com/uploadfile/image/20230718/k9zsdud798.png` | CH07-P01 / CH07-P01-S01 v0.4 producer review target | `RESERVED` | `LOCKED TO CH07-P01 UNTIL EXPLICIT RELEASE` |

`IMG-C04-C22-MACRO-01` source-hash note: the recorded hash is the exact persisted 850×567 JPEG used by C22 after Google Docs materialized the public official HTTP image; it is **not** a claim about the website-original byte hash. No C04 Notion/GitHub hit for `nb983qsaoo` and no pre-existing machine-ledger record were found before reservation.

`IMG-C04-CH07-P01-LANDSCAPE-01` source-hash note: the recorded hash is the exact persisted 600×400 PNG reserved for CH07-P01 after Google Docs materialized the public official HTTP image; it is **not** a claim about the website-original byte hash. Before reservation, the current ledger and GitHub had no `k9zsdud798` hit; Drive returned only the new source-materialization document; C04 Notion returned no direct filename-bound existing consumer.

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

## SYSTEM_REUSABLE

Only explicitly classified logo / wordmark / icon / operational state symbol / navigation symbol / brand pattern / design token may repeat. They must not be used as chapter content-image substitutes.

## Does not prove

This ledger records asset allocation only. It does not prove Design PASS, field truth, engineering validity, rights clearance, source correctness or Promotion.
