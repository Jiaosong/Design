# OLEANDER Practice — Responsive Focal Anchor

## Training question

How should a claim-bearing image survive a large aspect-ratio change without losing the object or relation that carries the claim?

## Existing method reused

- `oleander-story-and-board`: one primary claim and one primary visual.
- Existing OLEANDER no-loss principle: hierarchy and responsive adaptation must not silently delete claim-bearing information.
- CSS Images `object-fit` / `object-position` are treated as implementation primitives, not design verdicts.

## Practice asset

`hero_source.svg` is an abstract 1600×900 landscape calibration asset. The claim-bearing observation node is deliberately placed at source coordinate `(1190, 410)` so center cropping can be tested rather than assumed.

Target mobile image box: `390×520`.

### Variant A — center crop

`cover + object-position: 50% 50%`

Rendered source width at cover scale: `924.44 px`. The declared focal anchor lands at `x = 420.33 px`, outside the `390 px` viewport.

Verdict: **REJECT**. Layout fits, claim does not.

### Variant B — focal crop

`cover + object-position-x: 74%`

The same focal anchor lands at `x = 292.07 px`, inside the viewport while retaining the relation line and surrounding landscape.

Verdict: **KEEP for design training**.

## Independent Design Crit

- First visual gate: KEEP for focal variant; REJECT for center variant.
- Composition: focal variant preserves node + relation + enough landscape context.
- Proportion: mobile crop changes the field strongly but does not turn the node into an isolated icon.
- Hierarchy: landscape remains the field; node remains the claim anchor.
- Typography: not the training variable; overlay safe zone must be checked together with crop in production.
- Material/spatial realism: N/A; abstract calibration geometry only.
- Scale: N/A for site truth; no measured site claim.
- Interaction: N/A for static crop proof.
- Narrative continuity: PASS for focal variant because the same primary claim survives ratio change.
- Professional finish: KEEP as calibration asset only.

## Failure mode

`responsive = no overflow` is insufficient. A page can be technically responsive while its image crop removes the exact object that carries the design claim.

Do not fix this by stretching the image, inventing missing pixels, or replacing the asset silently. Declare a focal anchor / safe region, simulate target ratios, then either adjust crop position or produce an art-directed source variant.

## Evidence boundary

The exact crop geometry and an independent static visual derivative were checked. A local Chromium screenshot attempt failed because the runtime GPU process was unusable, so browser runtime remains **HOLD**. The static proof must not be reported as browser PASS.

## Transfer

Applies to web hero images, project case-study pages, responsive portfolios, slides-to-mobile translations, video reframing, and board-to-screen derivatives. It does not replace image-rights checks, actual browser QA, source-asset identity checks, or scene-specific art direction.
