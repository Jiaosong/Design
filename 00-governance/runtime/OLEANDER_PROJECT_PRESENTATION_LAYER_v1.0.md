# OLEANDER Project Presentation Layer v1.0

Status: **DRAFT GOVERNANCE EXTENSION**. Extends the current Project Runtime Classification Framework, `oleander-story-and-board`, `oleander-visual-design`, Current Visual Communication knowledge, and Artifact Review. It is **not** a second project taxonomy, not a replacement for visual-design knowledge, and not a new source-of-truth layer for project facts.

## 1. Core boundary

`PROJECT TRUTH / DESIGN AUTHORITY → PRESENTATION PROJECTION → AUDIENCE / MEDIUM / CONTEXT → READBACK`.

Presentation may select, sequence, crop, annotate, compare, layer, simplify, summarize and translate approved project truth for a specific communication condition. It may not silently alter the underlying requirement, geometry, evidence, decision, baseline, measurement, claim ceiling or validation state.

Hard rules:

- `PRESENTATION KEEP ≠ PROJECT DESIGN KEEP`.
- `VISUAL IMPACT ≠ EVIDENCE STRENGTH`.
- `NEWER PRESENTATION ≠ NEWER PROJECT AUTHORITY`.
- `STYLE ≠ TRUTH`.
- `DECORATION ≠ PROOF`.
- `SYNTHETIC / SPECULATIVE VISUAL ≠ FIELD / TECHNICAL EVIDENCE`.
- `PRESENTATION DERIVATIVE ≠ SOURCE ARTIFACT` unless explicitly promoted by Project Authority.

## 2. Why ARTIFACT is insufficient

A project `ARTIFACT` answers what carrier exists: drawing, model, image, chart, file, report, prototype, video, etc.

The Presentation Layer answers a different question:

**How should one or more authoritative objects be projected to a particular audience, medium, context, reading time and decision?**

Therefore presentation semantics remain orthogonal to runtime `ARTIFACT` semantics.

## 3. Presentation runtime object classes

### PR1 — AUDIENCE_CONTRACT
Defines the real audience condition.

Minimum fields:
`audience_id, audience_type, baseline_knowledge, decision_right, information_need, expected_action, language, accessibility_needs, viewing_context, available_time, confidence, source`.

### PR2 — COMMUNICATION_OBJECTIVE
Defines what the presentation must accomplish.

Types:
`INFORM | EXPLAIN | COMPARE | REVIEW | DECIDE | PERSUADE | TEACH | NAVIGATE | DOCUMENT | EXHIBIT | HANDOFF | ARCHIVE`.

Minimum fields:
`objective_id, target_audience, primary_question, intended_outcome, required_claims, forbidden_overclaim, success_condition`.

### PR3 — ARGUMENT_UNIT
An audience-facing claim, question, decision or explanatory proposition.

Minimum fields:
`argument_id, audience_question, primary_claim_or_decision, project_source_object, proof_refs, caveat_refs, priority, sequence_role, claim_ceiling`.

Argument Unit is not a new project Claim Authority. It projects an upstream Claim / Decision / Requirement / Evidence relation.

### PR4 — EVIDENCE_PROJECTION
Defines how source evidence is shown without changing its epistemic meaning.

Minimum fields:
`projection_id, source_evidence_or_artifact, projection_method, crop_or_filter, annotations, omission_boundary, scale_or_view, does_not_establish, source_label, derivative_state`.

### PR5 — PRESENTATION_SEQUENCE
Defines ordering over time, page order, spatial route or interaction route.

Sequence types:
`LINEAR | BRANCHED | LOOPED | SPATIAL_ROUTE | SCROLL | STATE_DRIVEN | SELF_DIRECTED | HYBRID`.

### PR6 — VIEW_UNIT
Atomic audience-facing surface or state.

Examples:
`slide, page, spread, board-zone, exhibition panel, scene, keyframe, web section, dashboard view, map state, interactive state, physical display zone`.

Minimum fields:
`view_id, medium, role, primary_argument, primary_proof, supporting_content, style_profile, technique_refs, target_size_or_distance, interaction_state, source_refs, accessibility_state, readback_refs`.

### PR7 — STYLE_PROFILE
A controlled set of observable visual/temporal/material relations. A Style Profile is not merely an adjective.

Minimum fields:
`style_profile_id, governing_axes, project_reason, inherited_identity_refs, allowed_techniques, restricted_techniques, medium_scope, evidence_boundary, accessibility_constraints, production_constraints, readback_state`.

### PR8 — TECHNIQUE_SET
A selected bundle of explicit presentation operations used to solve a communication problem.

Technique Set references the controlled technique catalog. It should not copy technique definitions locally unless materially modified.

### PR9 — MOTIF / SIGNATURE_RELATION
A recurring recognizable relation that contributes to project identity or continuity.

Examples:
`edge anchor, repeated datum line, sectional cut motif, repeated crop behavior, recurring caption rail, recurring material band, route ribbon, paired before/after frame`.

Motif is a relation/system, not decorative repetition by itself.

### PR10 — CHANNEL_VARIANT
A bounded transformation of one presentation system for a different medium/context.

Examples:
`A1 board → deck → mobile case-study → exhibition wall → print book → social teaser`.

Must preserve upstream truth while allowing recomposition.

### PR11 — PRESENTATION_RELEASE
Controlled package of presentation derivatives approved for a stated audience/scope.

Minimum fields:
`release_id, audience_scope, medium_scope, included_views, source_baseline, style_profile, version, owner, review_refs, release_state, supersedes`.

## 4. Presentation object relation families

Use strong relations instead of generic `related_to`:

- `targets_audience`
- `serves_objective`
- `projects_claim`
- `projects_decision`
- `projects_requirement`
- `projects_evidence`
- `projects_artifact`
- `explains`
- `compares_with`
- `contrasts_with`
- `precedes / follows`
- `branches_to`
- `reveals`
- `annotates`
- `crops_from`
- `derives_from`
- `uses_style_profile`
- `uses_technique`
- `inherits_visual_authority_from`
- `adapts_for_channel`
- `released_in`
- `supersedes_presentation`

A presentation relation never replaces the upstream Project Runtime relation.

## 5. Presentation state axes

Do not use one generic status.

### Content binding state
`UNBOUND → SOURCE_BOUND → CLAIM_BOUND → EVIDENCE_BOUND → CURRENT_SOURCE_CONFIRMED`.

### Composition maturity
`WIREFRAME → STRUCTURED → ART_DIRECTED → POLISHED → READBACK_VERIFIED`.

### Presentation disposition
`OPEN | REVISE | HOLD | KEEP_FOR_SCOPE | REJECT | SUPERSEDED`.

### Release state
`WORKING → REVIEWABLE → APPROVED_FOR_AUDIENCE → RELEASED → SUPERSEDED | WITHDRAWN`.

### Truth fidelity state
`SOURCE_FAITHFUL | BOUNDED_DERIVATIVE | SYNTHETIC_DISCLOSED | MISLEADING_REJECT`.

These axes are independent. A visually polished presentation can still be `SOURCE_BOUND` but not `EVIDENCE_BOUND`; a source-faithful presentation can still be visually weak and remain `REVISE`.

## 6. Presentation operating formula

`PRESENTATION = Audience Contract × Communication Objective × Upstream Claim/Evidence × Sequence × View Role × Style Profile × Technique Set × Medium × Context × Accessibility × Production × Readback`.

The ordering matters: style and technique are downstream of communication purpose and truth binding.

## 7. Existing-first binding

Presentation work must reuse the current OLEANDER visual/story capability stack rather than create a separate visual-method tree.

Existing owners include:

- Current Notion `FW-DESIGN-VISUAL-COMM-001` for information/hierarchy/medium logic;
- `oleander-story-and-board` for narrative sequence, board/deck/publication/story composition;
- `PRESENTATION_ARGUMENT_EVIDENCE_EXTENSION.md` for live Claim–Proof sequence;
- `EDITORIAL_PUBLICATION_SYSTEM_EXTENSION.md` for long-form publication architecture;
- `VISUAL_LAYER_BINDING.md` for existing visual method reuse;
- `oleander-visual-design` for composition, typography, identity and professional finish;
- `TYPOGRAPHY_SYSTEM_EXTENSION.md` for type-system behavior;
- `DESIGN_LANGUAGE_RECONSTRUCTION_EXTENSION.md` when reconstructing an existing design language;
- Current image-art-direction, data-viz, motion, web/UI, technical drawing and delivery-QC owners when those are the actual carriers.

The Presentation Layer compiles their outputs into runtime selection logic; it does not duplicate them.

## 8. Style is not a label

OLEANDER defines style as:

`STYLE = REPEATED OBSERVABLE RELATIONS + MATERIAL/GRAPHIC BEHAVIOR + HIERARCHY + RHYTHM + IMAGE/TYPE TREATMENT + MEDIUM BEHAVIOR`.

Words such as `minimal`, `brutalist`, `Swiss`, `cinematic`, `luxury`, `editorial`, `technical`, `playful` or `futuristic` may be used as **reference tags only**. They are insufficient as a Style Profile and cannot by themselves authorize a font, grid, color, effect, motion or material choice.

Each Style Profile must resolve observable axes and a project-specific reason.

## 9. Technique selection

A technique is a bounded operation, not a style identity.

Use:

`COMMUNICATION PROBLEM → SOURCE/EVIDENCE CONSTRAINT → CANDIDATE TECHNIQUE → VISIBLE OPERATION → TARGET-CONDITION READBACK → KEEP / REVISE / REJECT`.

A technique that is fashionable but does not improve comprehension, evidence visibility, identity, comparison, navigation, memory or intended emotion should be removed.

## 10. Cross-media invariants

Across presentation channels, preserve where applicable:

- semantic identity of primary claims;
- evidence provenance and claim ceiling;
- project identity / visual authority;
- relative importance of primary vs support content;
- source labels / caveats;
- accessibility meaning;
- stable IDs for claim/evidence/view when traceability matters.

Allow change where required:

- sequence;
- crop;
- scale;
- density;
- typography size/measure;
- interaction;
- motion;
- page count;
- image-to-text ratio;
- amount of visible supporting evidence.

`CROSS-MEDIA CONSISTENCY ≠ PIXEL IDENTICAL`.

## 11. Presentation authority boundary

Presentation may create a new audience-facing derivative, but it cannot:

- change an authoritative dimension to improve fit;
- redraw geometry into a false relation;
- remove a limitation that changes the claim;
- turn predicted performance into measured performance;
- turn concept render into site evidence;
- turn visual prominence into evidence strength;
- hide a failed/OPEN state when the audience decision materially depends on it;
- convert a reference precedent into proof of project performance;
- imply code compliance, certification or field verification without upstream authority.

## 12. Promotion / release floor

A Presentation Release may reach `APPROVED_FOR_AUDIENCE` only when:

1. target audience and communication objective are explicit;
2. all material Argument Units resolve to current upstream project objects;
3. primary proof is source-bound and claim-compatible;
4. presentation-only transformations are declared where material;
5. style/techniques have a project reason rather than trend-only rationale;
6. accessibility and medium constraints applicable to the release are checked;
7. actual target-condition readback is complete;
8. no presentation device causes a truth-fidelity regression;
9. independent Artifact Review / Design Review requirements are satisfied when required.

## 13. Review dimensions

Separate at least:

- **Truth Fidelity** — does it preserve what is actually known?
- **Argument Clarity** — can the intended audience understand the primary point?
- **Evidence Visibility** — can the audience see the proof needed for the claim?
- **Hierarchy / First-read** — does visual order match decision priority?
- **Sequence / Rhythm** — is attention managed across time/pages/space?
- **Identity / Style Coherence** — does the project have recognizable authorship without generic template drift?
- **Technical Legibility** — are precise drawings/data/specs readable when they need to be?
- **Accessibility** — can intended users perceive and operate the presentation?
- **Production Integrity** — does the intended output survive real media/export/printing/runtime?
- **Professional Finish** — does actual readback meet the target discipline standard?

## 14. External calibration boundary

Calibrated without becoming OLEANDER Authority against:

- ISO 9241-112:2025 — presentation of information across visual/auditory/tactile modalities;
- WCAG 2.2 — digital perceivability, distinguishability and understandable presentation;
- contemporary platform guidance such as Apple HIG for hierarchy, motion purpose and adaptable context;
- current OLEANDER Visual Communication / Story & Board / Artifact Review knowledge.

No external platform style, component library or house aesthetic is adopted as an OLEANDER default.
