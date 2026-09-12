---
name: oleander-ui-visual-composition
description: OLEANDER visual UI composition and first-visual quality skill for hierarchy, composition, typography, imagery, spacing, depth, color, responsive pixel quality, and professional finish. Use for UI critique, redesign, pixel refinement, first-read review, and final visual QA.
status: candidate
version: 0.1.0
---

# OLEANDER UI Visual Composition

## Purpose
Turn correct product logic into visually convincing finished pixels. This skill exists because evidence correctness, runtime correctness, and design-system cleanliness do not prove visual quality.

It is the UI-specific extension of OLEANDER's First Visual Gate.

## Authority discipline
- Read Current Authority and Existing Mature Design before judging a new version.
- Compare new pixels against the strongest relevant existing design at matched scale.
- Preserve concept/content when pixels fail. `Pixel Fail ≠ Design Delete`.
- Independent reviewer owns final visual verdict. Producer may only list observed qualities/defects and implementation evidence.

## First-read order
Review the actual rendered screen at target size before reading implementation notes.

Within 3 seconds, answer:
1. What is the primary visual object?
2. What is the primary user decision/action?
3. What is secondary?
4. Does the screen feel specific to this project or generically generated?
5. Is the visual hierarchy coming from composition, or from boxes/labels explaining the composition?

If these answers are unclear, stop and fix hierarchy before polish.

## Core principles
### 1. Feature before shell
Design the object/task first. Navigation chrome, headers, cards, frames, labels, and decorative panels are secondary.

### 2. Hierarchy before color
Establish hierarchy in grayscale using:
- scale;
- placement;
- whitespace;
- grouping;
- crop;
- weight;
- overlap;
- contrast.

Color and glow may reinforce hierarchy but may not create it from nothing.

### 3. One dominant visual per state
A screen can contain many systems but should have one dominant visual/event at a time. Avoid equal-weight regions unless comparison itself is the task.

### 4. Group by meaning
Spacing and alignment must express relationships. Related objects are closer and more aligned than unrelated objects. Avoid ambiguous gaps and arbitrary decorative grids.

### 5. Typography is structure
Use a small deliberate scale. Differences must be perceptible, not accidental.

Check:
- Chinese legibility at real device size;
- line-height and line length;
- title-to-body ratio;
- label density;
- over-tracking / fake sophistication;
- overuse of all caps;
- mixed language hierarchy;
- text competing with imagery.

### 6. Imagery owns the screen when imagery is the product
Protect real landscape/product imagery from UI clutter. Use controlled crop, scrim, local contrast protection, or quiet edge placement rather than large opaque cards.

### 7. Depth explains layers
Use overlap, scale, focus, shadow, blur, edge contrast, and parallax only when they clarify foreground/background, active/inactive, world/HUD, or entry/exit.

Do not use glass, glow, shadow, blur, or border as generic “premium” decoration.

### 7.1 World-anchored depth cue gate
Use this gate when a route, exploration layer, object marker, scene relation, or HUD claims to sit **in or across the world** rather than on a deliberately flat map/schematic.

1. **Declare the spatial mode before styling.** Classify the composition as `SCREEN-SPACE`, `WORLD-ANCHORED`, `WORLD-SPACE`, or deliberately `FLAT / CARTOGRAPHIC`. Do not imply world anchoring when the design is only a flat overlay.
2. **Use more than one truthful cue.** A world-anchored composition should normally combine at least two appropriate relative-depth cues such as occlusion, relative scale, perspective/convergence, texture gradient, atmospheric/edge contrast, or focus hierarchy. Shadow/glow alone do not establish spatial depth.
3. **Depth cue ≠ distance proof.** Relative-depth cues may communicate near/mid/far order but may not be translated into metres, slope, GPS precision, verified geometry, or site truth without independent evidence.
4. **Labels resolve to anchors.** Screen-space labels are allowed, but each claim-bearing label must resolve clearly to a world/object/route anchor through adjacency, leader, attachment, tracking, or another unambiguous relation. Repeated floating cards with no anchor default to `REVISE` when world cohesion is the intent.
5. **Route continuity survives occlusion.** Occlusion may create depth, but it must not permanently hide a critical decision node, Return cue, safety state, or required route transition. Reappearance must be visually recoverable.
6. **Scale and contrast follow depth role.** Near/mid/far markers should not all use identical size, line weight, edge contrast, and label treatment unless equal perceptual weight is intentional and justified.
7. **World first, ornament second.** The first read should be world/route/object relationship. Decorative HUD glass, glow, scanlines, vignette, blur, or border cannot substitute for spatial construction.
8. **Test at target views.** Reopen the actual rendered composition at intended viewport(s) and check near/mid/far separation, anchor readability, route continuity, and label collision. Small-screen recomposition may require different anchor placement while preserving the same route truth.
9. **Static proof has limits.** A still frame can verify overlap, scale, texture, atmospheric contrast, and perspective cues. It cannot prove parallax, tracked anchoring, camera behavior, or runtime world-space attachment; those require runtime evidence.
10. **Flat modes are exempt.** Do not force pseudo-3D depth into a plan, schematic, technical map, or intentionally flat cartographic view when flatness is semantically correct. The gate applies to claimed spatial embedding, not to all maps.

Failure pattern: uniform line width + uniform marker scale + uniform contrast + repeated floating cards across supposed depth layers is a `VISUAL-WORLD-COHESION` defect, even if route data and UI code are correct.

### 8. Cards are not the default
Use cards only when the content is genuinely a self-contained object. Do not solve weak composition by boxing every section.

Nested cards are a hard warning sign.

### 9. Project specificity
The result must inherit visual evidence from the project: world imagery, material, cultural logic, geometry, typography, route/interaction language, or other authentic design source.

A polished screen that could belong to ten unrelated apps is still weak.

### 10. Professional finish is a separate gate
Inspect:
- alignment precision;
- optical balance;
- crop quality;
- line quality;
- icon consistency;
- focus/selected/disabled states;
- safe-area finish;
- responsive reflow;
- long text;
- empty/error/loading states;
- pixel artifacts;
- accidental overlap;
- repeated generic motifs.

## Workflow
1. Open actual screenshots at target viewport.
2. Open strongest Existing Mature Design at matched scale.
3. Hide implementation/process information during first-read review.
4. Identify primary visual, primary action/decision, and scene hierarchy.
5. Run anti-pattern scan: dashboard, card wall, giant header, tiny labels, decorative glow, nested borders, over-framing, generic gradients, unmotivated blur.
6. Review composition and crop.
7. Review typography and density.
8. Review color roles and contrast.
9. Review layer/depth logic; invoke the world-anchored depth cue gate when spatial embedding is claimed.
10. Review project specificity.
11. Review responsive/edge states.
12. Produce findings by severity; do not average away a weak first visual.
13. Independent reviewer decides `KEEP / REVISE / REJECT / HOLD` and any numeric score if the project uses one.

## Hard failure conditions
- first read is a header/card/dashboard rather than the intended world/object/task;
- primary object is visually smaller/weaker than explanatory UI;
- important regions have equal visual weight without a comparison reason;
- dense labels or tiny text are required to understand the screen;
- layout is held together by borders and cards rather than composition;
- image crop contradicts the experience claim;
- visual effect masks a usability or truth-boundary problem;
- decorative UI reduces world/product readability;
- responsive version is a scaled-down desktop composition;
- world-anchored intent collapses into a flat overlay with no readable spatial relation;
- occlusion used for depth hides a critical route decision, Return, or safety cue;
- new version is visually weaker than a mature existing source without a justified tradeoff.

## Review format
```text
OBJECT / VIEWPORT:
BEST EXISTING COMPARISON:
3-SECOND FIRST READ:
PRIMARY VISUAL:
PRIMARY ACTION / DECISION:
COMPOSITION:
TYPOGRAPHY:
IMAGERY / CROP:
COLOR / CONTRAST:
SPATIAL MODE: SCREEN-SPACE / WORLD-ANCHORED / WORLD-SPACE / FLAT-CARTOGRAPHIC
DEPTH CUES USED:
ANCHOR / OCCLUSION / ROUTE CONTINUITY:
DEPTH / LAYER LOGIC:
PROJECT SPECIFICITY:
RESPONSIVE / EDGE STATES:
PROFESSIONAL FINISH DEFECTS:
SEVERITY-ORDERED FIXES:
INDEPENDENT VERDICT REQUIRED: YES
```

## Source lineage
Distilled for OLEANDER from external visual-composition/front-end craft skills such as `ui-visual-composition` and `impeccable`, combined with OLEANDER's existing First Visual Gate, Existing Mature Design First, no-loss, and independent-review rules. The world-anchored depth cue gate additionally uses established visual-perception depth cues only as relative perceptual guidance; it does not turn those cues into project geometry or field evidence.