---
name: oleander-story-and-board
description: Turn Oleander research, data, design logic, renders, and brand strategy into coherent boards, reports, decks, storyboards, promotional narratives, and VI / brand-identity manual presentation layers. Use whenever the user mentions Oleander project compilation, exhibition boards, design books, presentations, brand stories, VI manuals, logo standards, brand guidelines, visual identity systems, scripts, storyboards, key visuals, InDesign, Illustrator, Figma, PowerPoint, or connecting analysis to a persuasive narrative.
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

## Same-source paired-view gate

When a story uses a sequence such as `Landscape First → Relation Reveal`, `Object → Explanation`, `Overview → Highlight`, or any paired visual that is meant to deepen the same spatial/design object:

- Both views must derive from the **same authoritative visual geometry or source object**. The reveal may add masks, highlights, callouts, labels, state emphasis, or bounded overlays; it must not silently replace the base object with a cleaner abstract proxy.
- The first view must remain project-readable with explanatory labels removed. If the base landscape/object/journey cannot be recognized without the second explanatory layer, the pair is not evidence-led and must be REVISE.
- The second view must reveal only relations that change the audience's understanding or decision. Decorative overlays, redundant labels, and generic methodology graphics do not qualify as a reveal.
- Record `BASE_SOURCE / BASE_VERSION / PRESENTATION_ONLY_CHANGES / REVEAL_LAYER / DOES_NOT_PROVE` for any paired primary visual.
- If the reveal layer requires re-authoring geometry to make the argument work, stop and route back to the upstream design/evidence owner instead of repairing the story layer.
- A layout placeholder or abstract proxy may be used during composition, but it cannot receive `MAIN / KEEP` status until the authoritative asset is actually bound and re-reviewed.

**Promotion test:** `If view A is not project-readable without labels, view B cannot rescue it.` `Abstract proxy ≠ Main visual.`

## Project Web image uniqueness gate

For every OLEANDER project Web, image reuse is governed at the **whole-project Web level**, not per chapter, page, section, or component.

**Hard rule:** one underlying content-image source may occupy **one Web image slot only** across the entire project Web.

This applies to project photographs, landscape images, renders, AI-assisted concept images, screenshots used as content imagery, and other content-bearing raster image sources.

- Track every Web image by `SOURCE_ASSET_ID` and, when available, `SOURCE_SHA256`.
- The same source image appearing in a second project-Web slot is a **BLOCKER**, even if the second use changes crop, aspect ratio, scale, color grade, saturation, filter, mask, overlay, frame, caption, text, or responsive breakpoint. Presentation processing does not create a new source image.
- A derivative generated from the same underlying image source remains the same source for this gate unless it is a materially new evidence artifact with its own independent source authority rather than a presentation-only transformation.
- If the same subject must appear again, use a genuinely different source photograph/render/evidence asset, or change medium: map, editable SVG, diagram, model view, technical drawing, chart, motion state, or another non-duplicate evidence carrier.
- Before Web layout, create or refresh a project-wide image-use ledger with at least `WEB_SLOT_ID / PAGE_OR_SECTION_ID / SOURCE_ASSET_ID / SOURCE_SHA256 / SOURCE_URI_OR_AUTHORITY / DERIVATION / STATUS`.
- Before `MAIN / KEEP / PROMOTE`, scan the complete project Web ledger. Any repeated `SOURCE_ASSET_ID` or repeated underlying source hash across different image slots is `REVISE` until replaced.
- Responsive variants of the **same single Web slot** do not count as additional uses; they are one semantic slot rendered at multiple breakpoints.
- Brand marks, functional UI icons, repeated navigation symbols, and system texture tokens are governed by the identity/UI system and are excluded from this content-image uniqueness gate unless they are being used as content imagery.

For same-source reveal logic on Web, do **not** duplicate the base image into multiple static project-Web slots. Bind the authoritative source once and implement the reveal as a state/layer change in the same semantic component, or choose another evidence carrier for the second view.

**Promotion test:** `Same source twice anywhere in the project Web = REVISE.` `Crop / grade / mask / overlay ≠ new image source.`

## VI / Brand Identity Manual production

When the requested artifact is a **VI manual / visual identity handbook / logo standards page / brand guideline / brand identity Web chapter**, first resolve the Current Brand Identity METHOD and then read:

`oleander-skills/oleander-story-and-board/VI_MANUAL_PRODUCTION_EXTENSION.md`

This does **not** make `oleander-story-and-board` the Brand Identity authority. Brand Identity remains Notion-led with `NO_DEDICATED_OWNER`; this skill owns only the presentation/manual composition layer and must route specialist content to Current Visual Communication, Color, Image Ops and Technical Drawing methods/tools.

Mandatory VI production rule:

**Text rule ≠ visual specification.**

If a VI rule is operational, it must be visibly represented at the point of use. Examples:

- clearspace must show logo bounds + influence/exclusion bounds + dimensions;
- minimum size must show concrete values/units and a threshold specimen, plus a FAIL/below-threshold specimen when relevant;
- standard construction must be tied to the current authoritative geometry, not a decorative grid;
- wordmark rules must show the actual wordmark/baseline relation;
- color rules must show actual swatches/roles/contrast rather than only list values;
- typography rules must show real uppercase/lowercase/numerals/punctuation/CJK/weights rather than only name font families;
- material/image effects must keep effect-off and Flat Geometry Authority available.

Use Technical Drawing logic for construction, dimensions, safe areas, influence zones, optical limits and production geometry. Never invent a dimension just to make a VI page appear complete.

## Assembly workflow

1. Pull approved claims and sources from Notion.
2. Pull validated charts from `oleander-data-viz`.
3. Pull model manifests and approved renders from `oleander-3d-pipeline`.
4. Create a content inventory before layout.
5. Resolve the strongest current design/evidence source for every primary visual; record which objects are locked and may not be re-authored by layout.
6. For Web work, create or refresh the whole-project image-use ledger before assigning imagery; reject duplicate source allocation before polishing.
7. Establish grid, hierarchy, type system, palette, caption style, image treatment, and page/board numbering around those authority objects.
8. Produce a low-fidelity sequence before polishing.
9. Reuse the same narrative IDs across report sections, boards, deck slides, and film scenes.
10. Run content, visual, and production reviews separately.
11. For spatial primary visuals, perform an authority-preservation comparison against the strongest existing artifact before promotion.
12. For paired/reveal visuals, compare both frames side by side and confirm that the base geometry is identical except for declared presentation-only changes; on Web, keep the shared base in one semantic image slot and change only the state/layer rather than duplicating it across the project.
13. For VI/manual work, compare prose against the actual figure and reject any operational rule that exists only in explanatory text.
14. For Web, run the project-wide image uniqueness scan again on the finished build before `MAIN / KEEP / PROMOTE`.

## Deliverable variants

- Board: distance-readable hierarchy, restrained text, explicit sequence.
- Report/book: evidence depth, citations, cross-references, appendices.
- Deck: one decision or claim per slide.
- Brand story: human motivation, distinctive promise, proof, voice.
- VI / brand manual: visibly represented identity rules, actual master assets, dimensioned construction where required, color/type specimens, misuse, production boundaries, and editable/readback-ready pages.
- Film storyboard: scene purpose, image, motion, narration, sound, duration, source assets.

## Required output

Return the narrative outline, content inventory, page/board/scene map, missing-assets list, production specification, and final editable/source deliverable.

For any layout containing source-bound spatial evidence, include a short authority-preservation note naming the source object and confirming what was kept unchanged versus presentation-only edits.

For any paired/reveal primary visual, also return a same-source declaration naming the base source/version and the exact overlay/highlight differences between frames.

For any project Web, also return or persist the project-wide image-use ledger and the final duplicate-source scan result.

For VI/manual work, also return or persist the represented standard drawings/specimens used by the manual, actual readbacks at target size, and all proof-open production limits. A prose-only specification is not a complete VI deliverable.

## Quality checks

- Claims match approved research.
- No placeholder or unlicensed asset reaches final output.
- Captions identify what, where, when, and why it matters.
- Text remains readable at target print/view distance.
- The conclusion follows from the evidence rather than visual mood alone.
- The first visual remains the real project object, journey, landscape, product, or spatial relation — not a methodology dashboard explaining it.
- Locked/current geometry is not distorted by layout convenience.
- A redesign cannot be promoted if it is visually polished but spatially less credible than the best existing artifact.
- Paired/reveal views preserve the same base geometry; only declared presentation layers may change.
- A base frame that is unreadable without explanatory labels is not promotable as a primary visual.
- Project Web contains no repeated content-image source across separate image slots; crop/filter/mask/grade/overlay changes do not reset source identity.
- For VI work, every operational rule that is stated in prose is visibly represented on the page or explicitly routed to another current page/source.
- For VI construction pages, dimension/value/unit/safe-zone/minimum-size claims are visible in the drawing itself, not only in surrounding text.
- Material/raster display effects never become logo/vector/text geometry authority.
