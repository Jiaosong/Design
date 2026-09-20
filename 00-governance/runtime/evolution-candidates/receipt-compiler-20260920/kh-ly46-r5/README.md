# KH-LY46 R5 receipt-compiler exercise

This directory replays the historical bounded #674 Structural Engineering and Building Services / MEP `HOLD` evidence through the new non-authority receipt compiler.

The source facts are carried as standard `DOMAIN_PROCESS_INSTANCE` / `DOMAIN_STAGE_INSTANCE` objects. `compile_project_receipts.py` then derives candidate receipt projections and source-integrity readbacks from those stage facts plus the existing interface/system-track inputs.

Results:

- Structural process instance: validator `PASS`; compiled receipt remains `HOLD`; source integrity `PASS`.
- MEP process instance: validator `PASS`; compiled receipt remains `HOLD`; source integrity `PASS`.
- `KH-LY46_R5_COMPILER_PARITY_READBACK_v001.json` confirms bounded semantic parity for identity, source revision, claim ceiling, HOLD state, stage/interface identity and all historical `does_not_prove` boundaries.
- Persisted receipt/source digests use explicit `UTF8_TEXT_LF_CANONICAL_V1` semantics for these JSON/Markdown sources, preventing checkout EOL policy from changing identity.

This exercise does **not** supersede the #674 manual receipts and does not mutate KH-LY46 `PROJECT_STATE` or `CURRENT_MANIFEST`. The compiled receipts are evaluation projections only. No Structural, MEP, integration, field, statutory, Design KEEP or Promotion claim is added.
