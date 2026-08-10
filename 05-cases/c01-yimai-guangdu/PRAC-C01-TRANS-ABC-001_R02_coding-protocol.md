# R02 Researcher Coding Protocol

Status: `PROTOCOL / NOT HUMAN TEST`.

## Coding order

1. Coder receives only a condition-free response dataset.
2. Coder must not receive prompt card, blind card ID, OLD/v0.2/N0 label, or coordinator key.
3. Code Prompt Leakage Score (PLS) first.
4. Code Spontaneous Relation Emergence (SRE) provisionally from response text only.
5. Lock coding sheet.
6. Coordinator reveals condition mapping.
7. Recalculate SRE validity: every dimension explicitly prompted by that condition becomes `CONTAMINATED / NA`.
8. Compare conditions only after this invalidation step.

## PLS｜0–4

- +1 lexical/concept echo of a distinctive prompt phrase;
- +1 prompted relation/governance concept without independent observation/source/example;
- +1 response organization mirrors prompt order;
- +1 question/continuation only reformulates a prompt-provided path.

Interpretation:
- 0 no detectable uptake;
- 1 minor uptake;
- 2 moderate contamination;
- 3 high contamination;
- 4 response largely prompt-shaped.

## SRE｜0–3

Only unprompted dimensions count.

- 0 object/form only;
- 1 independently introduces actor/action/context relation;
- 2 relation + evidence/uncertainty boundary;
- 3 relation + evidence boundary + own unresolved question + independently named verifier/source.

## Mandatory flags

`PREMISE_REJECTED / NO_QUESTION / NO_NEXT_STEP / PRIOR_KNOWLEDGE / SOURCE_CONFLICT / FORM_ONLY / PROMPT_ECHO / METRIC_GAMING / PHOTO_CONTEXT_LIMIT`

## Non-negotiable rule

Rich output is not automatically better output. Prompt-shaped richness can score high PLS and zero valid SRE.

## Inter-coder gate

- a subset must be independently double-coded;
- disagreements are recorded before reconciliation;
- do not average away category disagreements;
- unblinding occurs only after first-pass coding is locked;
- no simulated record may be reported as a real participant result.
