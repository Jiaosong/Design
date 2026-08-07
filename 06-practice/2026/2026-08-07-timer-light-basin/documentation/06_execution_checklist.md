# Fusion 360 execution and review checklist

## Status boundary
- [ ] I understand that every dimension in this package is an **exercise assumption**.
- [ ] I will not use this package as a manufacturing, optical, electrical, ergonomic, safety or cost specification.
- [ ] The Fusion `.f3d` model and STEP export do not yet exist until I create and verify them in Fusion.

## File setup
- [ ] Parametric modeling mode is active.
- [ ] Root design name: `2026-08-07_Fusion360_TimerLightBasin_v01`.
- [ ] Components are created **before** geometry:
  - [ ] `01_Base_Housing`
  - [ ] `02_Light_Diffuser`
  - [ ] `03_Light_Mask`
- [ ] Units are millimetres.
- [ ] User Parameters are created with unique, semantic names.
- [ ] Timeline features are renamed.

## Geometry
- [ ] Base housing sketch is fully constrained.
- [ ] Base housing is created with a 360° Revolve.
- [ ] Housing wall thickness is controlled by `wall_thickness`.
- [ ] Diffuser is a separate component/body.
- [ ] The light surface edge is 3 mm higher than the centre.
- [ ] The visible light diameter is 100 mm.
- [ ] Nominal radial assembly gap is 0.5 mm.
- [ ] Fillets are applied after the primary form is stable.

## State system
- [ ] 100%, 50% and 10% remaining states are represented.
- [ ] State radii follow the supplied area-proportional reference table.
- [ ] State geometry is not confused with verified optical performance.

## Validation
- [ ] `Inspect > Section Analysis` is created and saved.
- [ ] `Inspect > Measure` confirms key dimensions.
- [ ] `Inspect > Interference` reports no unintended overlap.
- [ ] Parameter test A: body diameter +10%, model rebuilds without error.
- [ ] Parameter test B: body height -10%, model rebuilds without error.
- [ ] Parameter test C: wall thickness 1.5–2.5 mm, model rebuilds without error.
- [ ] No red/yellow timeline failures remain.
- [ ] All sketches and bodies are in the correct component.

## Deliverables
- [ ] Native Fusion archive `.f3d`.
- [ ] Neutral CAD export `.step`.
- [ ] Parameter export `.csv` generated **from Fusion**.
- [ ] Isometric screenshot.
- [ ] Top-view screenshot showing 3 states.
- [ ] Section Analysis screenshot.
- [ ] Timeline screenshot.
- [ ] 150–250 word review: retain / reject / revise.
