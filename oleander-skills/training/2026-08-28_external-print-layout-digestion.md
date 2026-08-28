# External Skill Digestion — SkillMedev/skills/print-layout

Date: 2026-08-28
Status: `EXTERNAL REFERENCE DIGESTION / KNOWLEDGE EVIDENCE`
License observed: MIT

## Scope read

Reviewed external `skills/print-layout/SKILL.md` and repository license state.

## Material delta accepted

1. commercial-print preparation should begin from the actual printer/process specification, not a universal prepress preset;
2. editable design master, production/prepress master, press-ready derivative, soft proof, hard proof and printed run are separate proof/authority classes;
3. raster quality must be judged at effective placed size and intended viewing/process condition;
4. overprint/knockout, total area coverage, spot/separation behavior and output intent belong to prepress validation rather than generic visual QA;
5. a named PDF/X preset is not proof that the actual exported file conforms;
6. print geometry should verify trim/bleed/safe/page boxes and should not create bleed by scaling finished artwork;
7. color-critical/finish-critical work needs an explicit proof plan; screen preview cannot prove substrate/ink/registration/finishing;
8. packaging/POP dielines and finishing geometry remain upstream technical authority and cannot be redrawn for presentation convenience.

## Existing-first mapping

- `oleander-visual-design` remains visual-layout/design owner.
- `oleander-delivery-qc` remains release/preflight owner and now receives `PRINT_PRODUCTION_PREFLIGHT_EXTENSION.md`.
- Technical Drawing/vendor/manufacturer authority remains responsible for production geometry/engineering where required.
- No separate Print Core Skill is created.

## Rejected / not imported as defaults

The external Skill's example values for bleed, safe area, DPI, rich black, type size, rule weight, ink limit, ICC profile and PDF/X flavor are not adopted as universal OLEANDER defaults. They remain process-dependent and must defer to the current printer/vendor specification.

No external checklist text or production preset is treated as certification evidence merely because it exists.

## Maturity

Candidate extension only. Requires real print-job specification, actual exported-file preflight and proof/production evidence for stronger claims.