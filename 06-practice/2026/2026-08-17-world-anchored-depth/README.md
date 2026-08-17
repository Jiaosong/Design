# OLEANDER Training — World-Anchored Relative Depth

Status: `TRAINING / CANDIDATE SKILL DELTA`

## Training question
How can route / exploration UI stop reading as a flat 2D overlay when the experience claim is spatially embedded, without inventing absolute distance or site geometry?

## Existing methods reused
- Candidate `oleander-ui-visual-composition`: First Visual Gate, world/UI layer logic, depth explains layers, project specificity, professional finish.
- Candidate `oleander-game-ui`: world-first hierarchy and UI/world cohesion.
- Candidate `oleander-route-wayfinding-ui`: preserve route truth and do not invent precision.
- OLEANDER no-loss, Existing Mature Design First, and independent Design Crit remain in force.

## Real project failure pattern
Recent QJ/C04 review exposed two related defects: ROUTE still read as a 2D UI overlay, and R13 did not convincingly carry the intended spatial compression/depth claim. The training isolates the transferable visual issue: route information can be correct while spatial embedding remains visually false or weak.

## External calibration
Established pictorial depth cues were used only as perceptual guidance: occlusion, relative size, perspective/convergence, texture gradient, and atmospheric/edge contrast. These indicate relative depth/order; they do not prove absolute metric distance, slope, GPS, or field geometry.

## Actual practice artifact
`world_anchored_depth_v2.svg` is an editable 1800×1100 vector calibration board. It compares the same route information in two treatments:
- A: `FLAT OVERLAY` — uniform terrain contrast, uniform marker scale, constant route weight, no occlusion, repeated screen-space cards.
- B: `WORLD-ANCHORED DEPTH` — near/mid/far hierarchy, occlusion, relative marker/line scale, atmospheric contrast, texture gradient, convergence, and labels attached to explicit world anchors.

All text remains vector/editable SVG text. No AI-generated image is used.

## Independent Design Crit
### v1 — REVISE
The depth stack was visually stronger than the flat overlay, but the middle ridge occluded/competed too strongly with the critical junction. The design gained depth while losing wayfinding clarity. `Spatial depth PASS` cannot override `critical decision readability FAIL`.

### v2 — KEEP as training asset
Repairs:
1. moved the critical junction into a clearer mid-depth aperture;
2. reconnected the route immediately after occlusion;
3. shortened/separated the leader from the ridge silhouette.

Observed result at full render:
- first visual: PASS — world/route relation reads before labels;
- composition: PASS — near/mid/far layers are distinct;
- proportion/hierarchy: PASS — marker and route weight decrease with depth role;
- typography: PASS — labels are secondary and attached to anchors;
- spatial realism: PASS only as **relative perceptual depth calibration**;
- scale: HOLD for real-world metric meaning; no metric claim is made;
- node readability: PASS after v2 repair;
- interaction: N/A for this static exercise;
- narrative: PASS — flat overlay vs spatially embedded relation is clear;
- professional finish: KEEP for training/calibration, not project promotion.

## Failure knowledge
- `glow / glass / shadow` do not create spatial embedding by themselves.
- `occlusion = depth` is incomplete: excessive occlusion can destroy route decisions.
- Uniform marker size, route weight, contrast, and floating cards make supposed near/mid/far layers collapse back into one screen plane.
- A perceptually convincing depth cue must never be translated into fake metres, slope, GPS precision, or field truth.
- Intentionally flat plans/maps are exempt; do not force pseudo-3D onto semantically flat information.

## Skill change
Existing candidate `skills/oleander-ui-visual-composition/SKILL.md` was extended with `World-anchored depth cue gate`. No new parallel skill was created.

## Cross-project transfer
Applicable to exploration routes, spatial web/UI, tourism interfaces, exhibition wayfinding, game-world overlays, landscape-first interaction, product/spatial relation viewers, and scene-based UI.

Not applicable as a mandatory treatment for technical plans, schematics, GIS/cartographic views, engineering drawings, or any interface where flatness is the correct semantic model.

## Truth boundary
`RELATIVE DEPTH ONLY / NTS / NO DISTANCE CLAIM / NO FIELD GEOMETRY CLAIM`.
