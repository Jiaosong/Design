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
9. Review layer/depth logic.
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
DEPTH / LAYER LOGIC:
PROJECT SPECIFICITY:
RESPONSIVE / EDGE STATES:
PROFESSIONAL FINISH DEFECTS:
SEVERITY-ORDERED FIXES:
INDEPENDENT VERDICT REQUIRED: YES
```

## Source lineage
Distilled for OLEANDER from external visual-composition/front-end craft skills such as `ui-visual-composition` and `impeccable`, combined with OLEANDER's existing First Visual Gate, Existing Mature Design First, no-loss, and independent-review rules.