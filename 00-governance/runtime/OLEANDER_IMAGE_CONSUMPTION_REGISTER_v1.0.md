# OLEANDER Image Consumption Register v1.0

Status: **ACTIVE CANDIDATE EXTENSION TO CURRENT RUNTIME**  
Decision date: **2026-08-19**  
Scope: **ALL OLEANDER projects / visual-producing owners / semantic content images**

This file does **not** create a new METHOD, Skill, visual framework, style system or Source Authority. It extends the Current Resolver + Image Processing Operator + Execution Receipt with one missing instance-control function: **which semantic content image has already been allocated to which consumer unit**.

## 1｜Core rule

`ONE SEMANTIC CONTENT IMAGE → ONE CONSUMER UNIT`

A semantic content image may be used by one project consumer unit only. Once reserved or consumed, all other independent pages / chapters / boards / film shots / App or Web surfaces must select another image.

The gate is checked **before image binding and before layout production**, not after a repeated image has already been designed into a surface.

## 2｜Existing-first + source gravity

The default order for visual production is:

`CURRENT SOURCE / MATURE DESIGN / CURRENT BOARD OR NATIVE ARTIFACT → CONSUMPTION LOOKUP → REUSE DIRECT IF AVAILABLE → PRESENTATION ADAPTATION → NEW VISUAL ONLY IF A REAL GAP REMAINS`

A presentation carrier must not re-author a mature design object merely because it needs a Hero, a landscape ratio or a cleaner composition.

Hard direction:

`OBJECT INTEGRITY → FRAME / LAYOUT`

not:

`FRAME / LAYOUT → CROP OR REAUTHOR OBJECT UNTIL IT FITS`.

## 3｜Identity

Every content-image family requires:

- `asset_id`
- `semantic_image_id`
- `parent_source_id`
- `source_file`
- `source_hash`
- optional `figure_bounds / crop_bounds`
- optional `child_hash`
- `semantic_role`

### Derivative laundering is forbidden

Crop, resize, recolor, mask, opacity, blend, screenshot, frame extraction, monochrome conversion, contour trace, background removal, blur, texture, typographic overlay or Web derivative **do not create a new semantic image identity**.

They inherit the parent `semantic_image_id` and its reuse lock.

A multi-image design board may expose a genuinely independent child figure only when that figure is already a distinct view / drawing / image object. The child must record `parent_source_id + figure_bounds + child_hash + semantic_role`. Fragmenting one subject view into several crops does not create several reusable images.

## 4｜Consumption states

- `AVAILABLE` — unallocated.
- `RESERVED` — allocated to an active candidate/consumer; blocks parallel reuse immediately.
- `CONSUMED` — accepted/current presentation use; permanently blocks other independent consumer units unless explicitly released.
- `RELEASED` — reusable only after explicit project authority records that the former consumer is `REJECT / NOT ENTER PROJECT / SUPERSEDED AND RELEASED`.
- `REJECTED_NOT_ELIGIBLE` — image itself is not eligible for further project presentation use.
- `LEGACY_MULTI_CONSUMED` — historical duplicate use already exists; no additional reuse is allowed.

Ordinary revision, crop change, layout change or superseding a downstream export does **not** release the image.

## 5｜Mandatory consumer record

Before a visual-producing owner binds a content image, record:

`asset_id / semantic_image_id / parent_source_id / source_file / source_hash / consumer_project / consumer_owner / consumer_unit_id / page_or_surface / role / reserved_at / consumed_at / state / reuse_lock / release_reason / does_not_prove`.

If another consumer already owns the same `semantic_image_id` in `RESERVED / CONSUMED / LEGACY_MULTI_CONSUMED`, the result is:

`BLOCK / SELECT_ANOTHER_IMAGE`.

No “make it a different crop” fallback is allowed.

## 6｜SYSTEM_REUSABLE exception

Only assets explicitly classified `SYSTEM_REUSABLE` may repeat across surfaces:

- logo / wordmark;
- UI icon;
- operational state symbol;
- navigation/service symbol;
- brand base texture / pattern;
- design token / non-content system motif.

A chapter Hero, evidence photograph, design rendering, board figure, landscape image, product image or key-scene image cannot be reclassified `SYSTEM_REUSABLE` merely to avoid the uniqueness gate.

## 7｜Same-source paired view

Same-source paired views are permitted only inside **one declared paired consumer unit**. Both views share one consumption record and one reuse lock. The method does not authorize using the same source image again in another chapter/surface.

## 8｜Execution Receipt binding

For any visual-producing execution that binds semantic content images, the Current Execution Receipt must include an `image_consumption` section with:

- `register_path_or_authority`;
- `lookup_performed`;
- `reservations_or_consumptions`;
- `conflicts`;
- `blocked_assets`;
- `release_actions`;
- `verdict`.

No image-consumption section is required for runs that use only `SYSTEM_REUSABLE` assets or no raster/content imagery, but `NOT_APPLICABLE` must state the reason.

## 9｜Review triggers

Direct `REVISE / BLOCK` if:

- same semantic content image appears in two independent consumer units;
- derivative treatment is used to evade identity;
- image binding occurs without lookup/record;
- mature current board/artifact is replaced by a weaker re-authored presentation without a real design reason;
- layout crops away object integrity, body scale, ground relation or primary semantic proof.

## 10｜Does not prove

This register proves allocation discipline only. It does not prove Design PASS, field truth, engineering validity, rights clearance, source correctness or Promotion.
