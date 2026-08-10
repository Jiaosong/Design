# PRAC-C01-TRANS-ABC-001｜R03 Measurement Calibration

Verified: 2026-08-10

Status: `MEASUREMENT MODEL LOCKED / RELIABILITY NOT YET ESTABLISHED / HUMAN PILOT NOT RUN`

Scope: `PHOTO PILOT ONLY`; no claim about 2026 site behavior, learning effects, heritage approval, or human-test success.

## 1｜Participant sequence locked

`N0a First Attention → N0b Free Curiosity → PK Prior Knowledge → B1 Evidence Boundary → C1 Facilitated Relation Probe → C2 progressive reveal`

- N0a commits before any curiosity, history, relation or prior-knowledge cue appears.
- N0b appears only after N0a lock.
- PK appears only after N0a/N0b lock.
- B1 explicitly asks for evidence boundaries, so new D8 evidence-discipline output after B1 is `PROMPTED_NA`, not spontaneous.
- C1 is explicitly facilitated and **never** used to claim spontaneous relation emergence.
- Every C2 stage commits before the next information reveal.

## 2｜SRE becomes an 8-dimensional profile

The primary measure is no longer one total score.

1. `D1 Actor relation`
2. `D2 Behavior / practice`
3. `D3 Institution / governance`
4. `D4 Temporal relation`
5. `D5 Spatial relation`
6. `D6 Value conflict / normativity`
7. `D7 Interpretation / source relation`
8. `D8 Evidence responsibility / uncertainty`

Each dimension stores:

`ABSENT / SPONTANEOUS / PROMPTED_NA / AMBIGUOUS / EXPLICIT_REJECTION`

Only `SPONTANEOUS` receives depth `1–3`. A later prompt cannot retroactively convert an earlier absent/ambiguous response into spontaneous evidence.

## 3｜PLS becomes four typed contamination scores

- `PLS-L` lexical echo, 0–2
- `PLS-S` semantic echo, 0–2
- `PLS-R` structural/order echo, 0–2
- `PLS-C` continuation/path echo, 0–2

`High Leakage = total >= 4/8 OR any subtype = 2`.

PLS is a prompt-contamination diagnostic, not a learning-effect score.

## 4｜Dual-coder reliability pre-registered

During the small adult photo-pilot, 100% of records must be independently coded by two coders before reconciliation.

Primary metrics:

- SRE categorical status → Cohen's kappa per dimension.
- SRE depth 0–3 → quadratic weighted Cohen's kappa.
- PLS subtype 0–2 → quadratic weighted Cohen's kappa.
- Exact agreement is always reported beside kappa.

OLEANDER internal pre-registered thresholds:

- `PASS`: kappa >= 0.75 AND exact agreement >= 85%.
- `REVISE`: kappa 0.60–0.749 OR exact agreement 75–84.9%.
- `REJECT FOR DECISION USE`: kappa < 0.60 OR exact agreement < 75%.
- If only one category appears, kappa is `NON_ESTIMABLE`; high raw agreement alone cannot create a PASS.

These are project decision thresholds, not claimed as universal psychometric standards.

## 5｜C2 progressive reveal

### C2-0 — image only
A/B photo order is randomized and recorded. No names, dates, biographies, locations or comparison dimensions.

### C2-1 — location reveal
Reveal location/context only. Record changed judgment or justified non-change and which reveal caused it.

### C2-2 — object/category reveal
Reveal names/category labels only. Lock again.

### C2-3 — biography/source reveal
Reveal minimal source-bound claims. Add the third object with deliberately incomplete visual context. The participant must be allowed to preserve `UNKNOWN` rather than fill the evidence gap.

## 6｜Pre-registered decision rules

### N0 spontaneous discoverability
- `>=50%` of valid pilot participants show at least one D1–D7 spontaneous relation at depth >=1 before B1/C1 → supports the discoverability hypothesis for the next design iteration.
- `25–49%` → weak/conditional.
- `<25%` → do not claim discoverability.

This is a pilot design heuristic, not population inference.

### C1 facilitated probe
- KEEP: premise rejection <=25%, high leakage <=50%, and >=50% valid records contain an evidence-bounded relation after facilitation.
- REVISE: premise rejection 26–40% or high leakage 51–70%.
- REJECT CURRENT PROBE: premise rejection >40% or high leakage >70%.
- C1 can never support a self-discovery claim.

### C2
- KEEP: information responsiveness >=75%, incomplete-evidence integrity >=75%, high leakage at C2-0 <=20%.
- REVISE: any core measure 50–74%.
- REJECT CURRENT REVEAL SEQUENCE: any core measure <50%.

## 7｜Pilot boundary

Operational target: `12–18 adults` for protocol debugging only. This is an exercise planning range, **not** a power calculation or formal sample-size conclusion. Minors remain out of scope until adult comprehension, codebook stability and local/ethical requirements are reviewed.

## 8｜Artifacts and evidence boundary

Generated locally/Drive:

- v0.3 one-way participant runner;
- blind coder console;
- machine-readable preregistration;
- SRE × PLS codebook;
- dual-coder CSV template;
- pure-Python Cohen/weighted-kappa calculator;
- C2 progressive-reveal protocol;
- pre-registered decision thresholds.

The reliability calculator has passed a **formula/boundary self-test only**. This does not establish inter-rater reliability. Two real independent coders and real pilot records are still required.

GitHub stores versioned logic and protocol only. Rights-pending project-source photographs remain internal/Drive evidence and are not republished as OLEANDER-owned media.