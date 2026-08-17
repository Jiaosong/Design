# Reference materialization entrypoint

Use `OLEANDER_REFERENCE_MATERIALIZATION_GATE_v1.0.md/.json` before any OLEANDER task claims a 1:1 reference reproduction.

Canonical helper:

`python tools/oleander-runtime/materialize_reference.py ...`

The helper creates local source bytes, SHA-256 evidence and an optional locked PDF reference frame. Source materialization is a precondition for deterministic overlay/difference review, not proof of fidelity or design quality.
