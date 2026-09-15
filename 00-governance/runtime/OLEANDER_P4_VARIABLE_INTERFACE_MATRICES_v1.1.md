# OLEANDER P4 Controlled Variable / Interface Matrices v1.1

Status: **DRAFT COMPANION / PRIORITY P4 SECOND PASS**. Semantic owner remains `OLEANDER_CONTROLLED_VARIABLE_INTERFACE_DEPENDENCY_CONTRACT_v1.0.*`.

## 1. Purpose

P4 second pass prevents local discipline correctness from masking whole-system inconsistency.

Core invariant:

`SHARED VARIABLE CONSISTENCY + INTERFACE ACCEPTANCE + CHANGE PROPAGATION > LOCAL ARTIFACT PASS`.

---

## 2. Controlled Variable Classification Matrix

A Controlled Variable should be objectified when it is shared, authority-sensitive, acceptance-relevant, or change-propagating.

| Variable class | Examples | Minimum semantics |
|---|---|---|
| `GEOMETRIC` | grid, datum, clearance, radius, section depth | value/range, unit, tolerance, coordinate/reference system |
| `PERFORMANCE` | capacity, illuminance, acoustic target, thermal value | metric, condition, method, acceptance boundary |
| `STATE` | UI/service state names, operational mode | controlled enum/state model, transition owner |
| `CONTENT_SEMANTIC` | naming, terminology, asset ID | canonical term/ID, aliases, consumer systems |
| `VISUAL_IDENTITY` | color token, type role, logo exclusion zone | source authority, tolerance/variant rules |
| `DATA_SCHEMA` | field name, unit, datatype, API/state contract | schema version, datatype, unit, cardinality |
| `HUMAN_FACTOR` | reach range, viewing distance, clearance assumption | population/context, source/evidence, uncertainty |
| `MATERIAL` | thickness, finish code, module size | specification, tolerance, supplier/availability boundary |
| `TEMPORAL` | service interval, animation duration, response time | time unit, scenario, tolerance |
| `AUTHORITY_POINTER` | Current source/baseline/ref | stable target identity, change authority, readback burden |

A variable class does not create a new hierarchy; it controls field and validator expectations.

---

## 3. Shared Variable Authority Matrix

| Condition | Authority rule | Disposition |
|---|---|---|
| one producer, many consumers | exactly one current `change_authority`; consumers register dependency | valid |
| several disciplines propose values | one integrator/decision authority must resolve Current value | `OPEN` until resolved |
| two active owners both claim change authority | authority conflict | `BLOCKED` |
| external mandate fixes variable | external mandate governs boundary; project controller manages implementation | no ordinary trade-off override |
| variable derived from another controlled variable | upstream relation + derivation method required | downstream becomes stale if derivation basis changes |
| variable intentionally differs by configuration | value scoped by baseline/configuration | no global single-value assumption |
| unit/tolerance missing for numerical shared variable | incomplete definition | cannot reach `COORDINATED` |

Hard rule: consumer count may be N; effective current change authority is 1 unless an explicit joint-authority contract defines decision mechanics.

---

## 4. Variable Value Contract

Numerical variable:

`value/range + unit + tolerance + reference/coordinate system + condition + baseline + source authority`.

Categorical variable:

`allowed values + meaning + transition/change rule + compatibility + baseline`.

Semantic variable:

`canonical identifier/term + aliases + forbidden variants + consumer bindings + version`.

Do not store a bare number such as `1200` when mm/m/inches or datum context can change meaning.

---

## 5. Interface Objectification Threshold Matrix

| Relation condition | Simple typed edge sufficient? | Interface object required? |
|---|---:|---:|
| informational awareness only, no lifecycle/property | YES | NO |
| one side consumes stable output; no acceptance/change authority of relationship | MAYBE | only if material coordination needed |
| shared variable/tolerance exists | NO | YES |
| relationship has own owner/integration owner | NO | YES |
| relationship has acceptance criteria/readback | NO | YES |
| relationship has criticality/coupling/maturity/disposition | NO | YES |
| change to relation can reopen multiple objects | NO | YES |
| legal/safety/accessibility boundary crosses sides | NO | YES |
| relationship itself needs historical audit | NO | YES |

Objectification is about lifecycle/semantics, not complexity of drawing.

---

## 6. Interface Participant Model

### 6.1 Pairwise interface
Use when two sides exchange a bounded set of responsibilities/variables.

### 6.2 N-way interface
Do **not** force all N-way relationships into one undifferentiated `side_a/side_b` object.

Use one of two models:

**Hub interface** — one shared interaction plane/contract genuinely governs all participants:
- `participants[]`;
- one `integration_owner`;
- participant-specific obligations;
- shared acceptance contract;
- shared variables.

**Decomposed pairwise interfaces** — use when participant pairs have materially different exchanged variables, authorities, failure modes or acceptance criteria.

Decision rule:
- if pair-specific failure can occur while others pass → decompose;
- if one integrated acceptance result is the only meaningful outcome → hub interface may remain one object.

---

## 7. Interface Definition Completeness Matrix

Before maturity `DEFINED`, material Interface should resolve:

| Field | Mandatory when applicable |
|---|---|
| participants/sides | always |
| purpose | always |
| interface type | always |
| owner per side | material/above |
| integration owner | MAJOR/CRITICAL; recommended MATERIAL |
| controlling authority | when a controlled property exists |
| exchanged inputs/outputs | when semantic/data/physical exchange exists |
| shared variables | when shared values exist |
| coordinate/reference systems | geometric/spatial/mechanical |
| units | numerical exchange |
| tolerances/allowed variation | numerical/geometric/performance exchange |
| constraints/requirements | when governing acceptance |
| coupling | material interface |
| criticality | material interface |
| required maturity | before promotion planning |
| acceptance question/contract | MATERIAL+; full contract MAJOR/CRITICAL |
| validation/verification method | when closure requires evidence |
| change-reopen rule | always for controlled interface |

NASA IRD practice explicitly separates purpose/scope, precedence, responsibility/change authority, coordinate systems, units/tolerances and interface requirements; P4 uses the same separation concept without importing NASA-specific project structure.

---

## 8. Coupling × Criticality Matrix

Coupling and criticality remain independent.

| Coupling \ Criticality | ROUTINE | MATERIAL | MAJOR | CRITICAL |
|---|---|---|---|---|
| `INFORMATIVE` | register only | explicit owner/readback as needed | unusual; justify criticality | possible if information omission is safety/regulatory-critical |
| `DEPENDENT` | lightweight dependency | acceptance question + trace | contract + impact analysis | contract + independent review as applicable |
| `RECIPROCAL` | coordinated check | bilateral coordination/readback | joint decision + integrated readback | full acceptance + independent whole-system review |
| `TIGHTLY_COUPLED` | integrated readback | integrated prototype/readback | full integrated assurance | strongest applicable integrated assurance; no local-pass closure |

Do not compute one blended score that allows low coupling to reduce a hard CRITICAL consequence.

---

## 9. Interface Maturity Entrance Matrix

| Maturity | Minimum evidence/state |
|---|---|
| `IDENTIFIED` | participants + reason interface exists |
| `DEFINED` | exchange semantics, ownership, constraints, variables, acceptance question explicit |
| `COORDINATED` | sides agree current definition + controlling authority; no unresolved same-property authority conflict |
| `EXERCISED` | instantiated in coordinated model/prototype/state flow/rehearsal/integrated representation appropriate to claim |
| `VERIFIED` | current configuration meets acceptance contract with accepted evidence |

Maturity does not equal disposition.

---

## 10. Interface Closure Matrix

| Interface condition | Can `CLOSED`? |
|---|---:|
| maturity below required maturity | NO |
| unresolved authority conflict | NO |
| material shared variable unbaselined/uncoordinated | NO |
| required acceptance contract missing | NO |
| TIGHTLY_COUPLED with no integrated readback | NO |
| required evidence stale/rejected | NO |
| open blocking dependency | NO |
| required maturity met + no in-scope blocker | YES |
| intentionally excluded from claim with explicit boundary | `OUTSIDE_CLAIM`, not `CLOSED` |

For MAJOR/CRITICAL interface, unilateral closure by one side is forbidden unless the acceptance contract explicitly gives that authority.

---

## 11. Acceptance Contract Matrix

Acceptance contract must answer:
- what relationship must work;
- under what configuration/conditions;
- which variables/tolerances are controlled;
- which requirement(s)/Need(s)/Claim(s) it supports;
- what method will exercise/verify it;
- what counts as PASS/FAIL/INCONCLUSIVE;
- who accepts result;
- what evidence carrier is required;
- what change reopens acceptance.

| Criticality | Contract burden |
|---|---|
| ROUTINE | optional concise acceptance note |
| MATERIAL | explicit acceptance question + condition + owner + readback |
| MAJOR | formal acceptance contract + joint ownership/decision path + integrated readback |
| CRITICAL | formal contract + authority resolution + integrated verification + independent review where applicable + explicit claim ceiling |

---

## 12. Material Dependency Matrix

Use `MATERIAL_DEPENDENCY` when the dependency itself requires ownership, state, acceptance or change propagation.

Dependency classes:
- `INPUT_DEPENDENCY`
- `SEQUENCE_DEPENDENCY`
- `CONFIGURATION_DEPENDENCY`
- `EVIDENCE_DEPENDENCY`
- `RESOURCE_DEPENDENCY`
- `AUTHORITY_DEPENDENCY`
- `AVAILABILITY_DEPENDENCY`

States:
`IDENTIFIED → DEFINED → ACTIVE → SATISFIED_FOR_SCOPE | STALE | SUPERSEDED`.

If dependency has no independent lifecycle/properties, keep it as typed edge instead of creating an object.

---

## 13. Interface Change Propagation Matrix

| Changed property | Mandatory first-order reopen | Typical second-order reopen |
|---|---|---|
| shared variable value/tolerance | interface + all registered consumers | artifacts, verification, decisions, presentation if proof affected |
| controlling authority | interface + Authority Snapshot | joint decision/promotion state |
| participant/side identity | interface definition | requirements, dependency graph, assurance |
| coordinate/reference system | geometric consumers | model/drawing/check outputs |
| acceptance criterion | interface assurance | prior PASS becomes historical if criterion material |
| coupling | required integration method | review/readback burden |
| criticality | governance floor | independent review/acceptance obligations |
| required maturity | closure eligibility | promotion state |
| source baseline/configuration | exercised/verified evidence | all claims using interface evidence |

No material interface change closes until affected consumers are reconciled or explicitly proven unaffected.

---

## 14. Interface Register Boundary

`INTERFACE_REGISTER` is a Runtime Control view over Project-plane Interface identities.

Register may summarize:
- ID;
- current maturity/disposition;
- owner;
- criticality;
- stale/reopen status.

Register must not become the only place where participant obligations, acceptance contract, evidence or history exist.

`REGISTER ROW ≠ INTERFACE OBJECT`.

---

## 15. Validator additions for P4 v1.1

- `P4/VAR-M01`: active shared variable has exactly one effective current change authority unless explicit joint contract exists.
- `P4/VAR-M02`: numerical shared variable requires unit and applicable tolerance/reference system before COORDINATED.
- `P4/VAR-M03`: configuration-specific variable values cannot be flattened into one global Current value.
- `P4/IF-M01`: relation meeting objectification threshold must not remain generic `related_to/depends_on` only.
- `P4/IF-M02`: N-way interface must use hub semantics or decomposed pairwise interfaces with explicit rationale.
- `P4/IF-M03`: MAJOR/CRITICAL interface requires one integration owner and formal acceptance contract.
- `P4/IF-M04`: TIGHTLY_COUPLED interface cannot close without integrated readback.
- `P4/IF-M05`: CLOSED requires maturity >= required_maturity and zero in-scope blocking conditions.
- `P4/IF-M06`: OUTSIDE_CLAIM is not CLOSED.
- `P4/IF-M07`: interface change must propagate to registered consumers and affected assurance.
- `P4/REG-M01`: Runtime Interface Register cannot replace Project Interface object identity/details.

## 16. External calibration boundary

NASA interface-management/IRD guidance explicitly treats interface responsibility, change authority, coordinate systems, units, tolerances and interface requirements as controlled information. buildingSMART IFC likewise demonstrates the value of objectified relationships when the relationship needs its own properties/behavior. These calibrate P4 modeling; OLEANDER remains broader than either engineering-specific schema.
