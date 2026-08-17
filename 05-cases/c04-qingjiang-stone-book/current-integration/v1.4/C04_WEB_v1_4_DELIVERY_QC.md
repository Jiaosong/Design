# C04 Web v1.4 — Delivery QC

Release candidate: `C04_WEB_v1_4_LOCALIZED_POLISH`

Skill invoked: current `oleander-delivery-qc`.

Status: `TECHNICAL / PACKAGE QC PASS FOR WEB CARRIER / DESIGN VERDICT SEPARATE`.

## 1. Package integrity

- Production runtime: `index.html / styles.css / app.js / assets/`.
- Editable/rebuildable source: `src/`; local rebuild reproduces root `index.html`, `styles.css`, and `app.js` byte-for-byte.
- No temporary portable/base64 readback HTML is included in the release package.
- v1.3 remains separate provenance and is not overwritten by v1.4.

## 2. Public-source hygiene

- Runtime scan: no `file://`, localhost, `127.0.0.1`, `/mnt/data`, or Windows absolute paths.
- Referenced local assets: all present; missing refs = 0.
- Public production-language residue scan removed `SUPPORT ONLY / RE-EDIT / 下一版 / PIXEL OPEN / MAIN KEEP / NO MAIN`.
- C04 rights handling follows current project instruction: minimal source tracing; asset-by-asset rights manifest is not a delivery blocker and no commercial-rights claim is made.

## 3. Browser / responsive readback

- 1920: `1920 == 1920` width; height `50241`; missing images `0`.
- 1366: `1366 == 1366` width; height `40128`; missing images `0`.
- 390: `390 == 390` width; height `49239`; missing images `0`.
- page errors: `0`.
- R13 interaction returns: `一线天`.
- Technical lightbox opens: `true`.
- Motion state readback: `ARRIVE → PASS → RETURN`.

## 4. Keyboard / interactive check

- focusable controls detected: 41.
- first Tab target: persistent `RETURN / 回程`.
- second Tab advances to an interactive button.
- Technical lightbox: ESC closes successfully.
- Return anchor remains available without pointer interaction.

## 5. Motion media

Existing reference film remains secondary concept material, not the final Motion deliverable:
- H.264, 1920×1080, 25 fps, duration 73.002 s.
- Web v1.4 scrollytelling does not claim to replace the final motion re-edit.

## 6. Non-blocking / bounded open items

R05 source pixel, P01 upstream presentation, Fluid Rest site/location, R06/R13 field/engineering/safety, and final Motion film remain open at their existing authority levels. They are not package-integrity failures and are not silently promoted.

## Sign-off

`WEB TECHNICAL DELIVERY QC = PASS`  
`INDEPENDENT FINISHED-PIXEL DESIGN VERDICT = PENDING`  
`PROJECT PROMOTION = NO`

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / FIELD PASS=NONE / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`
