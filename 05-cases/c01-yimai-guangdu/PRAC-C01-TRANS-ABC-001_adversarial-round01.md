# PRAC-C01-TRANS-ABC-001｜Simulated Participant Adversarial Test｜Round 01

Verified: 2026-08-10

Status: `SIMULATED ONLY / NOT HUMAN TEST / NOT EFFECT VALIDATION`

Source prototype: `Real-photo A/B/C Round 01`, using the same Zhenxiao Archway project-source photograph for B/C. This round deliberately constructs participants who resist, misunderstand, game or reject the task. It is a defect-discovery exercise, not an estimate of real participant behavior.

## Attack set

10 simulated attack profiles were used:

1. **SIM-01 / rushed visitor** — 30-second completion; refuses detailed reading.
2. **SIM-02 / form-aesthetic reader** — talks only about symmetry, carving and appearance.
3. **SIM-03 / high-compliance prompt echo** — repeats the interface vocabulary to look successful.
4. **SIM-04 / prior-history expert** — imports prior knowledge into direct observation.
5. **SIM-05 / premise rejector** — rejects the wording that the archway “required someone to obey something”.
6. **SIM-06 / locally familiar participant** — challenges project-source wording with local knowledge.
7. **SIM-07 / low-jargon or younger reader** — cannot reliably use inference / interpretation-right / verifier terminology.
8. **SIM-08 / evidence-strict reader** — refuses to infer approach/pass/leave behavior from one static photograph.
9. **SIM-09 / task optimizer** — manufactures an unresolved question because the success rule rewards it.
10. **SIM-10 / voluntary exit** — has no interest in continuing to another node/source.

These are attack vectors, not demographic personas.

## Defect register

### D01 / CRITICAL / C — leading normative premise

Current prompt: `这个对象在当时要求谁遵守什么？`

Problem: the task already inserts a normative/regulatory interpretation before the participant has generated one.

Decision: **REJECT participant-facing wording.** Replace with a neutral prompt such as: `从当前证据，你觉得它可能与哪些人、行为或制度有关？哪些不能确定？`

Normative/regulatory relations may be coded later by the researcher, not planted in the participant answer.

### D02 / CRITICAL / C — “interpretation rights” leakage

Current prompt: `今天谁有权解释它？`

Problem: OLEANDER's governance concept is given directly to the participant. Prompt-compliant answers can therefore look like autonomous governance awareness.

Decision: participant-facing wording becomes: `如果还想理解，你会去问谁或查什么？为什么？`

`local interpretation authority / governance / revision rights` moves to the facilitator coding layer after the free response.

### D03 / CRITICAL / C — forced unresolved question and forced next verifier

Current prototype requires an unresolved question and a next verifier. This creates false autonomy and suppresses valid exit/no-question states.

Revision must explicitly allow:

- no question;
- question already resolved enough for the participant;
- premise rejected;
- does not want to continue;
- no next step;
- other/free text.

A blank/exit response is valid evidence, not automatic failure.

### D04 / CRITICAL / C — spatial overclaim from photo-only evidence

The current C language contains `approach → observe → compare → continue`, but the real-photo prototype uses a static photograph. A static image cannot validate approach direction, passing behavior or stopping sequence.

Decision: photo version is downgraded to **Relation Hypothesis**. `Approach / pass / leave` is enabled only with the same-session three-segment field sequence or on-site test.

### D05 / HIGH / B — evidence options already interpret the image

The B selector supplies labels such as `整体几何 / 两柱三层` and `现代环境并置`. A compliant participant can repeat those labels without independently noticing the evidence.

Revision: Stage 1 is free observation with no named hotspots or structural labels. Researcher coding occurs after submission.

### D06 / HIGH / B — assumes a judgement changed

Current question: `哪个证据改变了你最初的判断？`

This presupposes change and pressures participants to invent one.

Revision: `你的判断有没有变化？无变化也有效；若变化，是什么导致的？`

### D07 / HIGH / B + C — prior knowledge and source conflict are not captured

A participant may know a date, biography or local story before seeing the image, or may directly contradict the project-source caption. The current form does not preserve this provenance conflict.

Add fields:

- `prior_knowledge`;
- `source_conflict`;
- `local_correction`;
- unresolved conflict status.

Do not silently reconcile conflicting source claims.

### D08 / HIGH / C2 — comparison dimensions are preloaded

The current C2 page displays biography/location/evidence/interpretation dimensions before free comparison. A participant can simply follow the intended matrix.

Revision: two-stage protocol:

1. **blind free comparison** — no research dimensions shown;
2. after submission, researcher coding matrix is revealed/used.

If participants do not spontaneously enter biography, institution, location, evidence or governance, do not rewrite the result as if they did.

### D09 / MEDIUM / A/B/C — unequal scaffolding

C currently has more steps and prompts than A/B. Therefore richer C output cannot be interpreted as evidence that the mechanism is stronger.

Control in human testing:

- exposure time;
- amount of text;
- photo treatment / occlusion;
- number of facilitator prompts;
- optional/mandatory fields.

Record `facilitator_prompt_count`.

### D10 / MEDIUM / B + C — jargon barrier

Participant-facing language should use:

`我看到 / 别人告诉我 / 我猜 / 我还不知道`

rather than requiring research terms such as `推断 / 解释权 / 核验者`. Professional terminology remains in the research coding layer.

## Round 01 decision

- **B:** `KEEP BUT REWRITE INPUT SEQUENCE`.
- **C direction:** `KEEP AS RESEARCH DIRECTION`.
- **Current C participant UI:** `REJECT / REWRITE`.
- **C2:** `KEEP / TWO-STAGE BLIND COMPARISON REQUIRED`.

## Assumptions rejected

1. `participant produced a question = autonomous question` → rejected.
2. `participant answered an interpretation-right question = participant independently perceived governance` → rejected.
3. `C produced more text = C is more effective` → rejected.
4. `relational design direction is valid = current relational prompts are valid` → rejected.
5. `one real photo = spatial behavior evidence` → rejected.

## v0.2 principle

`free response → evidence separation → premise may be rejected → question may be absent → next step may be absent → researcher codes relational/governance variables after submission`

Participant-facing UI no longer uses `解释权`, `要求谁遵守什么`, or a mandatory `下一核验者`.

## Evidence boundary

- Simulated attack profiles: `EXECUTED AS DESIGN ADVERSARIAL TEST`.
- Human participant test: `NOT RUN`.
- 2026 current-site spatial behavior: `NOT VERIFIED`.
- Cultural-learning effect: `NOT CLAIMED`.
- C01 remains `RESEARCH + PROPOSAL / EVIDENCE REVIEW`.

Full simulated records and runnable v0.2 package are stored in the project evidence Drive under `PRAC-C01-TRANS-ABC-001/05_Adversarial-Sim`.