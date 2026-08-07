# Website release gates

Status: DRAFT / NOT RELEASE READY  
Reviewed: 2026-08-07  
Scope: PR #7 website prototype

This record separates automated source/browser checks from human validation and rights authorization. A passing E1/E2 workflow does not authorize public release.

## E3 human validation

| Gate | Required evidence | Current state |
| --- | --- | --- |
| Screen reader | NVDA + Chrome/Firefox on Windows; VoiceOver + Safari on macOS/iOS; reading order, labels, errors, tabs and menu recorded | NOT RUN |
| 200% zoom and reflow | Real browser zoom at 200%; no clipped content, hidden controls or two-axis reading | NOT RUN |
| Touch and mobile | Physical phone/tablet; menu, tabs, sliders, project navigation and five-step form | NOT RUN |
| Keyboard | Full visible focus sequence, no traps, horizontal contact steps reachable | PARTIAL / automated only |
| Visual reading rhythm | Home Identity → Question → Relations → Evidence → Projects → Practice → About → Contact reviewed at target sizes | NOT RUN |
| Fonts | Actual Windows/macOS/iOS/Android fallback rendering and CJK glyph consistency | NOT RUN |
| Form delivery and privacy | Real endpoint owner, retention, access, deletion, consent and privacy text | NOT IMPLEMENTED; static simulation only |
| Content governance | Governance version, case status and evidence labels checked against current canonical source | PARTIAL |
| Rollback | Release commit, asset manifest and rollback owner recorded | NOT RECORDED |

## Rights and provenance

No repository record was found that closes source, creator, participant/model, property, trademark/product, modification/AI, publication-channel, term, territory, withdrawal and release approval for the following assets. Until an authorized record is attached, every item remains below E4 and blocked from public release.

| Asset | Evidence state | Missing record | Release |
| --- | --- | --- | --- |
| `assets/daylily/hero.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/daylily/site.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/daylily/market.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/daylily/imagination.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/daylily/positioning.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/daylily/principles.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/daylily/logo.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/daylily/symbol.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/daylily/palette.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/daylily/material.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/daylily/touchpoint.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/daylily/signage.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/daylily/environment.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/reno-cmf/hero.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/reno-cmf/finalseries.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/reno-cmf/lineup.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/reno-cmf/trend.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/reno-cmf/concept.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/reno-cmf/light.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/reno-cmf/reflection.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/reno-cmf/colorlogic.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/reno-cmf/palette.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/reno-cmf/palettewarm.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/reno-cmf/palettecool.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/reno-cmf/process.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/reno-cmf/material.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/reno-cmf/finalsilver.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |
| `assets/reno-cmf/portrait-safe.jpg` | UNKNOWN / below E4 | Source, creator, subject/property authorization, permitted channels, term, territory, modification/AI status, withdrawal contact and release decision are not recorded in the repository. | BLOCKED |

## Required disposition

- Daylily participant, space, market and brand-development imagery: verify creator/source, depicted people and places, project authorization, permitted publication and withdrawal.
- Reno product/CMF imagery and commercial information: verify creator/source, product/trademark context, whether imagery is portfolio concept material, permitted publication and non-endorsement wording.
- `portrait-safe.jpg`: verify the depicted person, photographer/source, portrait authorization, editing/AI status, channel scope and withdrawal route.
- If any item cannot reach E4, replace it with an authorized asset or remove it before release.
- Generated or composited imagery may illustrate a proposal only; it cannot prove implementation, commission, adoption, production, participation or impact.

## Release rule

PR #7 remains Draft until:

1. E2 completes successfully on the current head SHA.
2. Every E3 line above has an accountable reviewer, date, device/browser and result.
3. Every referenced asset has an E4 rights/provenance record or is removed/replaced.
4. The real contact mechanism and privacy handling are implemented and reviewed.
5. Governance version and case boundaries are synchronized immediately before release.
