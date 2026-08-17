---
name: oleander-story-and-board
description: Turn Oleander research, data, design logic, renders, and brand strategy into coherent boards, reports, decks, storyboards, and promotional narratives. Use whenever the user mentions Oleander project compilation, exhibition boards, design books, presentations, brand stories, scripts, storyboards, key visuals, InDesign, Illustrator, Figma, PowerPoint, or connecting analysis to a persuasive narrative.
compatibility: May use Notion, documents, presentations, PDF, Figma, InDesign, Illustrator, Photoshop, After Effects, Premiere, and LibreOffice.
---

# Oleander Story and Board

Build a single evidence-to-story spine so reports, boards, decks, and films tell the same project rather than becoming unrelated artifacts.

## Narrative spine

Define:

1. Context: what situation exists?
2. Tension: what is missing, changing, or contested?
3. Insight: what did research reveal?
4. Proposition: what does Oleander do?
5. System: how does the design work?
6. Experience: what will people see, feel, and do?
7. Proof: what evidence, analysis, or prototype supports it?
8. Invitation: what should the audience believe or do next?

Every section should have one primary claim and one primary visual.

## Existing mature design / evidence first

Before rebuilding a board visual, identify the strongest current spatial/design evidence already available. Reuse, edit, currentize, restructure, or deepen it before creating a substitute.

For maps, routes, plans, sections, model views, product geometry, technical nodes, diagrams, and other spatial evidence:

- The board is a **presentation layer**, not a new geometry authority.
- Preserve locked/current/strongest mature geometry. Do not stretch, flatten, straighten, re-author, simplify, or normalize it merely to make the page cleaner.
- If a layout conflicts with authoritative geometry, change the grid, crop, sequence, image scale, or page allocation — **not the evidence geometry**.
- For alternative journeys, phases, audience modes, states, or scenarios, show differences by masking/highlighting/subsetting the authoritative source. Do not redraw every variant into a visually uniform but spatially false shape.
- If an older/current artifact has stronger spatial credibility than a new derivative, keep the stronger artifact as the design source and revise only the presentation layer. Newer file ≠ stronger design.
- Context images and renders may establish atmosphere or spatial character, but they must not visually imply a false exact correspondence to map/node geometry.

A visually stronger board that weakens spatial truth is a regression and must be REVISE/REJECT rather than promoted.

## Assembly workflow

1. Pull approved claims and sources from Notion.
2. Pull validated charts from `oleander-data-viz`.
3. Pull model manifests and approved renders from `oleander-3d-pipeline`.
4. Create a content inventory before layout.
5. Resolve the strongest current design/evidence source for every primary visual; record which objects are locked and may not be re-authored by layout.
6. Establish grid, hierarchy, type system, palette, caption style, image treatment, and page/board numbering around those authority objects.
7. Produce a low-fidelity sequence before polishing.
8. Reuse the same narrative IDs across report sections, boards, deck slides, and film scenes.
9. Run content, visual, and production reviews separately.
10. For spatial primary visuals, perform an authority-preservation comparison against the strongest existing artifact before promotion.

## Deliverable variants

- Board: distance-readable hierarchy, restrained text, explicit sequence.
- Report/book: evidence depth, citations, cross-references, appendices.
- Deck: one decision or claim per slide.
- Brand story: human motivation, distinctive promise, proof, voice.
- Film storyboard: scene purpose, image, motion, narration, sound, duration, source assets.

## Required output

Return the narrative outline, content inventory, page/board/scene map, missing-assets list, production specification, and final editable/source deliverable.

For any layout containing source-bound spatial evidence, include a short authority-preservation note naming the source object and confirming what was kept unchanged versus presentation-only edits.

## Evidence-bound figure caption gate

When a figure's truth state materially changes how it may be interpreted, treat the caption as part of the evidence object rather than a remote footer.

- Keep `figure_id`, source/evidence class, the figure's primary claim, and any material `DOES NOT PROVE` boundary visually adjacent to the figure.
- Use one compact caption band or a tightly associated caption block by default. Do not turn evidence metadata into a competing dashboard, card grid, or second primary visual.
- The caption must identify **what the figure proves** and, where necessary, **what it does not prove**. A visually authoritative image without an adjacent boundary is incomplete evidence communication.
- If a figure contains a specific relation, node, crop, state, or detail that carries the claim, bind the caption to that visual object with a stable ID, local label, callout, or other explicit relation rather than relying on prose alone.
- Keep source class and limitation readable at the intended near-read scale. Do not hide them in an appendix, hover state, tiny legal footer, or source page if omission would change interpretation of the figure.
- Do not let truth-boundary text dominate the first visual. The project object/figure remains first-read; evidence state is near-read support.
- For repeated figures in boards, reports, web pages, and film, preserve the same `figure_id` and evidence role so that a derivative caption cannot silently strengthen or weaken the source claim.
- `SOURCE-GROUNDED`, `INFERRED`, `ASSUMPTION`, `AI-ASSISTED`, `NTS`, `FIELD OPEN`, `NOT SITE PHOTO`, and similar state labels must retain their semantic distinction; do not collapse them into a generic disclaimer style.
- If the full boundary is too long for the primary surface, keep the decisive interpretation-changing phrase adjacent to the figure and route the remainder to a referenced evidence note. Never move the entire boundary away merely to make the layout cleaner.
- Run two separate checks: **distance read** — the caption must not steal the hero role; **near read** — the evidence class and interpretation boundary must be unambiguous.

A captioned figure is still REVISE if the caption technically exists but is too detached, too weak, or too dashboard-like to bind truth state to the visual.

## Quality checks

- Claims match approved research.
- No placeholder or unlicensed asset reaches final output.
- Captions identify what, where, when, and why it matters.
- Text remains readable at target print/view distance.
- The conclusion follows from the evidence rather than visual mood alone.
- The first visual remains the real project object, journey, landscape, product, or spatial relation — not a methodology dashboard explaining it.
- Locked/current geometry is not distorted by layout convenience.
- A redesign cannot be promoted if it is visually polished but spatially less credible than the best existing artifact.
