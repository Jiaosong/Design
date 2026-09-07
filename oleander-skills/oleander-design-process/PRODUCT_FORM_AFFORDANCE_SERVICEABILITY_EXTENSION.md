# OLEANDER Product Form Affordance + Serviceability Extension

Status: `CANDIDATE EXTENSION / DESIGN-PROCESS`

Use when a physical product's form must communicate how it is held/operated, avoid deceptive pseudo-function, and support maintenance, repair or part replacement without letting render styling substitute for use logic.

This complements `PHYSICAL_PRODUCT_PHASE_GATES_EXTENSION.md`. It is a bounded form/use review, not a second industrial-design Skill.

## Core principle

`FUNCTION / USE TASK → FORM ROLE → AFFORDANCE CUE → BODY / CONTACT TEST → CONSTRUCTION TRUTH → SERVICE / REPAIR PATH → FORM REPAIR → VALIDATION HANDOFF`.

A visible feature should have a documented role in function, interaction, structure, protection, service, communication, identity or another Current brief requirement. Decorative expression is allowed when the brief actually assigns it a role; decoration must not impersonate ventilation, fastening, grip, control, structure or another functional cue it does not possess.

## Form-role ledger

For each material feature or surface, record as applicable:

- object/feature ID;
- intended role;
- who/what interacts with it;
- expected action or perception;
- supporting source/brief/geometry authority;
- whether the cue is functional, structural, ergonomic, protective, service-related, identity/semantic, or presentation-only;
- failure if removed, misunderstood or falsely interpreted;
- validation owner where physical performance is claimed.

Do not demand that every visual detail be mechanically functional. Do demand that every material detail has an accountable design role and does not falsely claim another one.

## Affordance gate

For material controls, handles, openings, grips, latches, insertion paths, removable parts and contact zones:

1. State the intended action before styling the cue.
2. Identify which geometry, contrast, texture, placement, resistance, labeling or contextual relation teaches the action.
3. Test novice interpretation where the interaction is not already conventional or self-evident.
4. Check alternate hand/body conditions relevant to the real use case.
5. Keep required labels/instructions when safety, regulation, complexity or learned convention requires them; do not treat the existence of instructions as automatic form failure.
6. If users repeatedly infer the wrong action, repair the cue or interaction relation rather than adding more decorative emphasis.

`VISIBLE CUE ≠ VERIFIED AFFORDANCE`.

## Body/contact reality check

When a body part materially governs geometry, inspect the actual contact/use relation rather than a presentation pose.

As applicable, test:

- grip/reach/contact path;
- handedness;
- wet/dirty/gloved or otherwise altered conditions when the use environment makes them relevant;
- force direction and posture;
- repeated-use burden;
- access/visibility while operating;
- interference with payload, clothing, neighboring parts or service operations.

Use current anthropometric, ergonomic or project evidence. Do not import fixed percentile ranges, grip dimensions, force limits or weight thresholds from an external Skill as universal values.

## Construction-truth gate

Reject form cues that materially imply a function/construction that is absent unless the project explicitly identifies them as symbolic/decorative and the interpretation risk is acceptable.

Examples requiring review include:

- decorative openings that read as vents;
- fake fasteners or seams that imply disassembly;
- grip textures where the hand never contacts;
- visual hinges/latches that do not correspond to motion;
- structural-looking ribs/fins with no structural/thermal/interaction role;
- service seams that cannot actually open.

The issue is semantic deception, not minimalism as a universal aesthetic.

## Serviceability / lifecycle gate

Activate when the product contains wear parts, consumables, batteries, filters, blades, seals, electronics, fasteners, serviceable mechanisms or other components whose access affects useful life.

Record:

- service/maintenance task;
- access path and tools;
- disassembly order;
- replaceable/non-replaceable parts and why;
- irreversible joints or destructive access;
- reassembly/alignment requirements;
- consumable/wear-part identity;
- cleaning/drain/drying needs when relevant;
- what lifecycle claim is proven versus only intended.

A design may legitimately use non-serviceable construction when safety, hygiene, cost, sealing, certification or another higher-priority constraint requires it. Record the trade-off rather than treating repairability as an absolute rule.

## Subtraction / addition test

For suspicious styling features, run a bounded deletion test:

`REMOVE FEATURE → FUNCTION / AFFORDANCE / STRUCTURE / SERVICE / IDENTITY CONSEQUENCE?`

- If nothing material changes and the brief gives the feature no intentional expressive role, removal is a strong candidate.
- If deletion damages a real use cue, structural relation, service path or authorized identity role, keep or refine it.
- Do not use subtraction as a stylistic ideology. Use it to expose unaccountable features.

## Cross-owner routing

- payload/cavity/mechanism sequencing → `PHYSICAL_PRODUCT_PHASE_GATES_EXTENSION.md`;
- fit/clearance/datum geometry → `oleander-3d-pipeline/PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md`;
- CMF/tactile/material performance → current CMF knowledge/owner;
- engineering, DFM/DfAM, tolerance, safety and certification → relevant validation owner/current source;
- final visual communication → `oleander-visual-design`.

## Required output

Return:

- function/use-task authority;
- form-role ledger;
- affordance map and observed/expected interpretation;
- body/contact conditions actually checked;
- construction-truth findings;
- service/disassembly/maintenance path when applicable;
- deletion/addition test;
- geometry/form repairs triggered by the review;
- technical/lifecycle claims still on HOLD.

## Project usage evidence｜C04｜2026-09-07

This Candidate extension now has bounded real-project use in the C04 physical line. The evidence advances project usage only; it does not establish cross-project maturity or final Design KEEP.

### P01｜scene-fit + footfall relation

A real editable project carrier was repaired because local object logic alone did not sufficiently preserve the relation between the intervention, body movement, circulation and scene role.

Observed consequence:
- `OBJECT / FEATURE` review was insufficient by itself;
- body/contact and use interpretation must be checked together with the route/scene relation when placement changes how the object is encountered;
- cosmetic/detail refinement should not precede a material scene/use repair when the latter changes whether the object belongs in the use path.

Bounded extension consequence:

When the physical object's affordance is materially dependent on where/how it is encountered, extend the body/contact check to:

`OBJECT / FEATURE → BODY / CONTACT → PATH / APPROACH → EXISTING SCENE RELATION`.

This does not mean every product needs a route analysis; trigger it only when scene/path materially changes use or interpretation.

### P02｜lean-rest body relation

A real editable railing intervention was repaired around a `LEAN / REST` use identity rather than a generic seat/decorative interpretation. The project carrier keeps body-contact surface, reversible clamp intent, isolation/buffer layer, drainage/cleaning path and independent replacement/service intent, while retaining `CONCEPT / NTS / FIELD OPEN / NOT FOR CONSTRUCTION` and no assumption that the existing railing is verified for added load.

Observed consequence:
- posture/use identity should be explicit before local form polish when body contact materially governs the object;
- `LEAN / PERCH / SIT / SUPPORT` are not interchangeable affordance labels;
- human figures should expose contact/use relation rather than operate as decorative scale figures;
- an existing substrate/base can support a design relation without becoming verified load/field authority;
- reversible/serviceable attachment intent remains separate from engineering approval.

Bounded extension consequence:

For body-contact interventions, add an explicit `USE-POSTURE IDENTITY` to the form-role ledger when posture changes contact, force direction, path obstruction or service relation.

### Maturity consequence

Current maturity for these additions:

`PROJECT_USAGE_EVIDENCE / ONE PROJECT FAMILY / REAL EDITABLE REPAIR / CROSS-CONTEXT TEST NEEDED / NO PROMOTION`.

Do not generalize C04 geometry, dimensions, clamp details or site conditions into this Skill. Future materially different product/spatial contexts must confirm or falsify the scene/path and use-posture additions before stronger promotion.

## Candidate boundary

This extension strengthens form/use honesty and serviceability reasoning. It does not import a universal minimalist aesthetic, ergonomic numbers, Rams-derived style rules, manufacturing feasibility or lifespan claims.

External study provenance: `getburo/buro-free` `industrial-designer`. The reviewed repository is `All Rights Reserved`; no source prose, templates, examples or house-style logic is copied. Only independently synthesized general design questions are retained.