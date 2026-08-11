# SP03-R02｜Light Role → Performance Interface

Status before runtime: **RADIANCE PERFORMANCE INTERFACE PENDING**.

## Purpose
Translate SP03-R01's conceptual light roles into an explicit performance input/output contract without pretending that a synthetic test cell is a real project.

## Controlled A/B experiment
Both schemes use the same 12 × 6 × 3.6 m synthetic room, materials, 7.2 m² total skylight area, 288 workplane sensors, sky cases and viewpoints. Only skylight-area distribution changes.

- Scheme A｜Uniform: four equal 1.2 m-wide skylights.
- Scheme B｜Sequence: widths 0.8 / 2.4 / 1.0 / 0.6 m assigned to Entry / Stay / Turn / Background.
- Intended role rank for the exercise: Stay > Turn > Entry > Background.

The role-rank correlation is a **custom exercise heuristic**, not a lighting standard.

## Real simulation scope
GitHub Actions must install and execute Radiance. The workflow runs:

- `gensky` for one overcast and three exercise solar-angle scenarios;
- `oconv` for each A/B × sky scene;
- `rtrace -I+` on the same 288-point workplane grid;
- `rpict` 180° fisheye HDR views for clear east/west cases;
- `evalglare` for DGP and vertical illuminance evidence;
- automated comparison plots and gate JSON.

Radiance `rtrace` is used as the ray-tracing engine, while `evalglare` evaluates 180° fisheye HDR images and reports DGP/vertical illuminance. These are software-runtime evidence only; project compliance is not claimed.

## Truth boundaries
OPEN until a real project provides them:

- project geometry/orientation;
- measured or verified material/glazing optical properties;
- actual location/weather/time conditions;
- program-specific illuminance/glare targets;
- user/task validation.

Therefore the maximum allowed result is:

`PERFORMANCE INTERFACE VERIFIED ON SYNTHETIC TEST CELL / PROJECT REALITY OPEN`

not Project Reality PASS.

## Review routing
After runtime completion, artifacts must undergo:

- AR-G01—G10 Common;
- AR-S03 Data;
- AR-S04 Code / Parametric;
- AR-S05-equivalent spatial-performance review for coordinate/time/sky truth;
- AR-S06/visual review for exported maps/charts where applicable;
- AR-S07 Documentation;
- AR-S09 Release Package.

Automatic success or a green GitHub Action is not sufficient. Final exported plots and evidence must be reopened and reviewed before `POST-REVIEW PASS`.
