# OLEANDER Website｜Project Display Framework v0.1

> This layer complements `PORTFOLIO_FRAMEWORK.md`. The portfolio home is an editorial, image-first reading spine; individual project displays are capability-driven and must not become a universal fixed page template.

## 1. Architecture

`Project data → Capability set → Project-specific display plan → Artifact/Evidence binding → Renderer slots`

The canonical project data owns meaning and status. The front-end adapter owns presentation only.

## 2. Non-negotiable rules

1. **Capability framework, not page template.**
   - A project declares the capabilities it needs.
   - `minimum_capabilities` is a floor, not a fixed page list.
   - Project-specific `display.plan` controls emphasis and ordering.
   - Required capabilities omitted from the explicit plan are appended automatically rather than silently lost.
2. **Work first, explanation follows.**
   - Where real retained imagery exists, large images lead.
   - Missing evidence is shown as `OPEN`; it must not be replaced by decorative filler.
3. **Evidence boundary survives presentation.**
   - `Fact / Source Claim / Judgment / Inference / Hypothesis / Observation / Unknown` remain visible in the project instance.
   - Digital evidence cannot be restyled into physical approval.
4. **Presentation Crop / Full Board / Diagnostic remain distinct.**
   - Review/full-board assets preserve source proportion with `contain`.
   - Diagnostic/research proxies default to collapsed/hidden.
5. **Project status controls public promotion.**
   - XJ01 is currently `internal_review / NOT_PUBLIC_RELEASE`.
   - It is intentionally not inserted into public `Selected Works`.

## 3. Generic route

`project.html?project=<project-id>`

The first registered instance is `xj01`.

The renderer uses a registry only to locate data. It does not hard-code a universal set of project sections. Rendering order comes from each project's `display.plan`, with required capabilities appended as safety coverage.

## 4. XJ01 pilot

The pilot demonstrates:
- D02 / D03 matched comparison
- Material hierarchy
- Interfaces
- Interaction gate
- VE06 open-state display
- VE07 lifecycle proxy boundary
- Evidence truth states
- Specification / promotion blockers

Open work remains open:
- VE06 Environment Adaptation
- VE07 Lifecycle Realism Repair
- 06C P1 physical interaction
- P1–P3 physical CMF samples
- Engineering-readable specification

## 5. Future adapters

A future brand, architecture, spatial or web project may define different capability composition and order. New project types should extend renderer types or use the generic fallback; they should not fork another fixed page architecture.
