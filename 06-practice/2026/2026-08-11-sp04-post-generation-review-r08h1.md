# SP04｜R08H.1 Post-Generation Review｜2026-08-11

Status: `POST-REVIEW FAIL / NEEDS REVISION`

## Why this review exists

R08H.1 had passed automated text/graphic boundary checks, but final artifact review still found design-drawing problems. Therefore automated QA is not sufficient evidence of final drawing quality.

## Findings

1. A1 title and upper dimension chain are too close; hierarchy and clear space are insufficient.
2. A2 labels for structural substrate / thermal-break keep-out / membrane continuity / waterproof-air barrier bridge are crowded with linework and hatches.
3. A2 dimension `60 [H]` does not match the actual 1:2 geometry shown. This is a geometry–annotation consistency failure.
4. `text_boundary_issues = 0` and `graphic_boundary_issues = 0` only prove panel containment, not final artifact correctness.

## Required next revision

- Rebuild A1 with a dedicated dimension zone and either exact 1:10 geometry or NTS labeling.
- Rebuild A2 dimensions from geometry values, never hard-code labels separately.
- Separate water / air / thermal / structural load paths so each can be traced independently.
- Reduce annotation density over hatches and control-layer linework.
- Re-run automated QA, then open final SVG/PNG and perform another Post-Generation Review.

## Gate

No DONE / PASS / Candidate status until `POST-REVIEW PASS`.

Canonical rule: [`../../00-governance/post-generation-review-gate.md`](../../00-governance/post-generation-review-gate.md)
