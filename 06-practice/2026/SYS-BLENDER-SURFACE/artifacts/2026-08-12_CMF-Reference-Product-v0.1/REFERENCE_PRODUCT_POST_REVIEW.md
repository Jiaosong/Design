# 2026-08-12｜IP03｜CMF Reference Product｜Product Geometry × Material Binding Validation

**Model:** `OLEANDER_CMF_Reference_Product_v0.1`  
**Status:** `F1 PASS / CANDIDATE_AUTHORITY / PRODUCT-SCOPED D3 BINDINGS`  
**Scope:** designer visual validation / not engineering CAD

## Decision question
Can one representative product geometry expose and validate all five v1.20 D2 CMF process simulations under real product curvature, joints, scale, occlusion and material adjacency?

## Geometry
- overall bounds: `140 × 102.5 × 121.361 mm`
- PP: lower housing, upper lid, U-frame anchors
- PU: anti-slip/contact pad + front soft-contact grip
- powder-coated metal: continuous U-frame
- brushed/anodized aluminum: control knob + index
- milky diffuser: top signal/light field

The product is intentionally a benchmark object rather than a commercial design. Its geometry combines broad molded surfaces, long tubular curvature, soft-contact details, a machined/metallic control and a transmissive optical element in one compact object.

## Execution evidence
- Blender `5.2.0 LTS`, build `fbe6228777e7`
- GitHub Run `31549292487`
- Job `93968262669`
- Artifact `9123645565`
- Artifact SHA-256 `09c8d1957421906774fd0d255913c2324109115a5fc3029bc053ae8f7a004b82`
- Cycles CPU
- `720 × 720`, `8 samples`
- Adaptive Sampling + Persistent Data
- Scene Compile = 1
- six renders in `66 s`

## Machine QA
PASS:
- all five D2 Parameter Presets are bound;
- all mesh components are manifold;
- object scale is `1,1,1`;
- overall dimensional corridor passes;
- HERO / TOP / SIDE framing preflight passes;
- six required render views exist.

Run 1 is retained as audit evidence only. It rendered successfully but exposed two QA-contract defects: an artificially tight height corridor and a camera-matrix preflight calculation before view-layer update. The model was not rejected on those failures.

## Visual QA

### Whole product
PASS. The product reads as one compact portable desktop object rather than a collection of material coupons. The U-frame creates the highest silhouette reach, while the PP housing remains the dominant mass. Diffuser and knob create a coherent signal/control zone.

### Framing / clipping / occlusion
PASS. HERO, TOP and SIDE retain usable margins. The CMF macro intentionally crops the U-frame because its purpose is the knob–diffuser–PP junction, not whole-product framing.

### PP
PASS. Broad molded surfaces remain quiet and continuous. No visible procedural grain or over-bump is introduced by the larger real-product curvature.

### PU
PASS. The added front grip makes the soft-contact material visually inspectable without turning it into a decorative color block. PU remains subordinate to the PP field.

### Powder-coated metal
PASS. The continuous U-frame creates a long highlight path and exposes coating response across changing curvature. It does not read as exposed chrome.

### Brushed / anodized aluminum
PASS. The knob stays distinctly metallic and directional, especially in CMF Macro / Grazing, without turning into painted stripes or mirror chrome.

### Milky diffuser
PASS WITH CONTEXT LOCK. It retains a readable translucent edge and internal-light depth. Its brightness is intentionally a product-context signal and therefore becomes a product-scoped profile rather than changing the global D2 preset.

## Authority decision
`WORKING_SOURCE → CANDIDATE_AUTHORITY`

This is a reusable OLEANDER benchmark/reference product, but not engineering CAD and not a frozen canonical product. It may be revised when new modeling/render workers need a stronger stress test.

## Product-scoped D3 bindings
The generic v1.20 presets remain `D2 DESIGN_CALIBRATED`. The following bindings are locked only for this reference product:

- `REFPROD / PP Housing → D3 PROJECT_LOCKED_VISUAL_PROFILE`
- `REFPROD / PU Contact → D3 PROJECT_LOCKED_VISUAL_PROFILE`
- `REFPROD / Powder-Coated U-Frame → D3 PROJECT_LOCKED_VISUAL_PROFILE`
- `REFPROD / Brushed/Anodized Knob → D3 PROJECT_LOCKED_VISUAL_PROFILE`
- `REFPROD / Milky Diffuser → D3 PROJECT_LOCKED_VISUAL_PROFILE`

D3 here is a product-context visual lock. It makes no supplier, material-grade, tooling or physical-measurement claim.

## Next use
Use this model as the first shared benchmark for:
1. Modeling Worker regression;
2. material binding regression;
3. selective render retry;
4. Whole Product / Detail / CMF Macro QA;
5. future geometry, asset-catalog and render-cache validation.
