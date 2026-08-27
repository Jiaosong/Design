# 2026-08-27｜DESIGN / Brand-POP / L5｜Discrete-State + Continuous-Benefit Claim-to-Form Translation

Status: **CANDIDATE PRACTICE / PROJECT RE-APPLICATION EXECUTED / VALIDATION HANDOFF OPEN / NO INDEPENDENT KEEP**

## Design Question
How should the current Baojiajie jump-card claim `自带两档 / 使用久一点` become a meaningful card silhouette rather than two lines of large type or two arbitrary decorative tabs?

## Inputs / Constraints / Authority
- Current task copy: `自带两档 / 使用久一点`; support: `七彩高弹棉 / 耐用吸水胶棉拖把 / 宝家洁新一代拖把`.
- Logo and portrait remain locked source assets; practice uses placeholders only.
- Portrait is secondary to claim/form.
- No AI-generated imagery.
- Production geometry, safe zone, substrate, mounting/spring/adhesive and dieline feasibility are downstream VALIDATION.

## Existing Skill First
Reused Candidate `oleander-design-process` from PR #394.

Gap: the Skill required options/readback/repair but had no concrete gate for a compound input containing different semantic dimensions that should not share one decorative metaphor.

## Research → Finding → Design Consequence
- Evidence: main copy combines `两档` and `久一点`.
- Inference: `两档` = discrete states; `久一点` = continuity/duration.
- Finding: translating both with the same device collapses different meanings.
- Consequence: assign orthogonal form roles before styling.

## Options
### A / 双翼标签 — REJECT
Two side tabs literally count “2”. Failure: numeric decoration does not encode a state sequence; duration remains text-only.

### B / 双档阶梯脊 — REVISE
Two steps encode discrete state; magenta vertical spine encodes duration. Improvement: semantics separate. Failure: the duration spine reads as a decorative arrow and competes with the claim.

### Repair / 两档切口 + 延展底座 — SELECTED DESIGN DIRECTION
- remove duration arrow;
- use taller continuous body for duration;
- keep two-state meaning in the stepped left silhouette;
- keep logo/portrait/product as source-bound slots.

## Actual Readback / Repair
The final PNG was opened at 1920×1080. First repair readback exposed blue `1/2` blocks as pasted UI-like buttons rather than structural form. They were removed; state meaning now stays in the stepped silhouette itself. PNG + Gray50 were rerendered and reopened.

Final local hashes:
- SVG `be8c8bcaa53956feb20db53769294dbd2ab33ba6531047b1d6dacc82150013c7`
- PNG `e65e82aa1f20264f23cc8a2ded1e3b9fc08a755354a2941d01480b6a324530f3`
- Gray50 `ab25812e274867287206f63118046c259d72453c0867c6b971d296e09d523b43`

## INTERNAL_ARTIFACT_FIRST_PROFESSIONAL_CRIT
### Evidence Gate
**PASS FOR DESIGN-PROCESS BOUNDARY**: current copy is treated as project input, locked assets are not recreated, production geometry is explicitly unvalidated.

### Design Quality Gate
**PRODUCER SELECTED DIRECTION / NOT INDEPENDENT KEEP**
- logic: PASS — discrete/continuous semantics use different form roles;
- proportion: PASS for schematic comparison;
- hierarchy: PASS — `自带两档 / 使用久一点` remains first read;
- form relation: PASS after removal of pasted number buttons;
- readability: PASS at training-board scale;
- template risk: reduced; selected shape is claim-derived rather than generic burst/cloud;
- completion: design-process level only, not finished retail artwork or production dieline.

Independent Professional Design Review remains OPEN.

## Root Cause / Repair / Retest
Root cause: `2 → two tabs/buttons` literal numeric decoration substituted for state semantics.

Repair: move meaning from attached graphics into the silhouette; keep continuous benefit on a different form axis.

Retest: remove labels/colored buttons — the stepped edge still preserves two distinct structural moments without a second icon system.

## Transfer Rule
When one claim combines **discrete states + continuous benefit**, decompose the semantics and assign orthogonal form roles before styling.

Applicable: POP, packaging claim architecture, product affordance, UI state+progress, analysis diagrams.

Counterexample: a pure quantity claim where two identical units are factually the subject.

## Skill Delta
`oleander-design-process` gains `Semantic-dimension-to-form gate`:
1. classify input dimensions as `DISCRETE / CONTINUOUS / DIRECTIONAL / RELATIONAL / HIERARCHICAL / TEMPORAL`;
2. generate at least two mappings;
3. reject literal counting decoration when it does not preserve the relation;
4. remove labels/numbering/arrows/decorative color and retest form logic;
5. issue Validation Handoff when selected form implies technical geometry.

Promotion test:
`REMOVE LABELS + DECORATIVE COLOR → DOES THE FORM STILL PRESERVE THE RELATION TYPE, NOT MERELY THE NUMBER OF GRAPHIC ELEMENTS?`

## Skill Record
- Problem: compound claims collapse into literal decorative form.
- Trigger: Baojiajie jump-card `自带两档 / 使用久一点`.
- Inputs: claim copy, locked brand assets, retail POP constraints.
- Technique: semantic decomposition → orthogonal form roles → A/B → deletion test.
- Conditions: one input contains at least two different relation types.
- Expected Result: form logic survives label/decorative-cue removal.
- Failure Symptoms: badges for “two”; arrow for “longer”; generic burst with unchanged logic.
- Transfer Boundary: DESIGN only; production and claim truth require VALIDATION.
- Applicable Domains: Brand/POP, packaging, UI, product affordance, diagrams.
- Application Mapping: Baojiajie jump card.
- Status: CANDIDATE PRACTICE / NOT ACTIVE.

## Validation Handoff
See `BJ_POP_CLAIMFORM_R01_VALIDATION_HANDOFF.json`.
