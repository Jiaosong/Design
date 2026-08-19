# CH13-01 v3｜OLEANDER Artifact Review｜Producer-side Compliance Evidence

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Object: `CH13-P01 / Physical Strategy`  
Status: `REVIEW PENDING / PRODUCER CANDIDATE / NO_PROMOTION`

## Skill / policy routing actually used
- `oleander-story-and-board` — one primary claim + one primary visual; Existing Mature Design first; presentation layer must not re-author source geometry; authority-preservation note required.
- `oleander-delivery-qc` — actual-open, dimensions, responsive runtime, image integrity, deterministic re-render, package/readback discipline.
- OLEANDER Existing Mature Design First Policy v1.0.
- OLEANDER Artifact Review System v1.1.
- OLEANDER Independent Design Verdict Policy v1.0.
- CH14 visual source grammar: `CONTEMPORARY EDITORIAL + LANDSCAPE SPACE / functional readability > brand decoration`.

## Existing-first / material delta
Previous CH13-01 candidates failed because they reused the project D Hero or cropped F01 so aggressively that product supports, ground relation and the body-use claim were weakened.

v3 delta:
1. D Hero removed completely.
2. Main image is a source-bound F01 crop with the full product top, both supports, ground contact and valley context retained.
3. `object-fit: cover` is prohibited; rendered main media uses contain / exact aspect preservation.
4. Same-source LEAN gesture is bound as secondary body evidence so `BODY BEFORE OBJECT` is not text-only.
5. CH13-P01 intervention gradient remains visible but subordinate to the physical scene; it is not a dashboard/card wall.

## Common Review AR-G01—AR-G10
- AR-G01 Identity & Naming: PASS — project / chapter / authoring unit / version explicit.
- AR-G02 Version & Status: PASS — `REVIEW PENDING / PRODUCER CANDIDATE`; no KEEP claim.
- AR-G03 Completeness: PASS for review candidate — HTML, desktop/mobile previews, crop register, control card, review request and hashes present.
- AR-G04 Internal Consistency: PASS — CH13-P01 claim, Level 0–3 gradient and source roles agree.
- AR-G05 Cross-file Consistency: PASS — ODB-02 remains upstream; F01 is descendant; no reverse-source claim.
- AR-G06 Evidence & Truth: PASS — FIELD 0/0, NOT LOCATED, NTS, NOT FOR CONSTRUCTION, concept-visual boundary visible.
- AR-G07 Open & Integrity: PASS — Chromium actual render; all embedded images decoded.
- AR-G08 Reproduction: PASS — desktop rerender was byte-identical (`684cee61...` both runs).
- AR-G09 Change Traceability: PASS — v1 Hero reuse and v2 crop/claim mismatch are superseded by v3 delta above.
- AR-G10 Final Artifact Review: PRODUCER READBACK COMPLETED; cannot be converted to independent Professional Design PASS by producer.

## Triggered Specific Review
### AR-S04 Code / Web carrier
- Chromium desktop 1920: `scrollWidth=1920`, overflow elements `0`, fonts loaded.
- Chromium mobile 390: `scrollWidth=390`, overflow elements `0`, fonts loaded.
- Embedded source images: natural sizes `1542×717` and `320×285`, both complete.
- HTML re-renders deterministically at desktop.

### AR-S06 Visual / CMF
Producer check only:
- Main visual is project-specific physical/body content, not generic method graphic.
- CH14 palette/type hierarchy used without turning the page into Brand-first decoration.
- Main crop keeps product silhouette/support/ground relation; no `cover` crop.
- LEAN body evidence is secondary and same-source.
- Intervention gradient is subordinate and continuous, not four equal cards.

This section is **not** an independent design verdict.

## Current gate state
- Control-card structural check: PASS.
- Machine/runtime/reflow: PASS.
- Source hierarchy: PASS.
- Primary crop geometry preservation: PASS at presentation-transform level.
- ODB-02 raw-byte materialization: HOLD.
- Independent Professional Design Review: **NOT RUN / REQUIRED**.
- Promotion: **BLOCKED** until independent reviewer provenance exists and returns an allowed KEEP-class verdict.
