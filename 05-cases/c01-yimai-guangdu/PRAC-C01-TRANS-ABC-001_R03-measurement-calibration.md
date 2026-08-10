# PRAC-C01-TRANS-ABC-001｜R03 Measurement Calibration

Verified: 2026-08-10

Status: `MEASUREMENT MODEL LOCKED / BROWSER DRY-RUN PASS / SMALL ADULT PHOTO PILOT READY / RELIABILITY NOT YET ESTABLISHED / HUMAN PILOT NOT RUN`

Scope: `PHOTO PILOT ONLY`; no claim about 2026 site behavior, learning effects, heritage approval, or human-test success.

## 1｜Participant sequence locked

`N0a First Attention → N0b Free Curiosity → PK Prior Knowledge → B1 Evidence Boundary → C1 Facilitated Relation Probe → C2-0 → C2-1 → C2-2 → C2-3`

- N0a commits before curiosity, history, relation or prior-knowledge cues.
- N0b appears only after N0a lock.
- PK appears only after N0a/N0b lock.
- B1 explicitly asks for evidence boundaries, so new D8 evidence-discipline output after B1 is `PROMPTED_NA`, not spontaneous.
- C1 is a **facilitated relation probe** and never supports a spontaneous-discovery claim.
- Every C2 stage commits before the next reveal.

## 2｜SRE = 8-dimensional profile

Primary dimensions:

1. `D1 Actor relation`
2. `D2 Behavior / practice`
3. `D3 Institution / governance`
4. `D4 Temporal relation`
5. `D5 Spatial relation`
6. `D6 Value conflict / normativity`
7. `D7 Interpretation / source relation`
8. `D8 Evidence responsibility / uncertainty`

Each dimension stores `ABSENT / SPONTANEOUS / PROMPTED_NA / AMBIGUOUS / EXPLICIT_REJECTION`. Only `SPONTANEOUS` receives depth `1–3`. The primary result remains a dimension vector rather than one SRE total.

## 3｜PLS = four typed contamination scores

- `PLS-L` lexical echo, 0–2
- `PLS-S` semantic echo, 0–2
- `PLS-R` structural/order echo, 0–2
- `PLS-C` continuation/path echo, 0–2

`High Leakage = total >= 4/8 OR any subtype = 2`.

PLS is a prompt-contamination diagnostic, not a learning-effect score.

## 4｜Raw-data / coding boundary

The R03 dry run identified and corrected one schema ambiguity:

- participant raw export contains only stage exposure, original response, timestamps/duration and C2 object order;
- participant raw data does **not** contain researcher SRE/PLS codes;
- blind coder export separately contains all eight SRE status/depth fields and four PLS subtype fields;
- reconciliation remains a third layer and cannot overwrite either original coder file.

Required chain:

`Raw Response → Stage/Prompt Exposure → Evidence Source → Minimal Code → PLS → SRE → Higher-order Interpretation → Decision`

## 5｜Dual-coder reliability pre-registered

During the small adult photo-pilot, 100% of records must be independently coded by two coders before reconciliation.

- SRE status → Cohen's kappa per dimension.
- SRE depth 0–3 → quadratic weighted Cohen's kappa.
- PLS subtype 0–2 → quadratic weighted Cohen's kappa.
- Exact agreement always reported beside kappa.

OLEANDER internal thresholds:

- `PASS`: kappa >= 0.75 AND exact agreement >= 85%.
- `REVISE`: kappa 0.60–0.749 OR exact agreement 75–84.9%.
- `REJECT FOR DECISION USE`: kappa < 0.60 OR exact agreement < 75%.
- one observed category → `NON_ESTIMABLE`; high raw agreement alone cannot create PASS.

These are project decision thresholds, not universal psychometric standards.

## 6｜C2 progressive reveal

- `C2-0`: A/B images only; order randomized and recorded; no names/dates/biographies/locations/comparison dimensions.
- `C2-1`: reveal location/context only; record change or justified non-change.
- `C2-2`: reveal object/category names only.
- `C2-3`: reveal minimal source-bound biography/context; add third object with incomplete visual evidence and require explicit uncertainty preservation.

Each stage locks before the next reveal.

## 7｜Pre-registered decision rules

### N0 spontaneous discoverability
- `>=50%` valid participants with >=1 D1–D7 spontaneous relation at depth >=1 before B1/C1 → supports discoverability hypothesis for the next design iteration.
- `25–49%` → weak/conditional.
- `<25%` → do not claim discoverability.

This is a pilot design heuristic, not population inference.

### C1 facilitated probe
- KEEP: premise rejection <=25%, high leakage <=50%, and >=50% valid records contain an evidence-bounded relation after facilitation.
- REVISE: premise rejection 26–40% or high leakage 51–70%.
- REJECT CURRENT PROBE: premise rejection >40% or high leakage >70%.
- C1 never supports self-discovery claims.

### C2
- KEEP: information responsiveness >=75%, incomplete-evidence integrity >=75%, C2-0 high leakage <=20%.
- REVISE: any core measure 50–74%.
- REJECT CURRENT REVEAL SEQUENCE: any core measure <50%.

## 8｜Browser dry-run integrity — EXECUTED

Headless Chromium / Playwright dry run reached exactly:

`N0a → N0b → PK → B1 → C1 → C2-0 → C2-1 → C2-2 → C2-3`

Observed:

- all 9 stages reached;
- no Back/Edit control appeared after locking;
- 9 stage records persisted;
- every record contained `started_at / locked_at / duration_ms`;
- randomized C2 object order was recorded;
- N0a/N0b early responses survived later stages unchanged;
- page-level JavaScript errors: `0`.

Boundary: the dry run did **not** test human comprehension, two-coder reliability, historical truth, image-rights clearance, 2026 site conditions, or design effectiveness.

Decision: `R03 DRY-RUN PASS / SMALL ADULT PHOTO PILOT READY`.

## 9｜Pilot boundary

Operational target: `12–18 adults` for protocol debugging only. This is an exercise planning range, not a power calculation or formal sample-size conclusion. Minors remain out of scope until adult comprehension, codebook stability and local/ethical requirements are reviewed.

GitHub stores versioned logic/protocol only. Rights-pending project-source photographs remain internal/Drive evidence and are not republished as OLEANDER-owned media.