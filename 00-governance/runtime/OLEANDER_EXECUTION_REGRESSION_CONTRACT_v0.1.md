# OLEANDER Execution Regression Contract v0.1

Status: **CANDIDATE_FOR_CURRENT**  
Decision date: **2026-08-18**  
Scope: **execution implementations, recipes, fixtures and runtime outputs**

## 0｜Purpose

Upgrade regression from byte/deterministic checks to four independent layers:

`STRUCTURAL → SEMANTIC → VISUAL_ROI → RUNTIME`.

All four are separate from Professional Design Review. Passing them does not grant KEEP.

## 1｜Structural Regression

Checks the artifact’s required structure and editability.

Examples:
- expected semantic layers still exist;
- SVG paths/groups/IDs required by downstream logic still exist;
- route topology/node-edge relationships are unchanged unless explicitly revised;
- technical drawing dimension bindings still point to the intended geometry;
- layered image master is not accidentally flattened;
- 3D hierarchy, units, axes and linked resources remain intact.

## 2｜Semantic Regression

Checks that the meaning encoded in the artifact did not change accidentally.

Examples:
- source values and units remain identical where no data revision is authorized;
- `NORMAL / DEGRADED / CLOSED / UNKNOWN` do not collapse into another state;
- uncertainty/provenance labels remain attached to the correct objects;
- route connectivity does not imply a connection absent from source authority;
- reference-derived geometry remains labelled reference-derived rather than field/native.

## 3｜Visual ROI Regression

Checks bounded visual regions and first-read relationships, not only full-frame hashes.

Minimum checks as applicable:
- dominant/primary object retains first-read priority;
- small-size/target-size readability;
- label/dimension collision;
- texture/noise does not cover task-critical text, route, data, joint or dimension;
- grayscale/non-color behavior when color carries state;
- negative-space and crop integrity;
- paired/reveal views preserve same-source geometry when required;
- motion intermediate frames do not create unintended dual focus.

Visual ROI must record region IDs or semantic object IDs so a regression can be localized.

## 4｜Runtime Regression

Checks the actual target execution environment.

Examples:
- browser viewport/breakpoint behavior;
- motion interruption/re-entry/reduced-motion;
- renderer differences that materially alter geometry, lineweight, masks, gradients or text;
- GLB/3D exchange and material assignment;
- PDF/vector export integrity;
- video decode/frame/timing integrity.

A preview generated in a different renderer is not runtime evidence unless equivalence is explicitly established.

## 5｜Baseline record

Each regression baseline records:

`baseline_id / artifact_id / implementation_commit / canonical_tool_or_skill_revision / runtime / renderer / viewport_or_frame / structural_assertions / semantic_assertions / visual_roi_assertions / runtime_assertions / baseline_hashes / approved_by / last_verified`.

## 6｜Result states

Per layer:

`PASS / FAIL / HOLD / NOT_APPLICABLE`.

Overall regression cannot be PASS when a required layer is FAIL or HOLD.

## 7｜Design-review boundary

Regression answers “did the implementation preserve declared structure/meaning/visual constraints/runtime behavior?”

Professional Design Review answers “is this design good enough to KEEP?”

The first cannot substitute for the second.

## 8｜Does not prove

Four-layer regression does not prove field truth, engineering validity, user comprehension, accessibility conformance, rights clearance or final Design PASS unless those are separately tested by the appropriate authority.
