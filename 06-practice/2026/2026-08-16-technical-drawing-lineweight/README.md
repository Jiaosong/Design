# 2026-08-16｜Technical Drawing / L5｜Lineweight Hierarchy Lab

Status: `CANDIDATE / NOT ACTIVE SKILL`

## Learning object
SANAA / Rolex Learning Center, Lausanne. Primary factual anchors are EPFL's official project/archive material and MoMA's SANAA exhibition record. The study is not a copy of SANAA drawings; it extracts a transferable graphic principle and tests it on new generic geometry.

## Visible facts
- The Rolex Learning Center uses a continuous single-level field whose spatial differentiation depends on slopes, patios and topographic variation rather than conventional stacked floors; EPFL describes the project as open and fluid, with level variations and large transparent patios.
- MoMA describes SANAA-related work through structural invention, non-hierarchical thinking, transparency and lightness.
- Published plan/section reproductions make the building legible through restrained monochrome information rather than decorative rendering.

## Candidate transfer rule｜Structural Lineweight Hierarchy
When a technical drawing contains multiple kinds of information, do not give every line equal visual authority. Use graphic weight to encode reading order: `CUT / PRIMARY EDGE > PROFILE / BOUNDARY > SECONDARY CONSTRUCTION > FURNITURE / HUMAN / DIMENSION / ANNOTATION`.

Problem: technically complete drawings read flat, noisy or amateur because every object competes at equal weight.

Cause: CAD/export defaults are treated as visual judgment; information presence is mistaken for information hierarchy.

Technique: establish the smallest number of lineweight classes needed to recover spatial reading. Start from section-cut or primary boundary, then lower secondary construction, context, furniture, dimensions and annotation until first-read mass is clear without erasing near-read evidence.

Parameters / conditions: lineweight ratios are relative, not universal fixed millimetres. In this lab the test uses approximately `3.0 : 1.7 : 0.9 : 0.5` as a screen-scale ratio only. It is not a construction-document standard.

Aesthetic judgment: professional finish appears when the drawing reads in two passes: first the spatial/constructive claim, then supporting detail. More information is not better if all information arrives at once.

Verification: same geometry + same text; only lineweight/annotation hierarchy changes. Before/after SVGs are included. Pixel readback confirms the hierarchical version establishes the retaining cut and main enclosure before furniture, person and dimension information.

Failure condition: heavy cut lines become diagrammatic black bars; light information becomes too faint to survive print/export; hierarchy is used to hide missing construction information.

Counterexample: a clean-looking section with bold perimeter and almost invisible technical detail may look 'professional' at thumbnail size but should still be `REVISE` if near-read construction evidence disappears.

Transfer boundary: architectural/landscape sections, product sections, exploded axons, node details, fabrication diagrams, exhibit boards. Do not replace discipline-specific drafting standards or authority requirements.

## Reverse audit｜C04
Highest-value transfer target: R06/C23 node and section material. The recurring risk is not absence of geometry but equal-weight presentation: terrain, structural cut, path, material seam, human scale and maintenance action can collapse into one visual layer.

Concrete modification rule for the next real C04 source edit: preserve authoritative geometry and re-map existing strokes into four explicit classes—`CUT`, `PRIMARY RELATION`, `SECONDARY CONSTRUCTION`, `ANNOTATION/HUMAN/MAINTENANCE`—before adding any new detail. Do not invent dimensions or geometry to improve appearance.

## Gates
- Evidence Gate: `PASS FOR LEARNING OBJECT` — EPFL/MoMA facts are source-grounded.
- Design Quality Gate: `CANDIDATE` — the single-variable lab passed visual readback; C04 real-source migration has not yet been visually read back, so this is not `VALIDATED` or `ACTIVE`.
- Environment: Web = `NATIVE_AVAILABLE`; SVG/Python/CairoSVG = `NATIVE_AVAILABLE`; visual pixel readback = `EXECUTED`; Figma = not used.

## Sources
- EPFL, Rolex Learning Center opening / project description: https://actu.epfl.ch/news/le-rolex-learning-center-concu-par-sanaa-ouvre-ses/
- EPFL, project publications and construction references: https://actu.epfl.ch/news/the-rolex-learning-center-in-publications-and-movi/
- EPFL Living Archives, Rolex Learning Center axonometry/project context: https://livingarchives.epfl.ch/projects/7266/rolex-learning-center-axonometry/
- MoMA, A Japanese Constellation: Toyo Ito, SANAA, and Beyond: https://www.moma.org/calendar/exhibitions/1615
