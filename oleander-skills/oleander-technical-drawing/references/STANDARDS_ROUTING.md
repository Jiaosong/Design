# OLEANDER Technical Drawing — Standards & Jurisdiction Routing

This file prevents generic drafting conventions from being mistaken for project compliance.

## 1. Separate four standard domains

Before citing a standard, classify it:

1. **Drawing representation/documentation** — line types, views, sections, dimensions, title blocks, document fields.
2. **Engineering/design** — structural, mechanical, electrical, drainage, material, tolerancing, etc.
3. **Safety/accessibility/code** — public safety, accessibility, fire, egress, barriers, stairs, ramps and jurisdiction-specific rules.
4. **Manufacturing/product definition** — GD&T, product definition, process, inspection and supplier/manufacturer requirements.

A drawing-representation standard does not prove engineering/safety compliance.

## 2. Jurisdiction resolver

Before any compliance claim, record:

- project country/region/city when relevant;
- discipline;
- project stage/status;
- responsible authority or client standard;
- applicable national/local code family;
- current standard number + edition/date;
- source used to verify current status;
- whether the full normative text was actually checked;
- unresolved interpretation or specialist review.

If any of these are missing, use `REFERENCE DOMAIN IDENTIFIED / COMPLIANCE NOT CLAIMED`.

## 3. ISO technical drawing anchor

Official ISO catalogue verification on 2026-08-17 supports these current anchor statements:

- `ISO 128-1:2020` remains published/current after systematic review and confirmation in 2026; it provides general rules for execution of 2D/3D technical drawings across mechanical engineering, construction, architecture and shipbuilding.
- `ISO 128-2:2022` is the published current basic-conventions-for-lines edition and replaces withdrawn `ISO 128-2:2020`.
- `ISO 128-3:2022` is the current published views/sections/cuts part listed by ISO/TC 10.
- `ISO 129-1:2018` remains published/current and has `Amd 1:2020`, but ISO also lists a new Edition 3 work item under development. Do not treat the future edition as published.

Official references:
- https://www.iso.org/standard/65296.html
- https://www.iso.org/standard/83355.html
- https://www.iso.org/standard/64007.html
- https://www.iso.org/standard/89306.html
- https://www.iso.org/cms/live/live/en/sites/isoorg/contents/data/committee/04/59/45986/x/catalogue/

The skill may use these scopes as convention anchors but must not reproduce or paraphrase unverified normative requirements beyond what the official public scope supports.

## 4. ASME product-definition/GD&T anchor

ASME's official product page lists `Y14.5-2018 (R2024)` as the dimensioning-and-tolerancing standard and describes it as establishing symbols, rules, definitions, requirements, defaults and recommended practices for GD&T/product definition.

Official reference:
- https://www.asme.org/codes-standards/find-codes-standards/y14-5-dimensioning-tolerancing/2018

Use only when the project/manufacturing authority adopts ASME Y14.5. Do not mix ASME and ISO GPS/GD&T conventions casually inside one controlled drawing set.

## 5. China standards routing

For PRC work, determine whether the requirement is:

- a GB/GB-T national standard handled through national standard systems;
- an engineering-construction standard under the responsible ministry/authority;
- a local standard;
- an industry standard;
- a project/client standard.

The official National Standard Full-text Disclosure system (`openstd.samr.gov.cn`) states that its general library does **not** include food safety, environmental protection or engineering-construction national standards and directs users to the relevant ministries. Therefore absence from that database does not prove that an engineering-construction standard does not exist or is not current.

Official discovery entry:
- https://openstd.samr.gov.cn/

For engineering-construction standards, verify through the responsible ministry/official engineering-construction standard publication route rather than relying only on the SAMR general database.

## 6. Manufacturer/system data

When a drawing uses a proprietary fixing, fastener, anchor, profile, hardware, coating or assembly:

- identify exact product/system/family;
- confirm current datasheet revision;
- separate manufacturer permitted range from project-selected value;
- do not copy one manufacturer's detail onto a different system without proof of equivalence;
- record required substrate/process/environment assumptions;
- preserve `CANDIDATE` status until the system is selected/approved.

## 7. Precedent boundary

Built precedent may support:
- assembly family;
- visual hierarchy;
- maintenance concept;
- material transition strategy;
- plausible dimension range when context is comparable.

It may not independently establish:
- code compliance for the current project;
- exact member/anchor/foundation size;
- site substrate condition;
- manufacturing tolerance;
- performance certification.

## 8. Compliance claim gate

Before writing words such as `COMPLIES`, `CODE-COMPLIANT`, `MEETS STANDARD`, `FOR FABRICATION`, `FOR CONSTRUCTION`, confirm:

1. correct jurisdiction;
2. current standard/edition;
3. applicable scope;
4. full required clause/requirement checked;
5. input geometry/data is authoritative enough;
6. specialist/authority review completed when required;
7. no open field condition invalidates the claim.

Otherwise use bounded language such as:

- `REFERENCE BASIS`
- `DESIGN TARGET`
- `TO BE VERIFIED`
- `ENGINEERING REVIEW REQUIRED`
- `FIELD VERIFY`
- `NOT FOR CONSTRUCTION`.

## 9. Standards change discipline

Do not hardcode 'latest' forever. A standards reference is a dated snapshot. When a drawing task is compliance-sensitive, re-check official status at execution time.

`STANDARD FOUND ≠ APPLICABLE ≠ FULL TEXT CHECKED ≠ COMPLIANT`.