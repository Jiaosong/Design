# 2026-08-17 Wayfinding — Decision Priority Validation

Status: **CANDIDATE strengthened / project-main validation pending**

## Existing-first
This round does not create a new Skill. It reuses the existing Wayfinding candidate `DECISION PRIORITY → GRAPHIC PRIORITY` from the Munich 1972 training, plus `oleander-story-and-board` for one-primary-claim / distance readability and the Universal Production Environment for editable SVG + pixel readback.

## Second independent case
Mijksenaar × Amsterdam Airport Schiphol. Official Mijksenaar material describes the system around orientation, navigation and experience, and the principle of delivering the right information in the right way at the right time. The long-running system uses consistent guidelines to maintain calm and efficient passenger flows.

Visible facts used: overhead placement, strong figure/ground contrast, destination grouping, explicit movement-related information, system consistency across the journey.

Design inference: consistency should not flatten decision priority. At a movement decision point, the most urgent action needs greater perceptual mass while lower-priority content stays visible but subordinate.

## C04 transfer
Current C04 authority retains `SERVICE / RETURN > ROUTE > OBSERVATION > EXPLANATION` and keeps FIELD OBSERVED=0 / FIELD MEASURED=0. The practice therefore changes only visual hierarchy, not route geometry, direction, distance, operation, safety or accessibility claims.

A keeps RETURN / ROUTE / OPTIONAL READING as near-equal bands. B keeps the same information set but makes RETURN primary through position, area, whitespace and type weight; ROUTE becomes secondary; optional reading becomes tertiary. A state override strip demonstrates that DEGRADED / CLOSED / UNKNOWN can supersede a normal route presentation.

## Readback
- editable SVG: executed;
- 1600×1000 PNG render: executed;
- first-read thumbnail: executed;
- near-read full-resolution review: executed;
- first-read result: B resolves RETURN materially faster than A without deleting content;
- near-read result: all preserved labels remain readable; state strip remains visibly subordinate but available.

## Gates
- Evidence Gate: PASS for the learning case and C04 authority mapping.
- Design Quality Gate: POST-REVIEW PASS for this project-specific practice artifact only.
- C04 MAIN / actual decision-point validation: PENDING; no current site sign, measured decision point, operational route direction or actual production UI was replaced in this round.
- Skill status: CANDIDATE strengthened, not VALIDATED/ACTIVE.

## Counterexample
A large RETURN block is not automatically correct. If a real CLOSED / UNKNOWN / hazard / accessibility condition becomes the highest-priority decision, that state must take the first visual position. The layout ratio is not a template.

## Transfer boundary
Do not copy Schiphol yellow, typeface, pictograms, airport sign geometry or trade dress. Do not invent C04 directions, travel times or opening state. `NO COMPRESSION / NO LOSS` applies: lower-priority content must remain recoverable rather than being deleted to manufacture simplicity.

## Artifact
- `OLEANDER_C04_RETURN_DECISION_HIERARCHY_v1.svg`
- local pixel readback SHA256 for SVG: `77f0848565657ce25ebbd6fc8e12445a1b7c28df02b989c1091fd8fe37bc4d72`
