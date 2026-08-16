# OLEANDER Control Plane Entrypoint

For executable project-control checks, use:

```bash
python 00-governance/control-plane/control_plane.py check <project-control-card.json>
```

For repository-wide Current Control Card discovery and validation, use:

```bash
python 00-governance/control-plane/scan_control_cards.py
```

This entrypoint is subordinate to current governance and compiles existing rules into execution. It does not redefine Knowledge Architecture, Application Mapping, Project Axis, Case Axis, delivery priority, evidence levels, Artifact Review, Post-Generation Review, PAP, Rights, Reality, Engineering, Human Test or project-specific contracts.

It also compiles the global default `NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS` policy into the existing Control Card.

Current stored Control Cards use schema v0.3. v0.2 remains supported for immutable replay/backward compatibility in explicit provenance/replay zones; repository-wide Current-card scanning rejects v0.2 outside those zones.

For v0.3, no-loss is not inferred only from `problem_layer=Architecture`. Every Current card declares `change_scope.kind = NON_RESTRUCTURE | RESTRUCTURE` plus affected surfaces. Any declared RESTRUCTURE — including Narrative, Presentation, Web, Board, PDF, Slides, Film/Motion, App/Digital, Integration or Final Edit work — requires a `preservation_review`.

A RESTRUCTURE must either:

- provide a source-bound `established_object_baseline`; or
- explicitly declare a genuine greenfield condition with no established objects.

`preservation_review.decisions` must cover the established baseline exactly. Missing, duplicate, or outside-baseline decisions fail closed. Structural `SPLIT / GROUP / MERGE / REMAP` decisions must expose target object IDs; non-CUT actions must preserve object identity/retrievability. `CUT` requires `concept_state=DROP` and cannot be used to delete a kept concept because current pixels are weak.

Material reduction actions use structured substantive reason codes. Compression, page count, cleaner presentation, shorter Web/film, less text or minimalism are not valid reason codes and cannot independently authorize DEMOTE/CUT/MERGE.

The schema continues to forbid any fixed global chapter count. C04's 12-layer architecture remains C04-specific; other projects keep their own justified architectures.

A PASS means only that the supplied card satisfies the applicable schema, namespace and gate-profile checks, CB-01 did not block continuation, and any declared restructure satisfied the machine no-loss contract. It is not a design-quality, MAIN, evidence, physical, rights, engineering, human-test, promotion or release approval.
