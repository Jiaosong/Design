# C04 C22 Concept Masterplan CH14 v4.7 — Artifact Review Target

Status: `EXECUTED / ACTUAL PIXELS REOPENED / SOURCE RESERVED ON MAIN / DRAWING-SCOPED GITHUB REVIEW COMMENTED / INDEPENDENT PROFESSIONAL DESIGN REVIEW PENDING / NO SELF-KEEP`.

## User defects addressed
1. **v4.6 image conflict**: R06 Landscape First is removed from C22. v4.7 uses a new official Enshi Tourism Group source image `nb983qsaoo.jpg`, showing Qingjiang + cable + peak-forest/pinnacle relation.
2. **route illegibility**: route primary/branch/loop hierarchy is raised to 7 / 5 / 4 px in the source-geometry coordinate system and placed on a Bone Mist fade band; route remains subordinate to landscape but is now functionally readable.

## Source uniqueness readback
- Current C04 machine ledger checked before binding.
- No matching semantic-image / filename record for `nb983qsaoo` was present before reservation.
- C04 Notion search for `nb983qsaoo` returned no C04 usage.
- GitHub repository search for `nb983qsaoo` returned no prior use.
- Reservation PR #332 passed CI and was squash-merged to `main`: `6064f77981d7d83c32cf8f06be9ec7293f78841d`.
- Main ledger readback now records `IMG-C04-C22-MACRO-01 = RESERVED / LOCKED_TO_C22_CONCEPT_MASTERPLAN_UNTIL_EXPLICIT_RELEASE`.

## Source materialization
- Publisher: 恩施旅游集团.
- Official URL: `https://www.eslygroup.com/uploadfile/image/20230809/nb983qsaoo.jpg`.
- Persisted C22 pixel source: `C22_QINGJIANG_CABLE_PEAK_SOURCE_nb983qsaoo.jpg`.
- Persisted pixels: 850×567.
- SHA256: `9c68159a8897f33373e3d41f4347e071b8d2860958df84e41a682aa79d69cc2f`.
- Durable Drive copy: `1jadqGSfPfB0cPcGYsDA5fzlaTwh-uLK3`; raw readback bytes = 82,421.
- Method: Google Docs `insertInlineImage` fetched the official public HTTP source; DOCX export yielded the exact persisted JPEG used by C22.
- Boundary: this hash describes the persisted C22 materialization, not the website-original byte hash.
- Image generation: **NOT USED**.

## Route / registration
- Route geometry: existing project route carrier topology only.
- Source styling: not reused.
- Photo ↔ route geographic registration: **NONE**. The route is an explicit relational trace band, not a GPS/survey overlay.
- Same-cable Return remains explicit; no second return route invented.

## Actual-pixel readback
- 1920×1080 corrected PNG SHA256 `fb257a8c5b5872b2495ddb3b1d60da4ed5221289e536e70e241252c33acd6323`; browser/page errors = 0.
- 1366×768 corrected PNG SHA256 `26abd763ee154c3d7930a4bbd02dfa90c93725c69e31e549919e36ff2aebcd0b`; browser/page errors = 0.
- First-read order in producer readback: Qingjiang/cable/pinnacle → route primary/branch/loop → optional reading edge.

## Runtime evidence correction
The first 1366 export used an invalid scaling script that globally replaced internal `1920×1080` dimensions and exposed the dark browser background on the right/bottom. That evidence was discarded. The corrected scaler changes **only the root SVG viewport size**; internal geometry remains unchanged. Corrected 1366 actual pixels retain the full Bone Mist page, readable route hierarchy and intact PAGE/TRACE edge.

## GitHub drawing scrutiny
- PR #324, v4.7 head review record: `4973912357` (`COMMENT`, not APPROVE).
- AI Governance Evals on v4.7 pre-runtime-fix head: #2632 = SUCCESS; final runtime-fix head CI must remain green before closure.
- This drawing-scoped review is not an independent Professional Design verdict.

## Open for independent design review
1. whether the lower Bone Mist transition integrates route and landscape without looking like a separate infographic strip;
2. whether route labels/legend are sufficiently subordinate at 1920 while remaining readable at 1366;
3. whether right reading edge should retreat another optical step;
4. whether the new landscape source is sufficiently C22-specific for final chapter ownership.

No producer `KEEP / MAIN / Professional Design PASS`.
