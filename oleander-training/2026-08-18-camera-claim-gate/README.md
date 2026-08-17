# OLEANDER Training — Camera Claim Gate

## Training question

How should OLEANDER choose a camera when the same authoritative geometry must serve an experiential Hero, a spatial-relation proof, and a technical comparison?

## Existing-first review

Reuses `oleander-3d-pipeline`. The existing Skill already required camera type/orientation/scale/crop to be locked, but did not define a design-quality gate for whether the chosen camera actually supports the intended claim.

Recent C04 reviews repeatedly separated clean model/render execution from Design PASS. This round therefore trains camera judgement rather than adding another modeling framework.

## External calibration

Primary-source reference: Blender Manual camera documentation.

Transferable facts used:
- perspective projection makes distant objects appear smaller and parallel lines converge;
- shorter focal lengths show a wider field of view, longer focal lengths a narrower field of view;
- orthographic projection keeps object size independent of distance and is useful for technical/proportion judgement;
- lens shift can adjust vanishing-point/framing behavior without rotating geometry.

These facts are calibration only. The practice does not claim a measured real lens match or a field-verified Qingjiang viewpoint.

## Real practice

Same synthetic 3D geometry in all candidates. Only camera/projection parameters change.

### A — 18 mm wide + close

`REJECT AS EXPERIENCE HERO`

The camera can fit more scene, but the foreground path dominates and the distant relation loses visual authority. Equal 1.7 m vertical bars at near/far depth project at about `2.61×` apparent-height ratio in the calibration.

### B — 35 mm moderate perspective

`KEEP FOR TRAINING / EXPERIENCE HERO`

The same scene retains human scale, route depth, and far context simultaneously. Equal-height near/far bars project at about `1.83×` ratio.

### C — orthographic

`KEEP FOR TRAINING / TECHNICAL RELATION`

Perspective size falloff is intentionally removed; the equal-height near/far ratio is `1.00×`. This makes relation comparison clear, but it is not experiential evidence.

## Design Crit

v1 = `REVISE` because the orthographic ridge was clipped, the camera contract rendered literal newline escapes, and the role claim was too implicit.

v2 = `KEEP FOR TRAINING` after:
- fitting all three views inside the review frame;
- making camera role and design claim explicit;
- separating `EXPERIENCE_HERO` from `TECHNICAL_RELATION`;
- retaining the same authoritative synthetic geometry across candidates;
- generating a 600 px distance-read derivative locally.

## Failure knowledge

- `camera locked != camera correct`;
- `fit everything != prove the intended relation`;
- focal length without camera position/distance is an incomplete camera contract;
- a visually dramatic wide-close view may exaggerate foreground/far relationships;
- an orthographic view may be excellent technical evidence and poor experiential evidence;
- camera/render quality does not establish field viewpoint, measured visibility, or site truth.

## Candidate rule

`CLAIM → PROJECTION → CAMERA DISTANCE / FOCAL LENGTH → FIRST-READ → ROLE VERDICT`

## Boundary

Synthetic relational geometry only. `NTS / FIELD OPEN / NO_PROMOTION`. No C04 geometry, site viewpoint, lens calibration, field visibility, safety, engineering, or overall Design PASS is asserted.
