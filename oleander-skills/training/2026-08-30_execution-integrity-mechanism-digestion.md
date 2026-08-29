# 2026-08-30｜Execution Integrity Mechanism Digestion

Status: EVIDENCE / EXISTING-FIRST DIGESTION / NO NEW CORE SKILL
Target owners: existing OLEANDER Control Plane + Work Coordination + `oleander-design-process`
Trigger: Existing-project repair rules were strong at the human-readable process layer, but artifact-delta, handoff integrity, stale derivatives, provenance and baseline rollback were not yet consistently fail-closed at machine-validation level.

## Existing-first decision

Do **not** install GitOps, OpenLineage, DVC, SLSA, NIST configuration-management tooling, or a new `oleander-execution-os` Skill.

Instead extract only mechanisms that close a demonstrated OLEANDER execution gap and bind them to existing owners.

Transfer rule:

`EXTERNAL MECHANISM → REMOVE EXTERNAL PRODUCT IDENTITY → MAP TO EXISTING OLEANDER OBJECT/OWNER → IMPLEMENT MINIMUM FIELD/GATE DELTA → REGRESSION ATTACK → REAL PROJECT USAGE → KEEP / REPAIR / REJECT`

## Source 1｜GitHub required status checks

Official source:
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks

Visible mechanism:
- a required check is a state-transition prerequisite;
- the relevant check must succeed for the latest commit state before merge;
- earlier success does not satisfy a later changed state.

OLEANDER transfer:
- `HANDOFF READY / ACCEPTED / CLOSED` becomes a guarded state transition;
- no material artifact delta + no real readback = no owner advancement;
- stale earlier readback cannot prove a later changed master.

Rejected transfer:
- branch protection is not equivalent to Design Quality;
- CI green cannot grant KEEP, Field PASS, technical approval or release truth.

## Source 2｜OpenLineage Run / Job / Dataset facets

Official source:
- https://openlineage.io/docs/spec/facets/

Visible mechanism:
- lineage centers on an activity/run plus explicit inputs and outputs;
- metadata facets describe job, run, inputs and outputs without turning every related object into an implicit edge.

OLEANDER transfer:
- record `RUN_ID / PRODUCER_OWNER / SKILL_REFS / INPUT ARTIFACTS / OUTPUT ARTIFACTS`;
- lineage edges are explicit only where the project claims a material dependency;
- project-wide co-presence does not imply every source produced every derivative.

Rejected transfer:
- no OpenLineage service, namespace or event taxonomy is installed;
- OLEANDER project/object IDs remain authoritative.

## Source 3｜DVC explicit deps / outs and affected-stage reproduction

Official source:
- https://dvc.org/blog/jupyter-notebook-to-dvc-pipeline/
- https://dvc.org/blog/april-22-community-gems/

Visible mechanism:
- stages declare dependencies and outputs explicitly;
- dependency changes identify affected downstream stages;
- without explicit dependency linkage, a system cannot safely infer what needs reproduction.

OLEANDER transfer:
- dependency edge stores `input artifact / current digest / consumed digest / output artifact / output status`;
- if Current input digest differs from the digest consumed by the derivative, the derivative may not remain `CURRENT`;
- valid states become `STALE / REGEN_REQUIRED / RETEST_REQUIRED / HOLD`.

Rejected transfer:
- no DVC runtime/cache/remote/lockfile dependency is introduced;
- only materially causal design/project edges are recorded.

## Source 4｜SLSA provenance

Official source:
- https://slsa.dev/spec/v1.1/provenance

Visible mechanism:
- provenance identifies output subjects and the inputs/dependencies resolved for the execution;
- external inputs and resolved dependencies remain explicit rather than implied by file existence.

OLEANDER transfer:
- material output must be listed in the same run provenance that identifies its inputs;
- source/baseline identities and output identities stay separate;
- `file exists / hash exists / PR exists` does not prove quality or authority.

Rejected transfer:
- no SLSA level claim is made;
- no software-supply-chain security certification is inferred from OLEANDER provenance fields.

## Source 5｜NIST baseline configuration + configuration change control

Official source:
- https://csrc.nist.gov/glossary/term/baseline_configuration
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/800-171r3/NIST.SP.800-171r3.html

Visible mechanism:
- a baseline is a reviewed reference state for subsequent changes;
- change control requires proposal/justification, implementation, monitoring/review and impact consideration;
- baseline changes create a new controlled state rather than erasing the prior reference.

OLEANDER transfer:
- repair declares `BEST EXISTING`, its reference, rollback reference and protected dimensions;
- change impact distinguishes DIRECT/INDIRECT affected artifacts and REVIEW/REGENERATE/RETEST duties;
- `CLOSED` is forbidden while required impacts remain OPEN/HOLD.

Rejected transfer:
- security/privacy controls are not generalized into design truth;
- OLEANDER retains specialist engineering, field, rights, human-test and release authorities.

## Synthesized OLEANDER delta

No new flow is created. The existing repair loop gains a machine-checkable integrity layer:

`BASELINE → RUN/INPUT/OUTPUT → MATERIAL DELTA → READBACK → HANDOFF → DEPENDENCY FRESHNESS → CHANGE IMPACT → CLOSE / RETURN / ROLLBACK`

Implemented in:
- `00-governance/control-plane/control-card.v0.3.schema.json` — optional repair execution-integrity fields; no schema-version bump;
- `00-governance/control-plane/validate_execution_integrity.py` — fail-closed semantic validation for declared repair-mode cards;
- `.github/workflows/ai-governance-evals.yml` — CI execution of the integrity gate;
- `00-governance/runtime/validate_governance_consolidation.py` — real Current Priority Queue validation, not synthetic examples only;
- `00-governance/templates/OLEANDER_PROJECT_CONTROL_CARD_v1.0.md` — human-facing mirror;
- `oleander-design-process/EXISTING_PROJECT_REPAIR_EXTENSION.md` — owner-local execution requirement.

## Maturity boundary

This is not yet a Golden reusable success claim.

Current state:
`MECHANISM DIGESTED → MACHINE CONTRACT IMPLEMENTED → CI/REGRESSION REQUIRED → REAL PROJECT USAGE REQUIRED`

Promotion requires actual project repair usage with:
- material artifact delta;
- readback;
- at least one dependency/change-impact case;
- owner handoff or return;
- downstream consequence;
- failure/repair/retest where available.

Until then:
`CI PASS ≠ PROJECT USAGE EVIDENCE ≠ DESIGN KEEP`.
