# OLEANDER Practice — Bilingual Typography Hierarchy

Training ID: `OLEANDER-TRN-2026-08-17-BITYPE`

## Problem selected

Recent OLEANDER boards and web surfaces frequently require Chinese and English on the same page. Existing `oleander-story-and-board` required a type system and distance readability but did not define how the two languages should divide visual responsibility. Equal font size, equal weight, equal width and repeated headline treatment can create two competing first reads and a template-like bilingual layout.

Repository search before training found no existing dedicated rule for bilingual hierarchy, mixed-script spacing, or bilingual line-break review.

## Reused authority

- Existing skill: `oleander-story-and-board`.
- W3C *Requirements for Chinese Text Layout (CLReq)*: Chinese punctuation and line-breaking constraints; Chinese/Western mixed text; proportional Latin and numeral forms; controlled spacing between Han and adjacent Western characters.

The W3C document is used as a composition reference. This practice does not claim blanket standards compliance.

## Actual practice artifact

A 1920×1080 editable SVG calibration board compares the same bilingual information with two layouts:

- `A / equal bilingual weight` — intentionally demonstrates two competing first reads.
- `B / primary language + support language` — Chinese carries first-read; English remains complete but shifts to verification/near-read.

No AI image was used. Text remains editable SVG text.

Local rendered artifact evidence:

- `bilingual_typography_v2.svg` — SHA256 `9845add891b0bf7fa45b4c9953f3c2c52e55120f0493dd7b6d5a4c2c27e6d5c2`
- `bilingual_typography_v2.png` — SHA256 `bbca7527de7aa88295e81030500022bf9ba449680b9fa25914be8105d2f44441`

## Design Crit

### v1 — REVISE

The deliberate equal-weight specimen accidentally cropped the English headline. That defect contaminated the exercise: it would have compared hierarchy failure plus overflow failure against the candidate. Export success therefore did not qualify the asset for KEEP.

### Repair

- Manually re-broke the English headline into two lines.
- Preserved its deliberately excessive visual weight so the training variable remained equal-language competition rather than overflow.
- Moved the divider and body copy to restore clean separation.

### v2 — KEEP / TRAINING ASSET

- First visual gate: PASS — candidate reads Chinese claim first, English second.
- Composition: PASS — primary title, secondary translation, primary body, secondary body form four distinct levels.
- Proportion: PASS — English is complete but no longer a co-hero.
- Typography: PASS — Chinese and Latin keep appropriate proportional forms; deliberate line breaks create a stable title block.
- Crop/overflow: PASS after v1 repair.
- Material/spatial realism: N/A — typography calibration only.
- Professional finish: KEEP for training use; not a project deliverable.

## Failure knowledge

1. `Bilingual completeness ≠ bilingual equal weight`.
2. A translated headline must not automatically inherit the same size, width and emphasis as the primary headline.
3. A deliberately bad comparison must still isolate one variable. Accidental overflow is not valid evidence for a hierarchy lesson.
4. Correct text content does not prove line-break quality. Rendered pixels must be reopened.
5. Typography must not hide translation drift or evidence-boundary differences.

## Skill delta

`oleander-story-and-board/SKILL.md` gains a `Bilingual typography gate` covering primary-language selection, unequal visual weighting without information loss, designed line breaks, Chinese/Latin mixed composition, technical-token integrity, distance/near-read review, translation alignment, and independent rendered QA.

## Transfer boundary

Applicable to exhibition boards, portfolio pages, web reports, decks, research books, captions, brand/editorial surfaces and bilingual technical presentations.

Not a substitute for translation review, font licensing, accessibility testing, localization for languages other than the tested CN–EN pairing, or project-specific content authority.
