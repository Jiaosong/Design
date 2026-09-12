# 2026-08-29｜Design Process / Product / L5｜Repairability → Disassembly Architecture

STATUS: `TRAINING_MODE / PRACTICE_EVIDENCE / SUPPORT / SCOPED / UNVERIFIED / NO_PROJECT_USAGE / NO_PROMOTION`

## GAP
Recent DESIGN Practice covered situated orientation media, program→massing and functional-allocation option space. This run attacks a different product boundary: whether **repairability/maintenance intent changes enclosure, fastener access and component dependency** before finish and service copy are credited.

## KNOWLEDGE READ STATE
Read in Current order:
- Notion root Current Authority;
- `OLEANDER Knowledge Retrieval & Lifecycle｜知识库机制 v1.0`;
- GitHub main Skill Registry / REVIEW / Work Coordination / Priority Queue / Human Professional Voice;
- current `oleander-design-process` Candidate boundary.

Current Priority Queue contains `PRJ-C04-DIGITAL-INTERACTION` with `PRESENTATION` as Current Owner. DESIGN therefore remains in `TRAINING_MODE` and does not mutate that object.

No K06 / chronology / Legacy / Snapshot carrier is used as authority.

## EXTERNAL DISCOVERY
### Source A
European Commission — Smartphones and Tablets / Ecodesign Requirements  
https://energy-efficient-products.ec.europa.eu/product-list/smartphones-and-tablets_en  
Accessed 2026-08-29.  
Material delta: current EU ecodesign explicitly includes disassembly/repair and spare-part obligations for covered products.

### Source B
EUR-Lex — Commission Regulation (EU) 2023/1670, 16 June 2023  
https://eur-lex.europa.eu/eli/reg/2023/1670/oj  
Official Journal L 214, 31.8.2023; current consolidated version indicated from 20.6.2025.  
Material delta: Annex II includes design-for-repair/reuse provisions, spare-part availability and required fasteners for covered mobile devices.

### Source C
EUR-Lex — Regulation (EU) 2024/1781 (ESPR)  
https://eur-lex.europa.eu/eli/reg/2024/1781/oj  
Material delta: repairability and maintenance/refurbishment are product parameters; impeded disassembly of key components is explicitly named as a potential cause of premature obsolescence.

### Rights / license boundary
Official EU legal and Commission sources are used as factual regulatory references. No Commission/EU visual identity, template, diagram or fixed product geometry is copied. The exercise does not claim legal compliance.

## CAPABILITY MAPPING / COMPARE WITH CURRENT
Existing `oleander-design-process` already covers >60%:
- requirement→function→part role→form/structure/material/interaction;
- form proof before finish;
- options/deletion/adverse-condition tests;
- Validation handoff.

External sources add a bounded missing emphasis:
**repairability is not merely after-sales information; access, disassembly and fastener/component boundaries are design consequences.**

Decision: `EXTEND/COMPOSE through Practice evidence`; no parallel Skill.

Rejected / not transferred:
- universal ban on adhesive;
- universal screw count/type;
- smartphone-specific spare-parts list as a rule for all products;
- regulatory times, repairability scoring, tool classes or compliance thresholds;
- any sealing, IP-rating, electrical-safety or battery-service claim not validated for the synthetic object.

## DESIGN QUESTION / INPUTS / CONSTRAINTS / E-I-A-D
Synthetic object: handheld rechargeable device.

Question:
If the battery or charge port fails, can each target part be reached and reassembled without first disturbing unrelated serviceable components?

Inputs:
- battery module;
- charging port;
- enclosure;
- fasteners/access panels.

Constraints:
- no dimensions;
- no actual mechanism;
- no sealing/IP claim;
- no thermal/electrical/safety/manufacturing validation.

EVIDENCE:
External ecodesign sources treat disassembly, repairability, spare-part access and fasteners as resource-efficiency concerns for covered products.

INFERENCE:
A repair requirement is weak when the target component is buried behind destructive or unrelated disassembly.

ADVERSE:
battery failure / port failure / required reassembly.

DESIGN CONSEQUENCE:
separate service zones; expose reusable mechanical access; avoid trapping one service action behind another.

## ARTIFACT / OPTIONS
Editable:
- `OLEANDER_REPAIRABILITY_DISASSEMBLY_ARCHITECTURE_R01.svg`

Rendered readback:
- full-size PNG;
- 50% Gray50 PNG.

### A / REJECT — Sealed Stack
Continuous rear enclosure with destructive perimeter bond. Port replacement requires passing through battery/board stack.

### B / KEEP candidate — Service-zoned Access
Battery and port have separate access zones. Reusable mechanical access is visible; neither target part depends on removal of the other in the exercise architecture.

### C / REVISE — Removable Cover, Trapped Part
The shell opens, but the charging port remains under the battery carrier. This proves `openable shell ≠ repairable component architecture`.

## A/B / ATTACK
1. `TARGET-PART TRACE`: list only parts/fasteners disturbed before target removal and reassembly.
2. `FASTENER-OFF`: remove mechanical access from B; repair path degrades.
3. `PORT FAILURE`: A/C reveal unrelated battery dependency.
4. `REASSEMBLY`: destructive access becomes a second dependency.
5. `COVER-OFF`: C remains problematic after the cover itself is removed.
6. `GRAY50`: access zones remain distinct without hue.

## ACTUAL READBACK / FAILURE / ROOT CAUSE
First full-size readback found a real representation failure:
- the top External Evidence text crossed into the Inference column;
- the evidence band therefore undermined the exact separation it was trying to teach.

Repair:
- shortened the external-source summary;
- shifted the Inference / Adverse / Consequence column starts;
- regenerated full-size and Gray50.

Retest:
- no text collision remains;
- A/B/C remain distinct;
- B service zones survive Gray50;
- no regulatory-compliance statement appears.

## PROFESSIONAL CRIT
- first read: PASS after repair;
- option differentiation: PASS;
- repairability→architecture causality: PASS for bounded Practice;
- counterexample quality: PASS (C);
- grayscale: PASS;
- mechanism/sealing/safety validity: HOLD;
- regulatory compliance: HOLD;
- independent professional review: HOLD.

## TRANSFER RULE
Bounded Practice claim:

`SERVICEABLE PART → REQUIRED ACCESS → DISASSEMBLY DEPENDENCIES → FASTENER / ENCLOSURE BOUNDARY → REASSEMBLY PATH`

Before calling a physical product “repairable” at design-process level, trace a named target part. If unrelated serviceable parts or destructive access must be disturbed first, record that dependency as design debt rather than hiding it behind finish or service copy.

This is not a universal regulation, fastener prescription or adhesive prohibition.

## BOUNDARY
Applicable to:
- handheld devices;
- appliances;
- serviceable product enclosures;
- modular controls;
- replaceable wear-part systems;
- early product architecture before industrialization.

Not sufficient for:
- legal compliance;
- ingress protection;
- battery safety;
- electrical safety;
- thermal design;
- structural integrity;
- manufacturing approval;
- repair-time scoring;
- proprietary-tool policy.

## KNOWLEDGE WRITE HANDOFF
Write state:
`PRACTICE_EVIDENCE / SUPPORT / SCOPED / UNVERIFIED`.

Suggested Existing Owner:
`oleander-design-process` / product-form reasoning.

Relations for KNOWLEDGE closure:
- Source: European Commission product ecodesign page; EU 2023/1670; EU 2024/1781.
- Domain: design process / product architecture / repairability.
- Method: `oleander-design-process`.
- Evidence: editable SVG + PNG/Gray50 readback + repair record.
- Freshness: official web sources accessed 2026-08-29.
- Trust: `UNVERIFIED`.
- Project relation: none.

Do not promote to Current Rule. KNOWLEDGE owns Migration Closure / Relation Closure.

## STATUS
`PRACTICE_EVIDENCE / EXTERNAL-SOURCE-CALIBRATED / UNVERIFIED`

No `PROJECT_USAGE_EVIDENCE`, `VALIDATED_CANDIDATE`, or `ACTIVE`.
