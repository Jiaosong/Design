# OLEANDER Reference Materialization Gate v1.0 — Smoke Test Receipt

Status: **EXECUTED / LOCAL RUNTIME TEST PASS**

The canonical adapter logic was executed in the current runtime against a deterministic one-page synthetic PDF before repository publication.

Test route:

`LOCAL PDF → MATERIALIZE COPY → SHA-256 → PDF PAGE LOCK @ 144 DPI → PNG → PNG SHA-256 → MANIFEST`

Observed runtime:

- `pdftoppm`: available at `/usr/bin/pdftoppm`
- `pypdfium2`: available as fallback
- source PDF bytes: `1380`
- source SHA-256: `4163e6d3acb471f606ae19632159bfa24ec7829290b5f9a5abd997ce9d9a53b6`
- locked page: `1`
- locked DPI: `144`
- locked PNG dimensions: `600 × 400`
- locked PNG bytes: `5711`
- locked PNG SHA-256: `0c1280e05f9df587b75c2103c1c89de5c619380c290a83b173e95bf876c0dcbf`

The test validates the deterministic byte-bridge and reference-frame-lock path for a local PDF in this runtime.

Does not prove:

- public-URL download availability in every execution surface;
- connector materialization availability in every conversation;
- Source Authority;
- rights clearance;
- reconstruction fidelity;
- design quality.

Per-run capability probing remains mandatory.
