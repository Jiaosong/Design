# 2026-08-18｜Game UI / Visual Composition L5｜Cross-Screen Family Grammar

## Training question
How can peer screens feel like one authored product family without forcing unrelated tasks into the same card template?

## Real project trigger
Current C04 Digital Companion keeps `TODAY / ROUTE / MY BOOK / SERVICE` in the IA, while current materialization is uneven: ROUTE and SERVICE are materially authored; TODAY and MY BOOK remain weaker/placeholding surfaces. Recent C04 review also identified uneven game-like quality across peer screens.

Recent training already covered Same-source Paired View, Exploration Motion Grammar, World-Viewport Framing, Small-Multiple Comparability, Cartographic Task Hierarchy, Shared Container Continuity and Attention-State Composition. This round therefore does not repeat motion, route framing, chart scale, or single-screen hierarchy.

## Existing skills / methods reused
- `skills/oleander-game-ui/SKILL.md` v0.1.1 — world-first, anti-dashboard, state-specific HUD, Exploration Motion Grammar.
- `skills/oleander-game-ui/VISUAL_LAYER_BINDING.md` — existing visual binding and independent-review inheritance.
- `oleander-ui-visual-composition` — first-read, hierarchy, typography and finish.
- `oleander-ui-interaction` — Return / interruption / state authority.
- OLEANDER Artifact Review System v1.1 — engineering/compliance and Professional Design remain separate.

No new Skill or framework was created.

## Practice artifacts
- `OLEANDER_CROSS_SCREEN_FAMILY_GRAMMAR_REJECT.svg` — intentional template-lock failure.
- `OLEANDER_CROSS_SCREEN_FAMILY_GRAMMAR_R01.svg` — corrected four-screen family grammar.

The exercise uses editable vector geometry and live text only. No generative image tool was used.

REJECT construction: TODAY / ROUTE / MY BOOK / SERVICE use the same central card, same icon shell and same action pattern; labels carry almost all identity.

Corrected construction: shared typography roles, edge rhythm, quiet metadata, Return placement, anchor language, spacing and chrome proportion remain stable while each screen receives a task-specific primary object:
- TODAY → temporal / landscape rhythm;
- ROUTE → continuous route + current anchor;
- MY BOOK → open-page / personal-trace object;
- SERVICE → return / support beacon.

## Actual preview / regression
Final PNG was reopened at full 1920×1080. A 50% grayscale derivative was also rendered and reopened.

Observed:
- REJECT: removing labels would collapse all four screens into the same generic card.
- R01: mode identity remains legible from primary silhouette/composition; grayscale still preserves family cohesion, so consistency is not color-only.
- R01 at 50%: main objects, shared edge rhythm, typography roles and Return line remain readable.

## Design Crit
### Gate 1 — execution / compliance
`PASS FOR TRAINING EXECUTION`
- editable SVG master exists;
- PNG actual-preview readback complete;
- no image generation;
- truth boundary visible;
- no project route/GPS/field fact invented;
- artifact remains training-only / NTS / FIELD OPEN / NOT C04 MAIN.

### Gate 2 — Professional Design
Producer frozen-criteria finding: `REVISE → corrected to KEEP-FOR-TRAINING CANDIDATE`, but **independent reviewer provenance is unavailable in the current tool surface**, so independent Professional Design Gate remains `HOLD / REVIEW REQUIRED`. No producer self-promotion to C04 MAIN or Design PASS is claimed.

Criteria on corrected R01:
- First visual: PASS — four task-specific silhouettes read before explanatory copy.
- Composition: PASS — shared device/edge rhythm, distinct internal compositions.
- Proportion: PASS — primary object dominates chrome on every screen; Service remains the densest but not panel-first.
- Hierarchy: PASS — task object → local meaning → quiet metadata/Return.
- Typography: PASS in actual preview and 50% derivative; live vector text retained.
- Material/spatial realism: PASS only as schematic UI language; not a field/site claim.
- Scale: PASS for board/readback scale; target-device ergonomics remains HOLD.
- Node readability: PASS where applicable; ROUTE has one dominant current anchor.
- Interaction/narrative: PASS at static family-grammar level; runtime behavior not proven.
- Professional finish: sufficient for training evidence; not sufficient for C04 MAIN without target-runtime binding and independent review.

## Failure knowledge
1. **Template lock is not coherence.** Repeating the same card shell across tasks creates sameness but erases mode identity.
2. **Color/logo is weak family evidence.** A family that collapses in grayscale is styling, not grammar.
3. **Text cannot carry task identity alone.** If removing titles makes peer screens indistinguishable, the primary visual object is under-authored.
4. **Task variation can overcorrect into family drift.** Different primary objects do not authorize random typography, Return placement, spacing, HUD density or state semantics.
5. **Chrome cannot become the stable hero.** Shared navigation/chrome should support continuity, not become more visually dominant than the task-specific object.

Invalid fixes:
- clone one card and change only labels/icons;
- add a shared accent color and call the set coherent;
- increase glow or decoration to make weak screens feel more game-like;
- make every mode use the ROUTE composition even when its task is memory or service.

## Skill delta
Modified existing `skills/oleander-game-ui/VISUAL_LAYER_BINDING.md`; no new Skill.

Previous gap: `oleander-game-ui` v0.1.1 already controlled world-first hierarchy and cross-screen motion semantics, but did not define how peer screens should share visual roles while preserving task-specific composition. A product could therefore pass motion grammar while TODAY / ROUTE / MY BOOK / SERVICE still looked like unrelated products — or solve that by cloning one generic card template.

Added `Cross-screen family grammar gate`:
- lock/bound typography roles, edge rhythm, stroke/radius/spacing vocabulary, active-anchor treatment, Return priority, HUD density and primary-object/chrome proportion;
- explicitly allow task-specific primary silhouettes, content geometry, local density and controls;
- add title-off, color-off, 50% compact, template-lock and family-drift tests;
- add hard failures for identical-card dependence, color/logo-only cohesion, panel-first drift, chrome dominance and title-dependent mode identity;
- promotion test: `If screen titles and accent color are removed, peer screens should still feel like one product while each screen remains identifiable by its task-specific primary object.`

## Cross-project transfer
Applicable to:
- C04 TODAY / ROUTE / MY BOOK / SERVICE and future peer companion screens;
- travel and museum companions;
- game-like exploration HUD families;
- map + journal + service ecosystems;
- mobile/web/kiosk products with several task modes sharing one world or brand language;
- 3D viewers where browse / inspect / annotate / return are peer modes.

Do not apply mechanically to:
- emergency / dispatch / command-control surfaces where explicit safety semantics dominate;
- payment, consent, delete or other irreversible transactional flows governed by platform conventions;
- partner/embedded surfaces intentionally owned by another brand/system;
- radically different modalities where shared composition would reduce accessibility;
- any case where safety/accessibility/platform authority requires changing the shared roles.

## Truth boundary
`TRAINING ONLY / NO IMAGE GENERATION / NTS / FIELD OBSERVED=0 / FIELD MEASURED=0 / NOT C04 MAIN / TARGET RUNTIME HOLD / INDEPENDENT DESIGN REVIEW HOLD`.
