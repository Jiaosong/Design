# Protocol Exercise 002｜OLEANDER Website Governance Sync

- Protocol: `OLEANDER AI Design Reasoning Protocol v0.2`
- Object: website governance-sync branch / PR #7
- Date: 2026-08-07
- Canonical content authority: Notion `00｜OLEANDER／织作｜命名与四层架构迁移基线` + website project pages
- Current maturity: **A3 / TESTABLE PROTOTYPE — automated-browser scope only**
- Release maturity: **NOT A4 / HOLD**

## Core question
Can the website become a reconstructable and automated-browser-tested implementation of the current OLEANDER governance model without converting unexecuted tests, unresolved rights, or placeholder contact infrastructure into public facts?

## READ
Current `main` still exposes legacy and unsupported content such as `Project 01–03`, `Academic / Prototyped / Tested`, numerical test results, and `hello@example.com`. PR #7 replaces most of these with C01/C02/C03, current case states, explicit test plans and unpublished-contact language.

Canonical case states:
- C01: `RESEARCH + PROPOSAL / EVIDENCE REVIEW`.
- C02: `INDEPENDENT PORTFOLIO / PROTOTYPED / TEST PLANNED / NOT RUN`.
- C03: `PORTFOLIO CONCEPT / VISUALIZED / SAMPLE TEST PENDING`; no OPPO commission, adoption, production or endorsement claim.

## FRAME
Locked:
- C01/C02/C03 are the only current-facing case IDs.
- Unexecuted tests cannot create participant results, VERIFIED status or performance evidence.
- Contact remains prototype-only until a real backend, verified address and privacy workflow exist.
- E2 automation cannot close E3 human/assistive-technology/device checks or rights/provenance.

Variable:
- wording, status labels, ARIA/interaction implementation and test infrastructure.

Stop/HOLD conditions:
- unsupported result language remains;
- E3 is not executed;
- website asset rights/provenance remain incomplete;
- real contact/privacy path is incomplete.

## CONSTRUCT
PR #7 is reconstructable source code and includes:
- HTML/CSS/JavaScript website implementation;
- keyboard/ARIA/reduced-motion/reflow fixes;
- Playwright + axe browser test infrastructure;
- C01/C02/C03 governance rewrite;
- placeholder-contact removal.

This satisfies **A2 / Reconstructable**.

## TEST｜2026-08-07
GitHub Actions run `Website quality` / run 31157266314 completed successfully:
- `e1-static`: PASS.
- `e2-browser`: PASS, including `npm run test:e2` after Chromium/Firefox/WebKit installation.

Within this automated-browser scope, the branch advances to **A3 / Testable Prototype**.

This does **not** establish A4 because E3 and rights/release evidence remain open.

## ATTACK｜remaining semantic blockers
Two content-level contradictions remain after the automated pass:

1. `website/index.html` C01 reflection still states that “多数参与者只把互动理解为个性化图案生成……”. The same branch correctly marks the C01 tests as `TEST PLAN / NOT RUN`. Unless a traceable historical test record is recovered, this result-like sentence must be rewritten as a failure hypothesis/risk rather than participant evidence.
2. `website/script.js` intended-state evidence label still reads `原型测试 + 设计假设`, while its detail correctly says the test is planned and not run. The label should become `测试计划 + 设计假设` or equivalent.

Additional review item:
- the project-practice matrix uses `Supported` in the Test column for cases whose formal testing is not run/pending. This should be audited against the canonical case states before release.

Automated tests passing cannot override these semantic evidence conflicts.

## A2 → A3 → A4 decision
- **A2: ACHIEVED** — versioned, reconstructable source exists.
- **A3: ACHIEVED WITH SCOPE** — automated E1/E2 browser checks passed for PR #7.
- **A4: HOLD** — requires semantic blockers closed, E3 human/assistive-tech/device evidence, real contact/privacy path as applicable, asset rights/provenance review, and a human release decision.

## Next actions
1. Resolve the three semantic evidence items above on PR #7.
2. Re-run Website quality and retain the run link/commit SHA.
3. Execute E3: keyboard + screen reader, real 200% zoom/reflow, physical-device touch, reading-rhythm review and target-platform font QA.
4. Complete rights/provenance for public assets.
5. Only then make a human `READY / MERGE / RELEASE` decision.

## Governance rule learned
**Automated technical success is evidence about implementation behavior, not evidence that narrative claims are true.** Content truth and technical correctness are independent gates.