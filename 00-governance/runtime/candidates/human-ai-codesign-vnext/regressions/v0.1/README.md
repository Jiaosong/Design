# OLEANDER Human–AI Co-Design vNext — Regression Pack v0.1

Status: **CANDIDATE / LOCAL / NO PROMOTION**

This pack turns the vNext interaction/runtime boundary into executable checks. It intentionally separates:

- **REAL_CARRIER** checks — read existing owner-native project/runtime carriers without changing them;
- **FIXTURE** checks — exercise conflict semantics that must not be fabricated inside a live project merely to obtain a test case.

The pack is not a second Project State, checkpoint database, authority registry, professional process or Promotion gate.

## Covered checks

| ID | Mode | Purpose |
|---|---|---|
| CD-01 | REAL_CARRIER | recover a current frontier without chat memory |
| CD-05 | FIXTURE | stale checkpoint may not mutate a newer sequence |
| CD-05B | FIXTURE | authority/source drift blocks authority-sensitive mutation but preserves bounded reversible work |
| CD-06 | HYBRID | real editable/readback carrier roles + explicit recency fixture prove that a later derivative does not replace its editable source |
| CD-07 | REAL_CARRIER | missing Fusion native surface keeps native completion on HOLD while bounded editable prototyping remains legal |
| CD-09 | REAL_CARRIER | owner-native state/checkpoint/native carriers live outside the plugin; actual plugin uninstall remains a separate runtime test |
| CD-11 | FIXTURE | scoped human roles do not collapse into latest-message-wins authority |

## Run

```powershell
py -3 00-governance\runtime\candidates\human-ai-codesign-vnext\regressions\v0.1\run_regressions.py
```

The runner writes `REGRESSION_RESULTS_v0.1.json` beside itself.

## Claim boundary

`PASS` here means the named regression behaved correctly at its declared test mode. It does **not** mean Design KEEP, professional PASS, field truth, plugin production readiness, Current promotion or project promotion.

`CD-09` is deliberately reported as **PARTIAL** until an actual installed-plugin removal/reinstall exercise is performed. Carrier independence can be proven locally; an uninstall event should not be fabricated.
