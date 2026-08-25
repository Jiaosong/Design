# OLEANDER Design Skill Training — 2026-08-17 / First-Visual Repair Loop

Status: **TRAINING PROVENANCE / EVIDENCE INCOMPLETE / NOT PROMOTION EVIDENCE**  
Scope: Cross-project visual composition, board, web, slide, story, spatial presentation  
Primary skill modified: `oleander-skills/oleander-story-and-board/SKILL.md`

## 2026-08-25 readback correction

The original training record below reported two local artifacts and their hashes:

- `OLEANDER_TRAINING_FIRST_VISUAL_GATE_C04.svg`
- `OLEANDER_TRAINING_FIRST_VISUAL_GATE_C04.png`

However, PR #167 contains only this Markdown training record and the Story/Board Skill change; those SVG/PNG artifact bytes are **not present in the PR**. Their recorded byte counts and hashes are therefore preserved as historical claims only and cannot be independently reopened or used as promotion evidence from this repository state.

Consequences:

- the historical `SELF-CHECKED / REVIEW PENDING` statement is retained as provenance, not upgraded;
- no `PIXEL KEEP / MAIN KEEP / PROFESSIONAL FINISH PASS / TRAINING PROMOTION` may be derived from the missing artifact bytes;
- the reusable Skill delta currentized from this record is limited to the inspectable method content that remains valid against Current main: diagnostic-to-repair, target-scale readback, and representative-surface propagation stop;
- Existing Mature Design / Evidence First, authority preservation, independent verdict policy, and reference-reconstruction rules are already Current elsewhere and are not re-created here.

## Why this exercise

Recent OLEANDER governance already separates design quality from execution quality and requires strict 1:1 fidelity when an exercise claims reproduction. The operational question recorded by this run was the gap between identifying a visual failure and turning that critique into a concrete, inspectable repair.

The training sequence was recorded as:

`FIRST-READ TEST → MISMATCH MAP → CAUSE → ONE MATERIAL REPAIR → TARGET-SCALE READBACK`

## Existing rules reused

- Existing Mature Design First.
- Independent Design Verdict Policy.
- Artifact existence ≠ Design quality.
- Traceability ≠ Professional finish.
- Evidence correctness ≠ Visual excellence.
- Process PASS ≠ MAIN KEEP.
- Reference Reconstruction Fidelity Gate.

No new parallel governance framework was intended.

## Practice object — historical report

The original run reported a 1920×1080 editable SVG training page for C04/Qingjiang narrative hierarchy, with the exercise goal:

**Landscape first → relation reveal → evidence strip.**

The record states that the composition avoided a card wall, dashboard, methodology grid, and equalized module hierarchy; the river/spatial mass owned the main perceptual field, route relations were secondary, and evidence/state text was consolidated into a low-weight lower strip.

Reported local training artifacts — **not persisted in this PR, therefore not independently verified here**:

- `OLEANDER_TRAINING_FIRST_VISUAL_GATE_C04.svg`
  - reported bytes: 3986
  - reported SHA256: `8746cbae20226f4d4167755247edf34b2ab6de9c7bc77a1eafe597a13d5e56fc`
- `OLEANDER_TRAINING_FIRST_VISUAL_GATE_C04.png`
  - reported bytes: 180521
  - reported SHA256: `8ca14d5b88442056b12f04c0c60a39f9c77c36ee12a48e66e067a3f0802819ca`

Historical boundary: training artifact only; not a site plan; FIELD OBSERVED=0; FIELD MEASURED=0; G1F HOLD.

## Failure found during execution — historical report

### Failure 01 — font fallback broke the intended composition

The run recorded that the first render produced missing CJK glyphs because the SVG font stack prioritized a Latin font and the renderer did not recover the expected Chinese fallback.

Reported observed failure:
- Chinese title and body became square placeholder glyphs.
- First-read hierarchy became invalid even though geometry/export technically succeeded.

This remains a valid general lesson:

`Artifact exists / render succeeds ≠ design quality`.

Reported repair:
- replace the ambiguous fallback stack with an explicitly available `Noto Sans CJK SC` family;
- regenerate the PNG and visually reopen the full 1920×1080 output.

Reported verification:
- CJK title/body rendered correctly;
- primary title, landscape mass, route layer, and evidence strip read in the intended hierarchy.

Because the resulting bytes are absent from this PR, the reported verification cannot be independently re-performed here.

Reusable lesson retained:
- a typography system is not validated by CSS/SVG syntax alone; the actual target renderer/font environment must be reopened and checked.

## Visual diagnosis after repair — historical self-check

The original record reported:

### What improved

- One dominant spatial mass won over explanatory content.
- Route/state information remained legible without becoming the hero.
- Evidence stayed visible but consolidated rather than distributed across multiple cards.
- The page could be understood at first-read without paragraph reading.

### Remaining limitations

- Structural transfer study, not a 1:1 reproduction of an external professional reference.
- River geometry was a training abstraction and did not claim survey accuracy.
- Producer-self-checked only; no `PIXEL KEEP`, `MAIN KEEP`, or `PROFESSIONAL FINISH PASS` was authorized.

Historical verdict recorded: `SELF-CHECKED / REVIEW PENDING`.

Current governance classification after readback: **`PROVENANCE / EVIDENCE INCOMPLETE / NOT PROMOTION EVIDENCE`**.

## Skill modification — currentized material delta

The historical branch attempted a broader rewrite. Current main already independently contains the mature-design/evidence-first and authority-preservation architecture, so the 2026-08-25 currentization retains only the missing, non-duplicative delta:

1. **Diagnostic-to-Repair Loop** — turn a visible first-read mismatch into observed failure → likely cause → one material repair → verification.
2. **Target-scale / distance readback** — board far/mid/near; Web/slide actual viewport; PDF full-page/reading/detail; film/storyboard playback-size hierarchy.
3. **Propagation stop** — bring one representative surface to professional-review level before multiplying a new page/board system across the rest of the project.

The old branch's duplicate mature-design-first rules, generic first-visual prose, producer self-promotion boundary, and reference-reconstruction language are not treated as separate new ownership because those controls already exist in Current OLEANDER governance/skills.

## Transfer rule

Use the retained repair/readback logic for visual/narrative assembly across:

- exhibition boards;
- project websites;
- slide/deck pages;
- report spreads;
- portfolio pages;
- storyboards and keyframes;
- spatial/product/brand pages where technical proof must remain visible but subordinate.

Do not use the hierarchy rule mechanically on pages whose explicit role is technical proof, detailed data comparison, or another artifact where evidence itself is the primary subject. The first-read test still applies, but the primary carrier may legitimately be a drawing, chart, table, or technical detail.

## Regression requirement

A future Practice may restore promotion-quality evidence only by persisting the actual editable source + rendered readback, reopening them at the target condition, and completing the required independent review. If the task is labeled reproduction, the Reference Reconstruction Fidelity Gate must also be completed.
