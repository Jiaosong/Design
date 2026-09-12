# 2026-08-19｜Wayfinding / Brand / L5｜Map-derived Identity ↔ Functional Wayfinding Semantic Firewall

Status: **TRAINING EXECUTED / PRODUCER KEEP-FOR-TRAINING CANDIDATE / INDEPENDENT DESIGN REVIEW HOLD / NO_PROMOTION**

## Project trigger

Current C04 CH14 P06 v2.0 deliberately binds `LINE / TRACE / NODE-PAGE RELATION` to the locked `ROUTE-03` geometry and states that P06 owns route-derived brand grammar while P07 owns legend, icons, signage, information decoding, App/paper-map usability and functional contrast/state semantics.

The real risk is therefore not route geometry drift alone. A source-correct brand trace can still be visually styled like an instruction to move. Adding nodes, arrows, `START HERE`, or directional emphasis to a low-authority identity carrier silently borrows wayfinding authority even when the underlying path geometry is correct.

Recent training already covered World-Viewport Framing, Cartographic hierarchy, Icon Optical Normalization, Brand↔Operational-State Color Separation, Semantic Occlusion Priority, Responsive Media Art Direction and Prompt↔Media Binding. This round isolates **role-authority leakage between route-derived identity graphics and functional wayfinding**.

## Existing Skill reused

`skills/oleander-route-wayfinding-ui/`:
- topology and Return rules;
- guide authority ≠ optional content;
- topology before geometry;
- source-grounded truth boundaries;
- world-viewport framing.

Gap before this round:
- the Skill said route styling must not invent GPS/live state, but did not explicitly prevent a source-correct brand trace from visually impersonating navigation;
- no carrier-role declaration existed for `IDENTITY_TRACE / FUNCTIONAL_ROUTE`;
- no label-off/arrow-off false-affordance test;
- no blocker for adding current-position/direction cues to a carrier that does not own those semantics.

## Actual exercise

Editable 1920×1080 SVG uses one locked synthetic route geometry in three controlled carriers.

### A / KEEP — BRAND TRACE
Allowed: crop / trace / visual rhythm / identity placement.

Not allowed: directional arrow / `you are here` / live state / distance / movement instruction.

### B / REJECT — FALSE AFFORDANCE
Same geometry is decorated with nodes, arrow and `START HERE`. The path is still source-identical, but the carrier now looks like a functional navigation instruction without owning current-position/direction evidence.

### C / KEEP — FUNCTIONAL WAYFINDING
Same route geometry is used with bounded functional semantics: node role / current-context cue / Return / truth boundary / movement-decision hierarchy.

No image generation was used. All marks and text are editable vector content.

## Pixel readback and repair

First rendered preview failed compositionally: the shared route master overflowed the A/C panel bounds. This was a real finished-pixel defect even though the SVG exported successfully.

Repair:
- scale the same route master inside all three carriers;
- preserve identical route geometry;
- reposition dependent annotations without changing the semantic comparison;
- re-render full PNG and 50% grayscale derivative;
- reopen both for final visual readback.

Final hashes:
- SVG: `dfcf8d62eb582a4e54a127d028bfd1e2a032e7760edd8a02dd76fea066a468d5`
- PNG: `5edc5606988f41220c584e4b76560c70b932ee191659e544865bd8b60d5ba15e`
- Gray50 PNG: `ffadeae58788deb07e03f42c3dc9712fc211b42e925a4c546b653c7e30a69eca`

## Design Crit

### Compliance / execution
**PASS FOR TRAINING EXECUTION**
- editable SVG exists;
- vector text remains live;
- PNG and grayscale derivatives rendered;
- actual full-size PNG and Gray50 were visually reopened;
- no generated imagery;
- no C04 official route, GPS, direction, live state or signage approval is claimed.

### Producer frozen-rubric
**KEEP-FOR-TRAINING CANDIDATE**

- First visual: PASS. A/B/C role difference reads before long text.
- Composition: PASS after route-overflow repair; equal panels support controlled comparison without turning into a dashboard.
- Proportion: PASS. Route mark remains dominant inside each specimen; metadata stays subordinate.
- Hierarchy: PASS. Identity carrier / false-affordance diagnosis / functional decoding are distinct.
- Typography: PASS at current training scale; no observed clipping or missing glyphs.
- Material/spatial realism: not applicable as physical realism; route is explicitly synthetic/NTS.
- Scale: training carrier only; no signage viewing distance or production size claim.
- Node readability: PASS. Functional node/current context and Return are readable; brand carrier intentionally avoids node semantics.
- Interaction/narrative: PASS as a static semantic-role comparison; no runtime navigation claim.
- Professional finish: sufficient for training calibration, not C04 MAIN.

### Independent Professional Design Gate
**HOLD / REVIEW REQUIRED.**
No independently attributable professional reviewer is available in this run. Producer review is not promoted to independent KEEP.

## Failure knowledge

1. `SOURCE-CORRECT GEOMETRY ≠ FUNCTIONAL WAYFINDING AUTHORITY`.
2. A brand trace can become a false affordance without changing a single path coordinate.
3. Nodes and arrows are semantic operators, not neutral decoration.
4. `START HERE`, current-position dots, directional arrows and closure/state cues require a carrier that explicitly owns navigation semantics.
5. Lowering opacity does not remove false functional meaning.
6. A brand carrier may reference route identity but must not become the only place where Return or operational status is communicated.
7. The reverse failure also matters: a functional route should not be weakened until identity styling makes immediate decisions hard to decode.

## Repair method

`SOURCE ROUTE → CARRIER ROLE → ALLOWED SEMANTICS → PROHIBITED SEMANTICS → LABEL-OFF / ARROW-OFF ATTACK → FUNCTIONAL DECODING CHECK → TRUTH-BOUNDARY READBACK`

Required tests:
1. `CARRIER-ROLE` — declare `IDENTITY_TRACE / FUNCTIONAL_ROUTE / OPTIONAL_READING`.
2. `LABEL-OFF` — remove labels; identity carrier must not still imply unsupported movement.
3. `ARROW-OFF` — remove directional marks; functional carrier must still preserve current-context and Return logic.
4. `FALSE-AFFORDANCE` — attempt adding node/arrow/start marker to identity carrier; reject if it implies route decisions not owned by the carrier.
5. `RETURN-OWNERSHIP` — Return cannot live only in a brand/decorative layer.
6. `STATUS-OWNERSHIP` — CLOSED/UNKNOWN/NORMAL semantics belong to functional state carriers, not identity traces.
7. `GEOMETRY-IDENTITY` — identity and functional carriers may share route source geometry, but one cannot mutate it for graphic convenience.

Promotion test:
> Remove labels and arrows: if a brand-derived route trace still looks like an instruction to move, it is borrowing wayfinding authority and must be restated.

## Skill delta

Updated existing `skills/oleander-route-wayfinding-ui/VISUAL_LAYER_BINDING.md`.

Added **Brand-derived route graphic ↔ functional wayfinding semantic firewall**:
- explicit carrier roles;
- allowed/prohibited semantics per role;
- false-affordance attack tests;
- Return/status ownership rules;
- hard blocker for decorative carriers impersonating navigation;
- review fields for `CARRIER_ROLE / SOURCE_ROUTE / OWNED_SEMANTICS / PROHIBITED_SEMANTICS / FALSE_AFFORDANCE_RESULT / DOES_NOT_PROVE`.

No new standalone Skill is created.

## Cross-project transfer

Applicable to:
- C04 CH14 P06/P07 and ROUTE-03 derived identity/wayfinding;
- travel and museum systems where map geometry also appears in brand graphics;
- architecture/landscape identities derived from circulation/site traces;
- event/festival identities derived from venue maps;
- product/service systems where diagram geometry is reused decoratively and functionally.

Not directly applicable to:
- purely decorative abstract lines with no reasonable map/route reading;
- statutory/regulatory wayfinding where higher-authority standards prescribe symbols and semantics;
- data visualizations where arrows/nodes encode analytical variables rather than movement decisions;
- platforms where the brand carrier is explicitly also the authoritative navigation surface and that dual role is documented/tested.

## Truth boundary

`TRAINING ONLY / SYNTHETIC ROUTE / NTS / NOT GPS / FIELD OPEN / NO LIVE STATUS / NO SIGNAGE APPROVAL / INDEPENDENT DESIGN REVIEW HOLD / NO_PROMOTION`.
