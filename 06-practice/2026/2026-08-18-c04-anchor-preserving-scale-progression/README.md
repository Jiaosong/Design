# 2026-08-18｜C04 Anchor-preserving Scale Progression

**Status:** `CANDIDATE / PRACTICE ONLY / PROJECT-MAIN VALIDATION PENDING`  
**Knowledge role:** `L7 PRACTICE / OUTPUT`  
**Project application:** `PRJ-C04-QINGJIANG-SHISHU`  
**Skill reuse:** `oleander-story-and-board` + `oleander-motion`  
**New Skill:** `NO`

## Decision question

When C04 film changes shot scale, can the viewer still track the same spatial/project relation, so scale progression carries the argument rather than becoming disconnected montage variety?

## Professional precedent

- Eames Office, *Powers of Ten and the Relative Size of Things in the Universe* (1977): https://www.eamesoffice.com/the-work/powers-of-ten/
- Library of Congress, Eames science exhibition / production art and storyboard: https://www.loc.gov/exhibits/eames/science.html

### Visible Fact

`Powers of Ten` changes scale continuously around a persistent point of reference; Library of Congress production materials include storyboard sketches, sequence charts and 42 production images used to construct the scale progression.

### Design Inference

Scale progression becomes narrative logic when the reference relation survives the scale change. The transfer is the relation, not the visual style of the Eames film.

### Transfer Rule

`CLAIM ORDER → STABLE OBJECT / RELATION → SHOT SCALE → SCALE TRANSITION → NEXT CLAIM → RETURN / RECOVERY`

## Real A/B practice

Same five claims and same information quantity in both variants:

`CONTEXT → ROUTE → R06 → DETAIL → RETURN`

- **A / REVISE:** scale, orientation and anchor all change. Each scene can look composed by itself, but the viewer must re-orient at every claim.
- **B / KEEP FOR PRACTICE:** shot scale changes while the R06 relation remains traceable. Scale now carries `context → relation → node → detail → recovery`.

No C04 route, platform, railing, terrain, source geometry or field fact is modified.

## Candidate record

- **Problem:** disconnected shot-size changes can turn C04 into a polished montage instead of one spatial argument.
- **Trigger:** current motion/story skills cover narrative continuity but needed a real scale-progression practice/readback.
- **Inputs:** Eames precedent; current C04 P2 authority; current presentation chain and evidence boundaries.
- **Visible Symptoms:** A loses the anchor; B preserves it through scale changes.
- **Cause:** treating camera/shot scale as visual variety rather than a relationship variable.
- **Technique:** lock the semantic/spatial anchor before changing scale; only introduce the next claim while the previous relation remains traceable.
- **Parameters / Conditions:** 15 s, 1920×1080, 24 fps; read points near 1.5 / 4.5 / 7.5 / 10.5 / 13.5 s; no-motion and Reduced Motion equivalents included.
- **Aesthetic Judgment:** at contact-sheet scale B should read as one argument; A should expose reorientation cost.
- **Verification:** FFmpeg full decode; 1920 contact first-read; 1920 keyframe near-read; 480 distance-read.
- **Failure Condition:** a scale change also changes orientation/anchor so completely that subtitles are needed to understand continuity.
- **Counterexample — looks PASS but should REVISE:** every frame is individually beautiful, grading is coherent and encoding is clean, but adjacent scenes share no spatial anchor and therefore become a generic cinematic montage.
- **Transfer Boundary:** film, scroll narratives, spatial/product/data explainers. Disorientation is allowed only when it is an explicit claim.
- **Applicable Domains:** Motion / Film Editing / Spatial Narrative / Product Explainer / Data Storytelling.
- **Application Mapping:** Spatial / C04.
- **Evidence Gate:** `PASS FOR TRAINING PRECEDENT + CURRENT PROJECT BOUNDARY`.
- **Design Quality Gate:** `POST-READBACK PASS FOR PRACTICE ONLY`.
- **Version:** `v0.1 / 2026-08-18`.
- **Status:** `CANDIDATE`; production C04 media binding and full-film readback are still required for `VALIDATED`.

## Design Crit

**A = REVISE.** Root cause: scale changes are not relationship-preserving, so every new scene resets orientation.

**B = KEEP FOR PRACTICE.** The same R06 anchor remains readable while the frame moves from context to route, node, detail and return. At 480 px the microcopy is intentionally no longer readable, but the A/B compositional behavior and five-stage progression remain distinguishable.

## Runtime / receipt

Adapter: `Python vector-like frame generator + FFmpeg 7.1.5`.

Capability: `FFmpeg / Pillow = NATIVE_AVAILABLE`.

| Artifact | SHA256 |
| --- | --- |
| A/B MP4 | `2e74526e98716032824dc7035a374ce88b70f352885501056b82f315ebadee34` |
| Reduced Motion MP4 | `cfe42c8c2160258676a086842ce8fee100e8e981297ec06e2236d06a678d0e6a` |
| Editable storyboard SVG | `c336df5a5aa8216f6038f7338f767831e5658650474b51a729f669da1979b3b0` |
| Contact 1920 | `caf07c1614705b7df646a2271a38df830761bbe76fc9677f20cc982d7c3d2356` |
| Contact 480 | `26f39133a96efdfb3abf661f5177e224f5ade00fc95348c803244f65550791ea` |

## Does not prove

- C04 final film Design PASS;
- real Qingjiang source pixels or site geometry;
- FIELD validation;
- user comprehension;
- final narrative lock;
- Candidate → Validated / Active Skill promotion.

## Notion binding

Canonical L7 Practice object: `PRAC-MOTION-SCALE-PROGRESSION-C04-20260818`.
