# OLEANDER AI Design Reasoning Protocol v0.2

- Status: ACTIVE reusable protocol / internally exercised / not a project validation result
- Canonical method body: Notion `01B｜OLEANDER AI 协同设计方法｜读取、反馈与验证`
- Method index: `MTH-AI-OLEANDER-001`
- Updated: 2026-08-07

> This file is a lightweight execution contract. It does not duplicate the full Canonical method narrative in Notion.

## Core loop
`Read → Frame → Hypothesize → Vary → Construct → Attack → Test → Decide → Archive`

## Input contract
Before design generation, provide:
1. Object / version
2. Context / users / medium / project stage
3. Evidence
4. Must / locked conditions
5. Variables allowed to change
6. Test target
7. Failure / stop condition
8. Truth state

If critical inputs are missing, the AI stays in reading/questioning/UNKNOWN rather than generating a final-looking proposal.

## Truth states
- `F` Verified Fact
- `S` Source Claim
- `J` Designer Judgment
- `I` AI Inference
- `H` Hypothesis
- `O` Observed Result
- `U` Unknown

Only an actually executed test can create `O`. Simulation, rendering or model scoring cannot independently promote H/I/U into verified fact.

## Nine execution gates
| Step | Required output | Gate |
| --- | --- | --- |
| READ | evidence ledger, contradictions, missing evidence, version differences | facts/claims/inferences/unknowns separated |
| FRAME | one core problem, ≤3 secondary tensions, locked/variable set, stop condition | no preselected form or vague style adjective |
| HYPOTHESIZE | falsifiable `if X → Y under Z, observed by M` statement | reality could disprove it |
| VARY | control + controlled variable matrix + extreme cases | change only 1–3 main variables per round |
| CONSTRUCT | reconstructable model/vector/component/parameter/detail/code/sample | measurable and repeatable |
| ATTACK | failure modes, misreadings, interface conflicts, deletion tests | risks become test tasks |
| TEST | observed result, scope, conditions, sample, anomalies, failures | actual test evidence exists; otherwise remain H/U |
| DECIDE | KEEP / REVISE / REJECT / HOLD + human rationale | responsible human decision recorded |
| ARCHIVE | version log, decision log, evidence links, next experiment | can answer why the design became this way |

## Adversarial checks added after Protocol Exercise 001
1. **Product-family existence ≠ current compliance.** An official manufacturer page can prove that a product family exists while its referenced standard, certificate version, factory, SKU or project applicability is stale or incomplete. Current compliance must be closed separately.
2. **Same category ≠ system compatibility.** Materials or components that all belong to “interior finish”, “CMF”, “structure” or another broad category must not be combined unless their substrate, process, interface, performance and installation logic are actually compatible.

These checks were exercised on the demountable compact-HPL wall workflow: they blocked an incorrect veneer/wood-finish component chain and kept a light-gauge steel subframe candidate on HOLD when its public product page referenced a superseded Chinese standard. This is an internal method exercise, not evidence that the wall system itself performs as intended.

## Return routes
- Test contradicts expectation → return to FRAME or HYPOTHESIZE.
- Multiple options fail at the same interface → reconsider system boundary before more styling.
- Evidence missing → return to READ.
- Variables contaminate each other → rebuild VARY controls.
- Safety, regulation or rights blocker → HOLD until the responsible real-world process closes it.
- Meaning exists only in explanatory copy → return to ATTACK / CONSTRUCT.

## Artifact maturity
- `A0` Prompt / Idea
- `A1` Representation
- `A2` Reconstructable
- `A3` Testable Prototype
- `A4` Evidence-backed Decision

A polished A1 render is not A3 or A4.

## Responsibility boundary
AI may retrieve, compare, cluster, construct parameter matrices, script, generate controlled variants, check conflicts, simulate readings, analyze failure modes, organize test data and archive decisions.

AI does **not** independently close bodily experience, real material appearance, structural/MEP safety, regulatory applicability, user behavior, manufacturing/construction feasibility, cultural rights/authorization, actual price/lead time, maintenance or operating performance.

## Minimum experiment record
`Experiment ID → Object/Version → Core Question → Hypothesis → Must/Locked Variables → Changed Variables → Evidence Inputs + Truth State → Constructed Artifact → Attack/Failure Modes → Test Method + Conditions → Observed Result → Unknowns → Human Decision → Decision Reason → Next Experiment → Evidence/File/Commit Links`

## Governance
- Notion `01B` remains the Canonical full method source.
- The Notion METHOD card is an index/pointer only.
- This GitHub file is the reusable lightweight execution contract.
- Real project evidence and dynamic decisions remain in Notion/project records; Drive stores actual files.