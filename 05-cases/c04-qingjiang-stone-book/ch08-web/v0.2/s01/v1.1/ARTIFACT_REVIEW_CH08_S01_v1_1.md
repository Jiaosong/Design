# CH08-S01 v1.1｜OLEANDER Artifact Review Record

Review scope: current producer candidate only. This record does **not** issue Professional Design KEEP and does not convert the object into a release candidate.

## Common Review｜AR-G01—AR-G10

| Gate | State | Evidence / boundary |
|---|---|---|
| AR-G01 Identity & Naming | PASS | `PRJ-C04-QINGJIANG-SHISHU / CH08 / CH08-S01-MAIN / v1.1` are explicit across source lock, owner receipt and package. |
| AR-G02 Version & Status | PASS | `PRODUCER CANDIDATE / INDEPENDENT DESIGN REVIEW PENDING / NO_PROMOTION` is explicit. |
| AR-G03 Completeness | PASS FOR PRODUCER PACKAGE | ZIP contains authored HTML/CSS, exact source carrier, Image Ops contract and required target-size/off-state readbacks. |
| AR-G04 Internal Consistency | PASS | source ID/hash, semantic slot, generation OFF and truth boundary agree across current records. |
| AR-G05 Cross-file Consistency | PASS WITH MIRROR NOTE | GitHub is the lightweight text/source-lock mirror; the immutable ZIP is the binary byte authority. Formatting of JSON mirrors may differ without changing recorded values. |
| AR-G06 Evidence & Truth | PASS | source-grounded image use is separated from FIELD/geometry/service/safety claims; `FIELD=0 / G1F HOLD / NO_PROMOTION`. |
| AR-G07 Open & Integrity | PASS | independently retrieved Drive ZIP tested with `unzip -t`; all 16 entries opened without compression errors; source hash rechecked inside ZIP. |
| AR-G08 Reproduction | PARTIAL | exact authored page was rerendered for desktop/mobile and operation-off states; live deployed URL/file-navigation evidence is not claimed. |
| AR-G09 Change Traceability | PASS | revoked v0.5 source remains revoked; v0.9 → v1.0 study → v1.1 delta and Image Ops bindings are recorded. |
| AR-G10 Final Artifact Review | OPEN / INDEPENDENT VISUAL VERDICT REQUIRED | final desktop/mobile/grayscale/effect-off pixels exist; producer does not issue first-visual or portfolio-worthiness verdict. |

## Triggered Specific Review

### AR-S04｜Code / Parametric Review
State: `PARTIAL PASS FOR AUTHORED RUNTIME / LIVE-NAVIGATION OPEN`.

- query-addressable off states exist for full FX, tonal, wash and edge layers;
- desktop/mobile readback reports 0 horizontal overflow, 0 broken images and 0 recorded console/page errors;
- operation deltas are bounded to the source photo rectangle;
- no runtime claim is made for a deployed/public URL or unrestricted `file://` navigation.

### AR-S06｜Visual Review
State: `INDEPENDENT PROFESSIONAL DESIGN REVIEW PENDING / NO SELF-KEEP`.

Actual target-size pixels, grayscale and effect-off baselines are available. Open independent questions include first-read balance between the large proposition and landscape, the material value of the treatment versus styling-only effect, and the visible limit imposed by the `1080×608` source at desktop display scale.

### AR-S09｜Release Package Review
State: `NOT A RELEASE CANDIDATE / NO PACKAGE RELEASE PASS`.

The current producer ZIP has durable Drive persistence and independent retrieval/hash/open verification. That PAP evidence proves recoverability only; promotion/release remains blocked by the independent Professional Design Gate and project-level Web integration gates.

## Current artifact-review conclusion
`ARTIFACT REVIEW = PARTIAL / TECHNICAL + PERSISTENCE EVIDENCE RECORDED / PROFESSIONAL DESIGN GATE OPEN / NO_RELEASE_PASS / NO_PROMOTION`.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`
