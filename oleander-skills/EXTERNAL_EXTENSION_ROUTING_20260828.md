# OLEANDER External-Digestion Extension Routing — 2026-08-28

Status: `CANDIDATE ROUTING INDEX / EXISTING-FIRST`

Purpose: make independently reformulated, source-bounded professional deltas discoverable by the existing OLEANDER Skill owners without creating parallel Core Skills.

This is an index, not a new authority layer. The Current Skill `SKILL.md`, resolver, owner map, project authority and more specific Current methods remain authoritative.

## Routing table

| Trigger / Required Native Output | Existing owner | Candidate extension | External study provenance |
|---|---|---|---|
| Parametric product/mechanical CAD, STEP/STP, fit-critical assembly, named datums/mates, purchased component geometry | `oleander-3d-pipeline` + Technical Drawing/VALIDATION as needed | `oleander-3d-pipeline/PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md` | `earthtojake/text-to-cad` |
| Repeatable project/brand motion character, coordinated multi-element choreography, temporal hierarchy | `oleander-motion` | `oleander-motion/MOTION_ART_DIRECTION_CHOREOGRAPHY_EXTENSION.md` | `LottieFiles/motion-design-skill` |
| Live presentation/pitch/review deck where audience decision, claim-proof sequence and evidence density matter | `oleander-story-and-board` | `oleander-story-and-board/PRESENTATION_ARGUMENT_EVIDENCE_EXTENSION.md` | `wbohanw/html-presentation` |
| Independent visual critique against a brief/current design source using actual rendered states and repair/recapture evidence | `oleander-visual-design` + relevant runtime owner | `oleander-visual-design/RENDERED_BRIEF_REVIEW_EXTENSION.md` | `julianoczkowski/designer-skills/design-review` |
| Commercial print, PDF/X, packaging/POP preflight, printer specification, proof planning | `oleander-visual-design` + `oleander-delivery-qc` | `oleander-delivery-qc/PRINT_PRODUCTION_PREFLIGHT_EXTENSION.md` | `SkillMedev/skills/print-layout` |
| Physical product whose form depends on payload/cavity, ergonomics, mechanism, assembly or CMF sequencing | `oleander-design-process` | `oleander-design-process/PHYSICAL_PRODUCT_PHASE_GATES_EXTENSION.md` | `shawnlix/claude-product-designer-skill` |

## Co-routing rules

- Physical product + fit-critical mechanism: `PHYSICAL_PRODUCT_PHASE_GATES_EXTENSION` → `PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION` → relevant Technical Drawing / Delivery QC validation.
- Product/brand presentation motion: Motion Role remains upstream; use `MOTION_ART_DIRECTION_CHOREOGRAPHY_EXTENSION` only after state/narrative semantics exist.
- Browser-based live deck: use the existing `LIVE_EDITABLE_HTML_PRESENTATION_EXTENSION.md` for editing/export/runtime and `PRESENTATION_ARGUMENT_EVIDENCE_EXTENSION.md` for audience/claim-proof narrative; these are orthogonal.
- Print-ready visual design: visual composition remains with `oleander-visual-design`; `PRINT_PRODUCTION_PREFLIGHT_EXTENSION` governs production specification and release proof classes.
- Rendered review: the reviewer uses `RENDERED_BRIEF_REVIEW_EXTENSION`; defects are returned to the actual owner instead of being repaired inside a hidden review skill.

## Rights / transfer boundary

Each training record under `oleander-skills/training/2026-08-28_external-*-digestion.md` records the observed source/license and accepted/rejected transfer. External CLI/API syntax, templates, prompt recipes, fixed heuristics, visual presets and runtime assumptions are not automatically OLEANDER rules.

The `wbohanw/html-presentation` repository did not expose a root LICENSE file in the reviewed state even though its `SKILL.md` declares MIT; therefore only high-level independently worded presentation principles were retained.

## Maturity boundary

Every entry above remains `CANDIDATE EXTENSION`. Documentation presence and CI success do not promote an extension, owner or external source to ACTIVE/installed authority. Real project use, actual artifact/runtime readback, regression evidence and independent review remain required for stronger maturity claims.