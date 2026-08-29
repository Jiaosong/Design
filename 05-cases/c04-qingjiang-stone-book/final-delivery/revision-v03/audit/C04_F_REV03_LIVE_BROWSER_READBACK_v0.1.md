# C04｜F REV03 Offline Web｜Live-Browser Responsive Readback v0.1

Status: `EVIDENCE PASS / EXACT F WEB HOLD`

Hard boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION`.

## Exact F artifact availability
- PR #114 manifest declares `outputs.web = web/index.html`.
- Exact branch path `05-cases/c04-qingjiang-stone-book/final-delivery/revision-v03/web/index.html` returned `404 NOT FOUND`.
- Connected Drive search returned no executable REV03 web match.
- PR-head workflow lookup surfaced only AI Governance Evals; no REV03 web artifact was surfaced.
- Therefore exact F REV03 live-browser artifact readback remains `HOLD_EXACT_F_ARTIFACT_UNAVAILABLE`.

## Browser evidence used instead
Per owner instruction, the frozen QJ-E portable HTML was loaded into an actual Chromium live DOM and tested. The old local-navigation policy was not used as a stop condition.

Browser: Chromium 144.0.7559.96.

### Responsive matrix
- `1920×1080`: no horizontal overflow; map M5 activation PASS; `UNKNOWN × OFFLINE` fail-closed PASS.
- `1366×768`: no horizontal overflow; map M5 activation PASS; `UNKNOWN × OFFLINE` fail-closed PASS.
- `390×844`: no horizontal overflow; map M5 touch activation PASS after Web-only responsive patch; `UNKNOWN × OFFLINE` fail-closed PASS.

### Interaction
- Keyboard `Tab → Enter` on Reading filter: PASS.
- Keyboard `Tab → Enter` into prototype Route: PASS.
- 390 touch: Service → UNKNOWN → OFFLINE: PASS; optional depth OFF; return primary; human confirmation required; pseudo-live prediction prohibited.
- 390 touch: S0 Digital Silence: PASS; header/nav removed.
- 390 scroll: PASS.

## Integration blocker and repair
Frozen E exposed one real mobile Web integration blocker: SVG node hit area collapsed below reliable touch size and the mobile map detail overlaid the map body. E source was not modified. A Web/F-only patch was validated:
- mobile map-stage reflow so detail and map are both visible;
- mobile-only invisible map-node hit targets (~46.6 CSS px on tested M5).
No route/content/state/feature/evidence authority changed.

## Print readback
Frozen `print/report.html` was printed by Chromium: `8 pages / A4`; all 8 pages rendered and visually reviewed PASS. Browser output is not byte-identical to the frozen PDF because of browser/font rendering, but page count, page geometry, hierarchy and clipping review pass.

## Evidence package
Google Drive: `C04_F_REV03_WEB_LIVE_BROWSER_READBACK_v0.1.zip`
- file id: `1oEEzyd0Unmsy5Q7kPggjEZpQ4yf-uE9y`
- size readback: `7,764,893 bytes`
- local ZIP SHA-256: `c97bc98edb7d122611ed10dd335ab7ecb2bd7a6b22d5c1071b726040a7605439`
- contains 13 actual Chromium screenshots, browser-print PDF, contact sheets, machine readback JSON, responsive patch and SHA manifest.

## Direct independent-review conclusion
- `PASS`: E portable browser behavior after Web-only responsive integration repair.
- `REVISE`: no remaining E/Web evidence defect found after repair.
- `HOLD`: exact F REV03 Offline Web live-browser readback because the manifest-referenced executable is not retrievable from connected sources.

When exact F `web/index.html` becomes available, rerun the same matrix only. Do not redesign E or add features.