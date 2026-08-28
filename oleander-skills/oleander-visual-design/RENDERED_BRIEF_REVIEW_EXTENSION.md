# OLEANDER Rendered Brief-to-Artifact Review Extension

Status: `CANDIDATE EXTENSION / INDEPENDENT DESIGN REVIEW INPUT`

Use when reviewing a visual, web/UI, board, deck or other rendered artifact against an explicit brief, adopted reference, Current design source or project-specific quality target.

This extension strengthens review evidence. It does not authorize a producer to self-KEEP.

## Core contract

`BRIEF / CURRENT DESIGN AUTHORITY → ACTUAL IMPLEMENTATION STATE → RENDER / VIEW AT TARGET CONDITION → OBSERVED MISMATCH → SEVERITY → OWNER → REPAIR → RECAPTURE / REOPEN`.

Code, source structure, token usage, export success and planned intent are useful supporting evidence but cannot replace seeing the actual result when the review claim is visual.

## Review source stack

Before critique, resolve the relevant comparison source:

1. Current project/design authority;
2. approved brief / requirement coverage map;
3. strongest mature existing artifact that must not regress;
4. adopted reference/template decomposition when applicable;
5. target runtime/viewing condition.

Do not compare against an invented aesthetic target after the artifact is built.

## Capture / render evidence

Capture or render the smallest sufficient set of states needed to judge the claim. Examples:

- target desktop/mobile viewport for web;
- far/mid/near read for board;
- full slide at playback size for deck;
- default + high-risk interaction states;
- light/dark variants only when both are part of the Current output;
- source-independent faithful render when the authoring surface cannot provide a screenshot.

Do not mechanically create every breakpoint/state when it does not affect the review claim. Conversely, do not judge responsive/state behavior from one static desktop image.

Record artifact identity, viewport/size/state and renderer/runtime so findings are traceable.

## Observation before diagnosis

For each material issue separate:

- **Observed fact** — what is visible in the rendered artifact;
- **Expected relation** — what the brief/authority requires;
- **Mismatch** — where the two differ;
- **Likely cause** — grid, scale, crop, type, image, state, token, DOM/runtime, motion, asset binding or another carrier;
- **Repair owner** — visual-design, image-art-direction, web-ui specialist, motion, upstream design-process, technical drawing, etc.;
- **Verification** — which recapture/reopen proves the repair actually changed the artifact.

Do not jump directly from `looks weak` to generic polish advice.

## Severity based on consequence

Use consequence, not personal taste:

- `BLOCKER / MUST FIX` — breaks required meaning/state/accessibility/source truth, prevents task completion, or materially violates Current authority.
- `MAJOR / SHOULD FIX` — hierarchy, responsive behavior, consistency, image binding, typography or interaction weakness that significantly reduces professional quality but does not invalidate the object.
- `MINOR / COULD IMPROVE` — bounded polish issue with low effect on meaning or primary quality.

Aesthetic preference without a brief/project basis must not be mislabeled as a blocker.

## Code-to-pixel cross-check

When source code/design tokens are available, use them to explain or verify the rendered finding:

- inspect computed/rendered state, not only declared source values;
- verify shared tokens/components survived integration;
- distinguish one-off hardcoding that causes drift from legitimate project-specific exceptions;
- inspect missing/broken assets, font loading, overflow, z-index/state collisions and layout behavior that source review can miss.

`SOURCE DIFF ≠ VISIBLE CHANGE`.

After repair, reopen/recapture. Do not close a visual defect because the code changed.

## State-aware review

For interactive artifacts, review state semantics separately from static polish. Where applicable inspect:

`default / hover / focus / pressed-or-selected / disabled / loading / empty / error / success / expanded-open / interrupted-reentry`.

Only review states relevant to the artifact. Missing required states are defects; unrequested theoretical states are not automatically required.

## Responsive review

Responsive quality is judged by preserved hierarchy and task/state meaning, not proportional similarity.

Check whether the design:

- recomposes instead of merely shrinking;
- preserves primary evidence/object ownership;
- adjusts crop and density intentionally;
- maintains touch/keyboard/readability requirements;
- avoids overflow/clipping and hidden critical actions.

## Output

A formal review record should include:

- reviewed artifact/version;
- brief/authority/reference used;
- captured/rendered evidence list with target conditions;
- strongest preserved aspects;
- observed mismatches grouped by severity;
- exact owner and repair operation for each material issue;
- recapture/reopen evidence after repair;
- unresolved HOLDs;
- separate Evidence/Runtime/Design Quality conclusions where applicable.

## Boundary

This extension does not make screenshot count a quality metric. It does not require a specific browser automation product. If a faithful independent renderer can establish the visual state, use it according to Delivery QC fallback rules. Native-source health, runtime interaction proof, accessibility conformance and Design KEEP remain separate proof classes.