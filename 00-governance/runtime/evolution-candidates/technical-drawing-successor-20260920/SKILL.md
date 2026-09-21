---
name: oleander-technical-drawing
description: Candidate successor for authority-bound professional drawing execution: plan, section, elevation, detail, node, assembly, dimension and source-bound technical SVG/DXF carriers with actual reopen/readback. Use only inside its declared Candidate boundary until explicit promotion.
compatibility: Editable SVG and ASCII DXF; external CAD/BIM/model authority may be referenced but is not replaced.
---

# OLEANDER Technical Drawing — v0.3 successor candidate

**State:** `CANDIDATE_SUCCESSOR / NOT CURRENT / NO PROMOTION`.

This is the same Skill identity as PR #172. Use `SUCCESSOR_PROVENANCE_MANIFEST_v0.3.json` for no-loss lineage.

## Execution contract

Before drawing, resolve:

1. **Professional Decision Object** — what plan/section/detail question must be closed?
2. **Drawing status** — `DESIGN_STUDY / TECHNICAL_EXPLANATION / COORDINATION / FABRICATION / CONSTRUCTION`.
3. **Authority** — geometry, dimensions, levels, material, system, site and specialist authority.
4. **Native carrier** — project CAD/BIM when authoritative; otherwise editable DXF/SVG only within the claim ceiling.
5. **Readback** — how the actual file will be reopened and checked.
6. **Independent review** — who can judge the drawing beyond producer self-check.

Canonical route:

`DECISION OBJECT → SOURCE AUTHORITY → REQUIRED VIEW/DETAIL → NATIVE CARRIER → DRAW → REOPEN → MEASURE/COMPARE → REVIEW → VERDICT`.

## Hard rules

- A render/screenshot is not dimensional authority.
- A visually dense sheet does not become construction documentation.
- A Candidate Skill cannot satisfy a required Current owner.
- A range remains a range; do not collapse it to one invented value.
- `NTS` must be explicit when formal plotted scale is not closed.
- `FIELD OPEN`, `VERIFY`, `ENGINEERING REVIEW REQUIRED` and equivalent states remain visible.
- A detail must identify its parent/source view or source object.
- A drawing derived from a project model must not become the geometry authority unless the project explicitly promotes it.
- Project specialist signoff, statutory review and field verification remain outside this Skill.

## Minimum execution record

Use `templates/DRAWING_EXECUTION_TEMPLATE.md` and emit a machine-readable receipt with:

`drawing_id / project / decision_object / status / source_refs / authority_state / native_outputs / expected_dimensions_or_ranges / actual_readback / cross_view_checks / open_items / independent_review / claim_ceiling / does_not_prove`.

## Candidate currentization evidence

The successor includes:

- deterministic ASCII DXF + SVG round-trip fixture;
- C04 Qingjiang F01 research-envelope technical explanation with source ranges preserved;
- KH-LY46 ADD-07 project binding to an existing native DXF/SVG/readback chain without copying or re-authoring its external project geometry.

These exercises test routing and truthful technical translation only. They do not award Current status.
