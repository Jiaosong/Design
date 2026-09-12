# 2026-08-19｜Mobile UI / Media / L5｜Responsive Media Art Direction

Status: **TRAINING EXECUTED / PRODUCER KEEP-FOR-TRAINING CANDIDATE / INDEPENDENT DESIGN REVIEW HOLD / NO_PROMOTION**

## Project trigger

C04 official-media audit keeps `R01 RESPONSIVE ART-DIRECTION REQUIRED`. Recent training already covered Claim-bound Camera, Prompt↔Media Semantic Binding, Typographic Density Recomposition, World-Viewport Framing and Scene-Anchored Depth Grammar. The remaining gap is breakpoint-specific image framing: the same claim can become false when an automatic narrow crop removes one of its required objects or relations.

## Exercise

One synthetic landscape/world geometry is reused across all carriers. The claim is intentionally simple: the viewport must preserve a readable peak / river / observation-anchor relation.

- Desktop carrier: 1440×900, wider environmental context.
- Mobile KEEP carrier: 390×844, narrower viewBox deliberately shifted to keep the same evidence relation.
- Mobile REJECT carrier: 390×844 naive center crop; the required R06 anchor is lost.
- Responsive HTML: one geometry source, breakpoint-specific viewBox/copy measure.

No image generation is used. All training media is editable vector geometry; HTML copy remains live text.

## Design Crit

### Compliance / execution

PASS FOR TRAINING EXECUTION.

- editable HTML and SVG sources exist;
- desktop/mobile/reject PNG derivatives rendered from the SVG source;
- full-size desktop/mobile/reject PNGs were actually opened for visual readback;
- browser screenshot runtime was attempted but Chromium binary is absent, so **Browser Runtime PASS is not claimed**;
- no C04 field geometry, GPS, operational state or site photo truth is asserted.

### Professional producer rubric

**KEEP-FOR-TRAINING CANDIDATE**, not production KEEP.

- First visual: PASS — the designed mobile crop retains the same peak/river/anchor relation; the reject crop visibly loses the anchor.
- Composition: PASS — desktop keeps broad environmental context; mobile repositions copy and focal relation instead of shrinking the desktop composition.
- Proportion / scale: PASS for training carriers; 390×844 and 1440×900 are explicit carrier sizes, but they do not certify final C04 device ergonomics.
- Hierarchy: PASS — landscape evidence stays primary; copy and Return remain subordinate/functional.
- Typography: PASS in rendered SVG carriers; no missing-glyph issue observed.
- Material / spatial realism: schematic only; not a site-photo or field-geometry claim.
- Node readability: PASS — focal anchor survives in the designed mobile crop and fails in the naive crop.
- Interaction / narrative: static breakpoint story is coherent; actual browser breakpoint/runtime behavior remains OPEN because Chromium is unavailable.
- Professional finish: sufficient for training calibration; not a C04 MAIN visual.

Independent Professional Design reviewer provenance is unavailable in this run, therefore the independent Design Gate remains HOLD / REVIEW REQUIRED.

## Failure knowledge

1. `object-fit: cover` or a centered crop is an implementation mechanism, not art direction.
2. A breakpoint can preserve the image yet delete the evidence that makes the page claim true.
3. Desktop/mobile source swapping is not automatically valid; silent geometry replacement creates a second truth source.
4. Copy collision can invalidate a crop even if the focal object remains technically inside the frame.
5. Zooming into a local feature can manufacture severity or certainty; crop itself can alter the apparent claim.
6. Generative extension may not invent missing landscape/product evidence outside the source frame.

## Repair method

`SOURCE GEOMETRY → CLAIM → FOCAL OBJECTS/RELATIONS → WIDE CROP → NARROW CROP → AUTO-CROP ATTACK → COPY-COLLISION → NATIVE READBACK`

Promotion test:

> Across wide and narrow carriers, the composition may change but the evidence-bearing relation must not disappear, move to a different source geometry, or be manufactured by the crop.

## Skill delta

Updated existing `skills/oleander-mobile-game-ui/VISUAL_LAYER_BINDING.md` in the same open training branch/PR that already owns mobile scene-depth work. Added `Responsive media art-direction gate` with:

- SOURCE GEOMETRY / FOCAL EVIDENCE / CARRIER CROP split;
- CLAIM-OFF / FOCAL-EVIDENCE / AUTO-CROP / COPY-COLLISION / RETURN-SAFETY / SOURCE-IDENTITY / NATIVE-VIEWPORT tests;
- hard failures for evidence-losing crops, silent source replacement, claim-changing zoom and generative extension;
- review record fields for source/version, focal relations, crop/viewBox and native readback.

## Cross-project transfer

Applicable to:
- C04 R01/R06/R13 web and mobile landscape media;
- travel/museum companions;
- landscape/architecture portfolio heroes;
- product-detail hero and evidence images;
- responsive editorial/story pages where an image carries a factual or design claim.

Not sufficient for:
- regulatory/safety imagery with mandated framing;
- true multi-camera datasets where a different source is explicitly authoritative per carrier;
- pure decorative imagery without an evidence-bearing claim;
- AR registration, GPS, field visibility or production-photo truth.

## Artifact hashes

- HTML: `69d43a11ac98cafe008b5e4ecc409abc5132130ddb0d63d870630f0306609a30`
- Desktop SVG: `472a9b09e1d80d8ba6d5ceb364bb2401399b6d0deadcfc6f07405738ede9d138`
- Mobile KEEP SVG: `a249513f572a1ce55a62af74d59a8f96e7aeab9dd02af3d080b267fbe802ecbc`
- Mobile REJECT SVG: `97e4679e03fe5994683120df83a0878b99ba6e087a9d8395a5c9b56bbac4090b`
- Desktop PNG: `064ede0747597e9a839a24e5001fffb3945b1da6d0b8efacc3b840edcd3d9fac`
- Mobile KEEP PNG: `abbdd2bb296702222b9db4b85cba188fdac6fa333de2e150aea936c3d1db6dfa`
- Mobile REJECT PNG: `a9ab7e6bfdca99dfa6625087fa689df36f4773897ac0c26ca5d2a3ac6dd50175`
- Mobile Gray50 PNG: `9ba0b1d11b08fe2cf08ab570560a1f734f708794e8a089199dd4b885fc1471a4`

## Truth boundary

`TRAINING ONLY / SYNTHETIC GEOMETRY / NTS / NOT GPS / FIELD OPEN / NO_PROMOTION`.

This practice does not currentize C04 production screens or prove field/site/media authority.
