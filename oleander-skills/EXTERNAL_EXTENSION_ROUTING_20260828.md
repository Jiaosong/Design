# OLEANDER External-Digestion Extension Routing — 2026-08-28

Status: `CANDIDATE ROUTING INDEX / EXISTING-FIRST`

Purpose: make independently reformulated, source-bounded professional deltas discoverable by the existing OLEANDER Skill owners without creating parallel Core Skills.

This is an index, not a new authority layer. The Current Skill `SKILL.md`, resolver, owner map, project authority and more specific Current methods remain authoritative.

## Routing table

| Trigger / Required Native Output | Existing owner | Candidate extension | External study provenance |
|---|---|---|---|
| Parametric product/mechanical CAD, STEP/STP, fit-critical assembly, named datums/mates, purchased component geometry | `oleander-3d-pipeline` + Technical Drawing/VALIDATION as needed | `oleander-3d-pipeline/PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md` | `earthtojake/text-to-cad` |
| Editable `.scad` source for parameter-driven fabrication / 3D-print utility part, process-orientation and mesh derivative lineage | `oleander-3d-pipeline` + CAD/VALIDATION as needed | `oleander-3d-pipeline/OPENSCAD_PARAMETRIC_FABRICATION_EXTENSION.md` | `swh/openscad-skill` high-level bounded study |
| Repeatable project/brand motion character, coordinated multi-element choreography, temporal hierarchy | `oleander-motion` | `oleander-motion/MOTION_ART_DIRECTION_CHOREOGRAPHY_EXTENSION.md` | `LottieFiles/motion-design-skill` |
| Live presentation/pitch/review deck where audience decision, claim-proof sequence and evidence density matter | `oleander-story-and-board` | `oleander-story-and-board/PRESENTATION_ARGUMENT_EVIDENCE_EXTENSION.md` | `wbohanw/html-presentation` |
| Independent visual critique against a brief/current design source using actual rendered states and repair/recapture evidence | `oleander-visual-design` + relevant runtime owner | `oleander-visual-design/RENDERED_BRIEF_REVIEW_EXTENSION.md` | `julianoczkowski/designer-skills/design-review` |
| Commercial print, PDF/X, packaging/POP preflight, printer specification, proof planning | `oleander-visual-design` + `oleander-delivery-qc` | `oleander-delivery-qc/PRINT_PRODUCTION_PREFLIGHT_EXTENSION.md` | `SkillMedev/skills/print-layout` |
| Physical product whose form depends on payload/cavity, ergonomics, mechanism, assembly or CMF sequencing | `oleander-design-process` | `oleander-design-process/PHYSICAL_PRODUCT_PHASE_GATES_EXTENSION.md` | `shawnlix/claude-product-designer-skill` |
| Physical product form needs affordance, body/contact, construction-truth, maintenance/disassembly or repair-path review | `oleander-design-process` + 3D/Technical/VALIDATION as needed | `oleander-design-process/PRODUCT_FORM_AFFORDANCE_SERVICEABILITY_EXTENSION.md` | `getburo/buro-free` high-level bounded study only |
| Cross-media typography system, type roles, font delivery/fallback, bilingual/CJK or long-string stress | `oleander-visual-design` + `oleander-web-ui` when browser delivery applies | `oleander-visual-design/TYPOGRAPHY_SYSTEM_EXTENSION.md` | `event4u-app/agent-config` + `TheGoat395/Codex-Skills` |
| Repeated UI/brand icons, pictograms, glyph-family consistency, icon source/delivery verification | `oleander-visual-design` + relevant UI owner | `oleander-visual-design/ICONOGRAPHY_SYSTEM_EXTENSION.md` | `event4u-app/agent-config` |
| Existing brand identity must become an operational multi-media rule system with allowed/forbidden/context/specimen logic | `oleander-visual-design` + relevant delivery owner | `oleander-visual-design/BRAND_RULE_ENCODING_EXTENSION.md` | official `resend/design-skills` as high-level bounded study only |
| Existing repository/site/product must be reconstructed into persistent design-language guidance without promoting accidental implementation patterns | `oleander-visual-design` + `oleander-web-ui` for rendered/browser evidence | `oleander-visual-design/DESIGN_LANGUAGE_RECONSTRUCTION_EXTENSION.md` | `ibelick/ui-skills/create-design-md` |
| Several real image candidates compete for the same hero/support/sequence roles and selection/cohesion must be traceable | `oleander-image-art-direction` | `oleander-image-art-direction/IMAGE_SET_CURATION_EXTENSION.md` | `SkillMedev/skills/visual-asset-curation` |
| Navigation/page hierarchy, canonical content homes, labels, deep-route orientation, Return/recovery or spatial/digital wayfinding | `oleander-web-ui` + `oleander-route-wayfinding-ui` when specialist authority is required | `oleander-web-ui/INFORMATION_ARCHITECTURE_WAYFINDING_EXTENSION.md` | `jacob-balslev/skill-graph` + `Deibler/universal-design-principles` |
| Responsive page/screen composition, content-driven breakpoints, reflow and state-footprint stability | `oleander-web-ui` + current visual/interaction specialists | `oleander-web-ui/RESPONSIVE_LAYOUT_COMPOSITION_EXTENSION.md` | `jacob-balslev/skill-graph` |
| Semantic HTML, keyboard/focus contract, programmatic names/states, assistive-tech announcements and preference modes | `oleander-web-ui` + VALIDATION / interaction specialist as needed | `oleander-web-ui/ACCESSIBLE_INTERACTION_EXTENSION.md` | `jacob-balslev/skill-graph` |
| Reusable high-fidelity UI token system, semantic roles, multi-theme mapping and state × theme drift review | `oleander-web-ui` + `oleander-visual-design` | `oleander-web-ui/SEMANTIC_UI_TOKEN_THEME_EXTENSION.md` | `axross/skills/high-fidelity-ui-design` high-level bounded study |
| Multi-factor experiment, nuisance variation, interaction, pseudoreplication, blocked/nested/repeated or DOE run-design question beyond a genuinely two-condition Current A/B test | `oleander-research` + VALIDATION/statistical owner as needed | `oleander-research/EXPERIMENTAL_DESIGN_DOE_EXTENSION.md` | `K-Dense-AI/scientific-agent-skills/experimental-design` |
| Claim asks whether changing X causes Y and observational/experimental evidence needs confounder/collider/mediator classification, identification or sensitivity | `oleander-research` | `oleander-research/CAUSAL_IDENTIFICATION_EXTENSION.md` | `magnus919/agent-skills/data-scientist` causal-inference references |
| Measured/computed quantity affects a design, field, prototype, production or performance decision and units/traceability/material uncertainty matter | `oleander-research` + actual technical/validation owner downstream | `oleander-research/MEASUREMENT_UNCERTAINTY_EXTENSION.md` | `K-Dense-AI/scientific-agent-skills/uncertainty-and-units` |
| System behavior crosses component/subsystem/service interfaces and local object PASS cannot prove integrated behavior | `oleander-design-process` + 3D/Technical/VALIDATION as needed | `oleander-design-process/SYSTEM_INTERFACE_COUPLING_EXTENSION.md` | `K-Dense-AI/scientific-agents/systems-engineer` |

## Co-routing rules

- Physical product + fit-critical mechanism: `PHYSICAL_PRODUCT_PHASE_GATES_EXTENSION` → `PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION` → relevant Technical Drawing / Delivery QC validation.
- Physical product affordance/serviceability is orthogonal to phase sequencing: use `PRODUCT_FORM_AFFORDANCE_SERVICEABILITY_EXTENSION` only when form/use interpretation, construction truth or lifecycle access is a material question. Do not turn subtraction/minimalism into a default aesthetic.
- OpenSCAD fit-critical part: `.scad` source/process route → `OPENSCAD_PARAMETRIC_FABRICATION_EXTENSION`; named components, fit/mates or critical interfaces additionally co-route to `PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION`.
- Product/brand presentation motion: Motion Role remains upstream; use `MOTION_ART_DIRECTION_CHOREOGRAPHY_EXTENSION` only after state/narrative semantics exist.
- Browser-based live deck: use the existing `LIVE_EDITABLE_HTML_PRESENTATION_EXTENSION.md` for editing/export/runtime and `PRESENTATION_ARGUMENT_EVIDENCE_EXTENSION.md` for audience/claim-proof narrative; these are orthogonal.
- Print-ready visual design: visual composition remains with `oleander-visual-design`; `PRINT_PRODUCTION_PREFLIGHT_EXTENSION` governs production specification and release proof classes.
- Rendered review: the reviewer uses `RENDERED_BRIEF_REVIEW_EXTENSION`; defects are returned to the actual owner instead of being repaired inside a hidden review skill.
- Typography: establish type roles/source/rights first; then use the actual medium owner for browser, print, packaging or presentation delivery. A token file or installed font package does not grant Design KEEP.
- Iconography: inspect the incumbent brand/UI family before selecting or drawing a glyph. Accessibility role and target size are checked with the actual UI/runtime owner.
- Design-language reconstruction: explicit Current design/brand authority outranks repeated implementation. Reconstructed rendered patterns remain `OBSERVED` until promoted by authority; when a real token/theme system is found, co-route to `SEMANTIC_UI_TOKEN_THEME_EXTENSION` instead of inventing token semantics in the reconstruction document.
- Image set curation: preserve source/evidence truth and claim fit before cohesion. Do not use one LUT/white balance or a fixed aesthetic heuristic to make a heterogeneous evidence set look artificially uniform.
- IA → layout: resolve user goals, canonical homes, placement and labels before `RESPONSIVE_LAYOUT_COMPOSITION_EXTENSION` decides within-page spatial structure. Do not use page layout to hide a broken information architecture.
- Wayfinding → interaction/motion: current location, route decision, route monitoring, destination recognition and Return/recovery semantics exist before decorative transitions are added.
- Accessible interaction is not a final checklist. It cross-checks primitive choice, state model, keyboard/focus order and dynamic announcements during implementation and again after responsive/motion integration.
- Semantic token/theme work is wiring + appearance architecture, not a replacement for visual composition or accessibility. `TOKEN PASS ≠ ACCESSIBILITY PASS ≠ DESIGN KEEP`.
- Brand-rule encoding is project-specific. Never import Resend or any other third-party brand's exact fonts, colors, assets, dimensions, lockups or layout signatures as OLEANDER identity.
- Current A/B Controlled Experiment remains the owner for a genuine two-condition experiment. Route to `EXPERIMENTAL_DESIGN_DOE_EXTENSION` only when factor interaction, blocking, nesting, repeated measures, run-order or multi-factor design is material. `MORE EXPERIMENTS ≠ DOE`.
- Causal identification is downstream of the causal question and evidence-generating process, not a replacement for Design Goal Contract or A/B. `ASSOCIATION / REGRESSION / FEATURE IMPORTANCE ≠ IDENTIFIED CAUSAL EFFECT`.
- Measurement uncertainty is upstream evidence formation. Delivery QC can verify that units/metadata survive release, but it cannot retroactively create calibration, traceability or uncertainty authority that the measurement never had.
- System-interface coupling complements current Trade Study and FMEA. Use it when failure emerges between otherwise valid objects; do not recreate FMEA or install a generic systems-engineering lifecycle.

## Rights / transfer boundary

Each training record under `oleander-skills/training/` records the observed source/license and accepted/rejected transfer. External CLI/API syntax, templates, prompt recipes, fixed heuristics, visual presets and runtime assumptions are not automatically OLEANDER rules.

Specific reviewed boundaries:

- `wbohanw/html-presentation`: no root LICENSE exposed in reviewed state although `SKILL.md` declares MIT; only independently worded high-level presentation principles retained.
- `jacob-balslev/skill-graph`: repository root `LICENSE` is Apache-2.0; this repository-level license is used as the transfer boundary even where exported Skill frontmatter says MIT.
- `Deibler/universal-design-principles`: MIT with explicit attribution notes for the principle taxonomy/research lineage; OLEANDER retains independently reformulated relation models, not copied examples/prose.
- official `resend/design-skills`: no root LICENSE exposed in reviewed state; only high-level operational brand-rule patterns retained, with all Resend-specific values/assets/templates excluded.
- `SkillMedev/skills`: repository root MIT. Image-set curation mechanics are adapted, but fixed color-temperature/taste/candidate-count heuristics are explicitly not OLEANDER defaults.
- `getburo/buro-free`: root license is `All Rights Reserved`; only independently synthesized general affordance/serviceability questions are retained. No source prose/templates/examples/output format are copied.
- `axross/skills`: no repository-level license file found in the reviewed state; only high-level token/theme architecture is independently synthesized. Fixed dark-mode recipes, token names and values are excluded.
- `swh/openscad-skill`: no repository-level license file found in the reviewed state; only high-level parametric fabrication mechanisms are independently synthesized. BOSL2 house style, code templates, helper tools, printer/material/slicer tables and numeric defaults are excluded.
- `ibelick/ui-skills`: repository root MIT. OLEANDER adapts evidence/recurrence/intent-separation logic but does not adopt the external `DESIGN.md` schema, CLI, export targets or token naming constraints.
- `K-Dense-AI/scientific-agent-skills`: repository MIT. Experimental-design and uncertainty mechanisms are independently reformulated; scientific examples, package/version recipes, fixed sample/factor heuristics, statistical defaults and lab-specific workflow are excluded.
- `magnus919/agent-skills`: repository MIT. Causal-identification discipline is adapted; fixed diagnostic thresholds, estimator preferences and domain assumptions are excluded.
- `K-Dense-AI/scientific-agents`: repository MIT. Systems-engineering interface/coupling/V&V concepts are adapted without adopting ISO 15288/V-model/review-phase/tool-stack house process.
- `d-wwei/systems-thinking`: no repository license found in the reviewed tree; high-level comparison only. No source prose, extended worldview framework or packaged protocol is transferred.

## Maturity boundary

Every entry above remains `CANDIDATE EXTENSION`. Documentation presence and CI success do not promote an extension, owner or external source to ACTIVE/installed authority. Real practice evidence, cross-context reapplication, project use where authorized, actual artifact/runtime/measurement readback and independent review remain required for stronger maturity claims.