# OLEANDER Technical Drawing Skill

Current candidate: `v0.2` in PR #172.

Start with `SKILL.md`. Then load the module that matches the decision:

- `references/DISCIPLINE_PROFILES.md` — architecture/interior, landscape/site, industrial/product, structural/support and fabrication/assembly routing.
- `references/GRAPHIC_SYSTEM.md` — L1–L5 hierarchy, sections, plans, dimensions, leaders, hatches, typography, scale and multi-scale readback.
- `references/REALITY_CHECK.md` — real-world technical evidence, ranges, sensitivity and FIELD/engineer closure.
- `references/STANDARDS_ROUTING.md` — jurisdiction, ISO/ASME/PRC standards discovery and compliance-claim boundary.
- `references/ANALYSIS_DRAWING_SYSTEM.md` — spatial/design analysis diagrams: source/evidence/inference/decision overlays and Evidence → Spatial Finding → Design Consequence chains. Quantitative/statistical charts remain `oleander-data-viz`.
- `templates/DRAWING_EXECUTION_TEMPLATE.md` — reusable brief/register/QA carrier.
- `fixtures/golden/` — editable Golden Drawing Fixture candidates for architecture section, landscape node, product assembly/CMF, connection/foundation, spatial analysis plan and evidence-to-consequence analysis.
- `fixtures/validate_fixtures.py` — structural regression validator for required SVG groups, vector-only core content, fixed fixture canvas and non-promotion state.
- `examples/technical_drawing_hierarchy_calibration.svg` — earlier editable hierarchy calibration provenance; not the Golden suite and not a universal detail standard.

Core pipeline:

`CURRENT AUTHORITY → DISCIPLINE / ANALYSIS TYPE + STATUS + DECISION → VIEW / ANALYSIS SET → DIMENSION/REALITY/TRUTH-STATE REGISTERS → EDITABLE VECTOR DRAWING → MULTI-SCALE DESIGN CRIT → TD-G0…TD-G8 → INDEPENDENT REVIEW → DOWNSTREAM STORY/BOARD → DELIVERY QC`

Golden fixture pipeline:

`FIXTURE SOURCE → STRUCTURE ASSERTIONS → ACTUAL SVG OPEN/READBACK → THUMBNAIL / INTENDED SIZE / NEAR READ → INDEPENDENT OLEANDER DESIGN REVIEW → GOLDEN PROMOTION OR REVISE`.

The module is intentionally no-loss: the main skill owns the invariant rules; references deepen discipline, graphic, analysis, engineering-reality and jurisdiction logic without collapsing them into one checklist.

Hard boundaries:

`ARTIFACT EXISTS ≠ DRAWING PASS ≠ ENGINEERING PASS ≠ FIELD PASS ≠ MAIN KEEP`

`STRUCTURE PASS ≠ DESIGN PASS ≠ GOLDEN PROMOTION`
