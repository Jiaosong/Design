# OLEANDER Professional Research Gate v0.1

Status: extension of existing `oleander-research`; not a new Authority, Method family, taxonomy, Registry, Project State, or parallel research system.

> **Current binding:** this research-specific gate is retained for backward compatibility and detailed R0–R11 research execution. For formal professional research/knowledge content, it operates under `PROFESSIONAL_KNOWLEDGE_CONTENT_RESEARCH_STANDARD_v1.0.md`, which separates `R1 Research Conduct`, `R2 Study-Type Reporting`, `K1–K5 Knowledge`, `B1 Bilingual Semantic Parity`, and Independent Review. `R2 PASS` never grants `R1 PASS`, and research/content/knowledge-object/current states remain independent.

## Purpose

Convert research from “traceable source collection” into a professional, decision-grade process whose search scope, appraisal, synthesis, uncertainty, reproducibility, ethics, and design transfer can be audited.

This gate applies before a research result is allowed to support a consequential OLEANDER design, technical, strategy, safety, material, spatial, service, UX, accessibility, environmental, or governance decision.

It does **not** make every task a systematic review. Research depth must be proportional to consequence, uncertainty, reversibility, novelty, and cost of error.

## Research depth classes

Use the minimum sufficient class and name it explicitly.

- `RDC-0 ORIENTATION`: bounded orientation / terminology / landscape scan. No claim of completeness.
- `RDC-1 TARGETED REVIEW`: decision-specific search across the strongest relevant source classes. Default for most project research.
- `RDC-2 STRUCTURED EVIDENCE REVIEW`: predeclared search logic, inclusion/exclusion criteria, extraction matrix, contradiction handling, and explicit coverage limits.
- `RDC-3 SYSTEMATIC / SCOPING REVIEW`: only when the task actually follows an appropriate review protocol and reporting standard. Do not call ordinary web research “systematic”.
- `RDC-4 EMPIRICAL STUDY`: primary observation, interview, survey, experiment, field measurement, usability test, simulation-validation study, or other original data generation with an explicit protocol.

Escalate depth when one or more apply: life/safety consequence, irreversible or high-cost decision, regulation/compliance, strong stakeholder conflict, uncertain field condition, causal claim, quantitative performance target, human-subject claim, new material/process, major capital intervention, or weak/contradictory prior evidence.

## R0 — Authority and decision framing

Before searching, record:

- Current Authority / Project State / Source Authority / Current Task;
- exact research question;
- exact decision or design variable the research can change;
- domain(s), geography, population/user group, asset/system, and time horizon;
- required confidence and consequence of being wrong;
- known constraints and already accepted facts;
- current uncertainty / evidence gap;
- research depth class;
- stop condition: what evidence is sufficient to make, defer, or reject the decision.

Hard rule: a vague theme such as “research good museums” or “study materials” is not a valid professional research question until it is tied to a decision.

## R1 — Protocol before evidence accumulation

For `RDC-1+`, define a compact protocol before large-scale retrieval:

- question and decision;
- intended claims / variables;
- source classes to search;
- databases / repositories / official sites / standards bodies / manufacturer or studio sources as relevant;
- search terms and important synonyms when retrieval coverage matters;
- inclusion criteria;
- exclusion criteria;
- geographic / temporal limits;
- language limits if any;
- minimum source-strength expectations;
- treatment of grey literature, vendor evidence, precedent evidence, and secondary reporting;
- conflict-of-interest / sponsorship concerns;
- extraction fields;
- synthesis method;
- uncertainty method;
- planned validation / field check / prototype check;
- update trigger or staleness horizon.

Protocol changes after seeing evidence must be recorded as amendments with a reason. Do not silently redefine the question to fit the sources found.

## R2 — Search coverage and source routing

Search by claim type, not by one habitual source channel.

Default source ladder:

1. law / regulation / official code / current standard when the claim is normative;
2. original dataset / primary research / official technical documentation / patent / test report when the claim is empirical or technical;
3. current systematic review / consensus guideline / authoritative synthesis when appropriate;
4. original project / studio / manufacturer / institution source for precedent, implementation, or product facts;
5. high-quality secondary literature for context and triangulation;
6. curated media, award sites, forums, social posts, reposts, and image boards only as discovery or weak contextual evidence unless independently verified.

The ladder is **claim-dependent**, not universal. A manufacturer datasheet may be strongest for product dimensions but weak for independent performance comparison. An award page may be useful for authorship discovery but weak for causal design claims.

Search must include, when material:

- positive evidence;
- contradictory evidence;
- failure cases / recalls / post-occupancy problems / known limitations;
- competing methods or products;
- out-of-region or adjacent-domain evidence only with an explicit transferability check.

## R3 — Source appraisal

Every source used for a consequential claim must be appraised on at least:

- `authority`: who produced it and what authority/expertise they have;
- `originality`: primary/original vs secondary/reported;
- `method transparency`: can the method/data basis be understood;
- `directness`: how directly it addresses the current question;
- `recency`: whether the date matters and whether the source is stale;
- `geographic/context fit`;
- `sample / measurement / study-design adequacy` when applicable;
- `bias / sponsorship / conflict of interest`;
- `reproducibility / inspectability`;
- `consistency` with other strong evidence;
- `applicability boundary`;
- `source strength`: `STRONG / MODERATE / WEAK / DISCOVERY ONLY`.

Source strength is not claim confidence. Several weak sources do not automatically become strong evidence by quantity.

## R4 — Evidence extraction and provenance

For each material claim, preserve enough information for another reviewer to reconstruct the chain:

- claim ID;
- exact claim;
- source ID / citation / stable URL or file reference;
- author / organization;
- publication/version date;
- access date when relevant;
- source type;
- geography / population / system;
- method / sample / instrument where relevant;
- extracted fact, value, quote fragment, figure, table, or observation location;
- unit and measurement condition for quantitative evidence;
- source strength;
- limitation / bias;
- evidence state: `FACT / INTERPRETATION / ASSUMPTION / UNKNOWN`;
- applicability to current project;
- reviewer confidence.

No unsupported quantitative claim. No numerical value without unit, condition, and source when those materially affect interpretation.

## R5 — Synthesis, contradiction, and negative evidence

Do not summarize sources as a list. Synthesize by claim or decision variable.

For every consequential question, state:

- where evidence converges;
- where it conflicts;
- whether conflict is explained by population, geography, era, method, scale, material, operating condition, or measurement differences;
- what evidence is missing;
- what would falsify the current interpretation;
- whether a decision remains robust under the strongest credible counter-evidence.

Use a contradiction register when strong sources disagree. Never delete inconvenient evidence merely to make the narrative cleaner.

When an absence claim matters (“no evidence”, “no precedent”, “no requirement”), state the actual search coverage. Failure to find something is not proof of nonexistence.

## R6 — Claim confidence and uncertainty

Assign confidence to **claims**, not entire documents.

Default claim confidence:

- `HIGH`: multiple strong, direct, mutually consistent sources or high-quality direct measurement; major limitations unlikely to reverse the conclusion.
- `MODERATE`: useful direct evidence with one or more material limitations or limited triangulation.
- `LOW`: indirect, weak, sparse, dated, context-mismatched, or conflicting evidence.
- `INSUFFICIENT`: evidence cannot support the proposed decision.

Also record the dominant uncertainty type when relevant:

- measurement uncertainty;
- sampling uncertainty;
- model uncertainty;
- causal uncertainty;
- transferability uncertainty;
- temporal/staleness uncertainty;
- field-condition uncertainty;
- implementation uncertainty.

Do not convert `LOW` or `INSUFFICIENT` confidence into a confident design fact. Route it to reversible design, prototype, field verification, simulation, expert review, or HOLD as appropriate.

## R7 — Evidence-to-design translation

Professional research is complete only when the evidence chain reaches a project decision without erasing uncertainty.

Use:

`RESEARCH QUESTION → EVIDENCE → APPRAISAL → SYNTHESIS → CLAIM CONFIDENCE → APPLICABILITY → DESIGN IMPLICATION → DECISION / TEST → READBACK`

Every major design implication must declare whether it is:

- `REQUIREMENT`: externally binding or demonstrably necessary;
- `CONSTRAINT`: condition that limits viable options;
- `OPPORTUNITY`: evidence-supported direction worth testing;
- `HYPOTHESIS`: design proposition requiring validation;
- `REFERENCE MOVE`: precedent mechanism, not proof;
- `FIELD OPEN`: cannot be closed without site/user/physical verification.

Do not let a precedent image, benchmark, or studio statement become a technical requirement without independent support.

## R8 — Primary / human / field research controls

When research creates new data (`RDC-4`), add the domain-appropriate protocol before collection.

Minimum controls where applicable:

- participant / site / sample selection logic;
- inclusion/exclusion logic;
- informed consent / privacy / confidentiality;
- data minimization;
- vulnerable-group and accessibility considerations;
- interview / observation guide;
- instrument calibration / validity;
- task and scenario definition;
- confounds and competing explanations;
- stopping rule / saturation logic where suitable;
- adverse event / safety procedure;
- recording and anonymization method;
- analysis method defined before interpretive cherry-picking;
- raw-data provenance and retention;
- explicit distinction between observation and interpretation.

OLEANDER does not claim formal institutional ethics approval when none exists. Where regulated or institutional ethics review is required, that external approval remains an external gate.

## R9 — Reproducibility and research data management

A consequential research result should be reconstructable from its evidence package.

Preserve, as applicable:

- protocol and amendments;
- search strings / source routes;
- inclusion/exclusion decisions;
- evidence matrix;
- raw or minimally processed data references;
- transformation / calculation steps;
- analysis code or formulas;
- software / model / version information;
- units and coordinate reference systems;
- file hashes for critical evidence assets;
- decision log;
- readback result;
- permissions / licenses / access restrictions when relevant.

Research data and metadata should be findable, accessible under appropriate permissions, interoperable enough for the intended workflow, and reusable with provenance. FAIR is a data-stewardship principle, not proof that the underlying evidence is true.

## R10 — Professional Research Gate decision

The research package receives one state:

- `RESEARCH PASS`: question, protocol, source coverage, appraisal, synthesis, confidence, provenance, and decision transfer are sufficient for the stated consequence.
- `RESEARCH REVISE`: the question is answerable but a material methodological gap must be repaired.
- `RESEARCH HOLD`: external evidence, field data, expert input, permission, standard text, or other dependency is required before a defensible decision.
- `RESEARCH REJECT`: the research design, evidence basis, or claim structure is fundamentally invalid for the intended use.

Hard FAIL / non-PASS conditions include:

- calling a search systematic without a systematic method;
- using search ranking or source popularity as evidence quality;
- no decision question;
- consequential claim without traceable evidence;
- major contradiction hidden or omitted;
- unsupported causal inference;
- quantitative claim without source/unit/condition;
- vendor/marketing claim presented as independent proof;
- precedent similarity presented as performance proof;
- no uncertainty statement where uncertainty is material;
- primary human/field data collected without an appropriate protocol;
- analysis cannot be reconstructed from retained evidence;
- evidence is stale for a time-sensitive decision and has not been revalidated.

## R11 — Update and staleness control

Research is not permanently current.

Set an update trigger based on the domain:

- new law / code / standard / official guidance;
- product or software version change;
- new site survey / field measurement;
- changed project scope or decision;
- new high-quality contradictory evidence;
- time-based expiry for rapidly changing subjects;
- post-occupancy / prototype / testing evidence that materially changes the claim.

When the trigger fires, revalidate affected claims and downstream decisions rather than rewriting the entire research package by default.

## Required research outputs

For `RDC-1+`, the minimum output is:

1. Research question + decision linkage;
2. research depth class and protocol summary;
3. source/evidence table;
4. source-strength appraisal;
5. claim-evidence matrix;
6. contradiction / limitation / gap register;
7. claim confidence + uncertainty;
8. design implications and explicit applicability boundaries;
9. open questions / field checks / validation actions;
10. provenance / reproducibility record;
11. final `RESEARCH PASS / REVISE / HOLD / REJECT`.

## Professional standards used as calibration, not wholesale domain substitution

This extension is calibrated against current professional research principles from:

- PRISMA 2020: transparent reporting of systematic reviews and explicit review flow/checklists — https://www.prisma-statement.org/prisma-2020
- EQUATOR Network: choose study/reporting guidance appropriate to research design rather than one generic checklist — https://www.equator-network.org/reporting-guidelines/
- UK Research Integrity Office, Code of Practice for Research v3.5: integrity, data management, transparent methods, conflicts, and responsible use of emerging technologies — https://ukrio.org/ukrio-resources/publications/code-of-practice-for-research/
- National Academies, Reproducibility and Replicability in Science: transparent computational steps, data, methods, and conditions for reproducibility — https://nap.nationalacademies.org/catalog/25303/reproducibility-and-replicability-in-science
- FAIR Guiding Principles: findable, accessible, interoperable, reusable research objects with provenance and domain standards — https://www.go-fair.org/fair-principles/
- ISO 9241-210:2019: human-centred design activities integrated through the lifecycle for interactive systems; use when the research concerns human-system interaction — https://www.iso.org/standard/77520.html

These sources calibrate rigor and transparency. OLEANDER must still use the correct discipline-specific standard, code, reporting guideline, experimental method, or ethics requirement for the actual research question.

## Integration with existing OLEANDER flow

The existing Full Flow remains unchanged, but research now expands internally as:

`READ → REUSE → DEFINE → [R0–R1 FRAME/PROTOCOL] → BENCHMARK / SEARCH → [R2–R4 RETRIEVE/APPRAISE/EXTRACT] → [R5–R6 SYNTHESIZE/CONFIDENCE] → MAKE / TEST → [R7–R9 TRANSLATE/VALIDATE/REPRODUCE] → JUDGE → [R10 RESEARCH GATE] → REPAIR → RETEST → DISTILL → UPDATE → REAPPLY → [R11 STALENESS CONTROL] → REGRESSION-PROTECT → FLOW COMPLETION`

Professional Research PASS is evidence that the research process is decision-grade for its declared scope. It does **not** by itself prove Professional Design PASS, field truth, construction readiness, regulatory approval, or final project validity.
