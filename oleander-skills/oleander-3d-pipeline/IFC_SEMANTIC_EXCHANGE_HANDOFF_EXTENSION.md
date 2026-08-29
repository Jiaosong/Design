# IFC Semantic Exchange Handoff Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-3d-pipeline`

Use when an editable authoring/model source is exported, transformed, federated, checked or delivered through Industry Foundation Classes (IFC), and when geometry **and** semantic information must survive the exchange with explicit lineage.

This extension governs **native model → IFC exchange → downstream reopen semantic fidelity**. It does not make IFC the design master, does not create information requirements, and does not prove contractual BIM/openBIM compliance merely because a syntactically valid IFC exists.

## Existing-owner boundary

Use with:
- `oleander-3d-pipeline/SKILL.md` for native source identity, geometry, units/axes/origin, cross-tool exchange and actual reopen;
- `INFORMATION_REQUIREMENT_EXCHANGE_CONTRACT_EXTENSION.md` under `oleander-design-process` for requirement authority;
- `REALITY_CAPTURE_DERIVED_GEOMETRY_HANDOFF_EXTENSION.md` where field-derived geometry enters the authoring model;
- `oleander-delivery-qc/IDS_BCF_OPENBIM_VALIDATION_EXTENSION.md` for IDS/BCF/release validation;
- actual project BIM/information-management or discipline authority for formal mappings and acceptance.

## Core contract

`AUTHORITATIVE NATIVE MODEL + REQUIREMENT SET → EXCHANGE PURPOSE / MILESTONE → IFC SCHEMA VERSION + EXCHANGE VIEW / MVD OR PROFILE WHEN APPLICABLE → EXPORTER / MAPPING / FILTER CONFIG → IFC REVISION → STRUCTURAL / SEMANTIC INVENTORY → GEOMETRY CHECK + SEMANTIC CHECK → DOWNSTREAM TOOL / PARSER REOPEN → SOURCE↔IFC↔TARGET DIFF → KNOWN LOSSES / EXCEPTIONS → REQUIREMENT VALIDATION → DESIGN / COORDINATION / DELIVERY CLAIM CEILING`

`NATIVE MODEL ≠ IFC EXCHANGE MODEL ≠ DOWNSTREAM IMPORTED MODEL`.

Each can be useful and valid while carrying different authority and information.

## IFC identity contract

For each material exchange record:
- source model/object IDs and revision;
- exchange purpose and delivery milestone;
- IFC schema/version exactly enough to distinguish materially different semantics;
- exchange view/MVD/profile when the workflow declares one;
- exporter/tool/plugin and material version/configuration when it affects output;
- included/excluded discipline/model scope;
- unit, coordinate/reference, origin and georeferencing state;
- mapping rules or project export configuration;
- IFC file identity/hash when appropriate;
- downstream reader/validator version when result is tool-dependent.

Do not write only `IFC4` when the project decision depends on IFC4, IFC4.3, ADD2, a specific MVD or an implementation subset.

## Geometry and semantics are separate axes

At minimum distinguish:

### Geometry fidelity
- units and bounds;
- origin/axis/reference coordinates;
- placement hierarchy;
- shape/representation existence;
- critical dimensions/relations where required;
- clipping, tessellation, swept/BRep conversion or other material geometry change.

### Semantic fidelity
- entity class;
- `PredefinedType` or equivalent type semantics;
- type/occurrence identity;
- spatial containment/decomposition;
- system/group/assembly relations;
- material relations;
- classification references;
- property set/property identity, data type, value and unit;
- quantity set/quantity semantics;
- document/external references when required;
- stable identifiers/GUID lineage where the workflow depends on them.

`VISUAL GEOMETRY PASS ≠ SEMANTIC EXCHANGE PASS`.

`SEMANTIC INVENTORY PASS ≠ DESIGN QUALITY PASS`.

## Source-to-IFC mapping ledger

For every decision-critical mapping preserve:

`SOURCE OBJECT / PARAMETER / RELATION → SOURCE AUTHORITY → TARGET IFC ENTITY / ATTRIBUTE / PREDEFINEDTYPE / PSET / PROPERTY / QTO / RELATION → MAPPING METHOD → SCHEMA AVAILABILITY → EXPORT RESULT → DOWNSTREAM READBACK → REQUIREMENT ID → STATUS / EXCEPTION`.

When a source concept has no valid target in the selected schema/workflow, use `UNMAPPED / CUSTOM / DOCUMENTED EXCEPTION / HOLD` rather than forcing the nearest-looking class or property.

Do not infer semantic equivalence from similar labels.

## Entity and relationship integrity

IFC is relational. Validate not only object presence but the relations required by the exchange purpose.

Examples when material:
- object ↔ type;
- object ↔ spatial container;
- assembly/decomposition;
- ports/system/connectivity;
- material association;
- classification association;
- property/quantity assignment;
- document association;
- group/system membership.

A correct-looking object in a viewer can still be semantically detached or wrongly classified.

## Property / quantity semantics

Keep these distinct:
- native IFC attributes;
- property sets / properties;
- quantity sets / quantities;
- classification references;
- material/type/system relations;
- custom project extensions.

Rules:
1. Do not duplicate native IFC semantics into custom properties without a project requirement and reason.
2. Do not call a property a quantity because its label resembles `Qto`.
3. Data type and unit are part of the meaning when material.
4. Schema-specific Pset/Qto/class definitions must be checked against the actual schema/version.
5. Custom content must retain definition, ownership and requirement lineage.

## GUID / identifier boundary

A stable IFC `GlobalId` can support cross-revision issue/component tracing when the exporter/workflow preserves it, but GUID presence alone does not prove object continuity or semantic equivalence.

When identity matters, verify:
`SOURCE ID → IFC GLOBALID → NEXT REVISION GLOBALID / TARGET ID → OBJECT SEMANTIC CHECK`.

If identifiers are regenerated, record the break and use another controlled mapping strategy rather than pretending continuity.

## Coordinate / georeferencing boundary

Use the existing 3D and field-reference owners for unit/origin/CRS authority. IFC georeferencing is a carrier of that state, not a substitute for authoritative project coordinates.

Record applicable:
- project/site coordinate basis;
- unit state;
- local placement hierarchy;
- map conversion / projected CRS semantics when used;
- rebasing or exporter transforms;
- target-tool interpretation.

`IFC GEOREFERENCE EXISTS ≠ SURVEY AUTHORITY`.

## bSDD / semantic reference

bSDD or another controlled dictionary may supply stable definitions/identifiers for classes and properties.

Preserve:
`DICTIONARY OWNER + VERSION/STATUS + TERM IDENTIFIER/URI + DEFINITION + PROJECT REQUIREMENT / MAPPING`.

Do not confuse:
- a reusable dictionary definition;
- the IFC schema concept;
- a project-specific requirement;
- the value actually delivered.

`DICTIONARY LINK ≠ CORRECT VALUE`.

## Reopen and diff

A material IFC exchange needs actual readback appropriate to the claim.

Recommended layers:
1. file/schema parse succeeds;
2. source vs IFC inventory comparison;
3. geometry/readable coordinate comparison where required;
4. semantic mapping comparison;
5. downstream viewer/authoring/analysis reopen;
6. requirement/IDS validation when applicable;
7. exception/known-loss review.

Where practical, use deterministic counts/queries for key entity classes, mappings, Psets/properties/relations and known control objects. Visual viewer inspection alone is insufficient for semantic fidelity.

`IMPORT SUCCESS ≠ ROUND-TRIP FIDELITY`.

Do not claim full round-trip unless the workflow actually returns to the source-equivalent environment and the required geometry/semantic state is compared.

## Claim ceilings

Typical claim ceilings:
- IFC parses → syntax/schema readability only;
- model looks correct in viewer → bounded visual/geometry evidence only;
- entity/Pset inventory exists → bounded semantic presence evidence only;
- source↔IFC semantic diff passes for scoped requirements → scoped exchange fidelity evidence;
- IDS passes → only the requirements represented and covered by that IDS/runtime;
- target reopen + scoped diff passes → scoped interoperability evidence;
- none of the above alone proves design quality, engineering correctness, complete coordination, contractual BIM/ISO compliance or source-authoring health.

## Failure attacks

Reject or revise when:
- IFC existence is called openBIM delivery PASS;
- viewer geometry is correct but class/Pset/relations silently changed;
- source model and IFC are treated as the same authority object;
- schema/version/view is omitted although mappings differ by version;
- source categories/parameters are mapped to the nearest-looking IFC term without authority;
- `PredefinedType`, type/occurrence, spatial containment or system relation loss is ignored;
- property values survive but units/data types change materially;
- Qto/Pset semantics are inferred from naming alone;
- a bSDD URI is treated as project requirement satisfaction;
- GUID existence is treated as object continuity without revision check;
- exporter or target-tool interpretation hides coordinate/unit changes;
- syntax validation replaces semantic/readback validation;
- one exporter mapping table or Revit-specific recipe becomes universal OLEANDER truth.

## Source / transfer boundary

Professional sources studied:
- buildingSMART IFC 4.3 documentation — IFC is an open schema/exchange structure; implementation and exchange support are version/view-specific; retained schema/version/MVD and semantic/relationship fidelity principles.
- buildingSMART bSDD — retained dictionary/class/property reference semantics; bSDD is a service/reference layer, not project acceptance authority.
- buildingSMART IDS 1.0 — informs downstream requirement validation but does not replace source↔IFC mapping/readback.

External Skill studied:
- `jeffersonbim/Information-Manager-IFC-skill` — MIT. Retained schema-specific mapping, source-vs-IFC destination separation, deterministic exported-IFC verification and relation/property distinction. Revit categories, `IfcExportAs`, fixed scripts/runtimes, OpenClaw, Docker, Notion-RAG and local privacy architecture are source-specific and not imported as OLEANDER defaults.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / OFFICIAL-SOURCE + MIT-SKILL DIGESTED / PRACTICE NOT YET RUN / NO PROJECT USAGE / NO PROMOTION`.