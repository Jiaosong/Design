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

## Quality checks

- Claims match approved research.
- No placeholder or unlicensed asset reaches final output.
- Captions identify what, where, when, and why it matters.
- Text remains readable at target print/view distance.
- The conclusion follows from the evidence rather than visual mood alone.
- The first visual remains the real project object, journey, landscape, product, or spatial relation — not a methodology dashboard explaining it.
- Locked/current geometry is not distorted by layout convenience.
- A redesign cannot be promoted if it is visually polished but spatially less credible than the best existing artifact.

## Long-form project orientation gate

Use this gate when a case, report, portfolio, website, or design book contains many independent pages inside chapter or section containers.

1. Separate three navigation jobs: **orientation** answers “where am I?”, **local continuity** answers “what is immediately before/after?”, and **global access** answers “how do I jump elsewhere?”. Do not force one permanent mega-navigation surface to perform all three jobs.
2. Preserve the project hierarchy explicitly. `PROJECT → CHAPTER / SECTION → PAGE` must remain distinguishable; navigation must never collapse chapter count into page count or imply that one chapter equals one page.
3. Keep current location visible with a compact project/chapter/page marker. On the web, use semantic navigation and programmatically mark the current page when practical; breadcrumb-style hierarchy is appropriate when it matches the actual information architecture.
4. Local previous/next navigation should use meaningful page titles or claims, not only arrows or page numbers, so sequence is legible without opening the global index.
5. Global index access may be persistent when the task genuinely requires constant scanning, but long-form narrative reading should default to on-demand global access rather than exposing the complete project tree on every page.
6. When a desktop chapter rail collapses on mobile, global access must not disappear with it. Provide an explicit mobile-safe index/drawer/menu while keeping the current-page claim visually dominant.
7. If several navigation regions exist in a web page, give them distinct semantic purposes and labels; avoid redundant unlabeled navigation landmarks.
8. Full information availability does not require full simultaneous visibility. Hiding the directory is acceptable only when all pages remain reachable and current orientation/local continuity remain available.
9. Navigation presentation may change, but page identity, chapter binding, evidence order, and protected no-loss rules must not be rewritten merely to simplify the interface.
10. Promotion requires separate readbacks of at least: deep-linked current page, previous/next sequence, global-index closed state, global-index open state, desktop, and target mobile width. A layout with no overflow can still REVISE if the reader loses project/chapter/page orientation.

Default review sequence:

`PAGE IDENTITY → CURRENT LOCATION → LOCAL CONTINUITY → GLOBAL ACCESS → DESKTOP READ → MOBILE READ → OPEN/CLOSED INDEX STATE → DESIGN CRIT`
