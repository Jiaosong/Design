# 2026-08-18 Long-form Text Measure Calibration

Status: **CANDIDATE / project-main validation pending**

## Existing-first
Reuses `oleander-story-and-board` for report/board hierarchy and the Universal Production Environment for editable HTML/CSS plus browser pixel readback. No parallel typography Skill is created.

## Learning object
Jan Tschichold × Penguin Books, late 1940s. Design Museum documents Tschichold's disciplined Penguin templates and Composition Rules; the Penguin Archive preserves later editions of the rules. The training does not reproduce a Penguin page.

## Visible Fact
Tschichold systematized text composition, paragraphing, punctuation, display spacing and book make-up so Penguin page quality did not depend on local printer habit.

## Design Inference
A coherent grid does not automatically produce readable continuous prose. Long-form body measure must be treated as an independent reading variable.

## Real C04 transfer
Current C04 governance/evidence text is used as content only. Same font size, leading, copy and grid:

- A: body measure ≈ 104ch → REVISE FOR TRAINING;
- B: body measure ≈ 64ch → KEEP FOR TRAINING.

The calibration changes presentation only. It does not alter C04 route, geometry, R06 platform, FIELD status, safety, accessibility or promotion state.

## Readback
- editable HTML/CSS: executed locally;
- system Chromium `/usr/bin/chromium` via Playwright: executed;
- 1440 px A near-read: executed;
- 1440 px B near-read: executed;
- 480 px distance derivative: executed;
- first reopen caught `DOES NOT PROVE` run-in typography and was REVISE;
- repaired version separates the truth-boundary label and body, then re-rendered.

## Candidate rule
`CONTENT ROLE → BODY MEASURE → LEADING → PARAGRAPH RHYTHM → SUPPORTING METADATA`

`64ch` is the local Latin-script calibration value in this practice, not a universal standard. CJK/bilingual text, typeface, size, distance and medium require separate calibration.

## Failure condition
A page can have correct columns, baseline, caption and type tokens and still REVISE if long prose expands across every remaining column.

## Gates
- Evidence Gate: PASS for precedent + authority mapping.
- Design Quality Gate: POST-READBACK PASS for this practice only.
- C04 production page validation: PENDING.
- Skill status: CANDIDATE.

## Does not prove
Accessibility conformance, publication-standard compliance, user comprehension, C04 FIELD truth, project Design PASS or release readiness.
