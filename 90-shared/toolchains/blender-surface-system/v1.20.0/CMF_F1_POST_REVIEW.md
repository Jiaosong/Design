# OLEANDER Blender Surface System｜v1.20.0｜CMF Comparison Lab F1 Post-Review

**Status:** `F1 DESIGN VALIDATION PASS / 5 MATERIAL PRESETS D2 / REVIEW`

## Canonical evidence
- Blender 5.2.0 LTS / Cycles CPU
- Run `31511146453`
- Artifact `9109180350`
- Artifact SHA-256 `88600df62127d9586c64d66a0e705615812986c89519f37dcac096fb37b14636`
- `640×640 / 8 samples / Adaptive Sampling / Persistent Data / Scene Compile = 1`
- full 15-render Blender process time: `115 s`

## Decisions
- Fine Matte Powder-Coated Metal — `PASS → D2 DESIGN_CALIBRATED`
- Injection-Molded PP Fine Matte — `PASS → D2 DESIGN_CALIBRATED`
- PU Soft Matte Contact Surface — `PASS → D2 DESIGN_CALIBRATED`
- Brushed / Anodized Aluminum — `PASS → D2 DESIGN_CALIBRATED`
- Milky Transmissive Diffuser — `PASS AFTER ASSIST REVISION → D2 DESIGN_CALIBRATED`

## Revision chain
1. Run `31509223324`: executable PASS; test condition rejected because emitters were oversized relative to the 120 mm coupon.
2. Run `31509866030`: infrastructure failure only; corrupted compressed payload; no Blender evidence.
3. Run `31510040656`: emitter scale corrected but energy not distance-scaled; overexposure rejected.
4. Run `31510461281`: external Broad / Strip / Grazing rig valid; Diffuser assist still too strong.
5. Run `31511146453`: Canonical F1 evidence; Diffuser assist reduced to `1 W`.

Material center parameters remained locked while test conditions were corrected.

## Visual QA
Powder coat remains dielectric with a softened continuous highlight and no chrome/sandpaper/speckle artifact. PP remains clean molded polymer without visible procedural grain. PU reads softer than PP without pebbled-rubber caricature. Aluminum retains metallic directional response without painted stripes or mirror-chrome behavior. Diffuser retains milky transmission depth and Fresnel/edge behavior without clear-glass or flat-emission reading.

Run-4 → Run-5 isolation check: all 12 non-diffuser renders are pixel-identical; only the three diffuser renders changed.

## Promotion boundary
`D2` means design-calibrated Blender representation only. It does not mean measured physical properties. `D3 PROJECT_LOCKED_VISUAL_PROFILE` still requires the preset to be validated on project-specific geometry/context.

## Architecture note
This review is a current reusable toolchain record under `90-shared/toolchains/blender-surface-system/v1.20.0/`. Earlier `governance/`, `practice/`, and `tools/` paths on historical branches remain provenance only and do not define current repository architecture.

## Execution improvement
The next worker revision adds selective retry (`--only-material / --only-rig`) so a failed preset does not force the entire 5×3 matrix to rerender.
