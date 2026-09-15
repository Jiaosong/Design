# EV-PROF-INTERIOR-LANDSCAPE-20260915 — authority rebase note

**Status:** PROVENANCE / REBASE CONTROL NOTE  
**Prior evaluated baselines:** `main@5ca6449b9260f0539f2cd94e312b949d7af234bc`, then `main@20863ca819a22a7a6a0b47664a51f2d0996538e3`  
**Current frozen baseline:** `main@c1d848187f438961a98267b3c3d7474a6676933a`

Earlier EV3/green results and the original independent-review packet remain provenance only after Current architecture-control drift.

Material Current additions since the original EV3 baseline:

- PR #628: bounded multi-surface partial-commit reconciliation. A known incoherent partial commit blocks dependent handoff READY/ACCEPTED and DAG advance; reconciliation remains an ephemeral runtime projection and does not create transaction authority.
- PR #629: consequential decision authorization projection. Professional/independent judgment must resolve actor/authority, scope, claim boundary and applicable competence/independence/legal basis from owner-native evidence; machine identity or title cannot invent authority or competence.
- PR #630: Observability Event + bounded Recovery Incident contract. Telemetry is not authority; recovery preserves unaffected verified state, requires actual postcondition readback, reruns/reaccepts only affected reviews/handoffs, and resume remains authorization-bound.

The Interior/Landscape domain semantics are not automatically invalidated by these cross-cutting additions, but the candidate must be re-evaluated on the new Current baseline. Until that re-evaluation completes, the candidate state is `EV2_EVAL_READY`, not EV3/EV4.

The original review packet is explicitly superseded/provenance. A successor review packet must bind the exact fresh EV3 candidate head after regression on `c1d84818…`.

`PRIOR GREEN EVIDENCE ≠ CURRENT EV3 AFTER MATERIAL AUTHORITY DRIFT`.
