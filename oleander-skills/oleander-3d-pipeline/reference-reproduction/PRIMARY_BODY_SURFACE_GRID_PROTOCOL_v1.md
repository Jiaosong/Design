# Primary Body Surface Grid Protocol v1

Status: CURRENT CANDIDATE / extracted from the 992.2 V25–V30 benchmark.

## INPUT
- locked hard points and axle/wheel geometry;
- orthographic SIDE / FRONT / REAR reference envelopes;
- last-known-good per-gate baselines;
- sparse Source families for plan width, hood/deck spine, shoulder/fender crown, lower envelope and terminal return;
- current visible primary body mesh.

## MUST CHECK
1. **Primary mass precedes detail.** Do not spend iterations on lamps, seams, CMF or trim while hood/fender/quarter/body section remains generic.
2. **Dense evaluation does not replace sparse authority.** A denser visible grid may be regenerated from sparse causal controls; it must not silently become Source Authority.
3. **Longitudinal and transverse causality are separate.** SIDE X/Z silhouette, plan width and Y/Z section must each be represented and independently screened.
4. **Wheel-arch / rocker / bumper lower envelope stays locked after it passes.** A new body representation cannot reopen passing lower geometry without an explicit failed-gate reason.
5. **Fender crown and rear haunch are part of the same body grid.** They are not floating volumes or detail meshes.
6. **Terminal plan curvature belongs in the body grid.** Do not close a production-like body with a constant-X flat cap and then cover it with fascia detail.
7. **Surface grid must remain locally ordered.** Adjacent rails/stations must not form bow-ties, inverted strips, stretched spikes or disconnected visible islands.
8. **Topology screening is not surface-quality proof.** Connected components = 1 and normal flips = 0 do not prove reflection flow or reference fidelity.
9. **Representation experiments retain strict best-known locks.** Never widen regression thresholds because the new grid is exploratory.
10. **Actual 3/4 readback remains mandatory.** Orthographic compliance cannot prove body wrap, rear-engine mass distribution, fender-to-hood tension or shoulder flow.

## ALLOWED
- increase evaluated longitudinal station / section-rail density;
- rebuild the primary body grid while preserving the same sparse Source semantics;
- use wheel/axle influence functions to create causal fender crowns;
- use Y-dependent terminal X setback for rounded nose/tail plan curvature;
- keep a simpler cabin during a body-surface experiment if aperture authority and visual review status remain explicit.

## FORBIDDEN
- `more polygons = higher fidelity`;
- lowering regression standards for a representation experiment;
- using separate visible blobs for front fender or rear haunch when the reference reads as one shell;
- adding detail to disguise boxy/faceted primary form;
- promoting a smoother mesh without independent visual KEEP.

## EVIDENCE
- Source-control digest and protected families;
- final evaluated body station/rail counts;
- connected-component and adjacent-normal/fold evidence;
- SIDE + FRONT + REAR projection receipts;
- front/rear 3/4 beauty views;
- regression receipt against best-known per-gate baselines;
- independent visual review before promotion.

## FAIL / HOLD
- `FAIL_PRIMARY_BODY_GRID_FOLD`
- `FAIL_PRIMARY_BODY_TERMINAL_CAP`
- `FAIL_PROTECTED_LOWER_ENVELOPE_REGRESSION`
- `REJECT_DENSE_GRID_GENERIC_FORM`
- `HOLD_REFLECTION_FLOW_NOT_REVIEWED`
- `HOLD_INDEPENDENT_VISUAL_KEEP_REQUIRED`

## 992.2 benchmark
V25–V29 repeatedly changed greenhouse topology while the underlying primary body still read as a generic slab/crown loft. V30 therefore shifts the causal frontier to the body itself: a denser longitudinal ring grid, integrated fender/haunch crown, locked wheel/lower-envelope geometry and terminal plan curvature. This is a representation experiment only; strict V25 best-known regression locks remain in force and visual fidelity remains HOLD.
