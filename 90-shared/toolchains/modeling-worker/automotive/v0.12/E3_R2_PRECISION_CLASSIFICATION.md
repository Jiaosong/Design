# E3 R2 Precision Classification｜Quintic Surface Runtime Representation

Status: `PRECISION CLASSIFIED / COMPILER C2 THRESHOLD UNCHANGED / RUNTIME D2 = DIAGNOSTIC / R2 STILL SUBJECT TO FAIRNESS + HUMAN QA`

## Why this classification exists

E3 R2 uses a degree-5 longitudinal analytic patch chain compiled from shared station position / first-derivative / second-derivative jets. The failed run `31667359613` showed two different facts:

1. raw compiler-space C2 residuals are approximately machine-zero (`~1e-14` second derivative);
2. after independent derived control points are stored in Blender `mathutils.Vector` float representation, reconstructed second derivatives show approximately `5.27e-6` to `8.27e-6` residual.

The second observation must not be used to relax the compiler design threshold and must not be conflated with the separate rear-half fairness failure.

## Authority classification

### Compiler C2 authority

Authoritative continuity evidence remains the raw JSON/Python-float Surface Source compiler:

- max seam position error `<= 1e-7`;
- max tangent angle `<= 0.05°`;
- max second-derivative error `<= 1e-6`.

These thresholds are unchanged.

### Blender representation evidence

Blender does not own the analytic Surface Source in R2. Blender receives derived sampled execution geometry after the Surface Source is compiled. Therefore reconstructed second derivatives from separately quantized `mathutils.Vector` control points are retained as a **diagnostic representation residual**, not as a replacement C2 authority.

Runtime representation remains fail-closed through directly visible differential evidence:

- seam position representation must remain bounded;
- seam tangent-angle representation must remain `<= 0.05°`;
- seam normal-angle representation must remain `<= 0.05°`;
- runtime second-derivative residual must still be recorded in every report, but it does not override compiler-space C2 when source authority is not Blender float32 control points.

This is an evidence-class correction, not threshold relaxation.

## What this does not permit

This classification cannot convert a surface with failed interior fairness into PASS. The first R2 run also failed real rear-half normal-flow / curvature-rate checks, so R2 remains `ARCHITECTURE REVISE` until those source-jet values pass the existing fairness contract and Human Project/Visual QA.

No Class-A, engineering, manufacturing, PAP or Promotion authority is implied.
