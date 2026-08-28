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
| Cross-media typography system, type roles, font delivery/fallback, bilingual/CJK or long-string stress | `oleander-visual-design` + `oleander-web-ui` when browser delivery applies | `oleander-visual-design/TYPOGRAPHY_SYSTEM_EXTENSION.md` | `event4u-app/agent-config` + `TheGoat395/Codex-Skills` |
| Repeated UI/brand icons, pictograms, glyph-family consistency, icon source/delivery verification | `oleander-visual-design` + relevant UI owner | `oleander-visual-design/ICONOGRAPHY_SYSTEM_EXTENSION.md` | `event4u-app/agent-config` |
| Navigation/page hierarchy, canonical content homes, labels, deep-route orientation, Return/recovery or spatial/digital wayfinding | `oleander-web-ui` + `oleander-route-wayfinding-ui` when specialist authority is required | `oleander-web-ui/INFORMATION_ARCHITECTURE_WAYFINDING_EXTENSION.md` | `jacob-balslev/skill-graph` + `Deibler/universal-design-principles` |
| Responsive page/screen composition, content-driven breakpoints, reflow and state-footprint stability | `oleander-web-ui` + current visual/interaction specialists | `oleander-web-ui/RESPONSIVE_LAYOUT_COMPOSITION_EXTENSION.md` | `jacob-balslev/skill-graph` |
| Semantic HTML, keyboard/focus contract, programmatic names/states, assistive-tech announcements and preference modes | `oleander-web-ui` + VALIDATION / interaction specialist as needed | `oleander-web-ui/ACCESSIBLE_INTERACTION_EXTENSION.md` | `jacob-balslev/skill-graph` |
| Existing brand identity must become an operational multi-media rule system with allowed/forbidden/context/specimen logic | `oleander-visual-design` + relevant delivery owner | `oleander-visual-design/BRAND_RULE_ENCODING_EXTENSION.md` | official `resend/design-skills` as high-level bounded study only |

## Co-routing rules

- Physical product + fit-critical mechanism: `PHYSICAL_PRODUCT_PHASE_GATES_EXTENSION` → `PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION` → relevant Technical Drawing / Delivery QC validation.
- Product/brand presentation motion: Motion Role remains upstream; use `MOTION_ART_DIRECTION_CHOREOGRAPHY_EXTENSION` only after state/narrative semantics exist.
- Browser-based live deck: use the existing `LIVE_EDITABLE_HTML_PRESENTATION_EXTENSION.md` for editing/export/runtime and `PRESENTATION_ARGUMENT_EVIDENCE_EXTENSION.md` for audience/claim-proof narrative; these are orthogonal.
- Print-ready visual design: visual composition remains with `oleander-visual-design`; `PRINT_PRODUCTION_PREFLIGHT_EXTENSION` governs production specification and release proof classes.
- Rendered review: the reviewer uses `RENDERED_BRIEF_REVIEW_EXTENSION`; defects are returned to the actual owner instead of being repaired inside a hidden review skill.
- Typography: establish type roles/source/rights first; then use the actual medium owner for browser, print, packaging or presentation delivery. A token file or installed font package does not grant Design KEEP.
- Iconography: inspect the incumbent brand/UI family before selecting or drawing a glyph. Accessibility role and target size are checked with the actual UI/runtime owner.
- IA → layout: resolve user goals, canonical homes, placement and labels before `RESPONSIVE_LAYOUT_COMPOSITION_EXTENSION` decides within-page spatial structure. Do not use page layout to hide a broken information architecture.
- Wayfinding → interaction/motion: current location, route decision, route monitoring, destination recognition and Return/recovery semantics exist before decorative transitions are added.
- Accessible interaction is not a final checklist. It cross-checks primitive choice, state model, keyboard/focus order and dynamic announcements during implementation and again after responsive/motion integration.
- Brand-rule encoding is project-specific. Never import Resend or any other third-party brand's exact fonts, colors, assets, dimensions, lockups or layout signatures as OLEANDER identity.

## Rights / transfer boundary

Each training record under `oleander-skills/training/2026-08-28_external-*-digestion.md` records the observed source/license and accepted/rejected transfer. External CLI/API syntax, templates, prompt recipes, fixed heuristics, visual presets and runtime assumptions are not automatically OLEANDER rules.

Specific reviewed boundaries:

- `wbohanw/html-presentation`: no root LICENSE exposed in reviewed state although `SKILL.md` declares MIT; only independently worded high-level presentation principles retained.
- `jacob-balslev/skill-graph`: repository root `LICENSE` is Apache-2.0; this repository-level license is used as the transfer boundary even where exported Skill frontmatter says MIT.
- `Deibler/universal-design-principles`: MIT with explicit attribution notes for the principle taxonomy/research lineage; OLEANDER retains independently reformulated relation models, not copied examples/prose.
- official `resend/design-skills`: no root LICENSE exposed in reviewed state; only high-level operational brand-rule patterns retained, with all Resend-specific values/assets/templates excluded.

## Maturity boundary

Every entry above remains `CANDIDATE EXTENSION`. Documentation presence and CI success do not promote an extension, owner or external source to ACTIVE/installed authority. Real project use, actual artifact/runtime readback, regression evidence and independent review remain required for stronger maturity claims.