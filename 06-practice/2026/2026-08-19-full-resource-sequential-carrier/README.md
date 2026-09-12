# 2026-08-19｜Story & Board / Resource Presentation / L5｜Full-Resource Sequential Carrier

Status: **TRAINING EXECUTED / PRODUCER KEEP-FOR-TRAINING CANDIDATE / INDEPENDENT DESIGN REVIEW HOLD / NO_PROMOTION**

## Project trigger

Current C04 CH16-P01 v3.3 explicitly requires:
- resource remains the visual center;
- interaction deepens reading rather than creating a dashboard/card system;
- **NO CROP**;
- if supporting material cannot fit, use carousel/sequential full-resource presentation.

Recent training already covered responsive media art direction, same-source paired view, typographic density recomposition, scene-anchored depth, semantic occlusion, icon optical normalization and prompt↔media binding. The remaining gap is different: **how to preserve one complete reviewed/current resource across multiple reading states without replacing it with state-specific crops or compressing all states into equal cards**.

## Existing Skill reused

`oleander-story-and-board/VISUAL_LAYER_BINDING.md`.

Before this round it already required image-first hierarchy, dominant field, authoritative geometry protection and actual-pixel review, but it did not define a no-crop/sequential carrier rule for dense source resources.

## Actual exercise

A synthetic technical resource was created with one complete 1000×620 frame containing body scale, path relation, platform, interface anchor A and technical proof.

Controlled comparison:

- **REJECT** — CLEAN / BODY / ASSEMBLY / SERVICE are compressed into a 2×2 crop wall. Each state uses a different crop and gradually replaces the whole resource with extracted fragments.
- **KEEP candidate** — one complete resource remains on stage. CLEAN / BODY / ASSEMBLY / SERVICE only change bounded focus and peripheral reading. The full frame remains recoverable.

Editable asset:
`OLEANDER_FULL_RESOURCE_SEQUENTIAL_CARRIER_R01.svg`

Local execution also produced:
- `OLEANDER_FULL_RESOURCE_SEQUENTIAL_CARRIER_R01.png`
- `OLEANDER_FULL_RESOURCE_SEQUENTIAL_CARRIER_R01_GRAY50.png`
- `OLEANDER_FULL_RESOURCE_SEQUENTIAL_CARRIER_R01.html`

No image generation was used. Text remains vector/live text.

## Actual-pixel readback

The 1920×1080 PNG and 50% grayscale derivative were rendered from the editable SVG and reopened for finished-pixel review.

Observed:
- KEEP remains resource-first;
- the complete frame is legible as one object;
- state controls do not create a second hero;
- the reject crop wall visibly loses source identity/context;
- grayscale readback preserves hierarchy without relying on hue.

## Design Crit

### Compliance / execution

**PASS FOR TRAINING EXECUTION**

- editable SVG exists;
- PNG/Gray50 derivatives render;
- actual pixels were reopened;
- no generated imagery;
- synthetic NTS geometry only;
- no C04 dimension, construction, field, source approval or MAIN claim.

### Producer frozen-rubric

**KEEP-FOR-TRAINING CANDIDATE**

- First visual: PASS — KEEP reads one complete technical resource; REJECT reads fragments.
- Composition: PASS — KEEP has one dominant field and a secondary state rail; no card wall.
- Proportion: PASS — source stage dominates controls and annotations.
- Hierarchy: PASS — resource → bounded focus → state rail → metadata.
- Typography: PASS at 1920/Gray50 training readback.
- Material/spatial realism: schematic only; not a field/construction claim.
- Scale: NTS/training carrier only; no final device or print-scale certification.
- Node readability: PASS — interface A remains inside its parent resource rather than becoming an orphan detail.
- Interaction/narrative: static board + local HTML logic show CLEAN→BODY→ASSEMBLY→SERVICE sequencing; browser runtime PASS is not claimed here.
- Professional finish: sufficient for training calibration, not C04 MAIN.

### Independent Professional Design Gate

**HOLD / REVIEW REQUIRED**.

No independently attributable professional reviewer is available in this run. Producer pixel review is not promoted to independent KEEP.

## Failure knowledge

1. `NO COMPRESSION / NO LOSS` does **not** mean “show every state at once”.
2. A crop can keep the same file source while still destroying source identity and evidence context.
3. A 2×2 card wall can preserve artifact count but destroy first-read hierarchy and technical legibility.
4. Extracted detail may become a new apparent resource even when it was meant only as a focus state.
5. Progressive disclosure is valid only when deferred information remains recoverable later; deletion is not deferral.
6. Focus veil/annotation must remain bounded to the resource stage and may not silently rewrite geometry.
7. A new explanatory diagram/AI substitute is not justified merely because the current reviewed resource is dense.

## Repair method

`FULL RESOURCE → BOUNDED FOCUS → SEQUENTIAL SUPPORT → RETURN TO FULL RESOURCE`

Required tests:
- FULL-FRAME;
- STATE-IDENTITY;
- CROP-ATTACK;
- COMPRESSION-ATTACK;
- RETURN-TO-WHOLE;
- SUPPORT-CONTINUITY;
- NATIVE-CARRIER.

Promotion test:

> Step through every state: the full source frame must remain recoverable and identifiable; focus may deepen reading but may not become a replacement crop.

## Skill delta

Updated existing `oleander-story-and-board/VISUAL_LAYER_BINDING.md` with **Full-resource sequential carrier gate**.

Added:
- resource identity lock;
- no-crop authority handling;
- sequential full-frame/carousel/step-through carriers;
- focus/state continuity rules;
- compression/crop attacks;
- hard failures for replacement crops, crop walls, card-wall compression and information deletion;
- machine/review fields for resource source/version, full-frame visibility, state set, focus method and Return-to-whole.

No standalone Skill was created.

## Cross-project transfer

Applicable to:
- C04 CH16 technical/resource-led pages;
- C04 CH10/CH08 resource-led interaction where one reviewed resource must remain primary;
- architecture/landscape boards with dense source drawings;
- product/CMF explanation stages;
- portfolios and exhibition pages presenting complete original work;
- mobile/desktop carousels where cropping would remove evidence.

Not directly applicable to:
- sources whose authority explicitly permits editorial cropping;
- pure decorative imagery without an information-preservation requirement;
- true alternative schemes where each state is genuinely a different source object;
- analytical dashboards whose task requires simultaneous comparison of all panels;
- regulatory documents that require all information visible simultaneously.

## Truth boundary

`TRAINING ONLY / SYNTHETIC RESOURCE / NTS / FIELD OPEN / NO IMAGE GENERATION / INDEPENDENT DESIGN REVIEW HOLD / NO_PROMOTION`.
