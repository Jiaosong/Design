# OLEANDER TP8 Cross-Software Artifact / Handoff Replay — 2026-09-15

Status: **DRAFT MULTI-CASE REPLAY / EXTERNAL-BENCHMARKED / NOT CURRENT**.

Purpose: test whether OLEANDER can accept useful exchange/derivative artifacts without confusing `file opens` with `semantic handoff valid`, and without forcing every lossy conversion into HOLD.

Real OLEANDER cases:

1. FreeCAD native `.FCStd` → STEP roundtrip / Blender display derivative.
2. Jade controller reference reconstruction → GLB exchange / fallback rebuild / native Blender gap.
3. Timer v3.3 audited package → GitHub deploy-source incompleteness / browser gate blocked while canonical Library package remains valid.

External professional benchmarks used as comparison, not project authority:

- NIST / ISO 10303 STEP product-data exchange literature;
- NIST work on standardized parametric CAD exchange and design-intent preservation;
- buildingSMART IFC 4 / IFC 4.3 Model View Definition and Reference View documentation;
- Khronos glTF 2.0 official registry/site.

The replay does not promote any exchange artifact to Source Master or editable authority.

---

# 1. Native master and exchange derivative answer different questions

Real FreeCAD Practice evidence establishes that native `.FCStd` save/reopen can check native semantics including:

- parameter values;
- expression dependency;
- Body Tip;
- solid validity;
- project-specific invariants.

The STEP benchmark can preserve result geometry for the bounded benchmark but does **not** preserve FreeCAD named-parameter / PartDesign dependency graph.

Therefore:

```text
STEP RESULT-GEOMETRY PASS
≠
NATIVE AUTHORING-INTENT PASS
```

A STEP derivative can be valid for a geometry-consumption role while invalid as an editable/parametric/source master.

## External consistency

NIST’s STEP literature distinguishes broad product-data exchange from pure geometry exchange and separately documents the difficulty of preserving CAD parameters, constraints, features, construction history and other design-intent semantics. NIST’s parametric STEP work exists precisely because ordinary shape exchange does not automatically carry those semantics.

## Replay result

`CONFIRMED / EXTERNALLY CONSISTENT`.

### Replay-derived rule

`P8/LOSS-RP02 HANDOFF_LOSS_ACCEPTABILITY_IS_CARRIER_ROLE_SPECIFIC; A_LOSS_CAN_BE_ACCEPTABLE_FOR_A_DERIVATIVE_ROLE_AND_AUTHORITY_BREAKING_FOR_A_SOURCE_OR_EDITABLE_MASTER_ROLE`.

---

# 2. Preserved/lost dimensions must be explicit

The existing P8 loss flags are sufficient as loss categories, but replay shows the handoff receipt also needs a positive statement of what was preserved.

Minimum role-aware matrix:

```yaml
handoff_role:
source_master_ref:
exchange_derivative_ref:
preserved_dimensions: []
lost_dimensions: []
unknown_dimensions: []
permitted_loss: []
consumer_readback: []
roundtrip_invariants: []
authority_after_handoff:
acceptance_by_role: {}
```

Example for FreeCAD → STEP:

```yaml
preserved_dimensions:
  - RESULT_GEOMETRY_BOUNDED_BENCHMARK
lost_dimensions:
  - PARAMETRIC_DEPENDENCY_GRAPH
  - NAMED_PARAMETER_AUTHORING_SEMANTICS
unknown_dimensions:
  - APPLICATION_SPECIFIC_FEATURE_SEMANTICS_NOT_TESTED
authority_after_handoff:
  geometry_source: FREECAD_OCCT_BREP
  step: DERIVATIVE_EXCHANGE
  blender: DISPLAY_DERIVATIVE_ONLY
```

### Replay-derived rule

`P8/HAND-RP02 HANDOFF_ACCEPTANCE_REQUIRES_DECLARED_PRESERVED_LOST_AND_UNKNOWN_SEMANTIC_DIMENSIONS_RELATIVE_TO_THE_INTENDED_CONSUMER_ROLE`.

---

# 3. Exchange requirement must be defined before judging interchange quality

buildingSMART IFC explicitly structures interoperability through Model View Definitions / exchange requirements: a subset of information is selected to support a recognized workflow or purpose. IFC Reference View is mainly one-directional and is not intended as a full exchange of design intent.

This external benchmark validates a general OLEANDER principle:

```text
GOOD HANDOFF
≠ MAXIMUM POSSIBLE DATA TRANSFER
GOOD HANDOFF
= REQUIRED INFORMATION FOR DECLARED PURPOSE TRANSFERRED + VERIFIED
```

### Replay-derived rule

`P8/HAND-RP03 EVERY_MATERIAL_CROSS_SOFTWARE_HANDOFF_REQUIRES_AN_EXCHANGE_REQUIREMENT_OR_EQUIVALENT_PURPOSE_SCOPED_INFORMATION_CONTRACT_BEFORE_PASS_FAIL_IS_MEANINGFUL`.

Recommended fields:

```yaml
exchange_requirement_id:
purpose:
producer_role:
consumer_role:
required_information_classes: []
optional_information_classes: []
forbidden_authority_promotions: []
required_consumer_readbacks: []
```

---

# 4. One-directional reference workflow is legitimate

Not all cross-software handoffs require round-trip editability.

buildingSMART Reference View explicitly supports reference-model workflows where modifications are requested back to the original author instead of editing the imported model and sending it back as if it were the source.

This is directly compatible with OLEANDER’s FreeCAD/OCCT → Blender rule:

```text
CAD authoritative mutation upstream
→ Blender display derivative downstream
→ downstream display does not acquire B-Rep authority
```

### Replay-derived rule

`P8/HAND-RP04 ONE_DIRECTIONAL_REFERENCE_HANDOFF_IS_VALID_WHEN_CHANGE_AUTHORITY_REMAINS_UPSTREAM_AND_THE_CONSUMER_ROLE_DOES_NOT_REQUIRE_ROUNDTRIP_AUTHORING_SEMANTICS`.

This prevents overengineering every visual/reference consumer into a bidirectional authoring workflow.

---

# 5. Derivative consumer may not seize source authority

The current runtime evidence already states:

- `FREECAD_OCCT_BREP` is geometry authority;
- Blender is `DISPLAY_DERIVATIVE_ONLY` for CAD-native results;
- unstable topology ordinals such as `FaceN` are not durable semantic authority.

The handoff therefore needs an authority statement independent of file technical capability.

### Replay-derived rule

`P8/AUTH-RP02 IMPORT_EDIT_CAPABILITY_DOES_NOT_GRANT_SOURCE_CHANGE_AUTHORITY; AUTHORITY_AFTER_HANDOFF_MUST_BE_EXPLICITLY_DECLARED`.

Even if a consumer application technically allows editing imported geometry, the governance role can remain read-only/reference.

---

# 6. Jade controller — exchange reopen can PASS while native gap remains

The Jade controller review records:

- stable ID/version across source/docs/review;
- GLB/OBJ/MTL/source/textures/reviews/manifests present;
- native BLEND explicitly runtime-pending;
- GLB independently reopened;
- 23 components preserved;
- clean-copy fallback rebuild reproduced 23 components, 39,098 triangles and identical ~97.3 × 22.02 × 153.3 mm extents;
- GLB byte serialization hash is not treated as deterministic-geometry equivalence;
- professional design verdict remains REVISE / not KEEP.

This is an ideal mixed handoff result:

```text
EXCHANGE READBACK = PASS
COMPONENT/EXTENT INVARIANTS = PASS
NATIVE BLENDER REVIEW = OPEN
PROFESSIONAL DESIGN = REVISE
```

### Replay-derived rule

`P8/HAND-RP05 EXCHANGE_REOPEN_PASS_MAY_CLOSE_ONLY_THE_DECLARED_EXCHANGE_INVARIANTS; NATIVE_AUTHORING_GAP_AND_PROFESSIONAL_DESIGN_STATE_REMAIN_INDEPENDENT`.

---

# 7. Byte identity is not always the right round-trip criterion

The Jade review explicitly refuses to use GLB byte serialization hash as a deterministic-geometry criterion.

Timer separately proves that different hashes can carry equivalent protected geometry when an explicit equivalence test is run.

Therefore cross-software round-trip should use semantic invariants appropriate to the carrier/purpose, for example:

- stable object IDs where format supports them;
- component count where meaningful;
- units/axis;
- bounding boxes/extents;
- topology/solid validity where relevant;
- protected dimensions;
- material assignment identity if required;
- semantic properties / Psets if required;
- relation graph if required;
- render/interaction behavior where required.

### Replay-derived rule

`P8/RTRIP-RP01 ROUNDTRIP_ACCEPTANCE_MUST_USE_PURPOSE_APPROPRIATE_SEMANTIC_INVARIANTS; BYTE_HASH_EQUALITY_IS_REQUIRED_ONLY_WHEN_BYTE_IDENTITY_ITSELF_IS_THE_CONTROLLED_PROPERTY`.

---

# 8. glTF / GLB role boundary

Khronos describes glTF as a runtime 3D asset delivery format optimized for efficient transmission/loading of scenes and models. Its core can carry scenes/nodes, cameras, meshes, buffers, materials, textures, skins and animations.

That makes glTF highly appropriate for delivery/runtime/presentation consumers. It does **not** by itself establish preservation of a source application’s full parametric construction history, feature tree or engineering authoring intent.

### Replay-derived rule

`P8/ROLE-RP02 FORMAT_CAPABILITY_AND_CARRIER_ROLE_MUST_BE_DISTINGUISHED; RUNTIME_DELIVERY_FORMAT_SUCCESS_CANNOT_IMPLY_NATIVE_PARAMETRIC_AUTHORING_PRESERVATION_WITHOUT_EXPLICIT_EVIDENCE`.

This rule is format-neutral even though glTF makes the distinction especially clear.

---

# 9. Package transport failure is not source artifact invalidation

Timer’s integrated browser gate records:

- the audited complete v3.3 package exists in File Library;
- GitHub deploy source is incomplete;
- browser phase is therefore not run / blocked;
- the canonical GLB identity is known;
- the source-package transport/deployment problem does not overturn the locked four-gate photography calibration;
- engineering validation remains separately NOT RUN/PENDING.

This means a cross-surface/package handoff can fail while upstream source evidence remains valid for its existing scope.

### Replay-derived rule

`P8/HAND-RP06 DOWNSTREAM_PACKAGE_TRANSPORT_OR_DEPLOYMENT_INCOMPLETENESS_BLOCKS_THAT_HANDOFF_OR_RELEASE_SCOPE_BUT_DOES_NOT_AUTOMATICALLY_INVALIDATE_UNCHANGED_UPSTREAM_SOURCE_OR_PRIOR_SCOPED_ASSURANCE`.

This is P8’s artifact-level counterpart to P5 partial invalidation.

---

# 10. Handoff status should be per intended role

A single artifact may validly have:

```text
GEOMETRY_REFERENCE_CONSUMPTION = ACCEPT
PARAMETRIC_EDITING = REJECT / OUTSIDE_ROLE
PRESENTATION_RUNTIME = ACCEPT_WITH_LIMITATION
MANUFACTURING = OUTSIDE_CLAIM
ROUNDTRIP_EDITABILITY = NOT_EVALUATED
```

Therefore a global `HANDOFF PASS` is often too coarse.

### Replay-derived rule

`P8/HAND-RP07 CROSS_SOFTWARE_HANDOFF_DISPOSITION_MAY_REQUIRE_PER_ROLE_OR_PER_INFORMATION_CLASS_RESULTS_WHEN_THE_SAME_DERIVATIVE_HAS_DIFFERENT_VALIDITY_FOR_DIFFERENT_CONSUMERS`.

---

# 11. Unknown loss is a blocker only when material to declared purpose

`UNKNOWN_LOSS` already exists in P8. Replay clarifies how to use it.

If an unknown loss could affect a required exchange information class, the handoff must HOLD or remain unverified for that role.

If the unknown area is outside the declared consumer purpose/claim, it can remain outside claim without blocking a bounded handoff.

### Replay-derived rule

`P8/LOSS-RP03 UNKNOWN_LOSS_BLOCKS_HANDOFF_ONLY_WHEN_IT_INTERSECTS_REQUIRED_INFORMATION_OR_AUTHORITY_FOR_THE_DECLARED_ROLE; OTHERWISE_RECORD_OUTSIDE_CLAIM`.

---

# 12. Cross-software handoff normalized model

```yaml
handoff_id:
source_object_id:
source_master_ref:
source_authority:
producer_tool:
producer_tool_version:
exchange_format:
exchange_derivative_ref:
consumer_tool:
consumer_tool_version:
consumer_role:
exchange_requirement_id:
purpose:
required_information_classes: []
preserved_dimensions: []
lost_dimensions: []
unknown_dimensions: []
permitted_loss: []
consumer_readback:
  executed: true|false
  evidence_refs: []
roundtrip_invariants: []
per_role_results: {}
authority_after_handoff:
change_request_route:
claim_ceiling:
disposition:
```

---

# 13. False-positive patterns exposed

The typed system must reject:

1. `STEP opens` → therefore native parameters/design history preserved;
2. `IFC imports` → therefore full design intent transferable;
3. `GLB reopens` → therefore native Blender/CAD authoring semantics passed;
4. downstream editable capability → therefore downstream tool owns source authority;
5. one failed deployment copy → therefore canonical source becomes invalid;
6. different byte hash → therefore geometry necessarily changed;
7. same byte hash → therefore all semantic consumer behavior necessarily passed;
8. handoff PASS without declaring intended exchange purpose/information classes.

---

# 14. TP8 replay-derived rules

New rules:

- `P8/LOSS-RP02` loss acceptability is carrier-role specific;
- `P8/HAND-RP02` declare preserved/lost/unknown dimensions;
- `P8/HAND-RP03` material handoff requires purpose-scoped exchange requirement;
- `P8/HAND-RP04` one-directional reference handoff can be valid;
- `P8/AUTH-RP02` import/edit capability does not grant source authority;
- `P8/HAND-RP05` exchange reopen closes only declared exchange invariants;
- `P8/RTRIP-RP01` round-trip uses purpose-appropriate semantic invariants;
- `P8/ROLE-RP02` format capability ≠ native authoring preservation;
- `P8/HAND-RP06` downstream package incompleteness does not globally invalidate upstream source;
- `P8/HAND-RP07` handoff result may be per role/information class;
- `P8/LOSS-RP03` unknown loss blocks only when material to declared exchange purpose/authority.

---

# 15. TP8 disposition

```text
NATIVE MASTER VS EXCHANGE DERIVATIVE = CONFIRMED
PARAMETRIC/SEMANTIC LOSS WITH GEOMETRY PRESERVATION = CONFIRMED
ONE-DIRECTIONAL REFERENCE HANDOFF = EXTERNALLY CONFIRMED + OLEANDER CONSISTENT
GLB EXCHANGE REOPEN WITH NATIVE GAP = CONFIRMED
PURPOSE-SCOPED EXCHANGE REQUIREMENT = EXTERNALLY CONFIRMED
DERIVATIVE AUTHORITY NON-PROMOTION = CONFIRMED
ROLE-SCOPED LOSS ACCEPTABILITY = CONFIRMED
DOWNSTREAM PACKAGE FAILURE VS UPSTREAM VALIDITY = CONFIRMED
```

Overall:

`TP8 CROSS-SOFTWARE ARTIFACT / HANDOFF REPLAY = FIRST PASS COMPLETE WITH EXTERNAL BENCHMARK ALIGNMENT`.

No Current promotion is authorized.