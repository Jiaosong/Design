# OLEANDER Existing Mature Knowledge Base First Policy v1.0

Status: ACTIVE  
Scope: ALL OLEANDER knowledge supplementation / research / training / Stage 03 / L4–L7 enrichment  
Companion policy: `OLEANDER_EXISTING_MATURE_DESIGN_FIRST_POLICY_v1.0.md`

## 1. Core rule

> **补充知识时，优先从市场上已经存在、结构成熟、来源可追溯的知识库中消化，而不是从零发明；一次只消化一个知识库中的一个主题/对象，完成写入与 readback 后再进入下一个。**

Default order:

`CURRENT OLEANDER → EXISTING MATURE EXTERNAL KNOWLEDGE BASE → ORIGINAL / PRIMARY SOURCE → TARGETED WEB RESEARCH → NET-NEW SYNTHESIS ONLY FOR THE REMAINING GAP`

A mature external knowledge base is an input source, not a replacement taxonomy and not a new Current Authority.

## 2. What counts as a mature knowledge base

Prefer structured sources with stable provenance, versioning, identifiable authorship/ownership and repeatable retrieval, including when legally accessible:

- standards and code databases;
- professional institutions and technical handbooks;
- manufacturer technical libraries, product selectors, BIM/specification libraries and engineering documentation centers;
- material databases and environmental/product declaration libraries;
- academic journal/book platforms and research repositories;
- museum, archive and design-history collections;
- established design-method/toolkit libraries;
- mature commercial knowledge platforms with identifiable source chains.

Random blog posts, SEO summaries, anonymous aggregators and AI-generated summaries are not first-line knowledge bases.

## 3. Source priority inside one topic

When sources disagree, use this order unless a domain-specific authority contract says otherwise:

`CURRENT LAW / STANDARD / PRIMARY RECORD → OFFICIAL ORIGINAL SOURCE → MATURE KNOWLEDGE-BASE INTERPRETATION → REPUTABLE SECONDARY SOURCE → COMMUNITY / WEB DISCUSSION → AI SYNTHESIS`

A knowledge base may help locate and structure evidence, but it may not overrule a more authoritative primary source.

## 4. Mandatory one-by-one digestion loop

Every supplementation run uses this loop:

`ONE KNOWLEDGE BASE → ONE TOPIC / OBJECT → READ → MAP → DEDUP → DIGEST → WRITE → READBACK → CLOSE → NEXT`

### KB-01｜Locate and qualify the knowledge base
Record:
- name / owner;
- URL or stable access path;
- scope;
- current version/date when available;
- source type;
- rights/access boundary;
- why it is useful to an existing OLEANDER gap.

### KB-02｜Read its structure before extracting content
Understand its taxonomy, object types, metadata, evidence depth, update cadence and internal source chain.

Do not copy its taxonomy into OLEANDER by default.

### KB-03｜Deduplicate against Current OLEANDER
Before creating anything new, search for an existing Canonical L4/L5/L6 object.

Priority:

`UPDATE EXISTING → ADD RELATION / EVIDENCE → SPLIT ONLY IF SEMANTICALLY NECESSARY → CREATE NEW ONLY WHEN NO VALID CURRENT OBJECT EXISTS`

### KB-04｜Select one topic/object only
Do not batch-ingest a whole library.

One object may be a method, standard, material system, product family, case, designer, movement, technical detail, dataset or other bounded knowledge unit.

### KB-05｜Digest, do not clone
For the selected object extract only what changes OLEANDER understanding:
- factual claims;
- relationships;
- constraints and boundary conditions;
- failure modes;
- version/current-state information;
- source/provenance;
- contradictions;
- reusable design/engineering implication;
- unresolved UNKNOWN.

Keep `F / I / H / U` separated where applicable.

### KB-06｜Integrate into Current structure
Write to the valid Current Canonical target using existing Domain / L0–L7 architecture and Application Mapping.

External category labels remain source metadata unless OLEANDER independently adopts them.

### KB-07｜Attach a validation or practice consequence
Knowledge is not considered fully digested if it only produces a summary.

Where relevant, add at least one of:
- design practice;
- calculation/check;
- comparison;
- prototype;
- system interface test;
- failure-seeking scenario;
- real-use / field / human readback plan.

### KB-08｜Independent readback
After writing, re-fetch the Current object and verify:
- correct Canonical target;
- no duplicate page/object;
- source relation preserved;
- no accidental overwrite;
- material delta exists;
- UNKNOWN remains open where evidence is absent.

### KB-09｜Close before moving on
Only after `INTEGRATED + READBACK PASS` may the next topic/object from that knowledge base begin.

Do not leave dozens of half-digested placeholders.

## 5. Digestion status

Use the following operational states when tracking a source library:

`QUEUED → SCOPED → DIGESTING → INTEGRATED → READBACK PASS → COMPLETE`

Optional exception states:

`HOLD / RIGHTS-LIMITED / ACCESS-LIMITED / SUPERSEDED / NOT-USEFUL`

## 6. No bulk pollution rule

The following are prohibited by default:

- bulk scraping/importing a knowledge base into Notion or GitHub;
- creating one page per source item without semantic need;
- importing an external taxonomy as a parallel OLEANDER taxonomy;
- copying long proprietary text instead of extracting bounded knowledge;
- copying product catalogs without system relevance;
- creating duplicates because an external platform uses a different name;
- using knowledge-base completeness as a reason to reduce OLEANDER quality review;
- filling UNKNOWN with AI inference because the library is incomplete.

## 7. Rights and commercial knowledge bases

Commercial or paywalled knowledge bases may be used only within lawful access and citation/summary limits.

OLEANDER should preserve:
- source identity;
- access date/version;
- link/reference;
- rights/access limitation;
- extracted factual delta.

Do not mirror proprietary databases wholesale into OLEANDER.

## 8. Recommended source classes by knowledge type

Examples only; availability and authority must be checked each time.

- **Engineering / standards:** national standards databases, ISO/IEC, ASHRAE, CIBSE, NFPA, professional engineering bodies.
- **Products / construction / BIM:** manufacturer technical centers, NBS Source, BIMobject, ARCAT and equivalent specification libraries.
- **Materials / sustainability:** manufacturer EPD/TDS libraries, recognized material databases, EPD/program-operator libraries and material research platforms.
- **Design methods / UX / service:** Design Council, IDEO, Microsoft Inclusive Design, Nielsen Norman Group, established method/toolkit libraries and research institutions.
- **Design history / objects:** MoMA, Cooper Hewitt, V&A, CCA, museum archives, institutional collections and catalogues raisonnés.
- **Academic research:** peer-reviewed journal/book databases and institutional repositories; search engines are locators, not authority by themselves.

## 9. Queue priority rule

Choose the next external knowledge base by:

`CURRENT PROJECT / KNOWLEDGE GAP VALUE → SOURCE MATURITY → PRIMARY-SOURCE DEPTH → COVERAGE → UPDATE FRESHNESS → ACCESS / RIGHTS FEASIBILITY`

Do not prioritize novelty, trendiness or number of available pages.

## 10. Relationship to Existing Mature Design First

The two policies are cumulative:

- **Existing Mature Design First** prevents OLEANDER from rebuilding already-solved design work from zero.
- **Existing Mature Knowledge Base First** prevents OLEANDER from rebuilding already-structured knowledge from zero.

Together the default becomes:

`READ WHAT ALREADY EXISTS → VERIFY CURRENT AUTHORITY → DIGEST ONLY THE USEFUL DELTA → INTEGRATE WITHOUT DUPLICATION → VALIDATE → THEN ADD THE TRUE GAP`

## 11. Runtime guard

Before any new knowledge supplementation, answer:

1. Which Current OLEANDER object already covers this topic?
2. Which mature external knowledge base already structures this field?
3. Which one topic/object are we digesting now?
4. What material delta will enter OLEANDER?
5. What must remain UNKNOWN?
6. Has the write been independently read back?

If answers 1–3 are missing, do not begin bulk new-knowledge production.
