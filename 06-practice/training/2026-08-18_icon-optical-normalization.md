# 2026-08-18｜Icon System / L5｜Optical Normalization Across Carriers

Status: **KEEP-FOR-TRAINING CANDIDATE / INDEPENDENT DESIGN REVIEW HOLD / NO_PROMOTION**

## Project trigger
C04 CH14-P07 requires Signage / Map / App to share a visual grammar while preserving functional reading efficiency. Recent pictogram training on a 24 px Return + walk transfer already exposed a real failure: the return arrow and walking body began to merge at 24 px and required a v1→v2 repair. The remaining gap is cross-carrier optical normalization: the same semantic icon may appear at materially different target sizes, but one master cannot be assumed to survive mechanical scaling.

This round intentionally does not repeat recent training on attention hierarchy, motion grammar, world viewport framing, small-multiple comparability, prompt-media binding, brand/status color separation, or evidence-state styling.

## Reused existing knowledge
- `skills/oleander-ui-visual-composition/SKILL.md` — First Visual Gate, target-size pixel review, icon consistency, professional finish.
- Notion practice `2026-08-17｜Pictogram / Icon Design / L5｜24px 动作轮廓与关节负空间` — action silhouette topology + critical joint gaps; v1 failed, v2 passed for practice.
- C04 CH14-P07 — Signage / Map / App share visual grammar but functional reading efficiency has priority.

## External mechanism check
Only primary/official sources were used for mechanism calibration:
- Google Material Symbols documentation: optical-size (`opsz`) axis adjusts symbol stroke behavior across 20–48 dp. https://developers.google.com/fonts/docs/material_symbols
- Microsoft Fluent System Icons: distributes separate icon assets for multiple sizes including 16/20/24/28/48 instead of assuming one master is always sufficient. https://github.com/microsoft/fluentui-system-icons/tree/main/packages/svg-icons

Transfer boundary: OLEANDER adopts the optical-normalization mechanism, not Material/Fluent appearance or trade dress.

## Real exercise
Editable vector asset: `06-practice/training/assets/OLEANDER_ICON_OPTICAL_NORMALIZATION_R01.svg`.

Synthetic semantic: `RETURN`.
Carriers tested:
- MAP = 16 px
- APP = 24 px
- SIGNAGE = 32 px

A controlled REJECT family uses one 32 px master mechanically scaled to 24 and 16. The KEEP candidate uses three optical variants with the same semantic topology.

Locked invariants:
- U-turn direction;
- human forward lean;
- arrow/body separation;
- head/body gap;
- route endpoint remains open.

Allowed compensation:
- relative stroke increases as size decreases;
- critical gaps enlarge;
- secondary joints/details simplify;
- arrow shortens;
- local overshoot / whitespace rebalancing is allowed.

## Actual readback
Rendered full board at 1920×1080 and reopened at actual pixels. Also generated a 50% grayscale readback.

Observed failure in REJECT family:
- enlarged specimens appear acceptable;
- native 16 px readback begins to fuse head/body/return-arrow information;
- the semantic technically remains present, but first-read becomes noise.

Observed KEEP candidate result:
- 32 px retains the fuller relation;
- 24 px simplifies joints and protects arrow/body separation;
- 16 px further protects critical gaps and strengthens relative mass without changing U-turn direction or walking-body relation;
- grayscale does not remove the essential distinction.

Local artifact hashes:
- SVG SHA-256: `61a6b84e943dc6e216b0d1689dfc07e70aaacac25dfed6aa6c63ace5dcaeb508`
- PNG SHA-256: `e7d73592325b4bd58d9d6b21212ed04b68fefe473f514df2fa574fd053a5853b`
- 50% grayscale PNG SHA-256: `87a82cfc409913f00194cd1aca00de664041828fb50bed6bf7aa0e063d281a10`

## Design Crit
### Execution / compliance gate
**PASS FOR TRAINING EXECUTION**
- editable SVG exists;
- text remains vector text;
- PNG rendered and reopened;
- 50% grayscale readback executed;
- no AI image generation used;
- synthetic Return geometry is not presented as C04 official icon, field direction, signage standard, or safety instruction.

### Producer frozen-rubric
**KEEP-FOR-TRAINING CANDIDATE**
- First visual: PASS — reject vs optical-family logic reads before explanatory text.
- Composition: PASS — two controlled comparison fields; no accidental equal-weight dashboard because comparison is the task.
- Proportion: PASS — native-size strip is subordinate but present; enlarged specimens do not replace native readback.
- Hierarchy: PASS — semantic family → carrier size → invariants → promotion test.
- Typography: PASS — Chinese/English labels remain readable at board scale.
- Material/spatial realism: N/A for a vector icon-system exercise; no physical signage finish is claimed.
- Scale: PASS FOR TRAINING — actual 16/24/32 px instances are embedded; production viewing distance remains OPEN.
- Node readability: PASS — critical arrow/body and head/body gaps remain visible in KEEP family.
- Interaction/narrative: PASS FOR STATIC SEMANTIC STUDY — Return direction is legible; no runtime interaction is claimed.
- Professional finish: PASS FOR TRAINING — geometry, labels, alignment, and grayscale readback are controlled.

### Independent design gate
**HOLD / REVIEW REQUIRED**
No reviewer identity independent from the producer is available in the current tool surface. Producer readback must not be promoted to independent KEEP.

## Failure knowledge
1. `SAME FAMILY ≠ SAME MASTER SCALE()`.
2. Enlarged icon specimens can hide native-size failure.
3. Global stroke thickening is not a valid universal fix; it can close the very gaps that carry action semantics.
4. A small optical variant may simplify, but it may not change direction, topology, attachment point, or action meaning.
5. Map/App/Signage variants should not drift into unrelated pictogram idioms unless Current Authority requires different semantics.
6. Copying Material/Fluent appearance would be a transfer failure; only the optical-sizing mechanism is reusable.

## Skill delta
Modified existing `skills/oleander-ui-visual-composition/SKILL.md`, version `0.1.0 → 0.1.1`.

Before: the Skill mentioned icon consistency and target-size pixel QA but did not require multi-size semantic invariants, native-size family strips, or bounded optical compensation.

Added `Icon optical normalization gate` with:
- semantic invariants before optical correction;
- allowed compensation rules;
- native-size / one-size-down / grayscale / label-off / family-strip tests;
- hard failures for mechanical scale-down, all-stroke rescue, enlarged-review-only acceptance, semantic fusion, topology drift, carrier-family drift, and external trade-dress copying;
- machine-review fields and a promotion test.

Promotion test:
`Compare at native carrier size: semantic topology must stay constant, while critical gaps and stroke survive without making small sizes a different icon.`

## Cross-project transfer
Applicable to:
- C04 Return / Route / Service support symbols across App, map and signage;
- compact Web UI controls and dense tables;
- museum/travel wayfinding systems;
- product/service apps with responsive icon families;
- multi-scale dashboard and map annotation systems;
- branded service icons where identity and action semantics must survive size changes.

Not automatically applicable to:
- platform-native icons whose geometry is externally authoritative;
- emergency/regulatory signage governed by a higher standard;
- illustrations or decorative symbols that are not expected to work independently at small size;
- cases where different carriers intentionally communicate different semantics rather than the same semantic ID;
- physical signage sizes until viewing-distance, substrate, fabrication and accessibility proof exists.

## GitHub closure state
- Branch: `training/20260818-icon-optical-normalization`
- PR: `#277 Training: add icon optical normalization gate`
- Material delta: 3 files; Skill + training record + editable SVG.
- CI observed on pre-closure head `d8a064dde604fed0c43c1c7175b743913f7be715`: `AI Governance Evals #2037 = completed / success`.
- This closure-record commit changes the PR head after that CI result; final-head CI must be read back again before any merge consideration.
- Independent Professional Design Gate remains `HOLD`, therefore CI success cannot authorize merge or promotion.

## Truth boundary
This exercise does not currentize C04 official icon geometry, map direction, operational state, field truth, safety instruction, accessibility compliance, signage dimensions, or production materials. `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION` remain unchanged.