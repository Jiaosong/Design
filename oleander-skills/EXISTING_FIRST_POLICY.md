# OLEANDER Existing Skill / Existing Knowledge First

Status: **CURRENT POLICY CANDIDATE FOR MERGE**

Purpose: prevent OLEANDER from creating parallel Skills, Methods, Gates, Validators, runtimes or knowledge objects when mature reusable capability already exists internally or in the wider professional ecosystem.

## Default rule

When a capability, method or knowledge gap appears, OLEANDER must **search, evaluate and reuse existing resources before creating anything new**.

Required search order:

1. OLEANDER GitHub installed Skills, specialist owners, Candidate lineages, runtime contracts, REVIEW/AIG rules and existing project/practice implementations.
2. OLEANDER Notion Current/Canonical METHOD, Practice, Review Rule, Design Intelligence and professional knowledge objects.
3. Existing mature market Skills: agent skills, plugins, open-source workflows, professional toolchains, official SDKs/CLIs/samples and maintained community packages.
4. Existing mature knowledge bases: standards/specifications, official software/file-format documentation, university/professional-association resources, manufacturer technical libraries, handbooks, design systems, pattern libraries and public professional databases.
5. Only when the first four layers cannot satisfy the Required Native Output, project constraints or professional boundary may a new OLEANDER Candidate Skill/Method/Validator/Knowledge Object be created.

## Reuse threshold

If an existing resource covers roughly **60% or more** of the required capability, the default action is:

`REUSE → ADAPTER / WRAPPER → COMPOSITION → EXTENSION → PROJECT RE-APPLICATION → READBACK`

not parallel reimplementation.

A new Candidate requires explicit **Existing-First Evidence** showing why reuse, adaptation, composition or extension is insufficient.

## External resource evaluation

For every external Skill or knowledge source considered, record as applicable:

- source / author / organization;
- version and maintenance state;
- inputs / outputs;
- dependencies and runtime assumptions;
- license / rights boundary;
- evidence quality and source authority;
- applicable domains and professional scope;
- known failure modes, false positives / false negatives where relevant;
- compatibility or conflict with OLEANDER Current Authority;
- reusable portion;
- non-transferable portion;
- Transfer Boundary;
- Required Native Output coverage.

External resources do **not** automatically become OLEANDER Authority. They are inputs to be mapped through Source Authority, Evidence State, Design Quality and Validation boundaries.

## External-digestion extension routing

When an external professional Skill has already been evaluated and independently reformulated into an Existing-first OLEANDER extension, resolve the current routing index before creating another method or Skill:

`oleander-skills/EXTERNAL_EXTENSION_ROUTING_20260828.md`

The index maps task triggers to existing owners and Candidate extension files. It is a discovery aid only; it does not replace the owner map, resolver, individual `SKILL.md`, project Current Authority or more specific Current methods.

Rules:

- use the existing owner first, then the minimum relevant extension;
- read the associated training digestion record when license/transfer boundary matters;
- do not import the external source's CLI syntax, templates, prompt recipes, fixed heuristics, visual presets or runtime assumptions unless separately authorized and validated;
- documentation presence and CI success do not promote a Candidate extension to ACTIVE/installed authority;
- if the extension does not materially cover the current task, return to the normal Existing-first search rather than forcing it.

## Governance gate

A proposed new Skill, Method, Gate, Framework, Validator, runtime wrapper or Knowledge Object is `HOLD / REJECT` when any of the following is missing:

- OLEANDER internal search;
- market Skill/tool/workflow search;
- mature knowledge-base/standard/documentation search;
- capability mapping;
- explanation of why reuse/adaptation/composition/extension is insufficient;
- project re-application evidence for the claimed uncovered gap.

Do not maintain an inferior duplicate merely to keep an implementation "OLEANDER-owned". If a mature external resource is materially stronger, prefer:

`ABSORB KNOWLEDGE → ADAPT / COMPOSE → VALIDATE → PROJECT RE-APPLICATION → REVISE EXISTING OLEANDER SKILL`

## Relationship to the 11 Core Skill Registry

This policy does not change lifecycle or installation state.

- Core identity ≠ installed execution owner.
- Candidate / Composite / Draft ≠ ACTIVE / Installed / Independent KEEP.
- `oleander-web-ui` remains a composite route over existing specialist owners.
- `oleander-technical-drawing` continues its existing PR #172 Candidate lineage; no parallel implementation.
- New Candidate evidence cannot bypass existing AIG, review, validation or promotion gates.

## Scheduled-task enforcement

The five OLEANDER workstreams must enforce this policy:

- **KNOWLEDGE**: search mature knowledge bases before authoring new knowledge objects.
- **DESIGN**: search existing internal and market Skills/knowledge before creating a new design method or Candidate Skill.
- **VALIDATION**: prefer mature official validators, standards and toolchains before writing new validation logic.
- **PRESENTATION**: reuse mature visual, image, motion and UI methods/patterns before inventing new presentation frameworks.
- **GOVERNANCE**: reject Candidate creation without Existing-First Evidence and detect duplicate-wheel maintenance.

The objective is not to maximize OLEANDER-owned methods. The objective is to build the smallest, strongest, most verifiable professional capability stack by reusing mature knowledge and tools wherever they already exist.