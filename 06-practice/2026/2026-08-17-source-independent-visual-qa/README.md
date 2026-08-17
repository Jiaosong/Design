# OLEANDER Training — Source-Independent Visual QA

Training ID: `OLEANDER-TRN-2026-08-17-SIVQA`

## Trigger
The 2026-08-16 vector negative-space practice produced an editable artifact and parameter record, but visual QA remained HOLD because the Figma screenshot call hit the Starter-plan limit. The failure mode was not the vector artifact itself; it was a single-point dependency in the review pipeline.

## Training question
Can OLEANDER complete a real first-visual-gate review when the source application cannot produce a screenshot, without weakening traceability or design-quality standards?

## Existing rules reused
- Artifact existence does not equal design quality.
- Visual review must be independent from execution/traceability review.
- Editable/vector sources are preferred for design assets.
- Existing `oleander-delivery-qc` is extended rather than creating a parallel QC framework.

## Actual exercise
Created `source_independent_visual_qa.svg`, a 1600×1000 editable vector calibration sheet containing:
- a four-level stroke hierarchy;
- primary/secondary/detail annotation hierarchy;
- human-scale cue;
- a 25% first-read test;
- explicit fallback QA criteria.

The SVG was rendered independently with CairoSVG to a 1600×1000 PNG and reopened for visual inspection. Local render receipt:
- SVG SHA256 `af6629b5e9505a5bb54156a01a1d228fde488fe4abbf9d522aa50ce309969a21`
- PNG SHA256 `b3817237812c7f58c514ea200cc1a6baea5614e31b996392eb3aee4ca88cd37a`
- PNG bytes: `87125`
- renderer: `CairoSVG`

## Design Crit
Verdict: **KEEP / TRAINING ASSET**

- First visual gate: PASS — the primary frame and FORM → LOAD → DETAIL sequence read before annotation.
- Composition: PASS — two balanced fields and a lower QA band provide a stable scan path.
- Proportion: PASS — primary geometry occupies enough area to survive reduced view.
- Hierarchy: PASS — 8/4/2/1 px stroke ladder remains visibly distinct.
- Typography: PASS for calibration use; neutral system sans avoids style becoming the lesson.
- Material/spatial realism: N/A — this is a QA calibration sheet, not a construction claim.
- Scale: PASS — human figure provides relative scale without asserting real dimensions.
- Node readability: PASS — connection targets and leaders are explicit.
- Interaction/narrative: N/A for static artifact; reading sequence is explicit.
- Professional finish: KEEP for training/reference use, not a project deliverable.

## Failure mode captured
**Invalid rule:** “If the authoring tool cannot supply a screenshot, visual design review must remain HOLD.”

Why it fails: it confuses authoring-tool availability with the availability of a trustworthy rendered view.

## Correction
When the source is deterministic and renderable (SVG/HTML/PDF/vector export, image, video, etc.), use an independent renderer/viewer as a fallback, verify dimensions/content identity, reopen the rendered result, and perform the same Design Crit. Keep HOLD only when no faithful view of the artifact can be produced.

## Boundary
The fallback is valid for visual QA, not for proving native editability, authoring-tool state, hidden layers, interactive state, 3D scene correctness, or source-specific behavior. Those remain separate gates.
