# 2026-08-07｜状态先于造型｜Timer Light Basin 01

## Training identity
- **Software:** Autodesk Fusion
- **Category:** Product modeling
- **Difficulty:** L3 — parameters, components and validation
- **Training type:** Deep practice
- **Estimated duration:** 180 minutes
- **Main capability:** Build a maintainable parametric product assembly in which product state, component structure and internal section remain readable.
- **Secondary capability:** Convert an OLEANDER method into explicit CAD parameters, component boundaries and evidence gates.

## Evidence boundary
All sizes in this package are **exercise assumptions**. They must not be used for production, optical, electrical, thermal, ergonomic, safety, tooling or cost decisions.

This package does **not** contain a completed Fusion model. The `.f3d`, STEP, screenshots and Fusion-generated parameter CSV remain **to be executed by the user in Autodesk Fusion**.

## OLEANDER method adopted
1. **Product as a state system:** define inactive, running, near-end, end and abnormal states before styling.
2. **Construction as evidence:** component boundaries, wall thickness, gap, section and timeline must be readable.
3. **Relationship before object:** the exercise focuses on relations among housing, diffuser, light area and time state—not a decorative “minimal” appearance.
4. **Single-variable validation:** keep base form fixed while comparing visible-area states.
5. **Evidence gate:** CAD geometry is a digital hypothesis; optical and manufacturing claims require physical testing.

## Design question
Can a screenless timer express remaining time through a shrinking luminous area while preserving a clear, editable and inspectable product construction?

## Exercise assumption parameters
See `01_parameters_reference.csv`.

Important: Autodesk recommends exporting a parameter CSV from Fusion first when a guaranteed header template is needed. Treat the supplied CSV as a **reference table**, then create the parameters in Fusion or replace it with a CSV exported from Fusion.

## 180-minute sequence

### 0–15 min｜Read and define
- Read the state model and evidence boundary.
- Create a new parametric Fusion design.
- Save as `2026-08-07_Fusion360_TimerLightBasin_v01`.

**Checkpoint:** the problem is stated without “poetic”, “minimal” or “premium” as design evidence.

### 15–35 min｜File structure and parameters
- Create internal components before geometry:
  - `01_Base_Housing`
  - `02_Light_Diffuser`
  - `03_Light_Mask`
- Open `Design > Solid > Modify > Change Parameters`.
- Create the named parameters from `01_parameters_reference.csv`.
- Rename sketches and features immediately.

**Checkpoint:** components are empty, named and separately activatable; all parameter units are valid.

### 35–80 min｜Base housing
1. Activate `01_Base_Housing`.
2. Create a half-section sketch on the XZ plane.
3. Constrain the centre axis and bottom datum.
4. Dimension the outer form with `body_diameter` and `body_height`.
5. Use `Solid > Create > Revolve`, Full 360°, New Body.
6. Use `Solid > Modify > Shell`, inside, with `wall_thickness`.
7. Apply `base_fillet` only after shell stability is confirmed.

**Checkpoint:** the profile sketch is fully constrained and the timeline has no warning.

### 80–115 min｜Light diffuser
1. Activate `02_Light_Diffuser`.
2. Create a separate half-section sketch.
3. Set edge height to `diffuser_edge_height`.
4. Set centre height to `diffuser_center_height`.
5. Build the shallow concave relation using an arc or constrained spline.
6. Revolve 360° as a separate body/component.
7. Offset or construct the lower face to achieve `diffuser_thickness`.
8. Preserve `assembly_gap` relative to the housing.

**Checkpoint:** the diffuser can be hidden independently and remains editable without modifying the housing sketch.

### 115–140 min｜Three product states
- Use `02_state_radius_table.csv`.
- Create 100%, 50% and 10% visible-area reference bodies or sketches inside `03_Light_Mask`.
- Keep overall product geometry unchanged.
- Change only the visible light radius.

**Checkpoint:** each state is named and can be shown independently. No state is described as verified optical performance.

### 140–165 min｜Inspection and stress test
- Create `Inspect > Section Analysis` through the centre plane.
- Use Measure for overall diameter, height, wall and gap.
- Run Interference on housing/diffuser/mask.
- Test:
  - body diameter +10%;
  - body height -10%;
  - wall thickness 1.5–2.5 mm.
- Return to baseline values.

**Checkpoint:** the model rebuilds without errors and no unintended interference remains.

### 165–180 min｜Evidence and export
Capture:
1. Isometric view.
2. Top views of the three states.
3. Section Analysis.
4. Browser/component structure.
5. Timeline.

Save:
- `.f3d` native Fusion archive;
- `.step` neutral solid export;
- Fusion-generated parameter `.csv`;
- screenshots;
- a short retain/reject/revise review.

## Common failure modes
1. **Modeling bodies in the root component.**  
   Result: history and ownership become ambiguous.  
   Correction: create and activate components before geometry.

2. **Using unconstrained splines for the diffuser.**  
   Result: form changes unpredictably during parameter tests.  
   Correction: reduce control points and constrain endpoints/tangency.

3. **Shell and fillet in an unstable order.**  
   Result: parameter changes break downstream features.  
   Correction: establish primary volume, shell it, then add secondary fillets.

4. **Confusing radius shrinkage with area shrinkage.**  
   Result: the visual state is mathematically distorted.  
   Correction: use the supplied area-proportional radius table.

5. **Treating CAD as optical proof.**  
   Result: generated light appearance becomes a false engineering claim.  
   Correction: label it a digital state model; physical LED/diffuser testing is still required.

6. **Exporting STEP as the only source.**  
   Result: feature history and editable design intent are lost.  
   Correction: retain `.f3d`; STEP is a neutral handoff, not the canonical editable source.

## Minimum pass standard — 80/100
- Fully constrained primary sketches.
- Three named components.
- Named user parameters and timeline features.
- Stable rebuild under three parameter stress tests.
- Section Analysis and interference evidence.
- Three visible-area states.
- `.f3d`, STEP, Fusion-exported CSV and four evidence screenshots.
- Explicit distinction between CAD result and unverified physical performance.

## Project-candidate standard — 90/100
In addition to the minimum standard:
- clean component ownership and timeline order;
- no default names;
- clear section showing constructable layer relationships;
- state views communicate remaining amount without explanatory text;
- retain/reject/revise decisions reference specific geometry and state relations;
- next physical prototype variables are stated without invented performance claims.

## Next advanced task
Create a 1:1 diffuser prototype matrix with three curvatures and three diffuser materials. Keep housing geometry fixed. Measure three-metre state legibility, glare, transition threshold and maintenance access. This remains blocked until real components, materials and observations exist.

## Files to retain
- Native `.f3d`
- STEP export
- Fusion-exported parameter CSV
- all screenshots
- this training package
- version note and unresolved issues

## Official Autodesk references — accessed 2026-08-07
- Parameters in Fusion
- Import or export parameters
- Revolve a solid body
- Shell a solid body
- Create new components
- Create a 3D section view
- Export designs

## Current status
`TRAINING PACKAGE GENERATED / FUSION EXECUTION PENDING`
