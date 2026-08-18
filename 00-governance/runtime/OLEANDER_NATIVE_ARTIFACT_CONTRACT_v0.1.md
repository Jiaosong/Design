# OLEANDER Native Artifact Contract v0.1

Status: **CANDIDATE_FOR_CURRENT**  
Decision date: **2026-08-18**  
Scope: **all cross-Skill native artifact handoffs**

## 0｜Purpose

Standardize what an execution owner hands to another owner. A handoff must be a typed native artifact record, not merely “a picture”, “a PDF” or a chat description.

Required fields:

`artifact_id / artifact_role / authority_source / authority_state / producer_owner / native_format / derived_formats / editable_state / semantic_layers / provenance_state / dependencies / hashes / runtime / renderer / permissions / current_or_superseded / created_at / last_verified / does_not_prove`.

## 1｜Artifact role

Valid roles:

- `NATIVE_SOURCE` — editable/native authoritative production source within its declared authority.
- `DERIVED_ASSET` — generated from a native/source object; cannot silently replace it.
- `DIAGNOSTIC_ASSET` — comparison, overlay, diff, QA or test artifact.
- `PREVIEW_RENDER` — visual/readback carrier; not source authority.
- `DELIVERY_DERIVATIVE` — downstream export/package format.
- `REFERENCE_DERIVED_GEOMETRY` — geometry reconstructed from a reference rather than measured/native geometry.

## 2｜Editable state

Declare one:

`FULLY_EDITABLE / PARTIALLY_EDITABLE / LINKED_EXTERNAL_SOURCE / FLATTENED_DERIVATIVE / RUNTIME_ONLY`.

If the task requires an editable master, `FLATTENED_DERIVATIVE` cannot satisfy the native-output contract by itself.

## 3｜Shared provenance vocabulary

Use the following vocabulary across Research, DataViz, Technical Drawing, 3D reconstruction and reference-bound work:

- `SOURCE_VISIBLE` — directly visible in the accepted source.
- `SOURCE_EXPLICIT` — directly stated/encoded in the accepted source.
- `REFERENCE_DERIVED_GEOMETRY` — geometry reconstructed from visual/reference evidence; not field-measured/native geometry.
- `INFERRED_FROM_MARK` — inferred from a visible mark/relationship; inference must be identified.
- `VISUAL_PROXY` — representation used to communicate a role/relationship without claiming source identity.
- `ASSUMED_FOR_PROTOTYPE` — bounded assumption used to keep a prototype executable.
- `UNREADABLE` — source exists but detail cannot be resolved honestly.
- `UNKNOWN` — state/value cannot be established from current evidence.
- `FIELD_OPEN` — requires field observation/measurement/verification.

Do not create local synonyms such as `estimated / inferred / proxy / assumed` without mapping them to this vocabulary.

## 4｜Semantic layers

`semantic_layers` identifies meaningful editable strata, not software layer count. Examples:
- chart: source values / encoding / labels / uncertainty / annotation;
- technical drawing: geometry / cut / edge / joint / dimensions / notes;
- 3D: geometry / material / light / camera / annotation;
- UI: content / state / interaction / visual treatment;
- image composite: source / mask / adjustment / material / atmosphere / text / FX.

## 5｜Dependencies and hash

Record required external sources, fonts, linked objects, runtime/library versions and source hashes where applicable.

A hash proves byte identity only. It does not prove authority, visual correctness, semantic correctness or design quality.

## 6｜Handoff permissions

Each handoff declares:

`READ_ONLY / DERIVE / MUTATE_PRESENTATION_ONLY / MUTATE_AUTHORIZED_SOURCE`.

Default is `READ_ONLY`.

A downstream owner must emit a new artifact ID when creating a derivative; it must not reuse the upstream artifact ID for materially changed content.

## 7｜Current / superseded

Each artifact record has one state:

`CURRENT / SUPERSEDED / HISTORY / HOLD`.

Only one CURRENT artifact may exist for the same declared artifact identity/revision line unless Current Authority explicitly defines parallel variants.

## 8｜Does not prove

A conforming artifact manifest does not prove the design is good, the source is true, field/engineering status is valid, rights are cleared, or the artifact should be promoted.
