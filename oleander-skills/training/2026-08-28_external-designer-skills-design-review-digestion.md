# External Skill Digestion — julianoczkowski/designer-skills/design-review

Date: 2026-08-28
Status: `EXTERNAL REFERENCE DIGESTION / KNOWLEDGE EVIDENCE`
License observed: Apache-2.0

## Scope read

Reviewed external `design-review/SKILL.md` and repository license state.

## Material delta accepted

1. formal visual review must compare the actual rendered artifact against an explicit brief/current design authority rather than review source code alone;
2. rendered evidence should be traceable to viewport/state/artifact identity;
3. observable mismatch should be separated from diagnosis and repair recommendation;
4. severity should reflect consequence to meaning, state, accessibility or professional quality rather than reviewer taste;
5. code/tokens/components should be used to explain a visible defect, not as a substitute for proof that pixels changed;
6. after repair, the affected state must be recaptured/reopened before closure;
7. state-specific and responsive review must use the relevant runtime states instead of extrapolating from one desktop screenshot.

## Existing-first mapping

- Existing OLEANDER Artifact Review remains authority and producer self-KEEP remains prohibited.
- New Candidate extension: `oleander-visual-design/RENDERED_BRIEF_REVIEW_EXTENSION.md`.
- `oleander-web-ui` continues to own real browser/runtime state evidence.
- `oleander-delivery-qc` retains source-independent faithful render fallback when the native authoring surface cannot capture.

## Stronger OLEANDER rules preserved

The external workflow's specific Playwright/Cursor priority and requirement to ask the user for screenshots when browser tooling is absent are not adopted. OLEANDER first uses faithful independent render/view fallback when it can prove the relevant visual state.

Fixed external breakpoint sets, minimum target sizes and directory conventions are not copied as universal rules; Current project/runtime requirements govern.

## Maturity

Candidate-only until exercised in independent project review with actual repair/recapture evidence.