# 2026-08-18｜Story & Board / L5｜Prompt ↔ Media Semantic Binding

Status: `EXECUTED / PRODUCER CRIT COMPLETE / INDEPENDENT DESIGN REVIEW HOLD / NO_PROMOTION`

## Project trigger

C04 R05 Photo-dominant Research Audit recorded a real failure: the runtime prompt asked the visitor to observe the distance relation between peaks and the Qingjiang river surface, while the bound media contained no readable river surface. The audit explicitly prohibited using a Relation Mark to draw or imply the absent river and chose prompt revision as the controlled repair path.

This is distinct from recent OLEANDER training on Same-source Paired View, Exploration Motion Grammar, World-Viewport Framing, Small-Multiple Comparability, Cross-Screen Family Grammar, and Experience ↔ Technical Proof Co-registration. The unresolved skill gap is semantic binding between copy/instruction and the evidence actually visible in the current frame.

## Existing methods reused

- `oleander-story-and-board/SKILL.md`: evidence-to-story spine, strongest-current-evidence first, same-source paired-view gate.
- `oleander-story-and-board/VISUAL_LAYER_BINDING.md`: image-first hierarchy, authority preservation, non-destructive image-ops routing.
- OLEANDER Artifact Review System principle: engineering closure and design quality are separate gates.
- C04 truth boundary remains `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION`.

## Exercise

Produced a 1920×1080 editable SVG comparison using synthetic, non-C04 landscape geometry:

A. `REJECT — PROMPT OVERREACH`: peaks-only media + prompt asking for peak-to-river distance.
B. `KEEP CANDIDATE — REPAIR THE PROMPT`: same peaks-only media + narrowed prompt asking only for peak height, density and front/back layering.
C. `KEEP CANDIDATE — REPAIR THE MEDIA`: source-bound replacement media visibly includes both peaks and river + original peak-to-river relation prompt.

The exercise also identifies an invalid repair: drawing a fake river or adding a Relation Mark that implies one.

Artifact: `OLEANDER_PROMPT_MEDIA_BINDING_R01.svg`.
Local preview hash during production: SVG SHA256 `35d8bd9d92b9fec880fdab0c7fbc8117375f6f9d9f7b83bdd74ff90024b5d054`; PNG SHA256 `afee9c82c03a3e9543cfb96147ada9351196e71dcc015c33339540c1840244cf`.

## Design Crit

### Execution / compliance gate

`PASS FOR TRAINING EXECUTION`

- Editable vector source exists.
- Final 1920×1080 raster preview was actually rendered and opened after generation.
- All text remains vector text in SVG.
- No generative image was used.
- Synthetic geometry is explicitly labeled training-only and does not claim C04 site truth.

### Producer frozen-rubric visual review

`KEEP-FOR-TRAINING CANDIDATE`

- First visual: the three semantic states are distinguishable before reading the explanatory footer.
- Composition: three equal test columns are appropriate because the task is controlled comparison, while the REJECT/KEEP headers establish decision hierarchy.
- Proportion: media remains the dominant object inside each mobile frame; explanatory UI stays secondary.
- Hierarchy: title → decision state → media → prompt → diagnostic note.
- Typography: CJK and Latin text rendered cleanly in final readback; prompt copy remains readable at the produced scale.
- Material/spatial realism: deliberately schematic; sufficient only for relation-training, not field or photographic proof.
- Scale: mobile-frame proportions are illustrative, not ergonomic certification.
- Node readability: not applicable as a route-node technical drawing; prompt/media relation is the reviewed node.
- Interaction/narrative: static sequence clearly demonstrates failure → two valid repair paths.
- Professional finish: adequate for training evidence; not a C04 MAIN visual.

### Independent Professional Design Gate

`HOLD / REVIEW REQUIRED`

No reviewer with provenance independent from the producing agent was available in this run. Producer review is not relabeled as independent review. Therefore no production Design PASS or MAIN promotion is claimed.

## Failure knowledge

1. Plausible copy can still be visually false when its requested object/relation is not in frame.
2. An overlay, arrow, Relation Mark, glow, generative fill, or diagram trace cannot manufacture missing evidence.
3. Correct source attribution does not rescue a semantically mismatched crop.
4. Prompt/media pairs must be checked per viewport; a responsive crop can remove the evidence that made the desktop pair valid.
5. If the media is authoritative, narrow the prompt. If the claim is authoritative, replace the media. Do not redesign the evidence to preserve both.

## Skill delta

Modified existing `oleander-story-and-board/VISUAL_LAYER_BINDING.md`; no new isolated skill created.

Added `Prompt ↔ Media semantic binding gate` with:

- prompt parsing fields: `ACTION / OBJECTS / RELATION / REQUIRED_VISUAL_EVIDENCE / EVIDENCE_STATUS`;
- explicit rule that every demanded object/relation must be directly perceivable or qualified as inference/assumption/unknown;
- prohibition on overlays/generative edits manufacturing missing factual evidence;
- two valid repair routes: prompt narrowing or source-bound media replacement;
- per-viewport semantic binding checks;
- machine-readable pair record: `PROMPT_ID / MEDIA_SOURCE / MEDIA_VERSION / REQUIRED_OBJECTS / REQUIRED_RELATION / VIEWPORTS_CHECKED / STATUS / DOES_NOT_PROVE`;
- hard failure for visually polished frames whose copy asks the audience to inspect an absent relation.

Promotion test: `Every noun, relation and action demanded by the prompt must be directly perceivable or explicitly marked as inference/unknown.`

## Cross-project transfer

Applicable to:

- C04 landscape observation prompts, Route cues, Return/service states, R06/R13 captions and storyboard voice-over;
- travel and museum companion apps;
- map/wayfinding captions tied to visible route evidence;
- architecture/landscape boards where text instructs a spatial reading;
- product diagrams, exploded views and technical captions;
- video narration/subtitles whose claim must be supported by the current shot;
- data visualization annotations when the annotated relation must be visible in the chart.

Not applicable as a rigid rule when the communication is intentionally speculative, metaphorical, poetic, or explicitly labeled inference/assumption; in those cases the evidence status must remain visible and the frame must not masquerade as factual proof.

## Current closure state

`REAL ARTIFACT EXECUTED → ACTUAL PIXEL READBACK PASS → MATERIAL SKILL DELTA WRITTEN → TRAINING RECORD WRITTEN → GITHUB PR CANDIDATE → INDEPENDENT DESIGN REVIEW HOLD → NO_PROMOTION`.
