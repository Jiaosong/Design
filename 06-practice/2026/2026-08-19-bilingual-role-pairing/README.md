# 2026-08-19｜UI Typography / L5｜Bilingual Role Pairing

Status: **TRAINING EXECUTED / PRODUCER KEEP-FOR-TRAINING CANDIDATE / INDEPENDENT DESIGN REVIEW HOLD / NO_PROMOTION**

## Project trigger

C04 `Visual Reading System v1.0` currently freezes typography by role — Functional Sans, Reading Text, Display/Chapter, Numeric/Meta — and explicitly requires mixed-language hierarchy review, but it does not define how Chinese and English should pair inside the same semantic role.

Recent training already covered Typographic Density Recomposition, Responsive Media Art Direction, Scene-Anchored UI Depth, Icon Optical Normalization, Brand↔Operational State color, Evidence-State surfaces, Prompt↔Media binding, Small-Multiple Comparability and World-Viewport Framing. This round therefore targets mixed-script role pairing rather than responsive density, media crop, icon, color, evidence-state or motion.

External calibration used only where internal evidence was incomplete:
- W3C CLReq confirms modern Chinese composition should use proportional Latin/numerals rather than fake fullwidth ASCII; mixed Chinese/Western text has explicit spacing and line-breaking behavior, including prohibition rules and bounded CJK–Latin spacing.
- These rules are used as typography-engine constraints, not as a source for C04 visual style.

## Existing Skill reused

`skills/oleander-ui-visual-composition/SKILL.md` v0.1.1 on PR #278.

Gap before this round:
- `Typography is structure` mentioned mixed-language hierarchy but had no repeatable pairing method;
- Typographic Density Recomposition protected information density, but did not prevent a translated English line from becoming a second hero;
- no explicit test for functional labels such as `RETURN`, `R06`, `12 min`, `NTS` being split or visually inflated;
- no authority boundary for Chinese-primary vs equal-language public-service contexts.

## Actual exercise

Editable 1920×1080 SVG compares two C04-inspired mobile compositions.

### REJECT
`Language-by-language duplication`
- Chinese and English each receive the same title scale/weight;
- supporting copy is duplicated at equal visual weight;
- bilingual button labels become long label blocks rather than clear controls;
- the English title becomes a second first-read hierarchy.

### KEEP candidate
`Role-paired typography`
- `CLAIM`: Chinese primary 31px / English semantic companion 14px;
- `SUPPORT`: Chinese 15px / English 12.5px;
- `ACTION`: Chinese 14px / English functional cue 9.5px;
- `META`: 11–13px;
- Latin remains proportional; no fake fullwidth Latin;
- action/state tokens remain short and stable;
- English retains semantic identity without duplicating Chinese visual weight.

Assets:
- `OLEANDER_BILINGUAL_ROLE_PAIRING_R01.svg`
- local PNG and 50% grayscale derivative rendered and reopened for visual readback.

## Design Crit

### Execution / compliance
**PASS FOR TRAINING EXECUTION**
- editable SVG;
- vector text;
- no generated imagery;
- synthetic landscape geometry only;
- no C04 field/service/GPS/accessibility truth claimed.

### Producer frozen-rubric
**KEEP-FOR-TRAINING CANDIDATE**

- First visual: PASS. KEEP reads one Chinese-primary claim, not two competing titles.
- Composition: PASS. The screen remains landscape + claim first; translation does not create an equal-weight second block.
- Proportion: PASS. Claim/support/action/meta pairs use visibly different role ratios.
- Hierarchy: PASS. `CLAIM > landscape > action > support > meta`; companion English remains semantically present but visually subordinate.
- Typography: PASS at the rendered training scale. Latin stays proportional; mixed-script hierarchy is legible.
- Material/spatial realism: schematic UI only; no site-photo claim.
- Scale: explicit training carrier logic only; final device typography/accessibility remains OPEN.
- Node/readability: `R06 · OBSERVE`, `REVEAL`, `RETURN`, `UNKNOWN · FIELD OPEN · NTS` remain compact and distinct.
- Interaction/narrative: actions remain controls rather than becoming bilingual text cards.
- Professional finish: training-level candidate, not a C04 production screen.

### Independent Professional Design Gate
**HOLD / REVIEW REQUIRED.**
No independently attributable professional reviewer is available in this run. Producer readback is not promoted to independent KEEP.

## Failure knowledge

1. `Same meaning ≠ same visual weight`.
2. Translation-by-duplication creates two competing hierarchy trees.
3. English all-caps or tracking can visually overpower a larger Chinese line despite smaller point size.
4. Bilingual actions can become paragraph-like labels; keep the control verb short and move explanatory translation elsewhere if needed.
5. Functional tokens (`R06`, `12 min`, `NTS`, `RETURN`) must not be broken into visually ambiguous fragments.
6. Fullwidth Latin/ASCII is not a legitimate alignment shortcut.
7. Reducing English until it is unreadable is not a valid hierarchy repair.
8. Chinese-primary hierarchy must not be mechanically applied to equal-language legal/public-service contexts.

## Repair method

`AUDIENCE AUTHORITY → SEMANTIC ROLE → LANGUAGE PRIORITY → PAIR SCALE/WEIGHT → MIXED-SCRIPT SPACING → LINE-BREAK LOCK → NATIVE READBACK → LANGUAGE-OFF TEST`

Required tests:
1. `CHINESE-OFF` — English alone still communicates the correct semantic role.
2. `ENGLISH-OFF` — Chinese alone still communicates the correct semantic role.
3. `PAIR-ON` — restoring both languages does not create a second first-read hierarchy.
4. `LINE-BREAK` — identifiers, quantities, units and action tokens do not split into misleading fragments.
5. `ALL-CAPS/TRACKING ATTACK` — Latin emphasis does not overpower the intended hierarchy.
6. `NARROW-WIDTH` — role pairing survives realistic line wrapping without global shrink.
7. `EQUAL-LANGUAGE AUTHORITY` — if project authority says languages are equal, do not demote either language; redesign the composition instead.

Promotion test:

> Remove either language in turn: semantic identity must survive; restore both and the companion language must not create a second first-read hierarchy.

## Skill delta

Updated existing `oleander-ui-visual-composition` v0.1.1 → v0.1.2 with a **Bilingual Role Pairing Gate**.

Added:
- Chinese/English semantic-role pairing instead of language-by-language duplicate hierarchies;
- explicit audience/language-authority decision before styling;
- proportional-Latin / mixed-script spacing discipline;
- protected functional tokens and line-break rules;
- language-off / pair-on / all-caps-tracking / narrow-width / equal-language-authority tests;
- hard failures for second-hero translations, unreadably demoted companion language, fake fullwidth Latin and authority-blind language demotion;
- review fields `LANGUAGE AUTHORITY`, `BILINGUAL ROLE PAIRS`, `MIXED-SCRIPT READBACK`.

## Cross-project transfer

Applicable to:
- C04 App / Web / route labels / reading prompts / exhibition captions;
- Baojiajie product pages and packaging UI;
- museum/travel companions;
- architecture/landscape boards with Chinese-primary bilingual captions;
- compact dashboards and product interfaces containing CJK + Latin identifiers.

Not directly applicable to:
- legally mandated equal-language public-service content;
- multilingual systems where neither language has primary authority;
- platform-native components governed by higher-authority localization rules;
- long-form translation products where both language bodies are intentionally parallel reading objects.

## Truth boundary

`TRAINING ONLY / CHINESE-PRIMARY CASE / VECTOR TEXT / NO IMAGE GENERATION / NOT C04 MAIN / FIELD OPEN / ACCESSIBILITY CERTIFICATION OPEN / INDEPENDENT DESIGN REVIEW HOLD / NO_PROMOTION`.
