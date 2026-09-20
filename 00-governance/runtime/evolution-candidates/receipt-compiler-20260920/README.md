# Receipt compiler provenance state

Current provenance receipt for PR #680 is `RECEIPT_COMPILER_OWNER_RECEIPT_v002.json`.

`RECEIPT_COMPILER_OWNER_RECEIPT_v001.json` is retained for no-loss historical readback but its digest semantics are `SUPERSEDED_HASH_SEMANTICS`: it hashed working-tree raw text bytes and therefore could drift across Windows CRLF/LF checkout policy without any semantic content change.

v002 binds the same 22 PR #680 material files to exact Git blobs at `ded584b413168718a21c28c58b7632c302dcea8e`. UTF-8 text identity uses `UTF8_TEXT_LF_CANONICAL_V1`; binary/unknown formats use `RAW_BYTES_V1`. This repair changes provenance/hash semantics only. It does not change professional verdicts, project authority, Structural/MEP claim ceilings, Technical Drawing authority, Design KEEP, or Promotion state.
