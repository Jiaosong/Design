# OLEANDER Machine Governance Schemas

Current machine authority:

- `claim-id.schema.json` — canonical Claim ID namespace; bare `Cnn` is reserved for Case Axis roots and cannot substitute for Project IDs.
- `c01-evidence-manifest.v1.schema.json` — canonical C01 evidence manifest contract.
- `c01-evidence-manifest.template.json` — current C01 starter template.
- `oleander-project-flow-v0.3.schema.json` — Project Flow machine contract. It separates `project_level + project_id`, Case ID, Delivery Priority, Application Mapping and `Domain / exact L0–L7` knowledge context; old `primary_layer / primary_node / supporting_nodes` semantics are not current authority.
- `production-asset-persistence-manifest.v1.schema.json` — canonical machine-readable contract for durable production binary persistence receipts.
- `production-asset-persistence-manifest.template.json` — starter receipt for native source + canonical model + production ZIP + checksum persistence.
- `validate_architecture_namespaces.py` — fail-closed architecture gate for Project Axis / AIG / current routing / frozen Legacy roots / Project Flow schema separation.
- `validate_namespaces.py` — fail-closed Case / Claim / Project-ID / Application-Mapping namespace checks used by governance CI.

Architecture order for new machine-readable objects is:

`Knowledge Architecture (Domain + exact L0–L7) → Application Mapping (B/CU/IP/SP) → Project Axis (P0–P4 + explicit Project ID) → Runtime / Evidence`.

A Case ID such as `C04`, an Application Mapping code such as `IP03`, a Gate such as `G2`, or a Delivery Priority such as `Priority-1` never substitutes for a Project Axis identity.

For a production persistence receipt to become `PERSISTENCE PASS`, every triggered required binary must have at least one durable copy with a stable provider ID, independent retrieval, matching byte size + SHA-256 and open/unzip/parse verification. A text/hash-only record does not satisfy the contract.

Historical `P01_evidence_manifest*` files remain immutable provenance sources and are explicitly superseded; they must not be used to validate or generate new C01 records.
