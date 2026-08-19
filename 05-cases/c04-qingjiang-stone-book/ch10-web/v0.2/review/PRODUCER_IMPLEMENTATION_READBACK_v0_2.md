# CH10 Web v0.2 — Producer Implementation Readback

## Material delta
- Replaced the flat 13-equal-row index with `Core 8 + Companion Pool + Trip Subset`.
- Restored R03/R04/R08/R10/R11 as known provisional objects rather than treating them as contentless.
- Added prompt/media evidence gates, state modifiers, failure/recovery, exit, memory residue and cross-chapter ownership.
- Added Companion competition / merge / substitute / OFF logic.
- R13 remains a silence/withdrawal proof.

## Runtime facts
1920×1080 and 390×844:
- horizontal overflow = 0
- minimum visible button target = 44×44
- tested JS/page errors = 0
- R06 selection changes detail/prompt
- LOW_STAMINA mode changes the interaction contract to `RECOVER → ORIENT → CONTINUE / RETURN → OPTIONAL CONTENT`
- R13 REOPEN state changes copy after PASS

## Producer-side bug found and repaired
The first v0.2 build reused `modeCopy` as both a data map and an element/global name. Mode selection changed the label but left QUICK copy visible. It was repaired by separating `modeTextMap` from the DOM target and the full viewport regression was rerun.

Runtime correctness does not equal Professional Design PASS.
Independent finished-pixel review remains required.
