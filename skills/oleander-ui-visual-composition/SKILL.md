---
name: oleander-ui-visual-composition
description: OLEANDER visual UI composition and first-visual quality skill for hierarchy, composition, typography, imagery, spacing, depth, color, responsive pixel quality, and professional finish. Use for UI critique, redesign, pixel refinement, first-read review, and final visual QA.
status: candidate
version: 0.1.2
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
Establish hierarchy in grayscale using scale, placement, whitespace, grouping, crop, weight, overlap, and contrast. Color and glow may reinforce hierarchy but may not create it from nothing.

### 3. One dominant visual per state
A screen can contain many systems but should have one dominant visual/event at a time. Avoid equal-weight regions unless comparison itself is the task.

### 4. Group by meaning
Spacing and alignment must express relationships. Related objects are closer and more aligned than unrelated objects. Avoid ambiguous gaps and arbitrary decorative grids.

### 5. Typography is structure
Use a small deliberate scale. Differences must be perceptible, not accidental. Check Chinese legibility at real device size, line-height and line length, title-to-body ratio, label density, over-tracking, all-caps abuse, mixed-language hierarchy, and text competing with imagery.

### 6. Imagery owns the screen when imagery is the product
Protect real landscape/product imagery from UI clutter. Use controlled crop, scrim, local contrast protection, or quiet edge placement rather than large opaque cards.

### 7. Depth explains layers
Use overlap, scale, focus, shadow, blur, edge contrast, and parallax only when they clarify foreground/background, active/inactive, world/HUD, or entry/exit. Do not use glass, glow, shadow, blur, or border as generic premium decoration.

### 8. Cards are not the default
Use cards only when the content is genuinely a self-contained object. Do not solve weak composition by boxing every section. Nested cards are a hard warning sign.

### 9. Project specificity
The result must inherit visual evidence from the project: world imagery, material, cultural logic, geometry, typography, route/interaction language, or other authentic design source. A polished screen that could belong to ten unrelated apps is still weak.

### 10. Professional finish is a separate gate
Inspect alignment precision, optical balance, crop quality, line quality, icon consistency, focus/selected/disabled states, safe-area finish, responsive reflow, long text, empty/error/loading states, pixel artifacts, accidental overlap, and repeated generic motifs.

## Typographic density recomposition gate
Use this gate whenever a desktop/tablet composition is adapted to a narrow mobile viewport, or when a screen contains enough explanatory/evidence text that body copy risks becoming metadata-sized.

### Locked information
Responsive work must preserve required information, truth-boundary labels, primary actions, and source/evidence access. `No loss` protects information, not the desktop reading order or desktop line count.

### Allowed recomposition
At narrow width, explicitly reassign each text object to one of these reading roles:
- `PRIMARY CLAIM` — first-screen statement; must remain immediately readable;
- `ACTION` — primary/Return action; must not be demoted below evidence metadata;
- `CONTEXT` — short orientation text supporting the primary object;
- `OPTIONAL EXPLANATION` — may move into progressive disclosure/reveal;
- `EVIDENCE / PROVENANCE` — preserved and reachable, but need not occupy first-screen visual weight;
- `STATUS / TRUTH BOUNDARY` — compact but legible; never hidden when it changes user interpretation.

Recomposition may change order, line breaks, measure, grouping, disclosure, crop relationship, and spacing. It may not solve density by globally shrinking all typography.

### Native-width tests
Before promotion, inspect the actual narrow viewport, not only an enlarged artboard:
1. `3-SECOND READ` — primary object + primary claim + primary action are identifiable without close inspection.
2. `BODY-SIZE FLOOR` — explanatory body copy has not collapsed into label/metadata size merely to preserve desktop layout.
3. `ROLE-OFF TEST` — hide optional explanation/evidence detail; the screen still communicates its main task and Return path.
4. `EXPAND TEST` — reveal deferred explanation/evidence; information remains complete without destroying the primary hierarchy.
5. `LONG-COPY TEST` — realistic Chinese/English expansion does not force a global type shrink.
6. `390PX / TARGET NATIVE READBACK` — review at the real target width and pixel density used by the project.

### Hard failures
- responsive version is a uniformly scaled-down desktop composition;
- all desktop text remains above the fold only because body copy is reduced to metadata size;
- evidence/provenance is deleted rather than deferred or reorganized;
- primary action or Return becomes visually weaker than explanatory copy;
- title shortening changes the claim rather than recomposing its presentation;
- narrow layout requires zoom/close inspection to distinguish body text from labels;
- progressive disclosure is used to hide safety/status/truth information that changes interpretation.

### Promotion test
`At native narrow width, preserve information but reassign reading roles: the first screen must remain legible without shrinking body text into metadata.`

## Bilingual role pairing gate
Use this gate whenever two languages share the same UI surface and are intended to express the same claim, action, label, status, or metadata role.

### 1. Decide language authority before styling
Record whether the surface is:
- `LANGUAGE-PRIMARY` — one language owns first read; the companion language must remain semantically complete but visually subordinate;
- `EQUAL-LANGUAGE` — both languages have equal authority because of legal, public-service, accessibility, audience, or project requirements;
- `LANGUAGE-SWITCHED` — only one language is visible at a time.

Do not mechanically demote a language when authority requires equality. In equal-language contexts, redesign composition/measure rather than shrinking one language into metadata.

### 2. Pair by semantic role, not by language block
Create pairs such as:
- `CLAIM ↔ CLAIM`;
- `SUPPORT ↔ SUPPORT`;
- `ACTION ↔ ACTION`;
- `STATUS ↔ STATUS`;
- `META ↔ META`.

A translation does not automatically receive the same point size, weight, width, tracking, or line count. Optical weight is judged at target size, not by nominal font size alone.

### 3. Mixed-script composition discipline
- use proportional Latin letters and numerals; do not use fullwidth ASCII as an alignment shortcut;
- keep CJK–Latin spacing deliberate and consistent rather than manually inserting arbitrary spaces;
- protect identifiers, quantities, units, route IDs, state tokens, and short functional verbs from misleading line breaks;
- avoid all-caps or excessive Latin tracking when it creates a second first-read hierarchy;
- never reduce a companion language below practical legibility merely to preserve the primary-language composition.

### 4. Required tests
1. `CHINESE/OFF` — remove Chinese; the companion language alone still communicates the correct semantic role.
2. `ENGLISH/OFF` — remove English; the primary language alone still communicates the correct semantic role.
3. `PAIR-ON` — restore both; the companion language does not become a second hero unless authority explicitly requires equal weight.
4. `LINE-BREAK` — route IDs, quantities/units, NTS/status tokens, and action verbs do not split into misleading fragments.
5. `ALL-CAPS/TRACKING ATTACK` — Latin emphasis does not overpower intended hierarchy.
6. `NARROW-WIDTH` — bilingual pairing survives realistic wrapping without global shrink.
7. `EQUAL-LANGUAGE AUTHORITY` — if both languages are authoritative, both remain fully legible and the composition absorbs the added density.

### Hard failures
- Chinese and English are designed as two independent duplicate hierarchy trees on the same surface;
- translated title becomes a second first-read hero without an authority reason;
- bilingual button/control becomes paragraph-like and loses action recognizability;
- fullwidth Latin/ASCII is used to fake alignment;
- companion language is made unreadable to preserve the primary composition;
- equal-language public-service/legal content is visually demoted by default;
- identifiers/units/action tokens break in ways that change or obscure meaning.

### Promotion test
`Remove either language in turn: semantic identity must survive; restore both and the companion language must not create a second first-read hierarchy unless equal-language authority explicitly requires it.`

## Workflow
1. Open actual screenshots at target viewport.
2. Open strongest Existing Mature Design at matched scale.
3. Hide implementation/process information during first-read review.
4. Identify primary visual, primary action/decision, and scene hierarchy.
5. Run anti-pattern scan: dashboard, card wall, giant header, tiny labels, decorative glow, nested borders, over-framing, generic gradients, unmotivated blur.
6. Review composition and crop.
7. Review typography and density; invoke the Typographic Density Recomposition Gate for narrow/responsive states and the Bilingual Role Pairing Gate for mixed-language surfaces.
8. Review color roles and contrast.
9. Review layer/depth logic.
10. Review project specificity.
11. Review responsive/edge states at native target width.
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
- bilingual translation creates an unjustified second first-read hierarchy;
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
TYPOGRAPHIC ROLE MAP:
LANGUAGE AUTHORITY:
BILINGUAL ROLE PAIRS:
MIXED-SCRIPT READBACK:
NATIVE-WIDTH READBACK:
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
Distilled for OLEANDER from external visual-composition/front-end craft skills such as `ui-visual-composition` and `impeccable`, combined with OLEANDER's existing First Visual Gate, Existing Mature Design First, no-loss, responsive recomposition, and independent-review rules. Mixed-script constraints are additionally calibrated against W3C Chinese Layout Requirements (CLReq); those requirements inform text-engine behavior and do not define OLEANDER visual style.