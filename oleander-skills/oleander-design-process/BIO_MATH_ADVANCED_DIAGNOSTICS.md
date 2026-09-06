# OLEANDER Bio–Math Advanced Computational Form Diagnostics

Status: **CANDIDATE DIAGNOSTIC EXTENSION / DESIGN-PROCESS OWNER / NO SILENT PROMOTION**

Upstream bridge: `BIO_MATH_STREAMLINED_FORM_EXTENSION.md`.

Current Notion owner: `KN-THEORY-BIO-MATH-STREAMLINED-FORM-001`.

Use this layer only when the design question materially needs advanced computational mathematics. Do not route here merely to make a project sound scientific.

## 1. Morse / Reeb / topology-transition route

Trigger: critical points, level sets, contour evolution, merge/split of regions, scalar-threshold topology change, Reeb graph, Morse decomposition.

Resolve `EVD-FORM-MORSE-REEB-TOPOLOGICAL-TRANSITIONS-20260830-001`.

Record the scalar function `f`, domain, discretization, critical-point policy, threshold/filtration and simplification/persistence policy. A Reeb graph is a summary relative to a chosen scalar function, not a complete geometric description of a solid.

Anti-shortcut: `REEB GRAPH ≠ COMPLETE SOLID DESCRIPTION`.

## 2. DEC / Hodge / direction-field route

Trigger: differential forms, surface vector fields, exact/coexact/harmonic components, cross fields, intrinsic field transport, cohomology, seamless direction patterns.

Resolve `EVD-FORM-DEC-HODGE-FIELD-TOPOLOGY-20260830-001` plus the existing differential-geometry and topology objects.

Record form/domain placement, discrete operator, boundary conditions, topology, singularities and mapping to geometry. Distinguish a mathematical/design field from a measured/solved physical flow or stress field.

Anti-shortcut: `DEC / HODGE FIELD ≠ PHYSICAL FLOW`.

## 3. TPMS / implicit porous route

Trigger: Gyroid, Diamond, Primitive, TPMS, triply periodic porous structure, implicit periodic lattice, sheet TPMS, graded TPMS.

Resolve `EVD-FORM-TPMS-IMPLICIT-POROUS-GEOMETRY-20260830-001` plus implicit/SDF, field and manufacturing evidence when applicable.

Record family/function, period/cell scale, level-set/offset, wall or sheet thickness, relative density/porosity, grading/orientation, boundary transition and source representation. Preserve the implicit/parametric master when continued grading/editability matters.

Anti-shortcut: `IDEAL TPMS ≠ PRINTED PART ≠ MEASURED PERFORMANCE`.

## 4. Stochastic distribution / sampling route

Trigger: Poisson disk, blue noise, controlled random scatter, CVT, Lloyd relaxation, density-driven points, pore/particle/vegetation distribution.

Resolve `EVD-FORM-STOCHASTIC-SAMPLING-DISTRIBUTION-20260830-001`.

Record density field, metric, minimum-distance/energy rule, boundary behavior, anisotropy, seed and target distribution statistics. Preserve seed/reproducibility for comparisons.

Anti-shortcuts:
- `RANDOM() ≠ NATURAL DISTRIBUTION`;
- `VORONOI + JITTER ≠ BLUE NOISE`;
- `EVEN-LOOKING ≠ CORRECT SAMPLING`.

## 5. L-system / formal growth grammar route

Trigger: L-system, rewrite grammar, developmental branching, turtle geometry, rule-based plant/tree/coral-like growth.

Resolve `EVD-FORM-LSYSTEM-FORMAL-GRAMMAR-20260830-001` and Biomimicry only if a biological mechanism claim is retained.

Record axiom, productions, parallel/context-sensitive semantics, parameters, derivation depth, stochastic seed, environmental input and geometry interpreter.

Anti-shortcuts:
- `TREE-LIKE OUTPUT ≠ L-SYSTEM`;
- `L-SYSTEM ≠ TRUE BOTANY`;
- `PROCEDURAL GROWTH ≠ BIOLOGICAL SIMULATION`.

## 6. Spectral geometry route

Trigger: Laplace–Beltrami eigenfunctions/eigenvalues, spectral modes, diffusion/wave kernel, intrinsic multiscale shape basis, spectral segmentation or correspondence.

Resolve `EVD-FORM-SPECTRAL-GEOMETRY-20260830-001`.

Record Laplacian discretization, mass/normalization, boundary conditions, selected mode/band and whether the intended meaning is intrinsic geometry, data basis or actual physics.

Anti-shortcut: `SPECTRAL EIGENMODE ≠ PHYSICAL VIBRATION MODE` unless the actual physical operator is being solved.

## 7. Fractal / multiscale route

Trigger: fractal, self-similar, self-affine, recursive geometry, scale invariance, lacunarity, multiscale roughness.

Resolve `EVD-FORM-FRACTAL-MULTISCALE-GEOMETRY-20260830-001` plus L-system when formal rewriting is involved.

Record whether the claim is exact, statistical or topological self-similarity, the finite scale interval, recursion/branch ratios, sampling resolution and the role of macro/meso/micro frequency bands.

Anti-shortcuts:
- `FRACTAL-LIKE ≠ FRACTAL MEASUREMENT PASS`;
- `FRACTAL ≠ NATURAL ≠ EFFICIENT`;
- one fractal-dimension number does not establish visual, biological or performance quality.

## 8. Choosing the mathematics

Do not stack methods because they all produce organic-looking forms. Choose the smallest causal owner set:

`DESIGN QUESTION → INVARIANT / FIELD / DYNAMICS / OPTIMIZATION / DISTRIBUTION / GRAMMAR → MINIMUM MATHEMATICS → GEOMETRIC REPRESENTATION → TEST`.

Examples:
- topology changes across threshold → Morse/persistence, not SubD;
- coherent line orientation on a surface → direction field/DEC, not random curves;
- continuous graded porous material → implicit/TPMS only if that family fits, not generic Voronoi;
- natural-looking scatter → stochastic sampling, not arbitrary jitter;
- developmental branching → grammar/dynamics, not merely a tree mesh;
- multiscale intrinsic shape basis → spectral geometry, not a physical vibration claim.

## 9. Required readback

For any advanced-math route, retain:

- mathematical object and definition used;
- source/authority;
- domain and representation;
- variables/parameters;
- boundary/initial conditions when material;
- discretization/sampling;
- solver/algorithm and convergence/iteration policy when material;
- design mapping;
- sensitivity/failure test;
- neutral geometry/field readback;
- visual readback;
- physical/biological/manufacturing HOLDs.

`MATHEMATICAL IMPLEMENTATION PASS ≠ DESIGN KEEP ≠ PHYSICAL OR BIOLOGICAL TRUTH`.
