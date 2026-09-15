# OLEANDER Machine Governance Schemas

Current machine authority:

- `claim-id.schema.json` — canonical Claim ID namespace; bare `Cnn` is reserved for Case Axis roots and cannot substitute for Project IDs.
- `c01-evidence-manifest.v1.schema.json` — canonical C01 evidence manifest contract.
- `c01-evidence-manifest.template.json` — current C01 starter template.
- `oleander-project-flow-v0.3.schema.json` — Project Flow machine contract. It separates `project_level + project_id`, Case ID, Delivery Priority, Application Mapping and `Domain / exact L0–L7` knowledge context; old `primary_layer / primary_node / supporting_nodes` semantics are not current authority.
- `architecture-design-development-receipt.v1.schema.json` — machine contract for triggered architectural design-development receipts; it records the current architecture process state, independent plan review, stale/reopen status and promotion result without converting design-process PASS into statutory/code/engineering approval.
- `design-quality-development-receipt.v1.schema.json` — machine contract for the shared OLEANDER Design Quality & Design Development Specification; it records triggered design-development dimensions, design maturity, multi-scale readback, genericity/coherence review, stale/reopen state and independent Design KEEP without turning design judgment into an automated score.
- `professional-domain-process.v1.schema.json` — subordinate generic contract for a reusable `PROFESSIONAL_DOMAIN_PROCESS_DEFINITION` or project `DOMAIN_PROCESS_INSTANCE` with embedded `DOMAIN_STAGE_INSTANCE` records. It preserves authentic domain stage IDs, reuses existing Integration maturity semantics, and does not expand the Master Runtime summary or create another professional-process taxonomy/database.
- `professional-domain-process.example.json` — bounded project-instance example showing an Architecture ADD stage instance without converting the example into Current project authority.
- `validate_professional_domain_process.py` — structural + narrow runtime-consistency validator for the generic definition/instance contract. It checks duplicate stage/binding/instance IDs and basic CLOSED/BLOCKED/STALE consistency; it never awards professional quality, Design KEEP, engineering/statutory validity or Promotion.
- `production-asset-persistence-manifest.v1.schema.json` — canonical machine-readable contract for durable production binary persistence receipts.
- `production-asset-persistence-manifest.template.json` — starter receipt for native source + canonical model + production ZIP + checksum persistence.
- `validate_architecture_namespaces.py` — fail-closed architecture gate for Project Axis / AIG / current routing / frozen Legacy roots / Project Flow schema separation.
- `validate_namespaces.py` — fail-closed Case / Claim / Project-ID / Application-Mapping namespace checks used by governance CI.

Architecture order for new machine-readable objects is:

`Knowledge Architecture (Domain + exact L0–L7) → Application Mapping (B/CU/IP/SP) → Project Axis (P0–P4 + explicit Project ID) → Runtime / Evidence`.

A Case ID such as `C04`, an Application Mapping code such as `IP03`, a Gate such as `G2`, or a Delivery Priority such as `Priority-1` never substitutes for a Project Axis identity.

For a production persistence receipt to become `PERSISTENCE PASS`, every triggered required binary must have at least one durable copy with a stable provider ID, independent retrieval, matching byte size + SHA-256 and open/unzip/parse verification. A text/hash-only record does not satisfy the contract.

Historical `P01_evidence_manifest*` files remain immutable provenance sources and are explicitly superseded; they must not be used to validate or generate new C01 records.
