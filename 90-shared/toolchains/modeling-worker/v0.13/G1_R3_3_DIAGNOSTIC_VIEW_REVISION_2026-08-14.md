# G1 R3.3｜Diagnostic View Revision｜2026-08-14

## State

`EXACT_B_EXECUTION_PASS / INTERFACE_FAIRNESS_CONFIRMED / LOCAL_BASIN_DEFINITION_VIEW_INSUFFICIENT / SOURCE_UNCHANGED`

The first R3.3 confirmation run used the exact selected `R3.2-B-CORE-RECOVERY` relation and passed all Machine, interior-fairness, shared-runtime, source-restore and authority checks. The run itself is valid evidence; its local camera framing is not sufficient to close the visual confirmation question.

## Evidence

Head:

`a11051992a0a04ee95371b9d954ace0d645ecdf1`

Workflow:

- `OLEANDER Modeling Worker v0.13 R3.3 Interface Confirmation`
- run `31798292093`
- result `SUCCESS`

Artifact:

- ID `9218343614`
- digest `sha256:ed04d577423fc5846287ef08e760744c8a23e194b492838b472a896480aecf10`
- size `5,402,773 bytes`

Exact B relation retained:

- `u_halfspan = 0.26`
- `theta_halfspan_rad = 1.06`
- `core_fraction = 0.29`
- `depth_m = 0.012`
- `theta_center = TOP_MERIDIAN`

Machine and fairness remain PASS.

## Visual Finding

The global HERO evidence remains consistent with the R3.2 direction decision: the severe R2 interface-right reflection compression is removed while the interface still reads as a subordinate recessed field.

The first local camera used:

- lens `120 mm`
- offset from live interface center `[0.11, -0.15, 0.09] m`

Under local Strip / Grazing / Zebra, B shows a materially smoother normal/reflection field than R2. However, the framing is too tight to include enough of the complete basin boundary and surrounding palm field. Therefore it cannot reliably answer the remaining visual question: whether local interface definition is preserved at the intended hierarchy.

This is a **diagnostic framing limitation**, not evidence that the Source relation failed.

## Legal Revision

Revise only the local diagnostic camera:

- keep exact B Source relation unchanged;
- keep HERO camera unchanged;
- keep Strip / Grazing / Zebra unchanged;
- widen the local view to include the whole interface basin plus surrounding palm field;
- create the revised camera through the shared Blender Surface System runtime;
- re-run the exact same Machine / fairness / source-restore gates.

No Source tuning, mesh-local edit, threshold relaxation, Candidate Promotion or Canonical Promotion is authorized.

## Authority

- `DESIGN STATE = REVISE / INTERFACE DIRECTION SELECTED`
- `AUTHORITY STATE = WORKING_SOURCE`
- `CANDIDATE REVIEW = REOPENED`
- `CANDIDATE PROMOTION = NOT_RUN / BLOCKED`
- `RIGHT / FRONT TERMINATION = OPEN / SEPARATE`
