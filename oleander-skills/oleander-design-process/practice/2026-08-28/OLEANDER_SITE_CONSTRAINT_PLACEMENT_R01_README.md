# 2026-08-28｜Design Process / Spatial / L5｜Site Constraint → Placement + Orientation

STATUS: `TRAINING_MODE / PRACTICE_EVIDENCE / EXTERNAL-SOURCE-CALIBRATED / NO_PROJECT_USAGE / NO_PROMOTION`

## GAP
Recent DESIGN evidence already covers functional-allocation option space, design↔validation change control, and program→adjacency→massing. This run attacks a different boundary: **can site conditions change placement/orientation/access ownership before form polish, rather than remaining a separate site-analysis layer?**

## EXISTING-FIRST
Read from GitHub main:
- `oleander-skills/SKILL_REGISTRY_v1.1.json`
- `oleander-skills/REVIEW.md`
- `00-governance/OLEANDER_WORK_COORDINATION_CONTRACT_v1.0.md`
- `00-governance/OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT.json`
- `00-governance/OLEANDER_HUMAN_PROFESSIONAL_VOICE_POLICY_v1.0.md`
- `oleander-skills/oleander-design-process/SKILL.md`

Priority Queue is empty; Practice/Candidate frontier only. Repository search did not resolve files literally named `Current Owner Map` or `Capability Contract`; missing contract content is not inferred. Registry/REVIEW owner-routing authority remains controlling.

Recent relevant DESIGN evidence checked: PR #430 program→adjacency→massing; PR #428 functional-allocation option space; PR #425 interface change control.

## EXTERNAL DISCOVERY
### Source 1 — U.S. Department of Veterans Affairs, Site Design Manual PG 18-10
Institution: U.S. Department of Veterans Affairs, Office of Construction and Facilities Management  
Published: February 2013; Revision 2: March 1, 2024  
URL: https://www.wbdg.org/FFC/VA/VADEMAN/dm_site_03_2024.pdf  
Accessed: 2026-08-28

Professional delta used:
- pre-design records site opportunities/constraints and survey information;
- conceptual design locates a proposed facility relative to existing conditions;
- spacing may respond to functional relationships, operational efficiency, future expansion and open space;
- orientation is considered together with facility location and surrounding site functions.

### Source 2 — WBDG, Landscape Architecture and the Site Security Design Process
Institution: Whole Building Design Guide / National Institute of Building Sciences  
URL: https://www.wbdg.org/resources/landscape-architecture-and-site-security-design-process  
Accessed: 2026-08-28

Professional delta used at high level: access/circulation planning starts from how people and vehicles arrive; surrounding street/arrival patterns affect access-point placement and should be coordinated with the building.

### RIGHTS / NON-TRANSFER
Used only as factual professional references. No VA/WBDG figure, diagram, template, wording, brand identity or fixed numeric rule is copied. No endorsement is claimed.

Rejected from OLEANDER Current: VA-specific mandatory procedures; security/fire setbacks; solar-orientation angles; roadway/parking/accessibility dimensions; topographic grading rules; traffic-capacity thresholds; federal submittal procedures. These remain project/jurisdiction/discipline authority questions.

Existing OLEANDER already covers >60% (site/context analysis, Evidence→Finding→Design Consequence, massing/circulation, options, attack tests), so this run extends Practice evidence rather than creating a parallel Skill.

## DESIGN QUESTION / INPUTS / E-I-A-D
Synthetic object: community workshop. NTS.

Exercise assumptions:
- west edge = public arrival;
- east edge = service-road arrival;
- north-center grove = retained site condition;
- public arrival and delivery can occur simultaneously;
- dashed grove retain-zone is **exercise-only / NTS**, not a real arborist setback.

EVIDENCE: west/public, east/service, retained grove.  
INFERENCE: a centered object can create crossing and conflict with the retained site condition.  
ASSUMPTION / ADVERSE: public + delivery overlap; retain-zone remains unavailable for building placement in the exercise.  
DESIGN CONSEQUENCE: shift/orient the mass around the retained condition and separate public/service approach ownership.

No claim: real survey, topography, tree assessment/protection radius, grading/drainage, traffic, accessibility, fire/code, structure or site approval.

## ARTIFACT / OPTIONS
Editable: `OLEANDER_SITE_CONSTRAINT_PLACEMENT_R01.svg`

A / REJECT — **Centered Object**: central mass placed first; west/public and east/service then attach. The mass intrudes into the exercise retain-zone and approach fields cross.

B / KEEP candidate — **Shifted Bar + Two-sided Access**: mass moves south; grove remains in forecourt; public owns west edge and service owns east edge; approach lines do not share the same conflict field.

C / REVISE — **Courtyard Around Grove**: grove is retained centrally, but service still uses the shared circulation ring; viable only if service circulation gains an independent edge.

## A/B / ATTACK
1. `LABEL-OFF` — access ownership and retained-site geometry should survive labels.
2. `FACADE-OFF` — placement/circulation logic should survive removal of style credit.
3. `SIMULTANEOUS ARRIVAL` — public + delivery overlap; A/C keep shared conflict carriers, B separates approach ownership.
4. `GROVE / RETAIN-ZONE DELETION` — deleting the retained condition removes A's main placement conflict; confirms the consequence is tied to the exercise site input, not a universal preference for shifted bars.
5. `SERVICE-EDGE DELETION` — if east/service arrival disappears, B's two-sided access is no longer mandatory.
6. `GRAY50` — option logic must survive without hue.

## READBACK → FAILURE → REPAIR → RETEST
Readback 1: A's grove conflict could be read as merely adjacent because only canopy/mass overlap was visible.

Repair 1: added a dashed, explicitly NTS exercise retain-zone around the grove in all three options. A intrudes; B avoids; C encloses. No dimensional tree-protection rule was introduced.

Readback 2: the longer retain-zone legend collided with public/service legend keys.

Repair 2: moved public/service keys rightward without changing the option grammar.

Final retest: full-size PNG reopened after both repairs; no legend collision remains; A conflict, B separated access ownership and C shared-ring conflict remain visible. Gray50 retains the same option distinction.

## PROFESSIONAL CRIT
First read: PASS after repairs.  
Option differentiation: PASS.  
Site→placement causality: PASS for synthetic Practice.  
Label/surface independence: PASS.  
Adverse-condition clarity: PASS.  
Architecture/site technical validity: HOLD.  
Independent professional review: HOLD.

## ROOT CAUSE
`SITE ANALYSIS EXISTENCE ≠ SITE-RESPONSIVE PLACEMENT`

A project can contain a correct site-analysis diagram while the building placement remains unaffected by the conditions it describes. A site condition also cannot function as design evidence when its spatial boundary is too ambiguous to show whether an option conflicts with it.

## TRANSFER RULE
Bounded Practice claim:

> Before giving credit to architectural form, remove facade styling and labels. A material site constraint or arrival relationship should leave a visible consequence in placement, orientation, access ownership or open-space structure.

If deleting the site condition leaves the design unchanged, the claimed site analysis may be descriptive rather than generative.

This is not a universal claim that buildings should shift south, orient east–west, use circular tree-retain zones or separate public/service access in every project.

## BOUNDARY / STATUS
Applicable to early site planning, architecture/landscape massing, campus/service-cluster placement and site-condition option comparison.

Not sufficient for survey truth, tree-protection requirements, grading/drainage, solar/wind optimization, traffic engineering, fire/accessibility/code, security planning, structure or final site approval.

Status remains `PRACTICE_EVIDENCE / EXTERNAL-SOURCE-CALIBRATED`.

No `PROJECT_USAGE_EVIDENCE`, `VALIDATED_CANDIDATE` or `ACTIVE` claim. Under NO-CHURN, no Current Skill body change is proposed; the existing Candidate already owns site/context analysis, massing and circulation.
