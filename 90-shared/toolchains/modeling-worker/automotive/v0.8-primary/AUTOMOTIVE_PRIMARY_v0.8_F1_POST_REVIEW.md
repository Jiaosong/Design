# OLEANDER Automotive Primary Surface｜v0.8｜F1 Post-Review

**Status:** `M5 PASS WITH LIMITATIONS / M6 PASS FOR F1 / CANDIDATE_AUTHORITY — PRIMARY SURFACE BENCHMARK`
**Modeling Contract:** `v0.2 / Spec Patch v0.2.1`

## Decision
The v0.8 automotive rebuild may now serve as the OLEANDER F1 primary-surface benchmark. It is not Class-A, engineering CAD or a final vehicle-design authority.

## Repair chain
- R01 — Hard Points + section network; visual cabin REVISE; height-QA bug identified.
- R02 — height Gate fixed; split BODY/CABIN closed-volume hat defect persisted.
- R03 — body-cabin interface conditionally unlocked; rebuilt as one integrated primary shell.
- R04 — floating glazing overlays REJECTED.
- R05 — controlled SubD longitudinal tension + flush face-level glazing zones; Machine/Construction PASS.
- R06 — normal diagnostic renderer fixed so silhouette review no longer destroys polygon material indices; normal F1 views reviewed.
- R07 — selective glazing-mask closure PASS.

## R07 diagnostic closure
GitHub Run `31559096522`, Job `93997527335`, Artifact `9127068419`, SHA-256 `a6d6ecd8acfa1264bf4e7356601afa444d76519e1bddf97a25259794376521cf`.

- material indices before/after: `3566 body / 612 glazing` → unchanged
- side glazing mask: `17,912` red-dominant pixels
- front glazing mask: `39,366` red-dominant pixels
- diagnostic closure: PASS

R06 normal diagnostic evidence: Run `31558664550`, Artifact `9126935876`, SHA-256 `3d6483b0a060e19d314340db191304f170cb8a4370e649b8ceadaa49e0ca6f65`.

## Visual QA
PASS:
- separate soft-hat architecture is closed;
- one continuous fastback primary volume is legible;
- flush glazing zones read as part of the shell, not floating patches;
- Broad / Strip / Grazing have coherent large-scale flow;
- stance and wheel openings remain stable;
- no premature M7/M8 details were used to make the primary form read.

LIMITATIONS:
- front volume remains broad/under-articulated until M7 bumper/lamp architecture;
- fender crown / hood relation remains primary-surface level;
- roof/glazing graphic remains generic benchmark geometry;
- no Class-A, G2 production, package, crash, aero, homologation or manufacturing claim.

## Promotion
`WORKING_SOURCE → CANDIDATE_AUTHORITY — PRIMARY SURFACE BENCHMARK`

M7 secondary geometry may begin only as a derived working source. Any M7 change that exposes a primary-surface failure must reopen M5 through `CONDITIONALLY_UNLOCKABLE` rather than patch locally.
