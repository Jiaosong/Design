# OLEANDER / 织作 — SP04-R02 Interoperability & Topology QA

Status: **ACTUALLY EXECUTED / PASS**

Layer: Spatial / SP04 — Construction & Operation.

R02 upgrades R01 from geometric parameter validation to a cross-format delivery gate.
Each T01–T05 variant is a single connected, watertight host-opening mesh.

Executed evidence:
- 5 native meshes;
- 15 exported models: OBJ / STL / GLB;
- 15/15 successful round-trip reload checks;
- analytical volume and bounding-box comparison;
- one real detected error in run 1: inward global winding caused negative signed volume;
- correction: normalize outward face orientation before export, then rerun the full matrix.

Internal review: **98/100**.

Scope boundary: geometric topology and interoperability only. No BIM semantics, IFC property sets, schedules, manufacturer data, or regulatory compliance are claimed.

All dimensions are training-only hypothetical parameters.
