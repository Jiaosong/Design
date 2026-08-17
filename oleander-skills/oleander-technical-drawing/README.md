# OLEANDER Technical Drawing Skill

Current candidate: `v0.2` in PR #172.

Start with `SKILL.md`. Then load the module that matches the decision:

- `references/DISCIPLINE_PROFILES.md` — architecture/interior, landscape/site, industrial/product, structural/support and fabrication/assembly routing.
- `references/GRAPHIC_SYSTEM.md` — technical hierarchy plus composition, contrast budget, grid/rails, whitespace, typography and 3s/30s/near-read review.
- `references/DETAIL_DENSITY_CALIBRATION.md` — professional near-read depth D0–D6: identity, primary relation, functional dimensions/datums, build-up/materials, connections/interfaces, environment/serviceability, and unresolved closure. Use it when a drawing is visually clean but still technically shallow.
- `references/VISUAL_HIERARCHY_TRANSFER.md` — cross-skill translation from mature Data-viz / Story-board / external design skills into technical drawing without importing UI decoration.
- `references/SPATIAL_TRANSLATION_PROTOCOL.md` — **mandatory before drawing decision-relevant spatial-analysis geometry**. Separates semantic identification from valid spatial translation through `SOURCE/PHENOMENON → SPATIAL MODEL → GEOMETRIC ABSTRACTION → GRAPHIC CARRIER → VISUAL ENCODING`; requires translation mode, registration class, preserved/relaxed spatial invariants and does-not-prove boundaries. Prevents arbitrary lines/dots/blobs that merely have the right label.
- `references/SOURCE_CARRIER_PRECEDENCE.md` — **mandatory whenever the source itself already contains the relevant spatial geometry**. Classify the source carrier as absent / insufficient / sufficient / authority before redrawing. `SOURCE_CARRIER_SUFFICIENT/AUTHORITY` defaults to `REUSE_DIRECT`; redraw/generalization/derivation requires a material analytical/editability/output reason. Aesthetic cleanliness, style matching or easier coloring are not valid redraw justifications.
- `references/LANDSCAPE_ANALYSIS_DRAWING.md` — landscape/site/public-realm carrier grammar for topography, hydrology, movement, vegetation/habitat, edge/threshold, view/experience, program/dwell and operations. Use together with `SPATIAL_TRANSLATION_PROTOCOL.md` and `SOURCE_CARRIER_PRECEDENCE.md`; knowing a line/node/field class is not enough until its geometry is validly translated, and a source-supported carrier must not be replaced merely because a cleaner custom graphic is possible.
- `references/REFERENCE_RECONSTRUCTION_FIDELITY.md` — base 1:1 reference reconstruction mode and RF-G0…RF-G6 separation from technical truth.
- `references/PIXEL_FORENSIC_PROTOCOL.md` — mandatory deep path for explicit `像素级 / pixel-level / pixel perfect / exact replica` work: RF-C0…RF-C3 claim levels, locked renderer/font/color environment, sub-pixel anchors, typography/stroke/pattern forensics, tolerance-zero diff, edge-radius diagnostics, critical ROI contracts and E0–E6 layer freezing.
- `references/PIXEL_SOLVER_PROTOCOL.md` — mandatory when forensic review finds measurable residuals that can be expressed as bounded editable SVG parameters. It replaces eyeballed nudging with renderer-locked, ROI-weighted, multi-cycle coupled coordinate descent and explicitly reopens earlier layers after coupled variables change.
- `references/MULTILAYER_RELATION_RECONSTRUCTION.md` — mandatory companion for stacked/exploded analytical diagrams and callout-heavy references. Adds shared-base genealogy, relation-evidence register, semantic-editability levels, callout-network topology, symbol dictionaries, dual visual-extraction/semantic-rebuild tracks and per-panel relationship ROI review. It explicitly rejects `path-cloud vector = editable` and `label present = relation drawn`.
- `references/VISUALIZATION_DATA_RECONSTRUCTION_BRIDGE.md` — mandatory bridge when the supplied reference is a chart/infographic/analytical visualization and the user expects editable data semantics. It separates RF pixel/relationship recovery from Data-viz source-data/encoding recovery, adds crossing-identity confidence, segment→layer promotion rules and deterministic data/spec/generator roundtrip requirements.
- `references/EDITORIAL_CALLOUT_FIDELITY.md` — targeted repair for exact leader landing, editorial side-icon crop/component fidelity, typography-only ROIs and rotated street/route labels. Use it after semantic structure exists but callout pixels still drift.
- `references/FLOW_DIRECTION_ANALYSIS.md` — circulation/mobility/route-network grammar: route edges/nodes, direction-marker taxonomy, primary/secondary hierarchy, base binding, speed/street/mode-symbol ownership, topology/pixel diagnosis, low-recall stop rule, FN-C0…FN-C3 claim ladder and R3/JPEG reconstruction ceiling.
- `references/BASE_INSTANCE_FIDELITY.md` — repeated main-body/base reconstruction: separates semantic geometry master, per-panel rendered base instance and bounded non-authoritative visual carrier; adds visibility/omission profiles, contamination blockers, BI-C0…BI-C3 and panel-specific neutral/base fidelity diagnosis.
- `references/THEME_OVERLAY_FIDELITY.md` — thematic-overlay reconstruction: separates semantic theme objects from bounded source-derived theme visual carriers, with TI-C0…TI-C3 and contamination/authority boundaries.
- `references/FINAL_STAGE_PIXEL_SOLVER.md` — last-stage typography/symbol/node/micro-flow repair after geometry/base/theme/flow are materially reconstructed. It permits only bounded local visual carriers, preserves editable semantic sources and forbids full-sheet residual path-cloud shortcuts.
- `references/REALITY_CHECK.md` — real-world technical evidence, ranges, sensitivity and FIELD/engineer closure.
- `references/STANDARDS_ROUTING.md` — jurisdiction, ISO/ASME/PRC standards discovery and compliance-claim boundary.
- `references/ANALYSIS_DRAWING_SYSTEM.md` — spatial/design analysis diagrams: source/evidence/inference/decision overlays and Evidence → Spatial Finding → Design Consequence chains. Quantitative/statistical charts remain `oleander-data-viz`. Any spatial geometry produced by this module must pass `SPATIAL_TRANSLATION_PROTOCOL.md`; if a usable source visual already carries the relation, also pass `SOURCE_CARRIER_PRECEDENCE.md` before redrawing.
- `templates/DRAWING_EXECUTION_TEMPLATE.md` — reusable brief/register/QA carrier; Section 9A becomes mandatory for exact reconstruction.
- `tools/reference_fidelity.py` — registered raster diagnostics and optional hard fidelity contract; it reports residual translation, tolerance-zero pixel error, r0/r1/r2 edge disagreement, mismatch concentration and ROI failures without warping the candidate.
- `tools/svg_parameter_solver.py` — bounded editable-SVG parameter solver. Supports numeric attributes and group translation, explicit renderer selection, ROI-weighted search, coarse-to-fine steps and repeated coupled cycles. It outputs solved SVG/PNG plus a complete accepted-parameter trace.
- `tools/validate_semantic_reconstruction.py` — machine gate for multilayer semantic editability: shared master-base reuse, relation carriers/targets, callout topology and reusable symbol instances. This gate cannot award pixel fidelity or Design KEEP.
- `tools/validate_flow_network.py` — machine gate for flow-network graph integrity: base geometry, route classes, edge/node topology, node degree, direction-marker ownership/tangency contract, route-label binding, mode-symbol ownership and external continuations. This gate cannot prove source completeness, route truth, pixel fidelity or Design KEEP.
- `tools/validate_spatial_translation.py` — machine gate for spatial translation **and source-carrier precedence** register integrity. It checks source binding, spatial model, translation mode, registration class, preserved invariants, carrier type, source-carrier adequacy and redraw justification. It rejects pseudo-map schematics, topology-only graphics claiming exact position, symbol-only relations, direct-reuse claims on insufficient sources, and sufficient/authoritative source carriers redrawn only for aesthetics. Machine PASS does not prove project interpretation or Design KEEP.
- `tools/validate_base_instances.py` — machine gate for repeated-base instance structure: semantic master preservation, distinct per-panel visual carriers, non-authority state, neutral-only vector content and no raster/text/theme contamination. This gate cannot prove pixel fidelity or geometry authority.
- `fixtures/reconstruction/ML-REL-01_SEMANTIC.svg` + `ML-REL-01_RELATION_REGISTER.json` — synthetic regression proving the semantic-reconstruction machine gate; not Golden promoted and not project authority.
- `fixtures/reconstruction/FLOW-01_NETWORK.svg` + `FLOW-01_NETWORK_REGISTER.json` — synthetic regression proving that circulation/mobility objects stay a semantic graph rather than collapsing into a few generic arrows; not Golden promoted and not project authority.
- `fixtures/reconstruction/SPATIAL-TRANSLATION-01_REGISTER.json` + `validate_spatial_translation_regression.py` — synthetic regression proving that semantic naming cannot skip spatial modelling and that source-carrier sufficiency cannot be ignored in favor of a cleaner redraw; not Golden promoted and not project authority.
- `fixtures/reconstruction/BASE-01_INSTANCE.svg` + `BASE-01_INSTANCE_REGISTER.json` — synthetic regression proving geometry-master / rendered-base-instance separation and bounded non-authoritative visual carriers; not Golden promoted and not project authority.
- `fixtures/reconstruction/` — synthetic strict reconstruction regression, including an RF-C3 zero-difference contract; not Golden promoted and not project authority.
- `fixtures/golden/` — editable Golden Drawing Fixture candidates for architecture section, landscape node, product assembly/CMF, connection/foundation, spatial analysis plan and evidence-to-consequence analysis.
- `fixtures/validate_fixtures.py` — structural regression validator for required SVG groups, vector-only core content, hierarchy scaffold, technical depth contract, fixed fixture canvas and non-promotion state.
- `examples/technical_drawing_hierarchy_calibration.svg` — earlier editable hierarchy calibration provenance; not the Golden suite and not a universal detail standard.

Core pipeline:

`CURRENT AUTHORITY → DISCIPLINE / ANALYSIS TYPE + STATUS + DECISION → PRIMARY CLAIM → SOURCE / PHENOMENON → SOURCE-CARRIER ADEQUACY → SPATIAL MODEL → GEOMETRIC ABSTRACTION + REGISTRATION CLASS + PRESERVED INVARIANTS → REUSE DIRECT | TRACE/DERIVE/GENERALIZE | SCHEMATIZE SEPARATELY → GRAPHIC CARRIER → VIEW / ANALYSIS SET → DIMENSION/REALITY/TRUTH-STATE/FLOW REGISTERS → EDITABLE VECTOR DRAWING / DIRECT SOURCE VISUAL → VISUAL ENCODING / 3S CLAIM / 30S LOGIC / NEAR-READ PROOF → DETAIL DENSITY D0–D6 → TD-G0…TD-G8 → INDEPENDENT REVIEW → DOWNSTREAM STORY/BOARD → DELIVERY QC`

For landscape/spatial-analysis work, the translation sequence is mandatory before styling:

`SOURCE / PHENOMENON → SOURCE_CARRIER_ABSENT | INSUFFICIENT | SUFFICIENT | AUTHORITY → SPATIAL MODEL → TRACE | DERIVE | GENERALIZE | SCHEMATIZE | INFER | DESIGN → MAP_BOUND | BASE_RELATION_BOUND | TOPOLOGY_BOUND | SEQUENCE_BOUND | DIAGRAM_ONLY → REUSE_DIRECT | TRACE_BOUNDED | DERIVE_REQUIRED | GENERALIZE_REQUIRED | SCHEMATIZE_SEPARATELY | REDRAW_JUSTIFIED → POINT | LINE | CENTERLINE | EDGE_PAIR | BAND | POLYGON | FIELD | NETWORK | SECTION | VECTOR | DIRECT_SOURCE_VISUAL → VISUAL ENCODING`.

If the producer cannot state the spatial model, source-carrier adequacy, or which invariants survive simplification, the carrier is not ready to draw. If the source carrier is already sufficient/authoritative, redraw is not the default.

Spatial-translation claim ladder:

`ST-C0 SEMANTIC IDENTIFIED → ST-C1 SPATIAL MODEL RESOLVED → ST-C2 GEOMETRIC TRANSLATION RESOLVED → ST-C3 GRAPHIC CARRIER VALIDATED`.

`ST-C3 != DESIGN KEEP`. A source-carrier precedence decision is part of ST-C2/ST-C3, not a separate design-quality award.

Hard boundaries:

`MORE DETAIL ≠ MORE PROFESSIONAL`

`SEMANTIC IDENTIFICATION ≠ SPATIAL TRANSLATION`

`KNOWN MEANING ≠ VALID GEOMETRY`

`SOURCE EXISTS ≠ REDRAW REQUIRED`

`CLEANER GRAPHIC ≠ BETTER SPATIAL TRANSLATION`

`SOURCE-CARRIER ADEQUACY > EDITORIAL DESIRE TO REDRAW`

`GRAPHIC SIMPLIFICATION ≠ PERMISSION TO INVENT SPATIAL RELATION`

`SCHEMATIC TOPOLOGY ≠ MAP GEOMETRY`

`POINT / LINE / FIELD CHOICE ≠ VISUAL CONVENIENCE`

`DIRECT SOURCE CARRIER ≠ VECTOR EDITABILITY ≠ SURVEY ACCURACY ≠ FIELD PASS`

`ARTIFACT EXISTS ≠ DRAWING PASS ≠ ENGINEERING PASS ≠ FIELD PASS ≠ MAIN KEEP`
