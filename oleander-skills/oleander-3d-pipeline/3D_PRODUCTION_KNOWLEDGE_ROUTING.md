# OLEANDER 3D Production Knowledge Routing

Status: **CANDIDATE EXECUTION BINDING / NO SILENT PROMOTION**

Purpose: bind the existing `oleander-3d-pipeline` to the Current Notion 3D Production knowledge stack. This is not a second Skill and does not replace project Source Authority, Artifact Review, CAD/manufacturing authority, or the computer-graphics quality gates.

Canonical framework: Notion `FW-CG-3D-PRODUCTION-001｜3D Production Knowledge Stack｜建模—程序化—表面—材质—渲染—技术美术`.

## 1. Routing principle

Route by **representation/problem**, then by software worker. Do not begin from a favorite application or plugin.

`SOURCE AUTHORITY → REPRESENTATION CHOICE → PRIMARY MASS → INTERFACES → CONTINUITY / TOPOLOGY → DETAIL FREQUENCY → MATERIAL / LIGHT DIAGNOSTIC → TARGET RUNTIME → ACTUAL PREVIEW REVIEW`

Software is a Worker. Stable modeling/rendering knowledge remains cross-software where possible; version-specific operation belongs in the corresponding DCC evidence object.

## 2. Modeling-method selection

For choosing between polygon, SubD, NURBS, CAD/B-Rep, sculpt/remesh, curve/spline, Boolean/kitbash or procedural modeling, resolve:

- `KN-METHOD-3D-MODELING-PARADIGMS-001`.

For the default OLEANDER modeling sequence and evidence discipline, resolve:

- `KN-METHOD-OLEANDER-3D-MODELING-001`;
- existing `KN-METHOD-3D-REFERENCE-CALIBRATION-001` when reproducing a real object/reference;
- existing Claim-bound Camera knowledge when camera/projection is part of the claim.

Do not add secondary screws, trims, shader noise or microdetail before primary mass, negative space, interfaces, sections and representation choice are credible.

## 3. Rhino / industrial freeform surface route

Trigger: NURBS, industrial/product surface, sweep/loft/network, MatchSrf, BlendSrf, G0/G1/G2, zebra, trimmed surface, Rhino SubD, STEP/IGES surface handoff.

Resolve together:

- `KN-METHOD-RHINO-SURFACE-MODELING-001`;
- `EVD-DCC-RHINO8-SURFACE-TOOLS-001`;
- `EVD-CG-SURFACE-CONTINUITY-001`.

When the claim becomes fit-critical/manufacturing-parametric, co-route to `PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md`. Rhino visual smoothness alone does not certify Class-A, tolerance or manufacturability.

## 4. Polygon / SubD DCC route

Trigger: traditional polygon modeling, topology, hard surface, subdivision, bevel/support loops, retopology, deformation topology.

Resolve:

- `KN-METHOD-DCC-POLYGON-SUBD-001`;
- `EVD-CG-SURFACE-CONTINUITY-001` for surface/normal/reflection claims.

Worker-specific evidence:

- Blender → `KN-METHOD-BLENDER-PRODUCTION-001` + `EVD-DCC-BLENDER-NATIVE-5_2-001`;
- Maya → `EVD-DCC-MAYA-2027-MODELING-001`;
- 3ds Max → `EVD-DCC-3DSMAX-2027-MODELING-001`.

Topology is judged by silhouette, curvature, shading, deformation, UV/bake and downstream requirements—not by a universal all-quads rule.

## 5. Blender native + Geometry Nodes route

Trigger: Blender mesh/edit operations, modifiers, curves, sculpt, multires/remesh, UV, native nodes, Geometry Nodes, procedural asset generation.

Resolve:

- `KN-METHOD-BLENDER-PRODUCTION-001`;
- `EVD-DCC-BLENDER-NATIVE-5_2-001`;
- `EVD-DCC-BLENDER-GEOMETRY-NODES-5_2-001` for fields/attributes/domains/instances/node tools.

Use native Mesh/Modifier/Curve/Sculpt/GN/Asset Browser/Python capabilities before introducing an external addon unless the addon passes the plugin-adoption gate.

For Geometry Nodes, retain exposed input contract, seed, named attributes, instance/realize policy, output counts/bounds, cache state and export readback when material.

## 6. Grasshopper / parametric route

Trigger: Rhino Grasshopper, Data Tree, parametric facade/panel/grid, attractor, algorithmic spatial/product generation, bake management.

Resolve:

- `KN-METHOD-GRASSHOPPER-PARAMETRIC-001`;
- existing `PRAC-20260809-01｜SP02 Grasshopper Data Tree｜Spatial Practice` as prior practice evidence.

Tree/list structure must be understood before Graft/Flatten/Simplify changes. Preview geometry is not silently the Rhino document master; bake/output identity must be explicit.

## 7. Houdini procedural / technical-art route

Trigger: Houdini SOP, attributes, VEX/Wrangle, HDA, packed/instances, terrain, procedural generation, simulation, Solaris/LOP/USD, Karma/MaterialX.

Resolve:

- `KN-METHOD-HOUDINI-PROCEDURAL-001`;
- `EVD-DCC-HOUDINI21-PROCEDURAL-001`;
- `KN-METHOD-TECHNICAL-ART-3D-001` when runtime/performance/asset-system claims are involved.

Keep Point/Vertex/Primitive/Detail attribute ownership explicit. Separate SOP geometry processing from LOP/USD scene composition. Simulation caches are derivatives/evidence with seed, scale and solver context, not automatic physical truth.

## 8. SketchUp spatial route

Trigger: SketchUp massing, architectural/spatial direct modeling, groups/components, solid tools, section scenes, conceptual terrain.

Resolve:

- `KN-METHOD-SKETCHUP-SPATIAL-MODELING-001`;
- `EVD-DCC-SKETCHUP2026-NATIVE-001`.

Use Groups/Components to prevent raw-geometry contamination. SketchUp is not promoted as final authority for high-quality G2 industrial surfaces, character sculpting or manufacturing B-Rep.

## 9. Surface-detail / high-low / UV / bake route

Trigger: sculpt detail, retopology, high-to-low, UV/UDIM, bake, normal/height/displacement, decal, trim sheet, micro-imperfection.

Resolve:

- `KN-METHOD-SURFACE-DETAIL-TEXTURE-001`;
- `EVD-TEXTURE-SUBSTANCE-PIPELINE-001` when Painter/Designer or mesh-map-driven texturing is used;
- `EVD-CG-SURFACE-CONTINUITY-001` when the detail changes actual form/surface claims.

Route detail frequency deliberately: macro → geometry; meso → geometry/displacement where justified; micro → normal/bump/roughness where silhouette authority is not required.

## 10. Material nodes / texture choice and processing route

Trigger: shader/material nodes, texture libraries, scans, procedural textures, texture selection, map generation/cleanup, channel packing, Substance.

Resolve:

- `KN-METHOD-SHADING-TEXTURING-001`;
- `EVD-TEXTURE-MAP-SELECTION-PROCESSING-001`;
- `EVD-TEXTURE-SUBSTANCE-PIPELINE-001` when applicable;
- `EVD-CG-BSDF-MICROFACET-001` for BSDF/Fresnel/roughness/metal/dielectric logic;
- `EVD-CG-COLOR-PIPELINE-001` for color-vs-data encoding and display comparison.

Texture selection order is material/process/physical scale/camera/texel-density/channel semantics before nominal resolution. Do not derive every PBR map from base-color grayscale by default.

## 11. Lighting / renderer / compositing route

Trigger: lighting, product light cards, architectural light, HDRI, renderer choice, samples, AOV, denoise, color management, compositing.

Resolve:

- `KN-METHOD-RENDER-LIGHTING-PRODUCTION-001`;
- `EVD-RENDERER-PRODUCTION-MATRIX-001`;
- `EVD-CG-LIGHTING-RADIOMETRY-001`;
- `EVD-CG-LIGHT-TRANSPORT-SAMPLING-001`;
- `EVD-CG-COLOR-PIPELINE-001`;
- `COMPUTER_GRAPHICS_QUALITY_LAYER.md` and CG-Q01—CG-Q10 for retained quality claims.

Diagnostic lighting precedes hero/narrative lighting when surface/material quality is under review. Offline renderer beauty does not replace target-runtime proof.

## 12. Technical Art / runtime route

Trigger: LOD/HLOD, Nanite or analogous virtualized geometry, instances, draw/setup cost, shader complexity, vertex data, runtime texture/streaming, Unreal/Unity/web engine, profiling, DCC bridge, export automation.

Resolve:

- `KN-METHOD-TECHNICAL-ART-3D-001`;
- `EVD-TA-RUNTIME-PIPELINE-001`;
- `EVD-CG-INTERCHANGE-PBR-001` for appearance handoff.

Use measured profiling, not universal triangle/material/sample budgets. Preserve DCC source, export artifact, target import settings, runtime readback and known losses.

## 13. Plugin / addon route

Trigger: addon/plugin selection, Hard Ops/Boxcutter-like tools, Max/Rhino/SketchUp ecosystems, SideFX Labs, scatter/retopo/UV/render bridges.

Resolve:

- `KN-METHOD-PLUGIN-TOOLCHAIN-GOV-001`;
- `EVD-PLUGIN-3D-ECOSYSTEM-20260830` only as **REVIEW / candidate evidence**.

Never infer that a plugin is installed, compatible or approved from its presence in the landscape page. Before Current adoption require native-alternative comparison, version pin, reopen test, standard bake/export fallback, license/redistribution state and no hidden destructive rewrite.

## 14. Cross-renderer / exchange route

For GLB/glTF, USD, FBX, Alembic or renderer/DCC appearance drift, resolve:

- `EVD-CG-INTERCHANGE-PBR-001`;
- relevant worker page above;
- target-runtime TA page when interactive.

`EXPORT PASS ≠ REOPEN PASS ≠ APPEARANCE MATCH ≠ DESIGN PASS`.

## 15. Production handoff record

For a retained 3D result, capture the applicable subset:

- source/master identity and software/version;
- representation type and reason;
- scale/units/axis/origin;
- primary-mass + interface + silhouette/section evidence;
- topology/continuity/normal strategy;
- modifier/history/node/HDA/GH dependency state;
- surface-detail carrier and UV/bake state;
- material/texture semantic record;
- lighting/renderer/sampling/color state;
- plugins/addons and versions actually used;
- target-runtime/export/reopen state;
- technical-art profile when applicable;
- CG-Q01—CG-Q10 status where applicable;
- remaining physical/field/engineering/manufacturing HOLD.

## 16. Maturity boundary

Notion documentation and source synthesis can reach AI-ready routing, but software-specific knowledge is not `M6 PRACTICED` until a real native/target artifact is executed and read back. Do not promote a DCC/plugin/runtime method merely because its documentation is comprehensive or CI is green.