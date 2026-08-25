# 2026-08-17 Graphic / Typography — Headline Letterform Relation

Status: **CANDIDATE / project transfer practice complete / broader validation pending**

## Existing-first
This round does not create a new Skill. It reuses `oleander-story-and-board` for grid / hierarchy / type system / distance readability and `oleander-delivery-qc` for final-pixel readback.

Recent training already covered dominant field / equal-grid hierarchy, including PR #187, so this round isolates a different question: whether the headline itself retains identity after decorative effects are removed.

## Learning object
Josef Müller-Brockmann, *Musica Viva*, 1958. MoMA records the work as linocut and letterpress, 128 × 90.5 cm. Museum für Gestaltung Zürich holds Müller-Brockmann’s estate.

Visible fact used: large geometric masses dominate the composition while program text sits in a narrow lower band with stable ordering.

Design inference: distinctiveness can be created by scale, width, line-break tension, tracking, leading and negative space before decoration is introduced.

## Transfer rule
`REMOVE DECORATION TEST`

Remove outline / sticker / burst / dot / gradient / decorative-line effects. If the title immediately loses first-read identity, the letterform hierarchy is not yet structurally sufficient and should REVISE.

## Baojiajie transfer
A 100 × 100 mm jump-card calibration keeps locked Logo and portrait assets out of the training file and reserves only their layout zones.

- A manufactures emphasis with outline + pill + underline + burst + dots.
- B keeps the same information role but relies on two-line size/width relation, tight tracking, controlled leading, two campaign colors by role, and a small brand-blue anchor.
- Copy is placeholder training copy and is not production-approved wording.

## Verification
- editable SVG produced;
- CairoSVG capability: `NATIVE_AVAILABLE`;
- 1600 × 1000 near-read rendered and reopened;
- v1 REVISE: evidence-strip columns adhered visually and footer label collided with body;
- v2 repaired both issues and was reopened;
- 480 × 300 distance readback: B still resolves the two headline masses first; A collapses into decorative noise.

## Candidate fields
- Problem: promotional headline looks busy but has weak typographic identity.
- Trigger: removing effects causes the title to collapse.
- Inputs: approved copy + card bounds + locked brand-asset zones + campaign palette.
- Visible Symptoms: many effects, similar weight among elements, weak word/line silhouette at distance.
- Cause: decoration is doing work that proportion and letterform relation should do.
- Technique: establish title event with scale ratio, width relation, line break, tracking, leading and negative space first; add decoration only after the structure survives.
- Parameters / Conditions: calibration used 72/64 headline sizes, approximately 1.12× second-line width relation, tight tracking and a short brand-blue anchor. These are not universal template values.
- Aesthetic Judgment: B is calmer but more distinctive because the headline itself has a readable silhouette.
- Verification: near-read + distance-read.
- Failure Condition: effects removed → title loses first-read identity.
- Counterexample: a highly decorated headline may look energetic at 100% zoom yet become an undifferentiated color block at retail distance; this must REVISE.
- Transfer Boundary: do not copy Müller-Brockmann’s circle composition, Swiss poster trade dress, or typography as style. Transfer only the relation-first discipline.
- Applicable Domains: retail POP, packaging front panel, campaign key visual, social tile, poster, web hero.
- Application Mapping: BAOJIAJIE retail jump cards first; reusable in other OLEANDER promotional-title systems after additional project validation.
- Evidence Gate: PASS for source facts and brand-authority boundary.
- Design Quality Gate: POST-REVIEW PASS for this calibration artifact only.
- Version: v0.1.
- Status: CANDIDATE.

## Does not prove
Artifact existence, render success, SHA, GitHub or CI do not prove production copy approval, print color, final Logo placement, portrait placement, SKU facts, commercial release, broader Skill validation or MAIN KEEP.