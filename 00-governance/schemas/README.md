# OLEANDER Machine Governance Schemas

Current authority:

- `claim-id.schema.json` — canonical Claim ID namespace; bare `Cnn` is reserved for case roots.
- `c01-evidence-manifest.v1.schema.json` — canonical C01 evidence manifest contract.
- `c01-evidence-manifest.template.json` — current C01 starter template.
- `production-asset-persistence-manifest.v1.schema.json` — canonical machine-readable contract for durable production binary persistence receipts.
- `production-asset-persistence-manifest.template.json` — starter receipt for native source + canonical model + production ZIP + checksum persistence.
- `validate_namespaces.py` — fail-closed checks used by AI Governance CI.

For a production persistence receipt to become `PERSISTENCE PASS`, every triggered required binary must have at least one durable copy with a stable provider ID, independent retrieval, matching byte size + SHA-256 and open/unzip/parse verification. A text/hash-only record does not satisfy the contract.

Historical `P01_evidence_manifest*` files remain immutable provenance sources and are explicitly superseded; they must not be used to validate or generate new C01 records.
