# OLEANDER Machine Governance Schemas

Current authority:

- `claim-id.schema.json` — canonical Claim ID namespace; bare `Cnn` is reserved for case roots.
- `c01-evidence-manifest.v1.schema.json` — canonical C01 evidence manifest contract.
- `c01-evidence-manifest.template.json` — current C01 starter template.
- `validate_namespaces.py` — fail-closed checks used by AI Governance CI.

Historical `P01_evidence_manifest*` files remain immutable provenance sources and are explicitly superseded; they must not be used to validate or generate new C01 records.
