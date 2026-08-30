# OLEANDER Modeling Essence Deep Diagnostics

Status: **CANDIDATE KNOWLEDGE BINDING / NO SILENT PROMOTION**

Purpose: extend the existing `oleander-3d-pipeline` with cross-software diagnostics for curve/surface mathematics, mesh topology, parameterization, fairing, robust intersections and subdivision semantics. This file does not create a second 3D Skill and does not prove native DCC/CAD practice.

Canonical parent: Notion `KN-THEORY-3D-MODELING-ESSENCE-001`.

## 1. Spline / NURBS structure

Trigger: Bezier, B-Spline, NURBS, degree/order, CV count, knots, multiplicity, spans, rational weights, curve rebuild/refit, unexplained curve waviness.

Resolve:
- `EVD-MODELING-SPLINE-NURBS-MATHEMATICS-20260830-001`;
- `KN-METHOD-RHINO-SURFACE-MODELING-001` when Rhino surface quality is involved;
- `EVD-CG-SURFACE-CONTINUITY-001` for retained reflection/continuity claims.

Do not equate control density with precision. Record degree/order, CV count, span/knot structure, multiplicity, rational/weight state, parameter domain and curvature/fairness readback. Knot insertion and degree elevation may change representation structure without changing the curve locus; degree reduction and knot removal generally require approximation/error control.

Anti-shortcut: `MORE CVS ≠ MORE ACCURACY ≠ BETTER FAIRNESS`.

## 2. Half-edge / Euler topology

Trigger: edge split/collapse/flip, join/split face, manifold repair, remesh topology drift, UV/weight/material data changing after connectivity edits.

Resolve:
- `EVD-MODELING-HALFEDGE-EULER-TOPOLOGY-20260830-001`;
- `EVD-MODELING-TOPOLOGICAL-VALIDITY-20260830-001`;
- `EVD-MODELING-MESH-PROCESSING-ALGORITHMS-20260830-001`.

Treat geometry and combinatorial connectivity separately. Check manifold/link conditions, border/orientation, topology delta and attribute-domain identity. Vertex/face indices are implementation identifiers unless the project explicitly establishes stronger semantic identity.

Anti-shortcut: `SMALL GEOMETRIC ERROR ≠ SAFE TOPOLOGY EDIT`.

## 3. UV / surface parameterization

Trigger: unwrap, seam placement, LSCM/harmonic/angle-based methods, stretch, texel density, lightmap, pattern/fabric mapping, UV transfer.

Resolve:
- `EVD-MODELING-UV-PARAMETERIZATION-DISTORTION-20260830-001`;
- `EVD-MODELING-PROXIMITY-PROJECTION-INTERSECTION-20260830-001` when correspondence/transfer is involved;
- texture/bake knowledge when the map becomes a production texture carrier.

First declare the target distortion objective: angle/conformal, area, metric/directional, non-overlap, source correspondence or perceptual sampling. Then define seam/cut graph, boundary/pin conditions and target texel policy. There is no context-free best unwrap or universal equal-texel-density rule.

## 4. Fairing / smoothing

Trigger: Smooth, Relax, Laplacian smoothing, scan denoise, surface fairing, curvature cleanup, noisy reflection flow.

Resolve:
- `EVD-MODELING-FAIRING-SMOOTHING-ENERGY-20260830-001`;
- source reconstruction/deviation evidence when scan or measured geometry is involved;
- NURBS continuity/fairness knowledge for industrial surface work.

State protected borders/interfaces/features, smoothing/fairing operator or energy, fitting strength, iteration policy and source deviation. Check silhouette, volume, curvature and boundary drift after the operation.

Anti-shortcut: `SMOOTHER ≠ FAIRER ≠ CLOSER TO SOURCE`.

## 5. Robust Boolean / intersection

Trigger: random Boolean failure, coplanar/near-coincident shells, tiny sliver faces, self-intersections, tolerance escalation, inconsistent result topology.

Resolve:
- `EVD-MODELING-BOOLEAN-INTERSECTION-ROBUSTNESS-20260830-001`;
- `EVD-MODELING-NUMERICAL-TOLERANCE-ROBUSTNESS-20260830-001`;
- `EVD-MODELING-TOPOLOGICAL-VALIDITY-20260830-001`;
- `EVD-MODELING-GEOMETRIC-OPERATORS-20260830-001`.

Diagnose stages separately: input validity → intersection configuration → numerical predicates/tolerance → splitting/corefinement → region classification → topology reconstruction → small-feature/reference readback. Never enlarge tolerance repeatedly until a result appears without checking what geometry is being merged or lost.

Anti-shortcut: `BOOLEAN EXISTS ≠ BOOLEAN VALID ≠ DOWNSTREAM SAFE`.

## 6. Subdivision / limit surface

Trigger: Catmull-Clark/Loop/SubD, support loops, crease/sharpness, extraordinary vertices/poles, UV seam behavior, viewport subdivision level, cross-DCC SubD handoff.

Resolve:
- `EVD-MODELING-SUBDIVISION-LIMIT-SURFACE-20260830-001`;
- `EVD-MODELING-HALFEDGE-EULER-TOPOLOGY-20260830-001` for cage connectivity;
- `EVD-CG-SURFACE-CONTINUITY-001` for reflection/surface-quality claims.

Separate base control cage, subdivision scheme, boundary rules, crease/sharpness tags, extraordinary valence, face-varying topology, mathematical limit surface and finite evaluated/display sampling. More viewport levels only improve approximation density; they do not repair a poor cage, crease policy or UV face-varying discontinuity.

Anti-shortcut: `SUBDIV LEVEL ↑ ≠ CONTROL TOPOLOGY BETTER ≠ LIMIT SURFACE BETTER`.

## 7. Diagnostic carrier set

When one of these issues is material, prefer the smallest evidence set that can expose the cause:
- curve: CV polygon + knots/spans + curvature graph + section/reflection;
- topology: wireframe/halfedge-domain inspection + manifold/boundary report + attribute-domain before/after;
- UV: checker/distortion heatmap + seam graph + target-size texture/readback;
- fairing: before/after silhouette + source deviation + curvature/reflection + protected-interface check;
- Boolean: operand validity + intersection configuration + result topology + tiny-feature/readback;
- SubD: control cage + crease/valence/FVar view + neutral reflection on evaluated limit approximation.

## 8. Maturity boundary

These objects are tutorial/documentation-translated evidence. They may improve routing and causal diagnosis, but remain below `M6 PRACTICED` until a real native artifact demonstrates the claimed operation, failure case, correction and reopen/readback. A passing schema or governance workflow is not native modeling evidence.
