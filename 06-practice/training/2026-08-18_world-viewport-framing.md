# 2026-08-18｜Route / Wayfinding UI L5｜World-Viewport Framing

## Status
**COMPLIANCE PASS FOR TRAINING / PROFESSIONAL DESIGN KEEP FOR TRAINING / NOT C04 MAIN**

## Real project trigger
C04 Digital Companion has repeatedly exposed a mobile route failure mode: route/world content can be source-correct yet still read as a 2D UI overlay or mini-map when the complete network is miniaturized into a bounded card. The current `ROUTE-03` currentization record explicitly treats the phone as a viewport into a larger world rather than a shrunken desktop map, but the reusable `oleander-route-wayfinding-ui v0.1.0` only stated that principle and lacked executable framing checks.

This training does not reopen `ROUTE-03`, does not redraw current route authority, and does not promote PR #255 or any C04 App candidate.

## Existing Skill / recent training reused
- `oleander-route-wayfinding-ui v0.1.0`: one world / multiple readings; mobile viewport; Return; topology-before-geometry.
- `oleander-game-ui v0.1.1`: exploration behavior grammar only; not duplicated here.
- recent `Cartographic Task Hierarchy`: lineweight/contrast/task priority while geometry is held constant; not duplicated here.
- recent `Same-source Paired View`: source-geometry identity across paired presentation states; reused as a boundary, but this exercise is about mobile framing rather than story-board pairing.

## Training question
How can a mobile route screen preserve a sense of world, readable targets and continuity without inventing new route geometry or shrinking the complete network into a mini-map?

## Real exercise artifact
Editable 1920×1080 SVG + rendered PNG:
- `assets/OLEANDER_ROUTE_WORLD_VIEWPORT_FRAMING_R01.svg`

The artifact compares two treatments of the **same synthetic route/world geometry**:
1. **REJECT PATTERN / ALL-AT-ONCE MINI-MAP** — whole world scaled down into the phone; route, nodes and labels lose presence and the world reads as a UI card.
2. **KEEP PATTERN / WORLD-VIEWPORT** — geometry stays at an exploration-readable scale; phone crops the current region; active anchor enters a defined safe zone; persistent controls remain subordinate.

Training geometry is intentionally synthetic and labeled `NTS / NOT GPS / FIELD OPEN`. It proves only the framing method.

## Actual-preview Design Crit
### Gate 1｜Compliance / truth boundary
**PASS FOR TRAINING**
- same underlying world geometry reused between treatments;
- no site distance, GPS precision, opening state or field geometry claim;
- route/world remains schematic and training-only;
- editable SVG exists and final PNG was actually rendered and reopened.

### Gate 2｜Professional Design
**KEEP FOR TRAINING / NOT C04 MAIN**

- **First visual:** PASS. The contrast between the compressed mini-map and the spatial viewport is immediate before reading annotations.
- **Composition:** PASS after repair. Two phone frames have stable mass and equivalent review weight; the right-side viewport maintains stronger world presence without becoming a dashboard.
- **Proportion:** PASS. The KEEP state allocates materially more visible frame area to the spatial field while keeping controls bounded.
- **Hierarchy:** PASS. World → active anchor → persistent controls → explanation is legible; optional text does not own first read.
- **Typography:** PASS FOR TRAINING. Vector text remains subordinate to the diagram and is readable at 1920×1080; not a typography-system proof.
- **Material / spatial realism:** NOT APPLICABLE as site realism; schematic world depth is sufficient for this framing test but does not claim C04 landscape realism.
- **Scale:** HOLD FOR TARGET RUNTIME. The exercise shows relative framing logic only; it does not prove final device ergonomics or real target pixels.
- **Node readability:** PASS. KEEP state preserves an active anchor and safe-zone relationship at a usable visual size.
- **Interaction / narrative:** PASS AS STATIC STATE MODEL. Crop/pan/focus logic is visible; actual runtime pan, interruption and animation remain outside this artifact.
- **Professional completion:** KEEP FOR TRAINING. Final repaired artifact is coherent and reviewable; it is not a production C04 screen.

## Failure knowledge captured
### Failure 1｜Definition object accidentally rendered
The first SVG placed reusable world geometry in a normal `<g id="world">` instead of `<defs>`. The definition therefore rendered at full size behind the title, even though file export succeeded.

**Why it matters:** artifact existence and successful rendering do not prove composition quality. Reusable geometry definitions must be visually read back, not trusted from DOM intent.

**Repair:** move the world object into `<defs>` and re-render/reopen the final PNG.

**Do not repeat:** never accept an SVG training asset based only on parse/export success; reopen the final raster or browser frame after the last code edit.

### Failure 2｜“Show everything” treated as context
All-at-once network miniaturization preserves nominal completeness but destroys target size, spatial presence and world-first reading.

**Repair:** crop/pan/focus before scale-down; reserve full-network overview for a deliberate overview state.

### Failure 3｜Crop without continuity can become a different map
Cropping alone is insufficient if adjacent views lose all landmarks or if the route is redrawn to make the crop convenient.

**Repair:** lock authoritative world geometry and preserve at least one continuity landmark/segment/portal across adjacent viewport states.

## Skill delta
Updated existing `skills/oleander-route-wayfinding-ui/SKILL.md` from **v0.1.0 → v0.1.1**. No new Skill created.

### Before
The Skill said mobile route views are viewports into a larger world, but the rule was descriptive. It had no explicit test for crop vs scale-down, active-anchor occlusion, world-first proportion or continuity between viewport states.

### Added / tightened
- `World-viewport framing gate` under Core Principle 6;
- world geometry identity requirement;
- crop-before-scale-down rule;
- active-anchor safe zone;
- continuity-landmark requirement;
- target integrity and world-first proportion tests;
- overlay-restraint and truth-boundary stability checks;
- explicit promotion test: `If the phone must shrink the whole network to explain context, framing has failed.`;
- workflow framing pass and independent overview-vs-exploration comparison;
- hard failures for mini-map default, route redrawing, anchor occlusion, continuity loss and dashboard takeover;
- viewport fields in recommended data shape and review output.

## Cross-project transfer
Applicable to:
- C04 mobile ROUTE / route-child contexts and future map-based digital companion states;
- travel guides, museum/site navigation and visitor experience apps;
- game maps and exploration HUDs where a larger world is inspected through a mobile/small viewport;
- 3D viewer / plan viewer / spatial prototype interfaces where overview and focus states share one geometry authority.

Not applicable as a universal rule to:
- emergency/safety overview screens where the complete network must be visible immediately;
- command/control or dispatcher interfaces whose primary task is simultaneous full-system monitoring;
- printed static maps that cannot pan/crop interactively;
- cases where the authoritative geometry itself changes between scenarios;
- field navigation requiring surveyed/GPS precision unless that authority exists separately.

## Boundary
`Training KEEP ≠ C04 Design PASS ≠ Field PASS ≠ MAIN promotion.`

C04 truth remains `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT GPS / STATUS UNKNOWN` unless Current Authority changes it.
