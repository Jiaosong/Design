# Long-form Text Measure Gate

Status: **CANDIDATE / project validation pending**

This is a bounded submodule of `oleander-story-and-board`; it does not create a parallel typography Skill.

## Problem
A long-form evidence/report page can have a correct grid, type scale, hierarchy and source boundary while remaining tiring to read because the body-text measure is too wide.

## Trigger
Use when continuous prose is a meaningful evidence layer in a report, portfolio, board near-read, case-study page, or long-form web section.

## Candidate rule

`CONTENT ROLE → BODY MEASURE → LEADING → PARAGRAPH RHYTHM → SUPPORTING METADATA`

Treat body measure as an explicit design variable before adding cards, separators, type-size escalation or decorative hierarchy.

## Calibration
The current training A/B holds font size, leading, copy and grid constant and changes only body measure:

- A: approximately `104ch` → **REVISE FOR TRAINING**;
- B: approximately `64ch` → **KEEP FOR TRAINING**.

`64ch` is a local Latin-script calibration value, **not** a universal rule. CJK, bilingual text, different typefaces, target distances and media require separate calibration.

## Aesthetic judgment
Whitespace beside a controlled reading band is functional. Do not fill all available columns merely because the grid permits it.

## Verification
- first-read / distance: the body band must remain subordinate to the page claim;
- near-read: line return should not require an excessive horizontal sweep;
- compare variants with identical font size, leading and copy when isolating measure;
- re-open final pixels after every measure change.

## Failure condition
A page may look system-consistent because columns, baseline, caption and type tokens are correct, yet still require **REVISE** if long prose expands across every remaining column.

## Counterexample
Do not mechanically apply a prose measure to data tables, code, map labels, short captions, diagrams, or layouts whose meaning depends on horizontal correspondence.

## Transfer boundary
This gate evaluates reading measure only. It does not prove content correctness, accessibility conformance, publication-standard compliance, project Design PASS, or FIELD truth.

## Applicable domains
Report / portfolio / board near-read / long-form web / case study / evidence page.

## Evidence Gate
PASS for the precedent and training comparison only.

## Design Quality Gate
`POST-READBACK PASS FOR PRACTICE ONLY`.

## Version
v0.1
