# OLEANDER Design Skill Training — 2026-08-17 / First-Visual Repair Loop

Status: TRAINING RECORD / SELF-CHECKED / REVIEW PENDING  
Scope: Cross-project visual composition, board, web, slide, story, spatial presentation  
Primary skill modified: `oleander-skills/oleander-story-and-board/SKILL.md`

## Why this exercise

Recent OLEANDER governance already separates design quality from execution quality and now requires strict 1:1 fidelity when an exercise claims reproduction. The remaining operational gap was between identifying a visual failure and turning that critique into a concrete, inspectable repair.

This training run therefore focused on the skill:

`FIRST-READ TEST → MISMATCH MAP → CAUSE → ONE MATERIAL REPAIR → TARGET-SCALE READBACK`

## Existing rules reused

- Existing Mature Design First.
- Independent Design Verdict Policy.
- Artifact existence ≠ Design quality.
- Traceability ≠ Professional finish.
- Evidence correctness ≠ Visual excellence.
- Process PASS ≠ MAIN KEEP.
- Reference Reconstruction Fidelity Gate.

No new parallel governance framework was created.

## Practice object

A 1920×1080 editable SVG training page was produced for C04/Qingjiang narrative hierarchy, with the specific exercise goal:

**Landscape first → relation reveal → evidence strip.**

The composition intentionally avoids a card wall, dashboard, methodology grid, and equalized module hierarchy. The river/spatial mass owns the main perceptual field; route relations are secondary; evidence/state text is consolidated into a low-weight lower strip.

Local training artifact:

- `OLEANDER_TRAINING_FIRST_VISUAL_GATE_C04.svg`
  - bytes: 3986
  - SHA256: `8746cbae20226f4d4167755247edf34b2ab6de9c7bc77a1eafe597a13d5e56fc`
- `OLEANDER_TRAINING_FIRST_VISUAL_GATE_C04.png`
  - bytes: 180521
  - SHA256: `8ca14d5b88442056b12f04c0c60a39f9c77c36ee12a48e66e067a3f0802819ca`

Boundary: training artifact only; not a site plan; FIELD OBSERVED=0; FIELD MEASURED=0; G1F HOLD.

## Failure found during execution

### Failure 01 — font fallback broke the intended composition

First render produced missing CJK glyphs because the SVG font stack prioritized a Latin font and the renderer did not recover the expected Chinese fallback.

Observed failure:
- Chinese title and body became square placeholder glyphs.
- First-read hierarchy became invalid even though geometry/export technically succeeded.

This is a direct example of:

`Artifact exists / render succeeds ≠ design quality`.

Repair:
- Replaced the ambiguous fallback stack with an explicitly available `Noto Sans CJK SC` family.
- Regenerated the PNG and visually reopened the full 1920×1080 output.

Verification:
- CJK title/body render correctly.
- Primary title, landscape mass, route layer, and evidence strip are readable in the intended hierarchy.

Reusable lesson:
- A typography system is not validated by CSS/SVG syntax alone. The actual target renderer/font environment must be reopened and checked.

## Visual diagnosis after repair

### What improved

- One dominant spatial mass now wins over explanatory content.
- Route/state information remains legible without becoming the hero.
- Evidence is visible but consolidated rather than distributed across multiple cards.
- The page can be understood at first-read without needing the paragraph text.

### Remaining limitations

- This is a structural transfer study, not a 1:1 reproduction of an external professional reference.
- The river geometry is a training abstraction and does not claim survey accuracy.
- The artifact is producer-self-checked only; it cannot receive `PIXEL KEEP`, `MAIN KEEP`, or `PROFESSIONAL FINISH PASS` under the Independent Design Verdict Policy.

Current verdict: `SELF-CHECKED / REVIEW PENDING`.

## Skill modification made

`oleander-story-and-board/SKILL.md` was strengthened with:

1. Existing-mature-design-first requirement before layout redesign.
2. An explicit First-Visual Composition Gate.
3. Reject/revise conditions for card walls, report aesthetics, equalized hierarchy, and text-carried specificity.
4. A Diagnostic-to-Repair Loop that converts critique into concrete edits.
5. Target-scale / distance readback requirements.
6. Producer self-KEEP prohibition in the workflow.
7. Reference-bound training language aligned with the new 1:1 Fidelity Gate.
8. Training outputs that require an actual practice artifact, failure, repair, validation, reusable rule, and transfer boundary.

## Transfer rule

Use the updated skill when the problem is visual/narrative assembly across:

- exhibition boards;
- project websites;
- slide/deck pages;
- report spreads;
- portfolio pages;
- storyboards and keyframes;
- spatial/product/brand pages where technical proof must remain visible but subordinate.

Do not use the hierarchy rule mechanically on pages whose explicit role is technical proof, detailed data comparison, or another artifact where evidence itself is the primary subject. In those cases the same first-read test still applies, but the primary visual may legitimately be a drawing, chart, table, or technical detail.

## Next regression target

Run the same diagnostic-to-repair loop on an existing mature OLEANDER page with a locked source/reference, then compare side-by-side at target scale. If the task is labeled reproduction, the 1:1 Fidelity Gate must be completed before any method extraction is promoted.
