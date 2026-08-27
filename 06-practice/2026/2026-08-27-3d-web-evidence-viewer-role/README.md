# 2026-08-27｜3D × Web / L5｜Interactive Technical Model Role Binding

Status: `EXECUTED / INTERNAL_ARTIFACT_FIRST_PROFESSIONAL_CRIT / RETEST ACCEPTED FOR CANDIDATE EVIDENCE / INDEPENDENT REVIEW OPEN / NO_PROMOTION`.

## Type classification

- Primary Domain: Digital / Interaction — Web portfolio presentation.
- Primary Type: embedded 3D evidence viewer.
- Supporting Type: 3D technical proof / model presentation.
- Stage: design development / current public-work producer support.
- Viewer task: understand spatial relation, body scale and assembly evidence without mistaking the model for the real landscape/site authority.
- Source Authority: Current project evidence first; model is derivative technical evidence unless Current Authority explicitly promotes it.
- Lead: DESIGN-led HYBRID.
- Skill target: `model role → viewer state → fallback/source boundary → hierarchy readback`.
- Type Brief: `PARTIAL`; K06 gap registered as `Embedded 3D Technical Viewer / Web Portfolio`.

## Existing Skill first

Current installed sources used first:
- `oleander-story-and-board` — strongest-current evidence, one primary claim/visual, presentation is not geometry authority.
- `oleander-3d-pipeline` — authoritative model identity, camera/render/exchange/scale discipline.

Existing candidate reused instead of creating a parallel gate:
- PR #205 `Mixed-media evidence-role gate` already covers the reusable failure where a clean model/render visually replaces source-grounded project evidence.

This round extends that exact candidate with Web-viewer-specific behavior. No new standalone Skill or Framework is created.

## Professional calibration

Official `<model-viewer>` documentation was used only for implementation mechanics, not visual style:
- a poster can remain visible until a model loads and can remain when a model source is invalid;
- camera controls/orbit/target are viewer behaviors, not proof-authority upgrades;
- panning can make re-centering difficult, so bounded proof views need reset/recenter logic if pan is exposed;
- hotspots/annotations can improve readable evidence annotation but screen-space overlay is not geometric truth.

## A/B + ONE BOLD MOVE

Editable source: `index.html`.

A / REJECT — `MODEL-AS-HERO`: technical status/source/truth/fallback disappear and the model becomes the first-read project object.

B / KEEP CANDIDATE — `EVIDENCE INSTRUMENT`: **ONE BOLD MOVE = replace “large model image” with a technical evidence instrument** carrying persistent `ROLE / TECHNICAL_PROOF`, same-object AXON/SIDE/SECTION states, MODEL OFF fallback, and an adjacent truth rail.

## Capability probe

- `/usr/bin/chromium`: available.
- Python Playwright: available.
- `file://` and localhost navigation: blocked by browser administrator policy in this runtime.
- Workaround: Playwright `page.set_content()` executed the same live HTML/CSS/JS in Chromium; no static-image substitution.
- AI image generation: not used.

## Actual readback → internal crit → root cause → fix → retest

### Failure 01 — mobile horizontal overflow
First mobile run: `viewport=390`, `scrollWidth=524`.

Root cause: unbounded intrinsic widths in HUD/state controls and long technical tokens. Hiding x-overflow would have masked rather than solved the carrier failure.

Fix: `min-width:0` on panel/instrument/rail/viewer; bounded HUD spans; mobile state controls recomposed to 2 columns; viewer width explicitly constrained.

Retest: `viewport=390`, `scrollWidth=390`.

### Failure 02 — view-state ghosting
SECTION readback initially retained a translucent AXON underlay.

Root cause: transition presentation preserved the previous view long enough to make two evidence states appear co-primary.

Fix: non-selected same-object view opacity → 0; state readback after 300 ms settling.

### Failure 03 — fallback looked unreadable
Initial MODEL OFF capture occurred before transition settling and the fallback was too weak.

Fix: strengthen fallback contrast/status hierarchy; explicit settle wait before screenshot.

Retest: fallback reads `MODEL FALLBACK POSTER / ROLE-SOURCE STATUS SURVIVES / GEOMETRY PROOF UNAVAILABLE`.

## Internal artifact-first professional crit

Producer context only; this is not an Independent Review.

- First read: REJECT intentionally lets the model become hero; KEEP reads a bounded technical instrument.
- Composition: KEEP preserves model viewport + role rail without becoming a dashboard.
- Proportion: model remains large enough for spatial reading; role/truth rail prevents authority ambiguity.
- Hierarchy: `project evidence > technical model role > view state > metadata`.
- Typography: target-size readback passes after mobile overflow repair.
- Spatial/material realism: proxy is explicitly synthetic/NTS; no site/model-source truth claimed.
- Scale: human proxy + relative span are relational only.
- Interaction: AXON/SIDE/SECTION/MODEL OFF are discoverable; settled states were read back.
- Professional finish: acceptable as training evidence; not C04 MAIN or production viewer.

Internal verdict: `RETEST ACCEPTED FOR CANDIDATE EVIDENCE`.
Independent KEEP: `NOT ISSUED`.

## Real project re-application — C04 current public Web

Current producer object = PR #353. Current Web source already places `04 / 3D` inside the AI+3D process and explicitly says AI does not own final geometry; current static gate remains asset-binding blocked.

Bounded support module: `C04_MODEL_TECHNICAL_PROOF_SUPPORT_v0_1.html`.

- exact current poster locator remains `assets/fluid_rest_object.png`;
- this run does not claim exact bytes are materialized;
- if the source cannot load, the module fails closed to `MODEL SOURCE PENDING` instead of inventing proxy geometry;
- public role = `空间关系 / 人体尺度 / 构件接口`;
- truth boundary = `研究级模型 / NTS / Field & Engineering Open`;
- support module does not alter the current 18-section runtime or replace the Qingjiang hero.

Actual support readback:
- desktop 1440: `scrollWidth=1440`, `SOURCE UNBOUND / FALLBACK ACTIVE / DO NOT SUBSTITUTE`;
- mobile 390: `scrollWidth=390`, same fail-closed state.

Status: `CANDIDATE / VALIDATION-SUPPORT / NOT PUBLIC RUNTIME OWNER`.

## Candidate Skill delta

PR #205 Mixed-media evidence-role gate now adds `Interactive 3D evidence-viewer binding` with declarations for `MODEL_ROLE`, project primary evidence, exact model source/version/hash when resolved, same-object view states, fallback state, truth boundary and does-not-prove.

Required attacks: `MODEL-OFF / HERO-TAKEOVER / VIEW-STATE SAME-OBJECT / LOAD-FAIL-FALLBACK / RESPONSIVE NATIVE VIEWPORT / SETTLING / SOURCE-ID / CONTEXT-OFF`.

Promotion test:
> Remove or fail the interactive model: the project claim and source authority must survive. Restore the model: it may deepen technical reading but must not silently become the project's stronger truth source.

## Transfer boundary

Applicable: C04 AI+3D/Technical Proof; architecture/landscape portfolio model viewers; product model/configurator evidence modules; museum object viewers; technical Web pages where models supplement drawings/source media.

Not sufficient: AR/GPS registration; field/survey verification; engineering approval; production CAD authority; accessibility certification; cases where Current Authority explicitly makes the model/product itself the primary design object.

## Gate state

- Evidence Gate: `PASS FOR TRAINING EXECUTION`.
- Design Quality Gate: `HOLD / INDEPENDENT REVIEW OPEN`.
- producer_id: `openai:gpt-5.6-sol:automation-producer`.
- reviewer_id: `null`.
- reviewer_independence_state: `NOT_RUN`.
- promotion_authority: `NONE`.
- OLEANDER_FLOW_CLOSED: `false`.

Local exact readback hashes are bound in `OLEANDER_EXECUTION_RECEIPT_v1.0.json`; PNGs remain local review evidence, not GitHub byte-persistence claims.