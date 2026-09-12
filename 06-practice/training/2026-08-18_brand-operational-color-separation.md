# 2026-08-18｜Game UI / Color System / L5｜Brand ↔ Operational State Color Separation

## Trigger
C04 CH14 and the Current System Locks explicitly state `BRAND COLOR ≠ OPERATIONAL STATUS COLOR`, while the current C04 App ROUTE model carries `NORMAL / DEGRADED / CLOSED / UNKNOWN`, Return priority and fail-closed behavior. Existing `KN-METHOD-COLOR-SYSTEM-001` already says Role Before Palette and forbids brand color everywhere as a consistency shortcut, but `skills/oleander-game-ui/VISUAL_LAYER_BINDING.md` did not yet turn this into a game/UI-specific state separation gate.

Recent training already covered Same-source Paired View, World-Viewport Framing, Small-Multiple Comparability, Exploration Motion Grammar, Cross-Screen Family Grammar, Experience↔Technical Proof, Prompt↔Media Binding and VI Optical Asset Handoff. This round therefore targets semantic color collision, not general hierarchy, motion, route framing or logo scaling.

## Existing knowledge reused
- Notion `KN-METHOD-COLOR-SYSTEM-001｜Color System｜角色—语义—媒介—生产—验证`.
- `skills/oleander-game-ui/VISUAL_LAYER_BINDING.md`.
- `skills/oleander-route-wayfinding-ui/SKILL.md` for Return / UNKNOWN / route truth boundary.
- OLEANDER Artifact Review System v1.1.

## Actual exercise
Editable 1920×1080 SVG: `OLEANDER_BRAND_OPERATIONAL_COLOR_SEPARATION_R01.svg`.

Controlled comparison:
- **REJECT**: Qingjiang-like brand teal is reused for brand header, route line and all four operational states. Without text the four states collapse into one meaning.
- **KEEP candidate**: brand teal remains in identity/passive context; operational states receive separate role tokens plus non-color redundancy through icon/shape, boundary style, label and behavior. UNKNOWN is visually unresolved and routes toward Return instead of reading as weak NORMAL.

No image generation used. The palette values are illustrative training tokens, not approved C04 palette values.

## Pixel readback
Full 1920×1080 PNG and a 50% grayscale derivative were opened after export. The KEEP side remains distinguishable without chroma because NORMAL / DEGRADED / CLOSED / UNKNOWN retain icon, shape, border and text differences. The REJECT side intentionally collapses after de-coloring.

## Design Crit
### Gate 1｜Execution / compliance
**PASS FOR TRAINING EXECUTION**
- editable SVG with live vector text;
- no AI-generated imagery;
- C04 route semantics are referenced without claiming live status, GPS or field verification;
- training tokens are explicitly non-authoritative.

### Gate 2｜Professional design
**Producer frozen-rubric finding: KEEP-FOR-TRAINING CANDIDATE**
- First visual: semantic collapse vs role separation is immediately visible.
- Composition: two-panel comparison is balanced; task hierarchy remains readable.
- Proportion: phone frames and state modules remain subordinate to the comparison thesis.
- Hierarchy: identity header → state modules → route context → diagnostic note.
- Typography: bilingual technical labeling remains legible at 50% readback.
- Material/spatial realism: not applicable beyond schematic UI; no material claim.
- Scale: training composition only; target-device accessibility proof remains OPEN.
- Node readability: route nodes and state cells remain distinguishable.
- Interaction/narrative: visual model supports fail-closed/Return semantics but static plate does not prove runtime behavior.
- Professional finish: training-grade KEEP candidate after actual pixel readback.

**Independent Professional Design reviewer provenance: HOLD / REVIEW REQUIRED.** Producer review is not represented as an independent review. No C04 Design PASS / MAIN promotion.

## Failure knowledge
1. `Brand color everywhere = consistency` can silently convert identity color into operational truth.
2. Correct state labels do not repair a color architecture that visually says all states are equivalent.
3. UNKNOWN rendered as a softer version of NORMAL is a semantic failure; uncertainty must stay visibly unresolved.
4. Interaction selection and operational availability are different state systems. A selected CLOSED node must not look OPEN.
5. Accessibility/contrast-tool PASS does not prove semantic color architecture is correct.

## Repairs that worked
- separate Identity / Interaction / Operational State lanes before choosing colors;
- add non-color redundancy to critical states;
- make CLOSED / UNKNOWN capable of suppressing brand chroma and optional effects;
- run Brand-off, Color-off/Grayscale and State-off readbacks;
- keep target-medium and accessibility proof explicitly separate from a training palette.

## Skill delta
Modified existing `skills/oleander-game-ui/VISUAL_LAYER_BINDING.md` rather than creating a new color or game-UI Skill.

Added:
- Current Color System METHOD as an inherited source;
- Brand ↔ operational-state color separation gate;
- Identity / Interaction / Operational State lane model;
- UNKNOWN / CLOSED priority rules;
- Brand-off / Color-off / State-off tests;
- hard failures for semantic borrowing and grayscale collapse;
- review-record fields and a promotion test.

Promotion test:
> Remove brand color, then remove status color: identity may weaken, but CLOSED / UNKNOWN meaning and Return priority must still survive.

## Cross-project transfer
Reusable for:
- C04 ROUTE / SERVICE / Return / status surfaces;
- travel and museum companion apps;
- game maps and exploration HUDs;
- mobility / booking / service-availability interfaces;
- web/app systems where brand identity coexists with operational state.

Do not apply mechanically to:
- purely editorial brand pages with no operational state;
- data visualization where color encodes quantitative/category structure instead of operational state;
- physical signage or printed safety systems without target-medium proof;
- platform-native accessibility/status conventions that have stronger current authority.

## Boundary
`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT GPS / STATUS UNKNOWN` remain unchanged. Artifact existence, GitHub write, CI or producer readback do not equal independent Design PASS.
