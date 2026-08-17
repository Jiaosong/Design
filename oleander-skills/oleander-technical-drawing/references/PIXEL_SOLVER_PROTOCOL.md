# OLEANDER Technical Drawing — Pixel Solver Protocol

Status: `v0.1 CANDIDATE / PR #172 / reconstruction subsystem`

Use this after `PIXEL_FORENSIC_PROTOCOL.md` has materialized a real reference and identified measurable mismatches. The solver exists to replace eyeballed nudging with reproducible parameter search.

`REFERENCE PIXELS → LOCKED RENDERER → PARAMETERIZED EDITABLE SVG → COUPLED SOLVER → ZERO-ERROR OR EXPLICIT HOLD`

This module does not authorize technical facts, engineering, field truth, fabrication, construction, or Design KEEP.

## 1. Why the solver is needed

Pixel-level reconstruction fails when visually coupled parameters are adjusted once in a fixed order. Example: a wrong font size may make the apparently best baseline wrong; after the font size is corrected, the baseline must be reopened. Therefore:

`E2 GEOMETRY → E3 TYPOGRAPHY → E4 STROKE` is not a one-pass pipeline.

Use multi-cycle repair:

`E2 → E3 → E4 → REOPEN E2/E3/E4 UNTIL NO MATERIAL IMPROVEMENT`.

Higher layers may stay frozen only while lower-layer corrections do not invalidate them.

## 2. Hard prerequisites

Before running `tools/svg_parameter_solver.py`:

- exact reference pixels are locally materialized and immutable;
- reference and candidate use the same comparison canvas;
- the candidate is editable SVG and does not embed the reference as a visual substitute;
- the comparison renderer is declared explicitly when strict fidelity matters;
- critical ROIs are declared before optimization;
- parameter bounds are narrow enough to prevent semantic/structural redesign;
- source/project truth boundaries are already known.

If the reference exists only as a web thumbnail/search preview and exact bytes cannot be materialized, do not claim RF-C3. Use RF-C0/RF-C1 and mark `REFERENCE_BYTES_OPEN`.

## 3. Renderer lock is part of the optimization problem

The same SVG can rasterize differently under Inkscape, CairoSVG, browsers, PDF engines, font stacks, and operating systems.

Before judging a parameter:

1. lock the renderer name and version when available;
2. lock the output width/height;
3. lock background/alpha handling;
4. lock fonts/shaping/fallback;
5. render the reference and candidate through the same path whenever the reference is vector;
6. if the reference is raster-only, record its capture/render provenance when known.

A renderer mismatch can make a correct geometry or baseline look numerically worse and can cause the optimizer to choose a false parameter value.

`WRONG RENDERER → WRONG OPTIMUM`.

## 4. Parameter specification

The solver specification is JSON. Parameters must correspond to visible, semantically bounded authoring variables.

Supported core parameter kinds:

- numeric SVG attributes such as `x`, `y`, `cx`, `cy`, `r`, `width`, `height`, `stroke-width`, `font-size`;
- group `translate_x` / `translate_y`;
- staged search using `stage`;
- coarse-to-fine step schedules;
- min/max bounds;
- ROI weighting.

Do not expose arbitrary project dimensions or engineering values to an optimizer merely to improve visual similarity.

Example:

```json
{
  "max_cycles": 4,
  "stages": ["E2_GEOMETRY", "E3_TYPOGRAPHY", "E4_STROKE"],
  "rois": [
    {"id":"title", "x":70, "y":70, "w":650, "h":100, "weight":4},
    {"id":"primary_geometry", "x":120, "y":330, "w":730, "h":230, "weight":5}
  ],
  "parameters": [
    {"name":"primary_dx", "stage":"E2_GEOMETRY", "target":{"id":"PRIMARY_GEOMETRY"}, "kind":"translate_x", "steps":[5,2,1,0.5], "min":-10, "max":10},
    {"name":"title_y", "stage":"E3_TYPOGRAPHY", "target":{"id":"TEXT", "tag":"text", "index":0}, "kind":"attribute", "attribute":"y", "steps":[3,1,0.5]},
    {"name":"title_size", "stage":"E3_TYPOGRAPHY", "target":{"id":"TEXT", "tag":"text", "index":0}, "kind":"attribute", "attribute":"font-size", "steps":[2,1,0.5]}
  ]
}
```

## 5. Loss is diagnostic, not a design score

During search, use a cheap pixel/ROI objective so repeated rendering remains practical. At final readback, add edge mismatch.

Current search emphasis:

`CRITICAL ROI PIXEL DIFFERENCE > GLOBAL CHANGED PIXELS > GLOBAL MAE`.

Final readback also checks edge mismatch.

No weighted loss value is a PASS threshold. RF-C3 still requires the hard Pixel Forensic contract, including zero unexplained in-scope difference under the locked comparison path.

## 6. Coupled coordinate descent

For each cycle:

1. visit parameters in stage order;
2. test `current-step` and `current+step` within declared bounds;
3. accept only a real objective improvement;
4. repeat the same step until no further improvement;
5. reduce the step size;
6. continue through all stages;
7. reopen earlier stages in the next cycle;
8. stop when an entire cycle produces no material improvement or `max_cycles` is reached.

This is intentionally conservative. It is designed for reconstructing known visual structure, not for free-form redesign.

## 7. Sub-pixel refinement

When integer-pixel search plateaus but edge/antialiasing residuals remain:

- add 0.5 / 0.25 / 0.125 px steps only to the specific implicated parameters;
- do not globally unlock all coordinates;
- verify that the residual is geometric/stroke phase rather than font renderer noise;
- re-run the final target-size raster comparison after supersampled diagnostics.

Sub-pixel parameter search is not permission to distort project-authoritative geometry in `PROJECT ADAPTATION` mode.

## 8. Typography coupling

Typography variables are strongly coupled:

`FONT FACE / WEIGHT → FONT SIZE → TRACKING → LINE BOX / WRAP → BASELINE → TEXT X/Y`.

If the exact font/shaping path is missing, hold RF-C3 rather than forcing geometry/text positions into a false optimum.

When the font is known, group typography parameters into repeated cycles. A baseline solved while the font size is wrong is provisional and must be reopened after size/weight/spacing changes.

## 9. Curve and path fitting boundary

The current solver is strongest for explicit numeric SVG attributes and group translations. Complex path fitting should use a separate bounded parameterization rather than blindly exposing the raw `d` string.

For Bezier/path work:

`VISIBLE EDGE SAMPLES → DECLARED CONTROL POINTS / HANDLES → BOUNDED SEARCH → SAME-SIZE RASTER READBACK`.

Do not run unconstrained pixel optimization over arbitrary path topology; that can overfit raster noise and destroy editable geometry logic.

## 10. Required evidence

A solver run must preserve:

- original editable candidate;
- solver spec;
- renderer choice;
- initial metrics;
- accepted parameter trace;
- solved SVG;
- solved PNG;
- final metrics;
- explicit list of parameters changed;
- `does_not_prove` boundary.

The solved file is a candidate, not automatically the new authority.

## 11. Synthetic regression result

`RF-CAL-01` intentionally begins with four known errors:

- primary geometry group `translateX = +5 px`;
- title baseline `108` instead of `105`;
- title font size `31` instead of `32`;
- interface stroke `2.8` instead of `2.2`.

When reference and candidate are rendered through the same CairoSVG path and the coupled solver is allowed to reopen typography after other corrections, the solver recovered:

- `primary_dx: 5 → 0`;
- `title_y: 108 → 105`;
- `title_font_size: 31 → 32`;
- `interface_stroke: 2.8 → 2.2`;
- final `changed_pixel_ratio = 0`;
- final normalized `MAE = 0`;
- final edge mismatch = `0`.

A prior one-pass run incorrectly settled on title `y=104` after optimizing against a still-wrong font size. This failure is retained as evidence for the coupled-cycle requirement.

## 12. Water World benchmark consequence

The Information is Beautiful `Water World` benchmark exposed a separate upstream blocker: a visible web/search reference can support structural reconstruction, but the current execution runtime may not materialize the exact remote image bytes into the local solver environment. In that state:

`STRUCTURAL RECONSTRUCTION MAY CONTINUE / RF-C3 MUST HOLD`.

Do not replace unavailable reference bytes with a screenshot of the reconstruction itself, a thumbnail of uncertain provenance, or a manually recreated proxy and then call the comparison pixel-exact.
