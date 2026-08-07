# v3.3 QA Report — Photography Render Lock

## Source / runtime gates
- HTML / CSS / SVG page source remains editable: **PASS**
- Complete AI-generated page / board references used as formal page: **NONE**
- Five photography modules: **PASS**
- Three.js: **0.174.0 pinned**
- postprocessing: **6.39.4 pinned**
- model-viewer: **4.1.0 pinned / inspection only**

## Executable WebGL photography calibration
**Calibration:** `CAL-20260807-1721-SWIFTSHADER`  
**Environment:** Chromium non-headless under Xvfb + Chrome DevTools Protocol  
**API:** `WebGL 2.0 (OpenGL ES 3.0 Chromium)`  
**Renderer:** `ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)`

- Housing highlight: **PASS**
- Diffuser volume: **PASS**
- Metal knob reflection: **PASS**
- Contact shadow falloff: **PASS**

Result: **`FOUR-GATE PASS / FINAL HERO-CMF RENDER PROFILE LOCKED`**.

Binary screenshot evidence is stored in the OLEANDER File Library v3.3-web calibration/final_lock directory. `calibration/CALIBRATION_REPORT_v3.3.md` and `calibration/FINAL_RENDER_LOCK_v3.3.json` carry the textual evidence chain in GitHub.

The earlier GitHub Actions run/artifact identifiers were removed because they were not the evidence chain used for this real calibration.

## Boundary
The render lock is a visualization-quality decision. Engineering validation remains pending, and integrated production-page browser QA is a separate release gate.
