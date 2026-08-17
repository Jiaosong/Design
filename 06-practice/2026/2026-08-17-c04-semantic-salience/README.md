# 2026-08-17｜C04 S1 Semantic Salience Training

Status: `OBSERVATION / TRANSFER STUDY / POST-REVIEW PASS`

## Authority / reuse

- Project authority: C04 Experience Architecture + Digital Product Architecture + Visual Reading System.
- Reused installed skills: `oleander-story-and-board` for one-primary-claim/one-primary-visual hierarchy; `oleander-delivery-qc` for final render/readback discipline.
- No new reusable Skill created. No installed Skill modified.
- Production adapter: editable SVG + deterministic PNG render/readback (`NATIVE_AVAILABLE`).

## Learning object

Braun ET 66 pocket calculator, Dieter Rams / Dietrich Lubs, 1987. Museum Angewandte Kunst documents simplification around key functions, functional color coding, convex keys, and a distinctive yellow sum key. Centre Pompidou independently records the ET 66 as a 1987 Braun calculator by Rams and Lubs.

Sources:
- https://sammlung-digital.museumangewandtekunst.de/detailpage/collection/8aaba9e5-2b9b-47ac-b304-11074467d180
- https://www.centrepompidou.fr/en/ressources/oeuvre/cX4y7Bj

## Visible Fact / Design Inference / Transfer Rule

**Visible Fact**
- Main numeric keys are visually grouped.
- Function keys use differentiated color roles rather than one decorative palette.
- The sum/equals action is given unusually strong visual salience.

**Design Inference**
The interface reduces search cost because the strongest accent is tied to an operationally meaningful action rather than spread evenly across controls.

**Transfer Rule**
For an interface with one required primary action, reserve the strongest accent for that action; persistent service/safety controls may keep a distinct semantic cue but must not visually compete with the task action.

## C04 reverse review

C04 current authority already requires `每屏 1 个强主动作`, S1 = one observation prompt + `记下这一页` + optional `再深一点`, and Service/Return to remain highly reachable without turning the screen into a task UI.

A deliberately weak A-state used two equally strong colored buttons (`记下这一页` and `再深一点`) plus a saturated service marker. This created three competing action signals.

B-state correction:
- keep `记下这一页` as the only filled accent action;
- demote `再深一点` to a text action;
- keep Service/Return visible through position + restrained functional cue rather than a second large button;
- retain landscape/blank field as the dominant visual mass.

## Validation / review

Artifact: `OLEANDER_C04_S1_Semantic_Salience_AB_20260817.svg`

Final SVG SHA-256: `da4dd08ba31f3c7ec872ad384e8d52466fa928516f7420b80a737ecc01eda106`

Actual visual readback was executed on a 1600×900 raster render.

The first render failed visual review because the right annotation was clipped and button labels inherited the wrong fill color. Both were repaired and the artifact was rerendered/reopened. A second review then caught a transparent uncovered canvas area after widening; the background was repaired and the artifact rerendered/reopened again.

Final review:
- First-read: B locks the primary action faster than A and no longer produces equal-weight CTA competition.
- Near-read: button labels are legible; annotation is fully inside canvas; Service/Return remains discoverable but subordinate.
- Occlusion: PASS for the training diagram.
- Scale/proportion: PASS for the training diagram; not a device-size usability validation.
- Evidence Gate: PASS for the stated ET66 observations and C04 authority mapping.
- Design Quality Gate: `POST-REVIEW PASS` for this isolated hierarchy study only.

## Failure condition / counterexample

A screen can look visually tidy yet still be `REVISE` when two or more saturated controls compete at the same hierarchy while the product logic requires one primary action.

Do not apply this rule mechanically when two actions are genuinely co-primary, when safety requires an interruptive control, or when accessibility/contrast requirements demand a stronger persistent affordance.

## Skill state

`OBSERVATION` only. One external reference + one C04 transfer exercise is not enough for Candidate promotion. A second independent professional case or a real project implementation/readback is required before promotion review.
