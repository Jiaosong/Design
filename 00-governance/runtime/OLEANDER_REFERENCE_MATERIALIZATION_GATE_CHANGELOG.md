# OLEANDER Reference Materialization Gate changelog

## v1.0 — 2026-08-17

Introduced a cross-project preflight gate for strict reference reconstruction.

Key change:

`browser-visible source` is no longer treated as equivalent to `local source bytes available to reconstruction QA`.

Required before a 1:1 reproduction claim:

`Source Authority → Source Bytes → SHA-256 → Locked Reference Frame → Comparison Runtime → Fidelity Review`.
