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

## Assembly workflow

1. Pull approved claims and sources from Notion.
2. Pull validated charts from `oleander-data-viz`.
3. Pull model manifests and approved renders from `oleander-3d-pipeline`.
4. Create a content inventory before layout.
5. Establish grid, hierarchy, type system, palette, caption style, image treatment, and page/board numbering.
6. Produce a low-fidelity sequence before polishing.
7. Reuse the same narrative IDs across report sections, boards, deck slides, and film scenes.
8. Run content, visual, and production reviews separately.

## Deliverable variants

- Board: distance-readable hierarchy, restrained text, explicit sequence.
- Report/book: evidence depth, citations, cross-references, appendices.
- Deck: one decision or claim per slide.
- Brand story: human motivation, distinctive promise, proof, voice.
- Film storyboard: scene purpose, image, motion, narration, sound, duration, source assets.

## Responsive focal-anchor gate

When a claim-bearing image moves across web, mobile, board, deck, or other aspect ratios, responsive success means preserving the claim, not merely fitting the media box.

1. Identify the visual object or relation that carries the claim before changing aspect ratio. Record it as a focal anchor or focal region.
2. Define a crop-safe zone around that anchor. The safe zone must include every element required to understand the primary claim, not only the most photogenic object.
3. Simulate every target ratio before approval. At minimum, compare the widest and narrowest intended presentation surfaces.
4. `object-fit: cover`, center crop, or an automated crop is never a design PASS by itself. If the declared focal anchor leaves the visible frame, the responsive variant is `REVISE` even when there is no overflow.
5. Use `object-position` or equivalent focal-coordinate controls only when a single source image can preserve the same claim at all required ratios.
6. Use art-directed source variants when one crop cannot preserve composition, scale, subject relation, or legibility across ratios. Do not stretch or distort one source to avoid producing a proper variant.
7. Keep focal coordinates, safe-zone intent, and crop decisions in the production specification so later web, slide, board, and video implementations do not silently recenter the asset.
8. If text overlays an image, test the image anchor and text safe zone together. Preserving the subject while causing title/body collisions is still `REVISE`.
9. Claim continuity and asset identity are separate gates: a crop may preserve the image file while destroying the claim, or preserve the claim while using an unauthorized replacement. Both must pass.
10. Browser/runtime evidence remains distinct from crop-geometry or static visual proof. A geometric crop simulation can support Design Crit but must not be reported as browser PASS.

Reference implementation logic: CSS Images defines `object-fit: cover` as preserving aspect ratio while filling the content box, and `object-position` as the alignment control inside that box. The skill uses those primitives as implementation tools, not as substitutes for composition review.

## Required output

Return the narrative outline, content inventory, page/board/scene map, missing-assets list, production specification, and final editable/source deliverable.

## Quality checks

- Claims match approved research.
- No placeholder or unlicensed asset reaches final output.
- Captions identify what, where, when, and why it matters.
- Text remains readable at target print/view distance.
- Claim-bearing images retain their declared focal anchor and safe zone across approved aspect ratios.
- The conclusion follows from the evidence rather than visual mood alone.

