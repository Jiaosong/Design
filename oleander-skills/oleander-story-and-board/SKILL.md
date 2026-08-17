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

## Bilingual typography gate

Use this gate whenever Chinese and English coexist on the same presentation surface.

1. Decide the primary reading language before styling. Bilingual presentation is not a requirement to give both languages equal visual weight.
2. Preserve the full information in both languages when both are required, but allocate unequal size, weight, line length, spacing, contrast, and placement according to reading priority.
3. A translated headline must not automatically duplicate the primary headline's type size, width, and emphasis. If both languages compete for first-read, mark the layout `REVISE` unless the page intentionally presents two equal claims.
4. Treat line breaks as designed structure. Break Chinese by semantic phrase and visual rhythm; do not leave opening punctuation at line end or closing/stop punctuation stranded at line start where the composition can avoid it.
5. In mixed Chinese/Latin text, keep proportional Latin letters and European numerals. Do not use fullwidth ASCII merely to make mixed-script text look aligned.
6. For Chinese-dominant horizontal text, allow controlled spacing between Han characters and adjacent Latin letters or numerals when needed for legibility; do not insert arbitrary spaces inconsistently across the same document.
7. Keep abbreviations, units, IDs, figure numbers, and technical tokens visually intact. Do not split an annotation mark from the text it marks or separate symbols from the numerals they qualify when that changes meaning.
8. Test both distance-read and near-read. At distance, the audience should identify the primary claim and language immediately; near-read must still preserve the secondary-language content without making it a footnote-like afterthought.
9. Do not use typography polish to hide translation drift. The secondary-language text must remain semantically aligned with the approved primary claim and evidence boundary.
10. A successful export, font load, or line-wrap implementation does not prove design quality. Reopen the rendered result and review hierarchy, line breaks, punctuation position, mixed-script spacing, crop/overflow, and paragraph density independently.

Calibration reference: W3C *Requirements for Chinese Text Layout (CLReq)* for Chinese punctuation, line-breaking constraints, and Chinese/Western mixed-text composition. Treat project-specific typography as a design decision, not as a blanket claim of standards compliance.

## Required output

Return the narrative outline, content inventory, page/board/scene map, missing-assets list, production specification, and final editable/source deliverable.

## Quality checks

- Claims match approved research.
- No placeholder or unlicensed asset reaches final output.
- Captions identify what, where, when, and why it matters.
- Text remains readable at target print/view distance.
- The conclusion follows from the evidence rather than visual mood alone.
- Bilingual pages identify a primary reading language, avoid accidental equal-weight competition, and pass line-break/crop review in the rendered output.

